"""Build families/T07/G0_SPEC_v2.md = G0_SPEC.md (v1 + redo2 notes) with the fix iteration 1 changes (marked "(v2)") and a
section 8. Every replacement is an exact-match assert: a v1 line that moved stops the build. Prints the sha256.

  ../../.venv/bin/python -B families/T07/pilot_i1_work/make_g0_v2.py [--write] [--m KEY=VALUE ...]
"""
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
v1 = (HERE / "G0_SPEC.md").read_text(encoding="utf-8")
M = dict(x.split("=", 1) for x in sys.argv[1:] if "=" in x and not x.startswith("--"))
sha1 = hashlib.sha256(v1.encode()).hexdigest()


def rep(text, old, new):
    assert text.count(old) == 1, old[:80]
    return text.replace(old, new)


s = v1
s = rep(s, "# G0-lite T07: headline promise vs footnote qualifier (gets / misses; which condition; which offers)",
        "# G0-lite T07 v2: headline promise vs footnote qualifier (gets / misses; which condition; which offers)")
s = rep(s, "**Status: FROZEN v1 (13 Oct 2026), sha256 pinned in plugin.py (G0_SHA256).** One Haiku ambiguity pass (workflow",
        "**Status: FROZEN v2 (14 Oct 2026; fix iteration 1 of at most 2, spec 6.4 step 6), sha256 pinned in plugin.py "
        "(G0_SHA256).** v2 = v1 + section 8: `G0_SPEC.md` (FROZEN v1, 13 Oct 2026, sha256 `T07Plugin.G0_SHA256_AUTHORED`) stays "
        "as the spec the Haiku tasks, the pools and the extraction records were authored under; v2 changes no pool, no Haiku task, "
        "no solver-B text and no gold semantics (marked \"(v2)\": S17, S18, S19, section 2 lines, section 8). "
        "One Haiku ambiguity pass (workflow")
# S17: None gold 1/k, slot, twin keep
s = rep(s, "Generated only when at most one condition of the ASKED footnote fails (the other footnote is unconstrained); "
           "gold none 25%, else uniform over the asked conditions; a ch_failing twin that lands on none is kept at "
           "TWIN_NONE_KEEP = 0.10 (kit relations.abstain_twin_kept), so none stays near 25% of all emitted ch_failing rows "
           "(unthinned: 38%) |",
        "Generated only when at most one condition of the ASKED footnote fails (the other footnote is unconstrained). "
        "(v2) k = the options shown, None included (2-6). Gold none on exactly 1/k of the rows of a k-cell (1 of every k rows of "
        "that k in the sampler's stream, strata per window of 4,096 seeds; was a flat 25%, 21% at k = 2), else uniform over the "
        "asked conditions. The display slot of None is exactly uniform per k (the same strata); the dimension labels follow in a "
        "key-hash order, so a twin or an equiv / inv partner prints the very same list (G-TW). A ch_failing twin that lands on none "
        "is kept at 1/(k-1)^2 (kit relations.abstain_twin_kept), so none stays at 1/k of ALL emitted rows of a k-cell |")
s = rep(s, "gold uniform over the four outcomes. Per ch_offers seed pair: one condition under each headline 85%; else",
        "gold uniform over the four outcomes (v2: stratified by index, outcome 0 both, 1 neither, 2 only the headline whose "
        "\"Only <benefit>\" text is the longer, 3 the other; each once per 4 rows of the stream, so the gold is the longest option "
        "on exactly 1/4). Per ch_offers seed pair: one condition under each headline 85%; else")
s = rep(s, "yes = bad outcome on misses / not_gets / fails_to |",
        "yes = bad outcome on misses / not_gets / fails_to. (v2) Polarity (kit c2_kit.polarity P1-P4; plugin POLARITY_CHECK, "
        "POLARITY_NEGATIVES, strict frames): a yes/no wording negates \"get\" syntactically OR uses a negative predicate "
        "(lose out on, forfeit, fail to ...), never both, reads with its form's polarity and opens with no contracted negative "
        "frame (\"Isn't it the case that ... doesn't get ...?\" reads either way). The 6 contracted yn_dneg_gets wordings of the "
        "frozen pool (3 training, 3 held out) are quarantined at generation (T07Plugin.ctx_for), never relabelled; the pipeline "
        "refuses one that reaches a row (G-LEX); lint_wording_v2 refuses a re-authored one |")
# section 2 lines
s = rep(s, "| Controls: base specs whose asked headline holds (yes/no gets, ch_failing none, ch_offers both); A13 | 30-40 | 36.1 (H36) |",
        "| Controls: base specs whose asked headline holds (yes/no gets, ch_failing none, ch_offers both); A13 | 30-40 | "
        + M.get("controls", "?") + " (v2: none at 1/k; was 36.1) |")
s = rep(s, "| ch_failing gold none (base specs; all emitted ch_failing rows); ch_offers both / neither (base) | 20-30 | 24.4, 23.9; 25.1 / 24.9 |",
        "| (v2) ch_failing gold none per k-cell (base specs; all emitted ch_failing rows); ch_offers both / neither (base) | "
        "1/k per cell (+/- 1 row per sampler and cell; emitted rows within 5 pp of the mean 1/k; was 20-30) | "
        + M.get("cfnone", "?") + " |")
s = rep(s, "| Abstain \"None\" wrong when shown; gold position | >= 50; uniform per bucket | 76.1; chi-square p > 0.01 |",
        "| Abstain \"None\" wrong when shown; gold position | >= 50; uniform per bucket | " + M.get("abwrong", "?")
        + " (v2; was 76.1); chi-square p > 0.01 |")
s = rep(s, "| Yes = bad outcome (emitted yes/no rows); yes/no share of emitted rows | 50 +/- 5; 45-55 | 49.9; 53.2 (base specs 45.2) |",
        "| Yes = bad outcome (emitted yes/no rows); yes/no share of emitted rows | 50 +/- 5; 45-55 | " + M.get("ynbad", "?")
        + " (v2; base specs 45.2) |")
s = rep(s, "| Twins; complements (of emitted yes/no rows); non-syntactic (of complement pairs); equiv; attack | 20-25; >= 20; >= 30; 5-10; 2-6 | 21.1; 54.0; 68.2; 7.0; 3.5 |",
        "| Twins; complements (of emitted yes/no rows); non-syntactic (of complement pairs); equiv; attack | 20-25; >= 20; >= 30; 5-10; 2-6 | "
        + M.get("overlay", "?") + " (v2) |")
# section 8
s = s.rstrip("\n") + "\n\n" + """## 8. v2 notes (14 Oct 2026, fix iteration 1: pilot/ PILOT_REPORT.json, program gates; no Haiku read yet)
The first pilot (1,001 rows, 545 units) passed G2 G3 G4 G-SL G-LEX G-TW G15 G7 overlay and spec 3.0, and failed G6 (choice: every
view +4 to +6 pp over chance 0.313) and G10 (gold-is-longest -5.14 pp). One cause: None was gold on a flat 25%, i.e. 21% of k = 2 rows
and 29 / 22 / 30% at k = 3 / 4 / 5 against 1/k, and its text is always the longest option. F1 S17 and S18 above (kit lesson
STAGE_B_PILOT_REPORT "patterns across families"; no gate bar and no G0 target other than the 1/k abstain bands moved; the controls
line now reads {CONTROLS}). F2 S19 polarity (kit c2_kit.polarity; the T35 G5-H lesson). F3 not adopted: the cards (spec 3.0 length) pass
(real-tokenizer mean ~650 of 800), so `cards.place_rules` is not used, and the card text and placement stay as in S16.
Pool note: the quarantine leaves 9 of 12 training and 3 of 6 held-out yn_dneg_gets wordings usable (G0 section 4 lists 12 / 6): a re-author
(Haiku, then 2/2 G-LEX and G13-seed) with `authoring.REAUTHOR_BRIEF_DNEG` is open; every other section 4 target line is untouched.
Code: plugin.py (row_plan, twin_none_keep, offers_holds, ctx_for, POLARITY_*), authoring.py (lint_wording_v2, REAUTHOR_BRIEF_DNEG),
load_v2.py, merged_pools.py and the pool builders (they check G0_SHA256_AUTHORED), test_i1_fixes.py, run_pilot_i1.py.
""".replace("{CONTROLS}", M.get("controls", "?"))
out = HERE / "G0_SPEC_v2.md"
n = len(s.splitlines())
print("lines", n, "sha256", hashlib.sha256(s.encode()).hexdigest(), "authored(v1) sha256", sha1)
assert n <= 200, n
if "--write" in sys.argv:
    out.write_text(s, encoding="utf-8")
    print("written", out)
