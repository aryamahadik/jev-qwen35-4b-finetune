"""COMMIT build frame: data access, commit-use registry (A52), wordings, persona seeds, card shells, the row emitter
(style pick, fmt1 render + loader_check, counted length with the 1.3 re-cut, negcount check, meta + sidecar).
Splits: 'cand' (candidates_r1, train repos), 'qc' (qc_sample, train repos, commits disjoint from cand), 'dev'
(mixdev_S5, the 30 held-out repo groups, held-out styles)."""
from __future__ import annotations

import ast
import collections
import functools
import glob
import gzip
import json
import random
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import render as RD  # noqa: E402
import texts as T  # noqa: E402

sys.path.insert(0, str(C.CSRC / "common"))
import negcount  # noqa: E402

GIT_SHA = subprocess.run(["git", "-C", str(C.LEAN), "rev-parse", "--short=12", "HEAD"], capture_output=True,
                         text=True).stdout.strip() or "unknown"
SEED = 20261003


class FrameError(Exception):
    pass


# ---------------------------------------------------------------------------------------------------------------
# data

_LINES = None      # rid -> raw JSON line (records are parsed on demand)
_INDEX = None      # rid -> light fields
_GROUPS = None


def _load():
    global _LINES, _INDEX
    if _LINES is None:
        _LINES, _INDEX = {}, {}
        with gzip.open(C.DATA / "pool.jsonl.gz", "rt") as f:
            for line in f:
                r = json.loads(line)
                _LINES[r["rid"]] = line
                _INDEX[r["rid"]] = {"ds": r["ds"], "group": r["group"], "split": r["split"], "n_files": r["n_files"],
                                    "lines": r["added"] + r["removed"], "lang": r["lang"], "bot": r["bot"],
                                    "first": r["msg"].split("\n", 1)[0][:200],
                                    "mtok": frozenset(C.m_tokens(r["msg"]))}


def index() -> dict:
    _load()
    return _INDEX


@functools.lru_cache(maxsize=60000)
def rec(rid: str) -> dict:
    _load()
    return json.loads(_LINES[rid])


def groups() -> dict:
    global _GROUPS
    if _GROUPS is None:
        _GROUPS = json.load(open(C.DATA / "groups.json"))
    return _GROUPS


@functools.lru_cache(maxsize=None)
def by_group(split: str, ds: str | None = None) -> dict:
    out = collections.defaultdict(list)
    for rid, x in index().items():
        if x["split"] == split and (ds is None or x["ds"] == ds):
            out[x["group"]].append(rid)
    for v in out.values():
        v.sort()
    return out


def pack(card_id: str, split: str, ds: str, frac: float = 0.4, eligible=None) -> tuple[str, list[str]]:
    """Repo-group set of a card (the domain pack, MAP): a fixed-seed share of the split's groups of one dataset."""
    gs = sorted(g for g in by_group(split, ds) if eligible is None or g in eligible)
    sel = [g for g in gs if C.h01("pack", card_id, g) < frac]
    return "pk-" + C.sha256(card_id + "|" + ",".join(sel))[:10], sel


# ---------------------------------------------------------------------------------------------------------------
# commit-use registry (A52): one type per commit, one base row per commit; a message shown in <= 2 uses

def sealed_exclude() -> set:
    """Record ids whose rows hit the sealed checker (replaced on the next build: never drawn again)."""
    p = C.DATA / "sealed_exclude.json"
    return set(json.load(open(p))) if p.exists() else set()


class Registry:
    def __init__(self):
        self.excluded = sealed_exclude()
        self.type_of = {}
        self.base = set()
        self.msg_uses = collections.Counter()
        self.split_of = {}

    def can_base(self, rid: str, typ: str, split: str) -> bool:
        return rid not in self.excluded and rid not in self.base and self.type_of.get(rid, typ) == typ and self.split_of.get(rid, split) == split \
            and self.msg_uses[rid] < 2

    def take_base(self, rid: str, typ: str, split: str):
        assert self.can_base(rid, typ, split), rid
        self.base.add(rid)
        self.type_of[rid] = typ
        self.split_of[rid] = split
        self.msg_uses[rid] += 1

    def can_extra(self, rid: str, typ: str, split: str) -> bool:
        return rid not in self.excluded and self.type_of.get(rid, typ) == typ and self.split_of.get(rid, split) == split and self.msg_uses[rid] < 2

    def take_extra(self, rid: str, typ: str, split: str):
        assert self.can_extra(rid, typ, split), rid
        self.type_of[rid] = typ
        self.split_of[rid] = split
        self.msg_uses[rid] += 1


# ---------------------------------------------------------------------------------------------------------------
# wordings (formats-2 family pools) and persona seeds (O*NET titles via packs)

def wordings(ctype: str, form: str) -> list[dict]:
    rows = [json.loads(l) for l in open(C.CSRC / "formats" / "formats-2" / "wordings" / "family_pools.jsonl")]
    ok = {"any", form}
    return [r for r in rows if r["family"] == "COMMIT" and r["commit_type"] == ctype and set(r["forms"]) & ok]


CANON_QID = re.compile(r"(rl|tl|gh0|md0)")


def card_wordings(ctype: str, form: str, card_id: str, k: int = 6) -> list[dict]:
    ws = sorted(wordings(ctype, form), key=lambda r: C.h01("wd", card_id, form, r["id"]))
    return ws[:k]


def persona_pool() -> list[tuple]:
    out = {}
    for fn in sorted(glob.glob(str(C.CSRC / "packs" / "packs-*" / "packs.jsonl"))):
        for line in open(fn):
            r = json.loads(line)
            ps = r.get("persona_seed")
            if isinstance(ps, str) and ps.startswith("{"):
                ps = ast.literal_eval(ps)
            if isinstance(ps, dict) and ps.get("onet_code") and ps.get("onet_title"):
                out[ps["onet_code"]] = ps["onet_title"]
                continue
            p = r.get("persona")
            if isinstance(p, str) and p.startswith("{"):
                p = ast.literal_eval(p)
            if isinstance(p, dict) and p.get("persona_seed") and p.get("onet_title"):
                out[p["persona_seed"]] = p["onet_title"]
    return sorted(out.items())


def draw_persona(card_id: str):
    pp = persona_pool()
    by = collections.defaultdict(list)
    for code, title in pp:
        by[code[:2]].append((code, title))
    gs = sorted(by)
    g = gs[int(C.h01("persona-group", card_id) * len(gs))]
    lst = by[g]
    return lst[int(C.h01("persona", card_id) * len(lst))]


# ---------------------------------------------------------------------------------------------------------------
# yes-rate draws (R2-11 antithetic pairs; R3-SC1 band check)

def antithetic_rates(card_ids: list[str], n_plan: int, key: str) -> dict:
    import math
    out = {}
    ids = sorted(card_ids)
    for i in range(0, len(ids) - 1, 2):
        a, b = ids[i], ids[i + 1]
        t = 0
        while True:
            r = 0.2 + 0.6 * C.h01("rate", key, a, t)
            k = round(r * n_plan)
            if math.ceil(0.2 * n_plan) <= k <= math.floor(0.8 * n_plan):
                break
            t += 1
        out[a], out[b] = r, 1 - r
    if len(ids) % 2:
        out[ids[-1]] = 0.5
    return out


def yes_count(r: float, n: int) -> int:
    return round(r * n)


# ---------------------------------------------------------------------------------------------------------------
# row emitter

class Emitter:
    def __init__(self, split: str):
        self.split = split
        self.heldout = split == "dev"
        self.tok = RD.Tok()
        self.rows, self.side, self.rels = [], [], []
        self.drops = collections.Counter()
        self.lengths = collections.defaultdict(list)

    def licence(self, rec: dict, extra: list[dict]) -> str:
        lic = sorted({rec["licence"]} | {e["licence"] for e in extra})
        return f"{C.COMPILATION_LICENCE[rec['ds']]}; repo licence: {', '.join(lic)}"

    def emit(self, sp: dict) -> dict | None:
        """sp keys: id, type, card, rec, view, form, qtype, question, qid, k, wording, card_ir, options, gold,
        msg, build_extra(budget)->(extra str, meta dict) | None, heading, depth, twin_of, twin_kind, call_id,
        option_level, trigger_entities, sidecar (dict), edge (list), extra_recs (records), state_first (str)."""
        card = sp["card"]
        restricted = sp["type"] == "route" or sp["view"] == "message_only"
        q = sp["question"]
        if sp["qtype"] == "noul" and "?" in sp["wording"]["text"] and not CANON_QID.match(sp.get("qid") or ""):
            # a polar question in the preamble must never meet a negated or inverted-frame question (it would ask
            # the opposite thing): those rows draw from the card's question-free yes/no wordings only
            alt = [w for w in card_wordings(sp["type"], "yn", card["card_id"], k=999) if "?" not in w["text"]]
            if not alt:
                raise FrameError("no question-free yes/no wording for " + sp["type"])
            sp = {**sp, "wording": alt[int(C.h01("wdq", card["card_id"], sp["id"]) * len(alt))]}
        if sp["qtype"] == "noul":
            ks = negcount.k_syn(q)
            if ks != sp["k"]:
                raise FrameError(f"negcount {ks} != template {sp['k']} on {sp['qid']}")
        budgets = sp.get("budgets") or [1500, 1100, 800, 550, 350, 200]
        style = None
        for bi, b in enumerate(budgets):
            got = sp["build_extra"](b) if sp.get("build_extra") else ("", {})
            if got is None:
                self.drops[f"{sp['type']}:decisive_over_cap"] += 1
                return None
            extra, emeta = got
            emeta = dict(emeta or {})
            sfirst = emeta.pop("_state_first", None) or sp.get("state_first")
            doc_msg = sp["msg"]
            if style is None:
                if not doc_msg.strip():
                    self.drops[f"{sp['type']}:empty_message"] += 1
                    return None
                try:
                    style = RD.pick_style("restricted" if restricted else "full", self.heldout, sp["id"],
                                          doc=sp.get("doc") or RD.message_doc(doc_msg,
                                                                              sp.get("heading", "Commit message")),
                                          allow=sp.get("style_ok"))
                except RD.FormatError:
                    self.drops[f"{sp['type']}:no_style_renders_message"] += 1
                    return None
            f, res = RD.assemble(style, msg=doc_msg, extra=extra or None, question=q, qtype=sp["qtype"],
                                 card=sp["card_ir"], options=sp.get("options"), wording=sp["wording"]["text"],
                                 gold=sp["gold"], row_id=sp["id"], heading=sp.get("heading", "Commit message"),
                                 state_first=sfirst, doc=sp.get("doc"))
            row = {"id": sp["id"], "qtype": sp["qtype"], "options": sp.get("options") if sp["qtype"] == "choice"
                   else None, "gold": sp["gold"], **f}
            n = self.tok.count(row)
            if n <= RD.CAP:
                break
            if not sp.get("build_extra") or bi == len(budgets) - 1:
                self.drops[f"{sp['type']}:{sp['form']}:over_cap"] += 1
                return None
        rec = sp["rec"]
        extra_recs = sp.get("extra_recs") or []
        meta = {"spec_id": C.SPEC_ID, "card_id": card["card_id"], "domain_pack": card["pack_id"],
                "sampler": card["sampler"], "gen_version": C.GEN_VERSION, "git_sha": GIT_SHA,
                "seed": int(C.h01("seed", sp["id"]) * 2 ** 31), "structure_hash":
                    C.sha256(C.jdump([sp["type"], card["card_id"], rec["rid"], sp["view"], sp.get("variant")])),
                "difficulty_bin": None, "crowd_pg": None, "depth": sp.get("depth", 1), "deep": False,
                "format_style": style["id"], "wording_id": sp["wording"]["id"],
                "defs_style": sp.get("defs_style", card.get("defs_style", "one_line")),
                "twin_of": sp.get("twin_of"), "twin_kind": sp.get("twin_kind"),
                "text_source": {"dataset": rec["ds"], "record_id": rec["rid"], "split": "train"},
                "licence": self.licence(rec, extra_recs), "edge": sp.get("edge", []),
                "input_view": sp["view"]}
        if sp["view"] == "message_only":
            meta["trigger_entities"] = sp.get("trigger_entities", [])
        if sp.get("option_level") is not None:
            meta["option_level"] = sp["option_level"]
        if card.get("persona"):
            meta["persona_seed"] = card["persona"][0]
        meta.update(emeta or {})
        out = {"id": sp["id"], "group_id": f"{rec['group']}|{rec['rid']}", "call_id": sp["call_id"],
               "source": f"commit_{sp['type']}", "state": f["state"], "qtype": sp["qtype"],
               "instructions": f["instructions"], "options": row["options"], "gold": sp["gold"],
               "role": sp.get("role", "base" if not sp.get("twin_of") else "twin"), "card": f["card"], "meta": meta}
        side = {"id": sp["id"], "commit_type": sp["type"], "repo_group": rec["group"], "language": rec["lang"],
                "sem_active": sp.get("sem_active", []), "card_form": sp.get("card_form", "normal"),
                "card_variant": sp.get("variant"), "polarity": sp.get("polarity"),
                "yes_rate_drawn": card.get("r"), "rule_id": card.get("rule_id"), "rubric_id": card.get("rubric_id"),
                "twin_flag": bool(sp.get("twin_of")), "asked_option": sp.get("asked_option"),
                "qid": sp["qid"], "k_syn": sp.get("k", 0), "counted_tokens": n, "split": self.split,
                "extra_records": [{"dataset": e["ds"], "record_id": e["rid"], "repo": e["repo"],
                                   "repo_licence": e["licence"], "use": e.get("_use", "extra")} for e in extra_recs],
                **(sp.get("sidecar") or {})}
        self.rows.append(out)
        self.side.append(side)
        self.lengths[(sp["type"], sp["form"])].append(n)
        return out

    def relate(self, a: str, b: str, kind: str):
        self.rels.append({"a": a, "b": b, "type": kind})

    def trim_per_type(self, cap: int):
        """S5 dev set: keep whole units (call_id) in emission order up to `cap` rows per type (spec: 400 items)."""
        units = collections.OrderedDict()
        for r, sd in zip(self.rows, self.side):
            units.setdefault(r["call_id"], []).append((r, sd))
        have, keep = collections.Counter(), set()
        for cid, u in units.items():
            t = u[0][0]["source"]
            if have[t] + len(u) <= cap:
                have[t] += len(u)
                keep.add(cid)
        pairs = [(r, sd) for r, sd in zip(self.rows, self.side) if r["call_id"] in keep]
        ids = {r["id"] for r, _ in pairs}
        self.rows, self.side = [r for r, _ in pairs], [sd for _, sd in pairs]
        self.rels = [x for x in self.rels if x["a"] in ids and x["b"] in ids]
        return dict(have)

    def write(self, name: str):
        C.OUT.mkdir(parents=True, exist_ok=True)
        with open(C.OUT / f"{name}.jsonl", "w") as f:
            for r in self.rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        with open(C.OUT / f"{name}.sidecar.jsonl", "w") as f:
            for r in self.side:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        if self.split != "dev":
            with open(C.OUT / f"{name}.rel.jsonl", "w") as f:
                for r in self.rels:
                    f.write(json.dumps(r) + "\n")


def rng(*key) -> random.Random:
    return random.Random(int(C.sha256("\x1f".join(map(str, key)))[:16], 16))
