# Build spec: fix-proof app for GitHub (Proposal B)

> **Status: draft, not chosen yet.** Proposals B and E tied at 24 of 35. This spec is for B because it sorted first. Run the Week 1 test in section 5 before writing product code.


**Terms:** *PR* = pull request, a proposed code change. *Draft PR* = a PR not yet ready to merge. *Retest* = running a check again after a fix. *SOC 2 / PCI DSS* = security audits for software firms and card payments. *DPA* = data processing agreement, the contract on how a vendor handles customer data. *GHAS* = GitHub Advanced Security, a paid scanning add-on.

## 1. The idea in one sentence

A GitHub app that scans a startup's code, drafts a fix as a draft PR, reruns the check to prove the fix works, and exports that proof as audit evidence.

## 2. Who pays and why

- **Buyer:** software firms of 20 to 200 staff that must show SOC 2 or PCI controls. The report says these firms "need evidence for PCI or SOC 2" and want "proof a fix worked" (section 4, points 1 and 2).
- **Size:** the report puts the 20 to 499 staff slice at about $1.3B a year for about 81,700 buyers (section 3; range $0.5B to $2.7B; unverified). It does not size our 20 to 200 software slice. Assume it is a fraction of that.
- **Price reference:** Aikido lists a $4,000 typical pentest (section 1; unverified). We do not sell pentests, so this is only a reference.
- **Catch:** GitHub's agentic autofix needs GHAS and a Copilot license (per a search summary of GitHub's docs; not read in full). Teams that already pay for these may get a basic rerun free. Aim at teams without them, or teams that need an exported audit record.

## 3. The MVP

**Software:**
1. **Scope lock.** The customer signs a scope record naming repos. The app refuses any other repo.
2. **Scans.** Runs on each PR and once a week, using open-source scanners such as Semgrep. Check each tool's license for commercial use.
3. **Draft fix.** The model drafts a patch and opens it as a draft PR. Nothing merges by itself.
4. **Fix proof.** Reruns the failing check on the patched commit. Logs pass or fail with the commit ID.
5. **Evidence export.** A retest record (PDF or CSV) mapped to SOC 2 or PCI control IDs, with a sign-off field.

**AI model** (hosted API or open-weight): reads diffs and scanner output, removes false positives, drafts patches and report text. It writes no exploits.

**Human:** you, then a paid reviewer. You approve scope, review each fix PR, and sign each retest record.

**The must-win point:** GitHub's changelog (10 Jul 2026) says autofix reruns "the original analysis" with CodeQL before opening a draft PR. The report's claim that this rerun covers only the default query suite is unconfirmed. I found no source either way. Our edge must be checks GitHub's rerun does not run, such as a second scanner or extra rules. Week 1 tests whether those checks catch anything extra.

## 4. What it does not do

- Exploit anything or attack live systems. It reads code and reruns checks in a build.
- Touch any repo outside the signed scope.
- Use uncensored models or remove safety settings.
- Train models or train on customer code. Use a provider with a no-training clause.
- Claim SOC 2 or PCI compliance. Only an auditor can say that.

## 5. 30-day plan

**Week 1: the 10-repo test, before you write the app.** Pick 10 repos you own or that owners approve in writing. Enable GHAS where needed. On each, run your scanner and GitHub's autofix. Count the flaws each finds and how many fixes pass the rerun.

**Weeks 1 to 2: the first 10 customer conversations.** Contact CTOs or heads of engineering at 20 to 200 person SaaS firms in a SOC 2 or PCI process. Get names from startup-focused SOC 2 auditors (ask for referrals) and founder communities. Ask:
1. How do you handle scanner findings today, and how long until a fix is verified?
2. What did your last SOC 2 or PCI audit ask you to show for fixes or retests?
3. If a tool gave you a draft fix and a signed retest record, what would the auditor need to see before accepting it?

Write each answer in one shared sheet.

**Weeks 2 to 4: the first pilot.** Build the thinnest version: scope lock, one scanner, one language, fix proof (estimate: 3 to 4 weeks). Then offer a free two-week pilot on one customer repo, in exchange for a written case study. Paid pilots come after that. The proposal assumes $1,000 for three months (untested).

## 6. Costs and tools

Every number is an assumption unless marked as arithmetic.
- Model API: $3 per million tokens (assumed). 200 PRs at 100K tokens each is 20M tokens, about $60 a month (my arithmetic).
- Hosting and CI: $100 a month (assumed).
- Running cost: about $160 a month (estimate).
- Lawyer review of terms and DPA: $1,500 once (assumed).
- Cyber insurance: $2,000 a year (assumed, no quote).
- Year-one cash: about $5,400 (my arithmetic). The proposal's $3,000 to $5,000 does not match its own inputs.
- Tools: a GitHub App (free to create; check GitHub's terms), Semgrep or CodeQL (check licenses), a model API, a small cloud host, a billing service.
- Your time: 8 to 10 weeks (estimate).

## 7. Kill criteria

Stop or pivot if any of these happen. Thresholds I chose are marked "mine."
1. GitHub's autofix rerun catches every flaw our checks catch in the 10-repo test. Stop and move to Proposal E.
2. Fewer than 70% of drafted fixes pass the rerun (the proposal's assumed bar).
3. Two or more SOC 2 or PCI auditors say they will not accept the retest record (mine).
4. Zero of 10 conversations name an audit deadline that a fix-proof record would help (mine).
5. No paid pilot by day 90 (mine).
6. Any run touches a repo outside signed scope. Stop all runs until the bug is fixed and reviewed.

## 8. Where the swarm idea fits

Not now. CAISI scored GLM-5.3, the strongest open-weight model it tested, at 9.4% on ExploitGym, against 44.4% for the best US model (report, section 2). Open-model swarms will be weak at exploit work. Later, a read-only swarm could triage findings inside this product. Exploit-style testing stays gated: Anthropic's Red Team tier covers only systems the customer is authorized to test, and your eligibility is unverified (section 2).

**Runner-up:** Proposal E (scope-and-authorization layer). It ties B at 24 in the ranking list, though the judges' notes give other scores. It lost on buyer pull: nothing forces a firm to buy, and its $500 monthly price is untested.

## Appendix: how the five proposals scored

Two judges scored each proposal 1 to 5 on seven criteria (maximum 35). One judge was a skeptical investor, the other an engineer who has to ship it.

| Proposal | Investor | Engineer | Average |
|---|---|---|---|
| B: fix-proof GitHub app | 24 | 24 | 24 |
| E: scope and authorization layer | 26 | 22 | 24 |
| A: AI-assisted pentest service | 24 | 21 | 22.5 |
| C: EU CRA triage | 18 | 20 | 19 |
| D: open-source bounty triage | 19 | 17 | 18 |

B and E are tied. The investor preferred E and the engineer preferred B. Both judges gave B the same seven scores.

Per criterion for the two finalists (investor / engineer):

| Criterion | B | E |
|---|---|---|
| Buildable by one student | 4 / 4 | 4 / 3 |
| First paying customer | 3 / 3 | 2 / 2 |
| Low legal risk | 4 / 4 | 4 / 3 |
| Demand evidence | 2 / 2 | 3 / 2 |
| Differentiation | 2 / 2 | 3 / 3 |
| No exploit dependency | 5 / 5 | 5 / 5 |
| Student fit | 4 / 4 | 5 / 4 |

**Main objection to B (both judges):** GitHub's autofix already reruns CodeQL before it opens a draft PR. The changelog says so. B has to catch flaws that GitHub's rerun misses, and nothing in the research shows auditors accept a tool-made retest record.

**Main objection to E (both judges):** Nothing forces a firm to buy, and the scope gate can be bypassed by scanners that skip the proxy.

**Not yet researched:** AI code-fix tools from Snyk, Semgrep and Aikido. They compete directly with B and should be checked before Week 1 ends.
