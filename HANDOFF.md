# Life Groups — Developer Handoff

**For:** the next Claude Code session (or developer) picking this app up.
**Owner:** Zac. **What this is:** one static web app, **Life Groups**, hosting eight
Salvation Army small-group "streams" behind a group picker. Built by duplicating and
generalising the standalone Marriage Life Group app.

Read this end-to-end before changing anything. The app is small, static, and
config-driven — almost all behaviour differences between groups are data, not code.

---

## 1. Status

- **Built and tested locally. Not yet deployed** (as of this handoff). Intended target:
  a **new** public GitHub Pages repo `life-groups`; the standalone marriage app stays
  live and untouched at `zacakkawy7459.github.io/marriage-life-group`.
- All **8 streams** load; all **7 tabs** render for every stream; scripture is **baked**
  (170 passages / 461 verses; 0 offset issues). Verified in-browser via DOM-state checks:
  group selector, the two structural variants (grief, premarital), highlighting, PDF,
  compare round-trip, refresh-skip, change-group.
- The folder is a git repo with one commit; it has **not** been pushed.

## 2. How to run and test locally

```bash
cd life-groups
python -m http.server 8767      # then open http://localhost:8767
```

Testing notes learned the hard way:
- **Check DOM state, not screenshots.** A backgrounded/automation browser tab freezes
  compositing and CSS transitions, so screenshots and computed transition colours lie.
  `document.getElementById(...).hidden`, `getComputedStyle(el).display`, and reading
  `innerHTML`/`textContent` are reliable; a mid-transition `borderColor` is not.
- **Compile-check the inline script** before trusting a load: fetch `index.html`, pull
  the last `<script>` body, `new Function(body)`. The #1 bug class here is a
  **double-quoted JS string containing an unescaped `"`** (e.g. `"<div class="x">"`) —
  use single quotes for HTML fragments that contain attributes.
- The **console buffer is cumulative across reloads** — an error there may be stale;
  re-verify against a fresh compile-check.

## 3. Architecture

Static site, no build step at runtime, no framework, no bundler. `index.html` holds the
whole engine inline. Everything group-specific is data:

```
index.html        The engine: gate (group→role→session), 7 tabs, highlighter,
                  timer, share/compare, PDF. Reads the active group's config +
                  stream data. ~700 lines of inline JS.
styles.css        Design system (Salvo navy/red/gold, Newsreader/Inter) + print
                  stylesheet + Life Groups additions (selector, rules, standing
                  notes, agreement dial, compare view).
groups.js         window.LG.groups — the config registry (one object per stream).
                  window.LG.attribution — the global NLT permission line.
streams/<id>.js   window.LG.streams[id] = { sessions, passages }. Session prose +
                  the baked NLT PASSAGES block (offsets frozen — do not hand-edit).
sw.js             Network-first service worker (offline once loaded). Bump CACHE +
                  the CORE list when files change.
tools/            Build pipeline + the source specs (see §5).
```

Load order in `index.html`: `groups.js`, then each `streams/*.js`. Each stream file
registers itself onto `window.LG.streams`.

### Data model

`state = { group, stream, n, tab, data, tabs, pendingRole }`. Per-device storage,
namespaced by group:

```
lg.v1.<group>.session.<n>   the person's work for that session (answers, highlights,
                            commitment/carry/action, comparisons, notes, role, ...)
lg.v1.<group>.meta          { lastSession }
lg.v1.<group>.timer.<n>     { endAt }   couple/personal-time countdown
lg.v1.meta                  { lastGroup }
```

Groups are fully isolated. Nothing leaves the device except copied text and exported
PDFs — the load-bearing privacy claim, stated on the gate and footer.

## 4. The group config schema (`groups.js`)

Each group object drives the engine. Fields actually consumed today:

| Field | Meaning |
|---|---|
| `id`, `title`, `blurb` | identity + one-line selector descriptor |
| `sessionCount` | 12 (or 8 for premarital) |
| `sessionMinutes`, `countdownMinutes` | run length + couple/personal-time timer default |
| `runSheet` | `[{time, block}]`, shown on Start (leader) + leader PDF |
| `howItRuns`, `dropOffLabel` | Start-tab blurb; label for the drop-off block/timer |
| `gateVariant` | `"role"` (default) or `"threeway"` (premarital) + `gateRoles`, `gatePrompt` |
| `commitmentModel` | `"commitment"` \| `"carry"` (grief) \| `"action"` (premarital) \| `"none"` |
| `commitmentLabel`, `commitmentIntro` | tab title + line above the card |
| `day14Model` | `"perSession"` \| `"fixedLine"` (grief) \| `"none"` (premarital) + `day14FixedLine` |
| `shareModel` | `"groupChat"` (default) \| `"compare"` (premarital) |
| `shareStandingLine` | money: "No numbers. Ever." pinned above the copy box |
| `shareOptionalAlways` | grief: soften share nudges, default toggles off |
| `gateNote` | confidentiality frame — gate + "say this aloud" leader block |
| `startTabNote` | Start-tab note (carers drop-in, grief timing) |
| `sessionRules` | shown at the top of **every** tab, both views (grief's four rules) |
| `standingNote` | support/disclaimer — gate note + leader Start/Message/Close + PDF back page |
| `watchForNote` | grief leader-only safeguard block |
| `pauseRule` | premarital mentor-view persistent block |
| `questionVariants` | blended (informational; `*(Birth parent)*` renders via italics) |
| `whereWasI` | parents-young flag (see TODO — not yet wired) |
| `attendees` | Share-tab "others" prefill (marriage = the four couples) |
| `yearExportLabel` | final-session export label ("Export the course" for premarital) |
| `session1Rhythm`, `leaderTip` | marriage session-1 leader announcements |

**All safety/disclaimer text is verbatim from the specs — never paraphrase it.**

## 5. The content build pipeline (`tools/`)

Session prose is **parsed from the specs**, not hand-typed. Scripture is **baked** from
Tyndale's NLT API.

1. `tools/*-sessions.md` — the eight source specs (the content bank + per-stream
   differences). These are the source of truth for wording.
2. `tools/build-streams.py` — parses the seven non-marriage specs into
   `streams/<id>.js` (session prose + empty PASSAGES block) and writes
   `tools/passages-manifest.json` (every passage id → API ref + display label).
   **Marriage is not parsed** — `streams/marriage.js` reuses the standalone app's
   already-baked data verbatim.
   ⚠️ Re-running this **overwrites** the stream files, wiping baked PASSAGES. After
   re-running, re-bake (step 3).
3. `tools/fetch-passages.py --key <KEY> [--stream a,b]` — reads the manifest, fetches
   NLT text, and injects the PASSAGES block into each `streams/<id>.js`. Idempotent per
   stream; safe to run one or a few streams at a time.

**Parser assumptions** (keep specs in this shape or the parser needs updating):
`### N — Title`; `**Premise:**`, `**Scripture:**` (refs `;`-separated); `**Beats**`
then `1.`–`4.` with the 4th `**Landing:** …`; `**Questions**` then `1.`–`n.`; trailing
`**Share:** / **Commitment:** / **Carry:** / **Notice:** / **Action:** / **Closing:** /
**Day 14:**`; optional `> **Leader note:** / **Mentor note:**`.

**NLT API / key.** Free non-commercial key from api.nlt.to (Zac holds it; ask him — it
is **never** committed and never ships to the browser; `.gitignore` covers key files).
`--key TEST` works anonymously (50 verses/request, 500/day). Two references needed a
manual override for non-contiguous verses (`API_OVERRIDE` in build-streams.py: e.g.
"Galatians 6:2 and 6:5" → "Galatians 6:2; Galatians 6:5"). The parser strips footnotes,
chapter numbers and subheads, keeps poetry line breaks, and stores `{ref,label,verses:
[{vn,start,end}],plain}` with frozen highlight offsets.

## 6. Structural variants worth understanding

- **grief** — `commitmentModel:"carry"` (a "Something to carry" field, no check-up),
  `day14Model:"fixedLine"`, `sessionRules` (four rules shown every tab, both views),
  `standingNote` (support lines on gate + leader views + PDF), `startTabNote` (timing),
  `watchForNote`, `shareOptionalAlways`. 60-min / 15-min timer.
- **premarital** — `gateVariant:"threeway"` (Getting married / Mentoring; "Mentoring"
  counts as leader/facilitator), 8 sessions, `commitmentModel:"action"`,
  `day14Model:"none"`, `shareModel:"compare"`, `pauseRule`. The **Compare** tab: each
  partner answers privately + sets an agreement dial per question (Questions tab), then
  "Copy my answers" produces a plain-text block (`Q1 [close] …`), the partner pastes it,
  and it renders side by side with a shared "what we noticed" field. Round-trip verified.

## 7. How to continue / extend

- **Edit wording:** change the spec in `tools/<id>-sessions.md`, re-run
  `build-streams.py`, re-bake that stream. (Or edit `streams/<id>.js` `SESSIONS`
  directly — but avoid touching the PASSAGES block.)
- **Add a new group:** drop a spec in `tools/`, add it to `STREAMS` in
  `build-streams.py`, run it, bake it, add a config object to `groups.js`, and add the
  `<script src>` line in `index.html` + the path in `sw.js` CORE.
- **Add a config knob:** add the field in `groups.js`, read it in the relevant `RENDER.*`
  function in `index.html`, and (if visual) add CSS.

## 8. Known gaps / TODO (good next-session work)

- **`whereWasI` (parents-young)** is declared in config but **not yet wired**. Intended:
  a "Where was I?" control returning to the last-touched question; the countdown already
  survives tab blur (it's wall-clock `endAt`-driven), so only the jump control is left.
- **Compare copy format is plain-text and brittle** to manual edits (`Q1 [close] text`).
  Fine for copy-paste between partners; consider a more robust encoding if edited by hand.
- **Premarital mentor PDF** currently prints answers like any stream. The spec wants the
  mentor export to omit private answers (only agreement dials + shared notes). Not yet
  differentiated by role in `buildSessionPrint`.
- **Run sheets** for the 75-min non-marriage streams use a neutral shared table; tune per
  stream if desired.
- **No visual/pixel QA** was done (automation tab couldn't composite). Open it locally
  once and eyeball the selector, the gold Commitment/Carry stage, and the compare grid.
- **Selector uses plain text buttons** (no per-group glyphs) to stay on-palette; add
  restrained glyphs if wanted.

## 9. Deployment (not done yet)

New public repo `life-groups`, GitHub Pages from `main` / root — same as the marriage
app. From `life-groups/`:

```bash
git remote add origin https://github.com/<user>/life-groups.git
git push -u origin main
```

Then Settings → Pages → Deploy from a branch → `main` / root. The umbrella title is
**"Life Groups"**. Bump `CACHE` in `sw.js` on every subsequent deploy so the
network-first worker refreshes cleanly.
