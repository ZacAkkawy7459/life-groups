# Preparing for Marriage — 8-Session Course

**For:** Claude Code
**Owner:** Zac
**Stream:** `premarital`
**Audience:** One engaged couple, working with one mentor couple. Salvation Army outreach.

Build as a stream inside the existing Life Group site. Core app behaviour, design, NLT handling, highlighting and PDF export are specified in `marriage-life-group-sessions.md`. This stream needs the most structural change of the four — read Part 1 carefully before building.

---

## Part 1 — How this stream differs

This is not a monthly group. It is a **course**: one engaged couple and one mentor couple, meeting weekly or fortnightly over roughly two to four months before the wedding. Everything below follows from that.

### Eight sessions, not twelve

Run in order, no skipping. Sessions 3 and 5 are the ones couples most want to skip and most need.

### The gate changes

The leader/participant question becomes a three-way choice:

> **Which are you tonight?**
> [ Getting married ] [ Mentoring ] [ ... ]

- **Getting married** — the engaged partners, one per laptop. Each answers privately.
- **Mentoring** — the mentor couple. Gets the full beats, the leader notes, the run sheet, and the guidance in Part 3.

### Two-column answers — the central change

In the other three streams, one person or one couple writes one answer. Here, **each partner answers privately first, then the answers are compared side by side.** Discovering that you assumed different things is the entire point of pre-marital work, and an interface that lets a couple write one shared answer defeats it.

Build it like this:

1. **Answer privately.** Each partner works on their own laptop. Their answers are stored locally as normal. A partner cannot see the other's answers at this stage — there's no shared storage, so this is enforced by the architecture rather than by a rule.
2. **Compare.** When both are done, one partner uses **Copy my answers**, pastes them to the other (message, email, whatever's to hand), and that person uses **Paste partner's answers**. The tab then renders both side by side, question by question.
3. **Talk about the gaps.** Under each pair, a shared field: *what we noticed about the difference.*

Add an **Agreement dial** on each question — each partner marks *we're aligned / we're close / we're not aligned* before comparing. The mismatches in that dial are more diagnostic than the answers themselves, and the compare view should surface them first.

The mentor couple's PDF export includes only the agreement dials and the shared notes — never the private answers, unless the couple chooses to show them. Say this on screen.

### Run sheet — 90 minutes

| Time | Block |
|---|---|
| 0:00–0:10 | Follow up on last session's action |
| 0:10–0:20 | Message, read by the mentor couple |
| 0:20–0:35 | Private answering — partners in separate rooms |
| 0:35–1:00 | Compare, together, with the mentors present |
| 1:00–1:20 | Mentor couple's turn — what this looked like in their marriage |
| 1:20–1:30 | Action for the fortnight, and prayer |

The mentor block is not filler. A couple who hear that a twenty-year marriage also got money wrong will believe it in a way no message can achieve.

### No group-chat sharing

Drop the Share tab's copy-to-group-chat feature for this stream. There is no group. Replace it with the compare view.

### The pause rule

Some things that surface in pre-marital work mean the course should stop and something else should start. Build this into the mentor view of every session, as a persistent, quiet footer note:

> **If any of these come up, pause the course and talk to your minister or a professional this week:** controlling behaviour, any violence or fear, undisclosed debt or hidden finances, pressure or coercion about sex or the wedding itself, ongoing addiction, or one partner not actually wanting to get married. Pausing is not failing them. Continuing regardless is.

---

## Part 2 — The 8 sessions

### 1 — What we think we're signing up for

**Premise:** You are each marrying the marriage you imagine.
**Scripture:** Genesis 2:18–25; Ecclesiastes 4:9–12

**Beats**
1. The first thing declared "not good" in a good creation is a person being alone. Marriage begins as an answer to a lack.
2. Every person walks in with a picture of what marriage looks like — assembled from their parents, their friends, and things they've never examined.
3. You are marrying a person, and also a set of expectations you have never compared.
4. **Landing:** tonight you find out how differently you've each been picturing this.

**Questions** *(answer privately, then compare)*
1. What do I expect marriage to be like day to day, one year in?
2. What am I most looking forward to, and what am I quietly nervous about?
3. What does a good marriage look like to me — whose marriage am I picturing?
4. What do I assume will change about us once we're married?

**Notice:** where your pictures differ, and whether either of you has assumed the other shares yours.
**Action:** each write down one expectation you didn't know the other had.

---

### 2 — Where we came from

**Premise:** You are both bringing a whole family into this, whether you like it or not.
**Scripture:** Genesis 2:24; Exodus 20:12

**Beats**
1. Leave and cleave. Leaving is an act — a decision to reorder your primary loyalty, made repeatedly, not once at a wedding.
2. Your family's normal is invisible to you and obvious to your partner. Theirs is the reverse.
3. Honouring your parents and building a new household aren't in conflict, but they do have to be negotiated out loud rather than assumed.
4. **Landing:** whose family's normal is going to win, and have you ever discussed it?

**Questions**
1. What did conflict, affection and money look like in my parents' relationship?
2. What do I want to carry forward, and what do I want to leave behind?
3. Where do I expect friction between our two families?
4. What boundaries will we need with each family, and who's going to hold them?

**Notice:** the boundary question. Couples who don't decide this before the wedding decide it during their first crisis, badly.
**Action:** one boundary agreed and written down.

---

### 3 — Money

**Premise:** The most common thing couples fight about, and the thing they're least likely to have discussed properly.
**Scripture:** Luke 14:28–30; 1 Timothy 6:6–10

**Beats**
1. Jesus uses the image of a builder counting the cost before starting. The point is about discipleship, and the principle is not subtle.
2. Money fights are about safety, control and what money meant in the house you grew up in — rarely about the actual amount.
3. Almost every couple thinks they've talked about money. Almost none of them has said the actual numbers out loud.
4. **Landing:** tonight you both say your numbers. All of them.

**Questions**
1. What do I earn, what do I owe, what do I have? Actual figures.
2. What did money mean in my family — scarcity, security, status, secrecy?
3. Am I a spender or a saver, and what do I think my partner is?
4. Whose money will it be, and how will we decide what's spent?

**Notice:** anything one of you didn't already know. That's the finding.
**Action:** write a one-page picture of your combined position — income, debts, assets — and agree how decisions get made.

> **Mentor note:** hold the line on real figures. A couple who won't say their debt out loud in front of you almost certainly haven't said it to each other. If something significant surfaces here that one partner didn't know, stop the session and let them have that conversation. It's more important than finishing the material.

---

### 4 — How we fight

**Premise:** You will fight. The only question is what happens next.
**Scripture:** Ephesians 4:26–27; Matthew 5:23–24

**Beats**
1. Paul assumes anger. The instruction is about not letting it set, not about avoiding it.
2. Every couple has a shape: one pursues, one withdraws, and each makes the other worse.
3. Repair is the skill. Couples who last aren't the ones who fight less — they're the ones who come back faster.
4. **Landing:** what did each of you watch your parents do when it got hard? That's your default until you choose otherwise.

**Questions**
1. What do I do when we argue — push, withdraw, go quiet, score points?
2. What does my partner do that makes it worse for me?
3. What have we not resolved that we keep circling back to?
4. What works as an apology for me, and does my partner know?

**Notice:** whether you've ever had a proper fight. If you haven't, that isn't a good sign — it usually means one of you is swallowing things.
**Action:** agree a repair phrase and a hard stop, and write them down.

---

### 5 — Sex and intimacy

**Premise:** The conversation most couples have least well before the wedding.
**Scripture:** 1 Corinthians 7:3–5; Song of Songs 2:10–13

**Beats**
1. Paul writes about mutual obligation and mutual authority — a strikingly reciprocal passage for its time.
2. The Song is in the Bible, celebrating desire in marriage without embarrassment. The church's discomfort is not the Bible's.
3. Expectations here are almost never discussed plainly, and mismatched assumptions cause real pain later.
4. **Landing:** you need to be able to talk about this, out loud, without either of you dying of embarrassment. Tonight is practice.

**Questions**
1. What do I expect about frequency, initiation and how we talk about this?
2. What am I embarrassed to say, and what would help me say it?
3. What has shaped my expectations — upbringing, church teaching, past experience, what I've watched?
4. How will we raise it when one of us is unhappy?

**Notice:** whether you can discuss this at all without deflecting into humour.
**Action:** agree how you'll raise it in future when something's wrong.

> **Mentor note — read before running this session.** Offer at the start to split by gender for the first half, mentor with mentee, and let them take it. Many couples will. Be clear you're not asking for sexual history in front of the group, and don't press for it. If anything raises a concern — pressure, coercion, a significant undisclosed history that one partner clearly needs to hear about, or a disclosure of past abuse — stop, don't handle it yourself, and help them get to a professional this week. Have that referral ready before the session starts.

---

### 6 — Work, home and who does what

**Premise:** Every couple thinks this will sort itself out. It sorts itself out badly.
**Scripture:** Philippians 2:3–4; Proverbs 31:10–31

**Beats**
1. Paul's instruction is to look to the interests of the other. In a shared house that's a logistics problem before it's a spiritual one.
2. The default is that whoever notices first does it, and whoever notices first does it forever.
3. Careers, moves and children force this open eventually. Deciding in advance is cheaper than discovering during a crisis.
4. **Landing:** whose job moves if one of you gets an offer interstate?

**Questions**
1. Who does what at home, and how did we arrive at that?
2. What do we each expect about work — hours, ambition, whose career leads?
3. What do we assume about children — whether, when, how many, and who steps back?
4. What happens if one of us wants to change direction?

**Notice:** the children question. Couples routinely assume agreement here and are wrong.
**Action:** write down what you've each assumed about children, and compare it honestly.

---

### 7 — Faith together

**Premise:** Two Christians can still want quite different things.
**Scripture:** Joshua 24:15; Amos 3:3

**Beats**
1. Amos asks whether two can walk together unless they've agreed to. It's a question about direction, not doctrine.
2. Shared faith is not the same as shared practice. Church, giving, prayer, and how you'd raise children can all differ sharply between two committed believers.
3. Joshua's declaration is a decision announced by a household. Yours hasn't made one yet.
4. **Landing:** what is your household going to be, and have you actually agreed it?

**Questions**
1. What do I expect about church — where, how often, how involved?
2. What do I expect about praying, reading and giving together?
3. How would I want children raised in faith, and what if we disagree?
4. Where is my faith actually at right now, honestly?

**Notice:** the honesty question. Engaged couples sometimes over-report here, to each other and to mentors.
**Action:** write one sentence: *our household will be a place where ___.*

---

### 8 — The covenant

**Premise:** You're about to make promises in front of witnesses. Do you know what they mean?
**Scripture:** Matthew 19:4–6; Ecclesiastes 4:9–12

**Beats**
1. Jesus goes back past the law to the beginning — two becoming one, joined by God. He treats marriage as something formed, not merely agreed.
2. A covenant is different from a contract. A contract limits your exposure; a covenant deliberately increases it.
3. The vows you're about to say were written by people who knew about poverty, sickness and worse. They're not decoration.
4. **Landing:** say the vows to each other tonight, out loud, in an ordinary room with the lights on. Find out what they feel like without a crowd.

**Questions**
1. Which line of the vows do I find hardest, and why?
2. What am I actually promising when I say *for worse*?
3. What do I want our marriage to be for, beyond the two of us?
4. What do I want to be true of us in fifty years?

**Notice:** the fifty-year question. If your answers point in different directions, that's worth knowing now.
**Action:** write your own one-line statement of what your marriage is for. Keep it. Read it on your first anniversary.

**Closing:** You've now had eight conversations most couples don't have until something forces them. Export the whole course. Keep it. You'll want it in about three years.
