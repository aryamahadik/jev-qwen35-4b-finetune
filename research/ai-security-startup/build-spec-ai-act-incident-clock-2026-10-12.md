# Build spec: AI Act incident clock (Proposal C)

> **Status: draft.** Scored 23.5 of 35, the top of five. The Article 73 dates and the Omnibus timeline come from secondary sources. Check EUR-Lex and the Official Journal before building on them.


## 1. The idea in one sentence

A private log that starts the EU AI Act serious-incident clock for AI companies, drafts the report, and keeps a signed record of who decided what.

*Terms: a "serious incident" is a harmful AI event the EU AI Act says must be reported. A "provider" is the company that builds or sells an AI system.*

## 2. Why it is unique

Crowding is real, but in other niches. Six AI-security startups were bought between July 2025 and September 2026, mostly in guardrails and red-teaming (competitor map, 12 Oct 2026). Incident reporting is a different job.

- **OneTrust:** broad privacy suite. Its incident module targets personal-data breaches, not AI incidents.
- **Credo AI, Holistic AI, Trustible:** AI governance registries with monitoring. My searches found no incident intake or authority reporting. Their newer modules are unchecked.
- **AI Incident Database, OECD AI Incidents Monitor:** public trackers. No private evidence store and no deadlines.
- **Openlayer, Secure Privacy, Modulos:** monitoring tools for the period before an incident. None found runs a reporting clock or drafts authority reports.

Three searches today found no product doing this. The sample is small, so treat the gap as likely, not proven. A governance vendor could add it as a module. Your edge is AI-specific focus, owning the clock and signed log, and feeding the public trackers.

## 3. Who pays and why

**The buyer is the AI provider, not the firm using the AI.** Firms that use AI (deployers) send serious incidents to the provider. Your first list should be AI vendors selling hiring, credit or health tools in the EU. The proposal's target, compliance leads at user firms, is the wrong buyer.

Facts and checks (run today):

- Article 73 sets 15 days for most serious incidents, 10 days if a person died, and 2 days for widespread infringement or serious, irreversible disruption of critical infrastructure. The clock starts when the provider becomes aware. Source: secondary summaries. Check the official text on EUR-Lex.
- Regulation (EU) 2026/1744 (Digital Omnibus) took effect 27 Jul 2026, per law-firm alerts. High-risk duties for Annex III systems start 2 Dec 2027. Annex I starts 2 Aug 2028. No source says whether Article 73's start moves too. My inference: it likely follows the high-risk date.
- So buyers pay for readiness, not a current deadline. Expect about 14 months with no hard pain.
- The Commission's reporting guidance is still a draft from 26 Sep 2025. I found no final version.
- Budget signals: 54% plan AI security spend within six months (ETR, Summer 2026). Only 36% have a dedicated budget line (Open Future Forum, Aug 2026; survey of 45 people). Buyer pain for this product is unproven.

## 4. The MVP

Build in this order:

1. **Clock engine:** you enter the awareness time. It sets the deadline for the tier and sends alerts.
2. **Write-once log:** each entry stores evidence (logs, model version, inputs) and a fingerprint (hash). Each entry also stores the fingerprint of the one before it, so any edit shows.
3. **Decision log:** who decided the incident was serious, the causal-link date (when you could show the AI caused the harm), and why. Signed by a named person.
4. **Report drafts:** fills the Commission's draft template. Allows an incomplete first report, then a complete one (Article 73(5)).
5. **Export:** PDF and JSON.

- **AI model:** an open 8B model (8 billion parameters; Llama 3.1 8B or Qwen 3 8B). It reads raw notes, pulls out dates and system names, suggests a tier, and lists missing fields.
- **Human:** decides if it is a serious incident, sets the causal-link date, signs, and submits. The model never decides reportability.

## 5. What it does not do

- Give legal advice or a compliance certificate.
- Decide reportability.
- Submit anything automatically.
- Detect prompt injection or filter outputs.
- Cover duties of large general-purpose model makers (Article 55).

## 6. 30-day plan

**Days 1-5:** List 30 targets: heads of compliance, ML or product leads at AI vendors selling hiring, credit or health tools in the EU. Find them on LinkedIn and in EU AI compliance groups. Send about 40 short messages (plan, not measured).

**Days 6-30:** Hold 10 calls of 20 minutes. Ask:

1. "When one of your AI systems hurts someone, how do you find out, and who decides if it must be reported?"
2. "If a regulator gave you two days, what could you hand over today, and how long would it take?"
3. "Who owns this budget, and what would make you pay for a tool that runs the clock and keeps a signed log?"

**Day 30 goal:** one provider agrees to a free tabletop drill, a practice run on a fake incident. Spend nothing on counsel until three providers agree to a drill.

**First pilot:** run the drill, then offer a paid pilot at an assumed $500 a month (untested).

## 7. Costs and tools

Tools: Python, SQLite (a simple database), a small web app, a PDF library, Modal (rented GPUs), OpenRouter (API access to open models), Git.

Budget arithmetic (all estimates):

- Speed test: one Modal L4 GPU at $0.80/hr for about 2 hours = about $2.
- 500 synthetic cases through an 8B model on OpenRouter = under $2 (price unverified).
- Modal test runs = $1-2 (proposal estimate).
- Reserve for re-runs = $10 (assumption).
- **Subtotal with free hosting: about $16.**
- Paid hosting, if needed: up to $20 a month, so up to $60 for three months.
- **Worst case: about $76.** Inside the $100 limit. Above $50 only if you pay for hosting.

Not priced: counsel review (likely your largest real cost), your time, and the pilot fee.

Checks: the OpenRouter key has a $10 limit, and the last balance noted was $6.58 on 30 Sep (not rechecked). Modal's Starter plan includes a $30 monthly credit. It is unverified whether that covers GPU time.

## 8. Kill criteria

Thresholds are my proposals, not research.

- Fewer than 3 of 10 interviewed providers call the reporting step a current pain. **Stop.**
- No provider agrees to a drill by day 60. **Stop.**
- A governance vendor or tracker ships an authority-report clock before your first drill, and your top prospects choose it. **Stop.**
- Final Commission guidance changes the 2, 10 or 15-day tiers, or drops the template. **Pause** until rebuilt.
- The open 8B model misses a required field in over 20% of 100 test cases after prompt fixes. **Pause** the AI drafting and sell the log alone.
- No paid pilot or signed paid commitment by day 90. **Stop.**
- Spend passes $100 before a paid pilot. **Stop.**

Runner-up: Proposal A (license checker, 22 of 35) lost because its headline Llama clause binds very few companies, and each rule card needs lawyer sign-off, which makes it a services business. C scored 23.5, so this is not a tie.
