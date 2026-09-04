# Marriage Life Group — Session Site + 12-Session Bank

**For:** Claude Code
**Owner:** Zac
**Group:** Marriage Life Group — Salvation Army outreach. First Monday of the month, run over Facebook video chat. Everyone is on a laptop.

**Site title:** *Marriage Life Group.* Use this on the opening gate, the browser tab, the PDF cover, and the repo name. Nowhere should it read "Young Marrieds".

---

## Part 1 — What to build

A single-page website. One link, shared into the group chat. Everyone opens it on their own laptop while the video call runs, says whether they're leading or joining, picks the session for that month, and works through seven tabs.

**No server. No accounts. No email. Nothing leaves the device.** Everything typed is held in `localStorage` in that person's own browser. Four people opening the same link get four completely separate, private sessions that happen to look identical. Nobody sees anybody else's typing.

Say this plainly on the opening screen. It's the load-bearing claim of the whole design — people will only be honest if they believe it, and it happens to be exactly true.

Two things ever leave a device, and only because the person chose:
- text they copy into the group chat from the **Share** tab
- the PDF they export at the end

### Hosting

Build as `index.html` + `sessions.js` + `styles.css`. Deploy to **GitHub Pages**. Set up the repo and the Pages deploy as part of this build and hand Zac the link. He'll want to edit session wording later, so the README must cover how to change `sessions.js` and redeploy.

### Opening gate — first thing on load

Before anything else, a full-screen question:

> **Are you leading tonight, or joining in?**
> [ I'm leading ] [ I'm joining in ]

Calm, centred, generously spaced — it sets the tone for the whole site. Underneath, one quiet line: *Nothing you type here leaves this laptop.*

The answer sets the view for the session:

**Leader view** gets everything a participant gets, plus:
- the full four message beats with delivery notes on the Message tab
- leader notes where a session has them (sessions 3, 10 and 11 do)
- the run sheet with timings
- the "what to say before everyone drops off" script
- the day-14 check-in message generator on the Close tab

**Participant view** gets:
- the session premise and the landing line on the Message tab
- the full beats behind a collapsed *Tonight's notes* disclosure, closed by default, so the natural behaviour is listening rather than reading ahead
- everything else identical

**Ask this per session, not once ever.** Leadership rotates — Zac won't always be the one running it. Store the answer against that session so a mid-session refresh doesn't re-ask, and put a small, unobtrusive switch in the footer so somebody who picked wrong can change without losing anything.

### Persistence

`localStorage`, keyed per session. Suggested schema:

```js
mlg.v1.session.<n> = {
  role: "leader" | "participant",
  name: "",
  date: "",
  highlights: { "<passageId>": [ { start, end } ] },
  scriptureNotes: { "<passageId>": "" },
  answers: [ { text: "", share: false } ],   // ×4
  commitment: { what: "", howOften: "", howWeKnow: "", share: true },
  othersCommitments: [ { who: "", what: "" } ],
  lastMonthOutcome: "",
  notes: ""
}
mlg.v1.meta = { lastSession }
```

Keying per session means next month starts clean without wiping last month, highlights from March are still there in November, and by session 12 the browser holds the whole year — which is what makes the year-end export possible.

Include a visible **Start this session fresh** control, and **Clear everything** behind a confirm.

### Bible text — NLT

Fetch the passages **once, at build time**, from Tyndale's NLT API at `api.nlt.to`, and bake the text into `sessions.js`.

Do not fetch live and do not generate the text from memory. Baking it in means the site works with no internet, no API key ships to the browser, there's no rate limit to hit mid-session, and — critically — the text never shifts underneath saved highlight offsets.

Get a free key at api.nlt.to. Free tier is non-commercial, which this is.

**Passages to fetch:**

| Session | References |
|---|---|
| 1 | Ephesians 5:25–33; Revelation 2:4 |
| 2 | Ephesians 4:29; James 3:3–5 |
| 3 | 1 Timothy 6:6–10; Matthew 6:21 |
| 4 | Ephesians 4:26–27; Matthew 5:23–24 |
| 5 | Colossians 3:13; Matthew 18:21–35 |
| 6 | Mark 6:31; Genesis 2:2–3 |
| 7 | John 13:3–15; Philippians 2:3–4 |
| 8 | Matthew 18:19–20; Colossians 3:16 |
| 9 | Genesis 2:24; Exodus 20:12 |
| 10 | Song of Songs 2:10–13; Proverbs 5:18–19 |
| 11 | Ecclesiastes 3:1–8; Romans 5:3–5; 2 Corinthians 1:3–4 |
| 12 | Joshua 24:15; Matthew 5:14–16 |

Roughly 86 verses total, across a site that is overwhelmingly original writing. Well inside Tyndale's terms.

**Attribution — required.** Put `NLT` at the end of each passage on screen, and this line in the site footer and on the PDF back page:

> Scripture quotations are taken from the Holy Bible, New Living Translation, copyright © 1996, 2004, 2015 by Tyndale House Foundation. Used by permission of Tyndale House Publishers, Carol Stream, Illinois 60188. All rights reserved.

Store each passage with a stable `passageId` (e.g. `s1-eph-5-25-33`) and both a rendered form with verse numbers and a normalised plain-text form for highlight offsets.

### The tabs

Seven. On a laptop the strip fits across the top with full labels — no scrolling, no hamburger. Add a large **Next** button at the foot of every tab, and left/right arrow-key navigation, since people will be typing anyway.

| # | Tab | Contents |
|---|---|---|
| 1 | **Start** | Session picker (all 12), then that session's title, premise, how the night runs, name field, and last month's commitment with a *how did it go?* field |
| 2 | **Scripture** | The NLT passages — highlightable, with a personal notes box |
| 3 | **Message** | Four beats and the landing line. Full for leaders, collapsed for participants. |
| 4 | **Questions** | Four questions, one per screen, with the couple-time countdown |
| 5 | **Commitment** | The commitment card |
| 6 | **Share** | Builds the group-chat message; records everyone else's commitments |
| 7 | **Close** | Closing words, the day-14 heads-up, **Export PDF** |

The Start tab stays reachable throughout so someone arriving late can jump straight in.

### Tab 2 — Scripture, highlighting and notes

The passages are set larger than anything else on the site, with hanging quote marks and plenty of air.

**Highlighting.** Select any text within a passage and a small popover appears with a single **Highlight** action and, on already-highlighted text, **Remove**. One colour only — the gold — because three colours invites a taxonomy nobody maintains.

Store as character offsets `{ start, end }` against the passage's normalised plain text. Because the text is baked in at build time, those offsets stay valid forever. Merge overlapping ranges on save. Re-render by splitting the passage into marked and unmarked runs.

Highlights persist across months. Someone who highlighted a line in March sees it still marked in November, and it prints into every PDF export of that session.

**Notes.** Under each passage, a text area labelled plainly:

> **What stood out to you?**
> Optional. Nobody sees this but you.

Autosave, same as everywhere else.

### Tab 4 — Questions and the countdown

One question per screen. Large question in the reading face, generous text area beneath, Back / Next, quiet progress indicator. Autosave on every keystroke, debounced.

Each answer carries a small toggle: *include this in what I share.* **Off by default.**

**The countdown.** A 22-minute timer, started by the person, sitting quietly at the top of the tab. Not a klaxon — a calm readout that turns amber at five minutes and red at one.

This exists because Messenger has no breakout rooms. Everyone hangs up for couple time and rejoins at a stated minute, and once the call is empty there is nobody left to call time. This timer is the single most useful thing on the site.

### Tab 5 — Commitment

Visually distinct from everything else — this is what the whole night is aimed at. Gold ground, three fields:

- **Our commitment this month** — one concrete habit, not a sentiment
- **How often**
- **How we'll know it happened**

Share toggle defaults **on** here, because the commitment is the accountability.

### Tab 6 — Share

**Top: the group-chat draft.** Assembles whatever's been ticked, plus the commitment, into clean formatted text with one **Copy for group chat** button. Show a *Copied* confirmation. Include a selectable plain-text fallback box, since clipboard access is unreliable inside in-app browsers.

```
Tristan & Elyse — Session 4, Conflict and repair

What we're sharing:
[whatever they ticked]

Our commitment this month:
Sunday night 20-minute reset before the week starts.
We'll know it happened because it's in both our calendars.
```

**Below: everyone else's commitments.** Editable rows, prefilled:

- Tristan & Elyse
- Sean & Jenna
- Ash & Matt
- Zac & Elyse

Allow adding and renaming rows — attendance varies and the group may grow. **Note the two Elyses: always render the full couple label, never the first name alone.**

These notes go into the PDF, which is what makes accountability survive past the night.

### Tab 7 — Close, and PDF export

Closing words for the session, the day-14 heads-up, and **Export PDF**.

Build the PDF with a dedicated print stylesheet and `window.print()`. Best typography, no dependencies, and Save-as-PDF is clean on a laptop. Only reach for `html2pdf.js` if print can't be made to look right.

**Contents:**
- Cover — session number and title, the date, the name from the Start tab
- The scripture passages, **with highlights preserved as a printed tint**, and the personal notes underneath
- The message beats and landing line — full version, for leaders and participants alike
- All four questions with their answers, shared or not
- The commitment card, given a full page
- Everyone else's commitments
- Closing page: the day-14 check-in question, then blank ruled space to write on later
- Back page: the NLT attribution

Everything the person typed goes in, regardless of what they ticked. The toggles govern the group chat, not the keepsake.

**Leader PDFs** also include the run sheet.

**Year-end:** at session 12, a second button — **Export the year.** All twelve commitments and how each went, in one document.

### Design direction

Four couples at home on a Monday night, on a video call, typing honest things about their marriage. It should read like a well-made devotional notebook: calm, warm, unhurried, easy on the eye across a 75-minute sitting.

**Palette — Salvation Army, used with restraint**

| Token | Hex | Use |
|---|---|---|
| Ground | `#FBF8F3` | Page. Warm paper, not grey. |
| Ink | `#0A2540` | Salvo navy. Body text and structure. |
| Ink soft | `#4A6178` | Secondary text, labels, captions |
| Red | `#E4002B` | Salvo red. Accent only — active tab marker, rules, occasional emphasis. Never a background for text. |
| Gold | `#FFC72C` | Salvo yellow. **Commitment tab and text highlights only.** |
| Gold tint | `#FFF0C7` | Highlight fill behind scripture text |
| Line | `#E5DED2` | Hairlines, field borders |

Do not drift into cream-and-terracotta. Navy, red and gold on warm paper — that's the brief.

**Typography**

- Reading face: a warm serif with real texture for scripture, questions, message. *Newsreader*, *Source Serif 4*, or *Fraunces* at a low softness setting.
- UI face: a quiet sans for tabs, buttons, labels. *Inter* or *Public Sans*.
- Base body **18px**, line-height 1.65, measure capped around 66 characters. Laptop screens tempt you to run text full width — don't. Comfort beats density.
- Scripture gets the largest setting on the site.

**Signature element:** the Commitment tab. Gold ground, the commitment set large in the serif, the date beneath like a signature line. Everything else stays disciplined so this one screen lands.

**Motion:** a soft cross-fade between questions, and the highlight popover easing in. Nothing else. Respect `prefers-reduced-motion`.

**Floor:** works offline once loaded, visible keyboard focus throughout, no layout shift as text areas grow, arrow-key tab navigation, and a clean print stylesheet.

**Copy voice:** plain, warm, direct. No church-marketing language, no exclamation marks. Buttons say what happens. *Copy for group chat* produces *Copied.*

---

## Part 2 — The run sheet (leader view only)

Video is more tiring than a lounge room, so this runs shorter than an in-person version. **75 minutes.**

| Time | Block |
|---|---|
| 0:00–0:10 | **Report back** (sessions 2+). Each couple: how did last month's commitment land? Wins and misses. |
| 0:10–0:20 | Catch-up |
| 0:20–0:30 | **Message** — read from tab 3 |
| 0:30–0:52 | **Couple time** — everyone drops off the call |
| 0:52–1:10 | **Share** — back on, one thing each |
| 1:10–1:15 | Commitments read aloud, then prayer |

### The bit that will break: there are no breakout rooms

Messenger video has no breakout function, and nobody talks honestly with three other households listening. So everyone hangs up at the 30-minute mark and rejoins at 52.

Put this script on the leader's Message tab, to be read before anyone leaves:

> We're all going to hang up now and come back at [time]. Twenty-two minutes. There's a timer on the Questions tab — start it when you're ready. Answer as much or as little as you want to; none of it is going anywhere unless you choose to share it.

Also post the return time into the group chat as a message, so nobody has to hold it in their head.

### The rhythm to announce at session 1

> In two weeks you'll get a message in the group chat asking for one honest line about how it's going. And at the next session we'll all report back — wins and misses both.

Naming it in advance means nobody's ambushed by the accountability, and if the usual leader is away one month somebody else picks it up, because everyone already knows what's meant to happen.

Whoever sends the day-14 message goes first. If the leader shares something real, everyone else can.

---

## Part 3 — The 12 sessions

One per month. Run them in order — vulnerability is meant to build, and session 10 in month two would be a mistake.

Store all of this in `sessions.js` as structured data so Zac can edit wording without touching code.

---

### 1 — Drift

**Premise:** Nobody plans to drift. Drift is what happens in the absence of a plan.
**Scripture:** Ephesians 5:25–33; Revelation 2:4

**Beats**
1. Nobody plans to drift. It's just what happens when nothing else is decided.
2. Paul never describes love as a feeling that arrives. He describes something a husband *does*, deliberately, at cost.
3. Most of us have quietly downgraded and called it being settled. Some of that really is settled. Some of it is asleep.
4. **Landing:** tonight isn't about fixing a broken marriage. It's about refusing to coast in a good one.

**Questions**
1. What's changed in us over the last six months — for better and for worse?
2. Where have we quietly settled for less than we promised each other?
3. What does my spouse carry that I've stopped noticing?
4. What would growth actually look like for us in three months?

**Share:** the thing we noticed tonight that we don't want to leave where it is.
**Commitment:** one habit, daily or weekly, for the next month.
**Closing:** You didn't fix anything tonight. You just stopped drifting, on purpose, for the first time in a while. That's the whole win.
**Day 14:** One honest line — is the habit alive, or has it slipped?

---

### 2 — Words

**Premise:** Your spouse's inner voice probably sounds like you.
**Scripture:** Ephesians 4:29; James 3:3–5

**Beats**
1. James says the tongue is small and steers the whole thing. In marriage the rudder is usually the first five minutes after one of you walks in the door.
2. Paul's test isn't *was it true.* It's *did it build.*
3. Sarcasm is the cheapest way to say something cruel and keep deniability.
4. **Landing:** your spouse's inner voice probably sounds like you. What are you teaching it to say?

**Questions**
1. What do I say most often that lands as criticism, even when I don't mean it that way?
2. When did I last say something specific and admiring out loud, rather than just thinking it?
3. What's a phrase in our house that always escalates things?
4. What would I need to hear this week to feel like you're on my side?

**Share:** one phrase we're retiring, or one we're adding.
**Commitment:** something spoken and specific — one piece of praise, out loud, daily.
**Closing:** Nobody changes how they speak by deciding to be nicer. They change it one sentence at a time, on purpose, when they're tired. That's this month.
**Day 14:** Has the phrase stayed retired, or has it resurfaced?

---

### 3 — Money

**Premise:** Money fights are almost never about money.
**Scripture:** 1 Timothy 6:6–10; Matthew 6:21

**Beats**
1. Money fights are almost never about money. They're about safety, control, and what each of us learned money means.
2. Jesus runs the logic the direction we don't expect — the heart follows the treasure, not the other way around.
3. Two savers or two spenders is rare. Most couples are one of each, and that's a feature, not a fault.
4. **Landing:** if you can't say the actual numbers out loud to each other, that's the growth edge.

**Questions**
1. What did money mean in the house I grew up in — scarcity, security, status, secrecy?
2. Do we both actually know our numbers: what comes in, what goes out, what we owe?
3. What's one purchase in the last year that one of us still quietly resents?
4. What are we generous with — and is that a decision or an accident?

**Share:** one thing changing about how we handle money together. No figures required.
**Commitment:** a recurring money conversation — same time, same length, in the diary.
**Closing:** Nobody here needs to be good with money. You need to be honest with each other about it. Those are different skills and only one of them is required.
**Day 14:** Did the money conversation actually happen? Yes or no is fine.

> **Leader note:** if Zac is leading this one — you're a CFO. You'll be the most comfortable person on the call, which is a risk; it can make everyone else go quiet. Go second, not first, and lead with something you and Elyse actually got wrong.

---

### 4 — Conflict and repair

**Premise:** Strong couples aren't the ones who fight less. They're the ones who come back faster.
**Scripture:** Ephesians 4:26–27; Matthew 5:23–24

**Beats**
1. Paul assumes you'll be angry. The instruction isn't *don't* — it's *don't let it set.*
2. Every couple has a fight style. Usually one pursues and one withdraws, and each makes the other worse.
3. Repair matters more than technique. Strong couples aren't the ones who fight less — they're the ones who come back faster.
4. **Landing:** what's the longest we've ever gone without repairing? That's our real number.

**Questions**
1. What do I do in a fight — pursue, withdraw, keep score, go quiet?
2. What does my spouse do mid-argument that makes me feel unsafe?
3. What do we keep fighting about that we've never actually resolved?
4. What's the fastest way back for us — what actually works as an apology?

**Share:** one repair move we're going to use.
**Commitment:** name the repair phrase and agree the hard stop.
**Closing:** You will fight again this month. The only thing decided tonight is how long it lasts.
**Day 14:** Has the repair move been tested yet? How did it go?

---

### 5 — The ledger

**Premise:** Repair ends a fight. Forgiveness clears the ledger. They're not the same thing.
**Scripture:** Colossians 3:13; Matthew 18:21–35

**Beats**
1. Repair ends a fight. Forgiveness clears the ledger. A marriage can be very good at the first and still quietly drowning in the second.
2. Peter asks for a number. Jesus gives him one so absurd it's obviously not a number — it's a posture.
3. The servant in the parable is forgiven an amount he could never repay, then throttles someone over pocket change. That's what unforgiveness in a marriage looks like from the outside.
4. **Landing:** what are you still charging your spouse interest on?

**Questions**
1. What's something I said I forgave but still bring up?
2. What do I suspect my spouse is still carrying from something I did?
3. What makes it hard for me to let go — does forgiving feel like saying it didn't matter?
4. What's one thing I could actually clear this month?

**Share:** what forgiveness would cost me, and whether I'm willing to pay it.
**Commitment:** one item named, and a conversation to clear it, by a date.
**Closing:** Forgiveness isn't pretending the debt wasn't real. It's deciding to stop collecting on it. That decision usually has to be made more than once.
**Day 14:** Has the ledger item been cleared, or is it still open?

---

### 6 — Rhythm and rest

**Premise:** Your diary is a spiritual document.
**Scripture:** Mark 6:31; Genesis 2:2–3

**Beats**
1. Jesus pulls the disciples out of good, necessary, urgent work — to rest. Busyness isn't a virtue.
2. Your diary is a spiritual document. It says what you actually believe matters.
3. Most young marriages don't have a time problem, they have a leftovers problem. The marriage gets what's left.
4. **Landing:** if we don't schedule us, we only ever get the tired version of each other.

**Questions**
1. What's currently getting the best of me, and what's getting the leftovers?
2. When did we last have unhurried time together that wasn't admin or a screen?
3. What would we have to say no to, in order to say yes to each other?
4. What does rest actually look like for each of us — and do I know your answer?

**Share:** one thing coming off the calendar, or one thing going on it.
**Commitment:** a protected weekly slot, with a rule attached.
**Closing:** Everything in your calendar was put there by somebody. Some of it by you. That's better news than it sounds.
**Day 14:** Did the protected time survive the fortnight?

---

### 7 — The unglamorous stuff

**Premise:** Invisible work stays invisible right up until it stops.
**Scripture:** John 13:3–15; Philippians 2:3–4

**Beats**
1. Jesus knows exactly who he is, and takes the servant's job anyway. Security is what makes service possible.
2. Most of married romance is logistics — who does the bins, who books the appointments, who holds the whole schedule in their head.
3. Invisible work stays invisible right up until it stops.
4. **Landing:** name the thing your spouse carries that nobody ever thanks them for.

**Questions**
1. What does my spouse do that I've never actually thanked them for?
2. What's the mental load in our house, and who's carrying more of it?
3. What's one job I've avoided because I decided it was theirs?
4. What would make my spouse's Monday easier?

**Share:** one job changing hands.
**Commitment:** take one thing off their plate — permanently, not as a favour.
**Closing:** Nobody writes songs about who does the bins. Do it anyway.
**Day 14:** Is the job still off their plate?

---

### 8 — Praying together

**Premise:** Almost every Christian couple believes they should. Very few do.
**Scripture:** Matthew 18:19–20; Colossians 3:16

**Beats**
1. Nearly every Christian couple believes they should pray together. Very few do. Say that out loud — it kills the shame in the room.
2. The barrier isn't unbelief, it's exposure. Praying out loud with your spouse means they hear what you actually want.
3. Small and consistent beats long and occasional. Thirty seconds counts.
4. **Landing:** the couples who pray together aren't more spiritual than you. They just started, badly, and kept going.

**Questions**
1. Have we ever prayed together outside a meal or a crisis? What stopped us?
2. What do I find hardest about praying out loud in front of you?
3. What's one thing I'd want you to pray for me this month?
4. What time of day could realistically work for us?

**Share:** what we're going to try, and how often.
**Commitment:** something small enough to survive — sixty seconds, same time, most nights.
**Closing:** Start badly. Everyone who does this started badly.
**Day 14:** How many nights out of the last fourteen? Honesty over performance.

---

### 9 — What we brought with us

**Premise:** You married a family, not just a person.
**Scripture:** Genesis 2:24; Exodus 20:12

**Beats**
1. Leave and cleave. Leaving is an act, not an event — some of us moved out without ever leaving.
2. You married a family, not just a person. Their normal isn't neutral, and neither is yours.
3. The patterns we swore we'd never repeat are exactly the ones we repeat under stress.
4. **Landing:** honouring your parents and building your own household aren't in conflict — but they do have to be negotiated, out loud, by the two of you.

**Questions**
1. What did conflict, affection and money look like in my parents' marriage — and what did I absorb?
2. Where do our two families' normals clash in our house?
3. Is there a boundary with either family we've needed to set and haven't?
4. What's one pattern from my family I want to keep, and one I want to break?

**Share:** one pattern we're keeping, one we're breaking.
**Commitment:** a specific conversation to be had, or a boundary to be set, by a named date.
**Closing:** You are the first generation of your household. Some of what you inherited is a gift. Some of it is just furniture you never chose.
**Day 14:** Has the conversation happened yet?

---

### 10 — Attention

**Premise:** Desire follows attention.
**Scripture:** Song of Songs 2:10–13; Proverbs 5:18–19

**Beats**
1. Scripture isn't squeamish about desire inside marriage. The Song is in the Bible and it isn't an allegory about admin.
2. Desire follows attention. A lot of what feels like a desire problem is an attention problem.
3. Most people want to be chosen again, not merely kept.
4. **Landing:** when did you last make your spouse feel wanted — on purpose?

**Questions**
1. When do I feel most wanted by you? Do you know my answer?
2. What's got in the way of us — tiredness, phones, resentment, something unspoken?
3. What did we do early on that we've stopped doing?
4. What's one thing I'd love you to initiate?

**Share:** one thing we're bringing back.
**Commitment:** one planned, intentional date — booked by whichever of you plans less.
**Closing:** Being chosen once is a wedding. Being chosen again is a marriage.
**Day 14:** Did the date happen?

> **Leader note:** say clearly before people drop off that sharing is optional this session, and mean it. The commitment still gets shared; the answers don't have to.

---

### 11 — Hard seasons

**Premise:** Ecclesiastes doesn't promise every season is good. It promises every season is a season.
**Scripture:** Ecclesiastes 3:1–8; Romans 5:3–5; 2 Corinthians 1:3–4

**Beats**
1. Ecclesiastes doesn't promise every season is good. It promises every season is a season.
2. Suffering doesn't automatically produce character. It produces character in people who aren't carrying it alone.
3. Couples grieve at different speeds. One wants to talk, one wants to function — both are grief, and each can look like coldness to the other.
4. **Landing:** the comfort Paul describes gets passed on. What you're carrying now is likely what you'll one day carry someone else through.

**Questions**
1. What's the hardest thing we've walked through together, and what did it show us about us?
2. When I'm struggling, what do I actually need from you — and have I ever said it plainly?
3. Is there something heavy right now that one of us is carrying alone?
4. Who has carried us well, and have we ever thanked them?

**Share:** whatever you're willing to name, and nothing more.
**Commitment:** one act of asking for help, or offering it.
**Closing:** You are ten months into a group of people who now know something true about you. That is not nothing. Use it.
**Day 14:** Did you ask for the help, or offer it?

> **Leader note:** this is the heaviest session. Some of this group will be carrying real things — loss, waiting, health, money, family. Say up front that nobody has to share. Don't fill silences. Don't try to resolve what someone names. If something serious surfaces, follow it up privately afterwards rather than on the call.

---

### 12 — What our marriage is for

**Premise:** A marriage turned only inward gets small.
**Scripture:** Joshua 24:15; Matthew 5:14–16

**Beats**
1. A marriage turned only inward gets small. Joshua's line is about a household with a direction.
2. Your marriage is either a resource to other people, or a fortress against them.
3. This movement was largely built by married couples who ran things together. That's the lineage this group sits in.
4. **Landing:** in ten years, what will people say this household was for?

**Questions**
1. If our marriage has a purpose beyond the two of us, what is it?
2. What are each of us good at that we've never used together?
3. Who outside this house is better off because we're married?
4. What's one thing we could do together in the next year that would scare us slightly?

**Share:** our one-line answer — *this household is for ___.*
**Commitment:** one concrete first step toward it, inside the month.
**Closing:** Twelve months ago you were coasting in a good marriage. Export the year, and read what you wrote in session one.
**Day 14:** What did the first step look like?

---

## Part 4 — Also worth building

Ranked by how much they'll matter on the night.

1. **The 22-minute countdown.** Highest-value addition. Once everyone hangs up there is nobody to call time.
2. **Last month's commitment on the Start tab,** pulled from storage with a *how did it go?* field. Makes the report-back block run itself and feeds the year-end export.
3. **A copyable day-14 message** on the leader's Close tab. Removes the biggest point of failure in the whole rhythm — somebody forgetting to send it.
4. **A running notes field on every tab.** People think of things out of order and lose them tabbing away.
5. **Offline-capable.** A small service worker, so a dropped connection mid-session doesn't lose the page.
6. **Export the year,** at session 12.

---

## Part 5 — Build order

1. Fetch the 12 sessions' NLT passages from `api.nlt.to`, bake into `sessions.js` with stable passage IDs
2. `sessions.js` — all 12 sessions as structured data
3. Shell: opening gate, tab strip, Next button, arrow keys, `localStorage` schema
4. Start tab — picker, name, last month's commitment
5. Scripture tab — render, highlight, notes
6. Message tab — leader and participant variants
7. Questions tab — one per screen, share toggles, countdown
8. Commitment card
9. Share tab — assembly, clipboard, others' commitments
10. Close tab, print stylesheet, PDF export
11. Offline, year-end export
12. Deploy to GitHub Pages; README covering how to edit `sessions.js` and redeploy
