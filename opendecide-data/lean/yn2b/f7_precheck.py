#!/usr/bin/env python
"""f7_precheck.py: the ship audit of family F7 'nested negation' (yn2b/F7_COVERAGE_CHECKLIST.md section 4).

Written independently of every F7 generator: it never imports a generator or its lexicon. It reads the built rows, their
relations and the per-row SIDECAR meta (data/v14_parts/f7_meta.jsonl, f7_probe_meta.jsonl, f7_devx_meta.jsonl), and it
evaluates each row's logical form (LF) with its OWN evaluator. Every numeric target of checklist section 3 is a named
constant below that cites its checklist line (CL:<line>).

Checks (one printed line per sub-check, number + status; the whole report goes to yn2b/f7_precheck.json):
  1 schema          sidecar fields, enums, LF well-formed, cue <-> LF consistency, row format, train_decoder.check_rows
  2 gold            LF re-evaluation = gold, distractor-deletion test, decide2 parse-back (+ independence), bivalence
                    line, non-presupposing distractors, choice LF
  3 coverage        checklist items 1-38 vs floors (train / dev / holdout), caps, tag consistency, depth x position x
                    class cells, lexicon, frames, size, depth mix, dev size, ladder kinds, distance bins, embedding depth
  4 balance         yes share per (depth x cue count) cell, rung and stratum; truth(P) per rung / depth / label; choice
                    rows; card-less rows; card style; distractors; parity; cue mix; cue positions
  5 surface probes  (a)-(j) with 5-fold CV grouped by ladder (+ train -> dev), |r| < 0.05, yes/no lines restate the
                    question, SPEC 8.4 TF-IDF
  6 composition     C1-C7 and the per-lexeme cue share
  7 EXCLUDE         regex scan X1-X12 over instructions, cards and options (state exempt, hits tagged); rule 2.11
  8 decontamination build_fix1.load_refs 12-gram sets, 6-word runs (dev / v11 / public negation benchmarks / the measured
                    failure frame / OHS-3 negation frames read from build_ohs3.py TEXT), dev / eval frames, ids, banned
                    words, SPEC 7.3 cue share, 7.4 unseen set, 7.5 dedupe, 7.7 names, dev sources; OHS-3 = owner step
  9 ladder          identical state, size, relations vs parity, R0 share, both golds, rung semantics, one side of split
  10 hold-out       held-out lexemes (with inflections) / frames / families / cue combinations / sources absent from
                    train; counts; 12-gram share <= 20%; iid != train; group-disjoint; not golden_train states; name pools
  11 blind read     (needs --blind-read; --write-blind-sample makes the sample without gold)

Statuses: PASS, FAIL, PENDING (an input or an owner step is missing: decide2 preds, blind read, OHS-3), SKIP (--fast).
Exit code: 1 if any FAIL; else 2 if any PENDING or SKIP; else 0 (ship only on 0).

Interpretations the checklist leaves open (each is a named constant or documented at its check):
  - share targets use the project's SPEC 4.6 integer rule (mv_core.share_ok): |k - n*mid| <= max(n*halfwidth, 1), so a
    stratum is held to the exact band once it is large enough and to 'within one row of the target' below that;
  - depth mix: the point targets of CL:313-315 with a tolerance of DEPTH_MIX_TOL;
  - C6 'ignore one class': a cue COUNTER that skips one class (all cues, incl. distractors and look-alikes); the
    scope-aware variant is reported as information;
  - C7 needs the sidecar field 'antonym_gold' (gold under the antonym reading) on item-21 rows;
  - 'held out' = declared in --holdout-spec, plus everything that occurs in holdout rows and in no train row;
  - a NOT node may carry "cue": null (an implicit flip with no cue word, e.g. the AR rung's complement label);
  - a CHOICE node may carry "cue" (the negated-selection cue word), which counts as scoping.
Arbiter fixes (2 Oct 2026, rulings in yn2b/F7_OBJECTIONS.md; no threshold changed):
  - 4.3 'truth(P) per depth' counts yes/no rows only (on a choice row truth_P == depth even by this tool's own
    definitions); 'per rung' still counts all rows (O1);
  - 3.5b checks generator rows (train, probe) only, not the blind hand-written devx (O2);
  - 3.3 rule for item 26 also accepts an AND / OR over >= 3 members (O2);
  - 4.13: a lexicon can_distract=false flag no longer exempts a syntactic lexeme or one used as a distractor (A1);
  - 8.11 also fails on a row that repeats another row of the same ladder byte for byte (A2).

  cd opendecide-data/lean && PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python yn2b/f7_precheck.py \
      [--train data/v14_parts/f7_train.jsonl] [--probe data/v14_parts/f7_probe.jsonl] [--devx data/v14_parts/f7_devx.jsonl]
      [--meta data/v14_parts/f7_meta.jsonl data/v14_parts/f7_probe_meta.jsonl data/v14_parts/f7_devx_meta.jsonl]
      [--decide2-preds P --decide2-code C --decide2-independent yes|no] [--blind-read B] [--fast] [--out yn2b/f7_precheck.json]
CPU only. No network, no model. OHS-3 data is never opened unless the OWNER passes --ohs3-blind (counts only).
"""
from __future__ import annotations

import argparse
import ast
import bisect
import glob
import hashlib
import json
import math
import os
import random
import re
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

LEAN = Path(__file__).resolve().parents[1]
YN2B = LEAN / "yn2b"
for _p in (str(LEAN), str(YN2B), str(LEAN / "extra")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True

CHECKLIST = "yn2b/F7_COVERAGE_CHECKLIST.md"

# ===================================================================================================== section 3 targets
# ---- phenomenon priorities (CL:39-172) and per-item checklist lines
PRIORITY = {1: "MUST", 2: "MUST", 3: "MUST", 4: "MUST", 5: "MUST", 6: "MUST", 7: "SHOULD", 8: "MUST", 9: "NICE",
            10: "MUST", 11: "MUST", 12: "MUST", 13: "MUST", 14: "SHOULD", 15: "MUST", 16: "MUST", 17: "SHOULD",
            18: "SHOULD", 19: "SHOULD", 20: "SHOULD", 21: "MUST", 22: "MUST", 23: "SHOULD", 24: "MUST", 25: "NICE",
            26: "SHOULD", 27: "MUST", 28: "SHOULD", 29: "NICE", 30: "SHOULD", 31: "SHOULD", 32: "SHOULD", 33: "SHOULD",
            34: "SHOULD", 35: "SHOULD", 36: "MUST", 37: "SHOULD", 38: "SHOULD"}
ITEM_LINE = {1: 39, 2: 41, 3: 43, 4: 45, 5: 49, 6: 53, 7: 56, 8: 58, 9: 61, 10: 64, 11: 68, 12: 71, 13: 76, 14: 79,
             15: 86, 16: 89, 17: 93, 18: 96, 19: 99, 20: 103, 21: 113, 22: 117, 23: 119, 24: 122, 25: 125, 26: 131,
             27: 133, 28: 136, 29: 138, 30: 141, 31: 143, 32: 145, 33: 151, 34: 155, 35: 158, 36: 166, 37: 169, 38: 172}
ITEM_NAME = {1: "depth-0 anchor", 2: "depth 1 clausal not in statement frame", 3: "depth 1 truth-value frame",
             4: "depth 1 lexical verb only", 5: "depth 1 affixal card label", 6: "depth 2 two classes",
             7: "depth 2 same class twice", 8: "depth 3 mixed", 9: "depth 4 stress", 10: "attributed negated claim",
             11: "card + question split", 12: "cross-sentence / distant", 13: "answer mapping",
             14: "inverted yes/no key", 15: "side-clause distractor", 16: "scoping + distractor",
             17: "two distractors, no scope", 18: "card-line distractor", 19: "negation in state",
             20: "look-alikes", 21: "not X != antonym", 22: "residual labels", 23: "exclusion clause",
             24: "only + negation", 25: "broader term as list", 26: "not all / none", 27: "only over negated set",
             28: "numeric bounds", 29: "approximate negators", 30: "De Morgan", 31: "exceptors",
             32: "not X but Y", 33: "must not / need not", 34: "unless / only if", 35: "non-factive scope edit",
             36: "negated choice selection", 37: "choice decoys", 38: "inner-negative polar question"}
ITEM_CAP = {9: (0.03, 61), 14: (0.10, 80), 38: (0.05, 172)}          # 'at most x% of rows' (train and dev; see 3.2)
# items whose checklist text requires a negation (CL:136 'numeric bounds WITH negation'; CL:141 De Morgan 'not both',
# 'neither ... nor', 'not (A or B)'): a row counts toward their floors only with a scoping negation (depth >= 1). The
# unnegated anchors keep the tag (3.3 accepts it) but never fill the floor. Item 31 (exceptors, CL:143) keeps its
# depth-0 rows: its own checklist example has no negation.
DEPTH1_ITEMS = (28, 30)
# ---- floors per phenomenon (CL:304-308): (train rows, dev rows iid+holdout, of which holdout)
FLOORS = {"full": {"MUST": (400, 40, 20), "SHOULD": (150, 20, 10), "NICE": (40, 10, 5)},       # CL:306-308
          "minimum": {"MUST": (200, 40, 20), "SHOULD": (75, 20, 10), "NICE": (0, 10, 5)}}  # CL:306-308 (1,000 ladders)
# ---- size (CL:297-300)
PLAN_LADDERS = 2500             # CL:298 (an estimate, reported)
TRAIN_ROWS_RESEARCH_MIN = 10000  # CL:298 research range 10-25K rows (full budget floor)
TRAIN_ROWS_RESEARCH_MAX = 25000  # CL:298 (reported)
TRAIN_LADDERS_MIN = 1000        # CL:299 never below 1,000 ladders
TRAIN_ROWS_AT_MIN = 4500        # CL:299-300 about 4.5K rows at the minimum
# ---- depth mix (CL:311-317)
DEPTH_MIX = {0: 0.18, 1: 0.25, 2: 0.30, 3: 0.24}   # CL:313-315
DEPTH4_MAX = 0.03                                  # CL:315 and CL:61
DEPTH_MIX_TOL = 0.02                               # tool tolerance around the CL:315 point targets
PARITY_SHARE = (0.45, 0.55)                        # CL:317 'odd and even parity at about 50/50' (stratum band CL:324)
# ---- balance (CL:319-327)
YES_CELL = (0.48, 0.52)          # CL:323 (depth x total cue count) cells and each rung
YES_STRATUM = (0.45, 0.55)       # CL:324 every other stratum
TRUTHP_RUNG_DEPTH = (0.48, 0.52)  # CL:325
TRUTHP_LABEL = (0.45, 0.55)      # CL:326
CHOICE_SHARE = (0.17, 0.23)      # CL:327 choice rows 20% +- 3 of rows
CHOICE_OPTS = (3, 5)             # CL:327 option count 3-5
CHOICE_POS_TOL = 0.03            # CL:327 gold position uniform +- 3 points per option count
CHOICE_NEGSEL = (0.45, 0.55)     # CL:327 'negated selection in 50% of choice rows' (stratum band CL:324)
CARDLESS_TOL = 0.02              # CL:231-232 card-less share equal at every depth and gold within +- 2 points
CARD_STYLE_TOL = 0.02            # CL:403 'card style per depth and gold' (same +- 2 points rule as CL:232)
STATE_NEG_TOL = 0.02             # CL:100-101 'the yes share must be the same' with and without state negation
# ---- distractors and parity (CL:329-335)
DIST_ANY_MIN = 0.35              # CL:333
DIST_PER_DEPTH_MIN = 0.25        # CL:333 within each depth 0-3
PARITY_MISMATCH_MIN = 0.30       # CL:334
AR_LEXONLY_MIN = 0.15            # CL:335 share of odd-parity rows
# ---- cue mix (CL:337-351)
CUE_MIX = {"syntactic": (0.25, 0.35), "affixal": (0.20, 0.30), "lexical": (0.20, 0.30),
           "truth_frame": (0.10, 0.15), "cross+answer": (0.05, 0.10)}   # CL:341-345
NOT_NT_MAX = 0.20                # CL:348
LEXEME_MAX = 0.10                # CL:348
LEXEME_MIN_ROWS = 30             # CL:349
LEXEME_ODD = (0.40, 0.60)        # CL:350 (and CL:246)
DISTRACT_USE_MIN = 0.10          # CL:351
# ---- cue positions, share of scoping cue tokens (CL:353-362)
POSITION_MIX = {"inner_claim": (0.25, 0.35), "outer_frame": (0.20, 0.30), "card_def": (0.15, 0.25),
                "separate_sentence": (0.05, 0.10), "yn_key+answer_map": (0.05, 0.10),
                "choice_option": (0.05, 0.10)}                          # CL:357-362
# ---- ladder types (CL:364-365, CL:220)
CARD_LADDER_MIN = 0.50           # CL:364
MULTITEXT_LADDERS = (0.10, 0.20)  # CL:364
# ---- frames and lexicon (CL:367-370, CL:258-272)
TRAIN_FAMILIES_MIN = 12          # CL:368
FRAMES_PER_FAMILY_MIN = 4        # CL:368
TRAIN_LEXEMES_MIN = 60           # CL:368 (CL:259)
LEXICON_CLASSES = 5              # CL:259-260
HOLD_FAMILIES_MIN = 3            # CL:369 (CL:269)
HOLD_LEXEMES_MIN = 15            # CL:369
HOLD_LEXEME_SHARE_MIN = 0.20     # CL:270
HOLD_COMBOS_MIN = 2              # CL:271
HOLD_SOURCES_MIN = 2             # CL:272
FRAME_MAX = 0.04                 # CL:370 (CL:265)
CARRIER_MAX = 0.03               # CL:370 (CL:265)
# ---- dev (CL:372-376)
DEV_IID_LADDERS_MIN = 150        # CL:373
DEV_HOLD_LADDERS_MIN = 150       # CL:373
DEV_ROWS_MIN = 1300              # CL:373
DEV_DEPTH_ROWS_MIN = 200         # CL:374 depth 0-3, iid + holdout
DEV_DEPTH4_MIN = 40              # CL:374
DEVX_ROWS_MIN = 100              # CL:375 (CL:274)
# ---- ladders (CL:205-219, SPEC 4.9)
LADDER_MAX_ROWS = 5              # CL:206
LADDER_MAX_ROWS_LONG = 3         # CL:207
LONG_STATE_CHARS = 6000          # CL:207
UNIT_STATE_MAX = 24000           # SPEC 4.9
R0_TRAIN_MIN = 0.80              # CL:215
R0_DEV_MIN = 1.00                # CL:215
# ---- audit (CL:380-458)
CELL_MIN_ROWS = 30               # CL:399-400
DISTANCE_BIN_MIN_ROWS = 30       # CL:71-73 'cover these distance bins' (tool: the CL:400 cell floor per bin)
EMBED_DEPTH_MIN_ROWS = 30        # CL:257 'vary the clause-embedding depth from 0 to 3' (tool: CL:400 floor per level)
DECIDE2_BUG_SHARE = 0.01         # CL:203-204, CL:396 (> 1% disagreement = generator bug); target 100%
PROBE_MAX = 0.55                 # CL:418
PROBE_STRATUM_MAX = 0.60         # CL:418
PROBE_STRATUM_MIN_N = 100        # CL:418
CORR_MAX = 0.05                  # CL:420
CV_FOLDS = 5                     # CL:406
C1_BAND = (0.45, 0.55)           # CL:426
C2_MAX, C2_DEPTH_MAX = 0.70, 0.75  # CL:427
C3_MAX = 0.65                    # CL:428
C4_MAX = 0.60                    # CL:429
C5_MAX = 0.60                    # CL:430
C6_MAX = 0.60                    # CL:431
C7_WRONG_MIN = 0.30              # CL:432
CUE_SHARE_BAND = (0.40, 0.60)    # CL:433
CUE_SHARE_MIN_ROWS = 30          # CL:433
DEV_TRAIN_12G_MAX = 0.20         # CL:453 (SPEC 7.6)
BLIND_RANDOM = 100               # CL:456
BLIND_PER_MUST = 10              # CL:456
BLIND_BAD_MAX = 0.03             # CL:458
MAX_AFFIX_PER_WORD = 1           # CL:277
MAX_CUES_PER_CLAUSE = 2          # CL:277
SPEC_CUE_SHARE_MAX = 0.60        # SPEC 7.3 (cue-share rule <= 60%)
SPEC_TFIDF_Q_MAX = 0.55          # SPEC 8.4 question alone
SPEC_TFIDF_SQ_MAX = 0.60         # SPEC 8.4 state + question
OHS3_FRAME_RUN = 5               # tool: OHS-3 frames are short, so their fixed text is banned at 5-word runs

# ===================================================================================================== contract enums
RUNGS = ("R0", "N1", "N2", "N3", "N4", "D", "AR", "CH")
CLASSES = ("syntactic", "affixal", "lexical", "truth_frame", "cross_sentence", "answer_mapping", "lookalike")
POSITIONS = ("outer_frame", "inner_claim", "card_def", "yn_key", "answer_map", "separate_sentence", "choice_option",
             "state")
DISTANCES = ("same_clause", "same_sentence", "next_sentence", "far", "other_field")
LADDER_KINDS = ("card", "multitext", "record")
DEV_KINDS = ("train", "iid", "holdout", "devx")
OPS = ("ATOM", "NOT", "AND", "OR", "ATLEAST", "ATMOST", "EXACTLY", "DIST", "CORE", "CHOICE")
REQUIRED = {"id": str, "ladder_id": str, "rung": str, "lf": dict, "truth_P": bool, "depth": int, "n_cues": int,
            "n_distractor": int, "cues": list, "phen": list, "frame_family": str, "frame_id": str, "ladder_kind": str,
            "source": str, "dev_kind": str, "card_style": str, "gold": int}
CUE_REQUIRED = {"lexeme": str, "cls": str, "position": str, "scoping": bool, "distance": str}
PART_KINDS = {"train": ("train",), "probe": ("iid", "holdout"), "devx": ("devx",)}
CLASS5 = {"syntactic": "syntactic", "affixal": "affixal", "lexical": "lexical", "truth_frame": "truth_frame",
          "cross_sentence": "cross+answer", "answer_mapping": "cross+answer"}
# depth x position x class cells that must each hold >= CELL_MIN_ROWS train rows at depth 1-3 (CL:399-400). The
# checklist does not list the allowed cells; this matrix is the tool's reading of rules 2.7-2.8 and section 1.
ALLOWED_CELLS = {"outer_frame": ("syntactic", "lexical", "truth_frame"),
                 "inner_claim": ("syntactic", "affixal", "lexical"),
                 "card_def": ("syntactic", "affixal", "lexical"),
                 "yn_key": ("answer_mapping",),
                 "answer_map": ("answer_mapping",),
                 "separate_sentence": ("cross_sentence",),
                 "choice_option": ("syntactic", "affixal", "lexical")}
QUESTION_POSITIONS = ("outer_frame", "inner_claim", "separate_sentence", "answer_map", "choice_option")
CARD_ITEMS = (21, 22, 23, 24, 25)          # CL:111 'card-format ladders over real texts'
MULTITEXT_ITEMS = (26, 27, 28, 29, 30, 31)  # CL:129, CL:226

# ===================================================================================================== text helpers
NARROW_RE = re.compile(r"\b(?:not|no|never|none|cannot)\b|n't\b", re.I)           # CL:413 narrow lexicon
NOT_RE = re.compile(r"\bnot\b|n't\b|\bcannot\b", re.I)
STATE_NEG_RE = re.compile(r"\b(?:not|no|never|none|nothing|nobody|nowhere|neither|nor|without|cannot)\b|n't\b", re.I)
QUOTE_RE = re.compile(r"\"[^\"\n]{1,120}\"|“[^”\n]{1,120}”|(?:(?<=\s)|^)'[^'\n]{1,80}'(?=[\s?.,;:!)]|$)")
YN_LINE_RE = re.compile(r"^\s*-\s*(yes|no)\s*:", re.I)
CARD_KEY_RE = re.compile(r"^\s*-\s*([^:]{1,120}):")
SENT_SPLIT_RE = re.compile(r"(?<=[.?!])\s+")
CLAUSE_SPLIT_RE = re.compile(r"[,;:.?!()\n]|\b(?:that|whether|if|unless|because|while|although)\b", re.I)
BIVALENCE_CUE_RE = re.compile(r"\b(?:refut\w*|unsupported|unfounded|baseless|contradict\w*|disput\w*|fail(?:s|ed|ing)?\s+"
                              r"to\s+(?:show|support|establish|bear)|settle\w*)\b", re.I)
BIVALENCE_LINE_RE = re.compile(r"\b(?:settles?|settled|decides?|decided)\s+(?:every|each|all|the)\b|\beither\s+holds?\s+"
                               r"or\s+fails?\b|\bis\s+either\s+true\s+or\s+false\b|\bevery\s+claim\s+(?:asked|here)"
                               r"[^.\n]*\b(?:true\s+or\s+false|holds?\s+or\s+fails?)\b", re.I)
PRESUPPOSING_RE = re.compile(r"(?:^|[.?!]\s+)(?:given\s+that|since|because|as|now\s+that|seeing\s+that)\b[^?]*,", re.I)
NONPRESUP_RE = re.compile(r"\b(?:whether\s+or\s+not|even\s+if|regardless\s+of\s+whether|no\s+matter\s+whether|"
                          r"irrespective\s+of\s+whether)\b", re.I)
CARDLESS_OK_RE = re.compile(r"\bis\s+it\s+(?:true|false)\s+that\b", re.I)                     # CL:231
LOGIC_LINE_RE = re.compile(r"(?:read|taken|understood|interpreted)\s+(?:literally|logically|strictly)|"
                           r"quantifiers?\s+(?:are|is)\s+(?:read|taken|meant)|\bmeans?\s+at\s+least\s+one\b|"
                           r"['\"“]?not\s+all['\"”]?\s+means\b|\bat\s+least\s+one\b[^.\n]{0,60}\bnot\b", re.I)
LOOKALIKE_RE = re.compile(r"\b(?:under|universal|universe|unique|uniform|union|unit|units|understand\w*|discuss\w*|"
                          r"interest\w*|display\w*|nonetheless|notabl[ey]|not\s+only|nothing\s+but)\b", re.I)
AFFIX_STOP = {"under", "until", "unit", "units", "unique", "universal", "universe", "uniform", "union", "united",
              "understand", "understood", "understanding", "unless", "undertake", "underlying", "underneath",
              "discuss", "discussion", "display", "displayed", "distance", "district", "distinct", "discount",
              "dispatch", "disk", "disc", "discover", "disclose", "disciplinary", "discipline", "dish", "dishes",
              "disease", "diseases", "nonetheless", "none", "regardless", "nevertheless", "doubtless", "unusual",
              "unanimous", "unanimously", "dishwasher", "distribution", "distributed", "display", "disposal"}
AFFIX_WORD_RE = re.compile(r"\b(?:non-?[a-z]{3,}|un[a-z]{3,}|dis[a-z]{3,}|[a-z]{3,}less|[a-z]{2,}-free)\b", re.I)


def words(t):
    return re.findall(r"[a-z0-9']+", (t or "").lower())


def mask_quotes(t):
    return QUOTE_RE.sub(" QUOTED ", t or "")


def card_lines(card):
    return [ln for ln in (card or "").split("\n") if ln.strip()]


def yn_lines(card):
    return [ln for ln in card_lines(card) if YN_LINE_RE.match(ln)]


def def_lines(card):
    return [ln for ln in card_lines(card) if not YN_LINE_RE.match(ln)]


def card_keys(card):
    out = set()
    for ln in def_lines(card):
        m = CARD_KEY_RE.match(ln)
        if m:
            out.add(m.group(1).strip().lower())
    return out


def mask_card_line(ln):
    """A card definition line with its label key masked (a label name is a mention, not a use)."""
    m = CARD_KEY_RE.match(ln)
    return ("- KEY:" + ln[m.end():]) if m else ln


def authored_texts(row):
    """F7-authored text a row shows: instruction, options, the card's yes/no lines (without the '- yes:' key)."""
    return [row.get("instructions") or ""] + [o for o in (row.get("options") or []) if isinstance(o, str)] + \
        [YN_LINE_RE.sub("", ln, count=1).strip() for ln in yn_lines(row.get("card"))]


def inflections(lex):
    """Surface forms of a word lexeme (first word inflected for a multi-word lexeme). Affix lexemes return []."""
    lex = (lex or "").strip().lower()
    if not lex or lex.startswith("-") or lex.endswith("-"):
        return []
    parts = lex.split()
    w, rest = parts[0], (" " + " ".join(parts[1:])) if len(parts) > 1 else ""
    forms = {w}
    if w in ("n't", "nt"):
        return ["n't"]
    if len(w) > 2 and w.endswith("y") and w[-2] not in "aeiou":
        forms |= {w[:-1] + "ies", w[:-1] + "ied", w + "ing"}
    elif w.endswith("e"):
        forms |= {w + "s", w + "d", w[:-1] + "ing"}
    elif w.endswith(("s", "x", "z", "ch", "sh")):
        forms |= {w + "es", w + "ed", w + "ing"}
    else:
        forms |= {w + "s", w + "ed", w + "ing"}
        if len(w) >= 3 and w[-1] not in "aeiouwxy" and w[-2] in "aeiou" and w[-3] not in "aeiou":
            forms |= {w + w[-1] + "ed", w + w[-1] + "ing"}
    return sorted(f + rest for f in forms)


def lexeme_regex(lex):
    forms = inflections(lex)
    if not forms:
        return None
    alts = "|".join(re.escape(f).replace(r"\ ", r"\s+") for f in sorted(forms, key=len, reverse=True))
    if lex.strip().lower() in ("n't", "nt"):
        return re.compile(r"n't\b", re.I)
    return re.compile(r"(?<![\w-])(?:" + alts + r")(?![\w-])", re.I)


def share_ok(k, n, lo, hi):
    """The band test as integers allow, the project's SPEC 4.6 rule (golden_src/gen3/mv_core.share_ok):
    |k - n * mid| <= max(n * halfwidth, 1), i.e. exactly [lo, hi] once n * halfwidth >= 1, else within one row."""
    if n <= 0:
        return True
    mid, half = (lo + hi) / 2, (hi - lo) / 2
    return abs(k - n * mid) <= max(n * half, 1.0) + 1e-9


def within(k, n, target, tol):
    return abs(k - n * target) <= max(n * tol, 1.0) + 1e-9


def r3(x):
    return None if x is None else round(float(x), 4)


def state_format(s):
    s = (s or "").lstrip()
    if s.startswith(("{", "[")):
        return "json"
    lines = [ln for ln in (s or "").split("\n") if ln.strip()]
    if sum(1 for ln in lines if ln.strip().startswith("|")) >= 2:
        return "md_table"
    if lines and sum(1 for ln in lines if ln.strip().startswith(("- ", "* "))) >= max(2, len(lines) // 2):
        return "bullets"
    if len(lines) >= 3 and len({ln.count(",") for ln in lines[:5]}) == 1 and lines[0].count(",") >= 2:
        return "csv"
    if len(lines) >= 3 and sum(1 for ln in lines if re.match(r"^[\w .-]{1,30}:\s", ln)) >= len(lines) // 2:
        return "key_value"
    return "prose"


def carrier(text):
    t = mask_quotes(text)
    t = re.sub(r"\d+", "0", t)
    t = re.sub(r"(?<=\s)[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?(?:\s+[A-Z]-0)?", "NAME", t)
    return " ".join(t.lower().split())


def quoted_label(row, m):
    if isinstance(m.get("quoted_label"), str):
        return m["quoted_label"]
    q = QUOTE_RE.search(row.get("instructions") or "")
    return q.group(0).strip(" '\"“”") if q else None


# ===================================================================================================== LF
class LFInfo:
    __slots__ = ("errors", "refs", "cores", "choice", "depth", "truth_P", "gold", "has_null_not", "ops", "core_sig",
                 "n_dist_nodes", "gold_options")

    def __init__(self):
        self.errors, self.refs, self.cores = [], defaultdict(list), []
        self.choice = None
        self.depth = self.truth_P = self.gold = None
        self.has_null_not, self.ops, self.core_sig, self.n_dist_nodes = False, Counter(), None, 0
        self.gold_options = None


class Undefined(Exception):
    """A distractor whose own semantics leave the question without a determinate answer (a false presupposition)."""


def lf_eval(node, full=False):
    """Contract semantics: DIST evaluates to its child. full=True also applies a DIST node's optional own semantics:
    "mode": "vacuous" (default: whether or not / even if / a format line), "presupposed" ('given that S') or
    "conditional" ('if S, ...'), with "side": the lf of S; a false S leaves the gold undefined."""
    op = node["op"]
    if op == "ATOM":
        return bool(node["val"])
    if op == "NOT":
        return not lf_eval(node["child"], full)
    if op == "DIST" and full and node.get("mode") in ("presupposed", "conditional"):
        if "side" not in node or not lf_eval(node["side"], full):
            raise Undefined(f"{node.get('mode')} distractor side is false or missing")
        return lf_eval(node["child"], full)
    if op in ("DIST", "CORE"):
        return lf_eval(node["child"], full)
    if op == "AND":
        return all(lf_eval(c, full) for c in node["children"])
    if op == "OR":
        return any(lf_eval(c, full) for c in node["children"])
    s = sum(1 for c in node["children"] if lf_eval(c, full))
    k = node["k"]
    if op == "ATLEAST":
        return s >= k
    if op == "ATMOST":
        return s <= k
    if op == "EXACTLY":
        return s == k
    raise ValueError(op)


def choice_gold(lf, full=False):
    want = lf["select"] == "true"
    return [i for i, o in enumerate(lf["options"]) if lf_eval(o, full) == want]


def lf_analyse(lf, n_cues, is_choice):
    """Validates the tree and derives depth / truth_P / gold with this tool's own evaluator."""
    I = LFInfo()
    if not isinstance(lf, dict):
        I.errors.append("lf is not an object")
        return I
    path_nots = set()

    def rec(node, anc, under_core, opt):
        if not isinstance(node, dict) or node.get("op") not in OPS:
            I.errors.append(f"bad node {str(node)[:60]}")
            return
        op = node["op"]
        I.ops[op] += 1
        if op == "ATOM":
            if not isinstance(node.get("val"), bool):
                I.errors.append("ATOM val is not a bool")
            if not isinstance(node.get("id"), str):
                I.errors.append("ATOM id is not a string")
            return
        if op == "CHOICE":
            I.errors.append("CHOICE below the root")
            return
        if op in ("NOT", "DIST"):
            c = node.get("cue", "missing")
            if op == "DIST" and (not isinstance(c, int) or isinstance(c, bool)):
                I.errors.append("DIST without an int cue")
            elif op == "NOT" and c == "missing":
                I.errors.append("NOT without a cue key (use null for an implicit flip)")
            elif c is not None and c != "missing" and (not isinstance(c, int) or isinstance(c, bool) or not 0 <= c < n_cues):
                I.errors.append(f"{op} cue {c!r} out of range")
            if op == "NOT" and c is None:
                I.has_null_not = True
            if op == "DIST":
                I.n_dist_nodes += 1
            if isinstance(c, int) and not isinstance(c, bool):
                I.refs[c].append((op, id(node), under_core, opt))
            if "child" not in node:
                I.errors.append(f"{op} without child")
                return
            rec(node["child"], anc + [node], under_core, opt)
            return
        if op == "CORE":
            if under_core:
                I.errors.append("CORE inside CORE")
            I.cores.append((node, list(anc), opt))
            if "child" not in node:
                I.errors.append("CORE without child")
                return
            rec(node["child"], anc + [node], True, opt)
            return
        ch = node.get("children")
        if not isinstance(ch, list) or not ch:
            I.errors.append(f"{op} without children")
            return
        if op in ("ATLEAST", "ATMOST", "EXACTLY"):
            k = node.get("k")
            if not isinstance(k, int) or isinstance(k, bool) or k < 0:
                I.errors.append(f"{op} k is not a non-negative int")
        for c in ch:
            rec(c, anc + [node], under_core, opt)

    if lf.get("op") == "CHOICE":
        if not is_choice:
            I.errors.append("CHOICE lf on a yes/no row")
        opts = lf.get("options")
        if not isinstance(opts, list) or len(opts) < 2:
            I.errors.append("CHOICE without >= 2 option lfs")
            return I
        if lf.get("select") not in ("true", "false"):
            I.errors.append("CHOICE select is not 'true' / 'false'")
            return I
        c = lf.get("cue")
        if c is not None:
            if not isinstance(c, int) or isinstance(c, bool) or not 0 <= c < n_cues:
                I.errors.append("CHOICE cue out of range")
            else:
                I.refs[c].append(("CHOICE", id(lf), False, None))
        elif lf["select"] == "false":
            I.errors.append("negated selection without a CHOICE cue")
        I.choice = lf
        for i, o in enumerate(opts):
            rec(o, [], False, i)
        per_opt = Counter(o for _, _, o in I.cores)
        if any(per_opt.get(i, 0) != 1 for i in range(len(opts))):
            I.errors.append("every option lf needs exactly one CORE")
    else:
        if is_choice:
            I.errors.append("choice row without a CHOICE lf")
        rec(lf, [], False, None)
        if len(I.cores) != 1:
            I.errors.append(f"{len(I.cores)} CORE nodes (exactly one)")
    if I.errors:
        return I
    for node, anc, _ in I.cores:
        for a in anc:
            if a["op"] == "NOT":
                path_nots.add(id(a))
    for c, lst in I.refs.items():
        if len(lst) > 1:
            I.errors.append(f"cue {c} referenced by {len(lst)} nodes")
        for op, nid, under_core, _ in lst:
            if op == "NOT" and under_core:
                I.errors.append(f"cue {c}: a NOT with a cue inside CORE (the core claim must be cue-free)")
    # refine NOT refs into path / off-path
    for c, lst in list(I.refs.items()):
        I.refs[c] = [("NOT_path" if (op == "NOT" and nid in path_nots) else ("NOT_off" if op == "NOT" else op),
                      nid, uc, o) for op, nid, uc, o in lst]
    try:
        if I.choice is not None:
            idx = choice_gold(I.choice)
            if len(idx) != 1:
                I.errors.append(f"{len(idx)} options evaluate to select (exactly one)")
                return I
            I.gold = idx[0]
            core, anc, _ = [x for x in I.cores if x[2] == I.gold][0]
            I.depth = sum(1 for a in anc if a["op"] == "NOT") + (1 if I.choice["select"] == "false" else 0)
            I.truth_P = lf_eval(core["child"])
            I.core_sig = json.dumps(core["child"], sort_keys=True)
            I.gold_options = idx
        else:
            core, anc, _ = I.cores[0]
            I.gold = int(lf_eval(lf))
            I.depth = sum(1 for a in anc if a["op"] == "NOT")
            I.truth_P = lf_eval(core["child"])
            I.core_sig = json.dumps(core["child"], sort_keys=True)
    except (KeyError, TypeError, ValueError) as e:
        I.errors.append(f"evaluation error {e!r}")
    return I


def lf_replace(node, pred, how):
    """A copy of the tree where every node with pred(node) is replaced: how='child' (deleted) or 'not' (made a NOT)."""
    if not isinstance(node, dict):
        return node
    if pred(node):
        if how == "child":
            return lf_replace(node["child"], pred, how)
        return {"op": "NOT", "cue": node.get("cue"), "child": lf_replace(node["child"], pred, how)}
    out = dict(node)
    if "child" in node:
        out["child"] = lf_replace(node["child"], pred, how)
    if "children" in node:
        out["children"] = [lf_replace(c, pred, how) for c in node["children"]]
    if "options" in node:
        out["options"] = [lf_replace(c, pred, how) for c in node["options"]]
    return out


def lf_value(lf, full=False):
    return choice_gold(lf, full) if lf.get("op") == "CHOICE" else int(lf_eval(lf, full))


def lf_has(lf, ops):
    if not isinstance(lf, dict):
        return False
    if lf.get("op") in ops:
        return True
    return any(lf_has(c, ops) for c in ([lf.get("child")] if "child" in lf else []) + list(lf.get("children") or [])
               + list(lf.get("options") or []))


def lf_set_conn(lf, min_children):
    """True when the tree holds an AND / OR node with >= min_children children (a quantifier over a set, written out)."""
    if not isinstance(lf, dict):
        return False
    if lf.get("op") in ("AND", "OR") and len(lf.get("children") or []) >= min_children:
        return True
    return any(lf_set_conn(c, min_children) for c in ([lf.get("child")] if "child" in lf else [])
               + list(lf.get("children") or []) + list(lf.get("options") or []))


# ===================================================================================================== result records
@dataclass
class Sub:
    id: str
    name: str
    status: str
    value: object = None
    target: object = None
    cite: str = ""
    detail: object = None


@dataclass
class Opts:
    budget: str = "full"
    fast: bool = False
    decide2_preds: dict | None = None
    decide2_code: list = field(default_factory=list)
    decide2_independent: str = "unknown"
    generator_code: list = field(default_factory=list)
    blind: list | None = None
    holdout_spec: dict | None = None
    lexicon: dict | None = None
    golden_train: str = "data/v14_parts/golden_train.jsonl"
    neg_manifest: str = "yn2b/decontam_only/negation_benchmarks.json"
    ohs3_blind: bool = False
    train_path: str | None = None
    unseen: bool = True
    seed: int = 20261001


class Ctx:
    """All rows of all parts with their sidecar meta and this tool's own analysis."""

    def __init__(self, parts: dict, metas: list, rels: dict, opts: Opts | None = None, log=print):
        self.opts = opts or Opts()
        self.log = log
        self.parts = {k: list(v) for k, v in parts.items()}
        self.rels = {k: list(v) for k, v in rels.items()}
        self.meta_list = list(metas)
        self.R = []
        for part, rows in self.parts.items():
            for r in rows:
                self.R.append({"row": r, "m": None, "part": part, "an": None})
        by_id = defaultdict(list)
        for m in self.meta_list:
            if isinstance(m, dict):
                by_id[m.get("id")].append(m)
        self.meta_by_id = by_id
        for R in self.R:
            ms = by_id.get(R["row"].get("id"))
            if ms and len(ms) == 1:
                R["m"] = ms[0]
        self._analyse()

    # ------------------------------------------------------------------ analysis
    def _analyse(self):
        for R in self.R:
            R["an"] = analyse_row(R)
        yn_train = sorted(len(R["row"].get("instructions") or "") for R in self.R
                          if R["an"]["ok"] and R["an"]["dev_kind"] == "train")
        if not yn_train:
            yn_train = sorted(len(R["row"].get("instructions") or "") for R in self.R) or [0]
        self.len_edges = [yn_train[int(len(yn_train) * q)] for q in (0.2, 0.4, 0.6, 0.8)] if len(yn_train) >= 5 else []
        for R in self.R:
            R["an"]["len_bin"] = bisect.bisect_right(self.len_edges, len(R["row"].get("instructions") or ""))
        self.ok = [R for R in self.R if R["an"]["ok"]]
        self.train = [R for R in self.ok if R["an"]["dev_kind"] == "train"]
        self.iid = [R for R in self.ok if R["an"]["dev_kind"] == "iid"]
        self.hold = [R for R in self.ok if R["an"]["dev_kind"] == "holdout"]
        self.devx = [R for R in self.ok if R["an"]["dev_kind"] == "devx"]
        self.dev = self.iid + self.hold
        self.ladders = defaultdict(list)
        for R in self.ok:
            self.ladders[R["m"]["ladder_id"]].append(R)
        self.by_rowid = {R["row"].get("id"): R for R in self.R}
        # surface lexicon (cue words of train rows; used only by the surface probes and the clause counter)
        self.lex_res = {}
        forms = set()
        for R in self.train:
            for c in R["m"]["cues"]:
                if c["cls"] == "lookalike":
                    continue
                for key in [c["lexeme"]] + ([c["surface"]] if isinstance(c.get("surface"), str) else []):
                    k = key.strip().lower()
                    if k and k not in self.lex_res:
                        rx = lexeme_regex(k)
                        if rx is not None:
                            self.lex_res[k] = rx
                            forms |= {f for f in inflections(k) if f not in ("n't", "nt")}
        lex = "|".join(re.escape(f).replace(r"\ ", r"\s+") for f in sorted(forms, key=len, reverse=True))
        self.cue_rx = re.compile((r"(?<![\w-])(?P<lex>" + lex + r")(?![\w-])|" if lex else "") +
                                 r"(?P<aff>\b(?:non-?[a-z]{3,}|un[a-z]{3,}|dis[a-z]{3,}|[a-z]{3,}less|[a-z]{2,}-free)\b)|"
                                 r"(?P<nar>\b(?:not|no|never|none|cannot)\b|n't\b)", re.I)
        self._cc = {}

    def full_cue_count(self, text):
        """Cue tokens in a text: the train lexicon (with inflections), negative-affix words, not/no/never/none/n't."""
        if text in self._cc:
            return self._cc[text]
        n = 0
        for m in self.cue_rx.finditer(mask_quotes(text)):
            if m.group("aff") and m.group("aff").lower() in AFFIX_STOP:
                continue
            n += 1
        if len(self._cc) < 500000:
            self._cc[text] = n
        return n

    def lexemes_in(self, text):
        t = mask_quotes(text)
        return sorted(k for k, rx in self.lex_res.items() if rx.search(t))


def sh8(text):
    return hashlib.blake2b((text or "").encode(), digest_size=8).digest()


def pair_key(r):
    import check_yn2b as cy
    return hashlib.sha1((cy.norm(r.get("state")) + "||" + cy.norm(r.get("instructions"))).encode()).digest()


def golden_scan(ctx):
    """One pass over golden_train (cached on ctx): which F7 states / (state, instruction) pairs it holds, and the
    12-gram hashes of the golden rows whose state an F7 row copies (for the in-family inheritance rule)."""
    if getattr(ctx, "_golden", None) is not None:
        return ctx._golden
    import check_yn2b as cy
    f7_states = {sh8(R["row"].get("state")) for R in ctx.R}
    f7_pairs = {pair_key(R["row"]) for R in ctx.R}
    states, pairs, grams = set(), set(), defaultdict(set)
    t0 = time.time()
    with open(LEAN / ctx.opts.golden_train, encoding="utf-8") as f:
        for line in f:
            g = json.loads(line)
            h = sh8(g.get("state"))
            if h in f7_states:
                states.add(h)
                grams[h] |= set().union(*[cy.row_ghash(t) for t in [g.get("state") or ""] + card_lines(g.get("card"))])
            k = pair_key(g)
            if k in f7_pairs:
                pairs.add(k)
    ctx._golden = {"states": states, "pairs": pairs, "grams": grams}
    ctx.log(f"golden_train pass: {len(states)} F7 states and {len(pairs)} F7 (state, instruction) pairs found "
            f"({time.time() - t0:.0f} s)")
    return ctx._golden


def analyse_row(R):
    row, m = R["row"], R["m"]
    an = {"ok": False, "errors": [], "dev_kind": None, "yn": row.get("qtype") == "noul"}
    if m is None:
        an["errors"].append("no sidecar meta (or a duplicated id)")
        return an
    errs = an["errors"]
    for k, t in REQUIRED.items():
        v = m.get(k)
        if k not in m:
            errs.append(f"missing {k}")
        elif t is int and (not isinstance(v, int) or isinstance(v, bool)):
            errs.append(f"{k} not int")
        elif t is not int and not isinstance(v, t):
            errs.append(f"{k} not {t.__name__}")
    if errs:
        return an
    if m["rung"] not in RUNGS:
        errs.append(f"rung {m['rung']!r}")
    if m["ladder_kind"] not in LADDER_KINDS:
        errs.append(f"ladder_kind {m['ladder_kind']!r}")
    if m["dev_kind"] not in DEV_KINDS:
        errs.append(f"dev_kind {m['dev_kind']!r}")
    if not all(isinstance(p, int) and not isinstance(p, bool) and 1 <= p <= 38 for p in m["phen"]):
        errs.append("phen must be a list of item numbers 1-38")
    for i, c in enumerate(m["cues"]):
        if not isinstance(c, dict):
            errs.append(f"cue {i} not an object")
            continue
        for k, t in CUE_REQUIRED.items():
            if k not in c or not isinstance(c[k], t):
                errs.append(f"cue {i} {k} missing or not {t.__name__}")
        if c.get("cls") not in CLASSES:
            errs.append(f"cue {i} cls {c.get('cls')!r}")
        if c.get("position") not in POSITIONS:
            errs.append(f"cue {i} position {c.get('position')!r}")
        if c.get("distance") not in DISTANCES:
            errs.append(f"cue {i} distance {c.get('distance')!r}")
        if isinstance(c.get("lexeme"), str) and not c["lexeme"].strip():
            errs.append(f"cue {i} empty lexeme")
    if 21 in (m.get("phen") or []) and m.get("antonym_gold") not in (0, 1, True, False):
        errs.append("item-21 row without antonym_gold (needed for C7)")
    if errs:
        return an
    an["dev_kind"] = m["dev_kind"]
    I = lf_analyse(m["lf"], len(m["cues"]), not an["yn"])
    an["lf_errors"] = list(I.errors)
    if I.errors:
        errs.extend(f"lf: {e}" for e in I.errors)
        return an
    cues = m["cues"]
    # cue <-> LF consistency
    n_dist = 0
    for i, c in enumerate(cues):
        refs = I.refs.get(i, [])
        kinds = [k for k, _, _, _ in refs]
        if not refs:
            if c["cls"] == "lookalike":
                if c["scoping"]:
                    errs.append(f"cue {i}: a look-alike cannot scope")
            elif c["position"] == "state":
                if c["scoping"]:
                    errs.append(f"cue {i}: a state cue cannot scope (CL:255)")
                n_dist += 1
            else:
                errs.append(f"cue {i} ({c['lexeme']}) is not in the lf")
            continue
        k = kinds[0]
        if c["cls"] == "lookalike":
            errs.append(f"cue {i}: a look-alike is referenced by a {k} node")
        if k in ("NOT_path", "CHOICE") and not c["scoping"]:
            errs.append(f"cue {i} ({c['lexeme']}) scopes over P in the lf but scoping=false")
        if k in ("NOT_off", "DIST") and c["scoping"]:
            errs.append(f"cue {i} ({c['lexeme']}) does not scope over P in the lf but scoping=true")
        if k == "DIST":
            n_dist += 1
    if m["n_cues"] != len(cues):
        errs.append(f"n_cues {m['n_cues']} != {len(cues)} cues")
    if m["n_distractor"] != n_dist:
        errs.append(f"n_distractor {m['n_distractor']} != {n_dist} (DIST nodes + state cues)")
    if m["depth"] != I.depth:
        errs.append(f"depth {m['depth']} != {I.depth} NOT nodes on the root->CORE path")
    if m["truth_P"] != I.truth_P:
        errs.append(f"truth_P {m['truth_P']} != eval(CORE) {I.truth_P}")
    row_gold = row.get("gold")
    if an["yn"]:
        if m["gold"] != row_gold:
            errs.append(f"sidecar gold {m['gold']} != row gold {row_gold}")
    else:
        opts = row.get("options") or []
        if not (0 <= m["gold"] < len(opts)) or opts[m["gold"]] != row_gold:
            errs.append("sidecar gold index does not point at the row's gold option")
        if len(I.choice["options"]) != len(opts):
            errs.append("CHOICE option lfs != row options")
    an["lf_gold"] = I.gold
    an["depth"] = I.depth
    an["truth_P"] = I.truth_P
    an["core_sig"] = I.core_sig
    an["null_not"] = I.has_null_not
    an["n_all"] = len(cues)
    an["n_dist"] = n_dist
    an["scoping"] = [c for c in cues if c["scoping"]]
    an["dist_cues"] = [c for i, c in enumerate(cues)
                       if (I.refs.get(i) and I.refs[i][0][0] == "DIST") or (not I.refs.get(i) and c["cls"] != "lookalike")]
    an["refs"] = {i: [k for k, _, _, _ in v] for i, v in I.refs.items()}
    an["ops"] = dict(I.ops)
    an["state_neg"] = bool(STATE_NEG_RE.search(row.get("state") or ""))
    an["state_format"] = state_format(row.get("state"))
    an["carrier"] = m.get("carrier_id") or carrier(row.get("instructions") or "")
    an["qlabel"] = quoted_label(row, m)
    an["has_yn"] = {ln.split(":")[0].strip(" -").lower() for ln in yn_lines(row.get("card"))} >= {"yes", "no"}
    an["select_false"] = (not an["yn"]) and m["lf"].get("select") == "false"
    an["gold_v"] = row_gold if an["yn"] else m["gold"]
    an["ok"] = not errs
    return an


# ===================================================================================================== small helpers
def count_share(rows, pred):
    n = len(rows)
    k = sum(1 for R in rows if pred(R))
    return k, n, (k / n if n else None)


def yes_rows(rows):
    return [R for R in rows if R["an"]["yn"]]


def gold_yes(R):
    return R["an"]["yn"] and R["row"]["gold"] == 1


def strata_keys(R):
    m, an = R["m"], R["an"]
    ks = [("depth", an["depth"]), ("parity", an["depth"] % 2), ("n_cues", an["n_all"]),
          ("ladder_kind", m["ladder_kind"]), ("frame_family", m["frame_family"]), ("frame_id", m["frame_id"]),
          ("source", m["source"]), ("card_style", m["card_style"]), ("len_bin", an["len_bin"]),
          ("state_neg", an["state_neg"]), ("state_format", an["state_format"]), ("template", an["carrier"]),
          ("n_distractor", an["n_dist"])]
    if an["qlabel"]:
        ks.append(("quoted_label", an["qlabel"]))
    for f in ("tier", "renderer", "pack", "format", "world_fmt"):
        if isinstance(m.get(f), (str, int)) and not isinstance(m.get(f), bool):
            ks.append((f, m[f]))
    seen = set()
    for c in m["cues"]:
        for k in (("cue_class", c["cls"]), ("cue_position", c["position"]), ("cue_lexeme", c["lexeme"].lower()),
                  ("cue_distance", c["distance"])):
            if k not in seen:
                seen.add(k)
                ks.append(k)
    return ks


def status(ok):
    return "PASS" if ok else "FAIL"


# ===================================================================================================== check 1: schema
def check_schema(ctx: Ctx):
    out = []
    ids = Counter(R["row"].get("id") for R in ctx.R)
    dup = [i for i, n in ids.items() if n > 1]
    meta_ids = Counter(m.get("id") if isinstance(m, dict) else None for m in ctx.meta_list)
    orphans = [i for i in meta_ids if i not in ids]
    dup_meta = [i for i, n in meta_ids.items() if n > 1]
    no_meta = [R["row"].get("id") for R in ctx.R if R["m"] is None]
    ok = not dup and not orphans and not dup_meta and not no_meta
    out.append(Sub("1.1", "sidecar <-> rows join by id (no missing, orphan or duplicate id)", status(ok),
                   {"rows": len(ctx.R), "sidecar": len(ctx.meta_list), "rows_without_meta": len(no_meta),
                    "orphan_meta": len(orphans), "duplicate_row_ids": len(dup), "duplicate_meta_ids": len(dup_meta)},
                   "all 0", "CL:385-392", {"examples": (no_meta + orphans + dup + dup_meta)[:8]}))
    field_errs = Counter()
    lf_errs, cons_errs = Counter(), Counter()
    ex = defaultdict(list)
    for R in ctx.R:
        if R["m"] is None:
            continue
        for e in R["an"]["errors"]:
            if e.startswith("lf: "):
                key, bucket = e[4:].split(" ")[0], lf_errs
            elif any(s in e for s in ("!=", "scop", "not in the lf", "referenced", "look-alike", "state cue")):
                key, bucket = re.sub(r"\d+", "#", e.split(":")[0] if ":" in e else e)[:60], cons_errs
            else:
                key, bucket = re.sub(r"\d+", "#", e)[:60], field_errs
            bucket[key] += 1
            if len(ex[id(bucket)]) < 6:
                ex[id(bucket)].append((R["row"].get("id"), e))
    out.append(Sub("1.2", "required fields, types and enums (+ antonym_gold on item-21 rows)", status(not field_errs),
                   sum(field_errs.values()), 0, "CL:385-392", {"by_error": dict(field_errs.most_common(12)),
                                                                "examples": ex[id(field_errs)]}))
    out.append(Sub("1.3", "LF well-formed (ops, one CORE, cue indices, no cue inside CORE, choice options)",
                   status(not lf_errs), sum(lf_errs.values()), 0, "task LF contract",
                   {"by_error": dict(lf_errs.most_common(12)), "examples": ex[id(lf_errs)]}))
    out.append(Sub("1.4", "cue <-> LF consistency (scoping flags, n_cues, n_distractor, depth, truth_P, gold field)",
                   status(not cons_errs), sum(cons_errs.values()), 0, "CL:200-201, CL:386-388",
                   {"by_error": dict(cons_errs.most_common(12)), "examples": ex[id(cons_errs)]}))
    bad_kind = [R["row"].get("id") for R in ctx.R if R["m"] is not None and isinstance(R["m"].get("dev_kind"), str)
                and R["m"]["dev_kind"] not in PART_KINDS.get(R["part"], ())]
    out.append(Sub("1.5", "dev_kind matches the file (train / probe: iid|holdout / devx)", status(not bad_kind),
                   len(bad_kind), 0, "CL:390", {"examples": bad_kind[:6]}))
    fmt = []
    for R in ctx.R:
        r = R["row"]
        p = []
        for k in ("id", "group_id", "call_id", "split", "track", "source", "state", "qtype", "instructions"):
            if not isinstance(r.get(k), str):
                p.append(f"{k} missing")
        if r.get("qtype") == "noul":
            if r.get("options") is not None or r.get("gold") not in (0, 1) or isinstance(r.get("gold"), bool):
                p.append("noul row needs options null and gold 0/1")
        elif r.get("qtype") == "choice":
            o = r.get("options")
            if not isinstance(o, list) or len(set(o)) != len(o) or r.get("gold") not in o:
                p.append("choice row needs unique options and gold among them")
            elif any(not isinstance(x, str) or len(x) > 200 or "\n" in x for x in o):
                p.append("options must be single lines <= 200 chars (SPEC 4.3)")
        else:
            p.append(f"qtype {r.get('qtype')!r}")
        if r.get("card") is not None and not isinstance(r.get("card"), str):
            p.append("card not a string")
        if isinstance(r.get("meta"), dict) and "teacher" in r["meta"]:
            p.append("meta.teacher on a program-labelled row")
        if p:
            fmt.append((r.get("id"), p))
    out.append(Sub("1.6", "row format (SPEC 4.5: qtype / options / gold / card; no meta.teacher)", status(not fmt),
                   len(fmt), 0, "SPEC 4.5", {"examples": fmt[:6]}))
    try:
        import train_decoder as td
        bad = []
        for part, rows in ctx.parts.items():
            try:
                td.check_rows(rows)
            except ValueError as e:
                bad.append(f"{part}: {str(e)[:300]}")
        out.append(Sub("1.7", "train_decoder.check_rows on every file", status(not bad), len(bad), 0,
                       "task: train rows must pass check_rows", bad[:3]))
    except Exception as e:  # noqa: BLE001
        out.append(Sub("1.7", "train_decoder.check_rows on every file", "FAIL", None, 0, "", f"import failed: {e!r}"))
    return out


# ===================================================================================================== check 2: gold
def check_gold(ctx: Ctx):
    out = []
    rows = ctx.ok
    bad = [R["row"]["id"] for R in rows if R["an"]["lf_gold"] != R["an"]["gold_v"]]
    out.append(Sub("2.1", "own LF evaluator: eval(lf) == gold", status(not bad and bool(rows)),
                   f"{len(rows) - len(bad)}/{len(rows)}", "100%", "CL:393-394", {"examples": bad[:8]}))
    del_bad, n_tests, potent, n_dist_nodes = [], 0, 0, 0
    for R in rows:
        lf = R["m"]["lf"]
        # the declared distractors: cues of DIST nodes (and unreferenced state cues). Off-path NOT cues (an exception
        # clause, item 23) are non-scoping but not distractors: they may change the gold, so they are not tested here.
        dist_idx = {i for i, c in enumerate(R["m"]["cues"]) if c["cls"] != "lookalike" and not c["scoping"]
                    and R["an"]["refs"].get(i, ["DIST"])[0] == "DIST"}
        if not dist_idx:
            continue
        try:
            base = lf_value(lf, full=True)
        except Undefined as e:
            base = f"undefined ({e})"
        for i in sorted(dist_idx):
            n_tests += 1
            pred = (lambda node, _i=i: node.get("op") == "DIST" and node.get("cue") == _i)
            try:
                after = lf_value(lf_replace(lf, pred, "child"), full=True)
            except Undefined as e:
                after = f"undefined ({e})"
            if after != base or isinstance(base, str):
                del_bad.append((R["row"]["id"], i, R["m"]["cues"][i]["lexeme"], str(base)[:60]))
            if R["an"]["refs"].get(i, [None])[0] == "DIST":
                n_dist_nodes += 1
                try:
                    if lf_value(lf_replace(lf, pred, "not")) != lf_value(lf):
                        potent += 1
                except Undefined:
                    pass
    out.append(Sub("2.2", "distractor-deletion test (each DIST node deleted, re-evaluated with the distractor's own "
                          "semantics: gold unchanged and defined)", status(not del_bad),
                   f"{n_tests - len(del_bad)}/{n_tests}", "100%", "CL:234-236, CL:395",
                   {"examples": del_bad[:8], "info_distractors_that_would_flip_gold_if_read_as_negation":
                    f"{potent}/{n_dist_nodes}"}))
    preds = ctx.opts.decide2_preds
    if preds is None:
        out.append(Sub("2.3", "independent decide2 parse-back agreement", "PENDING", None, "100% (bug if > 1% off)",
                       "CL:202-204, CL:396", "no --decide2-preds given"))
    else:
        dis, miss = [], 0
        for R in ctx.R:
            rid = R["row"].get("id")
            if rid not in preds:
                miss += 1
                continue
            want = R["row"].get("gold")
            if preds[rid] != want:
                dis.append((rid, want, preds[rid]))
        n = len(ctx.R)
        share = (len(dis) + miss) / n if n else 0
        out.append(Sub("2.3", "independent decide2 parse-back agreement", status(not dis and not miss),
                       {"agree": n - len(dis) - miss, "rows": n, "disagree": len(dis), "unparsed": miss,
                        "generator_bug": share > DECIDE2_BUG_SHARE}, "100% (bug if > 1% off)", "CL:202-204, CL:396",
                       {"examples": dis[:10]}))
    out.append(decide2_independence(ctx))
    need, miss_line = 0, []
    for R in rows:
        txt = " ".join(authored_texts(R["row"])[:1] + [o for o in (R["row"].get("options") or [])])
        if BIVALENCE_CUE_RE.search(mask_quotes(txt)):
            need += 1
            if not BIVALENCE_LINE_RE.search(R["row"].get("card") or ""):
                miss_line.append(R["row"]["id"])
    out.append(Sub("2.4", "bivalence stated: rows with refute / unsupported / fails-to-show frames have a 'settles' card line",
                   status(not miss_line), f"{need - len(miss_line)}/{need}", "100%", "CL:280-281",
                   {"examples": miss_line[:8]}))
    presup, ndist = [], 0
    for R in rows:
        if not any(c["position"] != "state" for c in R["an"]["dist_cues"]):
            continue
        ndist += 1
        q = R["row"].get("instructions") or ""
        if (PRESUPPOSING_RE.search(q) and not NONPRESUP_RE.search(q)) or \
                '"mode": "presupposed"' in json.dumps(R["m"]["lf"]):
            presup.append(R["row"]["id"])
    out.append(Sub("2.5", "distractor clauses never presuppose a fact (whether or not / even if / format lines only)",
                   status(not presup), len(presup), 0, "CL:237-238", {"rows_with_distractor": ndist,
                                                                    "examples": presup[:8]}))
    ch = [R for R in rows if not R["an"]["yn"]]
    bad = [R["row"]["id"] for R in ch if R["an"]["lf_gold"] != R["m"]["gold"]]
    out.append(Sub("2.6", "choice rows: exactly one option lf evaluates to select, and it is the gold option",
                   status(not bad), f"{len(ch) - len(bad)}/{len(ch)}", "100%", "task LF contract",
                   {"examples": bad[:6]}))
    return out


def decide2_independence(ctx):
    o = ctx.opts
    if o.decide2_preds is None:
        return Sub("2.3b", "decide2 independence (separate author; no generator import)", "PENDING", None,
                   "independent author, no generator import", "CL:202, SPEC 8.1", "no decide2 given")
    imp = []
    gen_names = {Path(p).stem for p in o.generator_code}
    for p in o.decide2_code:
        try:
            tree = ast.parse(Path(p).read_text())
        except (OSError, SyntaxError) as e:
            imp.append(f"{p}: unreadable ({e})")
            continue
        for node in ast.walk(tree):
            mods = []
            if isinstance(node, ast.Import):
                mods = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                mods = [node.module or ""]
            for mname in mods:
                if mname.split(".")[-1] in gen_names:
                    imp.append(f"{Path(p).name} imports {mname}")
    if imp:
        return Sub("2.3b", "decide2 independence (separate author; no generator import)", "FAIL", imp, "none",
                   "CL:202, SPEC 8.1")
    if o.decide2_independent == "no":
        return Sub("2.3b", "decide2 independence (separate author; no generator import)", "FAIL", "same author",
                   "independent author", "CL:202, SPEC 8.1", "declared --decide2-independent no")
    if o.decide2_independent != "yes":
        return Sub("2.3b", "decide2 independence (separate author; no generator import)", "PENDING", "unknown",
                   "independent author", "CL:202, SPEC 8.1", "authorship not declared (--decide2-independent)")
    return Sub("2.3b", "decide2 independence (separate author; no generator import)", "PASS", "declared independent",
               "independent author", "CL:202, SPEC 8.1", {"code_scanned": o.decide2_code})


# ===================================================================================================== check 3: coverage
def tag_rule(item, R):
    """True / False when the item's structure can be read from the sidecar, None when it cannot."""
    m, an = R["m"], R["an"]
    d = an["depth"]
    sc = [c for c in an["scoping"]]
    neg = [c for c in m["cues"] if c["cls"] != "lookalike"]
    cls = [c["cls"] for c in sc]
    pos = {c["position"] for c in sc}
    if item in CARD_ITEMS and m["ladder_kind"] != "card":
        return False
    if item in MULTITEXT_ITEMS and m["ladder_kind"] != "multitext":
        return False
    if item == 1:   # 'the question has no negation' (card-line / state distractors may exist)
        return d == 0 and not any(c["position"] in QUESTION_POSITIONS for c in neg)
    if item == 2:
        return d == 1 and any(c["cls"] == "syntactic" and c["position"] == "inner_claim" for c in sc)
    if item == 3:
        return d == 1 and "truth_frame" in cls
    if item == 4:
        return d == 1 and bool(sc) and all(c == "lexical" for c in cls)
    if item == 5:
        return d == 1 and "affixal" in cls
    if item == 6:
        return d == 2 and len(sc) == 2 and len(set(cls)) == 2
    if item == 7:
        return d == 2 and len(sc) == 2 and len(set(cls)) == 1
    if item == 8:
        return d == 3 and len(set(cls)) >= 2
    if item == 9:
        return d == 4
    if item == 10:
        return d >= 2 and any(c["position"] == "outer_frame" and c["cls"] in ("lexical", "truth_frame") for c in sc) \
            and any(c["position"] != "outer_frame" for c in sc)
    if item == 11:
        return bool(pos & {"card_def", "yn_key"}) and bool(pos & {"outer_frame", "inner_claim", "separate_sentence",
                                                                     "answer_map", "choice_option"})
    if item == 12:
        return any(c["distance"] in ("next_sentence", "far", "other_field") for c in sc)
    if item == 13:
        return "answer_map" in pos
    if item == 14:
        return "yn_key" in pos
    if item == 15:
        return an["n_dist"] >= 1
    if item == 16:
        return d >= 1 and an["n_dist"] >= 1
    if item == 17:
        return d == 0 and an["n_dist"] >= 2
    if item == 18:
        return any(c["position"] == "card_def" for c in an["dist_cues"])
    if item == 19:
        return an["state_neg"]
    if item == 20:
        return any(c["cls"] == "lookalike" for c in m["cues"])
    if item == 26:
        # ARBITER fix (F7_OBJECTIONS.md O2, 3.3): 'none / not all / not a single' over a batch is equally well
        # written as AND / OR over the member atoms (none = NOT(OR), not all = NOT(AND)); accept that set form when it
        # spans >= 3 members (a multi-text batch holds 3-5 texts, CL:226), as rule 27 already accepts AND / OR.
        return lf_has(m["lf"], ("ATLEAST", "ATMOST", "EXACTLY")) or lf_set_conn(m["lf"], 3)
    if item in (28, 29):
        return lf_has(m["lf"], ("ATLEAST", "ATMOST", "EXACTLY"))
    if item == 27:
        return lf_has(m["lf"], ("ATLEAST", "ATMOST", "EXACTLY", "AND", "OR")) and "outer_frame" in pos
    if item == 30:
        return lf_has(m["lf"], ("AND", "OR"))
    if item == 36:
        return (not an["yn"]) and an["select_false"]
    if item == 37:
        return not an["yn"]
    if item == 38:
        return d >= 1 and "inner_claim" in pos and an["has_yn"]
    return None


def check_coverage(ctx: Ctx):
    out = []
    fl = FLOORS[ctx.opts.budget]
    cnt = {k: Counter() for k in ("train", "dev", "hold")}
    d0_skipped = Counter()

    def counted(R):
        out = set()
        for p in set(R["m"]["phen"]):
            if p in DEPTH1_ITEMS and R["an"]["depth"] < 1:
                d0_skipped[p] += 1
                continue
            out.add(p)
        return out
    for R in ctx.train:
        for p in counted(R):
            cnt["train"][p] += 1
    for R in ctx.dev:
        for p in counted(R):
            cnt["dev"][p] += 1
            if R["an"]["dev_kind"] == "holdout":
                cnt["hold"][p] += 1
    table, below = {}, []
    for it in range(1, 39):
        pr = PRIORITY[it]
        f = fl[pr]
        got = (cnt["train"][it], cnt["dev"][it], cnt["hold"][it])
        okk = got[0] >= f[0] and got[1] >= f[1] and got[2] >= f[2]
        table[it] = {"priority": pr, "train": got[0], "dev": got[1], "holdout": got[2], "floor": list(f), "ok": okk,
                     "cite": f"CL:{ITEM_LINE[it]}"}
        if not okk:
            below.append(it)
    out.append(Sub("3.1", f"checklist items 1-38 at their floors (train/dev/holdout, budget={ctx.opts.budget}; items "
                          f"{'/'.join(map(str, DEPTH1_ITEMS))} count only rows with a scoping negation)",
                   status(not below), f"{38 - len(below)}/38 items", "all items", "CL:302-308, CL:136, CL:141",
                   {"below_floor": below, "table": table,
                    "depth0_rows_not_counted": {str(k): v for k, v in sorted(d0_skipped.items())}}))
    caps, shares = [], {}
    for it, (cap, line) in ITEM_CAP.items():
        # every cap binds train AND dev (the probe, iid + holdout): CL:61 / 80 / 172 say 'at most x% of rows'; item 9
        # also needs >= 40 dev rows at depth 4 (CL:374), so the dev keeps 40 <= depth-4 rows <= 3% (r6 trims the
        # probe). The blind devx (written by another agent, frozen) is reported, never trimmed.
        for name, rows in (("train", ctx.train), ("dev", ctx.dev), ("devx_report_only", ctx.devx)):
            k = sum(1 for R in rows if it in R["m"]["phen"])
            n = len(rows)
            shares[f"{it}|{name}"] = [k, n, r3(k / n) if n else None]
            if name != "devx_report_only" and n and k / n > cap + 1e-12:
                caps.append({"item": it, "set": name, "share": r3(k / n), "cap": cap, "cite": f"CL:{line}"})
    out.append(Sub("3.2", "item caps (9 <= 3%, 14 <= 10%, 38 <= 5% of train rows and of dev rows; devx reported)",
                   status(not caps), caps or "ok", "within caps", "CL:61, CL:80, CL:172, CL:374",
                   {"rows_share": shares}))
    mism = Counter()
    ex = defaultdict(list)
    for R in ctx.ok:
        for it in set(R["m"]["phen"]):
            v = tag_rule(it, R)
            if v is False:
                mism[it] += 1
                if len(ex[it]) < 3:
                    ex[it].append(R["row"]["id"])
    out.append(Sub("3.3", "tag consistency: every phen tag matches the row's LF / cues / ladder kind", status(not mism),
                   sum(mism.values()), 0, "CL:385-392 (tool rule per item)",
                   {"mismatch_by_item": dict(sorted(mism.items())), "examples": dict(ex)}))
    cells = Counter()
    for R in ctx.train:
        d = R["an"]["depth"]
        for (p, c) in {(c["position"], c["cls"]) for c in R["an"]["scoping"]}:
            cells[(d, p, c)] += 1
    missing = []
    for d in (1, 2, 3):
        for p, cl in ALLOWED_CELLS.items():
            for c in cl:
                if cells[(d, p, c)] < CELL_MIN_ROWS:
                    missing.append(f"d{d}|{p}|{c}={cells[(d, p, c)]}")
    n_cells = 3 * sum(len(v) for v in ALLOWED_CELLS.values())
    out.append(Sub("3.4", f"depth x cue position x cue class cells (depth 1-3) with >= {CELL_MIN_ROWS} train rows",
                   status(not missing), f"{n_cells - len(missing)}/{n_cells}", f">= {CELL_MIN_ROWS} each",
                   "CL:398-400", {"below": missing, "all_cells": {f"d{d}|{p}|{c}": n for (d, p, c), n in
                                                                  sorted(cells.items())}}))
    lex_rows, lex_cls = Counter(), {}
    for R in ctx.train:
        for lx_, cl in {(c["lexeme"].lower(), c["cls"]) for c in R["m"]["cues"] if c["cls"] != "lookalike"}:
            lex_rows[lx_] += 1
            lex_cls[lx_] = CLASS5[cl]
    classes = Counter(lex_cls.values())
    thin = {k: v for k, v in lex_rows.items() if v < LEXEME_MIN_ROWS}
    ok = len(lex_rows) >= TRAIN_LEXEMES_MIN and len(classes) >= LEXICON_CLASSES and not thin
    out.append(Sub("3.5", f"lexicon: >= {TRAIN_LEXEMES_MIN} train lexemes over 5 classes, each in >= {LEXEME_MIN_ROWS} rows",
                   status(ok), {"lexemes": len(lex_rows), "classes": dict(classes), "lexemes_below_30_rows": len(thin)},
                   f">= {TRAIN_LEXEMES_MIN}, 5 classes, 0 thin", "CL:258-261, CL:349, CL:368",
                   {"thin": dict(sorted(thin.items())[:40]), "rows_per_lexeme": dict(lex_rows.most_common())}))
    if ctx.opts.lexicon:
        lexd = {k.lower(): v for k, v in (ctx.opts.lexicon.get("lexemes") or {}).items()}
        # ARBITER fix (F7_OBJECTIONS.md O2, 3.5b): CL:261 binds the GENERATOR ('the generator draws cues only from this
        # file'). devx is hand-written blind by another agent who must not read the generator's lexicon (CL:274), so
        # its cue words are out of scope here; train and probe (generator rows) are checked as before.
        gen_rows = ctx.train + ctx.dev
        off = Counter(c["lexeme"].lower() for R in gen_rows for c in R["m"]["cues"]
                      if c["lexeme"].lower() not in lexd or (lexd[c["lexeme"].lower()].get("cls") not in (None, c["cls"])))
        out.append(Sub("3.5b", "every cue lexeme of a generator row (train, probe) is drawn from the curated lexicon "
                               "file (with its class)", status(not off),
                       sum(off.values()), 0, "CL:258-261", {"off_lexicon": dict(off.most_common(20)),
                                                            "devx_rows_not_checked": len(ctx.devx)}))
    else:
        out.append(Sub("3.5b", "every cue lexeme is drawn from the curated lexicon file (with its class)", "PENDING",
                       None, "lexicon file", "CL:258-261", "no --lexicon given"))
    fam_frames = defaultdict(set)
    frame_rows = Counter()
    carr = Counter()
    for R in ctx.train:
        fam_frames[R["m"]["frame_family"]].add(R["m"]["frame_id"])
        frame_rows[R["m"]["frame_id"]] += 1
        carr[R["an"]["carrier"]] += 1
    n = len(ctx.train)
    big_fams = [f for f, s in fam_frames.items() if len(s) >= FRAMES_PER_FAMILY_MIN]
    top_frame = frame_rows.most_common(1)[0] if frame_rows else ("-", 0)
    top_carr = carr.most_common(1)[0] if carr else ("-", 0)
    ok = (len(big_fams) >= TRAIN_FAMILIES_MIN and n > 0 and top_frame[1] / n <= FRAME_MAX + 1e-12
          and top_carr[1] / n <= CARRIER_MAX + 1e-12)
    out.append(Sub("3.6", f"frames: >= {TRAIN_FAMILIES_MIN} families x >= {FRAMES_PER_FAMILY_MIN} frames; frame <= 4%, "
                          f"carrier <= 3% of train rows", status(ok),
                   {"families": len(fam_frames), "families_with_4_frames": len(big_fams),
                    "top_frame": [top_frame[0], r3(top_frame[1] / n) if n else None],
                    "top_carrier_share": r3(top_carr[1] / n) if n else None},
                   "12 x 4; <= 0.04; <= 0.03", "CL:263-265, CL:367-370",
                   {"frames_per_family": {f: len(s) for f, s in sorted(fam_frames.items())},
                    "rows_per_frame": dict(frame_rows.most_common(40)), "top_carrier": top_carr[0][:200]}))
    tl = {R["m"]["ladder_id"] for R in ctx.train}
    rows_min = TRAIN_ROWS_RESEARCH_MIN if ctx.opts.budget == "full" else TRAIN_ROWS_AT_MIN
    ok = len(tl) >= TRAIN_LADDERS_MIN and len(ctx.train) >= rows_min
    out.append(Sub("3.7", f"size: >= {TRAIN_LADDERS_MIN} train ladders and >= {rows_min} train rows", status(ok),
                   {"train_ladders": len(tl), "train_rows": len(ctx.train)},
                   {"ladders": TRAIN_LADDERS_MIN, "rows": rows_min, "plan_ladders": PLAN_LADDERS,
                    "research_rows": [TRAIN_ROWS_RESEARCH_MIN, TRAIN_ROWS_RESEARCH_MAX]}, "CL:297-300"))
    dc = Counter(R["an"]["depth"] for R in ctx.train)
    n = len(ctx.train)
    fails = []
    for d, t in DEPTH_MIX.items():
        if not within(dc[d], n, t, DEPTH_MIX_TOL):
            fails.append(d)
    d4 = sum(v for k, v in dc.items() if k >= 4)
    if n and d4 / n > DEPTH4_MAX + 1e-12:
        fails.append("4+")
    odd = sum(v for k, v in dc.items() if k % 2)
    par_ok = share_ok(odd, n, *PARITY_SHARE)
    out.append(Sub("3.8", "depth mix 18/25/30/24/<=3 (+- 2 pts) and parity about 50/50 (train)",
                   status(not fails and par_ok and n > 0),
                   {"shares": {d: r3(dc[d] / n) if n else None for d in sorted(dc)}, "odd_share": r3(odd / n) if n else None},
                   {"mix": DEPTH_MIX, "depth4_max": DEPTH4_MAX, "tol": DEPTH_MIX_TOL, "odd": PARITY_SHARE},
                   "CL:311-317", {"off_target_depths": fails}))
    il = {R["m"]["ladder_id"] for R in ctx.iid}
    hl = {R["m"]["ladder_id"] for R in ctx.hold}
    ddc = Counter(R["an"]["depth"] for R in ctx.dev)
    thin_d = [d for d in range(4) if ddc[d] < DEV_DEPTH_ROWS_MIN] + (["4"] if sum(v for k, v in ddc.items() if k >= 4)
                                                                   < DEV_DEPTH4_MIN else [])
    ok = (len(il) >= DEV_IID_LADDERS_MIN and len(hl) >= DEV_HOLD_LADDERS_MIN and len(ctx.dev) >= DEV_ROWS_MIN
          and not thin_d and len(ctx.devx) >= DEVX_ROWS_MIN)
    out.append(Sub("3.9", "dev size: >= 150 iid + 150 holdout ladders, >= 1,300 rows, >= 200 rows per depth 0-3, "
                          ">= 40 at depth 4, devx >= 100 rows", status(ok),
                   {"iid_ladders": len(il), "holdout_ladders": len(hl), "dev_rows": len(ctx.dev),
                    "dev_rows_by_depth": dict(sorted(ddc.items())), "devx_rows": len(ctx.devx)},
                   {"iid": DEV_IID_LADDERS_MIN, "holdout": DEV_HOLD_LADDERS_MIN, "rows": DEV_ROWS_MIN,
                    "per_depth": DEV_DEPTH_ROWS_MIN, "depth4": DEV_DEPTH4_MIN, "devx": DEVX_ROWS_MIN},
                   "CL:372-376, CL:274", {"thin_depths": thin_d}))
    lk = Counter()
    for lid in tl:
        lk[ctx.ladders[lid][0]["m"]["ladder_kind"]] += 1
    nl = len(tl)
    ok = nl > 0 and lk["card"] / nl >= CARD_LADDER_MIN - 1e-12 and share_ok(lk["multitext"], nl, *MULTITEXT_LADDERS)
    out.append(Sub("3.10", "ladder kinds: card >= 50%, multi-text 10-20%, rest records (train ladders)", status(ok),
                   {k: r3(v / nl) if nl else None for k, v in lk.items()},
                   {"card": f">= {CARD_LADDER_MIN}", "multitext": MULTITEXT_LADDERS}, "CL:220, CL:364-365"))
    dist = Counter()
    for R in ctx.train:
        for dd in {c["distance"] for c in R["an"]["scoping"]}:
            dist[dd] += 1
    thin = {d: dist[d] for d in DISTANCES if dist[d] < DISTANCE_BIN_MIN_ROWS}
    out.append(Sub("3.11", "distance bins: every bin has >= 30 train rows with a scoping cue at that distance",
                   status(not thin), dict(dist), f">= {DISTANCE_BIN_MIN_ROWS} per bin", "CL:71-73, CL:257",
                   {"thin": thin}))
    emb = Counter()
    for R in ctx.train:
        e = R["m"].get("embed_depth")
        if not isinstance(e, int) or isinstance(e, bool):
            e = len(re.findall(r"\b(?:that|whether)\b", mask_quotes(R["row"].get("instructions") or ""), re.I))
        emb[min(3, e)] += 1
    thin = {e: emb[e] for e in range(4) if emb[e] < EMBED_DEPTH_MIN_ROWS}
    out.append(Sub("3.12", "clause-embedding depth 0-3 each in >= 30 train rows (meta embed_depth, else that/whether count)",
                   status(not thin), dict(sorted(emb.items())), f">= {EMBED_DEPTH_MIN_ROWS} per level", "CL:257",
                   {"thin": thin}))
    return out


# ===================================================================================================== check 4: balance
def balance_set(rows, name):
    """yes share per (depth x cue count) cell and rung (48-52), per other stratum (45-55)."""
    yn = yes_rows(rows)
    cell, rung, strat = defaultdict(lambda: [0, 0]), defaultdict(lambda: [0, 0]), defaultdict(lambda: [0, 0])
    for R in yn:
        y = 1 if R["row"]["gold"] == 1 else 0
        k = (R["an"]["depth"], R["an"]["n_all"])
        cell[k][0] += y
        cell[k][1] += 1
        rung[R["m"]["rung"]][0] += y
        rung[R["m"]["rung"]][1] += 1
        for s in strata_keys(R):
            strat[s][0] += y
            strat[s][1] += 1
    bad_cell = {f"d{d}xc{c}": [k, n] for (d, c), (k, n) in cell.items() if not share_ok(k, n, *YES_CELL)}
    bad_rung = {r: [k, n] for r, (k, n) in rung.items() if not share_ok(k, n, *YES_CELL)}
    bad_str = {f"{a}={b}": [k, n] for (a, b), (k, n) in strat.items() if not share_ok(k, n, *YES_STRATUM)}
    return bad_cell, bad_rung, bad_str, len(cell), len(strat), len(yn)


def check_balance(ctx: Ctx):
    out = []
    for name, rows in (("train", ctx.train), ("dev", ctx.dev), ("devx", ctx.devx)):
        bc, br, bs, ncell, nstr, n = balance_set(rows, name)
        sfx = {"train": "a", "dev": "b", "devx": "c"}[name]
        out.append(Sub(f"4.1{sfx}", f"[{name}] yes share 48-52% in every (depth x total cue count) cell and rung",
                       status(not bc and not br and (n > 0 or name == "devx")),
                       {"bad_cells": len(bc), "cells": ncell, "bad_rungs": len(br), "yes_no_rows": n}, "48-52%",
                       "CL:323", {"bad_cells": dict(list(bc.items())[:30]), "bad_rungs": br}))
        top = sorted(bs.items(), key=lambda kv: -kv[1][1])
        out.append(Sub(f"4.2{sfx}", f"[{name}] yes share 45-55% in every other stratum (SPEC 4.6 + cue class / position / "
                                    "lexeme / family / frame / source / label / card style / length / state negation)",
                       status(not bs), {"bad_strata": len(bs), "strata": nstr}, "45-55%", "CL:324, SPEC 4.6",
                       {"worst_by_size": dict(top[:40])}))
    # ARBITER fix (F7_OBJECTIONS.md O1): 'per depth' is measured on yes/no rows only. On a choice row this tool's own
    # lf_analyse defines truth_P = eval(CORE of the gold option) and depth = NOTs on that option's path (+1 for a
    # negated selection), so truth_P == (depth even) on every choice row by definition; with choice rows at 20% +- 3
    # (CL:327) no data could put the all-row share per depth inside 48-52%. 'Per rung' stays over all rows (the CH rung
    # share = the even/odd depth balance of the choice rows), and the choice-row identity is reported.
    bad = {}
    ch_identity_broken = 0
    for name, rows in (("train", ctx.train), ("dev", ctx.dev)):
        for key in ("rung", "depth"):
            c = defaultdict(lambda: [0, 0])
            for R in rows:
                if key == "depth" and not R["an"]["yn"]:
                    if bool(R["an"]["truth_P"]) != (R["an"]["depth"] % 2 == 0):
                        ch_identity_broken += 1
                    continue
                k = R["m"]["rung"] if key == "rung" else R["an"]["depth"]
                c[k][0] += 1 if R["an"]["truth_P"] else 0
                c[k][1] += 1
            for k, (a, n) in c.items():
                if not share_ok(a, n, *TRUTHP_RUNG_DEPTH):
                    bad[f"{name}:{key}={k}"] = [a, n]
    out.append(Sub("4.3", "truth(P) 48-52% per rung (all rows) and per depth (yes/no rows) (train, dev)",
                   status(not bad and not ch_identity_broken), len(bad), "48-52%", "CL:325 (+ F7_OBJECTIONS.md O1)",
                   {**bad, "info_choice_rows_breaking_truthP_eq_depth_even": ch_identity_broken}))
    bad = {}
    for name, rows in (("train", ctx.train), ("dev", ctx.dev)):
        c = defaultdict(lambda: [0, 0])
        for R in rows:
            if R["an"]["qlabel"]:
                c[R["an"]["qlabel"]][0] += 1 if R["an"]["truth_P"] else 0
                c[R["an"]["qlabel"]][1] += 1
        for k, (a, n) in c.items():
            if not share_ok(a, n, *TRUTHP_LABEL):
                bad[f"{name}:{k}"] = [a, n]
    out.append(Sub("4.4", "truth(P) 45-55% per quoted label (train, dev)", status(not bad), len(bad), "45-55%",
                   "CL:326", dict(list(bad.items())[:40])))
    out.append(choice_balance(ctx))
    out.extend(cardless_and_style(ctx))
    rows = ctx.train
    n = len(rows)
    k = sum(1 for R in rows if R["an"]["n_dist"] >= 1)
    per = {}
    for d in range(4):
        rd = [R for R in rows if R["an"]["depth"] == d]
        per[d] = (sum(1 for R in rd if R["an"]["n_dist"] >= 1), len(rd))
    ok = n > 0 and k / n >= DIST_ANY_MIN - 1e-12 and all(nn > 0 and a / nn >= DIST_PER_DEPTH_MIN - 1e-12
                                                         for a, nn in per.values())
    out.append(Sub("4.7", "distractors: >= 35% of rows, >= 25% within each depth 0-3 (train)", status(ok),
                   {"overall": r3(k / n) if n else None, "per_depth": {d: r3(a / nn) if nn else None
                                                                      for d, (a, nn) in per.items()}},
                   {"overall": DIST_ANY_MIN, "per_depth": DIST_PER_DEPTH_MIN}, "CL:239, CL:333"))
    mm = sum(1 for R in rows if (R["an"]["n_all"] % 2) != (R["an"]["depth"] % 2))
    out.append(Sub("4.8", "rows where parity(all cues) != parity(scoping cues) >= 30% (train)",
                   status(n > 0 and mm / n >= PARITY_MISMATCH_MIN - 1e-12), r3(mm / n) if n else None,
                   f">= {PARITY_MISMATCH_MIN}", "CL:334"))
    odd = [R for R in rows if R["an"]["depth"] % 2 == 1]
    arlex = sum(1 for R in odd if R["m"]["rung"] == "AR" or
                (R["an"]["scoping"] and all(c["cls"] == "lexical" for c in R["an"]["scoping"])))
    out.append(Sub("4.9", "AR rows + lexical-only flips >= 15% of odd-parity rows (train)",
                   status(bool(odd) and arlex / len(odd) >= AR_LEXONLY_MIN - 1e-12),
                   r3(arlex / len(odd)) if odd else None, f">= {AR_LEXONLY_MIN}", "CL:335"))
    toks = Counter()
    lex_tok = Counter()
    for R in rows:
        for c in R["m"]["cues"]:
            if c["cls"] == "lookalike":
                continue
            toks[CLASS5[c["cls"]]] += 1
            lex_tok[c["lexeme"].lower()] += 1
    nt = sum(toks.values())
    bad = {k: r3(toks[k] / nt) if nt else None for k, (lo, hi) in CUE_MIX.items()
           if not (nt and share_ok(toks[k], nt, lo, hi))}
    out.append(Sub("4.10", "cue mix by class (share of cue tokens, train)", status(not bad and nt > 0),
                   {k: r3(v / nt) for k, v in toks.items()} if nt else None, CUE_MIX, "CL:337-345", {"off": bad}))
    notnt = lex_tok["not"] + lex_tok["n't"] + lex_tok["nt"]
    top = lex_tok.most_common(1)[0] if lex_tok else ("-", 0)
    ok = nt > 0 and notnt / nt <= NOT_NT_MAX + 1e-12 and top[1] / nt <= LEXEME_MAX + 1e-12
    out.append(Sub("4.11", "'not' + \"n't\" <= 20% of cue tokens; no lexeme > 10%", status(ok),
                   {"not_nt": r3(notnt / nt) if nt else None, "top_lexeme": [top[0], r3(top[1] / nt) if nt else None]},
                   {"not_nt": NOT_NT_MAX, "lexeme": LEXEME_MAX}, "CL:348"))
    par = defaultdict(lambda: [0, 0])
    for R in rows:
        for lx_ in {c["lexeme"].lower() for c in R["m"]["cues"]}:
            par[lx_][0] += R["an"]["depth"] % 2
            par[lx_][1] += 1
    bad = {k: [a, nn] for k, (a, nn) in par.items() if not share_ok(a, nn, *LEXEME_ODD)}
    out.append(Sub("4.12", "every lexeme: share of its rows with odd parity 40-60% (train)", status(not bad),
                   {"bad_lexemes": len(bad), "lexemes": len(par)}, "40-60%", "CL:246, CL:350", bad))
    lexd = {k.lower(): v for k, v in ((ctx.opts.lexicon or {}).get("lexemes") or {}).items()}
    use, dis = Counter(), Counter()
    ever_dist = set()
    for R in ctx.ok:
        for c in R["an"]["dist_cues"]:
            ever_dist.add(c["lexeme"].lower())
    cls_of = {}
    for R in rows:
        for ci, c in enumerate(R["m"]["cues"]):
            if c["cls"] == "lookalike":
                continue
            k = c["lexeme"].lower()
            cls_of[k] = c["cls"]
            use[k] += 1
            if not c["scoping"] and (c["position"] == "state" or R["an"]["refs"].get(ci, ["?"])[0] == "DIST"):
                dis[k] += 1
    # ARBITER fix (F7_OBJECTIONS.md A1): the audited lexicon may ADD distractor capability but may not remove it.
    # This tool's own rule (every syntactic negation, and every lexeme used as a distractor anywhere) can host a
    # non-scoping use ('Even if the ticket doesn't name its writer', '- note: replies need not be formal'), so a
    # can_distract=false flag no longer exempts such a lexeme from CL:351.
    capable = {k for k in use if cls_of.get(k) == "syntactic" or k in ever_dist or lexd.get(k, {}).get("can_distract")}
    bad = {k: [dis[k], use[k]] for k in capable if use[k] and dis[k] / use[k] < DISTRACT_USE_MIN - 1e-12}
    out.append(Sub("4.13", "a lexeme that can serve as a distractor does so in >= 10% of its uses (train)",
                   status(not bad), {"capable": len(capable), "below": len(bad)}, f">= {DISTRACT_USE_MIN}", "CL:351",
                   bad))
    pos = Counter()
    state_scoping = 0
    for R in rows:
        for c in R["an"]["scoping"]:
            p = c["position"]
            if p == "state":
                state_scoping += 1
            pos["yn_key+answer_map" if p in ("yn_key", "answer_map") else p] += 1
    npos = sum(pos.values())
    bad = {k: r3(pos[k] / npos) if npos else None for k, (lo, hi) in POSITION_MIX.items()
           if not (npos and share_ok(pos[k], npos, lo, hi))}
    out.append(Sub("4.14", "scoping cue positions (share of scoping cue tokens, train); no scoping cue in the state",
                   status(not bad and npos > 0 and not state_scoping),
                   {k: r3(v / npos) for k, v in pos.items()} if npos else None, POSITION_MIX, "CL:247-257, CL:353-362",
                   {"off": bad, "scoping_cues_in_state": state_scoping}))
    sn = {}
    for name, rws in (("train", ctx.train), ("dev", ctx.dev)):
        yn = yes_rows(rws)
        a = [R for R in yn if R["an"]["state_neg"]]
        b = [R for R in yn if not R["an"]["state_neg"]]
        ya = sum(gold_yes(R) for R in a) / len(a) if a else None
        yb = sum(gold_yes(R) for R in b) / len(b) if b else None
        sn[name] = {"with": [r3(ya), len(a)], "without": [r3(yb), len(b)]}
        okk = ya is None or yb is None or abs(ya - yb) <= STATE_NEG_TOL + max(0.5 / len(a), 0.5 / len(b))
        sn[name]["ok"] = okk
    out.append(Sub("4.15", "yes share equal (+- 2 pts) for states with and without negation (item 19)",
                   status(all(v["ok"] for v in sn.values())), sn, f"|diff| <= {STATE_NEG_TOL}", "CL:99-101, CL:324"))
    return out


def choice_balance(ctx):
    res, bad = {}, []
    for name, rows in (("train", ctx.train), ("dev", ctx.dev)):
        ch = [R for R in rows if not R["an"]["yn"]]
        n = len(rows)
        res[name] = {"choice_share": r3(len(ch) / n) if n else None}
        if not share_ok(len(ch), n, *CHOICE_SHARE):
            bad.append(f"{name}: choice share {len(ch)}/{n}")
        oc = Counter(len(R["row"]["options"]) for R in ch)
        res[name]["option_counts"] = dict(oc)
        if any(not CHOICE_OPTS[0] <= k <= CHOICE_OPTS[1] for k in oc):
            bad.append(f"{name}: option count outside 3-5")
        for k in oc:
            rk = [R for R in ch if len(R["row"]["options"]) == k]
            pc = Counter(R["m"]["gold"] for R in rk)
            for p in range(k):
                if not within(pc[p], len(rk), 1 / k, CHOICE_POS_TOL):
                    bad.append(f"{name}: k={k} position {p} {pc[p]}/{len(rk)}")
        neg = sum(1 for R in ch if R["an"]["select_false"])
        res[name]["negated_selection"] = r3(neg / len(ch)) if ch else None
        if ch and not share_ok(neg, len(ch), *CHOICE_NEGSEL):
            bad.append(f"{name}: negated selection {neg}/{len(ch)}")
    return Sub("4.5", "choice rows: 20% +- 3 of rows; 3-5 options; gold position uniform +- 3 pts per option count; "
                      "negated selection ~50%", status(not bad), res,
               {"share": CHOICE_SHARE, "options": CHOICE_OPTS, "pos_tol": CHOICE_POS_TOL, "negsel": CHOICE_NEGSEL},
               "CL:327, CL:166", bad[:20])


def cardless_and_style(ctx):
    out = []
    bad_frame, bad_share = [], {}
    for name, rows in (("train", ctx.train), ("dev", ctx.dev)):
        yn = yes_rows(rows)
        nc = [R for R in yn if not (R["row"].get("card") or "").strip()]
        for R in nc:
            if not CARDLESS_OK_RE.search(R["row"].get("instructions") or ""):
                bad_frame.append(R["row"]["id"])
        tot = len(nc) / len(yn) if yn else 0
        for key, f in (("depth", lambda R: R["an"]["depth"]), ("gold", lambda R: R["row"]["gold"])):
            grp = defaultdict(list)
            for R in yn:
                grp[f(R)].append(R)
            for g, rs in grp.items():
                k = sum(1 for R in rs if not (R["row"].get("card") or "").strip())
                if not within(k, len(rs), tot, CARDLESS_TOL):
                    bad_share[f"{name}:{key}={g}"] = [k, len(rs), r3(tot)]
    out.append(Sub("4.6", "card-less rows only with 'Is it true/false that' frames; card-less share equal (+- 2 pts) at "
                          "every depth and both golds", status(not bad_frame and not bad_share),
                   {"bad_frame_rows": len(bad_frame), "bad_share_groups": len(bad_share)}, "0 / 0", "CL:231-232",
                   {"examples": bad_frame[:6], "groups": bad_share}))
    bad = {}
    for name, rows in (("train", ctx.train), ("dev", ctx.dev)):
        yn = yes_rows(rows)
        styles = Counter(R["m"]["card_style"] for R in yn)
        for st, tot_n in styles.items():
            tot = tot_n / len(yn)
            for key, f in (("depth", lambda R: R["an"]["depth"]), ("gold", lambda R: R["row"]["gold"])):
                grp = defaultdict(list)
                for R in yn:
                    grp[f(R)].append(R)
                for g, rs in grp.items():
                    k = sum(1 for R in rs if R["m"]["card_style"] == st)
                    if not within(k, len(rs), tot, CARD_STYLE_TOL):
                        bad[f"{name}:{st}:{key}={g}"] = [k, len(rs), r3(tot)]
    out.append(Sub("4.6b", "card style share equal (+- 2 pts) per depth and per gold", status(not bad), len(bad),
                   "0", "CL:229-232, CL:403", dict(list(bad.items())[:30])))
    return out


# ===================================================================================================== check 5: surface probes
def probe_texts(R):
    r = R["row"]
    return " ".join([r.get("instructions") or "", " || ", r.get("card") or "", " || "] +
                    [o for o in (r.get("options") or []) if isinstance(o, str)])


def length_feats(ctx, R):
    r = R["row"]
    q = r.get("instructions") or ""
    card = r.get("card") or ""
    opts = [o for o in (r.get("options") or []) if isinstance(o, str)]
    return [len(q), len(q.split()), len(card), len(card_lines(card)), len(opts),
            (sum(map(len, opts)) / len(opts)) if opts else 0, len(NARROW_RE.findall(mask_quotes(q))),
            ctx.full_cue_count(q), len(QUOTE_RE.findall(q)), len(SENT_SPLIT_RE.split(q)), q.count(","),
            1 if card.strip() else 0, len(yn_lines(card))]


def acc(pred, y):
    return sum(1 for a, b in zip(pred, y) if a == b) / len(y) if len(y) else None


def strat_acc(rows, pred, y):
    grp = defaultdict(lambda: [0, 0])
    for R, p, t in zip(rows, pred, y):
        for s in strata_keys(R) + [("rung", R["m"]["rung"]), ("depth_x_ncues", f"{R['an']['depth']}x{R['an']['n_all']}")]:
            grp[s][0] += 1 if p == t else 0
            grp[s][1] += 1
    worst = None
    for s, (k, n) in grp.items():
        if n >= PROBE_STRATUM_MIN_N:
            a = k / n
            if worst is None or a > worst[1]:
                worst = (f"{s[0]}={s[1]}", a, n)
    return worst


def check_probes(ctx: Ctx):
    out = []
    tr = yes_rows(ctx.train)
    dv = yes_rows(ctx.dev)
    if len(tr) < 10:
        out.append(Sub("5.0", "surface probes need yes/no train rows", "FAIL", len(tr), ">= 10", "CL:405-418"))
        return out
    ytr = [R["row"]["gold"] for R in tr]
    ydv = [R["row"]["gold"] for R in dv]
    groups = [R["m"]["ladder_id"] for R in tr]
    n_groups = len(set(groups))
    folds = min(CV_FOLDS, n_groups)
    from sklearn.model_selection import GroupKFold
    splits = list(GroupKFold(n_splits=folds).split(tr, ytr, groups)) if folds >= 2 else []
    maj = 1 if sum(ytr) * 2 >= len(ytr) else 0
    q = lambda R: R["row"].get("instructions") or ""  # noqa: E731
    probes = {}

    def rule(f):
        return [f(R) for R in tr], [f(R) for R in dv]
    probes["a1 always yes"] = rule(lambda R: 1)
    probes["a2 always no"] = rule(lambda R: 0)
    probes["b1 any cue -> no"] = rule(lambda R: 0 if ctx.full_cue_count(q(R)) > 0 else 1)
    probes["b2 any cue -> yes"] = rule(lambda R: 1 if ctx.full_cue_count(q(R)) > 0 else 0)
    probes["c 'not' present -> no"] = rule(lambda R: 0 if NOT_RE.search(mask_quotes(q(R))) else 1)
    probes["d even narrow cue count -> yes"] = rule(lambda R: 1 if len(NARROW_RE.findall(mask_quotes(q(R)))) % 2 == 0 else 0)
    probes["e even full-lexicon cue count -> yes"] = rule(lambda R: 1 if ctx.full_cue_count(q(R)) % 2 == 0 else 0)

    def cv(fit_predict):
        p = [None] * len(tr)
        for a, b in splits:
            pr = fit_predict([tr[i] for i in a], [ytr[i] for i in a], [tr[i] for i in b])
            for i, v in zip(b, pr):
                p[i] = v
        if not splits:
            p = [maj] * len(tr)
        return p, (fit_predict(tr, ytr, dv) if dv else [])

    def maj_by(keyf):
        def fp(rows_a, y_a, rows_b):
            c = defaultdict(lambda: [0, 0])
            for R, y in zip(rows_a, y_a):
                for k in keyf(R):
                    c[k][0] += y
                    c[k][1] += 1
            m0 = 1 if sum(y_a) * 2 >= len(y_a) else 0
            res = []
            for R in rows_b:
                vote = 0
                for k in keyf(R):
                    if k in c:
                        a, n = c[k]
                        vote += 1 if a * 2 > n else (-1 if a * 2 < n else 0)
                res.append(1 if vote > 0 else (0 if vote < 0 else m0))
            return res
        return fp
    lexcache = {}

    def lexs(R):
        rid = R["row"]["id"]
        if rid not in lexcache:
            lexcache[rid] = ctx.lexemes_in(q(R))
        return lexcache[rid]
    probes["f per-lexeme majority"] = cv(maj_by(lexs))
    probes["g1 per-frame majority"] = cv(maj_by(lambda R: [R["m"]["frame_id"]]))
    probes["g2 per-template majority"] = cv(maj_by(lambda R: [R["an"]["carrier"]]))
    skipped = []
    if ctx.opts.fast:
        skipped += ["h bag-of-words + bigrams LR", "i length / count LR"]
    else:
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler

        def bow(rows_a, y_a, rows_b):
            if len(set(y_a)) < 2:
                return [y_a[0]] * len(rows_b)
            v = CountVectorizer(ngram_range=(1, 2), min_df=2, binary=True, lowercase=True,
                                token_pattern=r"(?u)\b\w[\w'-]*\b")
            X = v.fit_transform([probe_texts(R) for R in rows_a])
            clf = LogisticRegression(C=1.0, max_iter=2000, solver="liblinear").fit(X, y_a)
            return list(clf.predict(v.transform([probe_texts(R) for R in rows_b])))

        def lenlr(rows_a, y_a, rows_b):
            if len(set(y_a)) < 2:
                return [y_a[0]] * len(rows_b)
            sc = StandardScaler()
            X = sc.fit_transform([length_feats(ctx, R) for R in rows_a])
            clf = LogisticRegression(C=1.0, max_iter=2000).fit(X, y_a)
            return list(clf.predict(sc.transform([length_feats(ctx, R) for R in rows_b])))
        probes["h bag-of-words + bigrams LR"] = cv(bow)
        probes["i length / count LR"] = cv(lenlr)
    for i, (name, (ptr, pdv)) in enumerate(probes.items()):
        atr, adv = acc(ptr, ytr), acc(pdv, ydv) if dv else None
        wtr = strat_acc(tr, ptr, ytr)
        wdv = strat_acc(dv, pdv, ydv) if dv else None
        ok = (atr <= PROBE_MAX + 1e-12 and (adv is None or adv <= PROBE_MAX + 1e-12)
              and (wtr is None or wtr[1] <= PROBE_STRATUM_MAX + 1e-12)
              and (wdv is None or wdv[1] <= PROBE_STRATUM_MAX + 1e-12))
        out.append(Sub(f"5.{name.split()[0]}", f"probe {name}", status(ok),
                       {"train_cv": r3(atr), "dev": r3(adv),
                        "worst_stratum_train": [wtr[0], r3(wtr[1]), wtr[2]] if wtr else None,
                        "worst_stratum_dev": [wdv[0], r3(wdv[1]), wdv[2]] if wdv else None},
                       f"<= {PROBE_MAX} overall, <= {PROBE_STRATUM_MAX} per stratum >= {PROBE_STRATUM_MIN_N}",
                       "CL:405-418"))
    for s in skipped:
        out.append(Sub(f"5.{s.split()[0]}", f"probe {s}", "SKIP", None, f"<= {PROBE_MAX}", "CL:416-417", "--fast"))
    out.append(choice_probes(ctx))
    out.append(correlations(ctx))
    out.append(yn_restates(ctx))
    if ctx.opts.fast:
        out.append(Sub("5.m", "SPEC 8.4 TF-IDF train -> dev (question <= 55%, state + question <= 60%)", "SKIP", None,
                       "<= 0.55 / <= 0.60", "SPEC 8.4", "--fast"))
    else:
        out.append(spec_tfidf(ctx, tr, dv))
    return out


def choice_probes(ctx):
    res = {}
    bad = []
    for name, rows in (("train", ctx.train), ("dev", ctx.dev)):
        ch = [R for R in rows if not R["an"]["yn"]]
        if not ch:
            res[name] = "no choice rows"
            continue
        gold = [R["m"]["gold"] for R in ch]
        pos_c = defaultdict(Counter)
        for R in ctx.train:
            if not R["an"]["yn"]:
                pos_c[len(R["row"]["options"])][R["m"]["gold"]] += 1
        rules = {
            "position majority": lambda R: (pos_c[len(R["row"]["options"])].most_common(1) or [(0, 0)])[0][0],
            "longest option": lambda R: max(range(len(R["row"]["options"])), key=lambda i: len(R["row"]["options"][i])),
            "most cues": lambda R: max(range(len(R["row"]["options"])),
                                       key=lambda i: ctx.full_cue_count(R["row"]["options"][i])),
            "fewest cues": lambda R: min(range(len(R["row"]["options"])),
                                         key=lambda i: ctx.full_cue_count(R["row"]["options"][i])),
            "most question overlap": lambda R: max(range(len(R["row"]["options"])), key=lambda i: len(
                set(words(R["row"]["options"][i])) & set(words(R["row"].get("instructions"))))),
        }
        res[name] = {}
        for rn, f in rules.items():
            pred = [f(R) for R in ch]
            a = acc(pred, gold)
            w = strat_acc(ch, pred, gold)
            res[name][rn] = [r3(a), [w[0], r3(w[1]), w[2]] if w else None]
            if a > PROBE_MAX + 1e-12 or (w and w[1] > PROBE_STRATUM_MAX + 1e-12):
                bad.append(f"{name}: {rn}")
    n_ch = sum(1 for R in ctx.ok if not R["an"]["yn"])
    return Sub("5.j", "probe (j) choice rows: position majority, longest option, most / fewest cues, most overlap",
               status(not bad and n_ch > 0), res, f"<= {PROBE_MAX} (no choice rows = FAIL: item 36 / CL:327 need them)",
               "CL:417", bad)


def corr(x, y):
    n = len(x)
    if n < 3:
        return None
    mx, my = sum(x) / n, sum(y) / n
    vx = sum((a - mx) ** 2 for a in x)
    vy = sum((b - my) ** 2 for b in y)
    if vx <= 0 or vy <= 0:
        return 0.0
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / math.sqrt(vx * vy)


def correlations(ctx):
    res, bad = {}, []
    for name, rows in (("train", ctx.train), ("dev", ctx.dev)):
        yn = yes_rows(rows)
        if len(yn) < 3:
            continue
        y = [R["row"]["gold"] for R in yn]
        feats = {
            "cue_count": [R["an"]["n_all"] for R in yn],
            "cue_count_parity": [R["an"]["n_all"] % 2 for R in yn],
            "has_not": [1 if NOT_RE.search(mask_quotes(R["row"].get("instructions") or "")) else 0 for R in yn],
            "has_affix": [1 if any(c["cls"] == "affixal" for c in R["m"]["cues"]) else 0 for R in yn],
            "has_lexical": [1 if any(c["cls"] == "lexical" for c in R["m"]["cues"]) else 0 for R in yn],
            "has_distractor": [1 if R["an"]["n_dist"] else 0 for R in yn],
            "length_bin": [R["an"]["len_bin"] for R in yn],
        }
        for st in sorted({R["m"]["card_style"] for R in yn}):
            feats[f"card_style={st}"] = [1 if R["m"]["card_style"] == st else 0 for R in yn]
        res[name] = {}
        for k, x in feats.items():
            r = corr(x, y)
            res[name][k] = r3(r)
            if r is not None and abs(r) >= CORR_MAX:
                bad.append(f"{name}:{k}={r3(r)}")
        ch = [R for R in rows if not R["an"]["yn"]]
        if len(ch) >= 3:
            gp = [R["m"]["gold"] / max(1, len(R["row"]["options"]) - 1) for R in ch]
            for k, x in (("negated_selection", [1 if R["an"]["select_false"] else 0 for R in ch]),
                         ("cue_count", [R["an"]["n_all"] for R in ch]),
                         ("option_count", [len(R["row"]["options"]) for R in ch]),
                         ("depth", [R["an"]["depth"] for R in ch])):
                r = corr(x, gp)
                res[name][f"choice_gold_position~{k}"] = r3(r)
                if r is not None and abs(r) >= CORR_MAX:
                    bad.append(f"{name}:choice_gold_position~{k}={r3(r)}")
    return Sub("5.k", "|r| < 0.05 between gold and cue count / parity / has not / affix / lexical / distractor / card "
                      "style / length bin; choice gold position", status(not bad), res, f"|r| < {CORR_MAX}",
               "CL:419-421", bad)


def yn_restates(ctx):
    """Rule 2.4: each yes/no card line restates the question with the same cue words (never a simplified form)."""
    n, bad = 0, []
    for R in ctx.ok:
        if not R["an"]["yn"] or not R["an"]["has_yn"]:
            continue
        n += 1
        yes_line = [ln for ln in yn_lines(R["row"].get("card")) if ln.split(":")[0].strip(" -").lower() == "yes"][0]
        yl = YN_LINE_RE.sub("", yes_line, count=1).lower()
        miss = []
        for c in R["m"]["cues"]:
            if c["cls"] == "lookalike" or c["position"] not in QUESTION_POSITIONS or c["position"] == "choice_option":
                continue
            surf = (c.get("surface") or c["lexeme"]).lower().strip()
            if surf.startswith("-") or surf.endswith("-"):
                if surf.strip("-") not in yl:
                    miss.append(surf)
                continue
            forms = inflections(surf) or [surf]
            if not any(re.search(r"(?<![\w-])" + re.escape(f).replace(r"\ ", r"\s+") + r"(?![\w-])", yl) for f in forms):
                if surf in ("n't", "nt") and re.search(r"n't\b|\bnot\b", yl):
                    continue
                miss.append(surf)
        if miss:
            bad.append((R["row"]["id"], miss[:3]))
    return Sub("5.l", "yes/no card lines restate the question with the same cues (no simplified form)", status(not bad),
               f"{n - len(bad)}/{n}", "100%", "CL:228-230", {"examples": bad[:8]})


def spec_tfidf(ctx, tr, dv):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    if not dv:
        return Sub("5.m", "SPEC 8.4 TF-IDF train -> dev (question <= 55%, state + question <= 60%)", "FAIL", None,
                   "<= 0.55 / <= 0.60", "SPEC 8.4", "no dev rows")
    ytr = [R["row"]["gold"] for R in tr]
    ydv = [R["row"]["gold"] for R in dv]
    res = {}
    for name, f, lim in (("question", lambda R: R["row"].get("instructions") or "", SPEC_TFIDF_Q_MAX),
                         ("state+question", lambda R: (R["row"].get("state") or "") + " || " +
                          (R["row"].get("instructions") or ""), SPEC_TFIDF_SQ_MAX)):
        v = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)
        X = v.fit_transform([f(R) for R in tr])
        clf = LogisticRegression(C=1.0, max_iter=2000, solver="liblinear").fit(X, ytr)
        a = acc(list(clf.predict(v.transform([f(R) for R in dv]))), ydv)
        res[name] = [r3(a), lim]
    ok = all(a <= lim + 1e-12 for a, lim in res.values())
    return Sub("5.m", "SPEC 8.4 TF-IDF train -> dev (question <= 55%, state + question <= 60%)", status(ok), res,
               "<= 0.55 / <= 0.60", "SPEC 8.4")


# ===================================================================================================== check 6: composition
def comp_preds(R):
    an, m = R["an"], R["m"]
    tp = 1 if an["truth_P"] else 0
    cues = m["cues"]
    allc = len(cues)
    syn = sum(1 for c in cues if c["cls"] == "syntactic")
    outer = any(c["position"] == "outer_frame" and c["cls"] != "lookalike" for c in cues)
    inner = any(c["position"] == "inner_claim" and c["cls"] != "lookalike" for c in cues)
    p = {"C1 ignore negation": tp, "C2 count all cues": tp ^ (allc % 2), "C3 count syntactic cues": tp ^ (syn % 2),
         "C4 outer cue only": tp ^ int(outer), "C5 inner cue only": tp ^ int(inner)}
    for cl, members in (("affixal", ("affixal",)), ("lexical", ("lexical",)),
                        ("cross-sentence", ("cross_sentence", "answer_mapping"))):
        k = sum(1 for c in cues if c["cls"] not in members)
        p[f"C6 counter ignoring {cl}"] = tp ^ (k % 2)
        ks = sum(1 for c in an["scoping"] if c["cls"] not in members) + (1 if an["null_not"] else 0)
        p[f"C6i scope reader ignoring {cl}"] = tp ^ (ks % 2)
    return p


def check_composition(ctx: Ctx):
    out = []
    for name, rows in (("train", ctx.train), ("dev", ctx.dev)):
        yn = yes_rows(rows)
        sfx = {"train": "a", "dev": "b"}[name]
        if not yn:
            out.append(Sub(f"6.0{sfx}", f"[{name}] composition probes need yes/no rows", "FAIL", 0, "> 0", "CL:422-433"))
            continue
        y = [R["row"]["gold"] for R in yn]
        preds = defaultdict(list)
        for R in yn:
            for k, v in comp_preds(R).items():
                preds[k].append(v)
        res = {k: r3(acc(v, y)) for k, v in preds.items()}
        c2_depth = {}
        for d in sorted({R["an"]["depth"] for R in yn}):
            idx = [i for i, R in enumerate(yn) if R["an"]["depth"] == d]
            c2_depth[d] = r3(acc([preds["C2 count all cues"][i] for i in idx], [y[i] for i in idx]))
        checks = [
            ("C1", "C1 ignore negation: gold = truth(P)", C1_BAND[0] - 1e-12 <= res["C1 ignore negation"] <= C1_BAND[1] + 1e-12,
             res["C1 ignore negation"], "45-55%", "CL:426"),
            ("C2", "C2 truth(P) XOR parity(all cues)", res["C2 count all cues"] <= C2_MAX + 1e-12 and
             all(v <= C2_DEPTH_MAX + 1e-12 for v in c2_depth.values()),
             {"overall": res["C2 count all cues"], "per_depth": c2_depth}, "<= 70% overall, <= 75% per depth", "CL:427"),
            ("C3", "C3 truth(P) XOR parity(syntactic cues)", res["C3 count syntactic cues"] <= C3_MAX + 1e-12,
             res["C3 count syntactic cues"], "<= 65%", "CL:428"),
            ("C4", "C4 truth(P) XOR (outer cue present)", res["C4 outer cue only"] <= C4_MAX + 1e-12,
             res["C4 outer cue only"], "<= 60%", "CL:429"),
            ("C5", "C5 truth(P) XOR (inner cue present)", res["C5 inner cue only"] <= C5_MAX + 1e-12,
             res["C5 inner cue only"], "<= 60%", "CL:430"),
            ("C6", "C6 cue counter ignoring one class (affixal / lexical / cross-sentence)",
             all(res[f"C6 counter ignoring {c}"] <= C6_MAX + 1e-12 for c in ("affixal", "lexical", "cross-sentence")),
             {k: v for k, v in res.items() if k.startswith("C6")}, "<= 60% each (C6i scope-reader variant: info)",
             "CL:431"),
        ]
        for cid, nm, ok, val, tgt, cite in checks:
            out.append(Sub(f"6.{cid}{sfx}", f"[{name}] {nm}", status(ok), val, tgt, cite))
        it21 = [R for R in yn if 21 in R["m"]["phen"]]
        if not it21:
            out.append(Sub(f"6.C7{sfx}", f"[{name}] C7 antonym reading wrong on >= 30% of item-21 rows", "FAIL", None,
                           ">= 30%", "CL:432", "no item-21 rows (MUST item)"))
        else:
            wrong = sum(1 for R in it21 if int(bool(R["m"]["antonym_gold"])) != R["row"]["gold"])
            out.append(Sub(f"6.C7{sfx}", f"[{name}] C7 antonym reading wrong on >= 30% of item-21 rows",
                           status(wrong / len(it21) >= C7_WRONG_MIN - 1e-12), r3(wrong / len(it21)), ">= 30%",
                           "CL:432", {"rows": len(it21)}))
        par = defaultdict(lambda: [0, 0])
        for R in yn:
            for lx_ in {c["lexeme"].lower() for c in R["m"]["cues"]}:
                par[lx_][0] += R["an"]["depth"] % 2
                par[lx_][1] += 1
        bad = {k: [a, n] for k, (a, n) in par.items() if n >= CUE_SHARE_MIN_ROWS and not share_ok(a, n, *CUE_SHARE_BAND)}
        out.append(Sub(f"6.CS{sfx}", f"[{name}] cue share: odd-parity share 40-60% for every lexeme with >= 30 rows",
                       status(not bad), {"bad": len(bad), "lexemes_ge30": sum(1 for v in par.values()
                                                                              if v[1] >= CUE_SHARE_MIN_ROWS)},
                       "40-60%", "CL:433", bad))
    return out


# ===================================================================================================== check 7: EXCLUDE
GRADABLE = ("happy|likely|common|usual|important|reasonable|kind|fair|clear|interesting|pleasant|helpful|polite|"
            "friendly|safe|satisfied|comfortable|pleased|attractive|impressive|significant|popular|familiar|typical|"
            "believable|convincing|sympathetic|welcome|worthy|appealing|honest|wise|lucky|easy|able|patient|healthy|"
            "tidy|fortunate|successful|effective|efficient|possible|probable|certain|sure|aware|reliable|willing|"
            "relevant|responsible|rational|regular|logical|loyal|respectful|attentive|reasonable|sensitive|mature|"
            "polished|professional|courteous|tolerable|acceptable|appropriate|adequate|sufficient|convenient")
AUX = r"(?:is|are|was|were|does|do|did|has|have|had|can|could|should|would|will|must|may|might|shall)"
NEG_AUX = (r"(?:isn't|aren't|wasn't|weren't|doesn't|don't|didn't|hasn't|haven't|hadn't|won't|wouldn't|shouldn't|"
           r"couldn't|can't|mustn't|needn't|shan't|ain't)")
X_RE = {
    "X1": [re.compile(r"(?:^|[.!?:]\s+)" + NEG_AUX + r"\b[^?.!]*\?", re.I),
           re.compile(r"(?:^|[.!?:]\s+)" + AUX + r"\s+not\b[^?.!]*\?", re.I),
           re.compile(r"(?:^|[.!?:]\s+)is\s+it\s+not\b[^?.!]*\?", re.I)],
    "X2": [re.compile(r"\b(?:not|n't|never)\s+(?:(?:very|so|too|entirely|altogether|that|exactly|particularly|wholly|"
                      r"totally|completely)\s+)?((?:un|in|im|ir|il|dis)(?:" + GRADABLE + r"))\b", re.I),
           re.compile(r"\b(?:not|n't)\s+(?:half\s+)?bad\b", re.I),
           re.compile(r"\bnot\s+without\s+(?:merit|interest|charm|reason|its\s+\w+)\b", re.I)],
    "X3": [re.compile(r"\bnot\s+[\w-]+\s*[,;:—–]\s*(?:it|this|that|he|she|they)\s*(?:'s|is|was|were|are)\b", re.I),
           re.compile(r"n't\s+[\w-]+\s*[,;:—–]\s*(?:it|this|that|he|she|they)\s*(?:'s|is|was|were|are)\b", re.I)],
    "X4": [re.compile(r"\b(?:may|might)\s+not\b|\b(?:mayn't|mightn't)\b", re.I)],
    "X5": [re.compile(r"(?:^|[.;:,!?]\s*|\b(?:that|whether|if|because|when|and|but|or|then)\s+)"
                      r"(?:all|every|everyone|everybody|everything)\b(?!\s+but\b)(?:\s+(?!(?:is|are|was|were|do|does|did|has|have|can|will|that|whether)\b)[\w'-]+){0,6}"
                      r"\s+(?:is|are|was|were|do|does|did|has|have|can|could|will|would|should|must)(?:n't|\s+not)\b", re.I)],
    "X6": [re.compile(r"\b(?:do|does|did)(?:n't|\s+not)\s+(?:think|believe|expect|suppose|imagine|reckon|guess|"
                      r"anticipate|feel\s+that)\b", re.I),
           re.compile(r"\b(?:don't|doesn't|didn't)\s+(?:seem|appear)\s+to\b", re.I)],
    "X7": [re.compile(r"\b(?:not|n't|never|fail(?:s|ed|ing)?\s+to|without)\s+(?:\w+\s+)?(?:notice|noticing|realize|"
                      r"realise|realizing|realising|know|knowing|regret|regretting|discover|discovering|forget|"
                      r"forgetting|remember|remembering|recognize|recognise|learn|learning|admit|admitting|acknowledge|"
                      r"acknowledging|reveal|revealing|find\s+out|be\s+aware|been\s+aware|resent|appreciate)\s+that\b",
                      re.I),
           re.compile(r"\b(?:unaware|not\s+aware|ignorant)\s+that\b", re.I)],
    "X8": [re.compile(r"n't\s+(?:(?!that\b|whether\b|if\b)\w+\s+){0,3}?(?:no|nothing|nobody|none|nowhere|neither|never)\b",
                      re.I),
           re.compile(r"\bnot\s+(?:(?!that\b|whether\b|if\b)\w+\s+){0,2}?(?:nothing|nobody|nowhere|none)\b", re.I),
           re.compile(r"\bnever\s+(?:(?!that\b|whether\b|if\b)\w+\s+){0,2}?(?:no|nothing|nobody|nowhere)\b", re.I)],
    "X9": [re.compile(r"\b(?:not|n't|never)\s+(?:\w+\s+){1,6}?(?:on|in|at|during|before|after|until)\s+(?:monday|"
                      r"tuesday|wednesday|thursday|friday|saturday|sunday|january|february|march|april|june|july|"
                      r"august|september|october|november|december|\d{1,2}(?:st|nd|rd|th)?\b|the\s+(?:morning|evening|"
                      r"afternoon|weekend)|time\b|purpose\b)", re.I),
           re.compile(r"\b(?:not|n't)\s+(?:\w+\s+){1,6}?because\b", re.I),
           re.compile(r"\b(?:not|n't)\s+(?:\w+\s+){0,6}?(?:deliberately|intentionally|on\s+purpose|by\s+mistake|by\s+"
                      r"accident|yesterday|today|last\s+(?:week|month|year)|this\s+morning)\b", re.I)],
    "X11": [re.compile(r"\bno\s+wonder\b|\bcan(?:'t|not)\s+help\s+(?:but|\w+ing)\b|\bnot\s+half\s+bad\b|\bno\s+doubt\b|"
                       r"\bwithout\s+(?:a\s+)?doubt\b|\bnothing\s+if\s+not\b|\bno\s+sooner\b|\bnone\s+other\s+than\b|"
                       r"\bnot\s+to\s+mention\b|\bcould(?:n't|\s+not)\s+care\s+less\b|\bnever\s+mind\b|\bnot\s+least\b|"
                       r"\bno\s+problem\b|\bnone\s+the\s+(?:less|worse|wiser)\b|\bnot\s+a\s+(?:bit|little)\b|"
                       r"\bnothing\s+short\s+of\b|\bnot\s+for\s+nothing\b", re.I)],
}
X10_RE = re.compile(r"\bnot\s+(?:all|every|everyone|everything|always)\b|\bsome\b[^.?!;:\n]{0,40}(?:\bnot\b|n't\b)", re.I)
INNER_NEG_Q = re.compile(r"(?:^|[.!?:]\s+)" + AUX + r"\s+(?!it\b|not\b)(?:(?!that\b|whether\b|if\b)[\w'-]+\s+){1,5}?"
                         r"not\s+\w+[^?.!]*\?", re.I)
# > 1 negative affix on one word: hyphenated stacks only (non-un..., un-non-..., non-X-free, unX-free, non-X-less); an
# unhyphenated 'non' + 'in...' cannot be told from a stem (non-injury), so affix stacks are also counted from the sidecar
DOUBLE_AFFIX = re.compile(r"\bnon-un[a-z]{4,}|\bun-?non-[a-z]+|\bnon-[a-z]+-free\b|\bun[a-z]+-free\b|\bnon-[a-z]+less\b",
                          re.I)
DOUBLE_AFFIX_OK = {"non-union", "non-unionized", "non-uniform", "non-unique", "non-universal", "non-units"}
NPI_RE = re.compile(r"\b(?:contains?|contained|mentions?|mentioned|includes?|included|has|have|had|asks?\s+for|gives?|"
                    r"gave|reports?|reported|shows?|showed|states?|stated|expresses?|expressed|names?|named)\s+any\b|"
                    r"\bever\b|\bat\s+all\b|\banymore\b", re.I)
NPI_LICENSOR = re.compile(r"\?|\b(?:not|no|never|none|nothing|nobody|neither|nor|without|cannot|only|every|all|each|few|"
                          r"if|whether|unless|before|than|too|false|untrue|unfounded|baseless|unsupported|deny|denies|"
                          r"denied|doubt\w*|refut\w*|reject\w*|disput\w*|lack\w*|fail\w*|free\s+of|devoid|hardly|"
                          r"at\s+most|no\s+more\s+than)\b|n't\b", re.I)


def clause_neg_count(ctx, clause):
    return ctx.full_cue_count(clause)


def exclude_hits(ctx, R):
    """{X: [matched text]} over instructions, card and options (quotes and card label keys masked)."""
    row = R["row"]
    keys = card_keys(row.get("card"))
    texts = [mask_quotes(row.get("instructions") or "")]
    texts += [mask_quotes(o) for o in (row.get("options") or []) if isinstance(o, str)]
    texts += [mask_quotes(mask_card_line(ln)) for ln in card_lines(row.get("card"))]
    auth = [mask_quotes(t) for t in authored_texts(row)]
    hits = defaultdict(list)
    for t in texts:
        for x, rxs in X_RE.items():
            for rx in rxs:
                for mt in rx.finditer(t):
                    s = mt.group(0)
                    if x == "X2" and mt.lastindex and mt.group(1).lower() in keys:
                        continue
                    hits[x].append(s[:80])
    # X1 (b): an inner-negative polar question needs full yes/no card lines (item 38, CL:172)
    q = mask_quotes(row.get("instructions") or "")
    if INNER_NEG_Q.search(q) and not R["an"].get("has_yn"):
        hits["X1"].append("inner-negative question without yes/no lines: " + INNER_NEG_Q.search(q).group(0)[:60])
    # X10: 'not all' / 'some ... not' without a card logic line
    if any(X10_RE.search(t) for t in auth) and not LOGIC_LINE_RE.search(row.get("card") or ""):
        hits["X10"].append([X10_RE.search(t).group(0) for t in auth if X10_RE.search(t)][0][:60])
    # X12: ill-formed stacks: > 1 affix per word, > 2 cues per clause, unlicensed NPIs
    for t in texts:
        for mt in DOUBLE_AFFIX.finditer(t):
            if mt.group(0).lower() not in DOUBLE_AFFIX_OK:
                hits["X12"].append("double affix: " + mt.group(0))
    surf = Counter((c.get("surface") or "").lower() for c in (R["m"] or {}).get("cues", [])
                   if c["cls"] == "affixal" and c.get("surface"))
    for w, k in surf.items():
        if k > MAX_AFFIX_PER_WORD:
            hits["X12"].append(f"{k} affixal cues on one word: {w}")
    # > 2 cues in one clause: counted from the sidecar per clause-level position (a linear text splitter cannot see
    # centre-embedded clauses such as 'the claim that <claim> is unfounded')
    pc = Counter(c["position"] for c in (R["m"] or {}).get("cues", []) if c["cls"] != "lookalike")
    for p_, k in pc.items():
        if p_ in ("inner_claim", "outer_frame", "separate_sentence", "answer_map") and k > MAX_CUES_PER_CLAUSE:
            hits["X12"].append(f"cues per clause > 2: {k} cues at {p_}")
    for t in auth:
        for sent in SENT_SPLIT_RE.split(t):
            for cl in re.split(r"[,;:]", sent):
                mt = NPI_RE.search(cl)
                if mt and not NPI_LICENSOR.search(sent if "?" in sent else cl):
                    hits["X12"].append("unlicensed NPI: " + cl.strip()[:60])
    return hits


def check_exclude(ctx: Ctx):
    out = []
    per_x = Counter()
    rows_hit = defaultdict(list)
    for R in ctx.ok:
        h = exclude_hits(ctx, R)
        for x, v in h.items():
            per_x[x] += 1
            if len(rows_hit[x]) < 5:
                rows_hit[x].append((R["row"]["id"], v[0]))
    state_tag = Counter()
    for R in ctx.ok:
        st = mask_quotes(R["row"].get("state") or "")
        for x, rxs in X_RE.items():
            if any(rx.search(st) for rx in rxs):
                state_tag[x] += 1
    xs = [f"X{i}" for i in range(1, 13)]
    out.append(Sub("7.1", "EXCLUDE X1-X12: 0 rows with a hit in instructions, cards or options", status(not per_x),
                   {x: per_x.get(x, 0) for x in xs}, "0 each", "CL:176-191, CL:435-439",
                   {"examples": dict(rows_hit), "state_hits_tagged_not_counted": dict(state_tag)}))
    return out


# ===================================================================================================== check 8: decontamination
def load_neg_bench(manifest_path, log):
    """6-word runs (hashed) of the public negation-benchmark texts listed in the decontam-only manifest."""
    import check_yn2b as cy
    p = LEAN / manifest_path
    if not p.exists():
        return None, {"missing_manifest": str(manifest_path)}
    man = json.loads(p.read_text())
    runs, info, missing = set(), {}, []
    for src in man["sources"]:
        pat = os.path.expanduser(src["path"])
        if not os.path.isabs(pat):
            pat = str(LEAN / pat)
        files = sorted(glob.glob(pat, recursive=True))
        if not files:
            missing.append(src["name"])
            continue
        texts = []
        for fp in files:
            try:
                if src["format"] == "csv":
                    import pandas as pd
                    df = pd.read_csv(fp)
                    for f in src["fields"]:
                        if f in df.columns:
                            texts += [str(x) for x in df[f].dropna().tolist()]
                elif src["format"] == "arrow":
                    import pyarrow as pa
                    try:
                        tb = pa.ipc.open_stream(fp).read_all()
                    except Exception:  # noqa: BLE001
                        tb = pa.ipc.open_file(fp).read_all()
                    for f in src["fields"]:
                        if f in tb.column_names:
                            texts += [str(x) for x in tb.column(f).to_pylist() if x is not None]
                elif src["format"] == "json_lines":
                    with open(fp, encoding="utf-8") as fh:
                        for line in fh:
                            if line.strip():
                                r = json.loads(line)
                                texts += [str(r[f]) for f in src["fields"] if r.get(f)]
                elif src["format"] == "template_list":
                    texts += json.loads(Path(fp).read_text())["templates"]
            except Exception as e:  # noqa: BLE001
                missing.append(f"{src['name']}: {e!r}"[:200])
        n0 = len(runs)
        for t in set(texts):
            for rr in cy.runs(t):
                if "zzslot" not in rr:
                    runs.add(hash(rr))
        info[src["name"]] = {"files": len(files), "texts": len(set(texts)), "new_runs": len(runs) - n0}
    log(f"negation benchmarks: {len(runs):,} 6-word runs from {len(info)} sources (missing {missing})")
    return runs, {"sources": info, "missing": missing}


def ohs3_frames():
    """OHS-3's negation frames, read from the TEXT of build_ohs3.py (code, never OHS-3 data) with ast."""
    p = LEAN / "build_ohs3.py"
    if not p.exists():
        return []
    tree = ast.parse(p.read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "NEG_FRAMES" for t in node.targets):
            return [f for _, f in ast.literal_eval(node.value)]
    return []


def failure_frame_runs():
    """6-word runs of the measured-failure dev questions (devp_card hate pairs: 'contains only non-hateful content')."""
    import check_yn2b as cy
    p = LEAN / "data" / "devp_card.jsonl"
    runs, n = set(), 0
    if not p.exists():
        return None, 0
    with open(p, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r.get("source") == "hate" and "hateful" in (r.get("instructions") or ""):
                n += 1
                runs |= cy.runs(r["instructions"])
    return runs, n


def dev_source_names():
    """Sources of every dev split (re-derived by program each run, CL:222-223)."""
    import check_yn2b as cy
    names = set()
    files = list(cy.SHIP_SPLITS) + ["devzs2", "debate_dev", "hard12_dev", "proc12_dev", "planted12_dev", "dev_hc"]
    for f in files:
        p = LEAN / "data" / f"{f}.jsonl"
        if p.exists():
            with open(p, encoding="utf-8") as fh:
                for line in fh:
                    m = re.search(r'"source":\s*"([^"]+)"', line)
                    if m:
                        names.add(m.group(1))
    return names


def source_clash(s, dev):
    import gate_dev
    hits = set(gate_dev.source_seen(s, dev))
    hits |= {d for d in dev if gate_dev.source_seen(d, [s])}
    core = lambda x: re.sub(r"^(?:gd|br|tb|std)_", "", x.lower())  # noqa: E731
    cs = core(s)
    for d in dev:
        cd = core(d)
        if len(cd) >= 3 and len(cs) >= 3 and (re.search(r"(?:^|_)" + re.escape(cd) + r"(?:_|$)", cs)
                                               or re.search(r"(?:^|_)" + re.escape(cs) + r"(?:_|$)", cd)):
            hits.add(d)
    return sorted(hits)


def dup_rows_in_ladder(ctx):
    """ARBITER fix (F7_OBJECTIONS.md A2): ids of rows that repeat another row of the SAME ladder byte for byte (state,
    instruction, card, options). The cross-ladder dedupe exempts a ladder's own rows (they share the state by design);
    a full repeat inside a ladder is never a rung, it only double-counts one question (SPEC 7.5 'within yn2b')."""
    seen, out = {}, []
    for R in ctx.R:
        r = R["row"]
        lad = (R["m"] or {}).get("ladder_id") or r.get("call_id")
        k = (lad, r.get("state") or "", r.get("instructions") or "", r.get("card") or "",
             json.dumps(r.get("options"), ensure_ascii=False))
        if k in seen:
            out.append(r.get("id"))
        else:
            seen[k] = r.get("id")
    return out


def check_decontam(ctx: Ctx):
    out = []
    import check_yn2b as cy
    rows = [R for R in ctx.R]
    lad_of = lambda R: (R["m"] or {}).get("ladder_id") or R["row"].get("call_id")  # noqa: E731
    drop = defaultdict(set)
    # ---- names-free cheap checks first
    bw, bw_card = [], 0
    for R in rows:
        for t in authored_texts(R["row"]):
            mt = cy.BANNED_RE.search(t)
            if mt:
                bw.append((R["row"]["id"], mt.group(1).lower()))
                drop["banned_word"].add(lad_of(R))
                break
        if any(cy.BANNED_RE.search(ln) for ln in def_lines(R["row"].get("card"))):
            bw_card += 1
    out.append(Sub("8.7", "SPEC 4.7 banned judge words: 0 in instructions / options / yes-no lines", status(not bw),
                   len(bw), 0, "CL:286-287, SPEC 4.7", {"words": dict(Counter(w for _, w in bw)),
                                                        "card_definition_lines_report_only": bw_card}))
    items = [("F7", "instruction", R["row"].get("instructions") or "", bool(R["an"].get("depth", 0) % 2))
             for R in ctx.ok]
    cs = cy.cue_shares(items) if items else {}
    bad = {k: v for k, v in cs.items() if not v["pass"]}
    out.append(Sub("8.9", "SPEC 7.3 cue-share rule: no instruction word with >= 30 rows has an odd-parity share > 60%",
                   status(not bad), cs, f"<= {SPEC_CUE_SHARE_MAX}", "SPEC 7.3"))
    keyf = lambda R: hashlib.sha1((cy.norm(R["row"].get("state")) + "||" + cy.norm(R["row"].get("instructions"))).encode()).digest()  # noqa: E731
    first, dups = {}, []
    for R in rows:
        k = keyf(R)
        if k in first and first[k] != lad_of(R):
            dups.append(R["row"]["id"])
            drop["dedupe_within"].add(lad_of(R))
        first.setdefault(k, lad_of(R))
    ctx.dup_rows_in_ladder = dup_rows_in_ladder(ctx)
    dev_src = dev_source_names()
    clash = {}
    for R in ctx.ok:
        for s in {R["m"]["source"], (R["row"].get("meta") or {}).get("derived_source")} - {None}:
            if s not in clash:
                clash[s] = source_clash(s, dev_src)
    clash = {k: v for k, v in clash.items() if v}
    named = {"clinc150", "banking77", "std_hate", "gd_ghc_hate", "tb_label_nli"}
    out.append(Sub("8.15", "no F7 source is a dev source (dev source list re-derived by program; gate_dev.source_seen both "
                           "ways + name containment)", status(not clash),
                   {"clashes": clash, "dev_sources": len(dev_src),
                    "checklist_named_found": sorted(named & dev_src), "checklist_named_missing": sorted(named - dev_src)},
                   "0 clashes", "CL:221-223"))
    if ctx.opts.fast:
        for sid, nm in (("8.1", "12-gram vs held-out + every dev / eval split (strict)"),
                        ("8.2", "12-gram vs in-family devs (golden_dev, breadth_dev, yn2b devs)"),
                        ("8.3", "6-word runs vs dev instructions / dialogue_rebuttal / OHS-1/2 / eval spans / v11"),
                        ("8.4", "6-word runs vs public negation-benchmark frames"),
                        ("8.5", "measured-failure frame (6-word runs + dev / eval frame regexes)"),
                        ("8.6", "OHS-3 negation frames (build_ohs3.py text): no frame, no 5-word run of its fixed text"),
                        ("8.8", "ids and (state, instruction) pairs of reference rows"),
                        ("8.10", "SPEC 7.4 unseen set unchanged with the F7 train file"),
                        ("8.11", "SPEC 7.5 dedupe (within F7 and vs golden_train)"),
                        ("8.12", "SPEC 7.7 names")):
            out.append(Sub(sid, nm, "SKIP", None, "0", "CL:440-444", "--fast"))
    else:
        out.extend(decontam_full(ctx, drop, dups))
    if ctx.opts.ohs3_blind:
        out.append(ohs3_blind_counts(ctx))
    else:
        out.append(Sub("8.13", "SPEC 7.1 OHS-3 12-gram check (counts only)", "PENDING", None, "0 hit units",
                       "SPEC 7.1", "owner step: the build agents never open OHS-3; the owner runs --ohs3-blind"))
    n_drop = len(set().union(*drop.values())) if drop else 0
    out.append(Sub("8.14", "ladders that a decontamination hit would drop", status(n_drop == 0), n_drop, 0,
                   "CL:444", {k: len(v) for k, v in drop.items()}))
    return out


def decontam_full(ctx, drop, dups):
    import build_fix1 as bf
    import check_yn2b as cy
    out = []
    t0 = time.time()
    rx = bf.frame_regexes()
    Rf = bf.load_refs(ctx.log)
    lad_of = lambda R: (R["m"] or {}).get("ladder_id") or R["row"].get("call_id")  # noqa: E731
    hit = defaultdict(list)
    infam_src_rows = []
    for R in ctx.R:
        r = R["row"]
        ga = set().union(*[cy.row_ghash(t) for t in authored_texts(r)]) if authored_texts(r) else set()
        gs = set().union(*[cy.row_ghash(t) for t in [r.get("state") or ""] + def_lines(r.get("card"))])
        if (ga | gs) & Rf["strict"]:
            hit["12gram_strict"].append(r["id"])
        if (ga | gs) & Rf["infam_y"]:
            hit["12gram_yn2b_dev"].append(r["id"])
        if ga & Rf["infam"]:
            hit["12gram_golden_dev_authored"].append(r["id"])
        sh = gs & Rf["infam"]
        if sh:
            infam_src_rows.append((R, sh))
        tr = set().union(*[cy.runs(t) for t in authored_texts(r)])
        if tr & Rf["t6_dev"]:
            hit["tmpl6_dev"].append(r["id"])
        if tr & Rf["t6_v11"]:
            hit["tmpl6_v11"].append(r["id"])
        if bf.frame_hits(r, rx):
            hit["dev_eval_frame"].append(r["id"])
        if r["id"] in Rf["ids"]:
            hit["id"].append(r["id"])
        if bf.norm_pair(r) in Rf["pairs"]:
            hit["text_pair"].append(r["id"])
    # in-family source-text contacts are inherited only when every hitting gram is in the golden_train text the row
    # copies (state byte-equal to a golden_train state, card definitions from that row's card)
    inherited, not_inh = 0, []
    if infam_src_rows:
        gram_of = golden_scan(ctx)["grams"]
        for R, sh in infam_src_rows:
            h = sh8(R["row"].get("state"))
            if h in gram_of and sh <= gram_of[h]:
                inherited += 1
            else:
                not_inh.append(R["row"]["id"])
    if not_inh:
        hit["12gram_golden_dev_source_not_inherited"] = not_inh
    for k, ids in hit.items():
        for i in ids:
            R = ctx.by_rowid.get(i)
            if R:
                drop[k].add(lad_of(R))
    out.append(Sub("8.1", "12-gram vs held-out (OHS-1/2, eval*, JevBench public) + every dev / eval split (strict)",
                   status(not hit["12gram_strict"]), len(hit["12gram_strict"]), 0, "CL:441, SPEC 7.1-7.2"))
    k2 = len(hit["12gram_yn2b_dev"]) + len(hit["12gram_golden_dev_authored"]) + len(not_inh)
    out.append(Sub("8.2", "12-gram vs in-family devs: yn2b devs strict; golden_dev / breadth_dev strict for F7 text, "
                          "report-only where the row copies golden_train text", status(k2 == 0),
                   {"yn2b_dev": len(hit["12gram_yn2b_dev"]), "golden_dev_in_f7_text": len(hit["12gram_golden_dev_authored"]),
                    "golden_dev_source_text_not_inherited": len(not_inh),
                    "report_only_inherited_from_golden_train": inherited}, 0, "SPEC 7.2"))
    out.append(Sub("8.3", "6-word runs (instructions, options, yes/no lines) vs ship-split instructions, "
                          "dialogue_rebuttal, OHS-1/2, eval injected spans, v11 templates",
                   status(not hit["tmpl6_dev"] and not hit["tmpl6_v11"]),
                   {"dev": len(hit["tmpl6_dev"]), "v11": len(hit["tmpl6_v11"])}, 0, "CL:442, SPEC 7.3",
                   {"examples": (hit["tmpl6_dev"] + hit["tmpl6_v11"])[:6]}))
    nb, nb_info = load_neg_bench(ctx.opts.neg_manifest, ctx.log)
    if nb is None:
        out.append(Sub("8.4", "6-word runs vs public negation-benchmark frames", "FAIL", None, 0, "CL:284, CL:442",
                       nb_info))
    else:
        nbh = [R["row"]["id"] for R in ctx.R
               if {hash(x) for t in authored_texts(R["row"]) for x in cy.runs(t)} & nb]
        for i in nbh:
            drop["tmpl6_negbench"].add(lad_of(ctx.by_rowid[i]))
        out.append(Sub("8.4", "6-word runs vs public negation-benchmark frames (decontam-only manifest)",
                       status(not nbh and not nb_info["missing"]), len(nbh), "0 hits, every listed source loaded",
                       "CL:284, CL:288, CL:442", {**nb_info, "examples": nbh[:6]}))
    ff, nff = failure_frame_runs()
    ffh = [R["row"]["id"] for R in ctx.R if ff and set().union(*[cy.runs(t) for t in authored_texts(R["row"])]) & ff]
    for i in ffh:
        drop["failure_frame"].add(lad_of(ctx.by_rowid[i]))
    out.append(Sub("8.5", "measured-failure frame: no 6-word run of the failing devp_card questions; no dev / eval frame",
                   status(bool(ff) and not ffh and not hit["dev_eval_frame"]),
                   {"failure_questions": nff, "run_hits": len(ffh), "dev_eval_frame_hits": len(hit["dev_eval_frame"])},
                   0, "CL:285, CL:442", {"examples": (ffh + hit["dev_eval_frame"])[:6]}))
    frames = ohs3_frames()
    o3 = []
    if frames:
        rxs, fixed = [], set()
        for f in frames:
            parts = re.split(r"\{[^{}]*\}", f)
            rxs.append(re.compile(r"\s*(.+?)\s*".join(re.escape(p.strip()) for p in parts), re.I))
            for p in parts:
                t = re.findall(r"[a-z0-9]+", p.lower())
                fixed |= {tuple(t[i:i + OHS3_FRAME_RUN]) for i in range(len(t) - OHS3_FRAME_RUN + 1)}
        for R in ctx.R:
            ts = authored_texts(R["row"])
            rr = set()
            for t in ts:
                tk = re.findall(r"[a-z0-9]+", t.lower())
                rr |= {tuple(tk[i:i + OHS3_FRAME_RUN]) for i in range(len(tk) - OHS3_FRAME_RUN + 1)}
            if any(x.search(t) for x in rxs for t in ts) or rr & fixed:
                o3.append(R["row"]["id"])
                drop["ohs3_frame"].add(lad_of(R))
    out.append(Sub("8.6", "OHS-3 negation frames (read from build_ohs3.py TEXT): no frame match, no 5-word run of "
                          "their fixed text", status(bool(frames) and not o3),
                   {"frames_read": len(frames), "rows_hit": len(o3)}, 0, "SPEC 7 (held-out protection)",
                   {"examples": o3[:6]}))
    out.append(Sub("8.8", "no row id and no (state, instruction) pair of a reference row", status(not hit["id"] and
                                                                                               not hit["text_pair"]),
                   {"ids": len(hit["id"]), "pairs": len(hit["text_pair"])}, 0, "SPEC 7 / build_fix1"))
    if ctx.opts.unseen and ctx.opts.train_path:
        try:
            import check_unseen as cu
            rel = str(Path(ctx.opts.train_path).resolve().relative_to((LEAN / "data").resolve()))[:-len(".jsonl")]
            res = cu.check(rel)
            out.append(Sub("8.10", "SPEC 7.4 unseen set unchanged with the F7 train file (check_unseen)",
                           status(not res["problems"]), {"unseen_sources": res.get("unseen_sources"),
                                                         "unseen_rows": res.get("unseen_rows")}, "17 / 3,847, no problem",
                           "SPEC 7.4", res["problems"]))
        except Exception as e:  # noqa: BLE001
            out.append(Sub("8.10", "SPEC 7.4 unseen set unchanged with the F7 train file (check_unseen)", "FAIL", None,
                           "pass", "SPEC 7.4", f"error {e!r}"[:300]))
    else:
        out.append(Sub("8.10", "SPEC 7.4 unseen set unchanged with the F7 train file (check_unseen)", "PENDING", None,
                       "pass", "SPEC 7.4", "no train path under data/ (or --no-unseen)"))
    gp_ = golden_scan(ctx)["pairs"]
    gdup = []
    for R in ctx.R:
        if pair_key(R["row"]) in gp_:
            gdup.append(R["row"]["id"])
            drop["dedupe_golden"].add(lad_of(R))
    inlad = getattr(ctx, "dup_rows_in_ladder", None)
    if inlad is None:
        inlad = dup_rows_in_ladder(ctx)
    out.append(Sub("8.11", "SPEC 7.5 dedupe: no repeated (state, instruction) across ladders; no byte-identical row "
                           "inside a ladder; none equal to a golden_train row",
                   status(not dups and not gdup and not inlad),
                   {"within_f7": len(dups), "identical_row_in_same_ladder": len(inlad),
                    "equal_to_golden_train": len(gdup)}, 0,
                   "SPEC 7.5 (+ F7_OBJECTIONS.md A2)", {"examples": (dups + inlad + gdup)[:6]}))
    out.append(names_check(ctx))
    ctx.log(f"decontamination done ({time.time() - t0:.0f} s)")
    return out


def names_check(ctx):
    """SPEC 7.7 + 4.11: pool names in F7 text are not in JevBench public / OHS-1/2 text, and each part uses its pool."""
    import check_yn2b as cy
    try:
        gen3 = LEAN / "golden_src" / "gen3"
        if str(gen3) not in sys.path:
            sys.path.insert(0, str(gen3))
        import mv_core as mv
    except Exception as e:  # noqa: BLE001
        return Sub("8.12", "SPEC 7.7 names", "FAIL", None, "0", "SPEC 7.7", f"mv_core import failed {e!r}")
    pools = mv._pools()
    first = {n: s for s, p in pools.items() for n in p["first"]}
    last = {n: s for s, p in pools.items() for n in p["last"]}
    stems = {n: s for s, p in pools.items() for n in p["stem"]}
    want_split = {"train": "train", "iid": "dev_iid", "holdout": "dev_holdout", "devx": "devx"}
    used, wrong = set(), []
    for R in ctx.ok:
        if R["m"]["ladder_kind"] != "record":   # real texts carry real names; only program records use the pools
            continue
        text = " ".join([R["row"].get("state") or "", R["row"].get("instructions") or ""] +
                        [o for o in (R["row"].get("options") or []) if isinstance(o, str)])
        found = []
        for a, b in re.findall(r"\b([A-Z][a-z]+) ([A-Z][a-z]+)\b", text):
            if a in first and b in last:
                found.append((f"{a} {b}", {first[a], last[b]}))
        for st, code in re.findall(r"\b([A-Z][a-z]+) ([A-Z]-\d+)\b", text):   # item names: pool stem + a code
            if st in stems:
                found.append((f"{st} {code}", {stems[st]}))
        for nm, sp in found:
            used.add(nm)
            if sp != {want_split[R["an"]["dev_kind"]]}:
                wrong.append((R["row"]["id"], nm, sorted(sp)))
    hits = {"F7": heldout_name_hits(sorted(used))} if used else {}
    nh = sum(len(v) for v in hits.values())
    return Sub("8.12", "SPEC 7.7 / 4.11 names: pool names not in JevBench public or OHS-1/2 text; each part uses its own pool",
               status(not nh and not wrong), {"names_used": len(used), "found_in_heldout_text": nh,
                                              "wrong_pool": len(wrong)}, "0 / 0", "SPEC 7.7, SPEC 4.11",
               {"examples": [list(v)[:5] for v in hits.values()] + wrong[:5]})


def heldout_name_hits(names):
    """check_yn2b.name_check (non-strict: the name's word sequence inside JevBench public / OHS-1/2 text), with a word
    n-gram set instead of a substring scan per name."""
    import check_yn2b as cy
    sizes = {len(cy._words(n)) for n in names} - {0}
    grams = set()

    def add(text):
        w = cy._words(text)
        for k in sizes:
            for i in range(len(w) - k + 1):
                grams.add(" ".join(w[i:i + k]))
    for d in cy.BENCH_DIRS:
        p = LEAN.parent.parent / d
        for fp in sorted(p.glob("*.jsonl")) if p.exists() else []:
            with open(fp, encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        for s_ in cy.strings(json.loads(line)):
                            add(s_)
    for f_ in cy.OHS12:
        p = LEAN / "data" / f"{f_}.jsonl"
        if p.exists():
            with open(p, encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        r = json.loads(line)
                        for s_ in [r.get("state"), r.get("instructions"), r.get("card")] + list(r.get("options") or []):
                            if isinstance(s_, str):
                                add(s_)
    return [n for n in names if " ".join(cy._words(n)) in grams]


def ohs3_blind_counts(ctx):
    """OWNER ONLY (--ohs3-blind): check_yn2b.ohs3_blind, counts only. Build agents never pass this flag."""
    import check_yn2b as cy
    rows = []
    for R in ctx.R:
        r = dict(R["row"])
        r["meta"] = dict(r.get("meta") or {})
        r["meta"]["latent_id"] = (R["m"] or {}).get("ladder_id") or r.get("call_id")
        rows.append(r)
    units, hashes, names, loaded = cy.ohs3_blind(LEAN, rows, ())
    n = sum(units.values()) if isinstance(units, dict) else len(units or ())
    return Sub("8.13", "SPEC 7.1 OHS-3 12-gram check (counts only)", status(loaded and n == 0),
               {"hit_units": n, "loaded": loaded}, "0 hit units", "SPEC 7.1")


# ===================================================================================================== check 9: ladders
def check_ladders(ctx: Ctx):
    out = []
    bad_state, bad_call = [], []
    call_to_lad = defaultdict(set)
    for lid, rs in ctx.ladders.items():
        if len({R["row"].get("state") for R in rs}) != 1:
            bad_state.append(lid)
        calls = {R["row"].get("call_id") for R in rs}
        if len(calls) != 1:
            bad_call.append(lid)
        for c in calls:
            call_to_lad[c].add(lid)
    shared_calls = [c for c, s in call_to_lad.items() if len(s) > 1]
    out.append(Sub("9.1", "every ladder: byte-identical state, one call_id, call_id not shared with another ladder",
                   status(not bad_state and not bad_call and not shared_calls),
                   {"state": len(bad_state), "call_ids": len(bad_call), "shared_calls": len(shared_calls)}, "0 / 0 / 0",
                   "CL:205-207, CL:446", {"examples": (bad_state + bad_call + shared_calls)[:6]}))
    big = []
    for lid, rs in ctx.ladders.items():
        long_ = any(len(R["row"].get("state") or "") > LONG_STATE_CHARS for R in rs)
        lim = LADDER_MAX_ROWS_LONG if long_ else LADDER_MAX_ROWS
        tot = sum(len(R["row"].get("state") or "") for R in rs)
        if len(rs) > lim or tot > UNIT_STATE_MAX:
            big.append((lid, len(rs), tot))
    out.append(Sub("9.2", "ladder size: <= 5 rows (<= 3 if a state > 6K chars); unit state total <= 24K chars",
                   status(not big), len(big), 0, "CL:206-207, CL:447, SPEC 4.9", {"examples": big[:6]}))
    out.append(check_relations(ctx))
    r0 = {}
    for name, kinds, need in (("train", ("train",), R0_TRAIN_MIN), ("dev", ("iid", "holdout"), R0_DEV_MIN)):
        lads = [lid for lid, rs in ctx.ladders.items() if rs[0]["an"]["dev_kind"] in kinds]
        k = sum(1 for lid in lads if any(R["m"]["rung"] == "R0" for R in ctx.ladders[lid]))
        r0[name] = [k, len(lads), r3(k / len(lads)) if lads else None, need]
    ok = all(v[1] > 0 and v[0] / v[1] >= v[3] - 1e-12 for v in r0.values())
    out.append(Sub("9.4", "R0 anchor in >= 80% of train ladders and 100% of dev ladders", status(ok), r0,
                   {"train": R0_TRAIN_MIN, "dev": R0_DEV_MIN}, "CL:215, CL:449"))
    one = [lid for lid, rs in ctx.ladders.items()
           if len({R["row"]["gold"] for R in rs if R["an"]["yn"]}) < 2]
    out.append(Sub("9.5", "every ladder has a yes row and a no row", status(not one), len(one), 0, "CL:219, CL:450",
                   {"examples": one[:6]}))
    out.append(rung_semantics(ctx))
    split = [lid for lid, rs in ctx.ladders.items() if len({R["an"]["dev_kind"] for R in rs}) > 1]
    out.append(Sub("9.7", "all rows of a ladder on one side of the split (one dev_kind)", status(not split), len(split), 0,
                   "SPEC 4.2"))
    dec = []
    rows = [R for R in ctx.train]
    if rows:
        tot = Counter(R["an"]["depth"] for R in rows)
        for i in range(10):
            part = rows[i * len(rows) // 10:(i + 1) * len(rows) // 10]
            c = Counter(R["an"]["depth"] for R in part)
            dec.append({d: r3(c[d] / len(part)) if part else None for d in sorted(tot)})
    out.append(Sub("9.8", "no curriculum: depth shares per file decile (info; train_decoder shuffles units)", "PASS",
                   dec, "mixed", "CL:291", "information only: the trainer shuffles units every epoch"))
    return out


def check_relations(ctx):
    bad = Counter()
    ex = []
    comp = Counter()
    n = 0
    for part, rels in ctx.rels.items():
        for rel in rels:
            n += 1
            t, a, b = rel.get("type"), ctx.by_rowid.get(rel.get("a")), ctx.by_rowid.get(rel.get("b"))
            why = None
            if t not in ("complement", "equiv", "inv"):
                why = "type"
            elif a is None or b is None:
                why = "missing endpoint"
            elif not (a["an"]["ok"] and b["an"]["ok"]):
                why = "endpoint without valid meta"
            elif a["m"]["ladder_id"] != b["m"]["ladder_id"]:
                why = "across ladders"
            elif not (a["an"]["yn"] and b["an"]["yn"]):
                if a["an"]["yn"] or b["an"]["yn"] or a["row"]["options"] != b["row"]["options"]:
                    why = "choice endpoint (trainer skips cross-type; choice needs identical options)"
            elif a["an"]["core_sig"] != b["an"]["core_sig"]:
                why = "different core claim"
            else:
                same_par = (a["an"]["depth"] % 2) == (b["an"]["depth"] % 2)
                same_gold = a["row"]["gold"] == b["row"]["gold"]
                if t == "complement" and (same_par or same_gold):
                    why = "complement but same parity / gold"
                if t in ("equiv", "inv") and (not same_par or not same_gold):
                    why = f"{t} but different parity / gold"
            if t == "complement":
                comp[rel.get("a")] += 1
                comp[rel.get("b")] += 1
            if why:
                bad[why] += 1
                if len(ex) < 6:
                    ex.append((rel.get("a"), rel.get("b"), t, why))
    many = [k for k, v in comp.items() if v > 1]
    if many:
        bad["row in > 1 complement"] += len(many)
    return Sub("9.3", "relations match parity (equiv / inv = same parity and gold, complement = opposite), same core "
                      "claim, same ladder, <= 1 complement per row", status(not bad and n > 0), {"relations": n,
                                                                                                "bad": dict(bad)},
               "0 bad", "CL:217-218, CL:448", {"examples": ex})


def rung_semantics(ctx):
    bad = Counter()
    ex = []
    for lid, rs in ctx.ladders.items():
        for R in rs:
            m, an = R["m"], R["an"]
            rg = m["rung"]
            negc = [c for c in m["cues"] if c["cls"] != "lookalike"]
            qneg = [c for c in negc if c["position"] in QUESTION_POSITIONS]
            why = None
            if rg == "R0" and (an["depth"] != 0 or qneg):
                why = "R0 needs depth 0 and no negation cue in the question"
            elif rg in ("N1", "N2", "N3", "N4") and an["depth"] != int(rg[1]):
                why = f"{rg} but depth {an['depth']}"
            elif rg == "D":
                twin = [S for S in rs if S is not R and S["an"]["n_dist"] < an["n_dist"] and S["an"]["depth"] == an["depth"]
                        and S["an"]["yn"] == an["yn"] and S["an"]["gold_v"] == an["gold_v"]]
                if an["n_dist"] < 1:
                    why = "D without a distractor"
                elif not twin:
                    why = "D without its twin (same depth and gold, fewer distractors) in the ladder"
            elif rg == "AR":
                odd_sib = [S for S in rs if S is not R and S["an"]["depth"] % 2 == 1 and S["m"]["rung"] != "AR"
                           and S["an"]["gold_v"] == an["gold_v"]]
                if qneg or an["scoping"]:
                    why = "AR with a cue word"
                elif an["depth"] % 2 != 1 or not an["null_not"]:
                    why = "AR must be an odd flip with no cue word (NOT cue null)"
                elif not odd_sib:
                    why = "AR without an odd-depth sibling of the same gold"
            elif rg == "CH" and an["yn"]:
                why = "CH on a yes/no row"
            elif rg != "CH" and not an["yn"]:
                why = "choice row not marked CH"
            if why:
                bad[why] += 1
                if len(ex) < 6:
                    ex.append((R["row"]["id"], why))
    return Sub("9.6", "rung semantics: R0 / N1-N4 depth, D has a distractor and its twin, AR cue-less odd flip with an "
                      "odd sibling, CH = choice", status(not bad), dict(bad), "0", "CL:208-214", {"examples": ex})


# ===================================================================================================== check 10: hold-out
def class_multiset(R):
    return tuple(sorted(CLASS5[c["cls"]] for c in R["an"]["scoping"]))


def contains_multiset(big, small):
    cb, cs = Counter(big), Counter(small)
    return all(cb[k] >= v for k, v in cs.items())


def check_holdout(ctx: Ctx):
    out = []
    spec = ctx.opts.holdout_spec or {}
    tr, ho = ctx.train, ctx.hold
    lex_tr = {c["lexeme"].lower() for R in tr for c in R["m"]["cues"] if c["cls"] != "lookalike"}
    lex_ho = {c["lexeme"].lower() for R in ho for c in R["m"]["cues"] if c["cls"] != "lookalike"}
    cls_of = {c["lexeme"].lower(): CLASS5[c["cls"]] for R in ho for c in R["m"]["cues"] if c["cls"] != "lookalike"}
    H_lex = (lex_ho - lex_tr) | {x.lower() for x in spec.get("lexemes", [])}
    fam_tr = {R["m"]["frame_family"] for R in tr}
    fam_ho = {R["m"]["frame_family"] for R in ho}
    H_fam = (fam_ho - fam_tr) | set(spec.get("frame_families", []))
    fr_tr = {R["m"]["frame_id"] for R in tr}
    H_fr = ({R["m"]["frame_id"] for R in ho} - fr_tr) | set(spec.get("frame_ids", []))
    src_tr = {R["m"]["source"] for R in tr}
    H_src = ({R["m"]["source"] for R in ho if R["m"]["ladder_kind"] in ("card", "multitext")} - src_tr) | \
        set(spec.get("sources", []))
    ms_tr = [class_multiset(R) for R in tr]
    combos_ho = {class_multiset(R) for R in ho if R["an"]["depth"] == 3}
    H_combo = {c for c in combos_ho if not any(contains_multiset(b, c) for b in ms_tr)} | \
        {tuple(sorted(c)) for c in spec.get("cue_combos", [])}
    # 10.1 lexemes, meta + text (inflections) in F7-authored train text
    leak_meta = sorted(H_lex & lex_tr)
    rx = {k: lexeme_regex(k) for k in H_lex}
    leak_text = Counter()
    ex = []
    for R in tr:
        t = mask_quotes(" ".join(authored_texts(R["row"])))
        for k, r in rx.items():
            if r is not None and r.search(t):
                leak_text[k] += 1
                if len(ex) < 6:
                    ex.append((R["row"]["id"], k))
    out.append(Sub("10.1", "held-out lexemes (with inflections) in 0 train rows (meta and F7-authored text)",
                   status(not leak_meta and not leak_text), {"meta": len(leak_meta), "text_rows": sum(leak_text.values())},
                   0, "CL:268-270, CL:452", {"meta": leak_meta, "text": dict(leak_text), "examples": ex}))
    lk_f = sum(1 for R in tr if R["m"]["frame_family"] in H_fam or R["m"]["frame_id"] in H_fr)
    out.append(Sub("10.2", "held-out frame families and frames in 0 train rows", status(lk_f == 0), lk_f, 0,
                   "CL:269, CL:452"))
    lk_c = sum(1 for b in ms_tr if any(contains_multiset(b, c) for c in H_combo))
    out.append(Sub("10.3", "held-out depth-3 cue-class combinations never occur together in a train row", status(lk_c == 0),
                   lk_c, 0, "CL:271, CL:452", {"held_out_combos": sorted(H_combo)}))
    lk_s = sum(1 for R in tr if R["m"]["source"] in H_src)
    out.append(Sub("10.4", "held-out sources in 0 train rows", status(lk_s == 0), lk_s, 0, "CL:272, CL:452"))
    all_lex = lex_tr | lex_ho
    hc = Counter(cls_of.get(k, "?") for k in H_lex)
    need_cls = {"syntactic", "affixal", "lexical", "truth_frame", "cross+answer"}
    ok = (len(H_fam) >= HOLD_FAMILIES_MIN and len(H_lex) >= HOLD_LEXEMES_MIN and all_lex and
          len(H_lex) / len(all_lex) >= HOLD_LEXEME_SHARE_MIN - 1e-12 and need_cls <= set(hc) and
          len(H_combo) >= HOLD_COMBOS_MIN and len(H_src) >= HOLD_SOURCES_MIN)
    out.append(Sub("10.5", "hold-out size: >= 3 families, >= 15 lexemes = >= 20% (>= 1 per class), >= 2 depth-3 "
                           "combinations, >= 2 whole sources", status(ok),
                   {"families": len(H_fam), "lexemes": len(H_lex),
                    "lexeme_share": r3(len(H_lex) / len(all_lex)) if all_lex else None, "lexeme_classes": dict(hc),
                    "combos": len(H_combo), "sources": len(H_src)},
                   {"families": HOLD_FAMILIES_MIN, "lexemes": HOLD_LEXEMES_MIN, "share": HOLD_LEXEME_SHARE_MIN,
                    "combos": HOLD_COMBOS_MIN, "sources": HOLD_SOURCES_MIN}, "CL:268-272, CL:369",
                   {"H_families": sorted(H_fam), "H_lexemes": sorted(H_lex), "H_sources": sorted(H_src)}))
    out.append(dev_vs_train_12(ctx))
    import check_yn2b as cy
    trs = {cy.norm(R["row"].get("state")) for R in tr}
    iid_eq = sum(1 for R in ctx.iid if cy.norm(R["row"].get("state")) in trs)
    gids = lambda R: {R["row"].get("group_id"), (R["row"].get("meta") or {}).get("derived_group"),  # noqa: E731
                      (R["row"].get("meta") or {}).get("derived_from"), R["m"].get("group")} - {None}
    tr_g = set().union(*[gids(R) for R in tr]) if tr else set()
    gd = sum(1 for R in ctx.dev + ctx.devx if gids(R) & tr_g)
    out.append(Sub("10.7", "no iid dev state equals a train state; dev / devx group-disjoint from train",
                   status(iid_eq == 0 and gd == 0), {"iid_state_equal": iid_eq, "group_overlap_rows": gd}, "0 / 0",
                   "CL:376, CL:454"))
    if ctx.opts.fast:
        out.append(Sub("10.8", "dev / devx states are not golden_train states (golden_train is in the fix2 mix)", "SKIP",
                       None, 0, "CL:376", "--fast"))
    else:
        seen = golden_scan(ctx)["states"]
        n = sum(1 for R in ctx.dev + ctx.devx if sh8(R["row"].get("state")) in seen)
        out.append(Sub("10.8", "dev / devx states are not golden_train states (golden_train is in the fix2 mix)",
                       status(n == 0), n, 0, "CL:376 (train = the fix2 training mix)"))
    plain = []
    for lid, rs in ctx.ladders.items():
        if rs[0]["an"]["dev_kind"] != "holdout":
            continue
        has = False
        for R in rs:
            m = R["m"]
            if (m["frame_family"] in H_fam or m["frame_id"] in H_fr or m["source"] in H_src or
                    any(c["lexeme"].lower() in H_lex for c in m["cues"]) or class_multiset(R) in H_combo):
                has = True
                break
        if not has:
            plain.append(lid)
    out.append(Sub("10.9", "every holdout ladder carries at least one held-out element", status(not plain), len(plain), 0,
                   "CL:268-272", {"examples": plain[:6]}))
    return out


def dev_vs_train_12(ctx):
    import check_yn2b as cy
    dev = ctx.hold + ctx.devx
    dg = {}
    for R in dev:
        g = cy.grams(R["row"].get("state") or "")
        if g:
            dg[R["row"]["id"]] = g
    tg = set()
    for st in {R["row"].get("state") or "" for R in ctx.train}:
        tg |= cy.grams(st)
    worst, fails = 0.0, []
    for i, g in dg.items():
        s = len(g & tg) / len(g)
        worst = max(worst, s)
        if s > DEV_TRAIN_12G_MAX + 1e-12:
            fails.append(i)
    return Sub("10.6", "holdout / devx states share <= 20% of their 12-grams with train states (union)",
               status(not fails), {"rows_over": len(fails), "max_share": r3(worst), "checked": len(dg)},
               f"<= {DEV_TRAIN_12G_MAX}", "CL:453, SPEC 7.6", {"examples": fails[:6]})


# ===================================================================================================== check 11: blind read
def blind_sample(ctx, n_random=BLIND_RANDOM, per_must=BLIND_PER_MUST, seed=20261001):
    rng = random.Random(seed)
    pool = sorted(ctx.ok, key=lambda R: R["row"]["id"])
    pick = {R["row"]["id"]: R for R in rng.sample(pool, min(n_random, len(pool)))}
    for it, pr in PRIORITY.items():
        if pr != "MUST":
            continue
        tagged = [R for R in pool if it in R["m"]["phen"] and R["row"]["id"] not in pick]
        for R in rng.sample(tagged, min(per_must, len(tagged))):
            pick[R["row"]["id"]] = R
    return [{"id": R["row"]["id"], "state": R["row"].get("state"), "card": R["row"].get("card"),
             "instructions": R["row"].get("instructions"), "options": R["row"].get("options")}
            for R in pick.values()]


def check_blind(ctx: Ctx):
    b = ctx.opts.blind
    if b is None:
        return [Sub("11.1", "blind read: 0 wrong gold, unreadable + ambiguous <= 3% (100 random + 10 per MUST item)",
                    "PENDING", None, "0 wrong, <= 3%", "CL:455-458", "no --blind-read given")]
    v = Counter(x.get("verdict") for x in b)
    n = len(b)
    ids = {x.get("id") for x in b}
    must_cov = {it: sum(1 for i in ids if i in ctx.by_rowid and ctx.by_rowid[i]["m"] and it in ctx.by_rowid[i]["m"]["phen"])
                for it, pr in PRIORITY.items() if pr == "MUST"}
    short = {k: c for k, c in must_cov.items() if c < BLIND_PER_MUST}
    bad = (v["unreadable"] + v["ambiguous"]) / n if n else 1
    ok = n >= BLIND_RANDOM and v["wrong_gold"] == 0 and bad <= BLIND_BAD_MAX + 1e-12 and not short
    return [Sub("11.1", "blind read: 0 wrong gold, unreadable + ambiguous <= 3% (100 random + 10 per MUST item)",
                status(ok), {"rows": n, "verdicts": dict(v), "bad_share": r3(bad), "must_items_short": short},
                "0 wrong, <= 3%", "CL:455-458")]


# ===================================================================================================== run
CHECKS = [("1", "schema", check_schema), ("2", "gold", check_gold), ("3", "coverage", check_coverage),
          ("4", "balance", check_balance), ("5", "surface shortcut probes", check_probes),
          ("6", "composition probes", check_composition), ("7", "EXCLUDE scan", check_exclude),
          ("8", "decontamination", check_decontam), ("9", "ladder integrity", check_ladders),
          ("10", "hold-out integrity", check_holdout), ("11", "blind read", check_blind)]


def run_checks(ctx: Ctx, only=None):
    res = {}
    for num, name, fn in CHECKS:
        if only and num not in only:
            continue
        t0 = time.time()
        try:
            subs = fn(ctx)
        except Exception as e:  # noqa: BLE001  (a crashing check is a FAIL, never a silent pass)
            import traceback
            subs = [Sub(f"{num}.E", f"{name} crashed", "FAIL", None, None, "", traceback.format_exc()[-1500:])]
        res[num] = {"name": name, "subs": subs, "seconds": round(time.time() - t0, 1)}
        ctx.log(f"check {num} {name}: {Counter(s.status for s in subs)} ({time.time() - t0:.1f} s)")
    return res


def overall(subs):
    st = {s.status for s in subs}
    return "FAIL" if "FAIL" in st else ("PENDING" if st & {"PENDING", "SKIP"} else "PASS")


def fmt_val(v, w=70):
    s = json.dumps(v, default=str) if not isinstance(v, str) else v
    return s if len(s) <= w else s[:w - 3] + "..."


def print_table(res):
    lines = []
    for num, r in res.items():
        lines.append(f"== {num:>2} {r['name']}: {overall(r['subs'])}")
        for s in r["subs"]:
            lines.append(f"   {s.id:<7} {s.status:<7} {s.name[:88]:<88} {fmt_val(s.value)}")
    return "\n".join(lines)


def load_rows(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def default_rel(p):
    p = Path(p)
    if p.name.endswith("_train.jsonl"):
        return p.with_name(p.name[:-len("_train.jsonl")] + "_relations.jsonl")
    return p.with_name(p.name[:-len(".jsonl")] + "_relations.jsonl")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load_preds(path):
    p = Path(path)
    txt = p.read_text()
    try:
        obj = json.loads(txt)
        if isinstance(obj, dict) and set(obj) == {"id", "gold"}:
            return {obj["id"]: obj["gold"]}
        if isinstance(obj, dict):
            return {k: v for k, v in obj.items()}
        return {x["id"]: x["gold"] for x in obj}
    except json.JSONDecodeError:
        return {x["id"]: x["gold"] for x in (json.loads(l) for l in txt.splitlines() if l.strip())}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    D = "data/v14_parts/"
    ap.add_argument("--train", default=D + "f7_train.jsonl")
    ap.add_argument("--probe", default=D + "f7_probe.jsonl")
    ap.add_argument("--devx", default=D + "f7_devx.jsonl")
    ap.add_argument("--train-rel", default=None)
    ap.add_argument("--probe-rel", default=None)
    ap.add_argument("--devx-rel", default=None)
    ap.add_argument("--meta", nargs="+", default=[D + "f7_meta.jsonl", D + "f7_probe_meta.jsonl", D + "f7_devx_meta.jsonl"])
    ap.add_argument("--fast", action="store_true", help="skip the slow probes and the reference-set decontamination")
    ap.add_argument("--budget", choices=("full", "minimum"), default="full")
    ap.add_argument("--decide2-preds", default=None, help="JSONL {id, gold} or JSON {id: gold} from the independent decide2")
    ap.add_argument("--decide2-code", nargs="*", default=[])
    ap.add_argument("--decide2-independent", choices=("yes", "no", "unknown"), default="unknown")
    ap.add_argument("--generator-code", nargs="*", default=["golden_src/gen3/gen3_nested_negation.py",
                                                            "golden_src/gen3/nn_lexicon.py"])
    ap.add_argument("--blind-read", default=None)
    ap.add_argument("--write-blind-sample", default=None)
    ap.add_argument("--holdout-spec", default=None)
    ap.add_argument("--lexicon", default=None)
    ap.add_argument("--golden-train", default=D + "golden_train.jsonl")
    ap.add_argument("--neg-manifest", default="yn2b/decontam_only/negation_benchmarks.json")
    ap.add_argument("--no-unseen", action="store_true")
    ap.add_argument("--ohs3-blind", action="store_true", help="OWNER ONLY: OHS-3 12-gram counts (opens OHS-3)")
    ap.add_argument("--only", nargs="*", default=None, help="check numbers to run (default all)")
    ap.add_argument("--out", default="yn2b/f7_precheck.json")
    a = ap.parse_args(argv)
    t0 = time.time()
    log = lambda s: print(f"[{time.time() - t0:6.1f}s] {s}", flush=True)  # noqa: E731
    parts, rels, metas, inputs = {}, {}, [], {}
    for part, path, rp in (("train", a.train, a.train_rel), ("probe", a.probe, a.probe_rel), ("devx", a.devx, a.devx_rel)):
        p = LEAN / path
        if not p.exists():
            log(f"{part}: {path} not found (the part is empty)")
            parts[part] = []
            continue
        parts[part] = load_rows(p)
        inputs[path] = sha(p)
        rpath = LEAN / (rp or default_rel(path))
        if rpath.exists():
            rels[part] = load_rows(rpath)
            inputs[str(Path(rp or default_rel(path)))] = sha(rpath)
        else:
            rels[part] = []
            log(f"{part}: no relations file {rpath.relative_to(LEAN) if rpath.is_relative_to(LEAN) else rpath}")
    for mp in a.meta:
        p = LEAN / mp
        if p.exists():
            metas += load_rows(p)
            inputs[mp] = sha(p)
        else:
            log(f"sidecar {mp} not found")
    opts = Opts(budget=a.budget, fast=a.fast, decide2_code=a.decide2_code, decide2_independent=a.decide2_independent,
                generator_code=a.generator_code, golden_train=a.golden_train, neg_manifest=a.neg_manifest,
                ohs3_blind=a.ohs3_blind, train_path=str(LEAN / a.train) if parts.get("train") else None,
                unseen=not a.no_unseen)
    if a.decide2_preds:
        opts.decide2_preds = load_preds(LEAN / a.decide2_preds)
        inputs[a.decide2_preds] = sha(LEAN / a.decide2_preds)
    if a.blind_read:
        opts.blind = load_rows(LEAN / a.blind_read) if a.blind_read.endswith(".jsonl") else \
            json.loads((LEAN / a.blind_read).read_text())
    if a.holdout_spec:
        opts.holdout_spec = json.loads((LEAN / a.holdout_spec).read_text())
    if a.lexicon:
        opts.lexicon = json.loads((LEAN / a.lexicon).read_text())
    log(f"rows: { {k: len(v) for k, v in parts.items()} }, sidecar entries {len(metas)}, relations "
        f"{ {k: len(v) for k, v in rels.items()} }")
    ctx = Ctx(parts, metas, rels, opts, log=log)
    log(f"rows with valid meta: {len(ctx.ok)} / {len(ctx.R)} (train {len(ctx.train)}, iid {len(ctx.iid)}, holdout "
        f"{len(ctx.hold)}, devx {len(ctx.devx)})")
    if a.write_blind_sample:
        smp = blind_sample(ctx)
        Path(LEAN / a.write_blind_sample).write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in smp))
        log(f"blind sample: {len(smp)} rows without gold -> {a.write_blind_sample}")
    res = run_checks(ctx, set(a.only) if a.only else None)
    table = print_table(res)
    print(table)
    allsubs = [s for r in res.values() for s in r["subs"]]
    verdict = overall(allsubs)
    summ = Counter(s.status for s in allsubs)
    report = {"tool": "yn2b/f7_precheck.py", "checklist": CHECKLIST, "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                                                                       time.gmtime()),
              "args": vars(a), "inputs_sha256": inputs, "seconds": round(time.time() - t0, 1),
              "rows": {k: len(v) for k, v in parts.items()}, "rows_with_valid_meta": len(ctx.ok),
              "verdict": verdict, "status_counts": dict(summ),
              "checks": {num: {"name": r["name"], "status": overall(r["subs"]), "seconds": r["seconds"],
                               "subs": [s.__dict__ for s in r["subs"]]} for num, r in res.items()}}
    outp = LEAN / a.out
    outp.write_text(json.dumps(report, indent=1, default=str, ensure_ascii=False))
    print(f"\nf7_precheck: {verdict} ({dict(summ)}) in {time.time() - t0:.0f} s -> {a.out}")
    return 1 if verdict == "FAIL" else (2 if verdict == "PENDING" else 0)


if __name__ == "__main__":
    sys.exit(main())
