"""build_fix2.py: the training file of the 4B top-up q35_4b_main500k_fix2 (candidate C4; draft amendment A8-prime,
prereg_drafts/A8prime.md section C). CPU only: no network, no model, no OHS-3 file.

The mix (whole units only, so every relation keeps both ends; every row is a byte copy of its source line):
  F    F7 "nested negation" train ladders (data/v14_parts/f7_train.jsonl = F7 v2 r6, program labels, gold only, no
       meta.teacher), minus the pairs listed in yn2b/f7_fix2_drops.json and minus every ladder derived from a listed
       source row (blind read 2 and the source-label audit after blind read 3 flagged them). Since r5
       (golden_src/gen3/f7_repair_r5.py, r6) F7 itself never selects such a pair, so these drops must come out empty;
       a non-empty drop stops the build (ALLOW_F7_DROPS): F7 is then repaired, not cut. F7's relations are copied as
       built: in a ladder with an R0, same-answer links are 'inv' with a = the R0; in a ladder without R0 they are
       'equiv' (r6); opposite answers 'complement' (at most one per row).
  G_t  (optional, --part2 gt; NOT used: the default is --part2 none) golden_train units that hold a 'dneg' row.
  F4   (optional, --part2 gt+f4; NOT used) the yn2b F4 polarity-ladder units (gd_gen3_polarity_ladder).
       Part (ii) rests on real-text labels never audited to F7's bar (A8-prime O1), so the built file has none.
  G_r  stratified golden_train replay: the eligible golden units, drawn per stratum (source x unit qtype: noul /
       choice / mixed) with one seeded shuffle per stratum ('fix2-replay:<source>|<kind>') in proportion to the
       stratum's rows, until G_r ALONE is >= 70% of all rows (--replay-share). G_r never counts G_t or F4 rows.
       G_r rows are C1's own training rows, byte for byte, with golden_relations' own types (never retyped).
Relations: only part (ii) units (G_t, F4) would be retyped ('equiv' inside a dneg unit -> 'inv' with a = the
affirmative row); a golden dneg unit the replay draws keeps C1's 'equiv' (A8-prime C.4). Probe / devx relations are not
touched (measurement only).

Exclusions (any hit drops the WHOLE unit; F7 hits drop the whole a/b pair; the written file is re-read from disk and
re-checked, and every check must give 0):
  (a) dev / eval / held-out sources and wording. Reference sources: every source of the dev splits, the eval sets,
      OHS-1/2 (read from those files) and the 14 OHS-3 source names (read from the TEXT of build_ohs3.py, never from
      OHS-3 data), matched with gate_dev.source_seen in both directions plus name containment (f7_precheck.source_clash)
      on the row source and meta.derived_source.
      - F7 and part (ii): every reference source is excluded, and build_fix1.row_check applies in full (strict 12-grams
        vs every dev / eval split, OHS-1/2 and JevBench public text; 6-word template runs vs the 9 gate splits'
        instructions, dialogue_rebuttal, OHS-1/2 and the eval injected spans; the DEV_* / EVAL_* frames, devp's
        wordings and container, NONE_EVAL; dev ids and (state, instruction) pairs).
      - The replay G_r (gr_check): the held-out exclusions only: OHS-1/2 / OHS-3 sources, OHS-1/2 and JevBench
        12-grams, OHS-1/2 instruction / card 6-word runs, the yn2b dev 12-grams, and never a dev / eval / OHS row (ids,
        (state, instruction) pairs). G_r MAY hold units of the dev / eval ("seen") sources and units sharing dev / eval
        wording: they are C1's own training rows, so they add no dev exposure, and they rehearse the sources the gate's
        seen-source part measures; their dev 12-gram / template / frame overlaps are counted, report only.
  (b) the hate / toxicity / offensive-language family (F7 and the replay): golden_train's own dataset tag
      meta.family == 'safety_policy_moderation'; a source name (or meta.derived_source) matching FAM_SRC; or a FAM_WORD
      whole word ((non-)hate, hateful, hatred, toxic, offensive, abusive, abuse(s/d), insult(s/ing/ed), slur(s),
      harass*, prejudic*, misogyn*, sexism/sexist, racism/racist, hostil*, bigot*) in the instruction, an option, a card
      label key or ANY card definition line, after the benign masks (chemical 'toxic', a battle's 'Offensive', drug /
      substance abuse, a drug label's 'abuse' section, armed 'hostilities'). A source with >= 15% family rows is
      excluded whole; otherwise only the units of its family rows drop.
  (c) the F7 probe and devx: the probe's held-out sources and devx's sources, any row whose state equals a probe / devx
      state, any row with more than 20% of its state 12-grams in a probe / devx state, and (after the draw) every
      probe / devx state must share at most 20% of its 12-grams with the whole file (SPEC 7.6).
  (d) the measured-failure frame (F7 and the replay): 6-word runs of the failing devp_card/hate questions; 'be
      rejected'; 'the statement that'; the words hate / hateful / non-hateful in any instruction, option or card line.
  (e) OHS-3 (PREREG_OHS3 rule 1), from the TEXT of build_ohs3.py only: no 5-word run of the fixed text of frames T1-T5,
      no frame regex match, no T6 form ('answer no if ..., (and) yes otherwise'), no 5-word run of the PROPS
      propositions / clause-negated questions and no match of their question regexes.
  (f) public negation benchmarks: no 6-word run shared with the decontam-only manifest's texts.
      SPEC 4.7 banned judge words: 0 in F7 / F4 instructions, options and yes/no lines (program-authored text); in the
      replay they are counted and reported only (golden_train's own human-task wording and C1's own objective).
  (g) label noise: units holding a yn2b/label_audit_known_bad_ids.json id, a yn2b/f7_fix2_drops.json source row or a
      flagged probe source row (probe_source_row_ids).
  Part (ii) and F4 rows only: no held-out probe lexeme (f7_holdout_spec.json, word lexemes with inflections) and no
  6-word run of a held-out probe or devx instruction / option / yes-no line in their instructions, options or cards.
Mix-level shortcut check (F7_COVERAGE_CHECKLIST.md section 4.6, composition probes C1 and C2, computed on the yes/no
rows of F7 plus part (ii)): C1 (gold = truth(P)) within 45-55%, C2 (truth(P) XOR parity of all cues) <= 70% overall and
<= 75% at every depth. A part (ii) choice that breaks a bar is refused.

Also writes byte copies of the F7 probe and devx (+ relations and sidecars) at data/f7_probe*.jsonl and
data/f7_devx*.jsonl, the split names od_gcp predict and gate/fix2_conditions.py read (data/<split>.jsonl).

Writes NEW files only (refuses to overwrite without --overwrite):
  data/v14_parts/fix2_train.jsonl, fix2_relations.jsonl, fix2_counts.json,
  data/v14_parts/f7fix2_train.jsonl, f7fix2_relations.jsonl, f7fix2_meta.jsonl (the F7 part exactly as used, for
  yn2b/f7_precheck.py --train ...), data/f7_probe{,_relations,_meta}.jsonl, data/f7_devx{,_relations,_meta}.jsonl

  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python extra/build_fix2.py [--dry] [--overwrite]   # from lean/; ~10 min
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import random
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

LEAN = Path(__file__).resolve().parents[1]
for _p in (str(LEAN), str(LEAN / "yn2b"), str(LEAN / "extra")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True
import build_fix1 as bf  # noqa: E402  (load_refs, row_check, frame_regexes, norm_pair: fix1's decontamination)
import check_yn2b as cy  # noqa: E402
import f7_precheck as pc  # noqa: E402  (source_clash, ohs3_frames, failure_frame_runs, load_neg_bench, text helpers)
import train_decoder as td  # noqa: E402  (READ-ONLY: make_units, check_rows)
import yn2b_common as yc  # noqa: E402

DATA = LEAN / "data"
V = "v14_parts/"
GOLD_TRAIN, GOLD_REL = V + "golden_train.jsonl", V + "golden_relations.jsonl"
YN2B_TRAIN, YN2B_REL = V + "yn2b_ab/yn2b_train.jsonl", V + "yn2b_ab/yn2b_relations.jsonl"
F7 = {k: V + f"f7_{k}.jsonl" for k in ("train", "relations", "meta", "probe", "probe_relations", "probe_meta",
                                         "devx", "devx_relations", "devx_meta")}
F7_SPEC, F7_LEX = V + "f7_holdout_spec.json", V + "f7_lexicon.json"
INPUT_SHA = {  # every input, pinned (golden = the main run's train_meta "data"; F7 = F7 v2 r6's f7_counts.json)
    GOLD_TRAIN: "ff7a395bc9b501ac27949ed7265b771e720406fa96f0e296700c2c101f62a2a9",
    GOLD_REL: "072ee6c45f3f246cca7cc7b465387c83412c406e552e2b161c05d291afb9b214",
    YN2B_TRAIN: "48a2bf0ffec2792a7c13bcc6c0278c5ec3b0ff77eee3794b662a78dd1741d259",
    YN2B_REL: "39a56113a4d55605fa8edf4d780c93b5bdc53f454cadc5c484e540346c7a40ae",
    F7["train"]: "ffa5cecacde7ed65f0b8a105784eae3fae62007650eefd7aff7d8df5197b601c",
    F7["relations"]: "895fab57e5db294ea89d638f37555f9438d2cb1685b6b6418a5f3dd37397a1a3",
    F7["meta"]: "b632cc2d702792cd94e6a24eb06eeeb32f589413eb9cc09935a04972ee34e598",
    F7["probe"]: "e715fbd054bf2846410ce9034fe8c9f1b4f384efa853f9e2dd5a3d5d0d7d0710",
    F7["probe_relations"]: "eda2e82450c9b6dcd14eb141887160249f21eb9c83b1524873d17de626684d04",
    F7["probe_meta"]: "f4c8c3357730b34616e735e093d4d59ee11628ce1f6baaf65abc0634a57330d4",
    F7["devx"]: "b5579786954652c201d9871a2d4e8a16c23340d4cad0254c1e5e84f8a4d34168",
    F7["devx_relations"]: "74cb00c9918959480caed38a1eb409974e7284578bde125f484994dc4c7da9d2",
    F7["devx_meta"]: "bc22f752d2e917f333401bfad926dfddfcf41a9d48ace2de156f6b10a11e5ac2",
    F7_SPEC: "ab2fe8539ba8dd850ba467de45729fe01b7f5de6d07f0c3dc335eb42b8f8fbd8",
    F7_LEX: "bc32ec4c0e4989467cecd136a492ca0495efa175c74bddce5c28a45fdab25675",
}
OTHER_INPUTS = {"yn2b/label_audit_known_bad_ids.json": "d4de5ed1bb9a74054968f652101f044053620afcb1f222b583e4d367c262e5a0",
                "yn2b/decontam_only/negation_benchmarks.json": "0ff200b57b926cb913637a88b0076efb000b4138f99cad063450d5dbe242d4ba"}
DROPS = LEAN / "yn2b/f7_fix2_drops.json"
OUT = {"train": V + "fix2_train.jsonl", "rel": V + "fix2_relations.jsonl", "counts": V + "fix2_counts.json",
       "f7_train": V + "f7fix2_train.jsonl", "f7_rel": V + "f7fix2_relations.jsonl", "f7_meta": V + "f7fix2_meta.jsonl"}
COPIES = {"f7_probe.jsonl": F7["probe"], "f7_probe_relations.jsonl": F7["probe_relations"],
          "f7_probe_meta.jsonl": F7["probe_meta"], "f7_devx.jsonl": F7["devx"],
          "f7_devx_relations.jsonl": F7["devx_relations"], "f7_devx_meta.jsonl": F7["devx_meta"]}

DEV_FILES = ("dev", "dev_nc", "taskbank_dev", "hard_dev", "dev_negwords", "dev_claims", "pg_dev", "devzs", "devp_card",
             "devp", "devzs_card", "devzs2", "devzs2_card", "debate_dev", "hard12_dev", "proc12_dev", "planted12_dev",
             "dev_hc")
EVAL_FILES = ("eval", "eval_card", "eval_hc", "eval_jagged", "eval_long", "eval_multi", "eval_opi", "eval_redef")
HELD_FILES = ("ohs", "ohs2")  # never ohs3: its source NAMES come from build_ohs3.py's text
REPLAY_SHARE = 0.70
SALT = "fix2-replay:"
KD_SKIP_SRC, KD_FULL_SRC = ("blend50",), ("gd_gen2_probability",)  # runs/q35_4b_main.json, unchanged
MAX_UNIT_ROWS, MAX_UNIT_ROWS_LONG, LONG_STATE, MAX_UNIT_CHARS = 5, 3, 6000, 24000  # SPEC 4.2 / 4.9: rows; total state
PROBE_GRAM_MAX = 0.20  # SPEC 7.6 / A8-prime C6 (c)
ALLOW_F7_DROPS = False  # F7 v2 r5 needs none; a drop means F7 must be repaired, not cut (A8-prime C.6 (g))
# The hate / toxicity / offensive-language family (A8-prime C.6 (b)): golden_train's own dataset tag, the source name,
# and the whole words below in the instruction, any option, any card label key AND any card definition line.
FAM_META = {"safety_policy_moderation"}   # golden_train meta.family of the hate / abuse / moderation datasets
FAM_SRC = re.compile(r"hate|toxic|offens|abus|insult|slur|harass|prejudic|misogyn|sexis|racis|bigot", re.I)
FAM_WORD = re.compile(r"(?<![\w])(?:(?:non-?)?hate|hateful|hatred|toxic|offensive|abusive|abuse[sd]?|insult(?:s|ing|ed)?|"
                      r"slurs?|harass\w*|prejudic\w*|misogyn\w*|sexis[mt]\w*|racis[mt]\w*|hostil\w*|bigot\w*)(?![\w])",
                      re.I)
FAM_BENIGN = (re.compile(r"\btoxic(?:ity)?\s+(?:materials?|agents?|vapou?rs?|substances?|chemicals?|fumes?|gas(?:es)?|"
                         r"exposures?|effects?|doses?|metals?|wastes?|compounds?|plants?|algae|spills?|leaks?)\b", re.I),
              re.compile(r"\b[A-Z][\w'-]+(?:\s+[A-Z][\w'-]+)*\s+Offensive\b"),  # chemical 'toxic'; battles ('Tet Offensive')
              # drug and substance abuse (medical, not speech): 'substance-abuse', 'drug abuse', 'abuse and misuse',
              # 'abuse-deterrent', 'potential for abuse'; armed 'hostilities'
              re.compile(r"\b(?:drug|substance|alcohol|opioid|medication|prescription|stimulant|narcotic)[\s-]+abuse\b|"
                         r"\babuse(?:\s+and\s+(?:misuse|dependence)|-deterrent|\s+potential|\s+liability)\b|"
                         r"\b(?:potential|signs?)\s+(?:for|of)\s+abuse\b|\bhostilities\b", re.I))
# a drug label's section names ('abuse', 'dependence', 'controlled substance', 'overdosage'): the bare word 'abuse' in a
# row whose options / card name these sections is a drug-label section, not abusive speech
DRUG_SECTION_CTX = re.compile(r"\b(?:controlled substance|overdosage|dependence)\b", re.I)
FAM_SOURCE_SHARE = 0.15  # a source with >= 15% family rows is a family dataset and is excluded whole
# Owner OHS-3 12-gram check (extra/fix2_ohs3_blind.py, run by the orchestrator under the owner's decision of 2 Oct,
# counts only) found 7 hit units in fix2 build 08743b52...: gd_redocred 6, gd_helpsteer3_pref 1. Both sources are
# left out of the top-up WHOLE (no per-unit ids were taken from the OHS-3 check). Neither is a source of the 9 gate
# splits, so the gate's rehearsal is unchanged.
OHS3_HIT_SOURCES = ("gd_redocred", "gd_helpsteer3_pref")
HATE_WORDS = re.compile(r"(?<![\w])(?:non-?)?hate(?:ful)?(?![\w])", re.I)
FAIL_PHRASES = re.compile(r"\bbe\s+rejected\b|\bthe\s+statement\s+that\b", re.I)
T6_FORM = re.compile(r"\banswer\s+no\s+if\b[^.?!\n]*?,\s*(?:and\s+)?yes\s+otherwise\b", re.I)
OHS3_RUN = 5
COMP_C1 = (0.45, 0.55)      # CL:426
COMP_C2_ALL, COMP_C2_DEPTH = 0.70, 0.75  # CL:427
ROLE_DEPTH = {"aff": 0, "para": 0, "neg": 1, "clause_neg": 1, "dneg": 2}


def sha(p):
    return yc.sha256_file(p)


def jl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def lines_of(path):
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                out.append(line if line.endswith("\n") else line + "\n")
    return out


def tok5(t):
    return re.findall(r"[a-z0-9]+", (t or "").lower())


def runs_n(t, n):
    w = tok5(t)
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


def card_lines(r):
    return [ln for ln in (r.get("card") or "").splitlines() if ln.strip()]


def authored(r):
    """Text the row's builder wrote (not the source document): instruction, options, every card line."""
    return [r.get("instructions") or ""] + [o for o in (r.get("options") or []) if isinstance(o, str)] + card_lines(r)


def label_names(r):
    names = [o for o in (r.get("options") or []) if isinstance(o, str)]
    for ln in card_lines(r):
        m = pc.CARD_KEY_RE.match(ln)
        if m:
            names.append(m.group(1))
    return names


def derived_sources(r):
    m = r.get("meta") or {}
    out = {r.get("source")}
    if m.get("derived_source"):
        out.add(m["derived_source"])
    return {s for s in out if s}


def derived_rows(r):
    d = (r.get("meta") or {}).get("derived_from")
    if not d:
        return set()
    return set(d) if isinstance(d, list) else set(str(d).split("|"))


# ------------------------------------------------------------------------------------------------ reference sets
def ohs3_text_refs():
    """OHS-3 source names, negation frames and consistency wordings, from the TEXT of build_ohs3.py (ast, no data)."""
    tree = ast.parse((LEAN / "build_ohs3.py").read_text())
    got = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id in ("PASSED", "NOT_PASSED", "NEG_FRAMES", "PROPS"):
                    got[t.id] = ast.literal_eval(node.value)
    names = list(got["PASSED"]) + list(got["NOT_PASSED"])
    frames = [f for _, f in got["NEG_FRAMES"]]
    fixed, rxs = set(), []
    for f in frames:
        parts = re.split(r"\{[^{}]*\}", f)
        rxs.append(re.compile(r"\s*(.+?)\s*".join(re.escape(p.strip()) for p in parts), re.I))
        for p in parts:
            fixed |= runs_n(p, OHS3_RUN)
    for q_rx, prop, negq in got["PROPS"]:
        rxs.append(re.compile(q_rx, re.I))
        rxs.append(re.compile(re.escape(negq).replace(re.escape('"{0}"'), '"[^"]+"'), re.I))
        for t in (prop, negq):
            for p in re.split(r"\{[^{}]*\}|\"\{0\}\"", t):
                fixed |= runs_n(p, OHS3_RUN)
    if len(names) != 14 or len(frames) != 6 or len(got["PROPS"]) != 5:
        raise SystemExit(f"build_ohs3.py text changed: {len(names)} names, {len(frames)} frames, {len(got['PROPS'])} PROPS")
    return names, frames, fixed, rxs


def file_sources(f):
    out = Counter()
    with open(DATA / f"{f}.jsonl", encoding="utf-8") as fh:
        for line in fh:
            m = re.search(r'"source":\s*"([^"]+)"', line)
            if m:
                out[m.group(1)] += 1
    return out


def load_all_refs(log):
    t0 = time.time()
    R = bf.load_refs(log)
    R["rx"] = bf.frame_regexes()
    o3_names, o3_frames, o3_fixed, o3_rx = ohs3_text_refs()
    R.update(o3_names=o3_names, o3_fixed=o3_fixed, o3_rx=o3_rx)
    src_files = defaultdict(set)
    for f in DEV_FILES + EVAL_FILES + HELD_FILES:
        for s in file_sources(f):
            src_files[s].add(f)
    for s in o3_names:
        src_files[s].add("ohs3 (name from build_ohs3.py)")
    R["ref_sources"] = sorted(src_files)
    R["ref_source_files"] = {k: sorted(v) for k, v in src_files.items()}
    # the held-out sets only (OHS-1/2 files and the OHS-3 names): the replay G_r keeps these source, 12-gram and
    # template exclusions; the dev / eval ones apply to F7 and part (ii) only (A8-prime C.6 (a))
    R["held_sources"] = sorted(k for k, v in src_files.items() if any(f in HELD_FILES or f.startswith("ohs3") for f in v))
    R["g12_held"] = set().union(*[R["g12"][f] for f in HELD_FILES], *[R["g12"][d] for d in cy.BENCH_DIRS])
    R["t6_held"] = cy.template_refs(LEAN)["ohs12_instructions_cards"]
    ff, n_ff = pc.failure_frame_runs()
    if not ff:
        raise SystemExit("the measured-failure frame runs could not be read from data/devp_card.jsonl")
    R["fail_runs"], R["fail_n"] = ff, n_ff
    nb, nb_info = pc.load_neg_bench("yn2b/decontam_only/negation_benchmarks.json", log)
    if nb is None or nb_info.get("missing"):
        raise SystemExit(f"negation-benchmark manifest incomplete: {nb_info}")
    R["negbench"], R["negbench_info"] = nb, nb_info
    log(f"extra refs: {len(R['ref_sources'])} dev/eval/OHS sources ({len(o3_names)} OHS-3 names), {len(o3_fixed)} OHS-3 "
        f"5-word runs, {len(o3_rx)} OHS-3 regexes, {len(ff)} failure-frame runs ({n_ff} questions), {len(nb):,} "
        f"negation-benchmark runs ({time.time() - t0:.0f} s)")
    return R


def probe_refs(log):
    """Probe + devx: states, state 12-grams, sources, held-out authored 6-word runs, held-out lexeme regexes."""
    spec = json.loads((DATA / F7_SPEC).read_text())
    states, grams, srcs, runs6 = set(), set(), set(), set()
    per_state = []
    for part in ("probe", "devx"):
        rows = jl(DATA / F7[part])
        metas = {m["id"]: m for m in jl(DATA / F7[part + "_meta"])}
        for r in rows:
            m = metas.get(r["id"]) or {}
            st = cy.norm(r.get("state"))
            if st not in states:
                g = cy.ghash(r.get("state") or "")
                per_state.append(g)
                grams |= g
            states.add(st)
            kind = m.get("dev_kind") or (r.get("meta") or {}).get("dev_kind")
            if kind in ("holdout", "devx"):
                for s in derived_sources(r) | {m.get("source")}:
                    if s:
                        srcs |= set(s.split("+")) | {s}
                for t in pc.authored_texts(r):
                    runs6 |= cy.runs(t)
    srcs = {s for s in srcs if s != "gd_gen3_nested_negation" and not s.startswith(("f7_record", "f7x_record"))}
    for s in spec["sources"]:
        srcs |= set(s.split("+")) | {s}
    lex = [(x, pc.lexeme_regex(x)) for x in spec["lexemes"]]
    log(f"probe/devx refs: {len(states)} states, {len(grams):,} state 12-grams, held-out/devx sources {sorted(srcs)}, "
        f"{len(runs6):,} held-out authored 6-word runs, {sum(1 for _, x in lex if x)} word lexemes "
        f"({[x for x, rx in lex if rx is None]} affix lexemes: F7 cue annotations only)")
    return {"states": states, "grams": grams, "per_state": per_state, "sources": srcs, "runs6": runs6,
            "lex": [(x, rx) for x, rx in lex if rx is not None], "spec": spec}


# ------------------------------------------------------------------------------------------------ per-row checks
def fam_word(t, drug_ctx=False):
    for rx in FAM_BENIGN:
        t = rx.sub(" ", t or "")
    if drug_ctx:
        t = re.sub(r"\babuse\b", " ", t, flags=re.I)
    return FAM_WORD.search(t)


def family_hits(r):
    """Every reason this row is in the hate / toxicity / offensive-language family (A8-prime C.6 (b)): golden_train's
    own dataset tag meta.family 'safety_policy_moderation', the source name (row source or meta.derived_source), or a
    family word in an option or card label key, the instruction, or any card definition line."""
    out = []
    if (r.get("meta") or {}).get("family") in FAM_META:
        out.append("family_meta")
    if any(FAM_SRC.search(s) for s in derived_sources(r)):
        out.append("family_source")
    drug = bool(DRUG_SECTION_CTX.search(" ".join([o for o in (r.get("options") or []) if isinstance(o, str)]
                                                  + [r.get("card") or ""])))
    if any(fam_word(t, drug) for t in label_names(r)):
        out.append("family_label")
    if fam_word(r.get("instructions") or "", drug):
        out.append("family_instruction")
    if any(fam_word(ln, drug) for ln in card_lines(r)):
        out.append("family_card")
    return out


def gr_check(r, R, grams=None):
    """The decontamination rule of the replay G_r (A8-prime C.6 (a), (d)): G_r rows are byte copies of C1's own
    golden_train rows, so the dev / eval 12-gram, 6-word template and frame filters (which keep NEW text away from the
    gate) do not apply; every held-out filter does (OHS-1/2 and JevBench public 12-grams, OHS-1/2 instruction / card
    6-word runs, the yn2b dev 12-grams), and so do the never-a-dev-row checks (dev / eval / OHS ids, (state,
    instruction) pairs, split). Returns (hard reasons, report-only reasons)."""
    grams = bf.row_grams(r) if grams is None else grams
    why, rep = [], []
    if grams & R["g12_held"]:
        why.append("12gram_heldout")
    if grams & R["infam_y"]:
        why.append("12gram_yn2b_dev")
    runs = cy.runs(r.get("instructions") or "")
    if runs & R["t6_held"]:
        why.append("tmpl6_heldout")
    if r["id"] in R["ids"]:
        why.append("id")
    if bf.norm_pair(r) in R["pairs"]:
        why.append("text")
    if r.get("split") != "train":
        why.append("split")
    if grams & R["strict"] and not grams & R["g12_held"]:
        rep.append("dev12gram_report_only")
    if runs & R["t6_dev"] and not runs & R["t6_held"]:
        rep.append("devtmpl6_report_only")
    if bf.frame_hits(r, R["rx"]):
        rep.append("devframe_report_only")
    return why, rep


def row_reasons(r, R, P, part, grams=None, src_bad=None):
    """Every reason this row must not be in the top-up (empty = clean). part: f7 | gt | f4 | gr (the replay: the
    lenient dev rule of gr_check) | gr_strict (a golden row judged for part (ii): the strict rule)."""
    if part == "gr":
        why, rep = gr_check(r, R, grams)
        why = why + rep
    else:
        why = list(bf.row_check(r, R, R["rx"], yn2b=(part == "f4"), grams=grams))
    srcs = derived_sources(r)
    if src_bad is not None and srcs & src_bad:
        why.append("excluded_source")
    why += family_hits(r)
    if srcs & P["sources"]:
        why.append("probe_source")
    st = r.get("state") or ""
    if cy.norm(st) in P["states"]:
        why.append("probe_state")
    g = cy.ghash(st)
    if g and len(g & P["grams"]) / len(g) > PROBE_GRAM_MAX:
        why.append("probe_12gram")
    texts = authored(r)
    if any(HATE_WORDS.search(t) for t in texts):
        why.append("hate_word")
    if any(FAIL_PHRASES.search(t) for t in texts):
        why.append("failure_phrase")
    r6 = set().union(*[cy.runs(t) for t in texts]) if texts else set()
    if r6 & R["fail_runs"]:
        why.append("failure_frame_run")
    if {hash(x) for x in r6} & R["negbench"]:
        why.append("negbench_run")
    r5 = set().union(*[runs_n(t, OHS3_RUN) for t in texts]) if texts else set()
    if r5 & R["o3_fixed"] or any(x.search(t) for x in R["o3_rx"] for t in texts) or any(T6_FORM.search(t) for t in texts):
        why.append("ohs3_frame")
    banned = any(cy.BANNED_RE.search(t) for t in pc.authored_texts(r))
    if banned:
        why.append("banned_word" if part in ("f7", "f4", "gt") else "banned_word_report_only")
    if part in ("gt", "f4"):
        why += heldout_hits(r, P, r6)
    return why


def heldout_hits(r, P, r6=None):
    """Part (ii) / F4 only: a 6-word run of a held-out probe or devx authored text, or a held-out probe lexeme."""
    texts = authored(r)
    if r6 is None:
        r6 = set().union(*[cy.runs(t) for t in texts]) if texts else set()
    out = []
    if r6 & P["runs6"]:
        out.append("probe_heldout_run")
    if any(rx.search(t) for _, rx in P["lex"] for t in texts):
        out.append("probe_heldout_lexeme")
    return out


HARD_SKIP = {"banned_word_report_only", "dev12gram_report_only", "devtmpl6_report_only", "devframe_report_only"}


def hard(why):
    return [w for w in why if w not in HARD_SKIP]


# ------------------------------------------------------------------------------------------------ helpers
def unit_kind(u):
    q = {r["qtype"] for r in u}
    return "noul" if q == {"noul"} else ("choice" if q == {"choice"} else "mixed")


def retype(rels, rows_by_id, unit_ids_with_dneg, anchor_of):
    """'equiv' links inside a dneg unit -> 'inv' with a = the affirmative row. Returns (new relation dicts, counts)."""
    out, n = [], Counter()
    for x in rels:
        a, b = rows_by_id.get(x["a"]), rows_by_id.get(x["b"])
        if x["type"] == "equiv" and a is not None and b is not None and a["call_id"] in unit_ids_with_dneg:
            aa, bb = anchor_of(a, b)
            if aa is None:
                raise SystemExit(f"equiv link in a dneg unit with no affirmative end: {x}")
            y = {k: v for k, v in x.items() if k not in ("a", "b", "type")}
            out.append({"type": "inv", "a": aa["id"], "b": bb["id"], **y, "retyped_from": "equiv"})
            n[f"equiv->inv {aa.get('role')}->{bb.get('role')}"] += 1
        else:
            out.append(x)
    return out, n


def is_affirmative(r):
    m = r.get("meta") or {}
    if r.get("role") == "aff":
        return True
    return r.get("role") == "para" and m.get("polarity") in (0, None) and r.get("source") == "gd_gen3_polarity_ladder"


def anchor_pair(a, b):
    if is_affirmative(a) and not is_affirmative(b):
        return a, b
    if is_affirmative(b) and not is_affirmative(a):
        return b, a
    if a.get("role") == "aff" and b.get("role") == "para":  # golden aff -> para (both affirmative): a = aff
        return a, b
    if b.get("role") == "aff" and a.get("role") == "para":
        return b, a
    return None, None


def comp_probe_parts(f7_meta_rows, part2_rows):
    """Composition probes C1 / C2 (f7_precheck.comp_preds) on the yes/no rows of F7 + part (ii). Part (ii) rows have no
    distractor: depth = cue count by role, truth(P) = gold XOR parity(depth)."""
    c1, c2, n = 0, 0, 0
    by_d = defaultdict(lambda: [0, 0])
    for m in f7_meta_rows:
        if m["qtype"] != "noul":
            continue
        tp = 1 if m["truth_P"] else 0
        g = int(m["gold"])
        n += 1
        c1 += g == tp
        ok2 = g == (tp ^ (len(m["cues"]) % 2))
        c2 += ok2
        by_d[m["depth"]][0] += ok2
        by_d[m["depth"]][1] += 1
    for r in part2_rows:
        if r["qtype"] != "noul" or r.get("role") not in ROLE_DEPTH:
            continue
        d = ROLE_DEPTH[r["role"]]
        g = int(round(float(r["gold"])))
        tp = g ^ (d % 2)
        n += 1
        c1 += g == tp
        c2 += 1
        by_d[d][0] += 1
        by_d[d][1] += 1
    res = {"rows": n, "C1": round(c1 / n, 4), "C2": round(c2 / n, 4),
           "C2_by_depth": {str(d): round(v[0] / v[1], 4) for d, v in sorted(by_d.items())}}
    res["pass"] = bool(COMP_C1[0] <= res["C1"] <= COMP_C1[1] and res["C2"] <= COMP_C2_ALL
                       and all(v <= COMP_C2_DEPTH for v in res["C2_by_depth"].values()))
    return res


# ------------------------------------------------------------------------------------------------ main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--replay-share", type=float, default=REPLAY_SHARE)
    ap.add_argument("--part2", choices=("none", "gt", "gt+f4"), default="none",
                    help="part (ii): none (A8-prime C.2: F7 alone; the default), gt or gt+f4 (their real-text labels "
                         "are not audited to F7's bar, so neither is used)")
    ap.add_argument("--dry", action="store_true", help="compute and print everything, write nothing")
    a = ap.parse_args(argv)
    t_start = time.time()
    log = lambda s: print(f"[{time.time() - t_start:6.0f}s] {s}", flush=True)  # noqa: E731
    outs = {}
    if not a.dry:
        for k, p in OUT.items():
            outs[k] = yc.guard_out(DATA / p, inputs=[DATA / q for q in INPUT_SHA], overwrite=a.overwrite)
        for k in COPIES:
            outs["copy:" + k] = yc.guard_out(DATA / k, inputs=[DATA / q for q in INPUT_SHA], overwrite=a.overwrite)
    for p, want in {**INPUT_SHA, **{q: w for q, w in OTHER_INPUTS.items()}}.items():
        path = (DATA / p) if p in INPUT_SHA else (LEAN / p)
        got = sha(path)
        if got != want:
            raise SystemExit(f"input {p} sha256 {got[:12]}... is not the pinned {want[:12]}...")
    log("inputs verified (sha256 of golden, yn2b, F7 train / probe / devx and their relations and sidecars)")
    drops = json.loads(DROPS.read_text())
    drop_pairs, drop_src = set(drops["f7_pairs"]), set(drops["source_row_ids"])
    bad_ids = set(json.loads((LEAN / "yn2b/label_audit_known_bad_ids.json").read_text())["all_ids"]) | drop_src | set(drops.get("probe_source_row_ids") or {})
    R = load_all_refs(log)
    P = probe_refs(log)

    # ------------------------------------------------------------ F7
    f7_lines = lines_of(DATA / F7["train"])
    f7_rows = [json.loads(l) for l in f7_lines]
    f7_meta = {m["id"]: m for m in jl(DATA / F7["meta"])}
    f7_rels = jl(DATA / F7["relations"])
    if {r["id"] for r in f7_rows} != set(f7_meta):
        raise SystemExit("F7 sidecar ids differ from the train rows")
    pair_of = lambda r: r["meta"]["latent_id"][:-1]  # noqa: E731  f7v2-tr-02499a -> f7v2-tr-02499
    f7_why = defaultdict(list)
    for r in f7_rows:
        if pair_of(r) in drop_pairs:
            f7_why[pair_of(r)].append((r["id"], "drop_list_pair"))
        if derived_rows(r) & bad_ids:
            f7_why[pair_of(r)].append((r["id"], "derived_from_bad_source_row"))
        why = hard(row_reasons(r, R, P, "f7"))
        if why:
            f7_why[pair_of(r)].append((r["id"], why))
    f7_drop_pairs = set(f7_why)
    keep_f7 = [i for i, r in enumerate(f7_rows) if pair_of(r) not in f7_drop_pairs]
    F = [f7_rows[i] for i in keep_f7]
    f_ids = {r["id"] for r in F}
    allowed = {"drop_list_pair", "derived_from_bad_source_row", "probe_12gram", "probe_state"}
    unexpected = {k: v for k, v in f7_why.items()
                  if any(w not in allowed for _, ws in v for w in ([ws] if isinstance(ws, str) else ws))}
    f7_drop_reason = {k: sorted({w for _, ws in v for w in ([ws] if isinstance(ws, str) else ws)})
                      for k, v in f7_why.items()}
    log(f"F7: {len(f7_rows)} rows, {len({r['meta']['latent_id'] for r in f7_rows})} ladders; dropped pairs "
        f"{f7_drop_reason} ({len(f7_rows) - len(F)} rows); unexpected hits {dict(list(unexpected.items())[:4])}")
    if unexpected:
        raise SystemExit(f"F7 rows fail an exclusion beyond the drop list: {dict(list(unexpected.items())[:6])}")
    if f7_why and not ALLOW_F7_DROPS:
        # F7 v2 r5 (golden_src/gen3/f7_repair_r5.py) never selects a pair these rules drop; a drop here would cut F7
        # below its checklist floors and balance bars without the precheck of the fix2 part noticing it first
        raise SystemExit(f"F7 needs {len(f7_why)} pair drops: repair F7 (golden_src/gen3/f7_repair_r5.py) instead of "
                         f"cutting it here ({dict(list(f7_drop_reason.items())[:6])})")
    if any(yc.kd_target(r) is not None or "teacher" in (r.get("meta") or {}) for r in F):
        raise SystemExit("an F7 row carries meta.teacher (gold only)")
    # ladder shape (SPEC 4.2 / 4.9; A8-prime C.4)
    lad = defaultdict(list)
    for r in F:
        lad[r["call_id"]].append(r)
    shape_bad = [k for k, u in lad.items()
                 if len(u) > MAX_UNIT_ROWS or (max(len(x.get("state") or "") for x in u) > LONG_STATE
                                               and len(u) > MAX_UNIT_ROWS_LONG)
                 or len({x.get("state") for x in u}) != 1]
    unit_chars = {k: sum(len(x.get("state") or "") for x in u) for k, u in lad.items()}  # SPEC 4.9: total state
    shape_bad += [k for k, c in unit_chars.items() if c > MAX_UNIT_CHARS]
    if shape_bad:
        raise SystemExit(f"F7 ladders break the unit shape rule: {shape_bad[:5]}")
    F_rel = [x for x in f7_rels if x["a"] in f_ids and x["b"] in f_ids]
    if any((x["a"] in f_ids) != (x["b"] in f_ids) for x in f7_rels):
        raise SystemExit("a dropped F7 pair left a relation half in the file")
    f7_rel_lines = [l for l in lines_of(DATA / F7["relations"]) if json.loads(l)["a"] in f_ids]
    ncomp = Counter()
    for x in F_rel:
        if x["type"] == "complement":
            ncomp[x["a"]] += 1
            ncomp[x["b"]] += 1
    if any(v > 1 for v in ncomp.values()):
        raise SystemExit("an F7 row has more than one complement relation")
    f7_meta_kept = [f7_meta[r["id"]] for r in F]
    log(f"F7 kept: {len(F)} rows, {len(lad)} ladders, {len(F_rel)} relations {dict(Counter(x['type'] for x in F_rel))}")

    # ------------------------------------------------------------ golden: one pass
    # two rules per row: the replay rule (G_r: held-out filters only, gr_check) and the strict rule of part (ii) (G_t:
    # the replay rule plus every dev / eval filter of build_fix1.row_check)
    light, g_why, g_strict, g_report, g_extra = [], {}, {}, Counter(), {}
    src_rows, src_family, src_rowfam = Counter(), Counter(), Counter()
    ref_src, held_src = R["ref_sources"], R["held_sources"]
    clash_cache = {}

    def clash(s):
        if s not in clash_cache:
            clash_cache[s] = pc.source_clash(s, ref_src)
        return clash_cache[s]

    held_set = set(held_src)

    def clash_held(s):
        return [c for c in clash(s) if c in held_set]

    with open(DATA / GOLD_TRAIN, encoding="utf-8") as f:
        for n, line in enumerate(f):
            r = json.loads(line)
            m = r.get("meta") or {}
            light.append({"id": r["id"], "call_id": r["call_id"], "source": r["source"], "role": r.get("role"),
                          "qtype": r["qtype"], "gold": r.get("gold"), "dsrc": m.get("derived_source"),
                          "teach": isinstance(m.get("teacher"), dict), "tsrc": m.get("teacher_src")})
            src_rows[r["source"]] += 1
            grams = bf.row_grams(r)
            why = row_reasons(r, R, P, "gr", grams=grams)
            strict = [w for w in bf.row_check(r, R, R["rx"], yn2b=False, grams=grams) if w not in why]
            if strict:
                g_strict[r["id"]] = strict
            ex = heldout_hits(r, P) + (["banned_word"] if "banned_word_report_only" in why else [])
            if ex:
                g_extra[r["id"]] = ex
                for w in ex:
                    g_report["report_" + w] += 1
            fam = [w for w in why if w.startswith("family")]
            if fam:
                src_rowfam[r["source"]] += 1
            for w in why:
                g_report[w] += 1
            for w in strict:
                g_report["part2_only_" + w] += 1
            h = hard(why)
            if h:
                g_why[r["id"]] = h
            if n % 100000 == 0:
                log(f"golden pass: {n:,} rows ({len(g_why):,} with a hit so far)")
    log(f"golden pass done: {len(light):,} rows; reasons {g_report.most_common()}")
    # source-level exclusions. Replay (G_r): the held-out sources (OHS-1/2 files, OHS-3 names), the family (golden's
    # meta.family tag, the name, or >= 15% of the rows with a family word), the probe / devx sources. Part (ii) also
    # drops every dev / eval source (A8-prime C.6 (a)).
    src_excl, src_excl_p2 = {}, {}
    for s in src_rows:
        why = []
        ch = clash_held(s)
        if ch:
            why.append(f"held-out (OHS) source {ch[:3]}")
        if FAM_SRC.search(s):
            why.append("family source name")
        if src_rowfam[s] >= FAM_SOURCE_SHARE * src_rows[s]:
            why.append(f"family dataset: family tag / name / word on {src_rowfam[s]} of {src_rows[s]} rows")
        if s in P["sources"]:
            why.append("probe/devx source")
        if s in OHS3_HIT_SOURCES:
            why.append("owner OHS-3 12-gram check hit (whole source left out)")
        if why:
            src_excl[s] = why
        c = [x for x in clash(s) if x not in ch]
        if c:
            src_excl_p2[s] = why + [f"dev/eval source {c[:3]} (part (ii) only; the replay keeps it)"]
        elif why:
            src_excl_p2[s] = why
    dsrc_excl = {r["dsrc"] for r in light if r["dsrc"] and (clash_held(r["dsrc"]) or FAM_SRC.search(r["dsrc"])
                                                             or r["dsrc"] in P["sources"])}
    dsrc_excl_p2 = dsrc_excl | {r["dsrc"] for r in light if r["dsrc"] and clash(r["dsrc"])}
    log(f"source-level exclusions: replay {len(src_excl)} sources, {sum(src_rows[s] for s in src_excl):,} rows; part "
        f"(ii) {len(src_excl_p2)} sources, {sum(src_rows[s] for s in src_excl_p2):,} rows; derived-source exclusions "
        f"replay {sorted(dsrc_excl)[:10]}, part (ii) {sorted(dsrc_excl_p2)[:10]}")
    for s in sorted(src_excl_p2, key=lambda x: -src_rows[x]):
        log(f"   excluded source {s} ({src_rows[s]} rows){'' if s in src_excl else ' [part (ii) only]'}: "
            f"{src_excl_p2[s]}")
    g_rels = jl(DATA / GOLD_REL)
    units, merged = td.make_units(light, g_rels)
    if merged:
        raise SystemExit(f"golden make_units merged {merged} inv pairs across call_ids")
    ukey = lambda u: u[0]["call_id"]  # noqa: E731
    if any(len({r["source"] for r in u}) > 1 for u in units):
        raise SystemExit("a golden unit mixes sources")

    def unit_bad(u, strict=False):
        out = set()
        for r in u:
            out |= set(g_why.get(r["id"], []))
            if strict:
                out |= set(g_strict.get(r["id"], []))
            if r["id"] in bad_ids:
                out.add("label_noise_id")
            if r["dsrc"] in (dsrc_excl_p2 if strict else dsrc_excl):
                out.add("excluded_derived_source")
        if u[0]["source"] in (src_excl_p2 if strict else src_excl):
            out.add("excluded_source")
        return out

    ubad = {ukey(u): unit_bad(u) for u in units}
    is_dneg = lambda u: any(r["role"] == "dneg" for r in u)  # noqa: E731
    gt_all = [u for u in units if is_dneg(u)]
    ubad_p2 = {ukey(u): unit_bad(u, strict=True) for u in gt_all}
    gt_extra = {ukey(u): {w for r in u for w in g_extra.get(r["id"], [])} for u in gt_all}
    GT_ok = [u for u in gt_all if not ubad_p2[ukey(u)] and not gt_extra[ukey(u)]]
    log(f"golden units: {len(units):,}; dneg units {len(gt_all)} ({sum(map(len, gt_all))} rows), clean for part (ii) "
        f"{len(GT_ok)} ({sum(map(len, GT_ok))} rows); replay unit-level reasons "
        f"{Counter(w for u in units for w in ubad[ukey(u)]).most_common(14)}")

    # ------------------------------------------------------------ F4 (yn2b polarity ladder)
    y_lines = lines_of(DATA / YN2B_TRAIN)
    y_rows = [json.loads(l) for l in y_lines]
    y_rels = jl(DATA / YN2B_REL)
    f4_idx = [i for i, r in enumerate(y_rows) if r["source"] == "gd_gen3_polarity_ladder"]
    f4_rows = [y_rows[i] for i in f4_idx]
    f4_units, f4_merged = td.make_units(f4_rows, [x for x in y_rels if x["type"] == "inv"])
    f4_why = {}
    for u in f4_units:
        w = set()
        for r in u:
            w |= set(hard(row_reasons(r, R, P, "f4")))
            if r["id"] in bad_ids or derived_rows(r) & bad_ids:
                w.add("label_noise_id")
            ren = (r.get("meta") or {}).get("renderer") or ""
            dsrc = "gd_" + ren.split(".", 1)[1] if ren.startswith("a.") else None
            if dsrc and (dsrc in src_excl_p2 or dsrc in P["sources"] or clash(dsrc) or FAM_SRC.search(dsrc)):
                w.add(f"f4_base_source_excluded:{dsrc}")
        f4_why[u[0]["call_id"]] = sorted(w)
    F4_ok = [u for u in f4_units if not f4_why[u[0]["call_id"]]]
    log(f"F4: {len(f4_rows)} rows in {len(f4_units)} units (merged {f4_merged}); clean {len(F4_ok)} units "
        f"({sum(map(len, F4_ok))} rows); reasons {Counter(w for v in f4_why.values() for w in v).most_common(12)}")

    # ------------------------------------------------------------ part (ii) choice + mix-level shortcut check
    variants = {"none": ([], []), "gt": (GT_ok, []), "gt+f4": (GT_ok, F4_ok)}
    comp = {}
    for k, (gt, f4) in variants.items():
        comp[k] = comp_probe_parts(f7_meta_kept, [r for u in gt + f4 for r in u] if (gt or f4) else [])
        comp[k]["part2_rows"] = sum(map(len, gt)) + sum(map(len, f4))
    log(f"mix-level composition probes (F7 + part ii, yes/no rows): {json.dumps(comp)}")
    if not comp[a.part2]["pass"]:
        raise SystemExit(f"--part2 {a.part2} breaks the checklist composition bars at the mix level: {comp[a.part2]}")
    GT, F4u = variants[a.part2]
    gt_keys = {ukey(u) for u in GT}

    # ------------------------------------------------------------ G_r: stratified replay
    n_target = len(F) + sum(map(len, GT)) + sum(map(len, F4u))
    need = math.ceil(n_target * a.replay_share / (1 - a.replay_share))
    strata = defaultdict(list)
    for u in units:
        if u[0]["source"] in src_excl:
            continue
        strata[(u[0]["source"], unit_kind(u))].append(u)
    rows_stratum = {k: sum(map(len, us)) for k, us in strata.items()}
    pool, pool_stats = {}, {}
    for k, us in sorted(strata.items()):
        us = sorted(us, key=ukey)
        random.Random(SALT + f"{k[0]}|{k[1]}").shuffle(us)
        ok = [u for u in us if ukey(u) not in gt_keys and not ubad[ukey(u)]]
        pool[k] = ok
        pool_stats[k] = {"rows": rows_stratum[k], "units": len(us), "clean_rows": sum(map(len, ok)),
                         "dirty_units": sum(1 for u in us if ubad[ukey(u)] and ukey(u) not in gt_keys),
                         "part2_units": sum(1 for u in us if ukey(u) in gt_keys)}
    elig_rows = sum(rows_stratum.values())

    def take(frac):
        pick, short = {}, {}
        for k, ok in pool.items():
            want = frac * rows_stratum[k]
            got, n = [], 0
            for u in ok:
                if n >= want - 1e-9 or n + len(u) - want > want - n:  # stop at the row count nearest the quota
                    break
                got.append(u)
                n += len(u)
            pick[k] = got
            if n < round(want):
                short[k] = round(want) - n
        return pick, short

    frac = need / elig_rows
    for _ in range(80):
        pick, short = take(frac)
        got = sum(len(u) for us in pick.values() for u in us)
        if got >= need:
            break
        frac *= need / max(1, got) * 1.0003
    else:
        raise SystemExit("could not reach the replay size")
    GR = [u for k in sorted(pick) for u in pick[k]]
    log(f"G_r: fraction {frac:.6f} of each eligible stratum ({len(strata)} strata, {elig_rows:,} eligible rows) -> "
        f"{len(GR)} units, {got} rows (need >= {need}); {len(short)} strata short of quota by {sum(short.values())} rows")

    # ------------------------------------------------------------ assemble rows and relations
    g_take = {r["id"] for u in GT + GR for r in u}
    gt_ids = {r["id"] for u in GT for r in u}
    f4_ids = {r["id"] for u in F4u for r in u}
    lines, rows = [], []
    with open(DATA / GOLD_TRAIN, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r["id"] in g_take:
                lines.append(line if line.endswith("\n") else line + "\n")
                rows.append(r)
    f4_idx_set = {i for i in f4_idx if y_rows[i]["id"] in f4_ids}
    lines += [y_lines[i] for i in sorted(f4_idx_set)]
    rows += [y_rows[i] for i in sorted(f4_idx_set)]
    lines += [f7_lines[i] for i in keep_f7]
    rows += F
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate ids in the mix")
    keep = set(ids)
    by_id = {r["id"]: r for r in rows}
    g_rel_keep = [x for x in g_rels if x["a"] in keep and x["b"] in keep]
    y_rel_keep = [x for x in y_rels if x["a"] in f4_ids and x["b"] in f4_ids]
    if any((x["a"] in keep) != (x["b"] in keep) for x in g_rels if x["a"] in g_take or x["b"] in g_take):
        raise SystemExit("a golden relation has only one end in the mix (units are whole, so this cannot happen)")
    # retype ONLY the units of part (ii) (G_t, F4): a golden dneg unit that the replay drew keeps C1's own 'equiv'
    # relations, so the replay is C1's text AND objective (A8-prime C.4, C.6 (f))
    dneg_calls = {r["call_id"] for r in rows if r.get("role") == "dneg" and (r["id"] in gt_ids or r["id"] in f4_ids)}
    g_rel_new, n_ret_g = retype(g_rel_keep, by_id, dneg_calls, anchor_pair)
    y_rel_new, n_ret_y = retype(y_rel_keep, by_id, dneg_calls, anchor_pair)
    rel_lines = [json.dumps(x, ensure_ascii=False) + "\n" for x in g_rel_new + y_rel_new] + f7_rel_lines
    rels = [json.loads(l) for l in rel_lines]
    cid = {r["id"]: r["call_id"] for r in rows}
    cross = [x for x in rels if cid[x["a"]] != cid[x["b"]]]
    if cross:
        raise SystemExit(f"{len(cross)} relations cross call_ids: {cross[:3]}")
    if any(x["type"] == "equiv" and cid[x["a"]] in dneg_calls for x in rels):
        raise SystemExit("an equiv link is left inside a part (ii) dneg unit")
    gr_ids_all = {r["id"] for u in GR for r in u}
    if any(x.get("retyped_from") and (x["a"] in gr_ids_all or x["b"] in gr_ids_all) for x in rels):
        raise SystemExit("a replay relation was retyped: the replay keeps C1's own objective")
    g_rel_by_pair = {(x["a"], x["b"]): x["type"] for x in g_rel_keep}
    if any(g_rel_by_pair.get((x["a"], x["b"])) != x["type"] for x in rels if x["a"] in gr_ids_all):
        raise SystemExit("a replay relation differs from golden_relations")
    gold_of = {r["id"]: r["gold"] for r in rows}
    if any(x["type"] == "inv" and by_id[x["a"]]["qtype"] == "noul" and by_id[x["b"]]["qtype"] == "noul"
           and gold_of[x["a"]] != gold_of[x["b"]] and x.get("retyped_from") for x in rels):
        raise SystemExit("a retyped inv link joins two yes/no rows with different gold")

    # ------------------------------------------------------------ checks on the final rows
    td.check_rows(rows, 0.5)
    n_kd, n_full = yc.counts_kd(rows, KD_SKIP_SRC, KD_FULL_SRC)
    fin_units, fin_merged = td.make_units(rows, rels)
    if fin_merged:
        raise SystemExit(f"make_units merged {fin_merged} inv pairs across call_ids in the final mix")
    seen, dup_f7, gold_rep = {}, [], 0
    for r in rows:
        k = bf.norm_pair(r)
        if k in seen and cid[seen[k]] != r["call_id"]:
            if seen[k] in f_ids or r["id"] in f_ids or seen[k] in f4_ids or r["id"] in f4_ids:
                dup_f7.append((seen[k], r["id"]))
            else:
                gold_rep += 1
        seen.setdefault(k, r["id"])
    if dup_f7:
        raise SystemExit(f"an F7 / F4 row repeats a (state, instruction) of another unit: {dup_f7[:4]}")
    part_of = lambda i: "F7" if i in f_ids else ("F4" if i in f4_ids else ("G_t" if i in gt_ids else "G_r"))  # noqa: E731
    # probe / devx state overlap with the whole file (SPEC 7.6 direction: each dev state vs the train set)
    train_grams = set()
    for r in rows:
        train_grams |= cy.ghash(r.get("state") or "")
    worst = max((len(g & train_grams) / len(g) for g in P["per_state"] if g), default=0.0)
    over = sum(1 for g in P["per_state"] if g and len(g & train_grams) / len(g) > PROBE_GRAM_MAX)
    if over:
        raise SystemExit(f"{over} probe/devx states share > 20% of their 12-grams with the mix (worst {worst:.3f})")
    log(f"probe/devx state 12-gram share with the mix: worst {worst:.4f} (bar {PROBE_GRAM_MAX})")
    # re-check of every final row with the same function (counts must be 0)
    recheck, gr_report = Counter(), Counter()
    for r in rows:
        pt = part_of(r["id"])
        why = row_reasons(r, R, P, {"F7": "f7", "F4": "f4", "G_t": "gt", "G_r": "gr"}[pt])
        for w in hard(why):
            recheck[(pt, w)] += 1
        if pt == "G_r":
            for w in why:
                if w.endswith("_report_only"):
                    gr_report[w] += 1
        if r["id"] in bad_ids:
            recheck[(pt, "label_noise_id")] += 1
        se, de = (src_excl, dsrc_excl) if pt == "G_r" else (src_excl_p2, dsrc_excl_p2)
        if pt != "F7" and (r["source"] in se or (r.get("meta") or {}).get("derived_source") in de):
            recheck[(pt, "excluded_source")] += 1
        if any(w.startswith("family") for w in why):
            recheck[(pt, "family_any")] += 1
    if recheck:
        raise SystemExit(f"final mix re-check finds hits: {dict(recheck)}")
    n_parts = Counter(part_of(i) for i in ids)
    share_gr = n_parts["G_r"] / len(rows)
    if share_gr < a.replay_share - 1e-12:
        raise SystemExit(f"stratified replay share {share_gr:.4f} < {a.replay_share}")
    log(f"final mix: {len(rows)} rows {dict(n_parts)}; replay share {share_gr:.4f}; kd targets {n_kd}, kd_full "
        f"{n_full}; units {len(fin_units)}")
    if a.dry:
        log("--dry: nothing written")
        return

    # ------------------------------------------------------------ write
    yc.write_lines_atomic(outs["train"], lines)
    yc.write_lines_atomic(outs["rel"], rel_lines)
    yc.write_lines_atomic(outs["f7_train"], [f7_lines[i] for i in keep_f7])
    yc.write_lines_atomic(outs["f7_rel"], f7_rel_lines)
    f7_meta_lines = [l for l in lines_of(DATA / F7["meta"]) if json.loads(l)["id"] in f_ids]
    yc.write_lines_atomic(outs["f7_meta"], f7_meta_lines)
    for dst, src in COPIES.items():
        yc.write_lines_atomic(outs["copy:" + dst], lines_of(DATA / src))
        if sha(DATA / dst) != INPUT_SHA[src]:
            raise SystemExit(f"data/{dst} is not a byte copy of {src}")
    disk = jl(outs["train"])
    if [r["id"] for r in disk] != ids:
        raise SystemExit("file on disk differs from the checked rows")
    if [x["a"] for x in jl(outs["rel"])] != [x["a"] for x in rels]:
        raise SystemExit("relations on disk differ")
    files = {OUT["train"]: sha(outs["train"]), OUT["rel"]: sha(outs["rel"]), OUT["f7_train"]: sha(outs["f7_train"]),
             OUT["f7_rel"]: sha(outs["f7_rel"]), OUT["f7_meta"]: sha(outs["f7_meta"]),
             **{k: sha(DATA / k) for k in COPIES}}

    # ------------------------------------------------------------ counts
    yn = [r for r in rows if r["qtype"] == "noul"]
    gr_dneg_calls = {r["call_id"] for r in rows if part_of(r["id"]) == "G_r" and r.get("role") == "dneg"}
    strat_dev = {}
    for k, ok in pick.items():
        want = frac * rows_stratum[k]
        strat_dev[f"{k[0]}|{k[1]}"] = {"stratum_rows": rows_stratum[k], "quota": round(want, 2),
                                       "picked": sum(map(len, ok))}
    by_src_pick, by_src_elig = Counter(), Counter()
    for k, v in strat_dev.items():
        s = k.split("|")[0]
        by_src_pick[s] += v["picked"]
        by_src_elig[s] += v["stratum_rows"]
    tot_pick = sum(by_src_pick.values())
    src_share_dev = {s: round(by_src_pick[s] / tot_pick - by_src_elig[s] / elig_rows, 5) for s in by_src_elig}
    qt_pick = Counter(r["qtype"] for r in rows if part_of(r["id"]) == "G_r")
    qt_elig = Counter()
    for u in units:
        if u[0]["source"] not in src_excl:
            for r in u:
                qt_elig[r["qtype"]] += 1
    counts = {
        "tool": "extra/build_fix2.py", "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "files": files, "inputs": {**INPUT_SHA, **OTHER_INPUTS, "yn2b/f7_fix2_drops.json": sha(DROPS)},
        "rows": len(rows), "n_relations": len(rels), "relations": dict(Counter(x["type"] for x in rels)),
        "part2": a.part2,
        "parts": {"F7": n_parts["F7"], "G_t_golden_dneg_units": n_parts["G_t"], "F4_polarity_ladder": n_parts["F4"],
                  "G_r_stratified_replay": n_parts["G_r"]},
        "shares": {k: round(v / len(rows), 4) for k, v in n_parts.items()},
        "replay_share_target": a.replay_share, "replay_fraction_of_each_stratum": round(frac, 6),
        "replay_rows_needed": need,
        "units": {"F7_ladders": len(lad), "G_t": len(GT), "F4": len(F4u), "G_r": len(GR), "all": len(fin_units)},
        "F7": {"rows_built": len(f7_rows), "ladders_built": len({r["meta"]["latent_id"] for r in f7_rows}),
               "dropped_pairs": f7_drop_reason, "rows_kept": len(F),
               "ladders_kept": len(lad), "relations": dict(Counter(x["type"] for x in F_rel)),
               "inv_anchor_is_R0": sum(1 for x in F_rel if x["type"] == "inv" and f7_meta[x["a"]]["rung"] == "R0"),
               "inv_anchor_other_rung": dict(Counter(f7_meta[x["a"]]["rung"] for x in F_rel
                                                     if x["type"] == "inv" and f7_meta[x["a"]]["rung"] != "R0")),
               "ladders_with_R0": sum(1 for u in lad.values() if any(f7_meta[x["id"]]["rung"] == "R0" for x in u)),
               "max_complement_per_row": max(ncomp.values()) if ncomp else 0,
               "max_ladder_rows": max(map(len, lad.values())), "max_ladder_total_state_chars": max(unit_chars.values())},
        "retyped": {**{f"golden {k}": v for k, v in n_ret_g.items()}, **{f"F4 {k}": v for k, v in n_ret_y.items()}},
        "composition_probes_mix_level": comp,
        "qtype": dict(Counter(r["qtype"] for r in rows)),
        "roles": dict(Counter(r.get("role") for r in rows).most_common()),
        "dneg_rows": sum(1 for r in rows if r.get("role") == "dneg"),
        "yes_share_noul": round(sum(1 for r in yn if float(r["gold"]) >= 0.5) / max(1, len(yn)), 4),
        "kd_targets": n_kd, "kd_full": n_full, "kd_skip_src": KD_SKIP_SRC, "kd_full_src": KD_FULL_SRC,
        "teacher_dict_rows_by_part": dict(Counter(part_of(r["id"]) for r in rows if yc.kd_target(r) is not None)),
        "replay": {"eligible_rows": elig_rows, "eligible_sources": len({k[0] for k in strata}), "strata": len(strata),
                   "strata_short": {f"{k[0]}|{k[1]}": v for k, v in short.items()},
                   "max_abs_source_share_deviation": max(abs(v) for v in src_share_dev.values()),
                   "qtype_share_picked": {k: round(v / max(1, n_parts["G_r"]), 4) for k, v in qt_pick.items()},
                   "qtype_share_eligible": {k: round(v / elig_rows, 4) for k, v in qt_elig.items()},
                   "per_stratum": strat_dev},
        "exclusions": {
            "excluded_sources": src_excl,
            "excluded_source_rows": sum(src_rows[s] for s in src_excl),
            "excluded_derived_sources": sorted(dsrc_excl),
            "excluded_sources_part2": src_excl_p2,
            "excluded_source_rows_part2": sum(src_rows[s] for s in src_excl_p2),
            "excluded_derived_sources_part2": sorted(dsrc_excl_p2),
            "replay_rule": "G_r = byte copies of C1's own golden_train units: held-out (OHS-1/2, OHS-3 names, JevBench) "
                           "source / 12-gram / template filters, never a dev / eval / OHS row (ids, (state, "
                           "instruction) pairs), the family, the probe / devx, label noise; the dev / eval 12-gram, "
                           "template and frame filters are report only (replay_dev_overlap_report_only)",
            "replay_dev_overlap_report_only": dict(gr_report),
            "replay_rows_from_dev_eval_sources": sum(1 for r in rows if part_of(r["id"]) == "G_r"
                                                     and r["source"] in src_excl_p2),
            "replay_dev_eval_sources_drawn": sorted({r["source"] for r in rows if part_of(r["id"]) == "G_r"
                                                     and r["source"] in src_excl_p2}),
            "golden_row_reasons": dict(g_report),
            "golden_unit_reasons": dict(Counter(w for u in units for w in ubad[ukey(u)])),
            "golden_dneg_units": {"all": len(gt_all), "clean": len(GT_ok), "rows_clean": sum(map(len, GT_ok)),
                                  "reasons": dict(Counter(w for u in gt_all
                                                          for w in ubad_p2[ukey(u)] | gt_extra[ukey(u)]))},
            "golden_dneg_units_in_replay": {"units": len(gr_dneg_calls),
                                            "rows": sum(1 for r in rows if part_of(r["id"]) == "G_r"
                                                        and r["call_id"] in gr_dneg_calls),
                                            "relations_kept_as_in_golden": "yes (not retyped)"},
            "f4_units": {"all": len(f4_units), "clean": len(F4_ok), "rows_clean": sum(map(len, F4_ok)),
                         "reasons": dict(Counter(w for v in f4_why.values() for w in v))},
            "family_rows_by_source_top": dict(src_rowfam.most_common(30)),
            "probe_refs": {"states": len(P["states"]), "sources": sorted(P["sources"]),
                           "heldout_runs6": len(P["runs6"]), "word_lexemes": [x for x, _ in P["lex"]]},
            "probe_state_12gram_share_worst": round(worst, 4),
            "ref_sources": len(R["ref_sources"]), "ohs3_names": R["o3_names"],
            "negbench": R["negbench_info"]["sources"], "failure_questions": R["fail_n"],
            "golden_rows_repeated_in_another_unit_as_in_golden_train": gold_rep,
            "final_recheck_hits": 0, "ohs3_data": "never opened (12-gram check vs OHS-3 is owner-only: "
                                                  "extra/fix2_ohs3_blind.py)"},
    }
    yc.write_lines_atomic(outs["counts"], [json.dumps(counts, indent=1, ensure_ascii=False, default=str)])
    log(f"wrote {OUT['train']} ({len(rows)} rows, sha256 {files[OUT['train']]}), {OUT['rel']} ({len(rels)} relations, "
        f"sha256 {files[OUT['rel']]})")
    print(json.dumps({k: counts[k] for k in ("rows", "parts", "shares", "units", "relations", "retyped", "dneg_rows",
                                             "kd_targets", "kd_full", "yes_share_noul", "files")}, indent=1))


if __name__ == "__main__":
    main()
