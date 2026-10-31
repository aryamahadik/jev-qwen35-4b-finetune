"""Scratch: write families/T06/G0_SPEC_v3.md from G0_SPEC.md (v2) + the plugin's card texts (run once, then freeze)."""
import sys
sys.dont_write_bytecode = True
C2 = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build"
sys.path.insert(0, C2)
from pathlib import Path
from families.T06 import plugin as T

fam = Path(C2, "families/T06")
v2 = (fam / "G0_SPEC.md").read_text(encoding="utf-8").split("\n")
V2_SHA = "4f6b322adab8a1810ac165686a2305d28607de558131118780c52da5f0e59563"


def row(prefix):
    idx = [i for i, ln in enumerate(v2) if ln.startswith(prefix)]
    assert len(idx) == 1, prefix
    return idx[0]


out = list(v2)


def put(prefix, new):
    out[row(prefix)] = new


# ---- semantics rows
s1 = out[row("| S1 |")]
out[row("| S1 |")] = s1[:-2] + ". ch_rule rows draw their periods by S10 instead (not from these sets)  |"
put("| S10 |",
    "| S10 | ch_rule | which rule gives the full refund. Options = the rules the record's coarse facts leave open plus \"none\" "
    "(the abstain option; texts per style, section 2): reject iff REASON = faulty; withdraw iff the goods are not excluded (S6); "
    "store iff the notice promises a refund for this REASON (S9); at least two rules are shown, so k = 3 or 4, in one label-blind "
    "order of the row key; a twin shows the same options as its base. Gold = the only rule that gives the refund, or none; "
    "generated only when at most one rule gives it. The target is drawn uniformly over the display before any date, so every shown "
    "option, \"none\" included, is gold on 1 / k of the rows (kit choiceplan abstain band). Windows: the target's window ends on a day "
    "drawn from 9..34 days after possession (S5: 35..45), every other window 1..3 days earlier (a refusal: all windows end within 3 "
    "days of one another, the request after the last); each period is its window's end minus its anchor lag (reject: end + days "
    "from delivery to possession; withdraw: end; notice: end + days from its anchor to possession), so no printed number says which "
    "rule wins. The request is one of the last 4 days of the target's window (refusal: one of the first 4 days after the last "
    "window) |")
s11 = out[row("| S11 |")]
out[row("| S11 |")] = s11[:-2] + (". Wording polarity (kit polarity.py P1-P3, POLARITY_CHECK; P4 off): a wording negates a positive predicate or uses an "
                                  "antonym word (refuse, decline, turn down, deny, withhold), never both; yn_double has two syntactic negations over a "
                                  "positive predicate |")
put("| S12 |",
    "| S12 | Rules (program text) | the statute excerpt in its style (section 2, one line per section) + newline + closed-world sentence "
    "\"The rules, the posted notice and the order record are complete; no other fact or message changes the case.\". On yes/no rows "
    "this is `row.card` (printed once); on choice rows it is the head of the instructions, before the question (kit cards.place_rules). "
    "Variant per row from the row key: full 25% / compact 60% / short 15% of training rows (S5: full only); compact and short keep "
    "every slot, number, operator word and negation count of full (kit cards.CardSpec problems() = []). Then a blank line and the "
    "question. No digit outside the slots. The state is a separate field; `meta.defs_style` = rules_in_card_<variant> |")
s13 = out[row("| S13 |")]
out[row("| S13 |")] = s13[:-2] + ". The three printed day counts are always written in digits (\"27 days\"), on every row, so the number of numerals says nothing about how late the request is |"
s16 = out[row("| S16 |")]
i = s16.index("Options: gold + 2-3")
j = s16.index("The gold's sorted rank")
s16n = (s16[:j] + "The option count k = 3 or 4 and the gold's position and sorted rank among the dates come from the kit's ChoicePlan "
        "of the row key (build_options plan=; twins strict_plan False), with no abstain option; an option equal to a date the record "
        "prints is not allowed (another structure is drawn, never another option) (v1 put the gold between the day-0 and one-day-late "
        "dates and \"take the second-highest date\" scored 0.71 vs chance 0.25) |")
out[row("| S16 |")] = s16n
s22 = out[row("| S22 |")]
a = s22.index("one that moves the gold onto none is kept")
b = s22.index("equiv (another skin")
s22n = (s22[:a] + "one that moves the gold onto none is kept at 0.22 (k = 3) / 0.05 (k = 4) (kit relations.abstain_twin_kept; else the next "
        "edit naming a rule is taken), so none is 1 / k of ALL emitted ch_rule rows in each k cell, not only base rows); " + s22[b:])
out[row("| S22 |")] = s22n

# ---- sections 4-7 replaced by a pointer + section 8
k4 = row("## 4. Haiku tasks")
out[k4:] = [
    "## 4-7. Unchanged from v2",
    "",
    "Haiku tasks, the ambiguity listing (A1-A16), its resolution and the Haiku ambiguity pass (H1-H52) are as in `G0_SPEC.md` (v2, sha256",
    "4f6b322adab8a1810ac165686a2305d28607de558131118780c52da5f0e59563) sections 4-7; the frozen pools_v2 were authored against v2. Of the",
    "v2 rulings only those that name a ch_rule display (H10: \"all four keys\") and the card line placement change, as S10 and S12 say. No",
    "frozen wording, skin, notice form or attack line changes; the polarity screen (S11) finds no frozen yes/no wording to quarantine.",
    "",
    "## 8. Stage B pilot fix iteration 1 (14 Oct 2026; iteration-0 verdict G6, G10 and spec 3.0 failed; no bar loosened, no label touched)",
    "",
    "1. Rules in `row.card` on yes/no rows, three variants (S12): spec 3.0 token mean 926.8 (iteration 0; bar 800) now about 777.",
    "2. ch_rule (S10): v2 showed all four keys, drew the periods before the target, and the coarse facts alone predicted the key",
    "   (card view LR 0.367 vs chance 0.262 at iteration 0). Now display = the open rules + none, target uniform over it, windows label-first; none is 1 / k",
    "   (abstain band), twins thinned per k; periods and printed counts carry no rule cue (card view at chance).",
    "3. Yes/no request day near a window end and counts always digits (S13, section 3): the metadata view (0.551 at iteration 0) no longer separates the labels.",
    "4. ch_end (S16): kit ChoicePlan for k, position and rank; options equal to a printed date are never used. G10 gold-is-longest (+2.87 pp at iteration 0): none is 1 / k in every k cell (S22).",
    "5. Polarity (S11): kit polarity check on; solver B and the tests read the new cards (G0 v3 section 2).",
    "G6 is also reported at 6,000 rows (PREREG A43): pilot_i1/G6_AT_6000.json.",
]
# ---- section 3: samplers
c = row("- **Gold.**")
out[c:c + 3] = [
    "- **Gold.** Yes/no 50 +- 2 (per form 47.9-50.9% on 12,000 specs); \"yes = bad outcome\" (bad for the buyer: yes means no full",
    "  refund, QuestionForm.yes_is_bad) 50 +- 5. ch_rule: uniform over the display (S10): none 1 / k, each shown rule (1 - 1 / k) /",
    "  (k - 1). Refund rate per goods type, reason, notice, handover and style: 44-54% on 12,000 specs.",
]
d = row("- **Draw order.**")
out.insert(d, "- **Request day (yes/no rows).** Never uniform over the days that hit the target: a refund is one of the last 4 days of an "
              "applicable window (a random one of them); a refusal with an applicable rule is one of the first 4 days after the latest "
              "window; a refusal with no applicable rule is one of the last 4 days of a period the case does not use. So the size of the "
              "printed day counts is the same in both classes (v2: refund rate 0.35 in the top decile of the mean numeral magnitude).")

dd = next(i for i, ln in enumerate(out) if ln.startswith("- **Draw order.**"))
out[dd + 6] = out[dd + 6].replace("the request day chosen among every day 1.. that realises the target (with the trap", "the request day chosen among the days that realise the target and lie near a window end (see above; with the trap")
out.insert(dd + 8, "  (yes/no and ch_end rows; a ch_rule row draws its display, then the target uniformly over it, then lags, delivery and the windows of S10.)")

# ---- traps and overlay: v3 measurements (12,000 training specs; pilot dry run)
ti = next(i for i, ln in enumerate(out) if ln.startswith("- **Traps (overlapping shares"))
oi2 = next(i for i, ln in enumerate(out) if ln.startswith("- **Overlay (measured shares"))
out[ti:oi2] = [
    "- **Traps (overlapping shares of rows, measured on 12,000 training specs; spec 3.13 target in brackets).** Stricter",
    "  notice, the statute wins 27% [25]; order date vs delivery (the order-date anchor flips the answer) 31% [20]; boundary",
    "  day (one day earlier or later flips it) 48% [20] (v3: every request sits within 4 days of a window end); conditional",
    "  exception 16% [15] (= the t06_absolute_exception mistake flips the decision: hygiene goods with the seal intact, or",
    "  excluded goods returned faulty inside the rejection period); a more generous notice decides 16% [10]. Tags go by which",
    "  rule gives the refund (stricter: the statute gives it, the notice does not and reads as refusing the case; generous:",
    "  only the notice gives it); each notice is one promise or none, so no notice is mixed. Also: delivery vs possession",
    "  anchor 12%, leap day inside the dates 11%, the request in another month than delivery 81%.",
]
oi2 = next(i for i, ln in enumerate(out) if ln.startswith("- **Overlay (measured shares"))
oe = next(i for i, ln in enumerate(out) if ln.startswith("## 4-7"))
out[oi2:oe] = [
    "- **Overlay (measured shares of emitted rows; pilot dry run of 1,001 rows, S1-S4).** Complement partners 40% of yes/no rows",
    "  (59% non-syntactic pairs); twins 20% of rows (spec 4.1: 20-25; twin rate 0.48); equiv 6%; inv 2%; deep 5%; yes 49%. Units",
    "  hold at most 3 rows. Real tokens (pinned tokenizer, rules in row.card on yes/no rows): mean about 777, max about 1,054.",
    "",
]

# ---- section 2: card texts, three variants
a = row("## 2. Card texts")
b = row("## 3. Samplers")
opt = [ln for ln in out[a:b] if ln.startswith("ch_rule option texts")]
oi = out.index(opt[0])
opt_block = out[oi:b]
sec2 = ["## 2. Card texts (program text; one line per section; solver B keeps its own copy)", "",
        "Three variants (S12). `full` is the frozen v2 card, unchanged; `compact` and `short` only drop filler. S5 uses the regulation card (full only).", ""]
for var, note in (("full", "full (25%):"), ("compact", "compact (60%):"), ("short", "short (15%):")):
    sec2 += [note, "", "```"]
    for st in ("act", "code", "charter", "regulation"):
        if var != "full" and st == "regulation":
            continue
        lines = T.CARD_TEXT[(st, var)].split("\n")
        tag = "regulation (S5 only)" if st == "regulation" else st
        sec2.append(f"{tag}: {lines[0]}")
        sec2 += lines[1:]
    sec2 += ["```", ""]
out[a:oi] = sec2

# ---- header
h0 = row("One page, as C2_DATA_SPEC 6.2")
hdr_end = row("## 1. Semantics table")
hdr = [
    "One page, as C2_DATA_SPEC 6.2 item 3 asks: a semantics table, then frozen (sha in `plugin.T06Plugin.G0_SHA256`;",
    "`validate_plugin` refuses the plugin if this file changes). **v3, frozen 14 Oct 2026, Stage B pilot fix iteration 1** (section 8):",
    "v2 (`G0_SPEC.md`, sha256 4f6b322a..., frozen 13 Oct after the one blind Haiku ambiguity pass) stays the text every pools_v2",
    "task, answer and manifest was authored against (`plugin.G0_SHA256_AUTHORED`); its sections 4 (Haiku tasks), 5 (ambiguity",
    "listing), 6 (resolution) and 7 (Haiku pass H1-H52) are unchanged and are not repeated here. v3 changes S10, S11, S12, S13,",
    "S16, S22, the card texts (section 2) and the samplers' request-day and gold rules (section 3). Any later edit needs a new",
    "sha and a pilot re-run. Target 900 selected rows (about 1,350 generated), wave 1. `solver_b.py` takes its semantics from this",
    "page and its parsing from the kit API (c2_build/README.md), never from `plugin.py`. All jurisdictions, stores, statutes and",
    "notices are invented; no UK or EU text.",
    "",
]
out[h0:hdr_end] = hdr
out[0] = "# G0-lite T06 v3: consumer return rights, non-waivable floor vs posted policy (C2 everyday tier; C2_DATA_SPEC 2.1, 3.13)"

Path(fam / "G0_SPEC_v3.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print(len(out))
