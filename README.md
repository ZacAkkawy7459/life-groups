# Life Groups

A single-page web app hosting eight Salvation Army small-group "streams" behind one
group picker. Everyone opens one link, chooses their group, says whether they're leading
or joining, picks the session, and works through seven tabs.

**Nothing leaves the device.** No server, no accounts, no email — everything typed is
held in that person's own browser (`localStorage`), isolated per group. The only things
that ever leave a laptop are the text a person copies into the group chat and the PDF
they export.

## Groups

Marriage Life Group · Preparing for Marriage · Parents of Young Children · Parents of
Teens & Young Adults · Blended Families · Caring for Ageing Parents · Money & Generosity
· Grief & Loss.

## Run it locally

```bash
python -m http.server 8767
```
Then open <http://localhost:8767>.

## Editing content

All session wording lives in the specs under `tools/<group>-sessions.md`. To change it,
edit the spec, then rebuild:

```bash
python tools/build-streams.py                       # parse specs -> streams/*.js
python tools/fetch-passages.py --key YOUR_NLT_KEY   # bake scripture (one or --stream x)
```

The marriage stream reuses already-baked data and is not re-parsed. Scripture is New
Living Translation, baked in at build time; the API key is never committed and never
ships to the browser.

## Deploy

Static GitHub Pages from `main` / root. See **HANDOFF.md** for full architecture, the
config schema, the build pipeline, deployment steps, and the list of things a future
session could continue.

Scripture quotations are taken from the Holy Bible, New Living Translation, copyright
© 1996, 2004, 2015 by Tyndale House Foundation. Used by permission of Tyndale House
Publishers. All rights reserved.
