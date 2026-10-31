"""F13 generator design v1 (c-lanes-v3, gen:F13). Binding inputs: G0_SPEC.md F13.G0.v7 (sha b4bb6319...), BUILDER_BRIEF.

This file is the working plan every F13 module follows. It fixes the concrete fact grammar (one surface per fact kind,
closed cue words from G0 section 11 / 2.5 / 7), the subset of G0 constructions round 1 emits, and the module split.
A construction not listed here is not emitted (G0 allows a subset; every emitted row obeys every G0 rule).

MODULES (gen/)
  f13_base.py     paths, seeded rng, dates (SEM-20), IDs (SEM-31), word lints (2.1 inert, 3.3 names, 7 banned forms),
                  pack adapter (packs-1..4 -> one F13 view), wordings (formats-2 F13 pool), fmt1 styles, tokenizer,
                  served-length measure (decoder_io.user_msg + render_chat, permutation max).
  f13_model.py    document model + SOLVER A (structure side): window/version/life-cycle/decision semantics, Q-P/Q-R/
                  Q-T/AG engines, trace completions (critical points), single-deletion set D + sufficiency, NM activation.
  f13_text.py     renderer: facts -> sentences (grammar below), sections -> fmt1 Doc IR, card IR (SEM lines, defs
                  styles), question / options / edge, attack lines.
  f13_samplers.py S1, S2, S3, S4, S6 (training) and S5 (held out): draw structure + query + near-misses + traces.
  f13_layout.py   length bin draw, decile placement, inert fill (pack-built inert facts), real-token fitting.
  f13_build.py    driver: cards, quotas, rows, twins, verification (A == B on parse, D, NM, lints), emission.
  f13_parse.py    independent parser (text -> sections -> facts); reads the card, the row text and the pack view only.
  f13_solve_b.py  SOLVER B on the parse: sqlite tables + SQL (scope/date/version), brute-force completions (no z3 in
                  the venv; documented deviation: exhaustive critical-point enumeration replaces z3, same domains).
  f13_g4.py       metamorphic relations MR1, MR2, MR5, MR6, MR9, MR10, MR11 (+MR4/MR8 via twins) on >= 1,000 rows/sampler.
qc/f13_gates.py   G2/G3 re-run on outputs, G4 summary, G15 (check_rows, loader_check random perm, units, tokens),
                  negcount quotas, length, sealed_check (program only), MANIFEST.json + QC_REPORT.json.

OUTPUTS (out/)
  candidates_r1.jsonl (+ relations_candidates_r1.jsonl, side/candidates_r1.f13_meta.jsonl): training samplers S1-S4,S6,
    1.5 x r1 = 3,075 rows (S1 675, S2 600, S3 600, S4 750, S6 450).
  qc_sample.jsonl (+ relations, side): >= 5,000 rows, same generators, other seeds (G6 sample; never trained).
  mixdev_S5.jsonl (+ side): 400 S5 items, held-out packs (>= 10) and held-out fmt1 styles only.
  MANIFEST.json (counts, sha256, relation counts/sha, parents), qc/QC_REPORT.json (pool sha256s, gate results).

ROW FORMAT: spec 2.4 + G0 12. id "f13-{split}-{card}-u{n:05d}-{a|b}"; group_id "f13_g_{split}-{card}-u{n:05d}";
  call_id "f13_c_{id}" (relation partner takes its base's call_id); source "c_f13"; role "own"; qtype "choice" | "noul";
  gold = option text (choice) | 1 / 0 (noul). meta: every 2.4 key; spec_id "F13.G0.v7"; licence "CC0 1.0
  (program-generated)"; text_source null; deep false; difficulty_bin / crowd_pg null (G9 fills); subtype "aggregate"
  only on AG rows; persona_seed when the pack has one; edge aligned to options (yes/no: [null, null]).
  structure_hash: X4 is not settled by the orchestrator; like every built family (F9 f9ast.structure_hash) F13 writes
  its own canonical 7.2 #6 form (rule graph + facts + query, names abstracted: IDs, scope units, people, outcomes and
  pack words replaced by role tokens; dates as offsets from the row date). g12_hash (sidecar) = decisive + near-miss
  facts + query + world + card line set, names abstracted.

CARDS: one pack per card (XF09). r1 45 training cards (S1 10, S2 9, S3 9, S4 10, S6 7) + >= 10 held-out S5 cards.
  Card fields: world open|closed (50/50 over cards), scope kind + >= 3 units (pack scope_dimension; S6: committees),
  precedence (S1/S2/S6 Q-P: "specific" | "later"), default outcome, outcome set (>= 3 names), tie rule (S3/S4:
  earlier date | lower record number), vote k (S6), value marker (one of 3 TR markers), governing-date name,
  defs style (one_line 35% | one_line_examples 50% | decision_list 15%), few_shot overlay (5-10% of cards),
  inverted (10-15% of cards; S1/S2/S6 only: every Q-P choice row is inverted), >= 5 wordings (F13 pool, 36).
  Every pair of cards differs in pack AND (sampler | world | scope kind | precedence | default | tie | k | outcome set).

GRAMMAR (one surface per fact kind; <D> in the card's SEM-20 date format; marks are item-level lines unless noted)
  rule version      "Rule <R>, version <R>.<n>: if <cond>, the <item> is <outcome>."
  amendment entry   "Amendment to rule <R>: version <R>.<n> amends version <R>.<n-1>; under version <R>.<n>, if <cond>,
                     the <item> is <outcome>."      (register / bulletin; sole statement of that version)
  version marks     "Version <R>.<n> is marked for <unit>."   "Version <R>.<n> status: <in force|draft|proposed|void>."
                    "Version <R>.<n>: effective <D>; <no end date | valid through <D> | repealed with effect from <D>>."
  exception         "Exception <E> to rule <R> covers every <item> whose <cond>."  + "Exception <E> is marked for <unit>."
                    + "Exception <E> status: <...>." + "Exception <E>: effective <D>; <end form>."
  cond atoms        num: "<attr> is at least|at most|more than|less than <T><unit>"; cat: "<attr> is <value>";
                    joined by " and " (all) or " or " (any); at most 3 atoms; one trace per predicate.
  case record       fields block "<Item> record <CID>": one pair per attribute + scope kind + governing-date name.
  case in question  "a <item> with <attr> <v>, ..., <scope kind> <unit> and <gdate name> <D>"
  life-cycle item   "Hold <H> on <noun> <ID>: placed on <D>[; released on <D>]."  (one statement per item, A58)
                    "Condition <C> on <noun> <ID>: imposed on <D>[; met on <D> | ; waived on <D>]."
                    "Action item <A>: assigned to <person> on <D>[; transferred to <person> on <D>][; closed on <D>
                     [; reopened on <D>]]."   + "<Item ID> is marked for <unit>." when scoped (S6: section mark)
  record status     "<Noun> <ID> status set to <status> on <D>."   holder: "<Noun> <ID> transferred to <person> on <D>."
                    register line "<Noun> <ID>: holder <person>; status <status>; registered on <D>."
  rename            "<Noun> <old> is renamed <new> on <D>."
  S2 decisions      "Decision notice on <matter>, dated <D>: the outcome is <outcome>."
                    "Revision notice on <matter>, dated <D>: the decision is revised; the outcome is <outcome>."
                    "Reversal notice on <matter>, dated <D>: the decision is reversed; the outcome is <outcome>."
                    "Correction to the <decision|revision|reversal> notice on <matter> dated <D>: the notice is void."
                    "Correction to the <decision|revision> notice on <matter> dated <D>: the outcome is <X>, not <Y>."
                    proposal: a revision notice + "Status: proposed." mark line.
  S6 motions        section mark "Committee: <X>." ; "Motion to <make|revise|reverse> the decision on <matter> so that
                    <matter> is <outcome>: in favour <a>, against <b>, abstain <c>." ; void / outcome correction forms of
                    G0 3.2 ("Correction to the minutes of <D>: ..."); proposal "Proposal to revise the decision on
                    <matter> so that <matter> is <outcome>." + "Status: proposed."
  S3 log entry      "<ts> | <entry no> | <actor> | <text>" (items); texts: "<cfg> version <V> recorded; status <in force|
                    proposed|draft>; value <val>", "<V> applied", "<cfg> rolled back to <V>", "VOID entry <no>",
                    "CORRECTION entry <no>: ...", "<Noun> <ID> status set to <status>", no-op "<Noun> <ID> viewed by <user>".
                    Segment mark line "Site: <unit>." on site cards.
  S4 tables         fmt1 table blocks; periodic table body line "Period: <D1> through <D2>."; split parts "Part <k> of
                    table <T>" + "Part total: <amount>"; criteria "Criterion <R>: an <entity> is <outcome> if <cond>."
                    (one version, effective before the earliest period, no end date); exclusions "Exclusion <X> for
                    <entity ID> is marked for <unit>; effective <D>; <end form>."
  traces            value: the card's marker in place of a value; part: "<label> (<scope label>): not included in this copy."
                    T-I labels only "Contact list" | "Staff directory" | "Telephone and e-mail list".
  inert facts       contacts ("Contact for <unit>: <person>, <role>, telephone <nnn nnnn>"), schedule, glossary (pack
                    jargon unused by rules), procedure steps, resource lists, purpose; pass the SEM-62 word lint.
  attack line       G13-checked templates: imperative, no domain fact, may name one option by text.

QUESTION FORMS (closed lexicon; "as of <D>" only as the question date; "for <unit>" on non-case questions)
  Q-P choice  "What is the outcome for <case>?"  options = outcome names + '<None option>' (closed) / '<NEI option>' (open)
  Q-P yes/no  closed: "Is <case> <outcome>?" / "Is it true that <case> is not <outcome>?"
              open: "Does the document establish that <case> is <outcome>?" / "... settle whether <case> is <outcome>?"
  inverted    "Which of these cases meets rule <R>?" options = complete case descriptions + abstain.
  Q-R         "Which version of rule <R> is in force for <unit> as of <D>?" (choice of version IDs);
              status "Is <noun> <ID> <status> as of <D>?" / choice "What is the status of <noun> <ID> as of <D>?";
              holder "Does <noun> <ID> belong to <person> as of <D>?"; "Who is the holder of action item <A> as of <D>?";
              decision "What is the decision on <matter> as of <D>?" / "Is the decision on <matter> <outcome> as of <D>?"
  AG-1        "How many exceptions for <unit> are active as of <D>?"; holds/conditions "How many holds on <noun> <ID>
              for <unit> are active as of <D>?"; "How many open action items for <committee> have <person> as their
              holder as of <D>?"; S4 "How many exclusions for <unit> are active as of <D>?"
  AG-2        version / configuration / decision in force (as Q-R, choice only, 2-3 decisive sections: K1/K2/K3)
  AG-3        "What is the total <measure> in table <T> for <D1> through <D2>?" (sum of part totals) / cross-part count
  Q-T         filter / count / compare / argmax (tie rule) / join / record-set (S3, S4, small tables in S2, S6)
  Q-D         settle-whether rows (open cards) + delete_nei twins.

TWINS: move (equiv, <= 5% rows), delete_nei (open, Q-D, own call_id), nm_activate / date_shift / boundary_flip (own
  call_id; label flips), attack (inv, ~5%), neg (complement), dneg (equiv), inner_neg (establish, own call_id).
  Units are 2 rows max (all F13 rows >= 2,000 tokens). Contrast sets 20-25% of rows after selection.

VERIFICATION per row (build time, 100%): solver A on the model == gold; render; parse; solver B on parse == gold;
  B's single-deletion set == A's == planned decisive set; sufficiency; every near-miss functional under its activation
  operator (B); trace checks (benign / NEI witness pair / >= 2 consistent values); loader_check (fmt1) + check_rows;
  state tokens in bin and >= 2,000; served max over measured orders <= 7,850; G3 lints. A failing row is redrawn.
"""
