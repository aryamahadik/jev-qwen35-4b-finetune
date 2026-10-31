"""scratch: build G0_SPEC_v2_2.md from the frozen v2.1 text (G0_SPEC.md, unchanged) plus the iteration-1 edits."""
import hashlib, sys
src = open('G0_SPEC.md', encoding='utf-8').read().split('\n')
out = list(src)

def row(prefix):
    for i, l in enumerate(out):
        if l.startswith(prefix):
            return i
    raise KeyError(prefix)

# ---- header paragraph (lines 2-8) -------------------------------------------------------------------------------
hdr_start = 2
hdr_end = row('**Labels on this page:**')
new_hdr = '''One page (C2_DATA_SPEC 3.15, 3.0, 4, 6.2 item 3; PREREG A37, A38). **v2.2, FROZEN 14 Oct 2026** (fix iteration 1 of at
most 2, spec 6.4 step 6, after the Stage B pilot verdict FIX: F1 premise wordings, F2 pack assignment, F3 length, F4 G6).
v2.2 = v2.1 + section 7: `G0_SPEC.md` (v2.1, frozen 13 Oct 2026, sha256 `T12Plugin.G0_SHA256_AUTHORED`) stays as the
spec the Haiku tasks, the pools (`pools/`, `pools_v2/`) and the extraction records were authored under; v2.2 changes
no pool, no Haiku task and no gold. Changed items: R1, R2, R6-R8, R12-R16, R18, R20-R22, R24, R25, R27 (marked
v2.2). The sha256 of THIS file is `T12Plugin.G0_SHA256`; validate_plugin() refuses the plugin if it changes. Plugin
`plugin.py` (solver A: rules.RuleSet first_match over a Decimal rule AST, paradigm rule_engine); `solver_b.py` (its own
parser, reads rules through cards.split_rules, + sqlite tables joined by line, integer cents, paradigm sql_sqlite) is
written from this page only; `authoring.py` + `wording_screen.py` (authoring checks, the generation-time wording screen).'''.split('\n')
out[hdr_start:hdr_end] = new_hdr

def setrow(prefix, text):
    out[row(prefix)] = text

# ---- semantics rows ---------------------------------------------------------------------------------------------
setrow('| R1 |', '| R1 | Documents | purchase order: PO_ID (id), VENDOR (name), n = 1-4 lines (v2.2 training weights 30 / 35 / 22 / 13%), each ITEM (name: no digit, comma, semicolon or pipe; distinct in a row), ordered quantity PO_Q (count 2-200, unit from the closed list bag box bottle carton case crate drum kit pack pallet ream roll set spool tube unit), PO unit price PO_P (integer cents > 0, drawn in the pack item\'s band, 200-100,000 cents). Goods receipt, exactly one per PO: GR_ID and per line the received quantity RCV_Q = PO_Q - shortfall, shortfall 0-3 clamped to PO_Q - 1 (so RCV_Q >= 1); it names no PO, vendor, item or date (its lines are the PO\'s lines by number, and the unit prints with the quantity). Invoice: INVOICE_ID, PO_ID (the PO it bills), per line INV_Q (1..PO_Q + 3) and INV_P = PO_P + D (cents > 0); it names no vendor and no date. INV_Q > PO_Q is generated only where RCV_Q = PO_Q; RCV_Q < INV_Q <= PO_Q also occurs (1.7% of rows) and fails (R4). Identity holds by construction and is not a check: the invoice names the PO_ID of the PO, the receipt is the PO\'s one receipt, every document lists the same line numbers and units, the PO and the invoice the same items (solver B refuses a row where they differ). Paid-invoice register REG_1..REG_m (m 2-4 invoice numbers, nothing else, same vendor) shown iff the duplicate check is on the card. No document carries a date (v2.2: no rule reads one; A13 and H26 cannot arise) |')
setrow('| R2 |', '| R2 | Printed intermediates | PO_TOTAL = the sum of PO_Q x PO_P over the lines and INV_TOTAL = the sum of INV_Q x INV_P, printed as the last row / line of the PO and of the invoice. Unit prices and both document totals are always printed; no line total is printed (v2.2: no check reads one), no tax, no freight. Solver B re-derives both totals from quantities and unit prices and checks them against the text |')

i = row('| R6 |'); out[i] = out[i].replace('(dup; on 50% of rows)', '(dup; on 40% of rows, v2.2)')
i = row('| R7 |'); out[i] = out[i].replace('(limit; on 50% of rows)', '(limit; on 40% of rows, v2.2)')
i = row('| R8 |'); out[i] = out[i].replace('dup and limit are each on the card on 50% of rows (independent seeded draws per row)', 'dup and limit are each on the card on 40% of rows (v2.2; independent seeded draws per row)')
assert '40% of rows (v2.2; independent' in out[i]

setrow('| R12 |', '| R12 | Card text (program; v2.2) | one block of lines, printed from `row.card` on yes/no rows (the prompt prints it once, as the definitions) and at the head of the instructions on choice rows (then a blank line and the question, the last paragraph); cards.place_rules. Style from the row key (cards.draw_style, label-blind): full 85%, short 15% (spec 3.0 "a short or no card on about 15% of rows"). Lines: header "AP policy of {ORG}: each invoice gets exactly one action." (short "{ORG} AP policy: each invoice gets exactly one action.") / per check, in the listed order, "{1.\\|-} {Quantity check\\|Price check\\|Duplicate check\\|Approval-limit check}: {cond}. If it fails: {hold for receipt\\|price-variance review\\|reject as a duplicate\\|route to a senior approver}." (short titles Quantity, Price, Duplicate, Approval limit; S3: table "\\| check \\| passes when \\| if it fails \\|" with the same cells) / "Check order: {ORDER}." where ORDER is the row\'s check names (quantity, price, duplicate, approval limit) in the check order joined by ", then " / {PREC} / "If every check passes: release for payment, the only action that pays. Lower invoiced prices always pass." (short: "... the only paying action. ...") / "Amounts: {CURRENCY code}, whole cents." / [answer codes] / "Nothing else applies: the policy and the documents shown are complete." (closed world). No "Checks:" heading. Both styles keep every slot, operator word and the negation count of the full phrasing (cards.variant_problems) |')
setrow('| R13 |', '| R13 | Conditions (program; v2.2) | qty "invoiced quantity is at most received quantity on every line" (short "invoiced quantity at most received quantity on every line"); price "invoiced unit price minus PO unit price is {TOL_CMP}[ of the PO unit price] on every line" (both styles; TOL_CMP bound to TOL_PCT, e.g. "3 percent", or to TOL_AMT, e.g. "$0.50"); dup "the invoice number is not in the paid-invoice register (exact match only)" (short "invoice number not in ..."); limit "the invoice total is {LIMIT_CMP} (limit of approver {APPROVER})" (short "invoice total is ...") |')
setrow('| R14 |', '| R14 | State blocks (program, blank-line separated; v2.2) | the narrative skin; PO, goods receipt, invoice and register, all in one container per row: key-value ("- line 1: item; 40 cases at $12.50"), markdown table, CSV export (amounts as 1234.50) or minified JSON (no space after "," or ":"; integer cents in keys ending in _cents). Heads: "Purchase order {PO_ID} from {VENDOR}" (table, csv, json: vendor field); "Goods receipt {GR_ID}" with lines "received {RCV_Q}" and no item column; "Invoice {INVOICE_ID} for purchase order {PO_ID}" (table "\\| purchase order"; csv po_number; json po_number); the document total is the last row ("- order total: ", "- invoice total: ", "\\| total \\| \\| \\| X \\|", "total,,,X", total_cents). Order: S1 / S2 / S5 narrative, PO, GR, invoice, register; S3 documents first, narrative last; S4 narrative, invoice, register, PO, GR. A pressure line (inv twins) is the last block and carries no fact. The narrative is one block that never starts with "Invoice", "Purchase order", "Goods receipt" or "Paid-invoice"; a json / yaml / log narrative is the narrative written as a small JSON object / YAML mapping / log line holding only narrative slots, never a document (document blocks are program text with their own heads, e.g. "Invoice (JSON):") |')

i = row('| R15 |')
assert 'gold uniform over the card\'s actions' in out[i]
out[i] = out[i].replace('gold uniform over the card\'s actions.', 'gold uniform over the card\'s actions: v2.2 draws it label-first from the seed, balanced exactly (+- 1) over any run of consecutive seeds inside a block of 4,096 seeds, the four training samplers taken together (S5 on its own), for each check set, so every action is gold 1 / k and a 1,000-row sample is not unbalanced by chance (a reader of the options alone learns such imbalances: Stage B patterns, G6).')
assert 'balanced exactly' in out[i]
i = row('| R16 |')
assert 'gold = the one failing line (75%) or none (25%)' in out[i]
out[i] = out[i].replace('gold = the one failing line (75%) or none (25%)', 'gold = "None of the lines" with probability 1 / (n + 1) for n PO lines (v2.2, a label-blind draw from the row key; was 25%), else the one failing line, uniform over the lines, so each of the k = n + 1 options is gold 1 / k of the time, balanced exactly (+- 1) per line count as in R15, and no option text carries a prior (a none option whose gold share differs from 1 / k leaks, Stage B patterns; for n = 1 the item was gold 75%)')
out[i] = out[i].rstrip(' |') + '. v2.2 wording rule (pilot F1): a ch_price_line wording never says what drives, shapes, decides or settles the result or what the policy\'s treatment points to (the gold ignores which check decides: on 8 of 1,001 pilot rows an earlier check decided and the literal answer to a "drives the result" wording was "none"); `wording_screen.py` quarantines such wordings (never relabels), 4 of the 18 in the pool |'
i = row('| R18 |')
out[i] = out[i].rstrip(' |') + '. v2.2: these two forms never tie the price check to the policy\'s decision ("does what the policy decides mean it fails ..."), screened like R16 (2 pool wordings) |'

setrow('| R20 |', '| R20 | Shares (base rows; v2.2) | ch_action 45, ch_price_line 10, yn_release 11.5, yn_dneg_release 3.5, yn_payment_stopped 5.5, yn_not_release 3.5, yn_within_tol 7, yn_over_tol 4, yn_price_review 10 (%; a golden-ratio sequence over seeds; yes/no 45% of base specs, was 42%, which puts the family at 50 +- 2% yes/no after the complements: length, spec 3.0). A card is one sampler\'s card c of 8 (10 on S5; v2.2, was 16): pack (the global card number (sampler index) x 8 + c indexes the pack list: the 32 training cards use 32 distinct packs, the 10 S5 cards 10 others), tolerance kind, document container (c mod the number of the sampler\'s containers), block order; checks, order and comparators vary per row. The card\'s rate r = 0.2 + 0.6 (rank + 0.5) / 8 for the card\'s seeded rank (spread evenly over 20-80%, family mean exactly 50%); a yes/no row on the card is gold yes with probability r. Complement on 65% of released-predicate bases (yn_release -> not_release 30 / payment_stopped 35 / exception_route 35; dneg -> not_release; payment_stopped -> release; not_release -> release or dneg) and 55% of price_ok bases. No abstain option (gold share 0): the "None of the lines" option of ch_price_line is an ordinary answer whose gold share is 1 / k (R16), the kit choiceplan\'s abstain rule realised directly |')

i = row('| R21 |')
assert 'S5 held out' in out[i]
out[i] = out[i].replace('S1 forward (kv / table);', 'S1 forward (kv / table; v2.2: S1 and S2 draw the skin register by a low-discrepancy step over the seed (label-blind) with weights memo 25%, ticket 25%, the other six training registers 8.3% each, so that with S3 and S4 every training register is about 12.5% of the family, spec 3.0 <= 15%; the skin within the register and the question wording are picked round-robin over a block of 4,096 seeds, label-blind (a seeded permutation of the candidates), so that every candidate is used once before any is used twice: spec 3.0 each skin <= 6 rows, each wording <= 2%);')
assert 'weights memo 25%' in out[i]

i = row('| R22 |')
out[i] = out[i].replace('(tags; spec target; measured on 2,000 training specs)', '(tags; spec target; measured on 1,170 training units, v2.2)')
out[i] = out[i].replace('totals_match_lines_differ 25% / 25.3% (label-blind plan: every PO quantity billed, any price move compensated on a second line); two_fail (two or more checks fail) 20% / 18.2% (label-blind plan); at_tolerance 20% / 24.5% (a line exactly at T: passes under cmp.le, fails under cmp.lt). Reported: wrong_base_trap 35.5%, display_order_trap 4.4%, line_by_line_trap 7.9%, totals_trap 24.3%, salience_trap 9.1%, near_miss_duplicate 22.0%, shortfall_billed_ok 47.2%, price_below_po 43.1%, qty_boundary 16.9%, limit_at_boundary 8.8%', 'totals_match_lines_differ 25% / 25.6% (label-blind plan on >= 2-line rows, probability 0.50 in v2.2: every PO quantity billed, any price move compensated on a second line); two_fail (two or more checks fail) 20% / 20.3% (label-blind plan, probability 0.52); at_tolerance 20% / 24.4% (a line exactly at T: passes under cmp.le, fails under cmp.lt). Reported: wrong_base_trap 31.4%, display_order_trap 6.1%, line_by_line_trap 8.0%, totals_trap 26.2%, salience_trap 8.9%, near_miss_duplicate 16.8%, shortfall_billed_ok 40.1%, price_below_po 37.5%, qty_boundary 20.5%, limit_at_boundary 6.6% (v2.2 distribution, 1,170 units)')
assert '25.6%' in out[i]

i = row('| R24 |')
t = out[i]
t = t.replace('drawn on 42% of base specs', 'drawn on 50% of base specs (v2.2; none for ch_price_line: the twin of a none row is an item row and the other way round, so twins inverted the 1 / k balance of R16)').replace('equiv drawn on 11% of base specs', 'equiv drawn on 14% of base specs (v2.2)')
t = t.replace('G4: rename the vendor, rename the buyer, reverse the line order (lines renumbered in printed order in all three documents at once, so the join by number holds), shift both dates by 7 days ("same"), reverse the check order', 'G4: rename the vendor, rename the buyer, rename the approver (limit check on the card), reverse the line order (lines renumbered in printed order in all three documents at once, so the join by number holds), reverse the check order (v2.2: no date exists to shift)')
t = t.replace('The answer is predicted from the base truths with that one check flipped;', 'Among the candidates the new answer is drawn first, uniformly over the answers they can reach, then a candidate that reaches it (v2.2: a uniform draw over candidates over-weighted hold / review, n lines giving n price and n quantity candidates, and made the longest ch_action option text gold 8 pp too often on twins). The answer is predicted from the base truths with that one check flipped;')
assert 'new answer is drawn first' in t
assert 'rename the approver' in t and '50% of base specs' in t and '14% of base specs' in t
out[i] = t

i = row('| R25 |')
out[i] = out[i].replace('totals and line totals are printed', 'the document totals are printed')
assert 'the document totals are printed' in out[i]

setrow('| R27 |', '| R27 | Length (v2.2) | every row <= 2,000 rendered tokens and the family mean <= 800 (spec 3.0; the real Qwen3.5-4B tokenizer through c_build/mixer.token_counts: the cygnet prompt prints the instructions twice and `row.card` once). v2.1 measured 1,075.4 (max 1,521) at 1,001 pilot rows. The v2.2 levers, in order of size: the rules of yes/no rows in `row.card` (printed once, -106 tokens), no line totals, no dates, a one-line header, receipt lines without items, no "Checks:" heading, minified JSON, 1-4 PO lines at 30 / 35 / 22 / 13%, dup and limit on 40%, yes/no 45% of base specs, 8 cards per sampler. Measured on 2,100 rows of the v2.2 generator before the freeze: mean 756.7, max 1,187 |')

# ---- balance paragraph -----------------------------------------------------------------------------------------
b0 = next(i for i, l in enumerate(out) if l.startswith('**Balance (measured'))
b1 = next(i for i, l in enumerate(out) if l.startswith('## 2.'))
bal = '''**Balance (v2.2, measured on 1,170 relation units of S1-S4 over the pool ctx, 2,100 rows).** yes/no 51.3% of rows; gold yes
49.9%; yes = bad 53.1% (share of yes/no rows whose form reports a bad outcome by yes: yn_not_release, yn_payment_stopped,
yn_exception_route, yn_over_tol, yn_price_review; spec 3.0: 50 +- 5); k_syn >= 1 on 17.9% and >= 2 on 7.1% of yes/no
rows; complements 47.0% of yes/no rows, 65.6% of the pairs non-syntactic; twins 22.3%, equiv 6.3%, inv 3.6% of rows;
short card 13.3% of rows; rows per call_id <= 3 (a twin has its own call_id). ch_action gold within 4 pp of uniform over
each card's actions; gold position uniform per option count. Visible-feature cues as in v2.1: P(totals equal | action)
0.32-0.38 for every action; a failing check needs its feature, mitigated by billed-correctly shortfalls, over-billing and
within-bound increases. Wording negation counts (k_all / k_syn): 0 / 0, except yn_not_release 1 / 1 and yn_dneg_release 2 / 2.
'''.split('\n')
out[b0:b1] = bal + ['']

text = '\n'.join(out).rstrip('\n') + '\n'
text += '''
## 7. v2.2 changes (fix iteration 1; the Stage B pilot of `families/T12/pilot/`, verdict `pilot/PILOT_VERDICT.json`)

F1 (premise wordings, R16, R18): `wording_screen.py` removes from the draw every wording whose text ties the price line or
the price check to the policy's decision (drive / shape / decide / settle / determine / point to on ch_price_line; decide /
decision / mean on yn_within_tol and yn_over_tol): 4 + 2 of the 217 pool wordings, chosen by their text only; the kit's
polarity rule P1-P3 (`c2_kit.polarity`, negative predicates `plugin.NEGATIVE_PREDICATES`) removes the one held-out
yn_dneg_release wording with a contracted negative frame (7 of 217 quarantined in all). `authoring.check_wording(..., screen=True)` applies the same
rules to any re-authored wording; the frozen pool stage ran without it, so `pools_v2/` is unchanged and reproducible.
F2 (packs, R20): one pack per card by the global card number. F3 (length, R1, R2, R8, R12-R14, R20, R27): the levers of
R27; semantics, solver A and the error models are unchanged, and so is every label's meaning: only the seeded draws of the labels change (R15, R16, R24). F4 (G6): re-run on the re-piloted rows. G6 on 1,000 rows is noise-limited for choice rows (a random-uniform gold leaves per-(k, action) imbalances of several points that an options-only reader learns; at 5,200 rows every view is within +1.5 pp), so v2.2 balances the golds of ch_action and ch_price_line by stratified seed draws (R15, R16) and draws the twin's new answer uniformly (R24).
Kit `choiceplan` (abstain gold 1 / k): realised directly for the "None of the lines" option of ch_price_line (R16: none is gold 1 / (n + 1), which a one-line row had at 25% instead of 50%); its plan machinery is not used (T12 has no abstain option, R20; gold position and length rank are uniform by G10). Resolved points that change: A13 / H26 moot (no dates).
'''
open('G0_SPEC_v2_2.md', 'w', encoding='utf-8').write(text)
print(len(text.split('\n')), hashlib.sha256(text.encode('utf-8')).hexdigest())
