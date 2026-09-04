#!/usr/bin/env python3
"""
build-streams.py — Life Groups content build step.

Parses each stream's *-sessions.md spec into a streams/<id>.js data file
(session prose only; scripture text is baked separately by fetch-passages.py)
and writes tools/passages-manifest.json listing every passage to fetch.

The marriage stream is NOT parsed here — it reuses the already-baked data in
streams/marriage.js. Run this, then run fetch-passages.py.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# stream id -> spec filename
STREAMS = {
    "premarital":    "premarital-sessions.md",
    "parents-young": "parents-young-children-sessions.md",
    "parents-teens": "parents-teens-sessions.md",
    "blended":       "blended-families-sessions.md",
    "carers":        "carers-ageing-parents-sessions.md",
    "money":         "money-generosity-sessions.md",
    "grief":         "grief-loss-sessions.md",
}

TRAIL_FIELDS = ["Share", "Commitment", "Carry", "Notice", "Action", "Closing", "Day 14"]
FIELD_KEY = {"Share": "share", "Commitment": "commitment", "Carry": "carry",
             "Notice": "notice", "Action": "action", "Closing": "closing", "Day 14": "day14"}


def slug(ref):
    s = ref.lower().replace("–", "-").replace("—", "-")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


# Compound references the API can't parse as written (non-contiguous verses).
API_OVERRIDE = {
    "Galatians 6:2 and 6:5": "Galatians 6:2; Galatians 6:5",
}


def api_ref(ref):
    # NLT API wants ascii hyphens for verse ranges; natural book names are fine.
    r = ref.replace("–", "-").replace("—", "-").strip()
    if r in API_OVERRIDE:
        return API_OVERRIDE[r]
    r = re.sub(r",\s+", ",", r)   # "Psalm 88:1-2, 18" -> "Psalm 88:1-2,18"
    return r


def split_sessions(md):
    # Session headers look like: ### 1 — Title   (em dash or hyphen)
    parts = re.split(r"(?m)^###\s+(\d+)\s+[—-]\s+(.+?)\s*$", md)
    # parts = [pre, n, title, body, n, title, body, ...]
    out = []
    for i in range(1, len(parts), 3):
        n = int(parts[i]); title = parts[i + 1].strip(); body = parts[i + 2]
        out.append((n, title, body))
    return out


def grab_line(body, label):
    m = re.search(r"(?m)^\*\*" + re.escape(label) + r":\*\*\s*(.+?)\s*$", body)
    return m.group(1).strip() if m else None


def numbered_items(chunk):
    # pull "1. ...", "2. ..." items (single-line each in these specs)
    items = re.findall(r"(?m)^\s*\d+\.\s+(.+?)\s*$", chunk)
    return [x.strip() for x in items]


def parse_beats(body):
    m = re.search(r"(?m)^\*\*Beats\*\*\s*\n(.*?)(?=\n\*\*Questions\*\*)", body, re.S)
    if not m:
        return [], None
    items = numbered_items(m.group(1))
    beats, landing = [], None
    for it in items:
        lm = re.match(r"^\*\*Landing:\*\*\s*(.+)$", it)
        if lm:
            landing = lm.group(1).strip()
        else:
            beats.append(it)
    return beats, landing


def parse_questions(body):
    # from **Questions** up to the first trailing field marker
    stop = r"(?=\n\*\*(?:" + "|".join(re.escape(f) for f in TRAIL_FIELDS) + r"):\*\*)"
    m = re.search(r"(?m)^\*\*Questions\*\*.*?\n(.*?)" + stop, body, re.S)
    chunk = m.group(1) if m else ""
    return numbered_items(chunk)


def parse_note(body):
    # blockquote leader/mentor note: > **Leader note...:** text (may span > lines)
    m = re.search(r"(?m)^>\s*\*\*(Leader note|Mentor note)[^:]*:\*\*\s*(.*(?:\n>.*)*)", body)
    if not m:
        return None, None
    kind = "mentorNote" if m.group(1).startswith("Mentor") else "leaderNote"
    text = re.sub(r"(?m)^>\s?", "", m.group(2)).replace("\n", " ").strip()
    text = re.sub(r"\s+", " ", text)
    return kind, text


def parse_stream(sid, md):
    sessions, manifest = [], []
    for n, title, body in split_sessions(md):
        premise = grab_line(body, "Premise")
        scrip_line = grab_line(body, "Scripture") or ""
        refs = [r.strip() for r in scrip_line.split(";") if r.strip()]
        scripture_ids = []
        for r in refs:
            pid = f"{sid}-s{n}-{slug(r)}"
            scripture_ids.append(pid)
            manifest.append({"id": pid, "ref": api_ref(r), "label": r})
        beats, landing = parse_beats(body)
        questions = parse_questions(body)
        sess = {"n": n, "title": title, "premise": premise,
                "scripture": scripture_ids, "beats": beats, "landing": landing,
                "questions": questions}
        for label in TRAIL_FIELDS:
            v = grab_line(body, label)
            if v is not None:
                sess[FIELD_KEY[label]] = v
        kind, note = parse_note(body)
        if note:
            sess[kind] = note
        sessions.append(sess)
    return sessions, manifest


def write_stream_file(sid, sessions):
    body = json.dumps(sessions, ensure_ascii=False, indent=2)
    js = (
        "/* Life Groups — '" + sid + "' stream data.\n"
        " * Session prose parsed from tools/" + STREAMS[sid] + " by tools/build-streams.py.\n"
        " * Scripture is baked into the PASSAGES block below by tools/fetch-passages.py —\n"
        " * do not hand-edit that block (highlight offsets depend on it).\n"
        " */\n"
        "(function () {\n"
        "  /* ===== PASSAGES:GENERATED:START — run tools/fetch-passages.py ===== */\n"
        "  const PASSAGES = {};\n"
        "  /* ===== PASSAGES:GENERATED:END ===== */\n"
        "  const SESSIONS = " + body + ";\n"
        "  window.LG = window.LG || { groups: [], streams: {} };\n"
        "  window.LG.streams[\"" + sid + "\"] = { sessions: SESSIONS, passages: PASSAGES };\n"
        "})();\n"
    )
    path = os.path.join(ROOT, "streams", sid + ".js")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(js)
    return path


def main():
    all_manifest = {}
    summary = []
    for sid, fname in STREAMS.items():
        md = open(os.path.join(HERE, fname), encoding="utf-8").read()
        sessions, manifest = parse_stream(sid, md)
        write_stream_file(sid, sessions)
        all_manifest[sid] = manifest
        summary.append((sid, len(sessions), len(manifest)))
    with open(os.path.join(HERE, "passages-manifest.json"), "w", encoding="utf-8") as f:
        json.dump(all_manifest, f, ensure_ascii=False, indent=2)
    print("stream            sessions  passages")
    total = 0
    for sid, ns, nm in summary:
        print(f"  {sid:15s} {ns:5d} {nm:9d}")
        total += nm
    print(f"  {'TOTAL passages to fetch':22s} {total}")


if __name__ == "__main__":
    main()
