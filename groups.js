/*
 * Life Groups — group registry / config.
 *
 * One object per stream drives the engine. Session prose + baked scripture live
 * in streams/<id>.js. Safety notes, disclaimers and rules are quoted verbatim
 * from the stream specs (tools/*-sessions.md) — do not paraphrase them.
 *
 * To add a new group: add a spec to tools/, run tools/build-streams.py, bake with
 * tools/fetch-passages.py, then add a config object here and list the file in
 * index.html + sw.js.
 */
(function () {
  window.LG = window.LG || { groups: [], streams: {} };

  var ATTRIBUTION =
    "Scripture quotations are taken from the Holy Bible, New Living Translation, " +
    "copyright © 1996, 2004, 2015 by Tyndale House Foundation. Used by permission " +
    "of Tyndale House Publishers, Carol Stream, Illinois 60188. All rights reserved.";
  window.LG.attribution = ATTRIBUTION;

  // Shared run sheets by session length.
  var RUN_75 = [
    { time: "0:00–0:10", block: "Report back on last month — wins and misses." },
    { time: "0:10–0:20", block: "Catch-up" },
    { time: "0:20–0:30", block: "Message — read from the Message tab" },
    { time: "0:30–0:52", block: "Personal time — everyone drops off the call" },
    { time: "0:52–1:10", block: "Share — back on, one thing each" },
    { time: "1:10–1:15", block: "Commitments read aloud, then prayer" }
  ];
  var RUN_60 = [
    { time: "0:00–0:08", block: "Report back on last month" },
    { time: "0:08–0:15", block: "Catch-up" },
    { time: "0:15–0:23", block: "Message" },
    { time: "0:23–0:40", block: "Personal time — drop off the call" },
    { time: "0:40–0:53", block: "Share" },
    { time: "0:53–1:00", block: "Commitments and prayer" }
  ];
  var RUN_60_GRIEF = [
    { time: "0:00–0:08", block: "Report back — how has the fortnight been?" },
    { time: "0:08–0:15", block: "Catch-up" },
    { time: "0:15–0:23", block: "Message" },
    { time: "0:23–0:38", block: "Personal time — drop off the call" },
    { time: "0:38–0:52", block: "Share — only if you want to" },
    { time: "0:52–1:00", block: "Something to carry, and prayer" }
  ];
  var RUN_90_PREMARITAL = [
    { time: "0:00–0:10", block: "Follow up on last session's action" },
    { time: "0:10–0:20", block: "Message, read by the mentor couple" },
    { time: "0:20–0:35", block: "Private answering — partners in separate rooms" },
    { time: "0:35–1:00", block: "Compare, together, with the mentors present" },
    { time: "1:00–1:20", block: "Mentor couple's turn — what this looked like in their marriage" },
    { time: "1:20–1:30", block: "Action for the fortnight, and prayer" }
  ];

  function runsLine(min) {
    return "Report back on last month, a short teaching, then everyone drops off the " +
      "call for personal time and comes back to share one thing each. Around " + min + " minutes.";
  }

  window.LG.groups = [
    {
      id: "marriage",
      title: "Marriage Life Group",
      blurb: "For married couples.",
      sessionCount: 12, sessionMinutes: 75, countdownMinutes: 22,
      runSheet: [
        { time: "0:00–0:10", block: "Report back (sessions 2+). Each couple: how did last month's commitment land? Wins and misses." },
        { time: "0:10–0:20", block: "Catch-up" },
        { time: "0:20–0:30", block: "Message — read from the Message tab" },
        { time: "0:30–0:52", block: "Couple time — everyone drops off the call" },
        { time: "0:52–1:10", block: "Share — back on, one thing each" },
        { time: "1:10–1:15", block: "Commitments read aloud, then prayer" }
      ],
      howItRuns: "Report back on last month, a short teaching, then everyone drops off the call for couple time and comes back to share one thing each. Around 75 minutes.",
      dropOffLabel: "Couple time",
      commitmentModel: "commitment", day14Model: "perSession", shareModel: "groupChat",
      attendees: ["Tristan & Elyse", "Sean & Jenna", "Ash & Matt", "Zac & Elyse"],
      session1Rhythm: "In two weeks you'll get a message in the group chat asking for one honest line about how it's going. And at the next session we'll all report back — wins and misses both.",
      leaderTip: "Whoever sends the day-14 message goes first. If the leader shares something real, everyone else can."
    },

    {
      id: "premarital",
      title: "Preparing for Marriage",
      blurb: "One engaged couple with a mentor couple. An 8-session course.",
      sessionCount: 8, sessionMinutes: 90, countdownMinutes: 15,
      runSheet: RUN_90_PREMARITAL,
      howItRuns: "A course for one engaged couple and a mentor couple. Each partner answers privately, then you compare side by side and talk about the gaps. Around 90 minutes.",
      dropOffLabel: "Private answering",
      gateVariant: "threeway",
      gateRoles: [
        { id: "getting-married", label: "Getting married" },
        { id: "mentoring", label: "Mentoring" }
      ],
      gatePrompt: "Which are you tonight?",
      commitmentModel: "action", commitmentLabel: "Action for the fortnight",
      day14Model: "none", shareModel: "compare",
      pauseRule: "If any of these come up, pause the course and talk to your minister or a professional this week: controlling behaviour, any violence or fear, undisclosed debt or hidden finances, pressure or coercion about sex or the wedding itself, ongoing addiction, or one partner not actually wanting to get married. Pausing is not failing them. Continuing regardless is.",
      yearExportLabel: "Export the course"
    },

    {
      id: "parents-young",
      title: "Parents of Young Children",
      blurb: "Parents with children roughly 0–10.",
      sessionCount: 12, sessionMinutes: 60, countdownMinutes: 17,
      runSheet: RUN_60, howItRuns: runsLine(60), dropOffLabel: "Personal time",
      commitmentModel: "commitment", day14Model: "perSession", shareModel: "groupChat",
      commitmentIntro: "Make it small enough that a bad week can't kill it.",
      whereWasI: true, attendees: []
    },

    {
      id: "parents-teens",
      title: "Parents of Teens & Young Adults",
      blurb: "Parents of children roughly 12–25.",
      sessionCount: 12, sessionMinutes: 75, countdownMinutes: 22,
      runSheet: RUN_75, howItRuns: runsLine(75), dropOffLabel: "Personal time",
      commitmentModel: "commitment", day14Model: "perSession", shareModel: "groupChat",
      gateNote: "What's said here about our children stays here. They're not in the room to give their side.",
      attendees: []
    },

    {
      id: "blended",
      title: "Blended Families",
      blurb: "Step-parents and remarried parents raising children from previous relationships.",
      sessionCount: 12, sessionMinutes: 75, countdownMinutes: 22,
      runSheet: RUN_75, howItRuns: runsLine(75), dropOffLabel: "Personal time",
      commitmentModel: "commitment", day14Model: "perSession", shareModel: "groupChat",
      gateNote: "What's said here about our children, and about their other parent, stays here. None of them are in the room.",
      questionVariants: true, attendees: []
    },

    {
      id: "carers",
      title: "Caring for Ageing Parents",
      blurb: "Adults caring for, or beginning to care for, ageing parents.",
      sessionCount: 12, sessionMinutes: 60, countdownMinutes: 17,
      runSheet: RUN_60, howItRuns: runsLine(60), dropOffLabel: "Personal time",
      commitmentModel: "commitment", day14Model: "perSession", shareModel: "groupChat",
      startTabNote: "Miss one, come back. Nothing here builds on what you missed.",
      standingNote: "If you're navigating aged care, start with My Aged Care (1800 200 422) for assessments and services, and Carer Gateway (1800 422 737) for practical and emotional support for carers, including counselling and respite. Both are free. Dementia Australia (1800 100 500) is the place for anything dementia-specific.",
      attendees: []
    },

    {
      id: "money",
      title: "Money & Generosity",
      blurb: "Individuals, couples and households. Written to work if you're behind, not just if you're saving.",
      sessionCount: 12, sessionMinutes: 75, countdownMinutes: 22,
      runSheet: RUN_75, howItRuns: runsLine(75), dropOffLabel: "Personal time",
      commitmentModel: "commitment", day14Model: "perSession", shareModel: "groupChat",
      shareStandingLine: "No numbers. Ever. Just what you decided.",
      standingNote: "Nothing in this course is personal financial advice. It's a conversation about what money means and what you want to do with it. For decisions about products, investments, insurance, super or tax, see a licensed adviser or an accountant who knows your situation. If you're in financial difficulty, the National Debt Helpline (1800 007 007) is free, independent and confidential.",
      attendees: []
    },

    {
      id: "grief",
      title: "Grief & Loss",
      blurb: "Adults some months or more past a significant bereavement.",
      sessionCount: 12, sessionMinutes: 60, countdownMinutes: 15,
      runSheet: RUN_60_GRIEF, howItRuns: "A group of people who have lost someone, saying true things. Company in the dark. Nobody has to share anything, ever. Around 60 minutes.",
      dropOffLabel: "Personal time",
      commitmentModel: "carry", commitmentLabel: "Something to carry",
      commitmentIntro: "An intention, a question to sit with, or a person to contact. Never a task, and nobody will check up on it.",
      day14Model: "fixedLine", day14FixedLine: "How are you this fortnight?",
      shareModel: "groupChat", shareOptionalAlways: true,
      startTabNote: "If your loss is very recent, this group may not be the right thing yet. Griefline (1300 845 745) and your GP are better places to start, and we'll still be here later.",
      sessionRules: [
        "Nobody has to share anything, ever. Silence is a complete contribution.",
        "Nobody gives advice, and nobody offers a silver lining.",
        "What's said here stays here.",
        "You can leave the call at any point without explaining."
      ],
      standingNote: "Support: Griefline 1300 845 745 (12pm–3am daily). Lifeline 13 11 14, any hour. Your GP can arrange a mental health care plan for subsidised counselling. StandBy Support After Suicide 1300 727 247. Red Nose 1300 308 307 for miscarriage, stillbirth and infant loss.",
      watchForNote: "Watch for these, and act rather than waiting for next month: someone who can't function months on, someone entirely isolated, someone whose drinking has escalated, someone who says they see no point in going on. Don't assess and don't diagnose. Stay with them after the call, help them contact their GP that week, and know that Lifeline (13 11 14) is there any hour. Tell the person you'll check in, then actually do it.",
      attendees: []
    }
  ];
})();
