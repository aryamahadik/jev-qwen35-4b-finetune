# Decision memo: the startup idea to build first

## 1. The pick

**Build Proposal C, the EU AI Act incident clock, which scored 26.5 out of 40.** B scored 22.5, so the call is not close.

This is a bet to test. It is not proof.

*Serious incident*: a harmful AI event that the EU AI Act says must be reported. *Provider*: the company that builds or sells an AI system.

## 2. Why it beats the others

- **B, fix-proof GitHub app (22.5):** GitHub's autofix already reruns its own check before it opens a fix. The rerun is a platform feature, and no auditor has shown that they accept a tool-made retest record.
- **O, cheap-model orchestration (19.5):** Fugu, Martian, Bifrost and OpenRouter already sell routing. The research's own math, under its assumptions, shows five cheap calls cost about 1.4 times one strong call per solved task, so the savings may not exist.
- **L, license checker (19):** Few buyers are bound by the big thresholds, and every answer needs lawyer sign-off. That makes it a services business.

The judges' notes list O and L at 18, which conflicts with the table. This memo uses the table. The older research files use other scales, so do not compare them directly.

## 3. What it is

- **Product:** a private, tamper-evident log for AI providers. It runs the reporting clock, drafts the report to the EU authority, and records who decided what.
- **Buyer:** AI vendors that sell hiring, credit or health tools in the EU. Not the firms that merely use those tools.
- **What the software does:**
  - **Clock:** you enter when you became aware of an incident. It works out the deadline and sends alerts.
  - **Write-once log:** each entry gets a fingerprint (a hash, a code that changes if the text changes). Each entry also stores the fingerprint of the one before it, so any edit shows.
  - **Decision log:** who judged the incident serious, the causal-link date (the day you could show the AI caused the harm), and why. A named person signs.
  - **Report drafts:** fills the EU Commission's draft template. It allows an incomplete first report, then a complete one.
  - **Export:** PDF and JSON.
  - **AI helper:** a small open model (8 billion parameters, such as Llama 3.1 8B). It reads raw notes, pulls out dates and system names, suggests a tier, and lists missing fields. You train nothing.
- **What a person does:** decides if the incident is serious, sets the causal-link date, signs, and submits.
- **What it does not do:** give legal advice or a compliance certificate, decide whether a report is required, submit anything on its own, detect prompt injection (tricks that hijack an AI), or cover the duties of the largest model makers.

## 4. Why it is unique

- **OneTrust:** a broad privacy suite. Our earlier research said its incident module covers personal-data breaches. A sponsored article says it also logs AI incidents. That is unverified, and it is the biggest threat to this claim.
- **Credo AI, Holistic AI, Trustible:** AI governance platforms. Their pages show risk registers, monitoring and evidence stores. None shows a workflow that files a report with a regulator. Holistic AI's Tracker watches incidents across the market, not your own reports (my inference).
- **AI Incident Database, OECD AI Incidents Monitor:** public lists with no private log and no deadlines.
- **A marketplace "skill":** claims to draft and submit Article 73 notices (the EU AI Act's reporting rule) for in-house lawyers. We saw only the listing. Watch it.
- **Six 2025-26 acquisitions** (Protect AI, CalypsoAI, Lakera, Virtue AI, Guardrails AI, Haize Labs) were guardrail and red-team firms, not reporting firms.

The evidence is thin: three searches earlier, five today, small samples. The gap is likely, not proven. A governance vendor can add a clock as one module.

## 5. Two-week validation test

- **Cost:** under $20 (my estimate; free tools).
- **Target:** 10 conversations. Pilots: none yet.

1. **Days 1-3:** List 30 targets: heads of compliance, or ML and product leads, at EU-facing AI vendors. Find them on LinkedIn and in EU AI compliance groups.
2. **Days 3-5:** Send about 40 short messages asking for a 20-minute call. The reply rate is not yet measured.
3. **Days 4-14:** Run 10 calls. Ask these three questions word for word:
   - "When one of your AI systems hurts someone, how do you find out, and who decides if it must be reported?"
   - "If a regulator gave you two days, what could you hand over today, and how long would it take?"
   - "Who owns this budget, and what would make you pay for a tool that runs the clock and keeps a signed log?"
4. **End of each call:** offer a free tabletop drill (a practice run on a pretend incident).
5. **Log every answer** in one shared sheet.

**Success:** at least 3 of 10 describe reporting as a current pain, meaning a past miss or no way to meet a deadline (my definition). At least 1 agrees to a drill by day 14. The 3-of-10 line comes from the research. The drill count is my addition.

**Stop** if fewer than 3 of 10 describe a current pain.

## 6. Ninety-day plan to a first paid pilot

All timings are my estimates.

- **Days 1-14:** the test above.
- **Days 15-30:** Check Article 73's start date and deadline tiers on EUR-Lex, the EU's official law site. Check whether the Commission guidance is final. Build the clock, then the write-once log. Spend nothing on lawyers yet.
- **Days 31-60:** Run drills with providers. Build the decision log and the report draft. Test the AI helper on 100 made-up cases.
- **Days 61-90:** After three providers agree to a drill, pay a lawyer to review your terms. Offer a paid pilot at an assumed $500 a month (untested). Goal: one signed paid commitment.

Build cost, from research estimates: about $16 with free hosting, or about $76 in the worst case with three months of paid hosting. A lawyer is not in these numbers. The research calls a lawyer likely your biggest real cost.

## 7. Kill criteria

**Stop if:**
1. Fewer than 3 of 10 interviewed providers call reporting a current pain.
2. No provider agrees to a drill by day 60.
3. A governance vendor ships an authority-report clock before your first drill, and your top prospects choose it.
4. No paid pilot or signed paid commitment by day 90.
5. Spend passes $100 before a paid pilot.

**Pause if:**
6. Final Commission guidance changes the 2, 10 or 15-day tiers or drops the template.
7. The AI helper misses a required field in over 20% of 100 test cases after prompt fixes. Then sell the log alone, without AI drafting.

**Runner-up:** B, but only if a drill fails and B's 10-repo test finds flaws that GitHub's autofix misses.

## 8. What you give up

- **Near-term money.** High-risk duties for Annex III systems start 2 December 2027, per sources. Sources disagree on Article 73. Some say 2 August 2026, which would make pain current. If the later dates hold, early sales are readiness pitches.
- **Proven pain.** Only 36% of security teams have an AI security budget line (45-person survey). A vendor survey (OneTrust, 6 Oct 2026) says 86% of organizations had an AI incident last year, but only 27% paused deployment. These are weak signals.
- **A simple moat.** A governance vendor can add a module. Your edge is focus and speed, not secrecy.
- **Market size.** You skip firms that use AI and sell only to EU-facing providers.
- **Moving rules.** The Commission's guidance is a September 2025 draft. The Digital Omnibus has already moved dates.
- **Legal cost and risk.** Lawyer fees sit outside the $100 limit.

**Bottom line:** C is the strongest of the four ideas here, but it is still a bet. Run the two-week test before you write product code.
