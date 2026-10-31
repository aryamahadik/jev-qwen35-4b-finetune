"""F11 S7: real-text codebook rows (G0 S7, SEM-45, SEM-46; spec 2.3). Generator side (solver A = the formats-2
codebook's full-set table). EDOS is out (X15 not granted: codebooks 'blocked_X15'), so S7 = MAMS 50 / XED 50.

Records: formats-2 records/*.jsonl with eligible.F11_S7, train part of the shared public-3 split, minus dev-part texts,
minus public-3 claims, minus F10's S7 / S5 records (one claim per normalized text across F11 groups; a record is used
in one twin set only). Twins: neg/dneg, attack (submitter note outside the quoted text), defs_swap, focal_target (MAMS).
card_flip is not built in round 1 (optional twin; logged in the build report).
"""
from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from functools import lru_cache

import lex
from common import (FAMILY, GEN_VERSION, SPEC_SHA256, FMT2, CSRC, canon, rng, sha256_text, toks, git_sha)
from fmt1 import card as fcard, pool
from names import code_ids, code_names
from rows import RowFail, prose_styles, f11_wordings

SCHEMES = ("xed", "mams_acsa", "mams_atsa")
REC_FILE = {"xed": "xed.jsonl", "mams_acsa": "mams_acsa.jsonl", "mams_atsa": "mams_atsa.jsonl"}
DATASET = {"xed": "xed_en", "mams_acsa": "mams", "mams_atsa": "mams"}
LICENCE = {"xed": "CC BY 4.0 (https://github.com/Helsinki-NLP/XED@76666d251f14)",
           "mams_acsa": "Apache-2.0 (https://github.com/siat-nlp/MAMS-for-ABSA/blob/master/LICENSE@cddcdb0f423b)",
           "mams_atsa": "Apache-2.0 (https://github.com/siat-nlp/MAMS-for-ABSA/blob/master/LICENSE@cddcdb0f423b)"}
TARGET = {"mams_acsa": ("aspect", "aspects"), "mams_atsa": ("target", "targets")}
EMOTIONS = ("anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust")
POLS = ("positive", "negative", "neutral")
LEADS = ("Text received by the {org} for coding", "Text logged by the {org} for review",
         "Text passed to the {org} ({decider} review)", "Text to code for the {org}")
_GIT = git_sha()


# ------------------------------------------------------------------------------------------------ data
@lru_cache(maxsize=1)
def codebooks():
    out = []
    for l in open(FMT2 / "codebooks" / "codebooks.jsonl"):
        c = json.loads(l)
        if c["family"] == FAMILY and c["status"] == "ready" and c["scheme"] in SCHEMES:
            out.append(c)
    return out


@lru_cache(maxsize=1)
def split_info():
    dev, part, claimed = set(), {}, set()
    for l in open(CSRC / "public" / "public-3" / "out" / "public3_split_3e.jsonl"):
        r = json.loads(l)
        part[r["id"]] = r["part"]
        if r["part"] != "train":
            dev.add(r["norm_sha256"])
    for l in open(CSRC / "public" / "public-3" / "out" / "public3_record_claims.jsonl"):
        claimed.add(json.loads(l)["norm_sha256"])
    return part, dev, claimed


@lru_cache(maxsize=1)
def f10_claims():
    """(dataset, record_id) pairs F10 uses in its training candidates and its S5 dev set."""
    out = set()
    for fn in ("candidates_r1.jsonl", "mixdev_S5.jsonl"):
        p = CSRC / "F10" / "out" / fn
        if not p.exists():
            continue
        for l in open(p):
            ts = json.loads(l)["meta"].get("text_source")
            if ts:
                out.add((ts["dataset"], str(ts["record_id"])))
    return out


S5_RESERVE = 0.08      # share of eligible texts reserved (by hash) for the S5 codebook arm; never in training rows


def s5_reserved(norm_sha256: str) -> bool:
    from common import uhash
    return uhash("F11-S5-reserve", norm_sha256) < S5_RESERVE


@lru_cache(maxsize=8)
def records(scheme, arm="train"):
    part, dev, claimed = split_info()
    f10 = f10_claims()
    drops = Counter()
    out = []
    f10_norm = set()
    rows = [json.loads(l) for l in open(FMT2 / "records" / REC_FILE[scheme])]
    for r in rows:
        if (r["dataset"], str(r["record_id"])) in f10:
            f10_norm.add(r["norm_sha256"])
    for r in rows:
        if not (r.get("eligible") or {}).get("F11_S7"):
            drops["not_eligible"] += 1
        elif arm == "s5" and scheme == "xed":
            # S5 codebook arm on XED: the 10% part of the orchestrator split (G0 S5), never a train-part record
            if part.get(r["id"]) != "dev":
                drops["xed_train_part"] += 1
            elif r["norm_sha256"] in claimed:
                drops["public_claim"] += 1
            elif r["norm_sha256"] in f10_norm:
                drops["f10_claim"] += 1
            else:
                out.append(r)
        elif part.get(r["id"], "train") != "train":
            drops["dev_part"] += 1
        elif r["norm_sha256"] in dev:
            drops["dev_text"] += 1
        elif r["norm_sha256"] in claimed:
            drops["public_claim"] += 1
        elif r["norm_sha256"] in f10_norm:
            drops["f10_claim"] += 1
        elif s5_reserved(r["norm_sha256"]) != (arm == "s5"):
            drops["other_arm"] += 1
        else:
            out.append(r)
    return out, dict(drops)


def units(rec, scheme):
    """Coding units: XED one per record; ACSA one per annotated category; ATSA one per term that passes the
    unique-term rule (F11-R3-05)."""
    a = rec["ann"]
    if scheme == "xed":
        return [None]
    if scheme == "mams_acsa":
        cats = [x[0] for x in a["aspects"]]
        if len(cats) != len(set(cats)):
            return []
        return list(range(len(a["aspects"])))
    terms = a["terms"]
    names = [t["term"].lower() for t in terms]
    if len(names) != len(set(names)) or not a.get("terms_unique", True):
        return []
    out = []
    for i, t in enumerate(terms):
        n = len(re.findall(r"(?<!\w)" + re.escape(t["term"].lower()) + r"(?!\w)", rec["text"].lower()))
        if n == 1 and t.get("span_ok", True):
            out.append(i)
    return out


def combo(rec, ti, scheme):
    a = rec["ann"]
    if scheme == "xed":
        return frozenset(a["emotions"])
    if scheme == "mams_acsa":
        return (a["aspects"][ti][1], frozenset(x[1] for j, x in enumerate(a["aspects"]) if j != ti))
    return (a["terms"][ti]["polarity"], frozenset(t["polarity"] for j, t in enumerate(a["terms"]) if j != ti))


def target_text(rec, ti, scheme):
    if scheme == "mams_acsa":
        return rec["ann"]["aspects"][ti][0]
    if scheme == "mams_atsa":
        return rec["ann"]["terms"][ti]["term"]
    return None


def steps(c, scheme):
    """One-step neighbours of an annotation combination (R26)."""
    out = []
    if scheme == "xed":
        for e in EMOTIONS:
            s = set(c) ^ {e}
            if s:
                out.append(frozenset(s))
        return out
    p0, oth = c
    for p in POLS:
        if p != p0:
            out.append((p, oth))
    for p in POLS:
        s = set(oth) ^ {p}
        if s:
            out.append((p0, frozenset(s)))
    return out


def s7_depth(c, cb, gold_code):
    """Repair r1 (A47 with R26 steps on S7): an S7 row has one attribute, the record's annotation vector, which the
    codebook maps to a code; no rule ever changes the result. d = 1 when some one-step change (R26) of the vector
    alters the gold code (an uncovered vector counts), else 0. The earlier d (label count + 1 for a merged code)
    restated the gold's own label count in metadata (G6 d; G7 'depth x option kind' crosses)."""
    return int(any(c.table.get(s2) != gold_code for s2 in steps(cb, c.scheme)))


def set_key(fs, scheme):
    if scheme == "xed":
        return frozenset(fs)
    return (fs[0], frozenset(fs[1]))


# ------------------------------------------------------------------------------------------------ card
def label_list(xs):
    xs = list(xs)
    if len(xs) == 1:
        return xs[0]
    return ", ".join(xs[:-1]) + " and " + xs[-1]


class S7Card:
    def __init__(self, cb, wrap, idx, *, short=False, attempt=0):
        key = ("s7card", cb["id"], wrap["pack_id"], idx, attempt)
        r = rng(*key)
        self.r = r
        self.sampler = "S7"
        self.is_s7 = True
        self.records = False
        self.cb = cb
        self.scheme = cb["scheme"]
        self.card_id = f"F11-S7-{idx:03d}"
        self.pack_id = wrap["pack_id"]
        self.persona_seed = wrap.get("persona_seed")
        self.wrap = wrap
        self.form = "short" if short else "oneline"
        self.shape = "s7"
        self.inverted = False
        self.report, self.reports = "text", "texts"
        self.dv = r.choice(("DV01", "DV02", "DV03", "DV05"))
        self.mark = r.choice(lex.MARK_WORDS)
        self.examples, self.worked = [], []
        n = len(cb["codes"])
        self.sets = []
        for c in cb["codes"]:
            if self.scheme == "xed":
                self.sets.append([sorted(fs, key=EMOTIONS.index) for fs in c["full_sets"]])
            else:
                self.sets.append([(fs[0], sorted(fs[1], key=POLS.index)) for fs in c["full_sets"]])
        self.marks = [bool(c["action_mark"]) for c in cb["codes"]]
        self.build_table()
        self.ids = code_ids(n, *key)
        sib = defaultdict(list)
        for k, ss in enumerate(self.sets):
            head = ss[0][0] if self.scheme == "xed" else ss[0][0]
            sib[head].append(k)
        groups = []
        for v in sib.values():
            for j in range(0, len(v), 3):
                groups.append(v[j:j + 3])
        avoid = list(EMOTIONS) + list(POLS) + ["named", "others", "other"]
        if short:
            self.names = [c["labelset_name"] for c in cb["codes"]]
            if any(x is None for x in self.names) or any(len(s) != 1 for s in self.sets):
                raise RowFail("short S7 card needs single-set codes with label-set names")
        else:
            self.names = code_names(n, groups, *key, avoid=avoid)
        ls = [c["labelset_name"] for c in cb["codes"]]
        self.swapped = None
        if not short and all(ls):
            perm = list(range(n))
            for _ in range(50):
                r.shuffle(perm)
                if all(perm[i] != i for i in range(n)):
                    self.swapped = [ls[perm[i]] for i in range(n)]
                    break
        self.order = list(range(n))
        r.shuffle(self.order)
        self.name_rows = True

    def build_table(self):
        self.table = {}
        for k, ss in enumerate(self.sets):
            for fs in ss:
                key = set_key(fs, self.scheme)
                if key in self.table:
                    raise RowFail("codebook covers one combination twice")
                self.table[key] = k

    @property
    def fill(self):
        d = {"report": "text", "reports": "texts", "entity": "text", "entities": "texts", "event": "review"}
        if self.scheme in TARGET:
            d["target"], d["targets"] = TARGET[self.scheme]
        return d

    def code_label(self, k, form):
        if form in ("code", "masked"):
            return self.ids[k]
        if form == "swapped":
            return self.swapped[k]
        return self.names[k]

    def code_neighbours(self):
        cn = defaultdict(set)
        for key, k in self.table.items():
            for s2 in steps(key, self.scheme):
                k2 = self.table.get(s2)
                if k2 is not None and k2 != k:
                    cn[k].add(k2)
        return {k: sorted(v) for k, v in cn.items()}

    def nv(self, c):
        g = self.table[c]
        out = set()
        for s2 in steps(c, self.scheme):
            k2 = self.table.get(s2)
            if k2 is not None and k2 != g:
                out.add(k2)
        return out

    # ---------------------------------------------------------------- text
    def body(self, k):
        parts = []
        if self.scheme == "xed":
            for fs in self.sets[k]:
                parts.append(f"{fs[0]} alone" if len(fs) == 1 else label_list(fs))
            s = "the labels are " + ", or ".join(parts) + "."
        else:
            t, ts = TARGET[self.scheme]
            for p0, oth in self.sets[k]:
                parts.append(f"the named {t} is {p0}; the other {ts} are {label_list(oth)}.")
            s = " Or: ".join(parts)
        if self.marks[k] and self.form != "short":
            s += " " + lex.MARK_FMT.format(mark=self.mark)
        return s

    def head(self, k, render):
        if render == "masked":
            return self.ids[k]
        nm = self.swapped[k] if render == "swapped" else self.names[k]
        return f"{self.ids[k]} {nm}"

    def reading_rules(self, render):
        f = self.fill
        R = [lex.SEM["SEM-01"].format(**f), lex.SEM["SEM-45"].format(dimension=self.cb["dimension"])]
        if self.scheme in TARGET:
            R.append(lex.SEM["SEM-45-MAMS"].format(**f))
        R.append(lex.SEM["SEM-46"])
        R.append(lex.SEM["SEM-10"])
        R.append(lex.SEM["SEM-38"].format(**f))
        if self.form != "short":
            if render == "masked":
                R.append(lex.SEM["SEM-36"])
            else:
                R.append(lex.SEM["SEM-35"])
        if any(self.marks):
            R.append(lex.SEM["SEM-52"].format(marks=lex.MARK_FMT.format(mark=self.mark),
                                              actions=lex.MARK_ACTIONS[self.mark]))
        return R

    def card_ir(self, render="base", route=None):
        blocks = [{"type": "section", "heading": "Reading rules",
                   "blocks": [{"type": "items", "items": self.reading_rules(render)}]}]
        if self.form == "short":
            items = [self.names[k] + (" " + lex.MARK_FMT.format(mark=self.mark) if self.marks[k] else "")
                     for k in self.order]
            blocks.append({"type": "section", "heading": lex.CODE_LIST_HEADING,
                           "blocks": [{"type": "items", "items": items}]})
            return {"blocks": blocks}
        entries = []
        for k in self.order:
            if route and k in route["offered"]:
                other = route["other"].get(k)
                pre = f"({other}) " if other else ""
                entries.append({"name": route["offered"][k], "text": pre + self.body(k)})
            else:
                entries.append({"name": self.head(k, render), "text": self.body(k)})
        blocks.append({"type": "section", "heading": lex.CODE_LIST_HEADING,
                       "blocks": [{"type": "defs", "variant": self.dv, "entries": entries}]})
        return {"blocks": blocks}

    def swap_copy(self, k1, k2):
        """defs_swap twin card: the definitions (label sets) of k1 and k2 change places; IDs, names, marks stay."""
        import copy
        c2 = copy.copy(self)
        c2.sets = list(self.sets)
        c2.sets[k1], c2.sets[k2] = self.sets[k2], self.sets[k1]
        c2.build_table()
        return c2


# ------------------------------------------------------------------------------------------------ units pool
class Pool:
    """Unclaimed units per codebook, indexed by gold code; one claim per normalized text across all F11 S7 cards."""
    claimed = set()

    def __init__(self, card, arm="train"):
        self.card = card
        recs, _ = records(card.scheme, arm)
        self.by_code = defaultdict(list)
        for rec in recs:
            for ti in units(rec, card.scheme):
                c = combo(rec, ti, card.scheme)
                k = card.table.get(c)
                if k is not None:
                    self.by_code[k].append((rec, ti))
        r = rng("s7pool", card.card_id)
        for v in self.by_code.values():
            r.shuffle(v)

    def take(self, k, pred=None):
        lst = self.by_code.get(k, [])
        for j, (rec, ti) in enumerate(lst):
            if rec["norm_sha256"] in Pool.claimed:
                continue
            if pred and not pred(rec, ti):
                continue
            Pool.claimed.add(rec["norm_sha256"])
            lst.pop(j)
            return rec, ti
        return None


# ------------------------------------------------------------------------------------------------ rows
class S7Gen:
    def __init__(self, card, setname, *, n_target=60, held_out=False, arm="train"):
        self.card = card
        self.setname = setname
        self.arm = arm
        self.r = rng("s7rows", setname, card.card_id)
        self.styles = prose_styles(held_out)
        self.r.shuffle(self.styles)
        self.styles = self.styles[:12]
        ws = f11_wordings()
        self.r.shuffle(ws)
        self.w_yn = [w for w in ws if set(w["forms"]) & {"any", "yn"}][:6]
        self.w_ch = [w for w in ws if set(w["forms"]) & {"any", "choice"}][:6]
        self.pool = Pool(card, arm)
        self.code_count = Counter()
        self.n_target = n_target
        self.cap = math.ceil(n_target / len(card.ids)) + 1
        self.yes_rate = self.r.uniform(0.2, 0.8)
        from rows import YES_RATE
        self.yes_rate = YES_RATE.get(card.card_id, self.yes_rate)   # repair r1 (build.assign_rates, G7)
        self.acc_yn = self.acc_yes = 0
        self.ids = card.ids

    def want_yes(self):
        """Repair r1 (G7): low-discrepancy yes draw over the card's accepted base yes/no rows: P(yes) = clip(rate *
        (n + 1) - n_yes, 0, 1), so the card's realized yes share stays within one row of its rate (one draw per row)."""
        p = min(1.0, max(0.0, self.yes_rate * (self.acc_yn + 1) - self.acc_yes))
        return self.r.random() < p

    def draw(self, need_nb=1):
        c, r = self.card, self.r
        ks = [k for k in range(len(c.ids)) if self.code_count[k] < self.cap and self.pool.by_code.get(k)]
        r.shuffle(ks)
        for k in ks:
            got = self.pool.take(k, pred=lambda rec, ti: len(c.nv(combo(rec, ti, c.scheme))) >= need_nb)
            if got:
                return got
        raise RowFail("no unit")

    def yn_spec(self):
        c, r = self.card, self.r
        rec, ti = self.draw(1)
        cb = combo(rec, ti, c.scheme)
        g = c.table[cb]
        if self.want_yes():
            K = g
        else:
            K = r.choice(sorted(c.nv(cb)))
        return {"form": "yn", "rec": rec, "ti": ti, "gold_code": g, "K": K, "n_frame": 0, "edge": []}

    def label_form(self):
        c, r = self.card, self.r
        if c.form == "short":
            return "name"
        x = r.random()
        if x < 0.12:
            return "masked"
        if x < 0.17 and c.swapped:
            return "swapped"
        return "code" if r.random() < 0.5 else "name"

    def choice_spec(self):
        c, r = self.card, self.r
        rec, ti = self.draw(2)
        cb = combo(rec, ti, c.scheme)
        g = c.table[cb]
        nall = c.nv(cb)
        n = len(c.ids)
        full = r.random() < 0.5 or n < 11
        none_shown = none_gold = False
        if full:
            shown = list(range(n))
        else:
            m = r.randint(8, min(15, n - 3))
            none_shown = r.random() < 0.30
            if none_shown:
                none_gold = r.random() < 1.0 / (m + 1)
            nb = sorted(nall)
            r.shuffle(nb)
            shown = [] if none_gold else [g]
            shown += nb[:r.randint(2, 3)]
            cn = c.code_neighbours()
            outside = [k for k in range(n) if k != g and k not in nall]
            if outside:
                D = r.choice(outside)
                shown.append(D)
                dn = [k for k in cn.get(D, []) if k != g and k not in shown]
                r.shuffle(dn)
                shown += dn[:r.randint(2, 3)]
            shown = [k for k in dict.fromkeys(shown) if not (none_gold and k == g)]
            rest = [k for k in range(n) if k not in shown and k != g]
            r.shuffle(rest)
            while len(shown) < m and rest:
                shown.append(rest.pop())
            shown = shown[:m]
            if not none_gold and g not in shown:
                shown[0] = g
            if not any(k in nall for k in shown):
                raise RowFail("no close distractor shown")
        r.shuffle(shown)
        return {"form": "choice", "rec": rec, "ti": ti, "gold_code": g, "shown": shown, "none_shown": none_shown,
                "none_gold": none_gold, "full": full, "label": self.label_form(), "edge": []}

    # ---------------------------------------------------------------- emit
    def doc(self, spec):
        r = self.r
        w = self.card.wrap
        lead = spec.setdefault("lead", r.choice(LEADS).format(org=w.get("org") or "review desk",
                                                               decider=w.get("decider") or "case"))
        blocks = [{"type": "para", "text": lead + ":"}, {"type": "para", "text": '"' + spec["rec"]["text"] + '"'}]
        if spec.get("attack"):
            blocks.append({"type": "para", "text": "Submitter note: " + spec["attack"]})
        return {"title": None, "meta": [], "blocks": blocks}

    def emit(self, spec, *, rid, gid, cid, role="base", twin_of=None, twin_kind=None, style=None, wording=None,
             card=None):
        c = card or self.card
        r = self.r
        f = spec["form"]
        fill = c.fill
        if c.scheme in TARGET:
            fill = dict(fill, T=target_text(spec["rec"], spec["ti"], c.scheme))
        note_parts, render, route, options = [], "base", None, None
        edge = list(spec.get("edge", []))
        mams = "_mams" if c.scheme in TARGET else ""
        cb = combo(spec["rec"], spec["ti"], c.scheme)
        gold_code = c.table[cb]
        spec["gold_code_card"] = gold_code
        wording = wording or spec.get("wording")
        if f == "yn":
            qtype = "noul"
            wording = wording or r.choice(self.w_yn)
            nf = spec["n_frame"]
            if c.form == "short":
                Kt = c.names[spec["K"]]
            else:
                Kt = c.ids[spec["K"]] if spec.setdefault("ylabel", r.choice(("code", "name"))) == "code" \
                    else c.names[spec["K"]]
            qk = ("s7_yn", "s7_yn_neg", "s7_yn_dneg")[nf] + mams
            question = lex.Q[qk].format(K=Kt, **fill)
            note_parts.append(lex.ROW_SEM["SEM-39"].format(K=Kt, **fill))
            hit = spec["K"] == gold_code
            gold = 1 if (hit != (nf == 1)) else 0
            spec["polar_bad"] = bool(c.marks[spec["K"]]) != (nf == 1)
        else:
            qtype = "choice"
            wording = wording or r.choice(self.w_ch)
            lf = spec["label"]
            render = {"masked": "masked", "swapped": "swapped"}.get(lf, "base")
            edge += [lf] if lf in ("masked", "swapped") else []
            options = [c.code_label(k, lf) for k in spec["shown"]]
            if spec["none_shown"]:
                options.insert(spec.setdefault("none_pos", r.randrange(len(options) + 1)), lex.NONE_CODES)
            none_gold = gold_code not in spec["shown"]
            if none_gold and not spec["none_shown"]:
                raise RowFail("gold not shown and no none option")
            gold = lex.NONE_CODES if none_gold else c.code_label(gold_code, lf)
            if none_gold:
                edge.append("none_gold")
            question = lex.Q["s7_choice" + mams].format(**fill)
            if c.form == "oneline":
                other = {k: None if lf == "masked" else (c.names[k] if lf in ("code",) else c.ids[k])
                         for k in spec["shown"]}
                route = {"offered": {k: c.code_label(k, lf) for k in spec["shown"]}, "other": other}
                note_parts.append(lex.ROW_SEM["SEM-53"])
                if lf != "masked":
                    note_parts.append(lex.ROW_SEM["SEM-53-NAME" if lf == "code" else "SEM-53-ID"])
                if not spec["full"]:
                    note_parts.append(lex.ROW_SEM["SEM-53-SUB"].format(heading=lex.CODE_LIST_HEADING))
            if not spec["full"]:
                note_parts.append(lex.ROW_SEM["SEM-34-NONE"].format(none=lex.NONE_CODES, **fill)
                                  if spec["none_shown"] else lex.ROW_SEM["SEM-34"])
        if c.form == "short":
            edge.append("short_card")
        st = style or spec.get("style") or r.choice(self.styles)
        spec["style"], spec["wording"] = st, wording
        doc = self.doc(spec)
        cir = c.card_ir(render, route)
        note = " ".join(note_parts) or None
        fields = fcard.render_row_text(st, doc=doc, question=question, qtype=qtype, card=cir, options=options,
                                       wording=wording["text"], note=note)
        row = {"id": rid, "group_id": gid, "call_id": cid, "source": "c_f11", "state": fields["state"],
               "qtype": qtype, "instructions": fields["instructions"], "options": options if qtype == "choice" else None,
               "gold": gold, "role": role, "card": fields["card"]}
        res = fcard.loader_check(row, must_show=fcard.must_show(cir, question=question, wording=wording["text"],
                                                                note=note))
        if not res["ok"]:
            raise RowFail("loader_check: " + "; ".join(res["problems"][:2]))
        rec = spec["rec"]
        struct = {"cb": c.cb["id"], "sets": canon([[list(map(str, x)) for x in s] for s in c.sets]),
                  "key": canon(sorted([n, list(map(str, cp["cond"])), list(map(str, cp["a"])), list(map(str, cp["b"]))]
                                      for n, cp in c.couplets.items())) if c.form == "key" else None,
                  "text": rec["norm_sha256"], "ti": spec["ti"], "form": f, "K": spec.get("K"),
                  "n_frame": spec.get("n_frame"), "shown": spec.get("shown"), "label": spec.get("label"),
                  "none": [spec.get("none_shown")], "attack": bool(spec.get("attack")), "render": render}
        depth = s7_depth(c, cb, gold_code)
        row["meta"] = {"family": FAMILY, "spec_id": SPEC_SHA256, "card_id": c.card_id, "domain_pack": c.pack_id,
                       "sampler": c.sampler, "gen_version": GEN_VERSION, "git_sha": _GIT,
                       "seed": int(sha256_text(canon(struct) + self.setname)[:12], 16),
                       "structure_hash": sha256_text(canon(struct))[:32], "difficulty_bin": None, "crowd_pg": None,
                       "depth": depth, "deep": False, "format_style": st["id"], "wording_id": wording["id"],
                       "defs_style": {"short": "short", "key": "decision_list"}.get(c.form, "one_line"),
                       "twin_of": twin_of,
                       "twin_kind": twin_kind,
                       "text_source": {"dataset": DATASET[c.scheme], "record_id": str(rec["record_id"]),
                                       "split": "dev" if (c.scheme == "xed" and self.arm == "s5") else "train"},
                       "licence": LICENCE[c.scheme], "edge": sorted(set(edge)),
                       "subtype": "codebook" if c.form == "key" else None,
                       "persona_seed": c.persona_seed}
        row["_spec"] = spec
        row["_card"] = c
        return row


# ------------------------------------------------------------------------------------------------ twins
def clone(spec):
    sp = dict(spec)
    sp["edge"] = list(spec.get("edge", []))
    return sp


def attack_twin(g, base, rid):
    import twins as TW
    sp = clone(base["_spec"])
    sp["attack"] = TW.attack_text(g, base)
    row = g.emit(sp, rid=rid, gid=base["group_id"], cid=base["call_id"], role="twin", twin_of=base["id"],
                 twin_kind="attack", style=base["_spec"]["style"], wording=base["_spec"]["wording"],
                 card=base["_card"])
    if row["gold"] != base["gold"] or row["options"] != base["options"]:
        raise RowFail("attack twin changed the label")
    return row, {"a": base["id"], "b": row["id"], "type": "inv"}


def neg_unit(g, base, rid, gid, cid):
    out = []
    for nf, kind in ((1, "neg"), (2, "dneg")):
        sp = clone(base["_spec"])
        sp["n_frame"] = nf
        out.append(g.emit(sp, rid=f"{rid}-{kind}", gid=gid, cid=cid, role="twin", twin_of=base["id"], twin_kind=kind,
                          style=base["_spec"]["style"], wording=base["_spec"]["wording"], card=base["_card"]))
    return out, [{"a": base["id"], "b": out[0]["id"], "type": "complement"},
                 {"a": base["id"], "b": out[1]["id"], "type": "equiv"}]


def defs_swap_twin(g, base, rid, cid):
    """Gold's definition swapped with a shown code neighbour's; gold follows the definition (A48)."""
    c, r = g.card, g.r
    sp = clone(base["_spec"])
    if sp["form"] != "choice" or c.form == "short" or sp["gold_code"] not in sp["shown"]:
        raise RowFail("defs_swap needs a full-card choice row with gold shown")
    g0 = sp["gold_code"]
    cands = [k for k in c.code_neighbours().get(g0, []) if k in sp["shown"]]
    if not cands:
        raise RowFail("no shown code neighbour")
    k2 = r.choice(cands)
    c2 = c.swap_copy(g0, k2)
    row = g.emit(sp, rid=rid, gid=base["group_id"], cid=cid, role="twin", twin_of=base["id"], twin_kind="defs_swap",
                 style=base["_spec"]["style"], wording=base["_spec"]["wording"], card=c2)
    if row["gold"] == base["gold"]:
        raise RowFail("defs_swap did not move the label")
    return row


def focal_target_twin(g, base, rid, cid):
    """MAMS: the same sentence, another annotated target with a different polarity is named."""
    c, r = g.card, g.r
    if c.scheme not in TARGET:
        raise RowFail("focal_target on MAMS only")
    sp = clone(base["_spec"])
    rec = sp["rec"]
    p0 = combo(rec, sp["ti"], c.scheme)[0]
    alts = [ti for ti in units(rec, c.scheme) if ti != sp["ti"] and combo(rec, ti, c.scheme)[0] != p0
            and combo(rec, ti, c.scheme) in c.table]
    if not alts:
        raise RowFail("no other target")
    sp["ti"] = r.choice(alts)
    cb2 = combo(rec, sp["ti"], c.scheme)
    g2 = c.table[cb2]
    sp["gold_code"] = g2
    if sp["form"] == "yn":
        if sp["K"] != g2 and sp["K"] not in c.nv(cb2):
            raise RowFail("asked code not in N(v) for the new target")
    elif sp["form"] == "choice":
        if g2 not in sp["shown"] and not sp["none_shown"]:
            raise RowFail("new gold not shown")
    row = g.emit(sp, rid=rid, gid=base["group_id"], cid=cid, role="twin", twin_of=base["id"],
                 twin_kind="focal_target", style=base["_spec"]["style"], wording=base["_spec"]["wording"],
                 card=base["_card"])
    if row["gold"] == base["gold"]:
        raise RowFail("focal_target did not move the label")
    return row


# ------------------------------------------------------------------------------------------------ cards
SHORT_CB = ("cb.F11.xed.x03", "cb.F11.xed.x04", "cb.F11.xed.x05", "cb.F11.mams_atsa.t01")


def make_cards(wraps):
    out = []
    for i, cb in enumerate(codebooks()):
        short = cb["id"] in SHORT_CB
        out.append(S7Card(cb, wraps[i], i, short=short))
    return out


# ------------------------------------------------------------------------------------------------ S5 codebook arm
def join_or(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " or " + xs[-1]


def kcond_holds(cond, cb, scheme):
    """Key condition on an annotation combination. kinds: 'any' / 'all' on the label set (XED) or on the other
    targets' polarities (MAMS); 'is' on the named target's polarity (MAMS; one value or one of several)."""
    kind, L = cond
    if scheme == "xed":
        S = cb
    else:
        if kind == "is":
            return cb[0] in L
        S = cb[1]
    return any(x in S for x in L) if kind == "any" else all(x in S for x in L)


def kcands(scheme):
    out = []
    labs = EMOTIONS if scheme == "xed" else POLS
    if scheme != "xed":
        out += [("is", (p,)) for p in POLS]
        out += [("is", (POLS[i], POLS[j])) for i in range(3) for j in range(i + 1, 3)]
    out += [("any", (e,)) for e in labs]
    for i in range(len(labs)):
        for j in range(i + 1, len(labs)):
            out += [("any", (labs[i], labs[j])), ("all", (labs[i], labs[j]))]
    return out


def build_key(table, scheme, r):
    """Dichotomous key over the codebook's covered combinations (greedy Gini splits, BFS couplet numbers). Every
    covered combination reaches its own code (pure leaves), so the key walk equals the codebook table on them."""
    from collections import deque
    cands = kcands(scheme)

    def gini(xs):
        n = len(xs)
        cc = Counter(k for _, k in xs)
        return 1.0 - sum((v / n) ** 2 for v in cc.values())
    couplets, q, nxt = {}, deque([(1, sorted(table.items(), key=lambda x: str(x[0])))]), 2
    while q:
        n, items = q.popleft()
        best = None
        for cd in cands:
            A = [x for x in items if kcond_holds(cd, x[0], scheme)]
            if not A or len(A) == len(items):
                continue
            B = [x for x in items if not kcond_holds(cd, x[0], scheme)]
            sc = (len(A) * gini(A) + len(B) * gini(B)) / len(items) + 0.002 * (len(cd[1]) - 1) + r.random() * 1e-6
            if best is None or sc < best[0]:
                best = (sc, cd, A, B)
        if best is None:
            raise RowFail("key: combinations not separable")
        _, cd, A, B = best
        cp = {"cond": cd}
        for side, S in (("a", A), ("b", B)):
            ks = {k for _, k in S}
            if len(ks) == 1:
                cp[side] = ("k", ks.pop())
            else:
                cp[side] = ("n", nxt)
                q.append((nxt, S))
                nxt += 1
        couplets[n] = cp
    return couplets


class S7KeyCard(S7Card):
    """S5 codebook arm (G0 S5): an F11 codebook written as a dichotomous key, then the code legend."""

    def __init__(self, cb, wrap, idx, attempt=0):
        super().__init__(cb, wrap, 900 + idx, short=False, attempt=attempt)
        self.sampler = "S5"
        self.card_id = f"F11-S5-C{idx:02d}"
        self.form = "key"
        self.swapped = None
        self.couplets = build_key(self.table, self.scheme, rng("s5key", cb["id"], idx, attempt))
        # coverage (program check): walk == table on every covered combination; every code reached
        for comb, k in self.table.items():
            if self.walk(comb) != k:
                raise RowFail("key walk differs from the codebook")
        if set(self.table.values()) != set(range(len(self.ids))):
            raise RowFail("key: a code is never reached")

    def walk(self, comb):
        n = 1
        while True:
            cp = self.couplets[n]
            t = cp["a"] if kcond_holds(cp["cond"], comb, self.scheme) else cp["b"]
            if t[0] == "k":
                return t[1]
            n = t[1]

    def cond_text(self, cond):
        kind, L = cond
        if kind == "is":
            t = TARGET[self.scheme][0]
            return f"the named {t} is {L[0]}" if len(L) == 1 else f"the named {t} is one of {join_or(L)}"
        subj = "the labels" if self.scheme == "xed" else f"the labels of the other {TARGET[self.scheme][1]}"
        return f"{subj} include any of {join_or(L)}" if kind == "any" else f"{subj} include all of {label_list(L)}"

    def reading_rules(self, render):
        f = self.fill
        R = [lex.SEM["SEM-01"].format(**f), lex.SEM["SEM-45-KEY"].format(dimension=self.cb["dimension"])]
        if self.scheme in TARGET:
            R.append(lex.SEM["SEM-45-MAMS"].format(**f))
        R.append(lex.SEM["SEM-46-KEY"])
        R.append(lex.SEM["SEM-18-KEY"])
        if any(cp["cond"][0] == "is" for cp in self.couplets.values()):
            R.append(lex.SEM["SEM-19"])
        R.append(lex.SEM["SEM-10"])
        R.append(lex.SEM["SEM-38"].format(**f))
        R.append(lex.SEM["SEM-36"] if render == "masked" else lex.SEM["SEM-35"])
        if any(self.marks):
            R.append(lex.SEM["SEM-52"].format(marks=lex.MARK_FMT.format(mark=self.mark),
                                              actions=lex.MARK_ACTIONS[self.mark]))
        return R

    def card_ir(self, render="base", route=None):
        blocks = [{"type": "section", "heading": "Reading rules",
                   "blocks": [{"type": "items", "items": self.reading_rules(render)}]}]
        lines = []
        for n in sorted(self.couplets):
            cp = self.couplets[n]
            ref = lambda x: (str(x[1]) if x[0] == "n" else self.ids[x[1]])  # noqa: E731
            lines.append(f"{n}a {self.cond_text(cp['cond'])} -> {ref(cp['a'])}")
            lines.append(f"{n}b otherwise -> {ref(cp['b'])}")
        bl = [{"type": "items", "items": lines}]
        if render != "masked":
            bl.append({"type": "items", "items": [f"{self.ids[k]}: {self.names[k]}" +
                                                  (" " + lex.MARK_FMT.format(mark=self.mark) if self.marks[k] else "")
                                                  for k in self.order]})
        elif any(self.marks):
            bl.append({"type": "items", "items": [f"Marked {lex.MARK_FMT.format(mark=self.mark)}: " +
                                                  ", ".join(self.ids[k] for k in self.order if self.marks[k]) + "."]})
        blocks.append({"type": "section", "heading": lex.CODE_LIST_HEADING, "blocks": bl})
        return {"blocks": blocks}


def make_key_cards(wraps, plan):
    """plan: [(codebook id, n_items)]; one held-out wrapper pack per card."""
    cbs = {c["id"]: c for c in codebooks()}
    out = []
    for i, (cbid, _) in enumerate(plan):
        for att in range(4):
            try:
                out.append(S7KeyCard(cbs[cbid], wraps[i], i, attempt=att))
                break
            except RowFail:
                continue
        else:
            raise RowFail(f"no key card for {cbid}")
    return out
