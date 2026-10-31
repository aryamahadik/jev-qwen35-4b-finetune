"""Builds families/T28/G0_SPEC.md v1.2 from the byte-exact v1.1 copy (G0_SPEC.v1_1.md): the section edits of the Stage B
pilot fixes (section 10) and a mechanical reflow of the hard-wrapped paragraphs of sections 7-9 (text unchanged) so the
page stays <= 200 lines. Run from families/T28:  python3 ../../pilot_runs/T28_i1_work/make_g0_v12.py"""
import hashlib, re, sys
from pathlib import Path

HERE = Path.cwd()
src = (HERE / "G0_SPEC.v1_1.md").read_text(encoding="utf-8")
assert hashlib.sha256(src.encode()).hexdigest() == "9ec78109c7448f7bad538a0bb7e3e716fbff5a77f54d02ec7d38ebe81c1081ec"
lines = src.split("\n")


def find(prefix, start=0):
    return next(i for i in range(start, len(lines)) if lines[i].startswith(prefix))


def para_end(i):
    j = i
    while j + 1 < len(lines) and lines[j + 1].strip() and not lines[j + 1].startswith(("|", "#", "- ")):
        j += 1
    return j


def replace_para(prefix, text, start=0):
    i = find(prefix, start)
    j = para_end(i)
    lines[i:j + 1] = text.split("\n")


def joined(i, j):
    return " ".join(x.strip() for x in lines[i:j + 1])


# ---- header (v1.2 sentence)
i = find("One page (C2_DATA_SPEC 3.1")
j = para_end(i)
hdr = joined(i, j)
hdr = hdr.replace("Status: FROZEN 13 Oct 2026 after the Haiku ambiguity pass (section 9: 57 points resolved).",
                  "Status: FROZEN 13 Oct 2026 after the Haiku ambiguity pass (section 9: 57 points resolved); v1.2 frozen 14 Oct 2026 (section 10).")
hdr += (" v1.2 (14 Oct, Stage B pilot fix iteration 1): section 10 lists the changes (S23 card placement and styles; the 1/k abstain band and the "
        "display plan of ch_rule; the listed calls and label options of ch_inverted; exact yes / no and verdict balance by slot groups; cards, registers and skins dealt; R2 wording "
        "polarity); no gold or semantics of S1-S22 changed. The v1.1 text the Haiku task files and pools_v2 were authored under is kept byte-exact in "
        "`G0_SPEC.v1_1.md` (`plugin.T28Plugin.G0_SHA256_AUTHORED`).")
lines[i:j + 1] = [hdr]

# ---- S19, S20 (table rows) and the new row S23
k = find("| S19 | ch_rule |")
lines[k] = ('| S19 | ch_rule | options = every rule id + "No rule applies (the default verdict is used)", k = n + 1 options, the default option shown on every row, '
            'in one label-blind order of the row key (a twin shows the same list); gold = the deciding rule (S8-S13); rows with a tied deciding rule are never '
            'generated. v1.2 display plan: n (the rule count, within the sampler\'s range) and whether the gold is the default option are drawn from the row key '
            'BEFORE the structure: the default is the gold on 1/k of the rows (the 1/k band, per k; so it is not predictive and gold-is-longest stays 1/k); solver A '
            'confirms, a structure that misses the plan is redrawn, never relabelled |')
k = find("| S20 | ch_inverted |")
assert "3-5 candidate calls as options (function-call text, no role); exactly one gets allow" in lines[k]
lines[k] = lines[k].replace("3-5 candidate calls as options (function-call text, no role); exactly one gets allow",
                            "3-5 candidate calls (function-call text, no role; k drawn from the row key) listed in the state; exactly one gets allow", 1)
lines[k] = lines[k].rstrip(" |") + (". v1.2: the state lists the calls in a block \"Calls to review:\" (lines `Call i: <function call>`, i = 1..k, in a label-blind order; it takes the call block's place in the "
                                    "layout) and the options are the labels `Call i` (a closed set in one label-blind order of the row key), so no option text can be matched to the policy: with the calls "
                                    "as options the gold call shared its tool and argument tokens with the policy far more than the wrong ones did (G6 card view, 5,000 pilot rows: +36 pp over chance "
                                    "on these rows; the gold had the most overlap in 78% of them) |")
k = find("| S22 | Solvers |")
lines.insert(k + 1, ('| S23 | Card placement and styles (v1.2) | the card (section 4) is printed once: in `row.card` on a yes/no row, at the head of the instructions (then a blank line '
                     'and the wording) on a choice row, because the served prompt prints `row.card` once on a yes/no row and the instructions twice (spec 3.0: family mean <= 800 '
                     'rendered tokens; the first pilot read 838.4 before this fix). Two styles, drawn from the seed and the sampler only (one per relation unit): full 85%, short 15% '
                     '(spec 3.0 "a short or no card on about 15% of rows"; no "none" style, every rule the answer needs is stated). The short style shortens four lines (section 4) and '
                     'changes no rule. `meta.defs_style` = `rules_in_card_<style>` / `rules_in_instructions_<style>` |'))

# ---- section 2 construction paragraph
i = find("Construction (label-first, display-blind)")
j = para_end(i)
old = joined(i, j)
old = old.replace("with j the slot's index among the block's slots of its form, the verdict is EFFECTS[(j + b) % 3] (EFFECTS = allow, ask, deny) and the yes/no target is yes iff (j + b) % 2 == 0; a \"no\" target takes its verdict from the two other effects, alternating by ((j + b) // 2 + b // 5) % 2.",
                  "with j the slot's index among the block's slots of its form (verdict rows) and g its index among all 18 yes/no slots of the block (v1.2: yes/no slots 2m and 2m + 1 have opposite targets, so a block holds exactly 9 yes and 9 no targets), the verdict is EFFECTS[(j + b) % 3] (EFFECTS = allow, ask, deny) and the yes/no target is yes iff (g + b) % 2 == 0; a \"no\" target takes its verdict from the two other effects, alternating by ((g + b) // 2 + b // 5) % 2.")
assert "(g + b)" in old
old = old.replace("gold position uniform per option count;", "gold position uniform per option count; ch_rule: \"No rule applies\" is the gold on 1/k of its rows, per k (S19);")
v12 = ("Overlay and deal (v1.2): complement, equiv, inv and twin presence, the twin's target and the verdict rows' mask draw (S17) are hashed per slot GROUP, never per seed: "
       "yes/no slots in pairs (2m, 2m + 1), verdict slots in triples (3m .. 3m + 2) of one block, any other slot alone; a group's targets (opposite yes / no; three different verdicts) "
       "meet the same overlay and cancel, so the yes rate and the verdict thirds are exact before drops. A verdict row's twin takes the verdict base + 1 or base + 2 (one step per "
       "group); a which-rule row's twin is the default option with probability 1 / (k - 1) when its base is a rule (the abstain gold stays 1 / k over bases and twins). Cards (spec 3.0): a card "
       "is one (sampler, pack); each training pack serves one or two training samplers (a circular window of ceil(1.5 m / 4) of the m sorted training pack ids per sampler; the pack is "
       "drawn from the seed alone), so 46 packs give 72 cards, about 14 rows each per 1,000 rows and 50 per 3,600. Registers and skins are dealt (spec 3.0: each register <= 15% of the rows, "
       "each skin <= 6 rows): in every aligned run of 8 seeds of a sampler each training register comes up once, in a seeded order, and a register's skins are used once each, in a "
       "seeded order, before any repeats (S5: the 2 held-out registers).")
lines[i:j + 1] = [old, v12]

# ---- section 3: R2
i = find("Complement partners (same spec, same skin, label-blind kind)")
r2 = ("R2 (v1.2, wording polarity; c2_kit.polarity P1-P4, plugin `POLARITY_*`): a yes/no wording must read with its form's declared polarity, a rule negcount's closed lexicon cannot see. "
      "A ban word (off-limits, forbidden, banned, barred, prohibited, blocked, withheld and their verb forms) counts as one negation layer: next to a syntactic negation it is refused (P1: two layers the form does "
      "not declare), and alone it flips the wording's polarity (P2; G0 section 3's own R1 already keeps ban words out of yn_deny); yn_mustnot's own phrasing carries one negation (`POLARITY_BASE`, so yn_mustnot_syn reads two: P2); contracted negative question frames (\"Isn't it ...\") are refused "
      "(P3); yn_deny_ant (an antonym word, no negation) and the option-framing forms are exempt; strict \"aux + subject + not\" frames stay allowed (P4 off: \"Is the agent not free to ...?\" is "
      "one plain negation of the predicate). `plugin.ctx_for` screens the pool label-blind (a failing wording is never picked) and a failing wording that reaches a row fails G-LEX. Lead "
      "ruling on the 1 flagged wording (quarantined, never relabelled): `T28-WD-q.t28.yn_mustnot#3dfd0fe3` (\"... amount to a flat ban, given it must not make the call ...\": a ban word "
      "and \"must not\"; 12 yn_mustnot wordings remain). The two held-out fixture wordings that used \"off-limits\" (tests only, never a pool) were re-worded.")
lines.insert(i, r2)

# ---- section 4: card paragraph (placement + short style)
i = find("Card (instructions, one line each in this order, then a blank line and the wording)")
lines[i] = lines[i].replace("Card (instructions, one line each in this order, then a blank line and the wording):",
                            "Card (S23: `row.card` on a yes/no row, the head of the instructions on a choice row, then a blank line and the wording; one line each in this order):", 1)
j = para_end(i)
card = joined(i, j)
card += (" Short style (v1.2, S23; every other line is verbatim): (1) \"A rule applies when its tool pattern matches the tool name and every condition listed with it holds; a condition about an "
         "argument or session role that the call does not include does not hold.\" (3) \"Owner values: an owner argument names who owns the item the call acts on; \"self\" is the requesting "
         "user, the user the agent works for; \"other\" is someone else.\" (5) tool_first \"Specificity: compare tool patterns first (an exact tool name beats a namespace pattern such as ns.*, "
         "which beats *); if they tie, more conditions is more specific. If two applicable rules are equally specific, deny beats ask and ask beats allow.\" or conds_first \"Specificity: "
         "compare the number of conditions first (more is more specific); if they tie, an exact tool name beats a namespace pattern such as ns.*, which beats *. If two applicable rules are "
         "equally specific, deny beats ask and ask beats allow.\" (8) \"Verdicts: allow = make the call without asking; ask = ask the user, then make the call only after the user confirms; deny = do "
         "not make the call.\" c2_kit.cards.variant_problems checks every pair (same slots, quoted literals, numbers, operator words and negation count).")
card += (" Inverted rows (S20, v1.2) have no call block: the block \"Calls to review:\" lists `Call i: T(...)` (the function-call text, i = 1..k in order), at the call block's place "
         "in the layout, and the options are `Call i`; an attack line, if any, closes the policy block.")
lines[i:j + 1] = [card]

# ---- section 6: partners per group
i = find("Complement (section 3). Minimal-edit twin")
t = joined(i, para_end(i))
t = t.replace("Units <= 3 rows; twins have their own call_id.",
              "Units <= 3 rows; twins have their own call_id. v1.2: which slot has which partner is hashed per slot group, and a twin's target is planned (section 2).")
lines[i:para_end(i) + 1] = [t]

# ---- reflow sections 7-9 (text unchanged): join each hard-wrapped bullet / paragraph
def reflow(start_prefix, end_prefix):
    a = find(start_prefix)
    b = find(end_prefix, a + 1) if end_prefix else len(lines)
    out, cur = [], None
    for x in lines[a + 1:b]:
        if not x.strip():
            if cur is not None:
                out.append(cur)
                cur = None
            out.append(x)
        elif x.startswith("- ") or cur is None:
            if cur is not None:
                out.append(cur)
            cur = x.rstrip()
        else:
            cur += " " + x.strip()
    if cur is not None:
        out.append(cur)
    lines[a + 1:b] = out


reflow("## 7. Haiku authoring", "## 8.")
reflow("## 8. Ambiguity points", "## 9.")
a = find("## 9. Resolution")
body = " ".join(x.strip() for x in lines[a + 2:] if x.strip())
chunks, cur = [], ""
for tok in re.split(r"(?<=\.) (?=H\d)", body):
    if len(cur) + len(tok) > 900 and cur:
        chunks.append(cur)
        cur = tok
    else:
        cur = (cur + " " + tok) if cur else tok
chunks.append(cur)
lines[a + 2:] = chunks

# ---- section 10
lines += ["", "## 10. v1.2: Stage B pilot fix iteration 1 (14 Oct 2026; STAGE_B_PILOT_REPORT patterns; the first T28 pilot, `pilot/PILOT_REPORT.json`)", "",
          ("Pilot 0 (1,000 rows, 563 units; G2-G4, G-SL, G-LEX, G-TW, G15, schema and options: 0 failed units) failed three gates: G7 (3 card-adjusted features: \"agent under\", \"user or\", "
           "`yn_allow_opt`; the 400 cards held 2.5 rows each, so the leave-one-out card null is nearly deterministic), G10 (yes rate 0.4768, bar 48-52) and spec 3.0 (mean 838.4 real tokens); "
           "its report also showed a register at 17.7% (bar 15%), 400 cards and an abstain option with no 1/k band. Fixes, generator and program text only, no label set: (F1) S23 card placement "
           "and the short style, solver B reads the rules through `cards.split_rules` and both styles; (F2) exact yes / no and verdict balance by slot groups (section 2: the g index, per-group "
           "overlay, planned twin targets); (F3) cards = (sampler, pack) over circular pack windows, registers and skins dealt; (F4) the ch_rule display plan (S19, the 1/k abstain band) and the "
           "ch_inverted listing (S20: the calls listed in the state, the options `Call i`); (F5) wording polarity R2 (1 wording quarantined). Section 9's resolutions H1-H57 are unchanged. The re-pilot is `pilot_i1/` (its report holds the "
           "numbers).")]
# ---- wrap every free paragraph (not a table row, heading or blank) at 300 characters: one page, readable lines
import textwrap
out = []
for x in lines:
    if not x.strip() or x.startswith(("|", "#")) or len(x) <= 300:
        out.append(x)
    elif x.startswith("- "):
        out += textwrap.wrap(x, 300, subsequent_indent="  ", break_long_words=False, break_on_hyphens=False)
    else:
        out += textwrap.wrap(x, 300, break_long_words=False, break_on_hyphens=False)
lines = out
(HERE / "G0_SPEC.md").write_text("\n".join(lines).rstrip("\n") + "\n", encoding="utf-8")
n = len((HERE / "G0_SPEC.md").read_text(encoding="utf-8").split("\n")) - 1
print("lines", n, "sha", hashlib.sha256((HERE / "G0_SPEC.md").read_bytes()).hexdigest())
