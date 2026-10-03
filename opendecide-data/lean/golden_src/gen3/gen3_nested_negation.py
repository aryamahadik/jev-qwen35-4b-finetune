"""gen3_nested_negation (F7 v2): family F7 'nested negation' rebuilt to the coverage checklist.

Why: C1 = q35_4b_main500k drops one negation in double- and triple-negated questions (ship constraint (e)). F7 is the
fix2 top-up family. v2 rebuilds F7 to yn2b/F7_COVERAGE_CHECKLIST.md (items 1-38, section 2 rules, section 3 targets,
section 4 audit = yn2b/f7_precheck.py). v1 is kept in data/v14_parts/f7_v1_backup/.

Design (checklist section 2):
  * LF first. Every row is built from a typed logical form (LF) tree; gold = the tree evaluated on the latent facts.
    The text is rendered from the tree's layers; gold is never computed from the surface text. Each cue records its
    lexeme, class, position, scope flag, distance and surface word.
  * Ladders. One ladder = one call_id with <= 5 rows on a byte-identical state: R0 (anchor, no cue), N1-N4 (scoping
    depth), D (a distractor twin of a sibling), AR (affirmative rewrite: a cue-less flip), CH (choice row).
  * Twin ladders. Ladders come in pairs with the SAME rung plan, instruction, card and options and OPPOSITE truth(P)
    (only the state differs: another real text, another text set, or a minimal edit of a program record). So no
    surface feature of the question predicts the gold, and every stratum of the audit is balanced by construction.
  * Kinds. card (one real classification text with its human gold, F4(a) eligibility, >= 50% of train ladders),
    multitext (3-5 real labelled texts, quantifier items 26-31, 10-20%), record (program-written records).
  * Relations. dev: equiv = same gold (same parity), complement = opposite gold; train: R0 -> same-gold rows 'inv'
    (a = R0, one-way KL), R0 <-> one opposite-gold row 'complement', <= 1 complement per row. A train ladder WITHOUT
    an R0 (at most 20%) has no affirmative anchor, so its same-gold rows are 'equiv' (symmetric; checklist 2.2), never
    'inv' with a negated row as the stop-gradient teacher (r6, golden_src/gen3/f7_repair_r6.py).
  * Items 28 (numeric bounds WITH negation) and 30 (De Morgan: not both / neither-nor / not (A or B)) count toward
    their floors only on rows with a scoping negation (depth >= 1); their unnegated R0 anchors keep the tag (r6).
  * Depth 4 is at most 3% of the rows of every part, train and dev (checklist item 9; r6).
  * Held out (dev_holdout): whole sources (civil_comments + toxic_conv, gd_saferproducts_severity,
    gd_wiki_help_routing), 3 frame families, 17 lexemes (>= 1 per class), 2 depth-3 cue-class combinations.
  * Dev texts are never golden_train / golden_dev states (fresh raw texts, old-pool toxicity texts not in golden).
  * Selection: a pool of 2.3x (train) / 4.5x (dev) twin pairs, then a swap search under the audit's thresholds, then
    the audit itself in the loop (see the 'pair selection' section).
  * r4 (blind-read repair, yn2b/F7_BLIND_READ.md): every disagreement came from a card line or a human label, never
    from the negation. So: a real text is kept only when it shows its human label the way the card defines it
    (label_evidence, nn_lexicon.py section 4b, same rule for train and dev); sources whose labels a careful reader
    cannot recover are retired (nn_lexicon.RETIRED_SOURCES); a residual card says the label may be off the card and
    never lists a label near the left-off one; derived terms are defined over the subject's noun; frame nos5 is
    retired; card-less rows define every term they use.
Labels are program-made. No model is called. CPU only. OHS-3 is never opened.

Outputs (data/v14_parts/): f7_train.jsonl, f7_relations.jsonl, f7_meta.jsonl, f7_probe.jsonl (iid + holdout),
f7_probe_relations.jsonl, f7_probe_meta.jsonl, f7_defs.json, f7_counts.json, f7_lexicon.json, f7_holdout_spec.json.

  cd opendecide-data/lean && PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python golden_src/gen3/gen3_nested_negation.py \
      --write --overwrite
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import pickle
import random
import re
import sys
import time
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
for _p in (HERE, LEAN, LEAN / "yn2b", LEAN / "extra"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
sys.dont_write_bytecode = True
import mv_core as mv  # noqa: E402
import nn_lexicon as lx  # noqa: E402
from build_v13_breadth import cid  # noqa: E402

KEY = "gen3_nested_negation"
SOURCE = "gd_gen3_nested_negation"
FAMILY = "F7"
GENERATOR = "golden_src/gen3/gen3_nested_negation.py"
VERSION = "v2"
REVISION = "r4"   # r1: round-1 repairs of yn2b/F7_OBJECTIONS.md (D1, decide2 findings #1-#6, A1, A2);
#                   r3: arbiter round 3 A3 (exceptive inclusion) and A4 ('opposite' / 'reverse' defined in the card);
#                   r4: blind-read repair (yn2b/F7_BLIND_READ.md): residual rule line + near labels, label-evidence
#                       rules per source, retired sources, frame nos5 retired, term nouns, defined complement terms
SEED = 20261001 + 70
DATA = LEAN / "data"
GOLD_TRAIN = "v14_parts/golden_train.jsonl"
GOLD_TRAIN_SHA = "ff7a395bc9b501ac27949ed7265b771e720406fa96f0e296700c2c101f62a2a9"
GOLD_DEV = "v14_parts/golden_dev.jsonl"
KNOWN_BAD = LEAN / "yn2b/label_audit_known_bad_ids.json"
OUT = {"train": "v14_parts/f7_train.jsonl", "train_rel": "v14_parts/f7_relations.jsonl",
       "train_meta": "v14_parts/f7_meta.jsonl", "probe": "v14_parts/f7_probe.jsonl",
       "probe_rel": "v14_parts/f7_probe_relations.jsonl", "probe_meta": "v14_parts/f7_probe_meta.jsonl",
       "defs": "v14_parts/f7_defs.json", "counts": "v14_parts/f7_counts.json",
       "lexicon": "v14_parts/f7_lexicon.json", "holdout_spec": "v14_parts/f7_holdout_spec.json"}
DEV_LABEL_SPLITS = ("dev_nc", "taskbank_dev", "hard_dev", "dev_negwords", "dev_claims", "pg_dev", "devzs", "devp_card",
                    "dev", "devzs2", "debate_dev", "hard12_dev", "proc12_dev", "planted12_dev", "dev_hc")
OLD_TOXIC_FILES = ("train_v05", "train_v06", "train_v06s", "train_v07", "train_v08s2", "train_v09s3", "train_v10s4",
                   "train_v11", "train_v11b", "train_v11c", "train_2b", "train_pilot", "train", "train_v13t",
                   "train_4b_v12t", "train_prism_arms")
MAX_STATE = 4800          # 5 rows x 4,800 chars <= 24K per unit (SPEC 4.9); no state > 6K
MAX_MULTI_TEXT = 1100     # one text inside a multi-text state
# ---- sizes (checklist section 3: ~2,500 train ladders, ~11-12K rows; dev >= 150 iid + >= 150 holdout ladders)
N_PAIRS = {"train": 1260, "iid": 120, "holdout": 130}
POOL_FACTOR = {"train": 2.3, "iid": 4.5, "holdout": 4.5}
SELECT_ITERS = {"train": 400000, "iid": 150000, "holdout": 150000}
KIND_SHARE = {"card": 0.53, "multitext": 0.17, "record": 0.30}       # card >= 50%, multitext 10-20% (CL:364)
# ---- targets the planner steers to (checklist section 3)
DEPTH_TARGET = {0: 0.18, 1: 0.25, 2: 0.30, 3: 0.245, 4: 0.025}
CLASS_TARGET = {"syntactic": 0.30, "affixal": 0.25, "lexical": 0.25, "truth_frame": 0.125, "cross+answer": 0.072}
POS_TARGET = {"inner_claim": 0.30, "outer_frame": 0.25, "card_def": 0.215, "separate_sentence": 0.066,
              "yn_key+answer_map": 0.066, "choice_option": 0.066}
NOT_NT_CAP = 0.175
R0_SHARE = 0.805
CH_SHARE_TARGET = 0.232
CHOICE_OPT_TARGET = 0.07
DEPTH_PULL = 1500.0       # weight of the depth deficit when a free N-rung picks its depth with its combo
KIND_SHARE_DEV = {"card": 0.5, "multitext": 0.22, "record": 0.28}
ALLOWED_CELLS = {"outer_frame": ("syntactic", "lexical", "truth_frame"),
                 "inner_claim": ("syntactic", "affixal", "lexical"),
                 "card_def": ("syntactic", "affixal", "lexical"),
                 "yn_key": ("answer_mapping",), "answer_map": ("answer_mapping",),
                 "separate_sentence": ("cross_sentence",), "choice_option": ("syntactic", "affixal", "lexical")}
FLOORS = {"MUST": (400, 40, 20), "SHOULD": (150, 20, 10), "NICE": (40, 10, 5)}
PRIORITY = {1: "MUST", 2: "MUST", 3: "MUST", 4: "MUST", 5: "MUST", 6: "MUST", 7: "SHOULD", 8: "MUST", 9: "NICE",
            10: "MUST", 11: "MUST", 12: "MUST", 13: "MUST", 14: "SHOULD", 15: "MUST", 16: "MUST", 17: "SHOULD",
            18: "SHOULD", 19: "SHOULD", 20: "SHOULD", 21: "MUST", 22: "MUST", 23: "SHOULD", 24: "MUST", 25: "NICE",
            26: "SHOULD", 27: "MUST", 28: "SHOULD", 29: "NICE", 30: "SHOULD", 31: "SHOULD", 32: "SHOULD", 33: "SHOULD",
            34: "SHOULD", 35: "SHOULD", 36: "MUST", 37: "SHOULD", 38: "SHOULD"}
QUESTION_POSITIONS = ("outer_frame", "inner_claim", "separate_sentence", "answer_map", "choice_option")
STATE_NEG_RE = re.compile(r"\b(?:not|no|never|none|nothing|nobody|nowhere|neither|nor|without|cannot)\b|n't\b", re.I)
HOLD_COMBOS = (("affixal", "cross+answer", "truth_frame"), ("cross+answer", "lexical", "truth_frame"))
DEPTH1_ITEMS = (28, 30)   # CL:136 'numeric bounds WITH negation', CL:141 De Morgan: floors count depth >= 1 rows only


def h8(s: str) -> bytes:
    return hashlib.blake2b((s or "").encode(), digest_size=8).digest()


def cap1(s: str) -> str:
    return s[:1].upper() + s[1:] if s else s


def low1(s: str) -> str:
    """Lower-case the first letter unless the first word is a name/label (all-caps token or a quote)."""
    if not s or s[0] in "'\"":
        return s
    w = s.split(" ", 1)[0]
    if len(w) > 1 and (w.isupper() or any(c.isdigit() for c in w)):
        return s
    return s[:1].lower() + s[1:]


DELIM_QUOTE_RE = re.compile(r"(?:(?<=[\s(])|^)'([^'\n]{1,80}?)'(?=[\s?.,;:!)]|$)")


def unquote(t: str) -> str:
    """Quote marks used as delimiters ('cleared' -> cleared) removed; apostrophes inside words kept (others' need,
    the partner's situation)."""
    return DELIM_QUOTE_RE.sub(r"\1", t)


def a_an(text: str, noun: str) -> str:
    """'a' -> 'an' before a document noun that starts with a vowel sound ('an attendance sheet', 'an action')."""
    if not noun or noun[0].lower() not in "aeio":
        return text
    return re.sub(r"\b([Aa]) (?=" + re.escape(noun) + r"\b)", lambda m: m.group(1) + "n ", text)


def fill(tpl: str, **kw) -> str:
    out = tpl
    for k, v in kw.items():
        out = out.replace("{" + k + "}", str(v))
    if re.search(r"\{[a-zA-Z_]+\}", out):
        raise ValueError(f"unfilled slot in {out!r}")
    return out


# ============================================================================================ LF helpers
def ATOM(aid, val):
    return {"op": "ATOM", "id": aid, "val": bool(val)}


def NOT(child, cue):
    return {"op": "NOT", "cue": cue, "child": child}


def DIST(child, cue):
    return {"op": "DIST", "cue": cue, "child": child}


def CORE(child):
    return {"op": "CORE", "child": child}


def lf_eval(n):
    op = n["op"]
    if op == "ATOM":
        return n["val"]
    if op == "NOT":
        return not lf_eval(n["child"])
    if op in ("DIST", "CORE"):
        return lf_eval(n["child"])
    if op == "AND":
        return all(lf_eval(c) for c in n["children"])
    if op == "OR":
        return any(lf_eval(c) for c in n["children"])
    s = sum(1 for c in n["children"] if lf_eval(c))
    if op == "ATLEAST":
        return s >= n["k"]
    if op == "ATMOST":
        return s <= n["k"]
    if op == "EXACTLY":
        return s == n["k"]
    raise ValueError(op)


def lf_core(n):
    """The CORE node of a single-CORE tree, and the number of NOT nodes above it."""
    def rec(x, d):
        if x["op"] == "CORE":
            return x, d
        for c in ([x["child"]] if "child" in x else []) + list(x.get("children") or []):
            r = rec(c, d + (1 if x["op"] == "NOT" else 0))
            if r:
                return r
        return None
    return rec(n, 0)


def set_atoms(n, vals: dict):
    """A copy of the tree with every ATOM's val taken from vals[id]."""
    n = dict(n)
    if n["op"] == "ATOM":
        n["val"] = bool(vals[n["id"]])
        return n
    if "child" in n:
        n["child"] = set_atoms(n["child"], vals)
    if "children" in n:
        n["children"] = [set_atoms(c, vals) for c in n["children"]]
    if "options" in n:
        n["options"] = [set_atoms(c, vals) for c in n["options"]]
    return n


# ============================================================================================ balancing helper
class Bal:
    """Deficit counters: least(key, choices) = the least-used choice (ties by rng)."""

    def __init__(self, rng):
        self.rng = rng
        self.c = Counter()

    def least(self, key, choices, w=None):
        w = w or {}
        m = min(self.c[(key, x)] / w.get(x, 1.0) for x in choices)
        x = self.rng.choice([x for x in choices if self.c[(key, x)] / w.get(x, 1.0) == m])
        self.c[(key, x)] += 1
        return x


# ============================================================================================ dev names and sources
def dev_label_names(root: Path = LEAN) -> set:
    """Every option name of every dev split (lower case): no F7 card label or quoted label may be one of them."""
    out = set()
    for sp in DEV_LABEL_SPLITS:
        with open(root / "data" / f"{sp}.jsonl", encoding="utf-8") as f:
            for line in f:
                r = json.loads(line)
                if r.get("qtype") == "choice":
                    out.update(o.strip().lower() for o in r.get("options") or [] if isinstance(o, str))
    return out


def dev_source_names(root: Path = LEAN) -> set:
    """Sources of every dev split, re-derived by program at build time (CL:222-223)."""
    import check_yn2b as cy
    names = set()
    for sp in set(DEV_LABEL_SPLITS) | set(cy.SHIP_SPLITS):
        p = root / "data" / f"{sp}.jsonl"
        if p.exists():
            with open(p, encoding="utf-8") as f:
                for line in f:
                    m = re.search(r'"source":\s*"([^"]+)"', line)
                    if m:
                        names.add(m.group(1))
    return names


def source_is_dev(src: str, dev_names: set) -> list:
    """gate_dev.source_seen in both directions plus token containment of the core name (gd_/br_/tb_/std_ stripped)."""
    import gate_dev
    core = lambda x: re.sub(r"^(?:gd|br|tb|std)_", "", x.lower())  # noqa: E731
    cs = core(src)
    hits = []
    for d in dev_names:
        cd = core(d)
        if (gate_dev.source_seen(d, {src}) or gate_dev.source_seen(src, {d})
                or (len(cd) >= 3 and len(cs) >= 3 and (re.search(r"(?:^|_)" + re.escape(cd) + r"(?:_|$)", cs)
                                                      or re.search(r"(?:^|_)" + re.escape(cs) + r"(?:_|$)", cd)))):
            hits.append(d)
    return sorted(hits)


def state_format(s):
    s = (s or "").lstrip()
    if s.startswith(("{", "[")):
        return "json"
    lines = [ln for ln in s.split("\n") if ln.strip()]
    if sum(1 for ln in lines if ln.strip().startswith("|")) >= 2:
        return "md_table"
    if lines and sum(1 for ln in lines if ln.strip().startswith(("- ", "* "))) >= max(2, len(lines) // 2):
        return "bullets"
    if len(lines) >= 3 and len({ln.count(",") for ln in lines[:5]}) == 1 and lines[0].count(",") >= 2:
        return "csv"
    if len(lines) >= 3 and sum(1 for ln in lines if re.match(r"^[\w .-]{1,30}:\s", ln)) >= len(lines) // 2:
        return "key_value"
    return "prose"


# ============================================================================================ decontamination refs
class Decon:
    """build_fix1's reference sets and frame regexes + the F7 bans + the measured-failure frame + OHS-3 frame text."""

    def __init__(self, log=print):
        import build_fix1 as bf
        import check_yn2b as cy
        self.bf, self.cy = bf, cy
        self.R = bf.load_refs(log)
        self.strict_all = self.R["strict"] | self.R["infam_y"]
        self.infam = self.R["infam"]
        self.rx = bf.frame_regexes()
        self.fail_runs = failure_frame_runs()
        self.ohs3_runs, self.ohs3_rx = ohs3_frame_runs()
        log(f"decon: measured-failure 6-word runs {len(self.fail_runs)}, OHS-3 frame 5-word runs {len(self.ohs3_runs)}")

    def text_ok(self, text, inherited=False):
        g = self.cy.row_ghash(text)
        if g & self.strict_all:
            return False
        if not inherited and g & self.infam:
            return False
        return not self.bf.frame_hits({"state": text}, self.rx)

    def authored_hits(self, texts):
        """Reasons an F7-authored text (instruction, option, yes/no line, card line) is banned."""
        cy = self.cy
        why = []
        for t in texts:
            if not t:
                continue
            g = cy.row_ghash(t)
            if g & self.strict_all or g & self.infam:
                why.append("12gram")
            r6 = cy.runs(t)
            if r6 & self.R["t6_dev"]:
                why.append("tmpl6_dev")
            if r6 & self.R["t6_v11"]:
                why.append("tmpl6_v11")
            if r6 & self.fail_runs:
                why.append("failure_frame")
            tk = re.findall(r"[a-z0-9]+", t.lower())
            if {tuple(tk[i:i + 5]) for i in range(len(tk) - 4)} & self.ohs3_runs or any(x.search(t) for x in self.ohs3_rx):
                why.append("ohs3_frame")
            if cy.BANNED_RE.search(t):
                why.append("banned_word")
            if lx.banned_hits(t):
                why.append("f7_ban")
        return why


def failure_frame_runs():
    """6-word runs of the measured-failure dev questions (devp_card hate pairs: 'contains only non-hateful content')."""
    import check_yn2b as cy
    runs = set()
    with open(DATA / "devp_card.jsonl", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r.get("source") == "hate" and "hateful" in (r.get("instructions") or ""):
                runs |= cy.runs(r["instructions"])
    return runs


def ohs3_frame_runs():
    """OHS-3's negation frames, read from the TEXT of build_ohs3.py (code, never OHS-3 data): their fixed text at
    5-word runs, and a regex per frame."""
    import ast
    p = LEAN / "build_ohs3.py"
    frames = []
    if p.exists():
        tree = ast.parse(p.read_text())
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "NEG_FRAMES" for t in node.targets):
                frames = [f for _, f in ast.literal_eval(node.value)]
    runs, rxs = set(), []
    for f in frames:
        parts = re.split(r"\{[^{}]*\}", f)
        rxs.append(re.compile(r"\s*(.+?)\s*".join(re.escape(x.strip()) for x in parts), re.I))
        for x in parts:
            t = re.findall(r"[a-z0-9]+", x.lower())
            runs |= {tuple(t[i:i + 5]) for i in range(len(t) - 4)}
    return runs, rxs


# ============================================================================================ text pools
def _vote_teacher(m) -> bool:
    t = m.get("teacher")
    return isinstance(t, dict) and bool(t) and m.get("teacher_src") is None


_G8_TOK = re.compile(r"[a-z0-9]+")


def word_8grams(text):
    """Word 8-grams of a text, tokenised as yn2b/f7_devx_pool_scan.py does (a text under 8 words is one gram)."""
    t = _G8_TOK.findall((text or "").lower())
    if len(t) < 8:
        return {" ".join(t)} if t else set()
    return {" ".join(t[i:i + 8]) for i in range(len(t) - 7)}


def load_pools(D: Decon, log=print):
    """All texts F7 may use, keyed by pool: {('card'|'prop'|'multi', source key, split): [base]}. Train pools come from
    golden_train under F4(a) eligibility (no vote-share teacher, no gold_probs, roles choice / aff, not renamed, not a
    known-bad id, not a dev source). Dev pools come from texts that are in neither golden_train nor golden_dev
    (data/v14_parts/raw files and, for the toxicity source, the older training files), never a devx state."""
    t0 = time.time()
    bad_ids = set(json.loads(KNOWN_BAD.read_text())["all_ids"])
    gold_states, dev_states = set(), set()
    with open(DATA / GOLD_DEV, encoding="utf-8") as f:
        for line in f:
            dev_states.add(h8(json.loads(line)["state"]))
    devx_states = set()
    devx_g8 = set()
    px = DATA / "v14_parts" / "f7_devx.jsonl"
    if px.exists():
        with open(px, encoding="utf-8") as f:
            for line in f:
                st = json.loads(line)["state"]
                devx_states.add(h8(st))
                devx_g8 |= word_8grams(st)
    # which golden source feeds which pool
    by_golden = defaultdict(list)
    for k, s in lx.CARD_SOURCES.items():
        if s["golden"]:
            by_golden[s["golden"]].append(("card", k, s))
    for k, s in lx.PROP_SOURCES.items():
        if s.get("golden"):
            by_golden[s["golden"]].append(("prop", k, s))
    oiics_g, oiics_raw, oiics_instr = lx.MULTI_GOLDEN["oiics"]
    by_golden[oiics_g].append(("oiics", "oiics", {"instr": oiics_instr}))
    pools = defaultdict(list)
    why = Counter()
    seen = set()
    with open(DATA / GOLD_TRAIN, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            hs = h8(r["state"])
            gold_states.add(hs)
            tg = by_golden.get(r["source"])
            if not tg:
                continue
            m = r.get("meta") or {}
            if r["id"] in bad_ids or _vote_teacher(m) or m.get("gold_probs") or m.get("renamed"):
                why["ineligible"] += 1
                continue
            if r.get("role") not in ("choice", "aff"):
                continue
            for kind, k, s in tg:
                base = None
                if kind in ("card", "oiics") and r["qtype"] == "choice" and r["role"] == "choice":
                    if not r["instructions"].startswith(s["instr"]):
                        continue
                    if kind == "card":
                        g = (s.get("gold") or {}).get(r["gold"], r["gold"])
                        if g not in s["labels"]:
                            continue
                    else:
                        g = r["gold"]
                    base = g
                elif kind == "prop" and r["qtype"] == "noul" and r["role"] == "aff" and r["instructions"] == s["instr"]:
                    base = (r["gold"] == 1) == s["gold1"]
                if base is None:
                    continue
                if (kind, k, hs) in seen:
                    continue
                seen.add((kind, k, hs))
                pools[(kind, k, "train")].append(
                    {"id": r["id"], "group_id": r["group_id"], "source": r["source"], "state": r["state"], "gold": base,
                     "meta": {x: m.get(x) for x in ("dataset", "licence", "revision")}, "inherited": True})
    # dev pools: raw files (texts outside golden_train and golden_dev)
    for kind, table in (("card", lx.CARD_SOURCES), ("prop", lx.PROP_SOURCES)):
        for k, s in table.items():
            if not s.get("raw"):
                continue
            rp = DATA / "v14_parts" / "raw" / f"{s['raw']}.jsonl"
            with open(rp, encoding="utf-8") as f:
                for line in f:
                    r = json.loads(line)
                    hs = h8(r["state"])
                    if hs in gold_states or hs in dev_states or hs in devx_states:
                        continue
                    if kind == "card":
                        if not r["instructions"].startswith(s["instr"]):
                            continue
                        g = (s.get("gold") or {}).get(r["gold"], r["gold"])
                        if g not in s["labels"]:
                            continue
                    else:
                        if r["instructions"] != s["instr"] or r["gold"] not in ("yes", "no"):
                            continue
                        g = (r["gold"] == "yes") == s["gold1"]
                    pools[(kind, k, "dev")].append(
                        {"id": "raw:" + r["key"] + ":" + str(r["rid"]), "group_id": "raw:" + r["key"] + ":" + str(r["rid"]),
                         "source": "gd_" + r["key"], "state": r["state"], "gold": g,
                         "meta": {"dataset": (r.get("meta") or {}).get("dataset"),
                                  "licence": (r.get("meta") or {}).get("licence"),
                                  "revision": (r.get("meta") or {}).get("revision")}, "inherited": False})
    rp = DATA / "v14_parts" / "raw" / f"{oiics_raw}.jsonl"
    with open(rp, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            hs = h8(r["state"])
            if hs in gold_states or hs in dev_states or hs in devx_states or not r["instructions"].startswith(oiics_instr):
                continue
            pools[("oiics", "oiics", "dev")].append(
                {"id": "raw:" + r["key"] + ":" + str(r["rid"]), "group_id": "raw:" + r["key"] + ":" + str(r["rid"]),
                 "source": "gd_" + r["key"], "state": r["state"], "gold": r["gold"],
                 "meta": {"dataset": (r.get("meta") or {}).get("dataset"), "licence": (r.get("meta") or {}).get("licence"),
                          "revision": (r.get("meta") or {}).get("revision")}, "inherited": False})
    # toxicity pool (held out): civil_comments / toxic_conv texts from the older training files, never in golden
    for b in toxic_pool(gold_states, dev_states, devx_states, why):
        pools[("prop", "toxic", "dev")].append(b)
    # decontaminate every text once; keep short enough states; one use per text
    out = {}
    for key, rows in pools.items():
        keep = []
        lim = MAX_STATE
        for b in rows:
            if len(b["state"]) > lim:
                why["long"] += 1
                continue
            ev = label_evidence(key[0], key[1], b)
            if ev:
                why["evidence:" + ev] += 1
                continue
            if not D.text_ok(b["state"], inherited=b["inherited"]):
                why["decon_text"] += 1
                continue
            if devx_g8 and word_8grams(b["state"]) & devx_g8:
                # round 3: a devx batch quotes its texts inside a numbered list, so a whole-state hash cannot see
                # them; no F7 text may share a word 8-gram with any devx state (yn2b/f7_devx_pool_scan.py, ruling
                # 10.8 as the devx author applied it: devx base texts share 0 word 8-grams with F7 train / probe)
                why["devx_8gram"] += 1
                continue
            b["state_neg"] = bool(STATE_NEG_RE.search(b["state"]))
            # a 12-gram shared with an in-family dev is inherited only while the row's state IS this golden_train
            # text (precheck 8.2); a multi-text state is never byte-equal to one, so such texts stay out of it
            b["infam"] = bool(D.cy.row_ghash(b["state"]) & D.infam)
            b["fmt"] = state_format(b["state"])
            b["qmark"] = "?" in b["state"]
            # item 23: the question mark is looked for in the unit the question asks about (the user's latest message
            # of a dialogue, else the whole text); qmark_agree = that unit and the whole state agree, so neither
            # reading of the exclusion term can change a gold (decide2 finding #2)
            b["qmark_unit"] = "?" in excl_unit_text(b["state"])
            b["qmark_agree"] = b["qmark_unit"] == b["qmark"]
            keep.append(b)
        keep.sort(key=lambda b: b["id"])
        out[key] = keep
    log(f"pools: {len(out)} pools, {sum(map(len, out.values()))} texts ({time.time() - t0:.0f} s); skipped {dict(why)}")
    for key in sorted(out):
        log(f"   pool {key}: {len(out[key])} texts, gold {dict(Counter(str(b['gold']) for b in out[key]).most_common(8))}")
    return out


_RX = {}


def _rx(pat, flags=re.I):
    k = (pat, flags)
    if k not in _RX:
        _RX[k] = re.compile(pat, flags)
    return _RX[k]


def nhtsa_states_event(text, key):
    """The NHTSA narrative states the event (fire / injury / crash): a match of lx.NHTSA_EVENT[key] with none of
    lx.NHTSA_HYPO in the 4 words before it, in the same sentence."""
    for m in _rx(r"\b(?:" + lx.NHTSA_EVENT[key] + r")\b").finditer(text):
        pre = re.split(r"[.;!?]", text[max(0, m.start() - 80):m.start()])[-1]
        if not _rx(lx.NHTSA_HYPO).search(" ".join(re.findall(r"[A-Za-z']+", pre)[-4:])):
            return True
    return False


def storm_winds(text):
    """Every wind speed a storm narrative gives: a number (or a range's two numbers) + mph after 'wind' / 'gust' in the
    same sentence."""
    out = []
    for m in _rx(lx.STORM_WIND_NUM).finditer(text):
        pre = re.split(r"(?<=[.!?])\s", text[max(0, m.start() - 90):m.start()])[-1]
        if _rx(lx.STORM_WIND_CTX).search(pre):
            out += [int(m.group(1))] + ([int(m.group(2))] if m.group(2) else [])
    return out


def ncbi_form(text):
    """The NCBI category the marked mention's form gives (nn_lexicon.py section 4b), or None when the form is unclear."""
    m = re.search(r"<e>(.*?)</e>", text)
    if not m:
        return None
    men, after = m.group(1).strip(), text[m.end():]
    if _rx(lx.NCBI_JOIN).search(men):
        return None
    if _rx(lx.NCBI_MOD_NEXT).match(after) or (_rx(lx.NCBI_MOD_SELF).search(men) and
                                               not _rx(lx.NCBI_CLASS_HEAD).search(men)):
        return "modifier"
    if _rx(lx.NCBI_CLASS_HEAD).search(men):
        return "disease class"
    if _rx(lx.NCBI_SPECIFIC_NAME, 0).search(men) or _rx(lx.NCBI_SPECIFIC_END).search(men):
        return "specific disease"
    return None


def label_evidence(kind, key, b):
    """r4 (yn2b/F7_BLIND_READ.md): None when the text shows its human label the way the card defines it, else the
    reason it is dropped. Template-level rules per source (nn_lexicon.py section 4b); the same rule for train and dev."""
    t, g = b["state"], b["gold"]
    if kind == "prop" and key in lx.NHTSA_EVENT:
        return None if nhtsa_states_event(t, key) == bool(g) else "nhtsa_" + key
    if kind != "card":
        return None
    if key == "storm":
        lo, hi = lx.CARD_SOURCES["storm"]["wind"][g]
        w = storm_winds(t)
        return None if w and all(lo <= x <= hi for x in w) else "storm_wind"
    if key == "medquad":
        body = t.split("Passage:", 1)[-1]
        if any(_rx(v, 0).search(body) for k, v in lx.MEDQUAD_HEADINGS.items() if k != g):   # headings: capitals
            return "medquad_heading"
        own = len(_rx(lx.MEDQUAD_WORDS[g]).findall(body))
        if own == 0 or any(own < 2 * len(_rx(v).findall(body)) for k, v in lx.MEDQUAD_WORDS.items() if k != g):
            return "medquad_topic"
        return None
    if key == "edgar":
        return None if bool(_rx(lx.EDGAR_RISK).search(t)) == (g == lx.EDGAR_RISK_LABEL) else "edgar_risk"
    if key == "drugprot":
        low_t = t.lower()
        if any(_rx(v).search(low_t) for k, v in lx.DRUGPROT_WORDS.items() if k != g):
            return "drugprot_two_relations"
        if g in lx.DRUGPROT_NEED_OWN and not _rx(lx.DRUGPROT_WORDS[g]).search(low_t):
            return "drugprot_no_own_word"
        return None
    if key == "ncbi":
        return None if ncbi_form(t) == g else "ncbi_form"
    if key == "safer":
        grave, care = bool(_rx(lx.SAFER_GRAVE, 0).search(t)), bool(_rx(lx.SAFER_CARE).search(t))
        ok = grave if g == "grave" else (care and not grave) if g == "middling" else not (grave or care)
        return None if ok else "safer_care"
    return None


LATEST_MSG = "User (latest message):"
OLD_TOXIC_LABEL_FILES = OLD_TOXIC_FILES + ("inj_v2",)   # every old copy whose human label must agree (not a text source)
OLD_BASE_ID_RE = re.compile(r"^r_[0-9a-f]{12}$")          # a plain base row: no _inj / _injg suffix, no r_vNc_ variant
# text that an augmented or injected copy carries besides the comment (a wrapper, a label assertion, a directive)
PAYLOAD_RE = re.compile(r"<!--|-->|ground[- ]?truth|system (?:message|note)|\bmetadata\b|prior_decision|"
                        r"system_note|ops_note|verified outcome|\bresponda\b|\boverride\b|validating the pipeline|"
                        r"correct decision|label for this|outcome (?:must|should) be|\b(?:answer|return|respond|mark|"
                        r"output|reply|label)(?: it)?(?: with| as)? ['\"]?(?:not )?toxic\b|\bresolution already\b|"
                        r"\bsigned off\b|\bmanager\b.{0,40}\btoxic\b", re.I)


def excl_unit_text(state):
    """The text an item-23 question asks about: the user's latest message of a dialogue, else the whole text."""
    return state.split(LATEST_MSG)[-1] if LATEST_MSG in state else state


def old_comment_key(state):
    """The comment body of an old civil / toxic row: a JSON wrapper's text field, the header line removed, whitespace
    collapsed. Used only to group copies of one comment."""
    t = state or ""
    if t.lstrip().startswith(("{", "[")):
        try:
            obj = json.loads(t)
        except ValueError:
            obj = None
        if isinstance(obj, dict):
            t = obj.get("content") or ((obj.get("message") or {}).get("body") if isinstance(obj.get("message"), dict)
                                       else None) or t
    t = re.sub(r"^[A-Za-z ]{1,40}:\n", "", t)
    return re.sub(r"\s+", " ", t).strip()


def old_toxic_label(r):
    """The human toxic / not-toxic label of one old choice row: the gold of a row whose options are exactly 'toxic' /
    'not toxic', or a symbol gold (Label-J ...) read through that row's own card definition. None when the card's
    definition is not one of the known toxic / civil wordings (the copy is then treated as unreadable)."""
    opts = sorted(r.get("options") or [])
    if opts == ["not toxic", "toxic"]:
        return r["gold"] == "toxic"
    d = dict(re.findall(r"^- ([^:\n]+): (.*)$", r.get("card") or "", re.M)).get(r.get("gold"), "").strip().lower()
    if re.match(r"(?:a comment is not toxic|the comment (?:is|stays) civil)\b", d):
        return False
    if re.match(r"(?:a comment is toxic|the comment is rude)\b", d):
        return True
    return None


def toxic_pool(gold_states, dev_states, devx_states, why):
    """The held-out toxicity texts (D1 + decide2 finding #1 of F7_OBJECTIONS.md). Every old choice copy of a comment
    is read (exact toxic / not-toxic options, or symbol labels through their card), and a comment is kept only when
    every copy that carries a label agrees and no copy is unreadable. The state is the comment's plain base row (id
    'r_' + 12 hex, no augmented / injected variant, no JSON wrapper), and no kept state may carry an injected payload."""
    labels, unreadable, clean = defaultdict(set), set(), {}
    for fn in OLD_TOXIC_LABEL_FILES:
        p = DATA / f"{fn}.jsonl"
        if not p.exists():
            continue
        with open(p, encoding="utf-8") as f:
            for line in f:
                if '"civil_comments"' not in line and '"toxic_conv"' not in line:
                    continue
                r = json.loads(line)
                if r.get("source") not in ("civil_comments", "toxic_conv") or r.get("qtype") != "choice":
                    continue
                k = old_comment_key(r["state"])
                lab = old_toxic_label(r)
                if lab is None:
                    unreadable.add(k)
                    continue
                labels[k].add(lab)
                if fn in OLD_TOXIC_FILES and OLD_BASE_ID_RE.match(r["id"]) and \
                        not r["state"].lstrip().startswith(("{", "[")):
                    clean.setdefault(k, (r["state"], r["source"]))
    out = []
    for k, (state, src) in sorted(clean.items()):
        if k in unreadable or len(labels[k]) != 1:
            why["toxic_label_disagrees"] += 1
            continue
        if PAYLOAD_RE.search(state):
            why["toxic_payload"] += 1
            continue
        hs = h8(state)
        if hs in gold_states or hs in dev_states or hs in devx_states:
            continue
        rid = "old:" + src + ":" + hs.hex()
        out.append({"id": rid, "group_id": rid, "source": src, "state": state, "gold": next(iter(labels[k])),
                    "meta": {"dataset": "google/civil_comments" if src == "civil_comments" else
                             "SetFit/toxic_conversations_50k", "licence": "CC0-1.0" if src == "civil_comments" else
                             "CC-BY-4.0 (Jigsaw toxic conversations)", "revision": None}, "inherited": False})
    bad = [b["id"] for b in out if PAYLOAD_RE.search(b["state"]) or b["state"].lstrip().startswith(("{", "["))]
    if bad:
        raise SystemExit(f"toxicity pool: {len(bad)} states carry a wrapper or payload: {bad[:3]}")
    return out


# ============================================================================================ subjects (one per twin pair)
class Reject(Exception):
    pass


def _forms_get(table, lex):
    return table.get(tuple(lex)) or []


class Subject:
    """One twin pair's latent: kind, source, the two states, the core claim P and how to word it. Twin A has
    truth(P) = self.tA, twin B the opposite. Every text it renders is the same for both twins."""
    kind = "card"
    ptype = "label"
    holdout = False

    _serial = 0

    def __init__(self, rng, part):
        self.rng, self.part = rng, part
        Subject._serial += 1
        self.uid = Subject._serial
        self.tA = rng.random() < 0.5
        self.card_extra = []      # authored card lines every row of this ladder carries
        self.logic = False

    # ---- interface
    def vals(self, twin):           # atom values of the twin
        raise NotImplementedError

    def core(self):                 # the CORE child (atoms carry placeholder values)
        raise NotImplementedError

    def forms(self, ctype, lex):    # [(decl, q, qn)] already filled except {S}/{T}
        raise NotImplementedError

    def lexicon_ok(self, lex):
        return all(lx.LEXICON[x]["split"] == ("holdout" if self.part == "holdout" else "train") or
                   (self.part == "holdout" and lx.LEXICON[x]["split"] == "train") for x in lex)

    def truth(self, twin):
        return self.tA if twin == "A" else not self.tA


def _ph(text, **kw):
    """Partial fill: replace known slots only."""
    for k, v in kw.items():
        text = text.replace("{" + k + "}", str(v))
    return text


class CardSubject(Subject):
    """A card-format ladder over one real classification text (two texts: one per twin). ptype:
       label    P = fit(L); twin A text has gold L iff tA. Card: rule + the label lines.
       ordinal  as label, L a pole of an ordinal scale; the other twin's text is (mostly) a middle label (item 21).
       residual P = the text fits one of the listed lines; the card adds 'something else' (item 22).
       group    P = the text's label is one of the group members (item 25).
       prop     a binary property source (two labels)."""
    kind = "card"

    def __init__(self, rng, part, key, pools, used, ptype, dev_labels):
        super().__init__(rng, part)
        self.key = key
        self.ptype = ptype
        self.isprop = key in lx.PROP_SOURCES
        S = lx.PROP_SOURCES[key] if self.isprop else lx.CARD_SOURCES[key]
        self.S = S
        self.holdout = S["split"] == "holdout"
        self.doc = S["doc"]
        # r4: derived terms are defined over the kind of thing the claim's subject is ('a name whose label ...' for
        # 'the marked name'), never over the document noun (yn2b/F7_BLIND_READ.md 7)
        self.tnoun = S.get("tnoun", S["doc"])
        self.subj = S["subj"]
        # r4: a pronoun claim subject sits after a frame that names the document ('Does the sentence support the claim
        # that ... applies to it?'), so 'it' would point at the document; when the claim's subject is not the document
        # itself (the marked mention, the user's latest message, the wizard's response ...) the full subject is used
        self.pron = S.get("pron", "it") if self.subj == "the " + self.doc else self.subj
        pk = ("prop" if self.isprop else "card", key, "train" if part == "train" else "dev")
        pool = [b for b in pools.get(pk, []) if b["id"] not in used]
        if len(pool) < 4:
            raise Reject(f"pool {pk} exhausted")
        self.source = S["golden"] or ("civil_comments+toxic_conv" if key == "toxic" else key)
        if self.isprop:
            self.labels = {S["pos"][0]: S["pos"][1], S["neg"][0]: S["neg"][1]}
            want = {"A": self.tA, "B": not self.tA}
            self.base = self._pick_pair(pool, lambda b, tw: b["gold"] == want[tw])
            self.L = S["pos"][0]
            self.card_rule = "exactly one of the two labels below fits the " + self.tnoun
            self.qlabel = None
            return
        labels = list(S["labels"])
        if ptype == "ordinal":
            ordl = S["ordinal"]
            self.L = rng.choice([ordl[0], ordl[-1]])
            self.antonym = ordl[-1] if self.L == ordl[0] else ordl[0]
            self.middle = [x for x in ordl if x not in (self.L, self.antonym)]
            mid_share = 0.8
            other = rng.choice(self.middle) if rng.random() < mid_share else self.antonym
            gA, gB = (self.L, other) if self.tA else (other, self.L)
            self.card_labels = ordl
        elif ptype == "group":
            gname, members = rng.choice(lx.GROUPS[key])
            self.L, self.members = gname, members
            outside = [x for x in labels if x not in members]
            inside = rng.choice(members)
            out1 = rng.choice(outside)
            gA, gB = (inside, out1) if self.tA else (out1, inside)
            self.card_labels = labels
        elif ptype == "residual":
            # P = the text fits one of the listed lines; the listed lines omit the 'outside' twin's gold. r4: the card
            # never lists a label near the left-off one (an inhibitor line next to a missing antagonist reads as a fit,
            # yn2b/F7_BLIND_READ.md 3.3), and its rule line says the label may be off the card (rule_open, 4.A)
            near = {frozenset(p) for p in S.get("near", ())}
            outsider = rng.choice(labels)
            listed = [x for x in labels if x != outsider and frozenset((x, outsider)) not in near]
            if len(listed) < 2:
                raise Reject("residual: fewer than two labels far from the left-off label")
            rng.shuffle(listed)
            listed = listed[:rng.choice([3, 4]) if len(listed) >= 4 else len(listed)]
            inside = rng.choice(listed)
            gA, gB = (inside, outsider) if self.tA else (outsider, inside)
            self.listed = listed
            self.card_labels = listed
            self.L = None
        elif ptype == "excl":
            # P = the text counts as the term 'a text that fits L, except one that contains a question mark'
            self.L = rng.choice(labels)
            self.term = rng.choice(lx.TERM_NAMES)
            bite = rng.random() < 0.5          # the false twin fails by the exception (fits L, has '?')
            other = rng.choice([x for x in labels if x != self.L])
            # the '?' is looked for in the unit the question asks about; only texts on which the unit and the whole
            # state agree are used, so neither reading of the definition changes a gold (decide2 finding #2)
            self.unit = S["excl_unit"]
            okT = lambda b: b["qmark_agree"] and b["gold"] == self.L and not b["qmark_unit"]  # noqa: E731
            okF = (lambda b: b["qmark_agree"] and b["gold"] == self.L and b["qmark_unit"]) if bite else \
                (lambda b: b["qmark_agree"] and b["gold"] == other and not b["qmark_unit"])  # noqa: E731
            self.base = self._pick_pair(pool, lambda b, tw: (okT if (tw == "A") == self.tA else okF)(b),
                                        match_neg=False)
            self.gA, self.gB = self.base["A"]["gold"], self.base["B"]["gold"]
            self.card_labels = labels
            self.labels = {x: S["labels"][x] for x in self.card_labels}
            self.card_rule = S["rule"]
            self.qlabel = self.term
            self.bite = bite
            return
        else:   # label
            self.L = rng.choice(labels)
            others = [x for x in labels if x != self.L]
            other = rng.choice(others)
            gA, gB = (self.L, other) if self.tA else (other, self.L)
            self.card_labels = labels
        self.gA, self.gB = gA, gB
        self.base = self._pick_pair(pool, lambda b, tw: b["gold"] == (gA if tw == "A" else gB))
        if ptype != "residual" and len(self.card_labels) > 6:
            keep = {gA, gB} | ({self.L} if self.L in labels else set())
            rest = [x for x in self.card_labels if x not in keep]
            rng.shuffle(rest)
            self.card_labels = [x for x in self.card_labels if x in keep or x in rest[:6 - len(keep)]]
        for x in self.card_labels:
            if x.lower() in dev_labels:
                raise Reject(f"dev label {x}")
        self.labels = {x: S["labels"][x] for x in self.card_labels}
        self.card_rule = S["rule_open"] if ptype == "residual" else S["rule"]
        self.qlabel = self.L

    def _pick_pair(self, pool, ok, match_neg=True):
        """Two texts (A, B) with the wanted gold; the same state format and state-negation flag."""
        rng = self.rng
        candA = [b for b in pool if ok(b, "A")]
        candB = [b for b in pool if ok(b, "B")]
        if not candA or not candB:
            raise Reject("no text with the wanted gold")
        rng.shuffle(candA)
        for a in candA[:40]:
            bs = [b for b in candB if b["id"] != a["id"] and b["fmt"] == a["fmt"] and b["state_neg"] == a["state_neg"]]
            if bs:
                return {"A": a, "B": rng.choice(bs)}
        raise Reject("no matched twin text")

    def states(self):
        return self.base["A"]["state"], self.base["B"]["state"]

    # ---- atoms
    def atom_id(self):
        if self.isprop:
            return "prop:" + self.key
        if self.ptype == "excl":
            return "core:" + self.L
        if self.ptype == "residual":
            return "listed"
        if self.ptype == "group":
            return "in:" + self.L
        return "fit:" + self.L

    def vals(self, twin):
        b = self.base[twin]
        g = b["gold"]
        v = {}
        if self.isprop:
            v[self.atom_id()] = bool(g)
            return v
        for x in self.labels:
            v["fit:" + x] = (g == x)
        if self.ptype == "residual":
            v["listed"] = g in self.listed
        if self.ptype == "group":
            v["in:" + self.L] = g in self.members
        if self.ptype == "excl":
            v["core:" + self.L] = (g == self.L) and not b["qmark_unit"]
        return v

    def core(self):
        return ATOM(self.atom_id(), True)

    def fmt_kw(self):
        return {"S": self.subj, "doc": self.doc}

    # ---- claim wordings
    def forms(self, ctype, lex):
        lex = tuple(lex)
        S = self.S
        if self.isprop:
            if ctype != "P":
                return []
            return [(d, q, None) for d, q in _forms_get(S["forms"], lex)]
        if ctype == "P":
            if self.ptype == "excl":
                return [tuple(_ph(x, T=self.term) if x else x for x in f) for f in _forms_get(lx.TERM_FORMS, lex)]
            if self.ptype == "residual":
                return [tuple(_ph(x, n=lx.NUMBER_WORDS[len(self.listed)]) if x else x for x in f)
                        for f in _forms_get(lx.RESIDUAL_FORMS, lex)]
            out = []
            for f in _forms_get(lx.LABEL_FORMS, lex):
                if "non-" in lex and " " in self.L:
                    continue
                out.append(tuple(_ph(x, L=self.L) if x else x for x in f))
            return out
        if ctype == "ONLY" and self.ptype in ("label", "ordinal"):
            return [tuple(_ph(x, L=self.L) if x else x for x in f) for f in _forms_get(lx.ONLY_FORMS, lex)]
        if ctype == "CONTRAST" and self.ptype == "label":
            Y = self.gB if self.tA else self.gA
            return [tuple(_ph(x, L=self.L, Y=Y) if x else x for x in f) for f in _forms_get(lx.CONTRAST_FORMS, lex)]
        return []

    def term_def(self, lexeme):
        """(definition text, surface) of a derived card term T = not-P carried by one lexeme (card_def cue)."""
        if self.ptype == "excl":
            return None
        if self.isprop or self.ptype in ("residual",):
            if self.ptype == "residual" and lexeme in lx.RESIDUAL_DEF:
                return lx.RESIDUAL_DEF[lexeme].replace("{noun}", self.tnoun), lexeme
            if self.isprop and lexeme in ("not", "fail", "lack", "un-", "non-", "without"):
                pos = self.S["pos"][0]
                d = {"not": f"a {self.tnoun} that does not count as '{pos}'",
                     "fail": f"a {self.tnoun} that fails to count as '{pos}'",
                     "non-": f"a non-'{pos}' {self.tnoun}" if " " not in pos else None,
                     "without": f"a {self.tnoun} without the features of '{pos}'"}.get(lexeme)
                if d:
                    return d, {"not": "not", "fail": "fails", "non-": "non-'" + pos + "'",
                               "without": "without"}[lexeme]
            return None
        L = self.L
        tpl = lx.TERM_DEFS.get(lexeme)
        if not tpl:
            return None
        if lexeme == "non-" and " " in L:
            return None
        if lexeme == "unless":
            return None if self.ptype == "group" else (fill(tpl, doc=self.tnoun, L=L), "unless")
        surf = {"not": "not", "n't": "isn't", "fail": "fails", "lack": "lacks", "exclude": "exclude",
                "rule out": "rule out", "non-": "non-" + L, "never": "never", "without": "without", "no": "no"}[lexeme]
        return fill(tpl, doc=self.tnoun, L=L), surf

    def ar(self):
        """An affirmative complement of P (no cue word): the other listed labels by name, or the complement label."""
        if self.isprop:
            d, q = self.S["ar"]
            return [(d, q, None)]
        if self.ptype in ("label", "ordinal"):
            rest = [x for x in self.labels if x != self.L]
            if len(rest) > 4:
                return []
            names = ", ".join(f"'{x}'" for x in rest[:-1]) + (" or " if len(rest) > 1 else "") + f"'{rest[-1]}'"
            return [(f"the label that fits {{S}} is {names}", f"Is the label that fits {{S}} {names}", None)]
        if self.ptype == "group":
            rest = [x for x in self.labels if x not in self.members]
            if len(rest) > 4:
                return []
            names = ", ".join(f"'{x}'" for x in rest[:-1]) + (" or " if len(rest) > 1 else "") + f"'{rest[-1]}'"
            return [(f"the label that fits {{S}} is {names}", f"Is the label that fits {{S}} {names}", None)]
        return []

    def card_lines(self):
        lines = [("rule", self.card_rule)]
        if self.ptype == "excl":
            lines += [(k, v) for k, v in self.labels.items()]
            lines.append((self.term, fill(lx.EXCLUSION_DEF, unit=self.unit, L=self.L)))
            return lines
        if self.ptype == "group":
            mem = " or ".join(f"'{x}'" for x in self.members)
            lines.append((self.L, f"a {self.tnoun} whose label is {mem}"))
        lines += [(k, v) for k, v in self.labels.items()]
        return lines

    def label_defs_text(self):
        # label names stay exact ('others' need'); only quote marks used as delimiters inside a definition go
        # (decide2 finding #3: stripping every apostrophe misspelt names and possessives)
        return "; ".join(f"{k} means {unquote(v)}" for k, v in self.labels.items())

    def meta(self, twin):
        b = self.base[twin]
        return {"dataset": b["meta"].get("dataset"), "licence": b["meta"].get("licence"),
                "revision": b["meta"].get("revision"), "derived_from": b["id"], "derived_source": b["source"],
                "derived_group": b["group_id"], "derived_by": GENERATOR, "text_gold": str(b["gold"])}

    def used_ids(self):
        return {self.base["A"]["id"], self.base["B"]["id"]}


AFFIX_SURF_RE = {"un-": r"\bun[a-z]{3,}", "non-": r"\bnon-[A-Za-z0-9-]+", "in-": r"\bin(?:complete|valid|formal|applicable)\b",
                 "im-": r"\bim(?:passable|personal)\b", "il-": r"\bil(?:legally|logical|legal)\b",
                 "dis-": r"\bdis[a-z]{3,}", "-less": r"\b[a-z]{3,}less\b", "-free": r"\b[a-z]+-free\b",
                 "ir-": r"\birregular\b", "a-": r"\basymptomatic\b"}


def find_surface(text, lexeme):
    """The exact cue word of a lexeme inside a rendered text (quotes not masked)."""
    if lexeme in AFFIX_SURF_RE:
        m = re.search(AFFIX_SURF_RE[lexeme], text, re.I)
        if not m:
            raise ValueError(f"no {lexeme!r} word in {text!r}")
        return m.group(0)
    for f in sorted(lx.LEXICON[lexeme]["forms"], key=len, reverse=True):
        if re.search(r"(?<![\w-])" + re.escape(f) + r"(?![\w-])", text, re.I) or (f.startswith("n't") and "n't" in text):
            return f
    raise ValueError(f"no {lexeme!r} in {text!r}")


def strip_prefix(t):
    return re.sub(r"^(?:User comment|Online comment|Complaint narrative|Comment):\s*", "", t.strip())


class MultiSubject(Subject):
    """A multi-text ladder: 2-5 real labelled texts in one numbered list (items 26-31). ptype (the CORE):
       SOME   ATLEAST(1, x)      'at least one of the N items ...'
       ALL    ATLEAST(N, x)      'all N items ...'
       COUNT  ATLEAST(k, x)      'at least k of the N items ...' (numeric bounds, exact boundaries)
       FEW    ATLEAST(2, x)      'two or more of the N items ...' (vs 'few' = at most one, fixed by the card)
       BOTH   AND(x_a, x_b)      'both item a and item b ...' (De Morgan)
       EITHER OR(x_a, x_b)       'item a or item b ...' (neither ... nor)
       EXCEPT ATLEAST(1, x_-j)   'some item other than item j ...' (exceptors)"""
    kind = "multitext"

    def __init__(self, rng, part, mkey, pools, used, ptype, choice_plans=(), bal=None):
        super().__init__(rng, part)
        sp = lx.MULTI_SOURCES[mkey]
        self.mkey, self.sp, self.ptype = mkey, sp, ptype
        self.holdout = sp["split"] == "holdout"
        self.item, self.items, self.Item = sp["item"], sp["items"], sp["Item"]
        self.doc = "batch"
        self.source = {"sd311": "gd_sd311_routing", "injury": "gd_nhtsa_complaints", "crash": "gd_nhtsa_complaints",
                       "fire": "gd_nhtsa_complaints", "acceptable": "gd_sc101",
                       "oiics": "gd_oiics_event", "toxic": "civil_comments+toxic_conv",
                       "wiki": "gd_wiki_help_routing"}[sp["src"]]
        split = "train" if part == "train" else "dev"
        if sp["src"] in ("sd311", "wiki"):
            pk = ("card", sp["src"], split)
            xof = lambda b: b["gold"] == sp["label"]  # noqa: E731
        elif sp["src"] == "oiics":
            pk = ("oiics", "oiics", split)
            xof = lambda b: b["gold"] == sp["label"]  # noqa: E731
        else:
            pk = ("prop", sp["src"], split)
            xof = lambda b: bool(b["gold"])  # noqa: E731
        pool = [b for b in pools.get(pk, []) if b["id"] not in used and len(b["state"]) <= MAX_MULTI_TEXT
                and not b.get("infam")]
        # r4 label evidence (yn2b/F7_BLIND_READ.md 3.2 / 6): a positive text shows the property the way the card's
        # definition does (pos_need / pos_drop); negatives come only from event types far from the property
        # (neg_block) and never describe a near event (neg_drop)
        pn, pd, nd = sp.get("pos_need"), sp.get("pos_drop"), sp.get("neg_drop")
        nb = set(sp.get("neg_block") or ())
        self.pos_pool = [b for b in pool if xof(b) and (not pn or _rx(pn).search(b["state"]))
                         and not (pd and _rx(pd).search(b["state"]))]
        self.neg_pool = [b for b in pool if not xof(b) and str(b["gold"]) not in nb
                         and not (nd and _rx(nd).search(b["state"]))]
        if len(self.pos_pool) < 6 or len(self.neg_pool) < 6:
            raise Reject(f"multi pool {pk} too small")
        Ns = [2, 3, 4] if ptype in ("BOTH", "EITHER") else [3, 4, 5]
        if choice_plans:
            Ns = [n for n in Ns if n >= 3] or [3]
        N = rng.choice(Ns)
        if ptype in ("BOTH", "EITHER"):
            N = max(N, 2)
        self.N = N
        self.k = {"SOME": 1, "ALL": N, "FEW": 2, "EXCEPT": 1}.get(ptype)
        if ptype == "COUNT":
            self.k = rng.randint(2, N - 1) if N >= 3 else 1
        self.ab = sorted(rng.sample(range(N), 2)) if ptype in ("BOTH", "EITHER") else None
        self.j = rng.randrange(N) if ptype == "EXCEPT" else None
        plans = []
        for cp in choice_plans or ():
            cp = dict(cp)
            k = min(len(cp["idx"]), N)
            cp["idx"] = rng.sample(range(N), k)
            cp["nneg"] = cp["nneg"][:k]
            if "lex" in cp:
                cp["lex"] = cp["lex"][:k]
            plans.append(cp)
        self.choice_plans = plans
        self._Ns = Ns
        self._world()
        self.logic = True

    def P_of(self, x):
        p = self.ptype
        if p in ("SOME", "ALL", "COUNT", "FEW"):
            return sum(x) >= self.k
        if p == "BOTH":
            return x[self.ab[0]] and x[self.ab[1]]
        if p == "EITHER":
            return x[self.ab[0]] or x[self.ab[1]]
        if p == "EXCEPT":
            return any(v for i, v in enumerate(x) if i != self.j)
        raise ValueError(p)

    def _world(self):
        rng, N = self.rng, self.N
        allv = [tuple((m >> i) & 1 == 1 for i in range(N)) for m in range(2 ** N)]
        want = {"A": self.tA, "B": not self.tA}
        cands = []
        for xa in allv:
            if self.P_of(xa) != want["A"]:
                continue
            if self.ptype == "EXCEPT" and not xa[self.j]:
                continue
            for xb in allv:
                if self.P_of(xb) != want["B"]:
                    continue
                if self.ptype == "EXCEPT" and not xb[self.j]:
                    # arbiter round 3, A3: 'no / none / not a single X other than X j ...' also says that X j has the
                    # property (the exceptive's inclusion condition). The excepted item has it in BOTH twins, so
                    # the literal (set-minus) and the exceptive readings agree on every row of the ladder, and no
                    # negative exceptive ever runs over an all-false batch.
                    continue
                ham = sum(1 for a, b in zip(xa, xb) if a != b)
                if not 1 <= ham <= 3:
                    continue
                if not all(choice_unique(cp, xa, xb) for cp in self.choice_plans):
                    continue
                cands.append((xa, xb))
        if not cands and self.choice_plans:
            tries = getattr(self, "_tries", 0)
            self._tries = tries + 1
            if tries < 12:
                # another text count / option subset before giving a plan up
                if tries % 3 == 2:
                    N = rng.choice([n for n in self._Ns if n >= 3] or [3])
                    self.N = N
                    self.k = {"SOME": 1, "ALL": N, "FEW": 2, "EXCEPT": 1}.get(self.ptype, self.k)
                    if self.ptype == "COUNT":
                        self.k = rng.randint(2, N - 1) if N >= 3 else 1
                    if self.ptype in ("BOTH", "EITHER"):
                        self.ab = sorted(rng.sample(range(N), 2))
                    if self.ptype == "EXCEPT":
                        self.j = rng.randrange(N)
                for cp in self.choice_plans:
                    kk = min(len(cp["nneg"]), self.N)
                    cp["idx"] = rng.sample(range(self.N), kk)
                return self._world()
            self.choice_plans = self.choice_plans[:-1]
            self._tries = 0
            return self._world()
        if not cands:
            raise Reject(f"no multitext world for {self.ptype} N={N}")
        # prefer boundary worlds for COUNT (counts k and k-1) and few-vs-none contrasts
        if self.ptype == "COUNT":
            bc = [c for c in cands if {sum(c[0]), sum(c[1])} == {self.k, self.k - 1}]
            cands = bc or cands
        xa, xb = rng.choice(cands)
        self.x = {"A": xa, "B": xb}
        for _ in range(30):
            pos, neg = list(self.pos_pool), list(self.neg_pool)
            rng.shuffle(pos)
            rng.shuffle(neg)
            ta, tb = [], []
            for i in range(N):
                pa = pos.pop() if xa[i] else neg.pop()
                ta.append(pa)
                if xa[i] == xb[i]:
                    tb.append(pa)
                else:
                    tb.append(pos.pop() if xb[i] else neg.pop())
            sa, sb = self.render(ta), self.render(tb)
            if bool(STATE_NEG_RE.search(sa)) == bool(STATE_NEG_RE.search(sb)) and len(sa) <= MAX_STATE and \
                    len(sb) <= MAX_STATE:
                self.texts = {"A": ta, "B": tb}
                self._states = (sa, sb)
                return
        raise Reject("multitext texts do not match on state negation / length")

    def render(self, texts):
        return "\n\n".join(f"{self.Item} {i + 1}:\n{strip_prefix(b['state'])}" for i, b in enumerate(texts))

    def states(self):
        return self._states

    def vals(self, twin):
        return {f"x{i + 1}": v for i, v in enumerate(self.x[twin])}

    def core(self):
        at = [ATOM(f"x{i + 1}", True) for i in range(self.N)]
        p = self.ptype
        if p in ("SOME", "ALL", "COUNT", "FEW"):
            return {"op": "ATLEAST", "k": self.k, "children": at}
        if p == "BOTH":
            return {"op": "AND", "children": [at[self.ab[0]], at[self.ab[1]]]}
        if p == "EITHER":
            return {"op": "OR", "children": [at[self.ab[0]], at[self.ab[1]]]}
        return {"op": "ATLEAST", "k": 1, "children": [a for i, a in enumerate(at) if i != self.j]}

    # ---- wording
    def _w(self):
        sp = self.sp
        cop = sp.get("adj") is not None
        a, b = (self.ab or [0, 1])
        return dict(N=lx.NUMBER_WORDS[self.N], items=self.items, item=self.item, Item=self.Item, sg=sp["sg"],
                    base=sp["base"], a=a + 1, b=b + 1, j=(self.j or 0) + 1, cop=cop, adj=sp.get("adj"),
                    k=lx.NUMBER_WORDS.get(self.k, str(self.k)), km1=lx.NUMBER_WORDS.get((self.k or 1) - 1, ""),
                    negadj=sp.get("negadj"), comp_sg=sp.get("comp_sg"), comp_base=sp.get("comp_base"))

    def forms(self, ctype, lex):
        if ctype != "P":
            return []
        w = self._w()
        p, lex = self.ptype, tuple(lex)
        cop, adj = w["cop"], w["adj"]
        N, items, item, Item, sg, base = w["N"], w["items"], w["item"], w["Item"], w["sg"], w["base"]
        a, b, j, k, km1 = w["a"], w["b"], w["j"], w["k"], w["km1"]
        pl = (f"are {adj}" if cop else base)
        qs = (lambda subj: f"Is {subj} {adj}") if cop else (lambda subj: f"Does {subj} {base}")
        qp = (lambda subj: f"Are {subj} {adj}") if cop else (lambda subj: f"Do {subj} {base}")
        F = {}
        if p == "SOME":
            F[()] = [(f"at least one of the {N} {items} {sg}", qs(f"at least one of the {N} {items}"), None)]
            F[("none",)] = [(f"none of the {N} {items} {sg}", None, None)]
            F[("no",)] = [(f"no {item} in the batch {sg}", None, None)]
            F[("not a single",)] = [(f"not a single {item} in the batch {sg}", None, None)]
            if w["negadj"]:
                aff = self.sp["negadj_aff"]
                F[(aff,)] = [(f"the batch is made up only of {w['negadj']} {items}", None, None)]
                F[("not", aff)] = [(f"the batch is not made up only of {w['negadj']} {items}", None, None)]
            if self.part == "holdout":
                F[("not one",)] = [(f"not one of the {N} {items} {sg}", None, None)]
        elif p == "ALL":
            F[()] = [(f"all {N} {items} {pl}", qp(f"all {N} {items}"), None)]
            F[("not all",)] = [(f"not all {N} {items} {pl}", None, None)]
            F[("not every",)] = [(f"not every {item} in the batch {sg}", None, None)]
        elif p == "COUNT":
            F[()] = [(f"at least {k} of the {N} {items} {pl}", qp(f"at least {k} of the {N} {items}"), None)]
            F[("no more than",)] = [(f"no more than {km1} of the {N} {items} {pl if km1 != 'one' else sg}", None, None)]
        elif p == "FEW":
            F[()] = [(f"two or more of the {N} {items} {pl}", qp(f"two or more of the {N} {items}"), None)]
            F[("few",)] = [(f"few of the {N} {items} {pl}", qp(f"few of the {N} {items}"), None)]
        elif p == "BOTH":
            F[()] = [(f"both {Item} {a} and {Item} {b} {pl}", qp(f"both {Item} {a} and {Item} {b}"), None)]
            F[("not",)] = [(f"{Item} {a} and {Item} {b} are not both {adj}" if cop else
                            f"{Item} {a} and {Item} {b} do not both {base}", None, None)]
        elif p == "EITHER":
            F[()] = [(f"{Item} {a} or {Item} {b} {sg}", qs(f"{Item} {a} or {Item} {b}"), None)]
            F[("neither",)] = [(f"neither {Item} {a} nor {Item} {b} {sg}", None, None)]
        elif p == "EXCEPT":
            F[()] = [(f"some {item} other than {Item} {j} {sg}", qs(f"any {item} other than {Item} {j}"), None)]
            F[("no",)] = [(f"no {item} other than {Item} {j} {sg}", None, None)]
            F[("none",)] = [(f"none of the {items} apart from {Item} {j} {pl}", None, None)]
            F[("not a single",)] = [(f"not a single {item} other than {Item} {j} {sg}", None, None)]
        return F.get(lex, [])

    def ar(self):
        w = self._w()
        p = self.ptype
        if not w["comp_sg"]:
            return []
        if p == "SOME":
            return [(f"every {w['item']} in the batch {w['comp_sg']}", None, None)]
        if p == "ALL":
            return [(f"at least one of the {w['N']} {w['items']} {w['comp_sg']}", None, None)]
        if p == "COUNT":
            # 'at most one of the five complaints reports ...' (singular after 'one'; decide2 finding #5)
            vp = (w["sg"] if w["km1"] == "one" else w["base"]) if not w["cop"] else \
                (("is " if w["km1"] == "one" else "are ") + w["adj"])
            return [(f"at most {w['km1']} of the {w['N']} {w['items']} {vp}", None, None)]
        return []

    def term_def(self, lexeme):
        w = self._w()
        p = self.ptype
        cop = w["cop"]
        d = None
        if p == "SOME" and lexeme == "no":
            d = (f"a batch in which no {w['item']} {w['sg']}", "no")
        elif p == "SOME" and lexeme == "none":
            d = (f"a batch in which none of the {w['items']} {w['sg']}", "none")
        elif p == "ALL" and lexeme == "not every":
            d = (f"a batch in which not every {w['item']} {w['sg']}", "not every")
        elif p == "EITHER" and lexeme == "neither":
            d = (f"a batch in which neither {w['Item']} {w['a']} nor {w['Item']} {w['b']} {w['sg']}", "neither")
        elif p == "BOTH" and lexeme == "not":
            d = (f"a batch in which {w['Item']} {w['a']} and {w['Item']} {w['b']} " +
                 (f"are not both {w['adj']}" if cop else f"do not both {w['base']}"), "not")
        return d

    def card_lines(self):
        # 'each one either reports an injury or does not' / 'each one either is toxic or is not' (grammar, decide2
        # finding #5: a copula property never takes 'or does not')
        tail = "is not" if self.sp.get("adj") else "does not"
        lines = [("rule", f"the batch holds {lx.NUMBER_WORDS[self.N]} numbered {self.items}; each one either "
                          f"{self.sp['sg']} or {tail}")]
        lines.append(("definition", self.sp["define"]))
        lines.append(("reading", lx.LOGIC_LINE))
        return lines

    def label_defs_text(self):
        return cap1(self.sp["define"]) + "."

    def meta(self, twin):
        ts = self.texts[twin]
        return {"dataset": "; ".join(sorted({str(b["meta"].get("dataset")) for b in ts})),
                "licence": "; ".join(sorted({str(b["meta"].get("licence")) for b in ts})), "revision": None,
                "derived_from": "|".join(b["id"] for b in ts), "derived_source": self.source,
                "derived_group": "|".join(b["group_id"] for b in ts), "derived_by": GENERATOR}

    def used_ids(self):
        return {b["id"] for tw in ("A", "B") for b in self.texts[tw]}

    # ---- choice options (item names); the plan was satisfied by the world search
    def option_names(self, idx):
        return [f"{self.Item} {i + 1}" for i in idx]


def choice_unique(plan, xa, xb):
    """True when the plan's choice row has exactly one option evaluating to its 'select' value in each twin and the two
    twins' golds sit at different positions."""
    ga, gb = choice_gold_of(plan, xa), choice_gold_of(plan, xb)
    return ga is not None and gb is not None and ga != gb


def choice_gold_of(plan, x):
    want = plan["select"] == "true"
    hits = []
    for pos, (i, nneg) in enumerate(zip(plan["idx"], plan["nneg"])):
        v = bool(x[i]) ^ (nneg % 2 == 1)
        if v == want:
            hits.append(pos)
    return hits[0] if len(hits) == 1 else None


POOL_SPLIT = {"train": "train", "iid": "dev_iid", "holdout": "dev_holdout"}
REC_FORMATS = ("md_table", "json", "csv", "bullets", "key_value", "prose")


class PackSubject(Subject):
    """A program-written record: a list of 3-6 invented items with one decisive field. P = the target item has the
    pack's property. Twin B is twin A with the target item's field flipped (and at most one other item changed, so
    that the ladder's choice row has exactly one answer in both twins)."""
    kind = "record"
    ptype = "pack"

    def __init__(self, rng, part, pkey, names_used, fmt, choice_plans=(), spec=None):
        super().__init__(rng, part)
        self.pkey = pkey
        self.P = spec or lx.PACKS[pkey]
        self.holdout = self.P["split"] == "holdout"
        self.doc = self.P["doc"]
        self.source = "f7_record:" + pkey
        self.fmt = fmt
        pool = mv.NamePool(POOL_SPLIT[part])
        N = rng.randint(3, 6)
        choice_plans = list(choice_plans or ())
        for cp in choice_plans:
            N = max(N, max(cp["idx"]) + 1)
        names = []
        seen = set()
        while len(names) < N:
            if self.P.get("people"):
                nm = pool.person(rng)
                k = nm
            else:
                nm = f"{pool.stem(rng)} {rng.choice('BCDFGHKLMNPRSTVWXZ')}-{rng.randint(100, 999)}"
                k = nm.split()[0]
            if k not in seen and nm not in names_used:
                seen.add(k)
                names.append(nm)
        self.names = names
        self.N = N
        self.t = 0
        self.person = pool.person(rng)
        self.ident = mv.NamePool.ident(rng, rng.choice("KQRT"), 5)
        self.choice_plans = choice_plans
        self._world()

    def _world(self):
        """Every world (x_A over the N items, x_B = x_A with the target flipped and at most one other item flipped)
        that gives each choice plan exactly one answer in both twins at different positions; minimal edits first.
        When two plans admit no common world, the second plan is dropped."""
        rng, N, t = self.rng, self.N, self.t
        want = {"A": self.tA, "B": not self.tA}
        for plans in ([self.choice_plans] + ([self.choice_plans[:1]] if len(self.choice_plans) > 1 else [])):
            exact, edited = [], []
            for bits in range(2 ** N):
                xa = [bool((bits >> i) & 1) for i in range(N)]
                if xa[t] != want["A"] or len(set(xa)) < 2:
                    continue
                xb = list(xa)
                xb[t] = want["B"]
                rest = [i for i in range(N) if i != t]
                flips = [()] + [(u,) for u in rest] + ([(u, v) for u in rest for v in rest if u < v]
                                                       if len(plans) > 1 else [])
                for fl in flips:
                    xb2 = list(xb)
                    for u in fl:
                        xb2[u] = not xb2[u]
                    if len(set(xb2)) < 2 or not all(choice_unique(cp, xa, xb2) for cp in plans):
                        continue
                    (exact if not fl else edited).append((xa, xb2))
            worlds = exact + edited
            rng.shuffle(worlds)
            worlds.sort(key=lambda w: sum(1 for i in range(N) if w[0][i] != w[1][i]))
            for xa, xb in worlds[:40]:
                self.x = {"A": xa, "B": xb}
                self.val = {}
                for tw in ("A", "B"):
                    self.val[tw] = []
                    for i in range(N):
                        if tw == "B" and xb[i] == xa[i]:
                            self.val[tw].append(self.val["A"][i])
                        else:
                            self.val[tw].append(rng.choice(self.P["pos"] if self.x[tw][i] else self.P["neg"]))
                self.noise = [rng.randint(1, 40) for _ in range(N)]
                sa, sb = self.render("A"), self.render("B")
                if bool(STATE_NEG_RE.search(sa)) != bool(STATE_NEG_RE.search(sb)):
                    continue
                self._states = (sa, sb)
                self.choice_plans = plans
                return
        raise Reject(f"no record world for {self.pkey}")

    def render(self, tw):
        P = self.P
        title = f"{P['title']} {self.ident}"
        fld, nz = P["field"], P["noise"]
        items = [{"name": n, fld: v, nz: q} for n, v, q in zip(self.names, self.val[tw], self.noise)]
        head = f"{title}\nPrepared by: {self.person}\n\n"
        cap = lambda w: w[0].upper() + w[1:]  # noqa: E731
        if self.fmt == "json":
            return mv.render_json({"title": title, "prepared_by": self.person, P["items"].replace(" ", "_"): items})
        if self.fmt == "md_table":
            body = [f"| {cap(P['item'])} | {cap(fld)} | {cap(nz)} |", "|---|---|---|"]
            body += [f"| {it['name']} | {it[fld]} | {it[nz]} |" for it in items]
        elif self.fmt == "csv":
            body = [f"{P['item']},{fld},{nz}"] + [f"{it['name']},\"{it[fld]}\",{it[nz]}" for it in items]
        elif self.fmt == "bullets":
            body = [f"- {it['name']}: {fld} {it[fld]}; {nz} {it[nz]}" for it in items]
        elif self.fmt == "key_value":
            body = []
            for k, it in enumerate(items, 1):
                body += [f"{P['item']} {k}: {it['name']}", f"{fld}: {it[fld]}", f"{nz}: {it[nz]}", ""]
            body = body[:-1]
        else:
            body = [f"{it['name']} is listed with {fld} \"{it[fld]}\" and {nz} {it[nz]}." for it in items]
        return head + "\n".join(body)

    def states(self):
        return self._states

    def subj_of(self, i):
        return fill(self.P["subj"], N=self.names[i])

    def vals(self, twin):
        return {f"x:{n}": v for n, v in zip(self.names, self.x[twin])}

    def core(self):
        return ATOM(f"x:{self.names[self.t]}", True)

    def forms(self, ctype, lex):
        if ctype != "P":
            return []
        return [tuple(f) for f in _forms_get(self.P["forms"], lex)]

    def ar(self):
        a = self.P.get("ar")
        return [(a[0], a[1], None)] if a else []

    def term_def(self, lexeme):
        if lexeme == "unless" and self.P.get("pos_term"):
            return (f"applies to every {self.P['item']} unless it counts as '{self.P['pos_term'][0]}'", "unless",
                    "review case")
        d = (self.P.get("dterms") or {}).get(lexeme)
        if not d:
            return None
        term, text = d
        return text, find_surface(text, lexeme), term

    def card_lines(self):
        P = self.P
        lines = []
        if P.get("rule"):
            lines.append(P["rule"])
        lines.append((P["pos_term"][0], P["pos_term"][1]))
        if P.get("ar") and P["ar"][2]:
            lines.append(P["ar"][2])
        return lines

    def label_defs_text(self):
        P = self.P
        s = f"here, {P['pos_term'][0]} means {P['pos_term'][1]}"
        if P.get("rule"):
            s = f"{P['rule'][1]}; " + s
        return unquote(cap1(s) + ".")

    def meta(self, twin):
        return {"dataset": f"program generator {GENERATOR}", "licence": mv.LICENCE, "revision": None,
                "pack": self.pkey, "world_fmt": self.fmt, "n_items": self.N, "target": self.names[self.t]}

    def used_ids(self):
        return set()

    def option_names(self, idx):
        return [self.names[i] for i in idx]


class TriageSubject(PackSubject):
    """Item 35: does the triage note claim P, make no claim, or claim not-P? The ticket's triage field reads 'yes'
    (claims P), 'no' (claims not-P) or is left blank (no claim)."""
    MESSAGES = [
        "The kettle I bought arrived with a dent and I have not used it yet. What can you do about it?",
        "My order came in the wrong colour and I don't want to keep it as it is. Please advise.",
        "The jacket is too small and I haven't worn it. How do I sort this out?",
        "The lamp flickers and I can't get it to stay on. I would like this handled soon.",
        "A part of the shelf kit was not in the box. I need help with this order.",
        "The headphones crackle on one side and I haven't dropped them. What are my options?",
    ]

    def __init__(self, rng, part, names_used, fmt, choice_plan=None, messages=None):
        Subject.__init__(self, rng, part)
        self.P = lx.TRIAGE
        self.pkey = "triage"
        self.holdout = False
        self.doc = "ticket"
        self.source = "f7_record:triage"
        self.fmt = fmt
        pool = mv.NamePool(POOL_SPLIT[part])
        self.person = pool.person(rng)
        self.ident = mv.NamePool.ident(rng, "T", 6)
        self.msg = rng.choice(messages or self.MESSAGES)
        self.field = {"A": "yes" if self.tA else rng.choice(["no", ""]),
                      "B": rng.choice(["no", ""]) if self.tA else "yes"}
        self.names = [self.person]
        self.choice_plans = []
        self.N, self.t = 1, 0
        self._states = (self.render("A"), self.render("B"))
        if bool(STATE_NEG_RE.search(self._states[0])) != bool(STATE_NEG_RE.search(self._states[1])):
            raise Reject("triage state negation differs")

    def render(self, tw):
        f = self.field[tw]
        return (f"Support ticket {self.ident}\nCustomer: {self.person}\nMessage: {self.msg}\n\nTriage note\n"
                f"refund requested: {f if f else '(left blank)'}\nqueue: returns")

    def vals(self, twin):
        f = self.field[twin]
        return {"note:yes": f == "yes", "note:no": f == "no"}

    def core(self):
        return ATOM("note:yes", True)

    def forms(self, ctype, lex):
        return [tuple(f) for f in _forms_get(self.P["forms"], lex)] if ctype == "P" else []

    def ar(self):
        return []

    def term_def(self, lexeme):
        return None

    def card_lines(self):
        return [("triage note", "the agent's summary; 'refund requested' reads yes (the note claims a refund "
                                "request), no (the note claims there is none) or is left blank (the note makes "
                                "no claim either way)")]

    def label_defs_text(self):
        return ("The triage field refund requested reads yes (the note claims a refund request), no (the note "
                "claims there is none) or is left blank (the note makes no claim either way).")

    def meta(self, twin):
        return {"dataset": f"program generator {GENERATOR}", "licence": mv.LICENCE, "revision": None,
                "pack": "triage", "world_fmt": "ticket", "n_items": 1, "target": self.person}

    def subj_of(self, i):
        return "the triage note"


# ============================================================================================ rendering
YN_KEYS = {"yn": ("yes", "no"), "YN": ("Yes", "No")}


def item_tags_rule(d, cues, n_dist, has_yn, state_neg, is_choice, select_false, lf, kind):
    """Checklist items whose structure can be read from the row (the same reading as f7_precheck tag_rule)."""
    sc = [c for c in cues if c["scoping"]]
    neg = [c for c in cues if c["cls"] != "lookalike"]
    cls = [c["cls"] for c in sc]
    pos = {c["position"] for c in sc}
    dist_cues = [c for c in cues if not c["scoping"] and c["cls"] != "lookalike" and c.get("_dist")]
    t = set()
    if d == 0 and not any(c["position"] in QUESTION_POSITIONS for c in neg):
        t.add(1)
    if d == 1 and any(c["cls"] == "syntactic" and c["position"] == "inner_claim" for c in sc):
        t.add(2)
    if d == 1 and "truth_frame" in cls:
        t.add(3)
    if d == 1 and sc and all(c == "lexical" for c in cls):
        t.add(4)
    if d == 1 and "affixal" in cls:
        t.add(5)
    if d == 2 and len(sc) == 2 and len(set(cls)) == 2:
        t.add(6)
    if d == 2 and len(sc) == 2 and len(set(cls)) == 1:
        t.add(7)
    if d == 3 and len(set(cls)) >= 2:
        t.add(8)
    if d == 4:
        t.add(9)
    if d >= 2 and any(c["position"] == "outer_frame" and c["cls"] in ("lexical", "truth_frame") for c in sc) \
            and any(c["position"] != "outer_frame" for c in sc):
        t.add(10)
    if pos & {"card_def", "yn_key"} and pos & {"outer_frame", "inner_claim", "separate_sentence", "answer_map",
                                                 "choice_option"}:
        t.add(11)
    if any(c["distance"] in ("next_sentence", "far", "other_field") for c in sc):
        t.add(12)
    if "answer_map" in pos:
        t.add(13)
    if "yn_key" in pos:
        t.add(14)
    if n_dist >= 1:
        t.add(15)
    if d >= 1 and n_dist >= 1:
        t.add(16)
    if d == 0 and n_dist >= 2:
        t.add(17)
    if any(c["position"] == "card_def" for c in dist_cues):
        t.add(18)
    if state_neg:
        t.add(19)
    if any(c["cls"] == "lookalike" for c in cues):
        t.add(20)
    if is_choice and select_false:
        t.add(36)
    if not is_choice and d >= 1 and "inner_claim" in pos and has_yn and kind == "pin":
        t.add(38)
    return t


class RowDef:
    """A twin-independent row: text, card, cues, LF template, tags. instantiate(twin) gives the row + sidecar."""

    def __init__(self, **kw):
        self.__dict__.update(kw)


def build_card(subj, extra_lines, style, yes_line, no_line, need_bival, key_lines=None):
    lines = list(subj.card_lines()) + list(extra_lines)
    if subj.logic:
        pass
    if need_bival:
        lines.append(("note", fill(lx.BIVALENCE_LINE, doc=subj.doc)))
    if style in ("yn", "YN"):
        y, n = YN_KEYS[style]
        if key_lines:
            yes_line, no_line = key_lines
        lines += [(y, cap1(yes_line) + "."), (n, cap1(no_line) + ".")]
    keys = [k.lower() for k, _ in lines]
    if len(set(keys)) != len(keys):
        # repeated 'note' keys: number them
        cnt = Counter()
        out = []
        for k, v in lines:
            cnt[k] += 1
            out.append((k if cnt[k] == 1 else f"{k} {cnt[k]}", v))
        lines = out
    for k, v in lines:
        if not k or ": " in k or "\n" in k or "\n" in v or not v.strip():
            raise Reject(f"card line {k!r}")
    return "\n".join(f"- {k}: {v}" for k, v in lines)


def combo_key(c):
    """The question a combo renders (AR and ARC render the same text)."""
    return (c["frame"], "AR" if c["ctype"] in ("AR", "ARC") else c["ctype"], tuple(c["inner"]), c.get("carddef"),
            c.get("ynkey"))


def can_distract(x):
    """CL:351 'a lexeme that can serve as a distractor': every syntactic lexeme (F7_OBJECTIONS.md A1) and every lexeme
    the curated lexicon flags."""
    v = lx.LEXICON.get(x) or {}
    return v.get("cls") == "syntactic" or bool(v.get("can_distract"))


def dist_fits(subj, F, kind, row):
    """A distractor template that may go on this ladder / frame: 'not all' / 'not every' side clauses only on cards
    with the logic line (EXCLUDE X10); no card line under the key the 'contrary' definition uses."""
    if kind == "side" and row[0] in lx.DIST_SIDE_LOGIC_ONLY and not getattr(subj, "logic", False):
        return False
    if kind == "card" and row[2] == lx.CONTRARY_KEY and frame_word(F):
        return False
    return True


FRAME_WORD_RE = re.compile(r"\b(" + "|".join(lx.FRAME_WORDS) + r")\b")


def frame_word(F):
    """'contrary' / 'opposite' / 'reverse' when the frame asks about that version of the claim, else None. Each of
    these words has a plain-denial and a stronger (contrary / antonym) reading, so the card defines it (decide2
    finding #6 for 'contrary'; arbiter round 3, A4 for 'opposite' and 'reverse')."""
    words = {m.group(1) for m in FRAME_WORD_RE.finditer((F["q"] + " " + F["y"] + " " + F["n"]).lower())}
    if len(words) > 1:
        raise ValueError(f"frame {F['id']} uses two frame words {sorted(words)}")
    return words.pop() if words else None


def frame_says_contrary(F):
    return frame_word(F) == "contrary"


# an exceptor phrase that excepts a numbered item ('other than Comment 4'), the only exceptive F7 renders (item 31)
_EXC = r"(?:other than|apart from|besides|but for|except for|except)\s+[A-Z][a-z]+ \d+"
# 'no / none of the / not a single X other than X 4', 'every X apart from X 2', and the fronted 'Apart from X 3, no X'
NEG_EXCEPTIVE_RE = re.compile(r"\b(?:no|none of the|not a single|not one of the|not one)\s+(?:[a-z]+\s+){0,2}?" + _EXC +
                              r"|\b" + _EXC + r",\s*(?:no|none|not a single|not one)\b", re.I)
UNIV_EXCEPTIVE_RE = re.compile(r"\b(?:every|all|each|all of the)\s+(?:[a-z]+\s+){0,2}?" + _EXC +
                               r"|\b" + _EXC + r",\s*(?:every|all|each)\b", re.I)


def ambiguity_invariants(subj, out):
    """Arbiter round 3 (yn2b/F7_OBJECTIONS.md): two English constructions with two readings must never be rendered
    with different golds under the two readings. These are build invariants: a violation is a generator bug and
    stops the build (rows are never filtered on it).
      A3  a negative / universal exceptive ('no X other than X j ...') requires the excepted item to have the
          property the quantifier denies the rest, in BOTH twins (MultiSubject._world guarantees it);
      A4  every row that asks about 'the contrary / opposite / reverse of' a claim defines that word in its card as
          the plain denial."""
    neg_exc = False
    for tw in ("A", "B"):
        for row, m, rd in out[tw]:
            texts = [row["instructions"] or "", row["card"] or ""] + [o for o in (row["options"] or [])]
            for t in texts:
                if UNIV_EXCEPTIVE_RE.search(t):
                    raise RuntimeError(f"A3: universal exceptive in {row['id']}: {t[:120]!r}")
                if NEG_EXCEPTIVE_RE.search(t):
                    neg_exc = True
            for w in lx.FRAME_WORDS:
                if re.search(r"\bthe %s\b" % w, row["instructions"] or "") and \
                        f"- {lx.CONTRARY_KEY}: {lx.frame_word_def(w)}" not in (row["card"] or ""):
                    raise RuntimeError(f"A4: '{w}' frame without its plain-denial card line in {row['id']}")
    if neg_exc:
        if not (subj.kind == "multitext" and subj.ptype == "EXCEPT" and subj.x["A"][subj.j] and subj.x["B"][subj.j]):
            raise RuntimeError(f"A3: negative exceptive whose excepted item lacks the property ({subj.kind})")


def render_yn(subj, spec):
    """spec: rung, ctype (P | TERM | ARC | ONLY | CONTRAST | AR), inner (tuple), form_i, carddef (lexeme),
    frame, ynkey (KEYS index), dists [(kind, idx)], look (lexeme), style. Returns a RowDef."""
    F = lx.FRAMES[spec["frame"]]
    ctype, inner = spec["ctype"], tuple(spec["inner"])
    cues = []

    def add(lexeme, pos, scoping, dist, surface, cls=None, distractor=False):
        cues.append({"lexeme": lexeme, "cls": cls or lx.LEXICON[lexeme]["cls"], "position": pos, "scoping": scoping,
                     "distance": dist, "surface": surface, "_dist": distractor})
        return len(cues) - 1

    # ---- the subject NP and the claim
    if subj.kind == "record":
        S_full = subj.subj_of(subj.t)
        S_pron = S_full
    elif subj.kind == "multitext":
        S_full = S_pron = ""
    else:
        S_full, S_pron = subj.subj, subj.pron
    S_used = S_pron if F["subj"] == "pron" else S_full
    term_line, term_name, term_surf, except_cue = None, None, None, None
    if ctype == "TERM":
        td = subj.term_def(spec["carddef"])
        if not td:
            raise Reject("no term")
        tdef, term_surf = td[0], td[1]
        term_name = td[2] if len(td) > 2 else spec["term_name"]
        term_line = (term_name, tdef)
        forms = [tuple(_ph(x, T=term_name) if x else x for x in f) for f in _forms_get(lx.TERM_FORMS, inner)]
    elif ctype in ("AR", "ARC"):
        if inner:
            raise Reject("AR claims carry no inner cue")
        forms = subj.ar()
    else:
        forms = subj.forms(ctype, inner)
    if not forms:
        raise Reject(f"no form {ctype} {inner}")
    form = forms[spec.get("form_i", 0) % len(forms)]
    if subj.kind == "multitext" and ctype == "TERM":
        S_full = S_used = "the batch"
    decl, q, qn = form
    c = fill(decl, S=S_full) if "{S}" in decl else decl
    cp = fill(decl, S=S_used) if "{S}" in decl else decl
    cq = fill(q, S=S_full) if q else None
    cqn = fill(qn, S=S_full) if qn else None
    needs = F["needs"]
    if needs == "cq" and not cq:
        raise Reject("frame needs an interrogative claim")
    if needs == "cqn":
        if not cqn:
            raise Reject("frame needs an inner-negative interrogative")
        cq = cqn
    # ---- cues: inner (outermost first), card_def, frame, key
    inner_idx = []
    for lexeme in inner:
        inner_idx.append(add(lexeme, "inner_claim", True, "same_clause", find_surface(c, lexeme)))
    cd_idx = None
    if ctype == "TERM":
        cd_idx = add(spec["carddef"], "card_def", True, "other_field", term_surf)
    frame_idx = [add(fc[0], fc[2] if len(fc) > 2 else F["pos"], True, fc[3] if len(fc) > 3 else F["dist"], fc[1])
                 for fc in F["cues"]]
    key_idx, key_lines = None, None
    if spec.get("ynkey") is not None:
        inv, klex, ky, kn = lx.KEYS[spec["ynkey"]]
        key_lines = (fill(ky, c=c, doc=subj.doc), fill(kn, c=c, doc=subj.doc))
        if inv:
            key_idx = add(klex, "yn_key", True, "other_field", klex)
    # ---- distractors and look-alike
    side_txt, sep_txt, sep_y, card_dist = "", "", "", []
    dist_idx = []
    for kind, i in spec.get("dists", []):
        if kind == "side":
            lexeme, surf, txt = lx.DIST_SIDE[i]
            side_txt = cap1(fill(txt, doc=subj.doc)) + ", "
            dist_idx.append(add(lexeme, "outer_frame", False, "same_sentence", surf, distractor=True))
        elif kind == "sep":
            lexeme, surf, txt, ytxt = lx.DIST_SEP[i]
            sep_txt = " " + fill(txt, doc=subj.doc)
            sep_y = ", " + fill(ytxt, doc=subj.doc)
            dist_idx.append(add(lexeme, "separate_sentence", False, "next_sentence", surf, distractor=True))
        else:
            lexeme, surf, key, txt = lx.DIST_CARD[i]
            card_dist.append((key, fill(txt, doc=subj.doc)))
            dist_idx.append(add(lexeme, "card_def", False, "other_field", surf, distractor=True))
    if key_lines:
        key_lines = (low1(side_txt) + key_lines[0] + sep_y, low1(side_txt) + key_lines[1] + sep_y)
    look_pre, look_sent = "", ""
    if spec.get("look"):
        L = lx.LOOKALIKES[spec["look"]]
        txt = fill(L["text"], doc=subj.doc)
        if L["kind"] == "prefix":
            look_pre = txt
        else:
            look_sent = txt
        add(spec["look"], "outer_frame" if L["kind"] == "prefix" else "separate_sentence", False, "same_sentence",
            spec["look"], cls="lookalike")
    # ---- instruction text
    kw = dict(c=c, cp=cp, doc=subj.doc)
    if cq:
        kw.update(cq=cq, cql=low1(cq))
    q_text = fill(F["q"], **{k: v for k, v in kw.items() if "{" + k + "}" in F["q"]})
    q_text = cap1(q_text)
    if side_txt:
        # the side clause attaches to the question sentence (the last sentence of a multi-sentence frame)
        m = list(re.finditer(r"[.?!] (?=[A-Z])", q_text))
        if m:
            cut = m[-1].end()
            q_text = q_text[:cut] + side_txt + low1(q_text[cut:])
        else:
            q_text = side_txt + low1(q_text)
    if look_pre:
        m = list(re.finditer(r"[.?!] (?=[A-Z])", q_text))
        if m:
            cut = m[-1].end()
            q_text = q_text[:cut] + look_pre + low1(q_text[cut:])
        else:
            q_text = look_pre + low1(q_text)
    instr = (look_sent + q_text + sep_txt).strip()
    # ---- yes / no lines
    style = spec["style"]
    yes_line = no_line = ""
    if style in ("yn", "YN") and not key_lines:
        if not F["yn"]:
            raise Reject("frame without yes/no lines")
        ykw = dict(c=c, cp=cp, doc=subj.doc, cneg="it does not hold that " + c)
        yes_line = fill(F["y"], **{k: v for k, v in ykw.items() if "{" + k + "}" in F["y"]})
        no_line = fill(F["n"], **{k: v for k, v in ykw.items() if "{" + k + "}" in F["n"]})
        if side_txt:
            yes_line = low1(side_txt) + yes_line
            no_line = low1(side_txt) + no_line
        if sep_y:
            yes_line += sep_y
            no_line += sep_y
    if key_lines and style not in ("yn", "YN"):
        raise Reject("key frame needs yes/no lines")
    extra = ([term_line] if term_line else []) + card_dist
    fw = frame_word(F)
    if fw:
        # 'contrary' (held out), 'opposite' and 'reverse' frames: the card defines the word as the plain denial, so
        # neither the contrary reading ('the opposite of none is all') nor the antonym label can be meant (decide2
        # finding #6; arbiter round 3, A4)
        extra.append((lx.CONTRARY_KEY, lx.frame_word_def(fw)))
    need_bival = True
    card = build_card(subj, extra, style, yes_line, no_line, need_bival, key_lines)
    # 'an attendance sheet', 'an action' (grammar, decide2 finding #5)
    instr, card = a_an(instr, subj.doc), a_an(card, subj.doc)
    # ---- LF
    x = CORE(subj.core())
    if ctype in ("AR", "ARC"):
        x = NOT(x, None)
    for i in reversed(inner_idx):
        x = NOT(x, i)
    if ctype == "CONTRAST":
        Y = subj.gB if subj.tA else subj.gA
        x = {"op": "AND", "children": [x, ATOM("fit:" + Y, True)]}
    if cd_idx is not None:
        x = NOT(x, cd_idx)
    for i in reversed(frame_idx):
        x = NOT(x, i)
    if key_idx is not None:
        x = NOT(x, key_idx)
    for i in dist_idx:
        x = DIST(x, i)
    embed = F["embed"] + (1 if ctype == "TERM" else 0)
    return RowDef(qtype="noul", instr=instr, card=card, cues=cues, lf=x, style=style, frame=F["id"],
                  family=F["family"], ctype=ctype, inner=inner, embed=embed, options=None, spec=spec,
                  pin=F["family"] == "polar_inner")


NEG1 = (("not",), ("n't",), ("fail",), ("non-",), ("in-",), ("rule out",), ("exclude",), ("lack",), ("miss",), ("cannot",))
NEG2 = (("not", "fail"), ("not", "non-"), ("not", "in-"), ("not", "rule out"), ("not", "exclude"), ("not", "lack"), ("not", "miss"),
        ("n't", "fail"))


def render_choice(subj, cs):
    """cs: frame (CHOICE_FRAMES id, or 'pack'), select, cue (lexeme or None), mode ('labels' | 'names' |
    'statements' | 'triage' | 'decoy'), opts [option descriptors], perm (display order). Returns a RowDef."""
    cues = []

    def add(lexeme, pos, scoping, dist, surface, cls=None):
        cues.append({"lexeme": lexeme, "cls": cls or lx.LEXICON[lexeme]["cls"], "position": pos, "scoping": scoping,
                     "distance": dist, "surface": surface, "_dist": False})
        return len(cues) - 1

    mode = cs["mode"]
    texts, lfs = [], []
    # r4: the options name the claim's subject when it is not the document itself (the frame asks about the document)
    opt_s = getattr(subj, "pron", "it") if subj.kind == "card" else "it"
    if mode in ("labels", "decoy"):
        for lab, lex in cs["opts"]:
            forms = _forms_get(lx.LABEL_FORMS, lex)
            forms = [f for f in forms if not ("non-" in lex and " " in lab)]
            if not forms:
                raise Reject(f"no label form {lex}")
            f = forms[cs.get("form_i", 0) % len(forms)]
            t = fill(_ph(f[0], L=lab), S=opt_s)
            idx = [add(x, "choice_option", True, "same_clause", find_surface(t, x)) for x in lex]
            x = CORE(ATOM("fit:" + lab, True))
            for i in reversed(idx):
                x = NOT(x, i)
            texts.append(t)
            lfs.append(x)
        pre = "Label definitions: " + subj.label_defs_text() + "."
    elif mode == "names":
        names = subj.option_names(cs["idx"])
        for i, nm in zip(cs["idx"], names):
            texts.append(nm)
            aid = (f"x{i + 1}" if subj.kind == "multitext" else f"x:{subj.names[i]}")
            lfs.append(CORE(ATOM(aid, True)))
        pre = subj.label_defs_text()
    elif mode == "statements":
        for i, lex in zip(cs["idx"], cs["lex"]):
            if subj.kind == "multitext":
                sp = subj.sp
                it = f"{subj.Item} {i + 1}"
                if not lex:
                    t = f"{it} {sp['sg']}"
                elif lex == ("not",):
                    t = f"{it} is not {sp['adj']}" if sp.get("adj") else f"{it} does not {sp['base']}"
                elif lex[0] in ("non-", "-free", "un-", "negadj") and sp.get("negadj"):
                    lex = (sp["negadj_aff"],)
                    t = f"{it} is {sp['negadj']}"
                else:
                    raise Reject("multitext statement form")
                aid = f"x{i + 1}"
            else:
                forms = subj.forms("P", lex)
                if not forms:
                    raise Reject("record statement form")
                t = fill(forms[cs.get("form_i", 0) % len(forms)][0], S=subj.subj_of(i))
                aid = f"x:{subj.names[i]}"
            idx = [add(x, "choice_option", True, "same_clause", find_surface(t, x)) for x in lex]
            x = CORE(ATOM(aid, True))
            for k in reversed(idx):
                x = NOT(x, k)
            texts.append(t)
            lfs.append(x)
        pre = subj.label_defs_text()
    elif mode == "ar":
        for i in cs["idx"]:
            if subj.kind == "multitext":
                t = f"{subj.Item} {i + 1} {subj.sp['comp_sg']}"
                aid = f"x{i + 1}"
            else:
                t = fill(subj.ar()[0][0], S=subj.subj_of(i))
                aid = f"x:{subj.names[i]}"
            texts.append(t)
            lfs.append(NOT(CORE(ATOM(aid, True)), None))
        pre = subj.label_defs_text()
        if subj.kind == "record" and subj.P.get("ar") and subj.P["ar"][2]:
            term, d = subj.P["ar"][2]
            pre = unquote(pre[:-1] + f"; {term} means {d}.")
    elif mode == "card_ar":
        for lab, is_ar in cs["opts"]:
            if is_ar:
                rest = [x for x in subj.labels if x != lab]
                names = ", ".join(f"'{x}'" for x in rest[:-1]) + (" or " if len(rest) > 1 else "") + f"'{rest[-1]}'"
                texts.append(f"the label that fits {opt_s} is {names}")
                lfs.append(NOT(CORE(ATOM("fit:" + lab, True)), None))
            else:
                texts.append(f"the label that fits {opt_s} is '{lab}'")
                lfs.append(CORE(ATOM("fit:" + lab, True)))
        pre = "Label definitions: " + subj.label_defs_text() + "."
    elif mode == "triage":
        o = lx.TRIAGE["options"]
        texts = list(o)
        lfs = [CORE(ATOM("note:yes", True)), CORE(ATOM("note:no", True)),
               NOT(CORE({"op": "OR", "children": [ATOM("note:yes", True), ATOM("note:no", True)]}),
                   add("nothing", "choice_option", True, "same_clause", "nothing"))]
        pre = subj.label_defs_text()
    else:
        raise ValueError(mode)
    perm = cs["perm"]
    texts = [texts[i] for i in perm]
    lfs = [lfs[i] for i in perm]
    if cs["frame"] == "pack":
        q = cs["q"]
        fid, fam = cs["fid"], "choice"
    else:
        CF = {f["id"]: f for f in lx.CHOICE_FRAMES}[cs["frame"]]
        q = fill(CF["q"], doc=subj.doc) if "{doc}" in CF["q"] else CF["q"]
        fid, fam = CF["id"], CF["family"]
    cue_idx = None
    if cs.get("cue"):
        cue_idx = add(cs["cue"], "outer_frame", True, "other_field", find_surface(q, cs["cue"]))
    lf = {"op": "CHOICE", "options": lfs, "select": cs["select"]}
    if cue_idx is not None:
        lf["cue"] = cue_idx
    instr = a_an((pre + " " + q).strip() if pre else q, subj.doc)
    texts = [a_an(t, subj.doc) for t in texts]
    for t in texts:
        if len(t) > 200 or "\n" in t:
            raise Reject("option too long")
    if len(set(texts)) != len(texts):
        raise Reject("duplicate options")
    return RowDef(qtype="choice", instr=instr, card=None, cues=cues, lf=lf, style="choice", frame=fid, family=fam,
                  ctype="CH", inner=(), embed=0, options=texts, spec=cs, pin=False)


# ============================================================================================ instantiate
def depth_of(lf):
    if lf["op"] == "CHOICE":
        return None
    r = lf_core(lf)
    return r[1]


def choice_eval(lf, vals):
    want = lf["select"] == "true"
    out = []
    for i, o in enumerate(lf["options"]):
        if lf_eval(set_atoms(o, vals)) == want:
            out.append(i)
    return out


def instantiate(subj, rd, twin, vals):
    """The row (golden format) + its sidecar meta for one twin."""
    if rd.qtype == "noul":
        lf = set_atoms(rd.lf, vals)
        gold = int(lf_eval(lf))
        core, depth = lf_core(lf)
        truthP = lf_eval(core["child"])
    else:
        lf = set_atoms(rd.lf, vals)
        g = choice_eval(lf, vals)
        if len(g) != 1:
            raise Reject(f"choice row: {len(g)} options evaluate to select")
        gold = g[0]
        core, d0 = lf_core(lf["options"][gold])
        depth = d0 + (1 if lf["select"] == "false" else 0)
        truthP = lf_eval(core["child"])
    return lf, gold, depth, truthP


# ============================================================================================ planner
CARD_PTYPES = {"label": 0.52, "ordinal": 0.18, "residual": 0.11, "group": 0.07, "excl": 0.05, "prop": 0.07}
MULTI_PTYPES = {"SOME": 0.30, "ALL": 0.14, "COUNT": 0.18, "FEW": 0.08, "BOTH": 0.08, "EITHER": 0.08, "EXCEPT": 0.14}
STYLE_TARGET = {"defs": 0.48, "yn": 0.42, "YN": 0.10}
ITEM_GOAL_MULT = 1.15


def cls5(c):
    return lx.CLASSES5.get(c, c)


def posg(p):
    return "yn_key+answer_map" if p in ("yn_key", "answer_map") else p


class Stats:
    """Running counts over the committed rows of one part (both twins counted)."""

    def __init__(self):
        self.rows = 0
        self.depth = Counter()
        self.cls = Counter()
        self.pos = Counter()
        self.cells = Counter()
        self.items = Counter()
        self.items_hold = Counter()
        self.lex_rows, self.lex_odd, self.lex_dist, self.lex_tok = Counter(), Counter(), Counter(), Counter()
        self.lex_rows_yn, self.lex_odd_yn = Counter(), Counter()
        self.frame_rows, self.frame_odd, self.family = Counter(), Counter(), Counter()
        self.dist_d, self.mis_d, self.n_d = Counter(), Counter(), Counter()
        self.style_d = Counter()
        self.kinds = Counter()
        self.ptypes = Counter()
        self.sources = Counter()
        self.choice = 0
        self.ch_pos = Counter()
        self.ch_neg = 0
        self.ch_even = 0
        self.rungs = Counter()
        self.ctypes = Counter()
        self.word_rows, self.word_odd = Counter(), Counter()
        self.cx = Counter()
        self.ch_src_n, self.ch_src_even = Counter(), Counter()
        self.tmpl_rows, self.tmpl_odd = Counter(), Counter()

    def add_row(self, meta, instr, frame, dev_kind):
        d = meta["depth"]
        odd = d % 2
        self.rows += 1
        self.depth[d] += 1
        self.rungs[meta["rung"]] += 1
        cues = meta["cues"]
        for c in cues:
            if c["cls"] != "lookalike":
                self.cls[cls5(c["cls"])] += 1
                self.lex_tok[c["lexeme"]] += 1
        for c in cues:
            if c["scoping"]:
                self.pos[posg(c["position"])] += 1
        for (p, cl) in {(c["position"], c["cls"]) for c in cues if c["scoping"]}:
            self.cells[(d, p, cl)] += 1
        for it in set(meta["phen"]):
            self.items[it] += 1
            if dev_kind == "holdout":
                self.items_hold[it] += 1
        for lexeme in {c["lexeme"] for c in cues}:
            self.lex_rows[lexeme] += 1
            self.lex_odd[lexeme] += odd
            if meta["qtype"] == "noul":
                self.lex_rows_yn[lexeme] += 1
                self.lex_odd_yn[lexeme] += odd
        for c in cues:
            if c.get("_dist"):
                self.lex_dist[c["lexeme"]] += 1
        self.frame_rows[frame] += 1
        self.frame_odd[frame] += odd
        self.family[meta["frame_family"]] += 1
        self.n_d[d] += 1
        if meta["n_distractor"]:
            self.dist_d[d] += 1
        if len(cues) % 2 != odd:
            self.mis_d[d] += 1
        if meta["qtype"] == "noul":
            self.style_d[(d, meta["card_style"])] += 1
            has_in = any(c["position"] == "inner_claim" and c["cls"] != "lookalike" for c in cues)
            has_out = any(c["position"] == "outer_frame" and c["cls"] != "lookalike" for c in cues)
            self.cx["c5n"] += 1
            self.cx["c5ok"] += 1 if has_in == bool(odd) else 0
            self.cx["c4n"] += 1
            self.cx["c4ok"] += 1 if has_out == bool(odd) else 0
            if odd:
                self.cx["oddn"] += 1
                sc = [c for c in cues if c["scoping"]]
                if meta["rung"] == "AR" or (sc and all(c["cls"] == "lexical" for c in sc)):
                    self.cx["arlex"] += 1
        else:
            self.choice += 1
            self.ch_neg += 1 if meta["select_false"] else 0
            self.ch_even += 1 if odd == 0 else 0
            if any(c["position"] == "choice_option" for c in cues):
                self.cx["ch_cue_odd" if odd else "ch_cue_even"] += 1
            self.ch_src_n[meta["source"]] += 1
            self.ch_src_even[meta["source"]] += 1 if odd == 0 else 0
        for w in set(re.findall(r"[a-z0-9]+", instr.lower())):
            self.word_rows[w] += 1
            self.word_odd[w] += odd


class Planner:
    def __init__(self, part, pools, dev_labels, seed, used_ids, log=print):
        self.part = part
        self.pools = pools
        self.dev_labels = dev_labels
        self.rng = random.Random(seed)
        self.bal = Bal(self.rng)
        self.st = Stats()
        self.used_ids = used_ids
        self.names_used = set()
        self.log = log
        self.n_lad = 0
        self.ladders = []
        self.rejects = Counter()
        self.split = "train" if part == "train" else "holdout" if part == "holdout" else "train"
        hold = part == "holdout"
        self.frames = [f for f in lx.FRAMES_LIST if (f["split"] == "train" or hold)]
        self.depth_target = {0: 0.176, 1: 0.25, 2: 0.292, 3: 0.263, 4: 0.019}
        if part != "train":
            self.depth_target = {0: 0.20, 1: 0.28, 2: 0.22, 3: 0.26, 4: 0.04}
        self.floor_col = 0 if part == "train" else (1 if part == "iid" else 2)
        self.kind_share = KIND_SHARE if part == "train" else KIND_SHARE_DEV
        # the pool is POOL_FACTOR x the kept set: absolute goals (item floors, cells, thin lexemes) scale with it
        self.sc = POOL_FACTOR[part]
        self.cell_goal = 40 * self.sc

    # ------------------------------------------------------------------ helpers
    def lexeme_ok(self, lexeme):
        s = lx.LEXICON[lexeme]["split"]
        return s == "train" or (s == "holdout" and self.part == "holdout")

    def item_goal(self, it):
        f = FLOORS[PRIORITY[it]]
        if self.part == "train":
            return f[0] * ITEM_GOAL_MULT * self.sc
        if self.part == "iid":
            return (f[1] - f[2]) * 1.3 * self.sc
        return f[2] * 1.3 * self.sc

    def depth_deficit(self, d):
        n = max(1, self.st.rows)
        return self.depth_target.get(d, 0) - self.st.depth[d] / n

    # ------------------------------------------------------------------ subjects
    def choose_kind(self):
        n = sum(self.st.kinds.values()) + 1
        ks = dict(self.kind_share)
        hold = self.part == "holdout"
        if all(k in getattr(self, "multi_dead", ()) for k, s in lx.MULTI_SOURCES.items()
               if (s["split"] == "holdout") == hold):
            ks.pop("multitext")
        return max(ks, key=lambda k: (ks[k] - self.st.kinds[k] / n, self.rng.random()))

    def card_keys(self, ptype):
        hold = self.part == "holdout"
        if ptype == "prop":
            ks = [k for k, s in lx.PROP_SOURCES.items() if (s["split"] == "holdout") == hold]
        else:
            ks = [k for k, s in lx.CARD_SOURCES.items() if (s["split"] == "holdout") == hold]
            if ptype == "ordinal":
                ks = [k for k in ks if lx.CARD_SOURCES[k].get("ordinal")]
            if ptype == "group":
                ks = [k for k in ks if k in lx.GROUPS]
            if ptype == "excl":
                ks = [k for k in ks if k in lx.EXCL_SOURCES]
        if self.part != "train":
            ks = [k for k in ks if self.pools.get(("prop" if ptype == "prop" else "card", k, "dev"))]
        return ks

    def make_subject(self, kind):
        rng = self.rng
        self._cur_src = None
        if kind == "card":
            pt = self.bal.least((self.part, "card_ptype"), list(CARD_PTYPES), CARD_PTYPES)
            keys = self.card_keys(pt)
            if not keys:
                raise Reject(f"no card source for {pt}")
            key = self.bal.least((self.part, "card_src", pt), keys)
            return CardSubject(rng, self.part, key, self.pools, self.used_ids, pt, self.dev_labels)
        if kind == "multitext":
            hold = self.part == "holdout"
            dead = self.__dict__.setdefault("multi_dead", set())
            mk = [k for k, s in lx.MULTI_SOURCES.items() if (s["split"] == "holdout") == hold and k not in dead]
            if not mk:
                raise Reject("every multi-text source is used up")
            mkey = self.bal.least((self.part, "multi_src"), mk)
            pt = self.bal.least((self.part, "multi_pt"), list(MULTI_PTYPES), MULTI_PTYPES)
            plans = self.multi_choice_plan(pt, self.n_plans(), lx.MULTI_SOURCES[mkey])
            try:
                return MultiSubject(rng, self.part, mkey, self.pools, self.used_ids, pt, plans)
            except Reject as e:
                if "too small" in str(e):
                    dead.add(mkey)
                raise
        hold = self.part == "holdout"
        pks = [k for k, s in lx.PACKS.items() if (s["split"] == "holdout") == hold]
        extra = ["deontic", "triage"] if not hold else ["deontic_h", "triage_h"]
        pk = self.bal.least((self.part, "pack"), pks + extra, {"deontic": 4.5, "triage": 1.3, "deontic_h": 1.6,
                                                                "triage_h": 1.3})
        self._cur_src = "f7_record:" + pk
        fmt = self.bal.least((self.part, "rfmt"), list(REC_FORMATS))
        if pk in ("triage", "triage_h"):
            return TriageSubject(rng, self.part, self.names_used, fmt,
                                 messages=lx.TRIAGE_H_MESSAGES if pk == "triage_h" else None)
        spec = {"deontic": lx.DEONTIC, "deontic_h": lx.DEONTIC_H}.get(pk) or lx.PACKS[pk]
        plans = self.record_choice_plan(spec, self.n_plans())
        s = PackSubject(rng, self.part, pk, self.names_used, fmt, plans, spec=spec)
        return s

    def n_plans(self):
        share = self.st.choice / max(1, self.st.rows)
        return 2 if share < CH_SHARE_TARGET + 0.03 else 1

    def record_choice_plan(self, spec, n_plans=1):
        """Choice-row plans for a record ladder (each plan: options = 3-5 items, a mode, a select value and the
        negations of every option). Modes: names (options are item names; a negated selection carries the cue),
        statements (every option is a P-wording with nneg negations), ar (every option is the pack's affirmative
        complement: a cue-less flip, so a negated selection over it reaches depth 2 with no option cue)."""
        rng = self.rng
        keys = list(spec["forms"])
        cues = [x for x in spec["choice"] if x != "true" and self.lexeme_ok(x)]
        has2 = any(len(x) == 2 for x in keys)
        plans = []
        used = set()
        for _ in range(n_plans):
            k = 3
            opts = [("names_true", 0, "true", 0, [])]
            if cues:
                opts.append(("names_false", 1, "false", 0, []))
            opts += [("stmt_false0", 1, "false", 0, []),
                     ("stmt_true1", 1, "true", k, [(1, "choice_option", c) for c in ("syntactic", "affixal", "lexical")]),
                     ("stmt_false1", 2, "false", k, [(2, "choice_option", c) for c in ("syntactic", "affixal", "lexical")])]
            if spec.get("ar"):
                opts += [("ar_true", 1, "true", 0, []), ("ar_false", 2, "false", 0, [])]
            if has2:
                opts += [("stmt_true2", 2, "true", 2 * k, [(2, "choice_option", c) for c in ("affixal", "lexical")]),
                         ("stmt_false2", 3, "false", 2 * k, [(3, "choice_option", c) for c in ("syntactic", "affixal",
                                                                                                "lexical")])]
            opts = [o for o in opts if o[0] not in used]
            name, d, sel, _, _ = self.choice_design(opts)
            used.add(name)
            # option count after the design: designs with option cues mostly take 3 options (the cue budget)
            if name.startswith("stmt_") and name[-1] != "0" and rng.random() < 0.75:
                k = 3
                self.bal.c[((self.part, "ch_k"), 3)] += 1
            else:
                k = self.bal.least((self.part, "ch_k"), [3, 4, 5])
            idx = [0] + rng.sample(range(1, 6), k - 1)
            rng.shuffle(idx)
            if name == "names_true":
                plans.append({"mode": "names", "select": "true", "cue": None, "idx": idx, "nneg": [0] * k,
                              "q": spec["choice"]["true"], "design": name})
                continue
            if name == "names_false":
                cue = min(cues, key=lambda x: (round(abs((self.st.lex_odd[x] + 2) / (self.st.lex_rows[x] + 2) - 0.5)
                                                     + self.word_tilt(spec["choice"][x], 1), 2), rng.random()))
                plans.append({"mode": "names", "select": "false", "cue": cue, "idx": idx, "nneg": [0] * k,
                              "q": spec["choice"][cue], "design": name})
                continue
            if name.startswith("ar_"):
                plans.append({"mode": "ar", "select": sel, "cue": None, "idx": idx, "nneg": [1] * k, "design": name})
                continue
            nneg = int(name[-1])
            lexs = self.pick_stmt_lex(keys, nneg, k, d) if nneg else [() for _ in range(k)]
            if lexs is None:
                continue
            plans.append({"mode": "statements", "select": sel, "cue": None, "idx": idx, "nneg": [nneg] * k,
                          "lex": lexs, "design": name})
        return plans

    def multi_choice_plan(self, pt, n_plans=1, sp=None):
        """Multi-text choice plans (options = three of the numbered texts). SOME / ALL / BOTH / EITHER ladders have
        none: one twin has no (or every) text with the property, so no 'exactly one option' row exists for both."""
        if pt in ("SOME", "ALL"):
            return []
        rng = self.rng
        plans, used = [], set()
        for _ in range(n_plans):
            k = 3
            idx = [0, 1, 2]
            opts = [("names_true", 0, "true", 0, []), ("names_false", 1, "false", 0, []),
                    ("stmt_false0", 1, "false", 0, [])]
            if sp is None or sp.get("comp_sg"):
                opts += [("ar_true", 1, "true", 0, []), ("ar_false", 2, "false", 0, [])]
            opts += [
                    ("stmt_true1", 1, "true", k, [(1, "choice_option", "syntactic")]),
                    ("stmt_false1", 2, "false", k, [(2, "choice_option", "syntactic"), (2, "choice_option", "affixal")])]
            opts = [o for o in opts if o[0] not in used]
            name, d, sel, _, _ = self.choice_design(opts)
            used.add(name)
            if name.startswith("names"):
                plans.append({"mode": "names", "select": sel, "cue": "not" if sel == "false" else None, "idx": idx,
                              "nneg": [0] * k, "design": name})
            elif name.startswith("ar_"):
                plans.append({"mode": "ar", "select": sel, "cue": None, "idx": idx, "nneg": [1] * k, "design": name})
            else:
                nneg = int(name[-1])
                lexs = [() for _ in range(k)] if nneg == 0 else [("not",) for _ in range(k)]
                if nneg:
                    lexs[rng.randrange(k)] = rng.choice([("not",), ("negadj",)])   # one 'non-X' word per row (X12)
                plans.append({"mode": "statements", "select": sel, "cue": None, "idx": idx, "nneg": [nneg] * k,
                              "lex": lexs, "design": name})
        return plans

    def least_lex(self, lexs, odd):
        """The lexeme whose odd-parity share most needs a row of this parity (then the least used)."""
        st = self.st

        def key(x):
            n, o = st.lex_rows[x], st.lex_odd[x]
            return (abs((o + odd + 1) / (n + 2) - 0.5), n, self.rng.random())
        return min(lexs, key=key)

    # ------------------------------------------------------------------ yes/no row combos
    def inner_keys(self, subj, ctype):
        """Inner lexeme tuples with a wording for this subject and claim type."""
        cache_key = (subj.uid, ctype)
        if cache_key in getattr(self, "_ik", {}):
            return self._ik[cache_key]
        if not hasattr(self, "_ik"):
            self._ik = {}
        if ctype in ("TERM",):
            keys = list(lx.TERM_FORMS)
        elif ctype in ("AR", "ARC"):
            keys = [()] if subj.ar() else []
        else:
            cand = set(lx.LABEL_FORMS) | set(lx.ONLY_FORMS) | set(lx.CONTRAST_FORMS) | set(lx.RESIDUAL_FORMS) | \
                set(lx.TERM_FORMS)
            if subj.kind == "record":
                cand |= set(subj.P["forms"])
            if subj.kind == "card" and subj.isprop:
                cand |= set(subj.S["forms"])
            if subj.kind == "multitext":
                cand |= {(), ("none",), ("no",), ("not a single",), ("non-",), ("-free",), ("un-",), ("not", "un-"),
                         ("not", "non-"),
                         ("not", "-free"), ("not one",), ("not all",), ("not every",), ("no more than",), ("few",),
                         ("not",), ("neither",)}
            keys = [k for k in cand if subj.forms(ctype, k)]
        keys = [k for k in keys if all(self.lexeme_ok(x) for x in k)]
        self._ik[cache_key] = keys
        return keys

    def carddefs(self, subj):
        out = []
        for lexeme in ("not", "n't", "fail", "lack", "exclude", "rule out", "non-", "unless", "never", "without", "no",
                       "none", "not every", "neither", "un-", "-free", "dis-", "in-", "im-", "il-", "-less", "refuse",
                       "skip", "miss", "omit", "absent", "cannot", "reject", "withhold", "avoid", "decline", "nothing",
                       "nobody", "no one", "a-", "no longer", "ir-", "veto", "abstain"):
            if not self.lexeme_ok(lexeme):
                continue
            try:
                td = subj.term_def(lexeme)
            except (ValueError, KeyError):
                td = None
            if td:
                out.append(lexeme)
        return out

    def combos(self, subj):
        """Every (frame, ctype, inner, carddef) this subject can render, with its depth and scoping signature."""
        key = subj.uid
        if getattr(self, "_cmb_key", None) == key:
            return self._cmb
        out = []
        ctypes = ["P"]
        cds = self.carddefs(subj)
        if cds:
            ctypes.append("TERM")
        if subj.ar():
            ctypes.append("ARC")
        if subj.kind == "card" and subj.ptype in ("label", "ordinal"):
            ctypes.append("ONLY")
        if subj.kind == "card" and subj.ptype == "label":
            ctypes.append("CONTRAST")
        for F in self.frames:
            fc = [(c[2] if len(c) > 2 else F["pos"], lx.LEXICON[c[0]]["cls"], c[3] if len(c) > 3 else F["dist"])
                  for c in F["cues"]]
            for ct in ctypes:
                for inner in self.inner_keys(subj, ct):
                    if ct == "ARC" and inner:
                        continue
                    for cd in (cds if ct == "TERM" else [None]):
                        sc = list(fc) + [("inner_claim", lx.LEXICON[x]["cls"], "same_clause") for x in inner]
                        if cd:
                            sc.append(("card_def", lx.LEXICON[cd]["cls"], "other_field"))
                        d = len(sc) + (1 if ct == "ARC" else 0)
                        if d > 4:
                            continue
                        c5 = {cls5(x[1]) for x in sc}
                        if self.part != "holdout" and "truth_frame" in c5 and "cross+answer" in c5:
                            continue      # held-out combinations (rule 2.10) never occur in train or iid
                        if F["needs"] in ("cq", "cqn"):
                            fm = (subj.forms(ct, inner) if ct not in ("TERM",) else
                                  _forms_get(lx.TERM_FORMS, inner)) if ct != "ARC" else subj.ar()
                            if not any(f[1 if F["needs"] == "cq" else 2] for f in fm):
                                continue
                        base = {"frame": F["id"], "ctype": ct, "inner": inner, "carddef": cd, "depth": d,
                                "sc": tuple(sorted(sc)), "null": ct == "ARC", "ynkey": None}
                        if F["family"] == "key":
                            out.append(dict(base, ynkey="pos"))
                            if d < 4:
                                sc2 = tuple(sorted(sc + [("yn_key", "answer_mapping", "other_field")]))
                                out.append(dict(base, ynkey="inv", depth=d + 1, sc=sc2))
                        else:
                            out.append(base)
        self._cmb_key, self._cmb = key, out
        return out

    def sig_tags(self, d, sc, null):
        """Items implied by a scoping signature (same reading as item_tags_rule; distractor items come later)."""
        cues = [{"position": p, "cls": c, "distance": dd, "scoping": True} for p, c, dd in sc]
        return item_tags_rule(d, cues, 0, False, False, False, False, None, "") - {1, 15, 16, 17, 18, 19, 20, 36, 38}

    def score_sig(self, d, sc, null):
        """Signature score (lower = better): class / position deficits per token, cells and items under goal,
        C4 / C5 balance, AR + lexical-only odd flips."""
        st = self.st
        T = sum(st.cls.values()) + 1
        P = sum(st.pos.values()) + 1
        s = 0.0
        for p, c, _ in sc:
            k5 = cls5(c)
            s -= 120 * (CLASS_TARGET[k5] - st.cls[k5] / T)
            pg = posg(p)
            s -= 250 * (POS_TARGET.get(pg, 0) - st.pos[pg] / P)
        cell_goal = self.cell_goal if self.part == "train" else 0
        if cell_goal:
            for (p, c, _) in set(sc):
                if c in ALLOWED_CELLS.get(p, ()) and d in (1, 2, 3):
                    s -= 3.0 * max(0.0, cell_goal - st.cells[(d, p, c)]) / cell_goal
        for it in self.sig_tags(d, sc, null):
            g = self.item_goal(it)
            s -= 3.0 * max(0.0, g - self.item_count(it)) / g
        par = d % 2
        has_in = any(p == "inner_claim" for p, _, _ in sc)
        has_out = any(p == "outer_frame" for p, _, _ in sc)
        for key, has in (("c5", has_in), ("c4", has_out)):
            n = st.cx[key + "n"] + 1
            acc = st.cx[key + "ok"] / n
            ok = (has and par == 1) or (not has and par == 0)
            s += (acc - 0.5) * 40 * (1 if ok else -1)
        if par == 1:
            odd_n = st.cx["oddn"] + 1
            arl = st.cx["arlex"] / odd_n
            lexonly = bool(sc) and all(c == "lexical" for _, c, _ in sc)
            if arl < 0.20 and lexonly:
                s -= 10.0
        return s + self.rng.random() * 0.15

    def concrete_score(self, subj, cmb, parity):
        st = self.st
        F = lx.FRAMES[cmb["frame"]]
        lexs = [c[0] for c in F["cues"]] + list(cmb["inner"]) + ([cmb["carddef"]] if cmb["carddef"] else [])
        if cmb.get("ynkey") == "inv":
            lexs.append("fails to hold")
        s = 0.0
        tot = sum(st.lex_tok.values()) + 1
        notnt = (st.lex_tok["not"] + st.lex_tok["n't"]) / tot
        goal = 40 * self.sc if self.part == "train" else 0
        hgoal = 14 * self.sc
        sgn = 1 if parity == 1 else -1
        for x in lexs:
            # a yes/no row steers the lexeme's yes/no-row parity (6.CS); choice rows pick their frames by the
            # all-row parity (4.12), so the two do not pull against each other
            n, o = (st.lex_rows_yn[x], st.lex_odd_yn[x]) if st.lex_rows_yn[x] >= 16 else (st.lex_rows[x], st.lex_odd[x])
            sh = (o + 1) / (n + 2)
            w = min(1.0, (n + 1) / 16)
            s += 75 * sgn * (sh - 0.5) * w
            if sgn * (sh - 0.5) > 0.05:
                s += 6 * w
            n = st.lex_rows[x]
            if goal and n < goal:
                s -= 1.2 * (goal - n) / goal
            if self.part == "holdout" and lx.LEXICON[x]["split"] == "holdout" and n < hgoal:
                s -= 2.0 * (hgoal - n) / hgoal
            if x in ("not", "n't") and notnt > NOT_NT_CAP:
                s += 40 * (notnt - NOT_NT_CAP) + 1.0
            s += 60 * max(0.0, st.lex_tok[x] / tot - 0.055) + 250 * max(0.0, st.lex_tok[x] / tot - 0.075)
        fr = cmb["frame"]
        n, o = st.frame_rows[fr], st.frame_odd[fr]
        s += 30 * sgn * ((o + 1) / (n + 2) - 0.5) * min(1.0, (n + 1) / 16)
        if st.rows > 200 and n / st.rows > 0.032:
            s += 12.0
        if self.part == "holdout" and F["split"] == "holdout":
            s -= 1.0
        fam = F["family"]
        nf = sum(st.family.values()) + 1
        s += 3 * (st.family[fam] / nf)
        # instruction words (SPEC 7.3 cue-share rule): keep every word's odd-row share near half
        for w in self.combo_words(subj, cmb):
            nw = st.word_rows[w]
            if nw >= 10:
                sh = st.word_odd[w] / nw
                if sh > 0.53:
                    s += sgn * 100 * (sh - 0.53)
        return s + self.rng.random() * 0.2

    def combo_words(self, subj, cmb):
        key = (subj.uid, cmb["frame"], cmb["ctype"], tuple(cmb["inner"]), cmb["carddef"])
        if not hasattr(self, "_cw"):
            self._cw = {}
        if key in self._cw:
            return self._cw[key]
        F = lx.FRAMES[cmb["frame"]]
        txt = F["q"]
        try:
            if cmb["ctype"] == "TERM":
                fm = _forms_get(lx.TERM_FORMS, cmb["inner"])
            elif cmb["ctype"] in ("AR", "ARC"):
                fm = subj.ar()
            else:
                fm = subj.forms(cmb["ctype"], cmb["inner"])
            txt += " " + " ".join(x for f in fm for x in f if x)
        except Exception:  # noqa: BLE001
            pass
        if cmb["ctype"] == "TERM" and cmb["carddef"]:
            try:
                td = subj.term_def(cmb["carddef"])
                if td and len(td) > 2 and td[2]:
                    txt += " " + td[2]
            except (ValueError, KeyError):
                pass
        txt = re.sub(r"\{[^{}]*\}", " ", txt).lower()
        words = set(re.findall(r"[a-z0-9]+", txt))
        self._cw[key] = words
        return words

    def pick_yn(self, subj, depth, forbid_ctypes=(), req=None, with_score=False, used=()):
        cmbs = [c for c in self.combos(subj) if c["depth"] == depth and c["ctype"] not in forbid_ctypes
                and combo_key(c) not in used
                and (lx.FRAMES[c["frame"]]["family"] != "polar_inner" or (req and req["name"] == "item38"))
                and not (depth == 4 and (lx.FRAMES[c["frame"]]["family"] in ("key", "polar_inner") or
                                         not lx.FRAMES[c["frame"]]["yn"]))]
        if req:
            rc = [c for c in cmbs if req["f"](c)]
            if rc:
                cmbs = rc
        if not cmbs:
            raise Reject(f"no combo at depth {depth}")
        sigs = defaultdict(list)
        for c in cmbs:
            sigs[(c["sc"], c["null"])].append(c)
        par = depth % 2
        cand = []
        for k, lst in sigs.items():
            ss = self.score_sig(depth, k[0], k[1])
            pick = lst if len(lst) <= 8 else self.rng.sample(lst, 8)
            cand += [(ss, c) for c in pick]
        best = min(((sc[0] + self.concrete_score(subj, sc[1], par), i) for i, sc in enumerate(cand)))
        if with_score:
            return best[0], dict(cand[best[1]][1])
        return dict(cand[best[1]][1])

    def pick_yn_free(self, subj, ds, forbid_ctypes, taken, req=None, used=()):
        """A free N-rung: depth and combo chosen together (the combo score, which carries the lexeme / word parity
        terms, plus the depth deficit), so a combo whose lexemes lean odd goes to an even depth and vice versa."""
        st = self.st
        n = max(1, st.rows)
        best = None
        for d in ds:
            deficit = self.depth_target[d] - (st.depth[d] + 2 * taken[d]) / (n + 2 * (1 + sum(taken.values())))
            try:
                sc, cmb = self.pick_yn(subj, d, forbid_ctypes, req, with_score=True, used=used)
            except Reject:
                continue
            if req and not req["f"](cmb):
                sc += 50.0                    # the requirement cannot be met at this depth
            tot = sc - DEPTH_PULL * deficit
            if best is None or tot < best[0]:
                best = (tot, d, cmb)
        if best is None:
            raise Reject("no free combo")
        return best[1], best[2]

    # ------------------------------------------------------------------ rungs
    def supports_choice(self, subj):
        if subj.kind == "card":
            return subj.ptype in ("label", "ordinal") and len(subj.labels) >= 3
        if isinstance(subj, TriageSubject):
            return True
        return bool(subj.choice_plans)

    def rung_plan(self, subj):
        """The ladder's rungs: R0 (80-85% of train ladders, every dev ladder), choice rows, AR / D now and then, and
        N-rungs whose depths steer the depth mix. Quota rows (item floors, thin lexemes, held-out elements) carry a
        requirement on the combo; their depth is one the subject can render the requirement at."""
        rng, st = self.rng, self.st
        plan = []
        n_lad = max(1, 2 * len(self.ladders))
        r0 = self.part != "train" or (st.rungs["R0"] / n_lad < R0_SHARE + 0.008) or rng.random() < 0.3
        if r0:
            plan.append({"rung": "R0", "depth": 0})
        if self.supports_choice(subj):
            share = st.choice / max(1, st.rows)
            if subj.kind != "card" or (share < CH_SHARE_TARGET + 0.01 and rng.random() < 0.97):
                plan.append({"rung": "CH", "depth": None})
            if subj.kind == "card" and share < CH_SHARE_TARGET and rng.random() < 0.3:
                plan.append({"rung": "CH", "depth": None})
            if subj.kind in ("record", "multitext") and len(getattr(subj, "choice_plans", [])) > 1:
                plan.append({"rung": "CH", "depth": None})
        if subj.ar() and rng.random() < 0.35:
            arw = set(WORD_RE.findall(" ".join(x for f in subj.ar() for x in f if x).lower())) - _stop()
            arw = {w for w in arw if not w.startswith("{")}
            if all(st.word_rows[w] < 12 or st.word_odd[w] / st.word_rows[w] <= 0.5 for w in arw):
                plan.append({"rung": "AR", "depth": 1})
        if rng.random() < 0.10:
            plan.append({"rung": "D", "depth": None})
        # keep room for >= 2 N-rungs (an odd one, and an even one when there is no R0)
        for drop in ("D", "AR", "CH"):
            while 5 - len(plan) < 2 and any(p["rung"] == drop for p in plan) and \
                    (drop != "CH" or sum(1 for p in plan if p["rung"] == "CH") > 1):
                plan.remove(next(p for p in reversed(plan) if p["rung"] == drop))
        n_yn = 5 - len(plan)
        n = max(1, st.rows)
        tmp = Counter()

        def deficit(d):
            return self.depth_target[d] - (st.depth[d] + 2 * tmp[d]) / (n + 2 * (1 + sum(tmp.values())))
        allow4 = (self.depth_target[4] - st.depth[4] / n) > 0 and (self.part != "train" or st.depth[4] / n < 0.024)
        cmbs = self.combos(subj)
        rungs = []
        for req in self.quota_reqs(subj)[:n_yn]:
            ds = sorted({c["depth"] for c in cmbs if req["f"](c) and c["depth"] >= req.get("min_depth", 1)
                         and (c["depth"] < 4 or allow4)})
            if not ds:
                continue
            lexs = req.get("lexemes") or []
            wds = req.get("words") or []

            def rscore(x):
                par = 0.0
                if req.get("dev") is not None:
                    par += req["dev"] * (1 if x % 2 else -1) * 2
                for lx_ in lexs:
                    nn, oo = st.lex_rows[lx_], st.lex_odd[lx_]
                    par += ((oo + 1) / (nn + 2) - 0.5) * (1 if x % 2 else -1)
                for w in wds:
                    nn, oo = st.word_rows[w], st.word_odd[w]
                    par += 2 * ((oo + 1) / (nn + 2) - 0.5) * (1 if x % 2 else -1)
                return 50 * deficit(x) - 6.0 * par + rng.random() * 1e-3
            d = max(ds, key=rscore)
            tmp[d] += 1
            rungs.append({"rung": f"N{d}", "depth": d, "req": req, "free": ds})
        while len(rungs) < n_yn:
            ds = [1, 2, 3, 4] if allow4 else [1, 2, 3]
            d = max(ds, key=lambda x: (deficit(x), rng.random()))
            tmp[d] += 1
            rungs.append({"rung": f"N{d}", "depth": d, "free": ds})
        # every N-rung gets its depth together with its combo (make_pair), within its allowed depths; the ladder needs
        # an odd N-rung, and an even one when it has no R0
        def restrict(par):
            for r in sorted(rungs, key=lambda r: "req" in r):         # free rungs first, then quota rungs
                opt = [x for x in r["free"] if x % 2 == par]
                if opt and not any(all(x % 2 == par for x in q["free"]) for q in rungs):
                    r["free"] = opt
                    return True
            return any(all(x % 2 == par for x in q["free"]) for q in rungs)
        if not restrict(1):
            rungs[-1].update(rung="N1", depth=1, free=[1])
            rungs[-1].pop("req", None)
        if not r0 and not restrict(0):
            tgt = next((r for r in rungs if not all(x % 2 for x in r["free"])), rungs[0])
            tgt.update(rung="N2", depth=2, free=[2])
            tgt.pop("req", None)
        return plan + rungs

    def quota_reqs(self, subj):
        """Requirements for this ladder's rows: items still under their goal, thin lexemes, held-out elements."""
        rng = self.rng
        need = lambda it: self.item_count(it) < self.item_goal(it)  # noqa: E731
        out = []
        if self.part == "holdout" and subj.kind == "record":
            out.append({"name": "hold_elem", "f": lambda c: lx.FRAMES[c["frame"]]["split"] == "holdout" or any(
                lx.LEXICON[x]["split"] == "holdout" for x in tuple(c["inner"]) + ((c["carddef"],) if c["carddef"] else ()))})
        if subj.kind == "card" and subj.ptype == "ordinal" and need(21):
            out += [{"name": "item21", "lexemes": ["not", "n't"],
                     "f": lambda c: c["ctype"] == "P" and c["inner"] and c["inner"][-1] in ("not", "n't")}] * 2
        if subj.kind == "multitext" and subj.ptype == "SOME" and need(27):
            out += [{"name": "item27", "lexemes": [subj.sp["negadj_aff"]] if subj.sp.get("negadj_aff") else [],
                     "words": [w for w in re.findall(r"[a-z]+", subj.sp.get("negadj") or "") if w not in ("non", "free")],
                     "f": lambda c: bool({"non-", "-free", "un-"} & set(c["inner"])) and
                     any(p == "outer_frame" for p, _, _ in c["sc"]), "min_depth": 2}] * 3
        if getattr(subj, "pkey", None) in ("deontic", "deontic_h") and need(33):
            out += [{"name": "item33", "lexemes": ["need not", "must not", "forbid", "cannot"],
                     "f": lambda c: bool({"need not", "must not", "cannot", "forbid"} & set(c["inner"]))}] * 2
        if subj.kind == "multitext" and subj.ptype == "FEW":
            out.append({"name": "few", "lexemes": ["few"], "f": lambda c: "few" in c["inner"]})
        if subj.kind == "card" and subj.ptype in ("label", "ordinal") and need(24) and rng.random() < 0.7:
            out.append({"name": "item24", "f": lambda c: c["ctype"] == "ONLY"})
        if subj.kind == "card" and subj.ptype == "label" and need(32) and rng.random() < 0.6:
            out.append({"name": "item32", "f": lambda c: c["ctype"] == "CONTRAST"})
        if need(34) and rng.random() < 0.5:
            out.append({"name": "item34", "f": lambda c: c["ctype"] == "TERM" and c["carddef"] == "unless"})
        if need(38) and self.st.rows and self.item_count(38) / self.st.rows < 0.035 and rng.random() < 0.6:
            out.append({"name": "item38", "f": lambda c: lx.FRAMES[c["frame"]]["family"] == "polar_inner"})
        if need(14) and rng.random() < 0.4:
            out.append({"name": "item14", "f": lambda c: c.get("ynkey") == "inv",
                        "lexemes": ["fails to hold", "is false of"]})
        if need(2) and rng.random() < 0.5:
            out.append({"name": "item2", "f": lambda c: c["depth"] == 1 and any(
                p == "inner_claim" and cl == "syntactic" for p, cl, _ in c["sc"])})
        if need(5) and rng.random() < 0.5:
            out.append({"name": "item5", "f": lambda c: c["depth"] == 1 and any(cl == "affixal" for _, cl, _ in c["sc"])})
        # rule-defined items (2-14) and depth x position x class cells still under their goal
        defs = []
        for it in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14):
            g = self.item_goal(it)
            if self.item_count(it) < g:
                defs.append(((self.item_count(it) / g), "it%d" % it,
                             (lambda c, _it=it: _it in self.sig_tags(c["depth"], c["sc"], c["null"]))))
        if self.part == "train":
            for p_, cls_ in ALLOWED_CELLS.items():
                if p_ == "choice_option":
                    continue
                for c_ in cls_:
                    for d_ in (1, 2, 3):
                        n_ = self.st.cells[(d_, p_, c_)]
                        if n_ < self.cell_goal:
                            defs.append((n_ / self.cell_goal, f"cell{d_}{p_}{c_}",
                                         (lambda c, _d=d_, _p=p_, _c=c_: c["depth"] == _d and any(
                                             x[0] == _p and x[1] == _c for x in c["sc"]))))
        defs.sort(key=lambda x: x[0])
        for _, nm, f in defs[:2]:
            out.append({"name": nm, "f": f})
        # thin lexemes (each train lexeme in >= 30 rows; held-out lexemes in holdout rows)
        goal = 40 * self.sc if self.part == "train" else 14 * self.sc
        st = self.st
        avail = set()
        for c in self.combos(subj):
            F = lx.FRAMES[c["frame"]]
            avail |= {x[0] for x in F["cues"]} | set(c["inner"]) | ({c["carddef"]} if c["carddef"] else set())
        thin = [x for x in avail if st.lex_rows[x] < goal and (self.part == "train" or
                                                               lx.LEXICON[x]["split"] == "holdout")]
        thin.sort(key=lambda x: (st.lex_rows[x], rng.random()))
        def dev_(x):
            d_all = st.lex_odd[x] / st.lex_rows[x] - 0.5
            d_yn = (st.lex_odd_yn[x] / st.lex_rows_yn[x] - 0.5) if st.lex_rows_yn[x] >= 16 else 0.0
            return d_yn if abs(d_yn) > abs(d_all) else d_all
        tot_tok = sum(st.lex_tok.values()) + 1
        imb = sorted((x for x in avail if st.lex_rows[x] >= 16 and x not in thin and st.lex_tok[x] / tot_tok < 0.06),
                     key=lambda x: -abs(dev_(x)))
        for x in imb[:2]:
            if abs(dev_(x)) > 0.025:
                out.append({"name": "par:" + x, "lexemes": [x], "dev": dev_(x),
                            "f": (lambda c, _x=x: _x in set(c["inner"]) or _x == c["carddef"] or
                                  _x in {y[0] for y in lx.FRAMES[c["frame"]]["cues"]})})
        for x in thin[:2]:
            out.append({"name": "lex:" + x, "lexemes": [x],
                        "f": (lambda c, _x=x: _x in set(c["inner"]) or _x == c["carddef"] or
                              _x in {y[0] for y in lx.FRAMES[c["frame"]]["cues"]})})
        head = [r for r in out if r["name"] in ("hold_elem", "item21", "item27", "item33")]
        tail = [r for r in out if r not in head]
        rng.shuffle(tail)
        return head + tail



    def item_count(self, it):
        if self.part == "holdout":
            return self.st.items_hold[it]
        return self.st.items[it]

    # ------------------------------------------------------------------ special rows
    def r0_spec(self, subj):
        cmbs = [c for c in self.combos(subj) if c["depth"] == 0 and c["ctype"] == "P" and not c["inner"]]
        if not cmbs:
            raise Reject("no R0 combo")
        return dict(min(cmbs, key=lambda c: self.concrete_score(subj, c, 0)))

    def ar_spec(self, subj):
        cmbs = [c for c in self.combos(subj) if c["ctype"] == "ARC" and c["depth"] == 1 and not c["sc"]]
        if not cmbs:
            raise Reject("no AR combo")
        c = dict(min(cmbs, key=lambda c: self.concrete_score(subj, c, 1)))
        c["ctype"] = "AR"
        return c

    def extras(self, subj, spec, rung, depth):
        """Distractors, look-alike and card style. Steers: distractor share and parity mismatch per depth, the class
        mix, the >= 10% distractor-use rule of distractor-capable lexemes, lexeme parity, and style shares per depth."""
        st, rng = self.st, self.rng
        F = lx.FRAMES[spec["frame"]]
        cpos = [c[2] if len(c) > 2 else F["pos"] for c in F["cues"]]
        n_outer, n_sep = cpos.count("outer_frame"), cpos.count("separate_sentence")
        nd = max(1, st.n_d[depth])
        want_odd = st.mis_d[depth] / nd < 0.49
        # distractors lean to even depths (they carry fewer scoping cues), which keeps each lexeme's rows near 50/50
        want_dist = st.dist_d[depth] / nd < (0.70 if depth % 2 == 0 else 0.29)
        kinds_ok = ["card"]
        if rung not in ("R0", "AR"):        # R0: no negation word in the question (rung semantics, precheck 9.6)
            kinds_ok += (["side"] if n_outer < 2 else []) + (["sep"] if n_sep < 2 else [])
        if want_odd:
            opts = [(1, 0), (0, 1)] if want_dist else [(0, 1), (1, 0)]
        else:
            opts = [(1, 1), (2, 0), (0, 0)] if want_dist else [(0, 0), (1, 1)]
        if depth == 0 and self.item_count(17) < self.item_goal(17) and not want_odd and rng.random() < 0.4:
            opts = [(2, 0)] + opts
        n_dist, n_look = opts[0] if rng.random() < 0.85 else rng.choice(opts)
        T = sum(st.cls.values()) + 1
        cls_need = {k: CLASS_TARGET[k] - st.cls[k] / T for k in CLASS_TARGET}
        dists = []
        par = depth % 2
        for _ in range(n_dist):
            cands = []
            for kind in kinds_ok:
                if kind != "card" and any(k == kind for k, _ in dists):
                    continue
                table = {"side": lx.DIST_SIDE, "sep": lx.DIST_SEP, "card": lx.DIST_CARD}[kind]
                for i, row in enumerate(table):
                    x = row[0]
                    if not self.lexeme_ok(x) or (kind, i) in dists or not dist_fits(subj, F, kind, row):
                        continue
                    if kind == "card" and row[2] == lx.RESIDUAL_NAME and (subj.kind != "card" or subj.ptype == "residual"):
                        continue
                    if kind == "card" and any(lx.DIST_CARD[j][2] == row[2] for k2, j in dists if k2 == "card"):
                        continue
                    cands.append((kind, i, x))
            if not cands:
                break

            def dkey(c):
                kind, i, x = c
                use = st.lex_tok[x] + 1
                tot_ = sum(st.lex_tok.values()) + 1
                # the >= 10% distractor-use rule (CL:351, every distractor-capable lexeme): a bonus while the lexeme is
                # under 13%, growing with the shortfall, never a lexicographic win
                sh_ = st.lex_dist[x] / use
                need = (3.0 + 30.0 * max(0.0, 0.13 - sh_)) if (can_distract(x) and sh_ < 0.13) else 0.0
                share_pen = 80.0 * max(0.0, st.lex_tok[x] / tot_ - 0.05)
                n, o = st.lex_rows[x], st.lex_odd[x]
                pdev = abs((o + par + 0.5) / (n + 1) - 0.5)
                tn, to = st.tmpl_rows[(kind, i)], st.tmpl_odd[(kind, i)]
                pdev += 3 * abs((to + par + 0.5) / (tn + 1) - 0.5) * min(1.0, (tn + 1) / 10)
                if kind != "card":
                    trow = {"side": lx.DIST_SIDE, "sep": lx.DIST_SEP}[kind][i]
                    pdev += 15 * max(0.0, self.word_tilt(" ".join(x for x in trow[1:] if isinstance(x, str)), par))
                cn = cls_need.get(cls5(lx.LEXICON[x]["cls"]), 0)
                kb = self.bal.c[(self.part, "dkind", kind)] / {"card": 1.0, "side": 1.6, "sep": 0.9}[kind]
                # template variety (rule 2.8 'cue variety beats volume'): a template's uses so far weigh against it
                tn_all = self.bal.c[(self.part, "dtmpl", kind, i)]
                c4 = 0.0
                if kind == "side":
                    acc4 = st.cx["c4ok"] / (st.cx["c4n"] + 1)
                    has_out_already = n_outer > 0
                    if not has_out_already and acc4 > 0.53:
                        c4 = (acc4 - 0.5) * 40 * (1 if par == 1 else -1)
                return -need + share_pen - cn * 20 + pdev * 8 + kb * 0.002 + c4 + tn_all / 250.0 + rng.random() * 0.3
            kind, i, x = min(cands, key=dkey)
            self.bal.c[(self.part, "dkind", kind)] += 1
            self.bal.c[(self.part, "dtmpl", kind, i)] += 1
            dists.append((kind, i))
        look = None
        if n_look:
            ls = list(lx.LOOKALIKES)
            look = min(ls, key=lambda x: (st.lex_rows[x] // 6, abs((st.lex_odd[x] + par + 0.5) / (st.lex_rows[x] + 1)
                                                                  - 0.5), rng.random()))
        fam = F["family"]
        tot = Counter()
        for (dd, s_), v in st.style_d.items():
            tot[s_] += v
        T_ = sum(tot.values())
        share = {s_: (tot[s_] / T_ if T_ > 60 else STYLE_TARGET[s_]) for s_ in STYLE_TARGET}
        nd_y = sum(st.style_d[(depth, s_)] for s_ in STYLE_TARGET)
        deficit = lambda s_: share[s_] * (nd_y + 2) - st.style_d[(depth, s_)]  # noqa: E731
        if not F["yn"]:
            style = "defs"
        elif fam in ("key", "polar_inner"):
            style = max(("yn", "YN"), key=lambda s_: (deficit(s_) / STYLE_TARGET[s_], rng.random()))
        else:
            style = max(STYLE_TARGET, key=lambda s_: (deficit(s_), rng.random()))
        return dists, look, style

    # ------------------------------------------------------------------ choice rows
    def pick_perm(self, k, gpos, sel="true"):
        """A display order that puts the twins' gold options on the least-used positions (per option count), so the
        gold position stays uniform (checklist section 3: +- 3 points per position)."""
        rng = self.rng
        cnt = lambda p: 3 * self.bal.c[(self.part, "chpos", k, p)] + self.bal.c[(self.part, "chpos", k, sel, p)]  # noqa: E731
        positions = sorted(range(k), key=lambda p: (cnt(p), rng.random()))
        perm = [None] * k            # perm[display position] = canonical option index
        place = {}
        for g in gpos:
            if g in place:
                continue
            p = next(x for x in positions if perm[x] is None)
            perm[p] = g
            place[g] = p
        rest = [i for i in range(k) if i not in place]
        rng.shuffle(rest)
        for p in range(k):
            if perm[p] is None:
                perm[p] = rest.pop()
        for g in gpos:
            self.bal.c[(self.part, "chpos", k, place[g])] += 1
            self.bal.c[(self.part, "chpos", k, sel, place[g])] += 1
        return perm

    def choice_design(self, options):
        """options: [(name, depth, select, n_option_cues, cells)]. Picks by the depth deficit, the even / odd and
        negated-selection balance of choice rows, the option-cue budget (choice options 5-10% of scoping cues) and
        the depth x choice-option x class cells still under 30 rows."""
        st, rng = self.st, self.rng
        n = max(1, st.rows)
        P = sum(st.pos.values()) + 1
        over = st.pos["choice_option"] / P - CHOICE_OPT_TARGET
        ch = max(1, st.choice)
        even_def = 0.5 - st.ch_even / ch
        src = getattr(self, "_cur_src", None)
        if src is not None and st.ch_src_n[src] >= 6:
            even_def = 0.5 * even_def + 0.5 * (0.5 - st.ch_src_even[src] / st.ch_src_n[src])
        neg_def = 0.5 - st.ch_neg / ch

        d0_full = st.depth[0] / n > self.depth_target[0] - 0.004
        # a source's choice rows stay near half even (its label definitions sit in the choice instruction)
        if src is not None and st.ch_src_n[src] >= 4:
            sh = st.ch_src_even[src] / st.ch_src_n[src]
            want = 0 if sh < 0.42 else (1 if sh > 0.58 else None)
            if want is not None and any(o[1] % 2 == want for o in options):
                options = [o for o in options if o[1] % 2 == want]

        def sc(o):
            name, d, sel, ncue, cells = o
            s = -(self.depth_target[d] - st.depth[d] / n) * 60
            s -= even_def * 150 * (1 if d % 2 == 0 else -1)
            s -= neg_def * 80 * (1 if sel == "false" else -1)
            # option-cue budget: choice-option cues 5-10% of scoping cue tokens (target 7%)
            s += (3000 if over > 0 else 600) * over * ncue / 3
            if d == 0 and d0_full:
                s += 20
            if ncue:
                co, ce = st.cx["ch_cue_odd"], st.cx["ch_cue_even"]
                s += 0.15 * (co - ce) * (1 if d % 2 else -1)
            if self.part == "train" and cells:
                fr = [max(0.0, self.cell_goal - st.cells[cell]) / self.cell_goal for cell in cells]
                s -= 40.0 * sum(fr) + 100.0 * max(fr)
            return s + rng.random() * 0.3
        return min(options, key=sc)

    def pick_stmt_lex(self, keys, nneg, k, depth):
        """k option lexeme tuples with nneg negations each, balancing lexeme parity and the class mix."""
        st, rng = self.st, self.rng
        pool = [x for x in keys if len(x) == nneg and all(self.lexeme_ok(y) for y in x)]
        if not pool:
            return None
        T = sum(st.cls.values()) + 1
        need = {c: CLASS_TARGET[c] - st.cls[c] / T for c in CLASS_TARGET}
        par = depth % 2
        out = []
        aff_used = set()
        for _ in range(k):
            def key(x):
                s = 0.0
                for y in x:
                    nn, o = st.lex_rows[y], st.lex_odd[y]
                    dev = (o + par + 0.5) / (nn + 1) - 0.5
                    s += 30 * dev * dev - 12 * need.get(cls5(lx.LEXICON[y]["cls"]), 0)
                    s += 0.3 * sum(1 for z in out if y in z)
                return s + rng.random() * 0.3
            # an affixal lexeme renders the same word in every option: at most one option per row carries it
            # (precheck X12 counts affixal cues per surface word over the whole row)
            ok = [x for x in pool if not any(lx.LEXICON[y]["cls"] == "affixal" and y in aff_used for y in x)]
            if not ok:
                return None
            x = min(ok, key=key)
            aff_used |= {y for y in x if lx.LEXICON[y]["cls"] == "affixal"}
            out.append(x)
        return out

    def neg_lex(self, n, label, parity, depth=None, aff_used=None):
        pool = NEG1 if n == 1 else NEG2
        pool = [x for x in pool if all(self.lexeme_ok(y) for y in x) and not ("non-" in x and " " in label)]
        if aff_used is not None:
            # 'in-' renders 'inapplicable' in every option; 'non-' renders 'non-<label>' (one word per label)
            pool = [x for x in pool if not any(y in aff_used for y in x if y != "non-")] or pool[:1]
        st = self.st
        tot = sum(st.lex_tok.values()) + 1
        T = sum(st.cls.values()) + 1
        cls_need = {k: CLASS_TARGET[k] - st.cls[k] / T for k in CLASS_TARGET}

        def key(x):
            s = 0.0
            for y in x:
                nn, o = st.lex_rows[y], st.lex_odd[y]
                dev = (o + parity + 0.5) / (nn + 1) - 0.5
                s += 30 * dev * dev - 15 * cls_need.get(cls5(lx.LEXICON[y]["cls"]), 0)
                if y in ("not", "n't") and (st.lex_tok["not"] + st.lex_tok["n't"]) / tot > NOT_NT_CAP:
                    s += 2
                s += 80 * max(0.0, st.lex_tok[y] / tot - 0.06)
                s += 45 * (1 if parity == 1 else -1) * ((o + 1) / (nn + 2) - 0.5)
            if depth in (1, 2, 3) and self.part == "train":
                for c in {cls5(lx.LEXICON[y]["cls"]) for y in x}:
                    if c in ("syntactic", "affixal", "lexical"):
                        s -= 8.0 * max(0.0, self.cell_goal - st.cells[(depth, "choice_option", c)]) / self.cell_goal
            return s + self.rng.random() * 0.2
        return min(pool, key=key)

    def card_choice(self, subj, taken=()):
        """A choice row over statements about the card's labels (twin golds gA != gB). Designs by depth:
           d0  select true, every option positive;            d1b select true, the two twin-gold options negated;
           d1a select false, the other options negated;        d2  select false, every option negated;
           d3  select false, the twin-gold options doubly negated and the other options negated;
           dar select false, every option the affirmative complement 'the label that fits it is <the other labels>'
               (a cue-less flip per option, so depth 2 with no option cue).
        Ordinal ladders also get item-37 decoy rows (antonym vs exact negation)."""
        rng = self.rng
        self._cur_src = subj.source
        gA, gB = subj.gA, subj.gB
        extra = [x for x in subj.labels if x not in (gA, gB)]
        rng.shuffle(extra)
        if subj.ptype == "ordinal" and "decoy" not in taken and subj.antonym not in (gA, gB) and \
                self.item_count(37) < self.item_goal(37):
            # options: the antonym of one twin's label (the decoy), and the exact negations of both twins' labels;
            # each twin's answer is the negation of the OTHER twin's label (the antonym is never true), so the
            # answer always carries a cue but so does one wrong option (no 'most cues' shortcut)
            aff_used = set()
            nA = self.neg_lex(1, gA, 1, None, aff_used)
            aff_used |= {y for y in nA if lx.LEXICON[y]["cls"] == "affixal"}
            nB = self.neg_lex(1, gB, 1, None, aff_used)
            opts = [(subj.antonym, ()), (gA, nA), (gB, nB)]
            golds = []
            for tw in ("A", "B"):
                g = subj.base[tw]["gold"]
                hits = [i for i, (lab, lex) in enumerate(opts) if (lab == g) ^ (len(lex) % 2 == 1)]
                golds.append(hits[0] if len(hits) == 1 else None)
            if None not in golds and len(set(golds)) == 2:
                perm = self.pick_perm(3, golds, "true")
                return {"frame": self.true_frame(1), "select": "true", "cue": None,
                        "mode": "decoy", "opts": opts, "perm": perm, "item37": True, "design": "decoy"}
        kmax = min(len(extra) + 2, 5)
        if kmax < 3:
            raise Reject("too few labels for a choice row")
        cells = lambda d: [(d, "choice_option", c) for c in ("syntactic", "affixal", "lexical")]  # noqa: E731
        designs = {"d0": (0, "true", 0, 0), "d1b": (1, "true", 1, 0), "d1a": (1, "false", 0, 1),
                   "d2": (2, "false", 1, 1), "d3": (3, "false", 2, 1)}
        opts = [(name, d, sel, 2 * ng + no, cells(d) if (ng or no) else [])
                for name, (d, sel, ng, no) in designs.items() if name not in taken]
        if len(subj.labels) <= 6 and sum(len(x) + 4 for x in subj.labels) + 28 <= 200:
            if "dar" not in taken:
                opts.append(("dar", 2, "false", 0, []))
            if "dart" not in taken:
                opts.append(("dart", 1, "true", 0, []))
        key = self.choice_design(opts)[0]
        ks = [x for x in (3, 4, 5) if x <= kmax]
        if key == "dar":
            k = self.bal.least((self.part, "ch_k_card"), ks)
            labs = [(x, True) for x in [gA, gB] + extra[:k - 2]]
            golds = [[x for x, _ in labs].index(subj.base[tw]["gold"]) for tw in ("A", "B")]
            if len(set(golds)) != 2:
                raise Reject("card choice not unique")
            perm = self.pick_perm(k, golds, "false")
            fr = self.false_frame(0)
            self.bal.c[(self.part, "chfalse", fr)] += 1
            return {"frame": fr, "select": "false", "mode": "card_ar", "opts": labs, "perm": perm, "design": key,
                    "cue": lx.FALSE_CHOICE_CUE[fr]}
        if key == "dart":
            # select true over the complements of both twins' labels plus plain other labels: each twin's answer is
            # the complement of the OTHER twin's label (depth 1, no option cue)
            k = self.bal.least((self.part, "ch_k_card"), ks)
            labs = [(gA, True), (gB, True)] + [(x, False) for x in extra[:k - 2]]
            golds = []
            for tw in ("A", "B"):
                g = subj.base[tw]["gold"]
                hits = [i for i, (x, ar) in enumerate(labs) if (x == g) != ar]
                golds.append(hits[0] if len(hits) == 1 else None)
            if None in golds or len(set(golds)) != 2:
                raise Reject("card choice not unique")
            perm = self.pick_perm(k, golds, "true")
            return {"frame": self.true_frame(1), "select": "true", "mode": "card_ar", "opts": labs, "perm": perm,
                    "design": key, "cue": None}
        d, sel, ng, no = designs[key]
        if no and rng.random() < 0.75:
            k = 3
            self.bal.c[((self.part, "ch_k_card"), 3)] += 1
        else:
            k = self.bal.least((self.part, "ch_k_card"), ks)
        others = extra[:k - 2]
        par = d % 2
        aff_used = set()
        opts = []
        for lab, nn_ in [(gA, ng), (gB, ng)] + [(lab, no) for lab in others]:
            lex = self.neg_lex(nn_, lab, par, d, aff_used) if nn_ else ()
            aff_used |= {y for y in lex if lx.LEXICON[y]["cls"] == "affixal"}
            opts.append((lab, lex))
        golds = []
        for tw in ("A", "B"):
            g = subj.base[tw]["gold"]
            hits = [i for i, (lab, lex) in enumerate(opts) if ((lab == g) ^ (len(lex) % 2 == 1)) == (sel == "true")]
            if len(hits) != 1:
                raise Reject("card choice not unique")
            golds.append(hits[0])
        perm = self.pick_perm(k, golds, sel)
        if sel == "true":
            fr, cue = self.true_frame(d % 2), None
        else:
            fr = self.false_frame(d % 2)
            cue = lx.FALSE_CHOICE_CUE[fr]
        return {"frame": fr, "select": sel, "cue": cue, "mode": "labels", "opts": opts, "perm": perm, "design": key}

    def word_tilt(self, text, parity):
        """How far the text's instruction words (>= 10 rows so far) already lean to this row's depth parity (SPEC 7.3
        cue-share rule: no word with an odd-row share above 60%)."""
        st = self.st
        sgn = 1 if parity else -1
        s = 0.0
        for w in set(WORD_RE.findall(text.lower())) - _stop():
            n = st.word_rows[w]
            if n >= 10:
                s += sgn * (st.word_odd[w] / n - 0.5)
        return s

    def true_frame(self, parity):
        rng = self.rng
        qs = {f["id"]: f["q"] for f in lx.CHOICE_FRAMES}
        fr = min(["chs1", "chs4", "chs6"], key=lambda f: (round(self.word_tilt(qs[f], parity), 2),
                                                          self.bal.c[(self.part, "chtrue", f)], rng.random()))
        self.bal.c[(self.part, "chtrue", fr)] += 1
        return fr

    def false_frame(self, parity):
        st, rng = self.st, self.rng
        lex = lx.FALSE_CHOICE_CUE
        qs = {f["id"]: f["q"] for f in lx.CHOICE_FRAMES}
        sgn = 1 if parity else -1
        return min(lex, key=lambda f: (round(sgn * ((st.lex_odd[lex[f]] + 1) / (st.lex_rows[lex[f]] + 2) - 0.5)
                                             + self.word_tilt(qs[f], parity), 2),
                                       self.bal.c[(self.part, "chfalse", f)], rng.random()))

    def other_choice(self, subj, ci=0):
        rng = self.rng
        if isinstance(subj, TriageSubject):
            golds = []
            for tw in ("A", "B"):
                f = subj.field[tw]
                golds.append(0 if f == "yes" else (1 if f == "no" else 2))
            perm = self.pick_perm(3, golds, "true")
            return {"frame": self.true_frame(0), "select": "true", "cue": None, "mode": "triage",
                    "perm": perm, "item35": True}
        plan = subj.choice_plans[ci]
        k = len(plan["idx"])
        golds = [choice_gold_of(plan, subj.x["A"]), choice_gold_of(plan, subj.x["B"])]
        perm = self.pick_perm(k, golds, plan["select"])
        cs = {"select": plan["select"], "mode": plan["mode"], "idx": plan["idx"], "perm": perm,
              "lex": plan.get("lex"), "design": plan.get("design")}
        if plan["mode"] == "names":
            if subj.kind == "multitext":
                sp = subj.sp
                if plan["select"] == "true":
                    q = f"Which {subj.item} {sp['sg']}?"
                    cs.update(frame="pack", q=q, fid="mt:true", cue=None)
                else:
                    q = f"Which {subj.item} is not {sp['adj']}?" if sp.get("adj") else \
                        f"Which {subj.item} does not {sp['base']}?"
                    cs.update(frame="pack", q=q, fid="mt:not", cue="not")
            else:
                cs.update(frame="pack", q=plan["q"], fid=f"pk:{subj.pkey}:{plan['cue'] or 'true'}", cue=plan["cue"])
        else:
            if plan["select"] == "true":
                dd = (1 if plan["mode"] == "ar" else 0) + (plan["nneg"][0] if plan["mode"] == "statements" else 0)
                cs.update(frame=self.true_frame(dd % 2), cue=None)
            else:
                dd = (1 if plan["mode"] == "ar" else 0) + (plan["nneg"][0] if plan["mode"] == "statements" else 0) + 1
                fr = self.false_frame(dd % 2)
                self.bal.c[(self.part, "chfalse", fr)] += 1
                cs.update(frame=fr, cue=lx.FALSE_CHOICE_CUE[fr])
        return cs

    # ------------------------------------------------------------------ one twin pair
    def spec_from(self, subj, cmb, rung):
        rng = self.rng
        spec = dict(cmb)
        spec["rung"] = rung
        fm = len(lx.TERM_FORMS.get(tuple(cmb["inner"]), [])) if cmb["ctype"] == "TERM" else 4
        spec["form_i"] = self.bal.least((self.part, "form", cmb["ctype"], tuple(cmb["inner"])), list(range(max(1, fm))))
        # the card term's name: the one whose words lean least to this row's parity (SPEC 7.3 cue-share rule)
        par = cmb["depth"] % 2
        spec["term_name"] = (lx.RESIDUAL_NAME if subj.kind == "card" and subj.ptype == "residual" and
                             cmb["ctype"] == "TERM" else
                             min(lx.TERM_NAMES, key=lambda t: (round(self.word_tilt(t, par), 2), rng.random())))
        if cmb.get("ynkey") == "pos":
            spec["ynkey"] = rng.choice([0, 1])
        elif cmb.get("ynkey") == "inv":
            st = self.st
            par = cmb["depth"] % 2
            kx = min(["fails to hold", "is false of"],
                     key=lambda x: (st.lex_rows[x] >= 48, (1 if par else -1) * ((st.lex_odd[x] + 1) / (st.lex_rows[x] + 2)
                                                                             - 0.5), rng.random()))
            spec["ynkey"] = 3 if kx == "is false of" else 2
        else:
            spec["ynkey"] = None
        return spec

    def make_pair(self, dev_kind):
        rng = self.rng
        for attempt in range(60):
            kind = self.choose_kind() if attempt < 15 else rng.choice(list(self.kind_share))
            try:
                subj = self.make_subject(kind)
                plan = self.rung_plan(subj)
                specs = []
                taken_d = Counter()
                used_cmb = set()        # one question per combo in a ladder: no row repeats another (A2)
                for p in plan:
                    r, d = p["rung"], p["depth"]
                    if r == "R0":
                        cmb = self.r0_spec(subj)
                        specs.append(self.spec_from(subj, cmb, "R0"))
                    elif r == "AR":
                        cmb = self.ar_spec(subj)
                        specs.append(self.spec_from(subj, cmb, "AR"))
                    elif r.startswith("N"):
                        forbid = ("ARC",) if rng.random() < 0.5 else ()
                        d, cmb = self.pick_yn_free(subj, p["free"], forbid, taken_d, p.get("req"), used_cmb)
                        taken_d[d] += 1
                        specs.append(self.spec_from(subj, cmb, f"N{d}"))
                    else:
                        continue
                    used_cmb.add(combo_key(cmb))
                # AR needs an odd-depth sibling of the same gold (a non-AR odd rung)
                if any(s["rung"] == "AR" for s in specs) and not any(s["depth"] % 2 == 1 and s["rung"] != "AR"
                                                                      for s in specs):
                    raise Reject("AR without an odd sibling")
                for s in specs:
                    s["dists"], s["look"], s["style"] = self.extras(subj, s, s["rung"], s["depth"])
                if any(p["rung"] == "D" for p in plan):
                    d0_full = self.st.depth[0] / max(1, self.st.rows) > self.depth_target[0] - 0.005
                    sibs = [s for s in specs if s["rung"] != "AR" and not (d0_full and s["rung"] == "R0")] or \
                        [s for s in specs if s["rung"] != "AR"]
                    sib = rng.choice(sibs)
                    ds = dict(sib)
                    ds["rung"] = "D"
                    F = lx.FRAMES[ds["frame"]]
                    n_outer = [c[2] if len(c) > 2 else F["pos"] for c in F["cues"]].count("outer_frame")
                    have = {k for k, _ in sib["dists"]}
                    kinds = (["side"] if n_outer < 2 and "side" not in have else []) + \
                        (["sep"] if "sep" not in have else [])
                    if kinds:
                        kd = rng.choice(kinds)
                        tbl = lx.DIST_SIDE if kd == "side" else lx.DIST_SEP
                        ok = [i for i in range(len(tbl)) if self.lexeme_ok(tbl[i][0]) and
                              dist_fits(subj, F, kd, tbl[i])]
                        i = min(ok, key=lambda i: (self.st.lex_dist[tbl[i][0]] / (self.st.lex_tok[tbl[i][0]] + 1),
                                                   rng.random()))
                        ds["dists"] = list(sib["dists"]) + [(kd, i)]
                        specs.append(ds)
                rds = []
                for s in specs:
                    rd = render_yn(subj, s)
                    rd.rung = s["rung"]
                    rds.append(rd)
                taken = []
                ci = 0
                for p in plan:
                    if p["rung"] != "CH":
                        continue
                    if subj.kind == "card":
                        cs = self.card_choice(subj, taken)
                    else:
                        cs = self.other_choice(subj, ci)
                        ci += 1
                    taken.append(cs.get("design"))
                    rd = render_choice(subj, cs)
                    rd.rung = "CH"
                    rds.append(rd)
                lad = self.finish(subj, rds, dev_kind)
                self.commit(lad, dev_kind)
                return lad
            except Reject as e:
                self.rejects[str(e)[:60]] += 1
            except (ValueError, KeyError) as e:
                self.rejects["err:" + type(e).__name__ + ":" + str(e)[:50]] += 1
        raise RuntimeError(f"cannot build a pair for {self.part}: {self.rejects.most_common(8)}")

    # ------------------------------------------------------------------ finish: twins, tags, checks, relations
    def finish(self, subj, rds, dev_kind):
        self.n_lad += 1
        lid_base = f"f7v2-{ {'train': 'tr', 'iid': 'ii', 'holdout': 'ho'}[self.part]}-{self.n_lad:05d}"
        states = dict(zip(("A", "B"), subj.states()))
        out = {}
        for tw in ("A", "B"):
            vals = subj.vals(tw)
            lid = f"{lid_base}{tw.lower()}"
            gid = f"g:f7nn2:{lid}"
            call = cid(gid)
            state = states[tw]
            state_neg = bool(STATE_NEG_RE.search(state))
            rows = []
            for k, rd in enumerate(rds):
                lf, gold, depth, truthP = instantiate(subj, rd, tw, vals)
                cues = rd.cues
                n_dist = sum(1 for c in cues if c["_dist"])
                has_yn = bool(rd.card) and bool(re.search(r"^- (yes|Yes): ", rd.card, re.M)) and \
                    bool(re.search(r"^- (no|No): ", rd.card, re.M))
                sel_false = rd.qtype == "choice" and rd.lf["select"] == "false"
                tags = item_tags_rule(depth, cues, n_dist, has_yn, state_neg, rd.qtype == "choice", sel_false, lf,
                                      "pin" if rd.pin else "")
                tags |= self.semantic_tags(subj, rd, depth, cues)
                m = {"id": f"r_f7nn2_{lid.replace('-', '_')}_{k}", "ladder_id": lid, "rung": rd.rung, "lf": lf,
                     "truth_P": bool(truthP), "depth": depth, "n_cues": len(cues), "n_distractor": n_dist,
                     "cues": [{x: c[x] for x in ("lexeme", "cls", "position", "scoping", "distance", "surface", "_dist")}
                              for c in cues],
                     "phen": sorted(tags), "frame_family": rd.family, "frame_id": rd.frame,
                     "ladder_kind": subj.kind, "source": subj.source, "dev_kind": dev_kind,
                     "card_style": rd.style, "gold": gold, "embed_depth": rd.embed, "qtype": rd.qtype,
                     "ptype": subj.ptype, "ctype": rd.ctype, "select_false": sel_false,
                     "template_id": f"{rd.frame}|{rd.ctype}|{'+'.join(rd.inner) or '-'}"}
                if 21 in tags:
                    m["antonym_gold"] = self.antonym_gold(subj, rd, vals)
                role = {"R0": "aff", "AR": "para", "D": "para", "CH": "choice"}.get(rd.rung) or \
                    ("neg" if depth % 2 else "dneg")
                row = {"id": m["id"], "group_id": gid, "call_id": call, "split": "train" if self.part == "train" else "dev",
                       "track": "GD", "source": SOURCE, "state": state, "qtype": rd.qtype, "instructions": rd.instr,
                       "options": rd.options, "gold": gold if rd.qtype == "noul" else rd.options[gold], "card": rd.card,
                       "role": role,
                       "meta": {"family": FAMILY, "family_name": "nested_negation", "generator": GENERATOR,
                                "version": VERSION, "rung": rd.rung, "kind": subj.kind, "ptype": subj.ptype,
                                "frame": rd.frame, "ctype": rd.ctype, "latent_id": lid, "part": self.part,
                                "dev_kind": dev_kind, "card_style": rd.style, **subj.meta(tw)}}
                rows.append((row, m, rd))
            out[tw] = rows
        self.check_ladder(subj, out)
        rels = {tw: self.relations(out[tw]) for tw in ("A", "B")}
        return {"subj": subj, "rows": out, "rels": rels, "dev_kind": dev_kind}

    def semantic_tags(self, subj, rd, depth, cues):
        t = set()
        # items named by a cue word (26, 33, 34) count the word only where it scopes: the same word as a distractor
        # (a side clause or a format line, A1) is not the phenomenon
        lexs = {c["lexeme"] for c in cues if c["scoping"]}
        noul = rd.qtype == "noul"
        if subj.kind == "card" and noul:
            if subj.ptype == "ordinal" and rd.ctype == "P" and rd.inner and rd.inner[-1] in ("not", "n't") and depth >= 1:
                t.add(21)
            if subj.ptype == "residual":
                t.add(22)
            if subj.ptype == "excl" and depth >= 1:
                t.add(23)
            if rd.ctype == "ONLY" and depth >= 1:
                t.add(24)
            if subj.ptype == "group" and depth >= 1:
                t.add(25)
        if subj.kind == "multitext" and noul:
            p = subj.ptype
            if p in ("SOME", "ALL", "EXCEPT") and lexs & {"none", "no", "not a single", "not all", "not every", "not one"}:
                t.add(26)
            if p == "SOME" and ({"non-", "-free", "un-"} & set(rd.inner)) and \
                    any(c["scoping"] and c["position"] == "outer_frame" for c in cues):
                t.add(27)
            if p == "COUNT":
                t.add(28)
            if p == "FEW":
                t.add(29)
            if p in ("BOTH", "EITHER"):
                t.add(30)
            if p == "EXCEPT":
                t.add(31)
        if rd.ctype == "CONTRAST":
            t.add(32)
        if getattr(subj, "pkey", None) in ("deontic", "deontic_h") and lexs & {"need not", "must not", "cannot", "forbid", "at no point"}:
            t.add(33)
        if "unless" in lexs:
            t.add(34)
        if isinstance(subj, TriageSubject) and (depth >= 1 or not noul):
            t.add(35)
        if not noul and rd.spec.get("item37"):
            t.add(37)
        return t

    def antonym_gold(self, subj, rd, vals):
        """Gold under the antonym reading of item 21: the innermost 'not L' read as the opposite pole label."""
        inner_cue = [i for i, c in enumerate(rd.cues) if c["position"] == "inner_claim" and c["scoping"]][-1]

        def rec(n):
            n = dict(n)
            if n["op"] == "NOT" and n.get("cue") == inner_cue:
                core = n["child"]
                return CORE(ATOM("fit:" + subj.antonym, True))
            if "child" in n:
                n["child"] = rec(n["child"])
            if "children" in n:
                n["children"] = [rec(c) for c in n["children"]]
            return n
        lf2 = rec(rd.lf)
        v = dict(vals)
        return int(lf_eval(set_atoms(lf2, v)))

    def check_ladder(self, subj, out):
        import f7_precheck as fp
        A, B = out["A"], out["B"]
        ambiguity_invariants(subj, out)
        for tw in ("A", "B"):
            golds = {r["gold"] for r, m, rd in out[tw] if rd.qtype == "noul"}
            if golds != {0, 1}:
                raise Reject("ladder lacks a yes or a no row")
        for tw in ("A", "B"):
            surf = [(r["instructions"], r["card"], json.dumps(r["options"])) for r, m, rd in out[tw]]
            if len(set(surf)) != len(surf):
                raise Reject("repeated row inside a ladder")       # A2 / precheck 8.11
        for (ra, ma, rd), (rb, mb, _) in zip(A, B):
            if ra["instructions"] != rb["instructions"] or ra["card"] != rb["card"] or ra["options"] != rb["options"]:
                raise Reject("twin surface differs")
            if rd.qtype == "noul" and ra["gold"] == rb["gold"]:
                raise Reject(f"twin golds equal ({rd.rung} {rd.ctype})")
            if rd.qtype == "choice" and ma["gold"] == mb["gold"]:
                raise Reject("twin choice golds equal")
        D = self.decon
        for tw in ("A", "B"):
            for row, m, rd in out[tw]:
                R = {"row": row, "m": m, "an": {"has_yn": bool(row["card"]) and "- yes:" in (row["card"] or "").lower()}}
                h = fp.exclude_hits(None, R)
                if h:
                    raise Reject("X:" + ",".join(sorted(h)) + ":" + str(list(h.values())[0][0])[:40])
                miss = restate_miss(row, m)
                if miss:
                    raise Reject(f"restate:{miss[:2]}")
                if tw == "A":
                    texts = [row["instructions"]] + list(row["options"] or []) + \
                        [ln[2:].split(": ", 1)[1] for ln in (row["card"] or "").split("\n") if ": " in ln]
                    why = D.authored_hits(texts)
                    if why:
                        raise Reject("decon:" + ",".join(sorted(set(why))))
                    if lx.banned_hits(row["instructions"], *(row["options"] or [])):
                        raise Reject("ban")
                    if len(row["instructions"]) > 2400:
                        raise Reject("instruction too long")
                    mv.check_text(row["instructions"], "instruction")
                    if row["card"]:
                        mv.check_text(row["card"], "card")

    def relations(self, rows):
        """dev: equiv for the same gold, complement for the opposite; train: R0 -> same-gold rows 'inv' (a = R0),
        R0 <-> one opposite-gold row 'complement'; <= 1 complement per row; chain rows of one core claim only."""
        def chain(lf):
            n = lf
            while n["op"] in ("NOT", "DIST"):
                n = n["child"]
            return n["op"] == "CORE"
        yn = [(r, m) for r, m, rd in rows if rd.qtype == "noul" and chain(m["lf"])]
        if len(yn) < 2:
            return []
        anchor = next(((r, m) for r, m in yn if m["rung"] == "R0"), None) or \
            next(((r, m) for r, m in yn if m["depth"] % 2 == 0), yn[0])
        a, am = anchor
        rels, comp = [], set()
        train = self.part == "train"
        same = [(r, m) for r, m in yn if r is not a and r["gold"] == a["gold"]]
        opp = [(r, m) for r, m in yn if r["gold"] != a["gold"]]
        # 'inv' (one-way, a = the stop-gradient anchor) only when the anchor is the cue-less R0; a ladder without R0
        # links its same-gold rows symmetrically ('equiv'), so no negated row is ever the teacher (r6)
        one_way = train and am["rung"] == "R0"
        for r, m in same:
            rels.append({"type": "inv" if one_way else "equiv", "a": a["id"], "b": r["id"], "track": "f7v2"})
        if opp:
            r, m = opp[0]
            rels.append({"type": "complement", "a": a["id"], "b": r["id"], "track": "f7v2"})
            comp |= {a["id"], r["id"]}
        free_same = [r for r, m in same if r["id"] not in comp]
        for r, m in opp[1:]:
            if free_same:
                s = free_same.pop(0)
                rels.append({"type": "complement", "a": s["id"], "b": r["id"], "track": "f7v2"})
                comp |= {s["id"], r["id"]}
            elif not train:
                rels.append({"type": "equiv", "a": opp[0][0]["id"], "b": r["id"], "track": "f7v2"})
        return rels

    def commit(self, lad, dev_kind):
        subj = lad["subj"]
        self.used_ids |= subj.used_ids()
        if subj.kind == "record":
            self.names_used |= set(subj.names)
        self.st.kinds[subj.kind] += 1
        self.st.ptypes[(subj.kind, subj.ptype)] += 1
        self.st.sources[subj.source] += 1
        for tw in ("A", "B"):
            for row, m, rd in lad["rows"][tw]:
                self.st.add_row(m, row["instructions"], rd.frame, dev_kind)
                if rd.qtype == "noul":
                    for kd in rd.spec.get("dists") or []:
                        self.st.tmpl_rows[tuple(kd)] += 1
                        self.st.tmpl_odd[tuple(kd)] += m["depth"] % 2
        self.ladders.append(lad)


def restate_miss(row, m):
    """Rule 2.4 / precheck 5.l: the yes line repeats every question-position cue word (look-alikes and option cues
    excepted)."""
    import f7_precheck as fp
    if row["qtype"] != "noul" or not row["card"]:
        return []
    yl = [ln for ln in row["card"].split("\n") if re.match(r"^\s*-\s*yes\s*:", ln, re.I)]
    if not yl or not re.search(r"^- (no|No): ", row["card"], re.M):
        return []
    y = re.sub(r"^\s*-\s*yes\s*:", "", yl[0], flags=re.I).lower()
    miss = []
    for c in m["cues"]:
        if c["cls"] == "lookalike" or c["position"] not in QUESTION_POSITIONS or c["position"] == "choice_option":
            continue
        surf = (c.get("surface") or c["lexeme"]).lower().strip()
        if surf.startswith("-") or surf.endswith("-"):
            if surf.strip("-") not in y:
                miss.append(surf)
            continue
        forms = fp.inflections(surf) or [surf]
        if not any(re.search(r"(?<![\w-])" + re.escape(f).replace(r"\ ", r"\s+") + r"(?![\w-])", y) for f in forms):
            if surf in ("n't", "nt") and re.search(r"n't\b|\bnot\b", y):
                continue
            miss.append(surf)
    return miss


# ============================================================================================ build + write
def static_checks(dev_labels, dev_names, log=print):
    """Bans and decontamination of the lexicon itself (before any row is built)."""
    problems = []
    for k, s in list(lx.CARD_SOURCES.items()) + list(lx.PROP_SOURCES.items()):
        names = list(s.get("labels") or {}) + ([s["pos"][0], s["neg"][0]] if "pos" in s else [])
        for x in names:
            if x.lower() in dev_labels:
                problems.append(f"label {x!r} of {k} is a dev label name")
        src = s.get("golden")
        if src and source_is_dev(src, dev_names):
            problems.append(f"source {src} matches dev sources {source_is_dev(src, dev_names)}")
    for src in ("civil_comments", "toxic_conv", SOURCE):
        if source_is_dev(src, dev_names):
            problems.append(f"source {src} is a dev source")
    for f in lx.FRAMES_LIST:
        for k in ("q", "y", "n"):
            if lx.banned_hits(f[k].replace("{", "").replace("}", "")):
                problems.append(f"frame {f['id']} {k} banned: {lx.banned_hits(f[k])}")
    # held-out lexemes never appear in a train template
    hold = [x for x, v in lx.LEXICON.items() if v["split"] == "holdout"]
    train_txt = " ".join(f[k] for f in lx.FRAMES_LIST if f["split"] == "train" for k in ("q", "y", "n"))
    for x in hold:
        for form in lx.LEXICON[x]["forms"]:
            if not form.startswith("-") and not form.endswith("-") and \
                    re.search(r"(?<![\w-])" + re.escape(form) + r"(?![\w-])", train_txt, re.I):
                problems.append(f"held-out lexeme {x!r} in a train frame")
    if problems:
        raise SystemExit("static checks failed:\n  " + "\n  ".join(problems))
    log(f"static checks: {len(lx.FRAMES_LIST)} frames, {len(lx.lexemes('train'))} train + "
        f"{len(lx.lexemes('holdout'))} held-out lexemes; no dev label, dev source or ban")


def build(n_pairs=None, seed=SEED, log=print, decon=None, pools=None, audit=True, audit_rounds=None):
    n_pairs = n_pairs or N_PAIRS
    dev_labels = dev_label_names()
    dev_names = dev_source_names()
    static_checks(dev_labels, dev_names, log)
    D = decon or Decon(log)
    pools = pools if pools is not None else load_pools(D, log)
    used = set()
    parts = {}
    for part, s in (("train", 0), ("iid", 10 ** 9), ("holdout", 2 * 10 ** 9)):
        pl = Planner(part, pools, dev_labels, seed + s, used, log)
        pl.decon = D
        t0 = time.time()
        n_pool = int(round(n_pairs[part] * POOL_FACTOR[part]))
        for i in range(n_pool):
            pl.make_pair("train" if part == "train" else part)
            if (i + 1) % 400 == 0:
                log(f"  {part}: {i + 1} pairs ({time.time() - t0:.0f} s); rejects {sum(pl.rejects.values())}")
        log(f"{part}: pool {len(pl.ladders)} pairs, {pl.st.rows} rows, choice share "
            f"{pl.st.choice / max(1, pl.st.rows):.3f}, choice-option cue share "
            f"{pl.st.pos['choice_option'] / max(1, sum(pl.st.pos.values())):.3f}, depth "
            f"{ {d: round(pl.st.depth[d] / max(1, pl.st.rows), 3) for d in range(5)} }; top rejects {pl.rejects.most_common(4)}")
        wc = Counter()
        for lad in pl.ladders:
            for tw in ("A", "B"):
                for row, m, rd in lad["rows"][tw]:
                    for w in set(WORD_RE.findall(row["instructions"].lower())) - _stop():
                        wc[w] += 1
        parts[part] = {"pl": pl, "cands": list(pl.ladders), "s": s, "wc": wc}
    sel = select_all(parts, n_pairs, seed, log)
    rounds = 0
    max_rounds = AUDIT_ROUNDS if audit_rounds is None else audit_rounds
    while audit:
        if rounds >= max_rounds:
            fails = audit_selection(parts, sel, log)
            log(f"audit after {rounds} refinement rounds: failing checks {fails}")
            break
        fails = audit_selection(parts, sel, log)
        if not fails:
            break
        rounds += 1
        log(f"audit round {rounds}: {len(fails)} failing checks {fails}; refining the selection")
        sel = select_all(parts, n_pairs, seed, log, prev=sel, round_=rounds)
    for part, P in parts.items():
        pl = P["pl"]
        pl.ladders = [P["cands"][i] for i in sel[part]["idx"]]
        pl.selection = {"pool_pairs": len(P["cands"]), "kept_pairs": len(pl.ladders), "audit_rounds": rounds,
                        "local_search_penalty": sel[part]["pen"], "hard": sel[part]["hard"]}
    return {k: v["pl"] for k, v in parts.items()}, D


AUDIT_ROUNDS = 8
AUDIT_EXPECTED = {"3.9"}    # 3.9 counts devx rows: expected to fail only when no devx file exists (4.3: precheck O1)
REFINE_ITERS = {"train": 60000, "iid": 30000, "holdout": 30000}
REFINE_T0 = 2.0


DEVX_ROWS = DATA / "v14_parts" / "f7_devx.jsonl"
DEVX_META = DATA / "v14_parts" / "f7_devx_meta.jsonl"
DEVX_REL = DATA / "v14_parts" / "f7_devx_relations.jsonl"


def _jsonl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()] if p.exists() else []


def devx_word_base():
    """Round 3: precheck 8.9 (SPEC 7.3 cue-share rule) reads the instruction words of train + probe + devx rows
    together, and devx is a fixed file written blind by another agent. Its per-word row counts and odd-depth counts
    are the starting base of the word rule in every part, so the selection keeps the UNION under the limit (after
    the round-3 rebuild the word 'without' was 24 / 38 = 63% odd: F7 20 / 34 plus devx 4 / 4). Only these counts are
    read (instruction words and the parity of the sidecar depth); no devx text, gold or label enters a row."""
    rows, metas = _jsonl(DEVX_ROWS), {m["id"]: m for m in _jsonl(DEVX_META)}
    base = Counter()
    for r in rows:
        odd = int(metas[r["id"]]["depth"] % 2) if r["id"] in metas else 0
        for w in set(WORD_RE.findall((r.get("instructions") or "").lower())) - _stop():
            base[("w_r", w)] += 1
            base[("w_o", w)] += odd
    return base


def select_all(parts, n_pairs, seed, log, prev=None, round_=0):
    """Select every part (train first: its instruction words are the base of the dev parts' word rule; iid
    before holdout: the dev cue-share rule reads iid + holdout). The word rule of every part starts from the devx
    rows' counts (devx_word_base). prev: refine from the previous selection."""
    base, lbase, out = devx_word_base(), Counter(), {}
    for part in ("train", "iid", "holdout"):
        P = parts[part]
        s = P["s"]
        words = {w for w, c in P["wc"].items() if c >= 20}
        if part != "train":
            words |= {k[1] for k, v in base.items() if k[0] == "w_r" and v >= 8}
        cands = P["cands"]
        feats = [pair_features(c, words) for c in cands]
        frames = sorted({m["frame_id"] for lad in cands for tw in ("A", "B") for _, m, _ in lad["rows"][tw]})
        obj = Objective(part, sorted(lx.LEXICON), words, frames, base=Counter(base),
                        lbase=lbase if part == "holdout" else None)
        must = holdout_has_element if part == "holdout" else None
        rng = random.Random(seed + 7 + s + 1000 * round_)
        if prev is None:
            _, T, pen, idx = select_pairs(cands, n_pairs[part], obj, rng, log, iters=SELECT_ITERS[part], must=must,
                                          feats=feats)
        else:
            # a refinement round walks away from the previous selection (no restart to it) at a temperature, then
            # anneals: the audit checks that the objective does not model (the cross-validated surface probes) see a
            # different selection, and every hard limit still holds (the walk never raises the hard penalty)
            _, T, pen, idx = select_pairs(cands, n_pairs[part], obj, rng, log, iters=REFINE_ITERS[part], must=must,
                                          feats=feats, init=prev[part]["idx"], t0_temp=REFINE_T0, restart=False)
        out[part] = {"idx": idx, "pen": round(pen, 4), "hard": round(obj.hard(T), 4)}
        for i in idx:
            f = feats[i]
            base.update({k: v for k, v in f.items() if isinstance(k, tuple) and k[0] in ("w_r", "w_o")})
            if part == "iid":
                lbase.update({k: v for k, v in f.items() if isinstance(k, tuple) and
                              k[0] in ("lexr", "lexo", "lexr_yn", "lexo_yn")})
    return out


def audit_selection(parts, sel, log):
    """The audit (yn2b/f7_precheck.py, run as a library on the in-memory rows, fast mode plus the full surface probes
    of check 5, with the devx rows as in the ship run): the ids of the failing checks other than the expected ones. The tool reads no
    decontam-only file in this mode."""
    import f7_precheck as fp
    rows, metas, rels = {}, [], {}
    for part in ("train", "iid", "holdout"):
        P = parts[part]
        pl = P["pl"]
        keep = pl.ladders
        pl.ladders = [P["cands"][i] for i in sel[part]["idx"]]
        r, m, rl = rows_of(pl)
        pl.ladders = keep
        key = "train" if part == "train" else "probe"
        rows.setdefault(key, []).extend(r)
        rels.setdefault(key, []).extend(rl)
        metas.extend(strip_private(m))
        if part == "holdout":
            hold_m = strip_private(m)
    # round 3: the devx rows are part of the audit, as in the ship precheck, so every check that reads the union of
    # train, probe and devx (8.9 instruction-word parity, 8.11 dedupe, 10.6 / 10.7 disjointness, ...) is met here
    rows["devx"], rels["devx"] = _jsonl(DEVX_ROWS), _jsonl(DEVX_REL)
    metas.extend(_jsonl(DEVX_META))
    opts = fp.Opts(fast=True, lexicon=lexicon_json(), holdout_spec=holdout_spec_json(hold_m), unseen=False,
                   neg_manifest="(not read by the generator)", generator_code=[], decide2_code=[])
    ctx = fp.Ctx(rows, metas, rels, opts, log=lambda s_: None)
    res = fp.run_checks(ctx)
    # the surface probes in full (fast mode skips the bag-of-words and length LR probes, 5.h / 5.i, and the TF-IDF
    # probe 5.m): cross-validated probes are not modelled by the selection objective, so the audit loop is what keeps
    # them under their limits
    ctx.opts.fast = False
    res.update(fp.run_checks(ctx, only={"5"}))
    expected = AUDIT_EXPECTED if not rows["devx"] else set()
    fails = sorted({sb.id for r in res.values() for sb in r["subs"] if sb.status == "FAIL"} - expected)
    for r in res.values():
        for sb in r["subs"]:
            if sb.id in fails:
                log(f"    audit {sb.id} FAIL: {json.dumps(sb.value, default=str)[:400]}")
    return fails


def holdout_has_element(lad):
    """Checklist rule 2.10 / precheck 10.9: a holdout ladder carries a held-out source, frame family or lexeme."""
    subj = lad["subj"]
    if subj.kind in ("card", "multitext") and subj.holdout:
        return True
    for tw in ("A", "B"):
        for _, m, _ in lad["rows"][tw]:
            if lx.FRAMES.get(m["frame_id"], {}).get("split") == "holdout":
                return True
            if any(lx.LEXICON.get(c["lexeme"], {}).get("split") == "holdout" for c in m["cues"]):
                return True
    return False


def rows_of(pl):
    rows, metas, rels = [], [], []
    for lad in pl.ladders:
        for tw in ("A", "B"):
            for row, m, rd in lad["rows"][tw]:
                rows.append(row)
                metas.append(m)
            rels += lad["rels"][tw]
    return rows, metas, rels


def lexicon_json():
    return {"about": "F7 v2 curated cue lexicon (golden_src/gen3/nn_lexicon.py LEXICON); the builder draws every cue from "
                     "it", "lexemes": {k: {"cls": v["cls"], "split": v["split"], "can_distract": v["can_distract"],
                                         "forms": v["forms"]} for k, v in lx.LEXICON.items()}}


def holdout_spec_json(hold_rows_meta):
    lex = sorted({c["lexeme"] for m in hold_rows_meta for c in m["cues"]
                  if lx.LEXICON.get(c["lexeme"], {}).get("split") == "holdout"})
    fams = sorted({f["family"] for f in lx.FRAMES_LIST if f["split"] == "holdout"})
    fids = sorted({f["id"] for f in lx.FRAMES_LIST if f["split"] == "holdout"})
    srcs = sorted({m["source"] for m in hold_rows_meta if m["ladder_kind"] in ("card", "multitext")})
    return {"lexemes": lex, "frame_families": fams, "frame_ids": fids, "cue_combos": [list(c) for c in HOLD_COMBOS],
            "sources": srcs}


def strip_private(metas):
    out = []
    for m in metas:
        m = dict(m)
        m["cues"] = [{k: v for k, v in c.items() if not k.startswith("_")} for c in m["cues"]]
        out.append(m)
    return out


def write_all(parts, counts, overwrite=False, log=print):
    import yn2b_common as yc
    outs = {k: yc.guard_out(DATA / p, inputs=[DATA / GOLD_TRAIN], overwrite=overwrite) for k, p in OUT.items()}
    tr, trm, trr = rows_of(parts["train"])
    ii, iim, iir = rows_of(parts["iid"])
    ho, hom, hor = rows_of(parts["holdout"])
    dump = lambda xs: [json.dumps(x, ensure_ascii=False) for x in xs]  # noqa: E731
    yc.write_lines_atomic(outs["train"], dump(tr))
    yc.write_lines_atomic(outs["train_rel"], dump(trr))
    yc.write_lines_atomic(outs["train_meta"], dump(strip_private(trm)))
    yc.write_lines_atomic(outs["probe"], dump(ii + ho))
    yc.write_lines_atomic(outs["probe_rel"], dump(iir + hor))
    yc.write_lines_atomic(outs["probe_meta"], dump(strip_private(iim + hom)))
    yc.write_json(outs["lexicon"], lexicon_json())
    yc.write_json(outs["holdout_spec"], holdout_spec_json(hom))
    defs = {"frames": lx.FRAMES_LIST, "choice_frames": lx.CHOICE_FRAMES, "keys": lx.KEYS,
            "card_sources": lx.CARD_SOURCES, "prop_sources": lx.PROP_SOURCES, "multi_sources": lx.MULTI_SOURCES,
            "packs": {k: {kk: (list(map(list, vv.items())) if kk == "forms" else vv) for kk, vv in v.items()}
                      for k, v in lx.PACKS.items()},
            "label_forms": {"|".join(k): v for k, v in lx.LABEL_FORMS.items()},
            "term_defs": lx.TERM_DEFS, "dist_side": lx.DIST_SIDE, "dist_sep": lx.DIST_SEP, "dist_card": lx.DIST_CARD,
            "lookalikes": lx.LOOKALIKES, "banned_patterns": [p.pattern for p in lx.BANNED_PATTERNS]}
    def jsonable(x):
        if isinstance(x, dict):
            return {("|".join(k) if isinstance(k, tuple) else str(k)): jsonable(v) for k, v in x.items()}
        if isinstance(x, (list, tuple)):
            return [jsonable(v) for v in x]
        return x
    yc.write_json(outs["defs"], jsonable(defs))
    counts["files"] = {OUT[k]: yc.sha256_file(outs[k]) for k in OUT if k != "counts"}
    yc.write_json(outs["counts"], counts)
    log(f"wrote {', '.join(OUT.values())}")
    return outs


def summarize(pl):
    T = Counter()
    for lad in pl.ladders:
        T.update(pair_features(lad))
    kinds, ptypes, sources = Counter(), Counter(), Counter()
    for lad in pl.ladders:
        s = lad["subj"]
        kinds[s.kind] += 1
        ptypes[f"{s.kind}:{s.ptype}"] += 1
        sources[s.source] += 1
    n = max(1, T["rows"])
    return {"pairs": len(pl.ladders), "ladders": 2 * len(pl.ladders), "rows": T["rows"],
            "selection": getattr(pl, "selection", None),
            "depth": {d: [T[("depth", d)], round(T[("depth", d)] / n, 4)] for d in range(5)},
            "kinds_pairs": dict(kinds), "ptypes_pairs": dict(sorted(ptypes.items())),
            "sources_pairs": dict(sources.most_common()),
            "items": {i: T[("item", i)] for i in range(1, 39)},
            "class_tokens": {c: T[("cls", c)] for c in CLASS_TARGET},
            "position_tokens": {p: T[("pos", p)] for p in POS_TARGET},
            "choice_rows": T["ch"], "choice_negsel": T["ch_neg"], "choice_even_depth": T["ch_even"],
            "lexeme_rows": {x: T[("lexr", x)] for x in sorted(lx.LEXICON) if T[("lexr", x)]},
            "rejects": dict(pl.rejects.most_common(30))}


def main(argv=None):
    # reproducible builds: set / dict iteration over strings follows the hash seed, so the CLI pins it (the planner
    # draws from sets of lexemes and words)
    import os
    if os.environ.get("PYTHONHASHSEED") != "0" and argv is None:
        os.environ["PYTHONHASHSEED"] = "0"
        os.execv(sys.executable, [sys.executable] + sys.argv)
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--scale", type=float, default=1.0, help="fraction of the pair counts (dry runs)")
    ap.add_argument("--audit-rounds", type=int, default=None, help=f"selection refinement rounds (default {AUDIT_ROUNDS})")
    a = ap.parse_args(argv)
    t0 = time.time()
    log = lambda s: print(f"[{time.time() - t0:6.0f}s] {s}", flush=True)  # noqa: E731
    import yn2b_common as yc
    got = yc.sha256_file(DATA / GOLD_TRAIN)
    if got != GOLD_TRAIN_SHA:
        raise SystemExit(f"golden_train sha256 {got[:12]} is not the main run's {GOLD_TRAIN_SHA[:12]}")
    n_pairs = {k: max(4, int(round(v * a.scale))) for k, v in N_PAIRS.items()}
    parts, D = build(n_pairs, log=log, audit_rounds=a.audit_rounds)
    import train_decoder as td
    for k, pl in parts.items():
        rows, metas, rels = rows_of(pl)
        td.check_rows(rows, 0.5)
    allids = [r["id"] for pl in parts.values() for r in rows_of(pl)[0]]
    if len(allids) != len(set(allids)):
        raise SystemExit("duplicate row ids")
    counts = {"generator": GENERATOR, "version": VERSION, "revision": REVISION, "seed": SEED,
              "golden_train_sha256": GOLD_TRAIN_SHA,
              "parts": {k: summarize(pl) for k, pl in parts.items()}}
    if a.write:
        write_all(parts, counts, overwrite=a.overwrite, log=log)
    for k, v in counts["parts"].items():
        log(f"{k}: pairs {v['pairs']} rows {v['rows']} depth {v['depth']} choice {v['choice_rows']} kinds {v['kinds_pairs']} sel {v['selection']}")
    return parts, counts



# ============================================================================================ pair selection
# The planner steers every choice toward the section-3 targets, but its decisions are made one row at a time. The
# selection stage builds a larger pool of twin pairs and then picks the final set by local search on the aggregate
# criteria the audit reads (depth mix, cue class / position mix, per-lexeme parity and counts, cells, item floors,
# choice share and gold positions, distractor and parity-mismatch shares, the composition probes, instruction-word
# parity, frame / carrier caps, style per depth, R0 and kind shares). Labels never change: whole pairs are kept or
# dropped. Objective.hard holds the audit's own thresholds (with a small margin): once it reaches 0 no swap may raise
# it again, and the soft penalty then pulls every count toward the middle of its band. build() finally runs the
# audit (yn2b/f7_precheck.py as a library, fast mode, no devx) on the in-memory rows and refines the selection while a
# check other than the objected 4.3 (yn2b/F7_OBJECTIONS.md) and the devx-count 3.9 fails.
WORD_RE = re.compile(r"[a-z0-9]+")
SELECT_T0 = 0.0           # start temperature of the selection's simulated annealing
WORD_ODD_MAX = 0.57       # SPEC 7.3 cue-share rule is <= 60% odd at >= 30 rows; 3 points of margin for devx rows
STOPW = None


def _stop():
    global STOPW
    if STOPW is None:
        import build_v11_fixes as b
        STOPW = set(b.STOP)
    return STOPW


def pair_features(lad, words_ok=None):
    """Additive counts of one twin pair (both twins)."""
    f = Counter()
    for tw in ("A", "B"):
        for row, m, rd in lad["rows"][tw]:
            d = m["depth"]
            odd = d % 2
            yn = rd.qtype == "noul"
            cues = m["cues"]
            ncl = [c for c in cues if c["cls"] != "lookalike"]
            sc = [c for c in cues if c["scoping"]]
            f["rows"] += 1
            f[("depth", d)] += 1
            f[("n_d", d)] += 1
            if m["n_distractor"]:
                f[("dist_d", d)] += 1
            if len(cues) % 2 != odd:
                f[("mis_d", d)] += 1
            for c in ncl:
                f[("cls", cls5(c["cls"]))] += 1
                f[("lextok", c["lexeme"])] += 1
                if c.get("_dist"):
                    f[("lexdist", c["lexeme"])] += 1
            for c in sc:
                f[("pos", posg(c["position"]))] += 1
            for key in {(d, c["position"], c["cls"]) for c in sc}:
                f[("cell",) + key] += 1
            for x in {c["lexeme"] for c in cues}:
                f[("lexr", x)] += 1
                f[("lexo", x)] += odd
                if yn:
                    f[("lexr_yn", x)] += 1
                    f[("lexo_yn", x)] += odd
            for it in set(m["phen"]):
                if it in DEPTH1_ITEMS and d < 1:   # an unnegated anchor does not count toward items 28 / 30 (r6)
                    continue
                f[("item", it)] += 1
            for dd in {c["distance"] for c in sc}:
                f[("dbin", dd)] += 1
            f[("embed", min(3, m.get("embed_depth", 0)))] += 1
            f[("frame", m["frame_id"])] += 1
            f[("family", m["frame_family"])] += 1
            if odd:
                f["odd_rows"] += 1
                if m["rung"] == "AR" or (sc and all(c["cls"] == "lexical" for c in sc)):
                    f["arlex"] += 1
            words = set(WORD_RE.findall(row["instructions"].lower())) - _stop()
            for w in words:
                if words_ok is None or w in words_ok:
                    f[("w_r", w)] += 1
                    f[("w_o", w)] += odd
            if yn:
                f["yn"] += 1
                f[("ynd", d)] += 1
                f[("style", d, m["card_style"])] += 1
                tp = 1 if m["truth_P"] else 0
                g = row["gold"]
                allc = len(cues)
                syn = sum(1 for c in cues if c["cls"] == "syntactic")
                outer = any(c["position"] == "outer_frame" and c["cls"] != "lookalike" for c in cues)
                inner = any(c["position"] == "inner_claim" and c["cls"] != "lookalike" for c in cues)
                f["c1"] += int(g == tp)
                f[("c2", d)] += int(g == tp ^ (allc % 2))
                f["c3"] += int(g == tp ^ (syn % 2))
                f["c4"] += int(g == tp ^ int(outer))
                f["c5"] += int(g == tp ^ int(inner))
                for nm, mem in (("aff", ("affixal",)), ("lex", ("lexical",)), ("cross", ("cross_sentence", "answer_mapping"))):
                    k = sum(1 for c in cues if c["cls"] not in mem)
                    f[("c6", nm)] += int(g == tp ^ (k % 2))
            else:
                f["ch"] += 1
                sel_false = m["select_false"]
                f["ch_neg"] += int(sel_false)
                f["ch_even"] += int(odd == 0)
                k = len(row["options"])
                pos = m["gold"]
                f[("chpos", k, pos)] += 1
                f[("chk", k)] += 1
                sl = "f" if sel_false else "t"
                f[("chpos_sel", k, sl, pos)] += 1
                f[("chk_sel", k, sl)] += 1
                f[("chpos_par", k, odd, pos)] += 1
                f[("chk_par", k, odd)] += 1
                gp = pos / max(1, k - 1)
                for nm, x in (("neg", int(sel_false)), ("cue", m["n_cues"]), ("k", k), ("d", d)):
                    f[("corr", nm, "x")] += x
                    f[("corr", nm, "xx")] += x * x
                    f[("corr", nm, "xy")] += x * gp
                f[("corr", "y")] += gp
                f[("corr", "yy")] += gp * gp
    subj = lad["subj"]
    f["ladders"] = 2
    f[("kind", subj.kind)] += 2
    f["r0"] += sum(1 for tw in ("A", "B") if any(m["rung"] == "R0" for _, m, _ in lad["rows"][tw]))
    return f


def _band(share, lo, hi, w):
    if share < lo:
        return w * (lo - share) ** 2 * 1e4
    if share > hi:
        return w * (share - hi) ** 2 * 1e4
    return 0.0


def _corr(T, nm):
    n = T["ch"]
    if n < 3:
        return 0.0
    sx, sxx, sxy = T[("corr", nm, "x")], T[("corr", nm, "xx")], T[("corr", nm, "xy")]
    sy, syy = T[("corr", "y")], T[("corr", "yy")]
    vx = sxx - sx * sx / n
    vy = syy - sy * sy / n
    if vx <= 1e-9 or vy <= 1e-9:
        return 0.0
    return (sxy - sx * sy / n) / math.sqrt(vx * vy)


class Objective:
    """The aggregate penalty of a selection (0 when every modelled criterion sits inside its margin)."""

    def __init__(self, part, lexemes, words, frames, base=None, lbase=None):
        self.part = part
        self.lbase = lbase or Counter()
        self.lexemes = lexemes
        self.words = words
        self.frames = frames
        self.base = base or Counter()      # counts that are always added (e.g. train rows for the word rule)
        self.train = part == "train"
        self.styles = ("defs", "yn", "YN")

    def hard(self, T):
        """Rows outside the audit's own thresholds (with a small margin): the swap search never lets this grow
        again once it falls. Train: depth mix, class / position mix, lexeme token caps and parity (all rows and
        yes/no rows), instruction-word parity, item floors and caps, cells, lexeme counts, choice share / balance /
        gold positions, distractor / mismatch / AR shares, R0 and kind shares, composition probes C1-C6, frame cap.
        Dev parts: depth floors, item floors, yes/no lexeme parity (iid + holdout), choice share and balance."""
        def out(x, lo, hi):
            return max(0.0, lo - x) + max(0.0, x - hi)
        n = max(1, T["rows"])
        yn = max(1, T["yn"])
        ch = max(1, T["ch"])
        h = 0.0
        if self.train:
            for d, (lo, hi) in {0: (0.163, 0.197), 1: (0.233, 0.267), 2: (0.283, 0.317), 3: (0.223, 0.257),
                                4: (0.0, 0.027)}.items():
                h += n * out(T[("depth", d)] / n, lo, hi)
            nt = max(1, sum(T[("cls", c)] for c in CLASS_TARGET))
            for c, (lo, hi) in {"syntactic": (0.253, 0.347), "affixal": (0.203, 0.297), "lexical": (0.203, 0.297),
                                "truth_frame": (0.103, 0.147), "cross+answer": (0.053, 0.097)}.items():
                h += nt * out(T[("cls", c)] / nt, lo, hi)
            npos = max(1, sum(T[("pos", p_)] for p_ in POS_TARGET))
            for p_, (lo, hi) in {"inner_claim": (0.253, 0.347), "outer_frame": (0.203, 0.297),
                                 "card_def": (0.153, 0.247), "separate_sentence": (0.053, 0.097),
                                 "yn_key+answer_map": (0.053, 0.097), "choice_option": (0.053, 0.097)}.items():
                h += npos * out(T[("pos", p_)] / npos, lo, hi)
            h += max(0.0, T[("lextok", "not")] + T[("lextok", "n't")] - 0.195 * nt)
            for x in self.lexemes:
                h += max(0.0, T[("lextok", x)] - 0.097 * nt)
                if lx.LEXICON[x]["split"] == "train" and lx.LEXICON[x]["cls"] != "lookalike":
                    h += max(0.0, 31 - T[("lexr", x)])
                # CL:351 / precheck 4.13: a distractor-capable lexeme is a distractor in >= 10% of its uses (A1)
                if lx.LEXICON[x]["split"] == "train" and can_distract(x) and T[("lextok", x)]:
                    h += max(0.0, 0.104 * T[("lextok", x)] - T[("lexdist", x)])
            for p_, cl in ALLOWED_CELLS.items():
                for c in cl:
                    for d in (1, 2, 3):
                        h += max(0.0, 31 - T[("cell", d, p_, c)])
            for it, pr in PRIORITY.items():
                h += max(0.0, FLOORS[pr][0] * 1.02 - T[("item", it)])
            h += max(0.0, T[("item", 9)] - 0.027 * n)
            h += n * out(T["arlex"] / max(1, T["odd_rows"]), 0.153, 1.0) * 0.5
            h += n * out(sum(T[("dist_d", d)] for d in range(5)) / n, 0.355, 1.0)
            for d in range(4):
                nd = max(1, T[("n_d", d)])
                h += nd * out(T[("dist_d", d)] / nd, 0.255, 1.0)
            h += n * out(sum(T[("mis_d", d)] for d in range(5)) / n, 0.305, 1.0)
            lad = max(1, T["ladders"])
            h += lad * (out(T["r0"] / lad, 0.803, 1.0) + out(T[("kind", "card")] / lad, 0.503, 1.0) +
                        out(T[("kind", "multitext")] / lad, 0.103, 0.197))
            for fr in self.frames:
                h += max(0.0, T[("frame", fr)] - 0.039 * n)
            h += yn * out(T["c1"] / yn, 0.455, 0.545)
            for d in range(5):
                nd = T[("ynd", d)]
                if nd:
                    h += max(0.0, T[("c2", d)] - 0.745 * nd)
            h += max(0.0, sum(T[("c2", d)] for d in range(5)) - 0.695 * yn)
            h += max(0.0, T["c3"] - 0.645 * yn) + max(0.0, T["c4"] - 0.595 * yn) + max(0.0, T["c5"] - 0.595 * yn)
            for nm in ("aff", "lex", "cross"):
                h += max(0.0, T[("c6", nm)] - 0.595 * yn)
        else:
            for d in range(4):
                h += max(0.0, 104 - T[("depth", d)])
            h += max(0.0, 21 - T[("depth", 4)])
            h += max(0.0, T[("depth", 4)] - 0.027 * n)   # CL:61 item 9 <= 3% of rows in dev too (r6)
            for it, pr in PRIORITY.items():
                fl = FLOORS[pr]
                need = (fl[1] - fl[2]) * 1.02 if self.part == "iid" else fl[2] * 1.05
                h += max(0.0, need - T[("item", it)])
        # lexeme parity: all rows (4.12) and yes/no rows (6.CS, >= 30 rows), 9 points of the 10 allowed
        for x in self.lexemes:
            r, o = T[("lexr", x)] + self.lbase[("lexr", x)], T[("lexo", x)] + self.lbase[("lexo", x)]
            if r >= 10:
                h += max(0.0, abs(o - r / 2) - 0.09 * r)
            r2, o2 = T[("lexr_yn", x)] + self.lbase[("lexr_yn", x)], T[("lexo_yn", x)] + self.lbase[("lexo_yn", x)]
            if r2 >= 28:
                h += max(0.0, abs(o2 - r2 / 2) - 0.09 * r2)
        # instruction words (SPEC 7.3): odd share <= 59% for words with >= 26 rows (dev and devx add rows)
        for w in self.words:
            r = T[("w_r", w)] + self.base[("w_r", w)]
            if r >= 26:
                h += max(0.0, T[("w_o", w)] + self.base[("w_o", w)] - 0.59 * r)
        h += n * out(T["ch"] / n, 0.175, 0.225) + ch * out(T["ch_neg"] / ch, 0.455, 0.545) + \
            ch * out(T["ch_even"] / ch, 0.485, 0.515)
        for k in (3, 4, 5):
            nk = T[("chk", k)]
            if nk >= 20:
                for p_ in range(k):
                    h += nk * out(T[("chpos", k, p_)] / nk, 1 / k - 0.027, 1 / k + 0.027)
        h += max(0.0, T[("item", 14)] - 0.097 * n) + max(0.0, T[("item", 38)] - 0.048 * n)
        return h

    def penalty(self, T, bd=None, viol=None):
        P = 0.0
        n = max(1, T["rows"])
        yn = max(1, T["yn"])
        train = self.train
        last = [0.0]

        def V(vec, w):
            """Record a violated direction: vec = {feature key: coefficient} that should grow."""
            if viol is not None and w > 0:
                viol.append((vec, w))

        def mark(name):
            if bd is not None:
                bd[name] = round(P - last[0], 3)
                last[0] = P
        # depth mix
        if train:
            for d, tgt in DEPTH_TARGET.items():
                if d == 4:
                    b = _band(T[("depth", 4)] / n, 0.0, 0.024, 300)
                    P += b
                    V({("depth", 4): -1}, b)
                else:
                    sh = T[("depth", d)] / n
                    b = _band(sh, tgt - 0.013, tgt + 0.013, 100)
                    P += b
                    V({("depth", d): 1 if sh < tgt else -1}, b)
        else:
            for d in range(4):
                P += 3.0 * max(0, 112 - T[("depth", d)])
            P += 3.0 * max(0, 23 - T[("depth", 4)])
        mark("depth")
        nt = max(1, sum(T[("cls", c)] for c in CLASS_TARGET))
        if train:
            for c, (lo, hi) in {"syntactic": (0.26, 0.34), "affixal": (0.21, 0.29), "lexical": (0.21, 0.29),
                                "truth_frame": (0.105, 0.145), "cross+answer": (0.055, 0.095)}.items():
                sh = T[("cls", c)] / nt
                b = _band(sh, lo, hi, 5)
                P += b
                V({("cls", c): 1 if sh < lo else -1}, b)
            mark("class")
            npos = max(1, sum(T[("pos", p_)] for p_ in POS_TARGET))
            for p_, (lo, hi) in {"inner_claim": (0.26, 0.34), "outer_frame": (0.21, 0.29), "card_def": (0.16, 0.24),
                                 "separate_sentence": (0.055, 0.095), "yn_key+answer_map": (0.055, 0.095),
                                 "choice_option": (0.055, 0.092)}.items():
                sh = T[("pos", p_)] / npos
                b = _band(sh, lo, hi, 8)
                P += b
                V({("pos", p_): 1 if sh < lo else -1}, b)
            mark("position")
            P += _band((T[("lextok", "not")] + T[("lextok", "n't")]) / nt, 0, 0.185, 5)
            for x in self.lexemes:
                P += _band(T[("lextok", x)] / nt, 0, 0.09, 5)
            mark("lexeme_share")
        for x in self.lexemes:
            r, o = T[("lexr", x)] + self.lbase[("lexr", x)], T[("lexo", x)] + self.lbase[("lexo", x)]
            if train and lx.LEXICON[x]["split"] == "train" and lx.LEXICON[x]["cls"] != "lookalike":
                P += 3.0 * max(0, 34 - r)
            if train and lx.LEXICON[x]["split"] == "train" and lx.LEXICON[x]["cls"] != "lookalike" and r < 34:
                V({("lexr", x): 1}, 3.0 * (34 - r))
            if r:
                tol = max(0.08 * r, 1.0)
                dev = abs(o - r / 2)
                if dev > tol:
                    P += 4.0 * (dev - tol)
                    sgn = 1 if o > r / 2 else -1     # too odd -> want even rows with x
                    V({("lexr", x): sgn, ("lexo", x): -2 * sgn}, 4.0 * (dev - tol))
            r2, o2 = T[("lexr_yn", x)] + self.lbase[("lexr_yn", x)], T[("lexo_yn", x)] + self.lbase[("lexo_yn", x)]
            if r2 >= 26:
                tol = max(0.08 * r2, 1.0)
                dev = abs(o2 - r2 / 2)
                if dev > tol:
                    P += 4.0 * (dev - tol)
                    sgn = 1 if o2 > r2 / 2 else -1
                    V({("lexr_yn", x): sgn, ("lexo_yn", x): -2 * sgn}, 4.0 * (dev - tol))
            if train and can_distract(x):
                use = T[("lextok", x)]
                if use:
                    need = 0.11 * use - T[("lexdist", x)]
                    if need > 0:
                        P += 2.0 * need
                        V({("lexdist", x): 1}, 2.0 * need)
        mark("lexeme")
        if train:
            for p_, cl in ALLOWED_CELLS.items():
                for c in cl:
                    for d in (1, 2, 3):
                        b = 3.0 * max(0, 34 - T[("cell", d, p_, c)])
                        P += b
                        V({("cell", d, p_, c): 1}, b)
        mark("cells")
        for it, pr in PRIORITY.items():
            fl = FLOORS[pr]
            if train:
                b = 3.0 * max(0, fl[0] * 1.06 - T[("item", it)])
            else:
                need = (fl[1] - fl[2]) * 1.1 if self.part == "iid" else fl[2] * 1.15
                b = 3.0 * max(0, need - T[("item", it)])
            P += b
            V({("item", it): 1}, b)
        if train:
            P += _band(T[("item", 9)] / n, 0, 0.027, 8)
        P += _band(T[("item", 14)] / n, 0, 0.095, 5)
        P += _band(T[("item", 38)] / n, 0, 0.047, 5)
        mark("items")
        ch = max(1, T["ch"])
        b = _band(T["ch"] / n, 0.185, 0.215, 60)
        P += b
        V({"ch": 1 if T["ch"] / n < 0.185 else -1}, b)
        b = _band(T["ch_neg"] / ch, 0.47, 0.53, 30)
        P += b
        V({"ch_neg": 1 if T["ch_neg"] / ch < 0.47 else -1, "ch": 0}, b)
        b = _band(T["ch_even"] / ch, 0.49, 0.51, 30)
        P += b
        V({"ch_even": 1 if T["ch_even"] / ch < 0.49 else -1}, b)
        for k in (3, 4, 5):
            nk = T[("chk", k)]
            if not nk:
                continue
            for p_ in range(k):
                share = T[("chpos", k, p_)] / nk
                P += _band(share, 1 / k - 0.022, 1 / k + 0.022, 6)
        for nm in ("neg", "cue", "k", "d"):
            r = abs(_corr(T, nm))
            if r > 0.035:
                P += 2e4 * (r - 0.035) ** 2
        mark("choice")
        if train:
            P += _band(sum(T[("dist_d", d)] for d in range(5)) / n, 0.37, 1.0, 5)
            for d in range(4):
                nd = max(1, T[("n_d", d)])
                b = _band(T[("dist_d", d)] / nd, 0.27, 1.0, 5)
                P += b
                V({("dist_d", d): 1}, b)
            P += _band(sum(T[("mis_d", d)] for d in range(5)) / n, 0.32, 1.0, 5)
            P += _band(T["arlex"] / max(1, T["odd_rows"]), 0.165, 1.0, 5)
        mark("distractors")
        P += _band(T["c1"] / yn, 0.465, 0.535, 8)
        for d in range(5):
            nd = T[("ynd", d)]
            if nd:
                P += _band(T[("c2", d)] / nd, 0, 0.73, 5)
        P += _band(sum(T[("c2", d)] for d in range(5)) / yn, 0, 0.68, 5)
        P += _band(T["c3"] / yn, 0, 0.63, 5)
        b = _band(T["c4"] / yn, 0, 0.58, 8)
        P += b
        V({"c4": -1, "yn": 0.5}, b)
        b = _band(T["c5"] / yn, 0, 0.58, 8)
        P += b
        V({"c5": -1, "yn": 0.5}, b)
        for nm in ("aff", "lex", "cross"):
            P += _band(T[("c6", nm)] / yn, 0, 0.58, 5)
        mark("composition")
        for w in self.words:
            # train words from 16 rows (the dev parts and devx add rows before the >= 30-row rule applies)
            r = T[("w_r", w)] + self.base[("w_r", w)]
            if r >= 16:
                o = T[("w_o", w)] + self.base[("w_o", w)]
                over = o - WORD_ODD_MAX * r - (0.5 if r < 30 else 0.0)
                if over > 0:
                    P += 6.0 * over
                    V({("w_r", w): 1, ("w_o", w): -2}, 6.0 * over)
        mark("words")
        if train:
            for fr in self.frames:
                v = T[("frame", fr)]
                if v / n > 0.037:
                    P += 5.0 * (v - 0.037 * n)
        tot_style = Counter()
        for d in range(5):
            for s_ in self.styles:
                tot_style[s_] += T[("style", d, s_)]
        ts = max(1, sum(tot_style.values()))
        for d in range(5):
            nd = T[("ynd", d)]
            if nd < 10:
                continue
            for s_, v in tot_style.items():
                exp = v / ts * nd
                dev = abs(T[("style", d, s_)] - exp) - max(0.016 * nd, 0.8)
                if dev > 0:
                    P += 4.0 * dev
        mark("frames_styles")
        if train:
            lad = max(1, T["ladders"])
            P += _band(T["r0"] / lad, 0.81, 1.0, 8)
            P += _band(T[("kind", "card")] / lad, 0.515, 1.0, 8)
            P += _band(T[("kind", "multitext")] / lad, 0.11, 0.19, 8)
            for e in range(4):
                P += 3.0 * max(0, 34 - T[("embed", e)])
            for dd in ("same_clause", "same_sentence", "next_sentence", "far", "other_field"):
                P += 3.0 * max(0, 34 - T[("dbin", dd)])
        mark("kinds_misc")
        return P


def select_pairs(cands, n, obj, rng, log=print, iters=60000, must=None, feats=None, init=None, t0_temp=None,
                 restart=True):
    """Local search over swaps of whole twin pairs: keep exactly n pairs (must = a predicate every kept pair
    satisfies) and minimise obj.penalty. Half the proposals are guided: a violated criterion is drawn (weighted by
    its penalty) and the swap trades a kept pair that does little for it against a spare pair that does much."""
    feats = feats or [pair_features(c, obj.words) for c in cands]
    ok = [i for i in range(len(cands)) if must is None or must(cands[i])]
    rng.shuffle(ok)
    if init is not None:                       # continue from a given selection (audit refinement rounds)
        iset = set(init)
        selected, rest = list(init), [i for i in ok if i not in iset]
    else:
        selected, rest = ok[:n], ok[n:]
    T0 = SELECT_T0 if t0_temp is None else t0_temp
    # feature -> pairs that carry it (guided moves look only at pairs that can change the violated count)
    index = defaultdict(list)
    for i in ok:
        for k in feats[i]:
            index[k].append(i)
    where = {}                       # pair -> ("s", position in selected) or ("r", position in rest)
    for k_, i in enumerate(selected):
        where[i] = ("s", k_)
    for k_, i in enumerate(rest):
        where[i] = ("r", k_)
    T = Counter()
    for i in selected:
        T.update(feats[i])
    cur = obj.penalty(T)
    hcur = obj.hard(T)
    best, best_sel, best_h = cur, list(selected), hcur
    t0 = time.time()
    viol, wsum = [], 0.0

    def contrib(i, vec):
        f = feats[i]
        return sum(c * f[k] for k, c in vec.items())

    temp = [0.0]

    def swap(a_idx, b_idx):
        nonlocal cur, hcur, best, best_sel, best_h
        ia, ib = selected[a_idx], rest[b_idx]
        T.subtract(feats[ia])
        T.update(feats[ib])
        hnew = obj.hard(T)
        if hnew <= hcur + 1e-12:
            new = obj.penalty(T)
            if new <= cur or hnew < hcur - 1e-12 or \
                    (temp[0] > 0 and rng.random() < math.exp(-(new - cur) / temp[0])):
                cur, hcur = new, hnew
                selected[a_idx], rest[b_idx] = ib, ia
                if (hcur, cur) < (best_h, best):
                    best, best_sel, best_h = cur, list(selected), hcur
                where[ib] = ("s", a_idx)
                where[ia] = ("r", b_idx)
                return True
        T.subtract(feats[ib])
        T.update(feats[ia])
        return False
    for it in range(iters):
        if not rest or best <= 1e-9:
            break
        # simulated annealing: a falling temperature lets the search leave local minima early on; every 10,000
        # proposals the search restarts from the best set when it has drifted above it
        temp[0] = T0 * max(0.0, 1.0 - it / (0.8 * iters)) ** 2
        if restart and it % 10000 == 0 and it and (hcur, cur) > (best_h, best + 1e-9):
            for i in selected:
                T.subtract(feats[i])
            selected[:] = list(best_sel)
            sset = set(selected)
            rest[:] = [i for i in ok if i not in sset]
            for i in selected:
                T.update(feats[i])
            cur, hcur = obj.penalty(T), obj.hard(T)
            where.clear()
            for k_, i in enumerate(selected):
                where[i] = ("s", k_)
            for k_, i in enumerate(rest):
                where[i] = ("r", k_)
        if it % 400 == 0:
            viol = []
            obj.penalty(T, viol=viol)
            wsum = sum(w for _, w in viol)
        if viol and rng.random() < 0.6:
            x = rng.random() * wsum
            for vec, w in viol:
                x -= w
                if x <= 0:
                    break
            pool_ = set()
            for k in vec:
                lst = index.get(k, ())
                pool_.update(lst if len(lst) <= 400 else rng.sample(lst, 400))
            sa = [where[i][1] for i in pool_ if where[i][0] == "s"]
            sb = [where[i][1] for i in pool_ if where[i][0] == "r"]
            sa = (rng.sample(sa, 40) if len(sa) > 40 else sa) or rng.sample(range(len(selected)), min(40, len(selected)))
            sb = (rng.sample(sb, 40) if len(sb) > 40 else sb) or rng.sample(range(len(rest)), min(40, len(rest)))
            a_idx = min(sa, key=lambda k: contrib(selected[k], vec))
            b_idx = max(sb, key=lambda k: contrib(rest[k], vec))
            swap(a_idx, b_idx)
        else:
            swap(rng.randrange(len(selected)), rng.randrange(len(rest)))
        if it % 20000 == 0 and it:
            log(f"    select {obj.part}: iter {it}, hard {hcur:.4f}, penalty {cur:.2f} ({time.time() - t0:.0f} s)")
    if init is not None and hcur <= 1e-12:
        best_sel = list(selected)      # a refinement round returns where the walk ended (a different selection)
    T = Counter()
    for i in best_sel:
        T.update(feats[i])
    bd = {}
    best = obj.penalty(T, bd)
    log(f"  select {obj.part}: {len(best_sel)} of {len(cands)} pairs, hard {obj.hard(T):.4f}, penalty {best:.3f} "
        f"({time.time() - t0:.0f} s); by section {({k: v for k, v in bd.items() if v})}")
    return [cands[i] for i in sorted(best_sel)], T, best, sorted(best_sel)


if __name__ == "__main__":
    main()
