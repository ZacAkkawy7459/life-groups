#!/usr/bin/env python3
"""
fetch-passages.py — Life Groups scripture build step.

Reads tools/passages-manifest.json (written by build-streams.py) and bakes the
NLT text for every passage into the matching streams/<id>.js PASSAGES block.

Why bake: the site works offline, no API key ships to the browser, no rate
limit mid-session, and the text never shifts under saved highlight offsets.

Usage:
  python tools/fetch-passages.py --key YOUR_KEY                 # bake every stream
  python tools/fetch-passages.py --key YOUR_KEY --stream grief  # one (or a,b,c)
  NLT_KEY=... python tools/fetch-passages.py                    # key via env

The marriage stream is NOT in the manifest — it reuses its already-baked data.
Free non-commercial key from https://api.nlt.to (or --key TEST for anon: 50
verses/request, 500 requests/day). Bake a couple of streams per run if limited.
"""
import argparse, json, os, re, sys, time
from html.parser import HTMLParser
from urllib.parse import quote
from urllib.request import urlopen, Request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
API = "https://api.nlt.to/api/passages"
START_MARK = "/* ===== PASSAGES:GENERATED:START"
END_MARK = "/* ===== PASSAGES:GENERATED:END"


class VerseParser(HTMLParser):
    """Clean verse text out of the API HTML. Drops footnotes (span.tn),
    footnote markers (a.a-tn), the printed verse number (span.vn), and any
    heading (chapter numbers h2.chapter-number, subheads h3.subhead). Inserts a
    newline before each poetic line so poetry keeps its shape."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.verses = []
        self.cur = None
        self.cur_vn = None
        self.stack = []

    def _skipping(self):
        return any(skip for _, skip in self.stack)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = set((a.get("class") or "").split())
        if tag == "verse_export":
            self.cur = []
            try:
                self.cur_vn = int(a.get("vn"))
            except (TypeError, ValueError):
                self.cur_vn = a.get("vn")
            self.stack.append((tag, False))
            return
        if tag == "p" and any(c.startswith("poet") for c in classes):
            if self.cur is not None and "".join(self.cur).strip():
                self.cur.append("\n")
        if tag == "br" and self.cur is not None and not self._skipping():
            self.cur.append("\n")
        skip = (
            (tag == "span" and ("tn" in classes or "vn" in classes))
            or (tag == "a" and "a-tn" in classes)
            or tag in ("h1", "h2", "h3", "h4", "h5", "h6")
        )
        self.stack.append((tag, skip))

    def handle_endtag(self, tag):
        while self.stack:
            t, _ = self.stack.pop()
            if t == tag:
                break
        if tag == "verse_export":
            self.verses.append({"vn": self.cur_vn, "text": "".join(self.cur or [])})
            self.cur = None
            self.cur_vn = None

    def handle_data(self, data):
        if self.cur is not None and not self._skipping():
            self.cur.append(data)


def normalize(text):
    text = text.replace("\r", "")
    text = re.sub(r"[ \t]*\n[ \t]*", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def fetch(ref, key, version="NLT"):
    url = f"{API}?ref={quote(ref)}&version={version}&key={quote(key)}"
    req = Request(url, headers={"User-Agent": "LifeGroups-build/1.0"})
    with urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def build_passage(ref, label, key):
    html = fetch(ref, key)
    if "bibletext" not in html:
        raise RuntimeError(f"{ref}: unexpected response — {html[:160]!r}")
    p = VerseParser()
    p.feed(html)
    if not p.verses:
        raise RuntimeError(f"{ref}: no verses parsed")
    plain_parts, verses, offset = [], [], 0
    kept = [v for v in p.verses if normalize(v["text"])]
    for i, v in enumerate(kept):
        t = normalize(v["text"])
        start = offset
        plain_parts.append(t)
        offset += len(t)
        verses.append({"vn": v["vn"], "start": start, "end": offset})
        if i < len(kept) - 1:
            plain_parts.append(" ")
            offset += 1
    plain = "".join(plain_parts).rstrip()
    for v in verses:
        v["end"] = min(v["end"], len(plain))
    return {"ref": ref, "label": label, "verses": verses, "plain": plain}


def render_block(passages):
    body = json.dumps(passages, ensure_ascii=False, indent=2)
    return (
        "/* ===== PASSAGES:GENERATED:START — run tools/fetch-passages.py ===== */\n"
        "  const PASSAGES = " + body + ";\n"
        "  /* ===== PASSAGES:GENERATED:END ===== */"
    )


def inject(path, block):
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    s = src.find(START_MARK)
    e = src.find(END_MARK)
    if s == -1 or e == -1:
        raise RuntimeError("markers not found in " + path)
    e = src.find("*/", e) + 2
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(src[:s] + block + src[e:])


def bake_stream(sid, entries, key):
    passages = {}
    for j, ent in enumerate(entries):
        pid, ref, label = ent["id"], ent["ref"], ent["label"]
        for attempt in range(4):
            try:
                passages[pid] = build_passage(ref, label, key)
                sys.stderr.write(f"    ok  {ref}\n")
                break
            except Exception as ex:  # noqa: BLE001
                if attempt == 3:
                    raise RuntimeError(f"{sid}/{pid} ({ref}) failed: {ex}")
                time.sleep(2.0)
        time.sleep(0.25)
    block = render_block(passages)
    inject(os.path.join(ROOT, "streams", sid + ".js"), block)
    return len(passages)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", default=os.environ.get("NLT_KEY", "TEST"))
    ap.add_argument("--stream", default=None, help="comma-separated stream ids")
    args = ap.parse_args()
    manifest = json.load(open(os.path.join(HERE, "passages-manifest.json"), encoding="utf-8"))
    want = set(args.stream.split(",")) if args.stream else None
    total = 0
    for sid, entries in manifest.items():
        if want and sid not in want:
            continue
        sys.stderr.write(f"== {sid} ({len(entries)} passages)\n")
        n = bake_stream(sid, entries, args.key)
        total += n
        sys.stderr.write(f"   baked {n} into streams/{sid}.js\n")
    sys.stderr.write(f"\nDone. {total} passages baked.\n")


if __name__ == "__main__":
    main()
