"""Rendering of one built row into the raw row format (2.4 / 6), the 1.5 invariance check (meta.edge, short and
no-card rows), the per-row G15 loader check and real-tokenizer length, and the twin units of 1.7."""
from __future__ import annotations

import copy
import html
import itertools
import json
import random

from f9alt import REWRITE, applicable, flag_of, rewrite
from f9ast import atoms, depth, structure_hash, subtype
from f9cards import card_ir, short_ir
from f9fmt import round_half_up, to_frac
from f9frames import solve
from f9lex import (CBD as CBD_TXT, CMP_T10, GEN_VERSION, LICENCE, NONE_OPT, SOURCE, SPEC_ID, id_key, negcount,
                   no_record_opt, uh)
from f9render import (DEFAULT_FMT, ans_text, json_record, log_text, question, table_text, yaml_records, header_label,
                      cell_text)
from f9rows import ATTACKS, CPICK, NEG_FORMS, SHORT_FRAMES, WORDINGS, Ctx, RowMaker, fm_for, sha
from f9samp import Retry, col_index
from f9solve_a import CBD, NO_RECORD, NONE, SPECIALS, TIE, Reject, Undefined
from fmt1 import card as fcard
from fmt1 import pool as fpool


def trainer_pin_ok():
    """True when lean/train_decoder.py is the A16-pinned trainer, so fmt1's loader_check can run check_rows. When the
    working copy is edited by another lane, check_rows is not run here and G15 reports it as blocked (never faked)."""
    try:
        fcard._td()
        return True
    except fcard.FormatError:
        return False


CHECK_ROWS = trainer_pin_ok()
GIT_SHA = None


def git_sha():
    global GIT_SHA
    if GIT_SHA is None:
        import subprocess
        from f9lex import LEAN
        try:
            GIT_SHA = subprocess.check_output(["git", "-C", str(LEAN), "rev-parse", "HEAD"], text=True).strip()
        except Exception:
            GIT_SHA = "unknown"
    return GIT_SHA


# ------------------------------------------------------------------------------------------------ state
def render_state(card, st, container, fm, attack=None):
    s = card["sampler"]
    masked = fm.get("_masked")
    if s in ("S1", "S2"):
        t = st["tables"][0]
        return table_text(container, t["cols"], _attacked(t, attack), fm, masked)
    if s == "S3":
        sc = card["schema"]
        dim, fact = st["tables"]
        k1, k2 = container
        return (f"{sc['ent_pl'].capitalize()}:\n\n" + table_text(k1, dim["cols"], _attacked(dim, attack), fm,
                                                                   masked if masked and any(
                                                                       c["name"] == masked["col"] for c in dim["cols"])
                                                                   else None)
                + f"\n\n{sc['ev_pl'].capitalize()}:\n\n" +
                table_text(k2, fact["cols"], _attacked(fact, attack), fm,
                           masked if masked and any(c["name"] == masked["col"] for c in fact["cols"]) else None))
    if s == "S4":
        t = st["tables"][0]
        rows = _attacked(t, attack)
        names = [c["name"] for c in t["cols"]]
        recs = [dict(zip(names, r)) for r in rows]
        if container == "json_pretty":
            body = "[\n" + ",\n".join(json_record(r, t["cols"], fm, True) for r in recs) + "\n]"
            return "```json\n" + body + "\n```"
        if container == "json_compact":
            return "```json\n[" + ", ".join(json_record(r, t["cols"], fm, False) for r in recs) + "]\n```"
        if container == "jsonl":
            return "```jsonl\n" + "\n".join(json_record(r, t["cols"], fm, False) for r in recs) + "\n```"
        if container == "yaml":
            return "```yaml\n" + yaml_records(recs, t["cols"], fm) + "\n```"
        raise KeyError(container)
    if s == "S6":
        t = st["tables"][0]
        syntax, fence = container
        sc = card["schema"]
        return log_text(syntax, _attacked(t, attack), t["cols"], fm, sc["numf"], sc["code"]["name"], fence)
    if s == "S5":
        return pivot_text(card, st["pivot"], fm)
    raise KeyError(s)


def _attacked(t, attack):
    if not attack or attack["role"] != t["role"]:
        return t["rows"]
    rows = [list(r) for r in t["rows"]]
    rows[attack["i"]][attack["j"]] = attack["text"]
    return rows


def pivot_text(card, pv, fm):
    sc = card["schema"]
    marks = {tuple(m) for m in pv["marks"]}
    hdr = [sc["ent_sg"]] + pv["periods"]
    out = ["| " + " | ".join(hdr) + " |", "| " + " | ".join("---" for _ in hdr) + " |"]
    total = [0] * len(pv["periods"])
    for g in pv["groups"]:
        sub = [0] * len(pv["periods"])
        for e in g:
            cells = []
            for j, v in enumerate(pv["cells"][e]):
                if (e, j) in marks:
                    cells.append(f"{v}*")
                else:
                    cells.append(str(v))
                    sub[j] += v
                    total[j] += v
            out.append("| " + " | ".join([e] + cells) + " |")
        out.append("| " + " | ".join(["Subtotal"] + [str(x) for x in sub]) + " |")
    out.append("| " + " | ".join(["Total"] + [str(x) for x in total]) + " |")
    unit = sc["measure"]
    return f"{sc['measure']['name']} by {sc['ent_sg']} and week, in {unit['unit']}:\n\n" + "\n".join(out)


# ------------------------------------------------------------------------------------------------ card flag set
def used_flags(card):
    u = set()
    menu = card["menu"]
    s = card["sampler"]
    u.add("T10")
    if card.get("use_between") and s in ("S1", "S2", "S4"):
        u.add("T11")
    if card.get("use_in2"):
        u |= {"T12"}
        if card.get("use_not"):
            u.add("T13")
    tf = set(card["time_forms"])
    if s in ("S1", "S2", "S3", "S4"):
        if tf & {"from_to", "before", "after", "on_or_before", "on_or_after", "in_month"}:
            u.add("T15")
        if "rolling" in tf:
            u.add("T16")
    if s == "S6":
        if tf & {"on", "from_to"}:
            u.add("T15")
        if "half_open" in tf:
            u.add("T17")
    if {"Y_MEAN", "V_MEAN", "Y_COMPARE"} & set(menu):
        u.add("T22")
    u.add("T23")
    if {"R_EXT", "E_GMAX", "C_COMP", "R_TOP"} & set(menu) or any(f in menu for f in ("R_COND", "E_COND", "C_REQ")):
        u.add("T24")
    if s != "S5":
        u.add("T26")
    if {"Y_COUNT", "V_COUNT", "V_CDIST", "V_TCOUNT", "Y_GCOUNT", "V_GCOUNT", "V_LCOUNT", "Y_LCOUNT",
        "V_COLC"} & set(menu):
        u.add("T27")
    for t in (card.get("terms") or {}).values():
        if t.get("overrides") or t.get("usual"):
            u.add("T30")
    if card["schema"].get("bools"):
        u.add("T34")
    if "Y_COMPARE" in menu:
        u.add("T35")
    if any(v == "set" for v in menu.values()):
        u.add("T36")
    if card["sem"]["world"] == "T2" or card["sem"].get("missing") == "T5":
        u.add("T37")
    if card.get("allow_none", True):
        u.add("T37b")
    if s == "S4" and {"Y_ANY", "Y_EVERY"} & set(menu):
        u.add("T14")
    return u


# ------------------------------------------------------------------------------------------------ SEM as stated
def sem_stated(card, mode, row_flags=None):
    """The flags a row's card text states, with their values (the structure_hash SEM part; both sides build it)."""
    if mode == "none":
        return {}
    sem = card["sem"]
    out = {"world": sem["world"]}
    if sem.get("missing") and mode == "full":
        out["missing"] = sem["missing"]
        out["null"] = "null" if card["sampler"] == "S4" else (sem["null_tok"] if mode == "full" else "unknown")
    if mode == "short":
        out["t10"] = sorted(row_flags or [])
        return out
    out["t21"] = [sem["nf"], sem["df"], sem.get("tf"), sem.get("zone") if card["sampler"] == "S6" else None,
                  sem.get("csv") if "csv" in card["containers"] else None]
    out["tie"] = ([sem["tie_variant"]] + ([list(x) for x in sem.get("tie_chain") or []]
                                         if sem["tie_variant"] == "key" else [])) if "T24" in card["used"] else None
    out["round_dp"] = sem["round_dp"] if "T22" in card["used"] else None
    out["bool"] = sem["bool"] if "T34" in card["used"] else None
    out["merged"] = sem.get("merged") if card["sampler"] == "S6" else None
    out["terms"] = sorted(card.get("terms") or {})
    out["masked"] = sorted((card.get("masked") or {}).get("codes", {}).items()) if card.get("masked") else None
    return out


# ------------------------------------------------------------------------------------------------ G15 / tokens
_TOK = None


def tokenizer():
    global _TOK
    if _TOK is None:
        import os
        os.environ.setdefault("HF_HUB_OFFLINE", "1")
        os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
        from transformers import AutoTokenizer
        _TOK = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
    return _TOK


def served_tokens(row):
    """Real-tokenizer length of the served prompt: chat template, cygnet system, schema_branch_mark user message
    (instructions and options printed twice, 1.8)."""
    dio = fcard._dio()
    with fcard._serving(dio, len(row.get("options") or [1, 2])):
        user = dio.user_msg(row, None)
        text = dio.render_chat(tokenizer(), dio.CYGNET_SYSTEM, user)
    return len(tokenizer()(text)["input_ids"])


# ------------------------------------------------------------------------------------------------ emitter
class Emitter(RowMaker):
    def __init__(self, card, ctx, rng, mode, g3=None):
        super().__init__(card, ctx, rng, mode)
        self.g3 = g3
        self.cont_count = {}
        self.style_count = {}
        self.word_count = {}
        self.word_acc = {}  # repair r2 (G11 >= 5 wordings per card): wordings of accepted rows (CardBuilder.commit)

    # -------------------------------------------------------------------------------------------- picks
    def pick_container(self, exclude=None):
        card, rng = self.card, self.rng
        s = card["sampler"]
        opts = list(card["containers"])
        if exclude is not None:
            opts = [o for o in opts if o != exclude] or opts
        if s == "S3":
            k1 = min(opts, key=lambda o: self.cont_count.get(o, 0) + rng.random())
            k2 = k1 if rng.random() < 0.6 else rng.choice([o for o in opts if o != k1] or [k1])
            c = (k1, k2)
            if exclude is not None and c == exclude:
                c = (k2, k1) if k1 != k2 else (rng.choice(opts), k1)
            self.cont_count[k1] = self.cont_count.get(k1, 0) + 1
            return c
        if s == "S6":
            syn = min(card["syntaxes"], key=lambda o: self.cont_count.get(o, 0) + rng.random())
            if exclude is not None and syn == exclude[0]:
                syn = rng.choice([x for x in card["syntaxes"] if x != syn])
            self.cont_count[syn] = self.cont_count.get(syn, 0) + 1
            return (syn, "fence" if rng.random() < 0.7 else "indent")
        c = min(opts, key=lambda o: self.cont_count.get(o, 0) + rng.random())
        self.cont_count[c] = self.cont_count.get(c, 0) + 1
        return c

    def pick_style(self):
        sid = min(self.card["styles"], key=lambda o: self.style_count.get(o, 0) + self.rng.random())
        self.style_count[sid] = self.style_count.get(sid, 0) + 1
        return sid

    def pick_wording(self, form):
        ok = [w for w in self.card["wordings"] if WORDINGS[w]["forms"][0] in ("any", "yn" if form == "yn" else
                                                                             "choice")]
        # repair r2 (G11): least used among the card's ACCEPTED rows first (r1c counted every draw, so failed choice
        # draws used up the shared wordings and light cards' yes/no rows cycled over their two yes/no-only wordings);
        # draws break ties, so a card's first rows take distinct wordings before any repeats
        # (r2c: a failed draw adds 1/4, so a wording whose rows keep failing a balance cell yields after 4 draws; at 0
        # a dev card spent 331 draws on one wording)
        def key(o):
            a = self.word_acc.get(o, 0)
            return a + 0.25 * max(0, self.word_count.get(o, 0) - a) + 0.01 * self.rng.random()
        wid = min(ok, key=key)
        self.word_count[wid] = self.word_count.get(wid, 0) + 1
        return wid

    # -------------------------------------------------------------------------------------------- edge / invariance
    def live_flags(self, res, alts=None):
        card = self.card
        q, st, gold = res["q"], res["struct"], res["gold"]
        form = res["form"]
        fm = fm_for(card, "full")
        out = set()
        shown = res.get("shown")
        for alt in alts or applicable(q, card, form if form != "record" else "record"):
            try:
                a = solve(card, st, q, shown=shown, alt=alt)
            except (Undefined, Reject, KeyError, ZeroDivisionError):
                continue
            if self._key(res, a, alt) != self._key(res, gold, None):
                f = self._flag(q, alt)
                if f:
                    out.add(f)
        return sorted(out)

    def _key(self, res, a, alt):
        if isinstance(a, (bool, frozenset)) or a in SPECIALS:
            return repr(sorted(a)) if isinstance(a, frozenset) else repr(a)
        if res["form"] == "value":
            return ans_text(self.card, res["frame"], res["q"], a, fm_for(self.card, "full"),
                            alt if alt and alt[0] == "E23" else None)
        return repr(a)

    def _flag(self, q, alt):
        tag = alt[0]
        if tag in ("E2", "E3"):
            if alt[1] in ("thr", "cmp", "pcmp"):
                return "T35" if alt[1] == "cmp" else "T10"
            from f9alt import _base
            b = _base(q)
            a = atoms(b[alt[1]])[alt[2]]
            if a["k"] == "win":
                f = a.get("_form")
                return "T17" if f == "half_open" else ("T16" if f == "rolling" else "T15")
            if a["k"] == "between":
                return "T11"
            if a["k"] == "line":
                return "T33"
            return "T10"
        return flag_of(alt)

    def invariant(self, res, mode, stated):
        """1.5 short / no-card: no combination of unstated alternatives may change the gold."""
        card = self.card
        q, st = res["q"], res["struct"]
        alts = applicable(q, card, res["form"])
        un = []
        for a in alts:
            f = self._flag(q, a)
            if mode == "short" and f in stated:
                continue
            un.append(a)
        rew = [a for a in un if a[0] in REWRITE]
        modes = [a for a in un if a[0] not in REWRITE]
        gk = self._key(res, res["gold"], None)
        combos = []
        for r in range(0, min(3, len(rew)) + 1):
            combos += list(itertools.combinations(rew, r))
        if len(combos) * (len(modes) + 1) > 4096:
            return False
        for cb in combos:
            q2 = q
            try:
                for a in cb:
                    q2 = rewrite(q2, a)
            except (IndexError, KeyError, TypeError):
                continue  # a combination that removes the atom another rewrite addresses is not a reading
            for m in [None] + modes:
                if not cb and m is None:
                    continue
                try:
                    a = solve(card, st, q2, shown=res.get("shown"), alt=m)
                except (Undefined, Reject, KeyError, ZeroDivisionError):
                    return False
                if self._key(res, a, m) != gk:
                    return False
        return True

    # -------------------------------------------------------------------------------------------- render
    def render(self, res, mode, container, style, wid, attack=None):
        card = self.card
        fm = fm_for(card, mode)
        if mode == "full" and card["sampler"] == "S4":
            fm["_masked"] = card.get("masked")
        q = res["q"]
        frame = res["frame"]
        qtext = question(card, frame, q, fm)
        st = fpool.dev_style(style) if card.get("held_out") else fpool.training_style(style)
        wtext = WORDINGS[wid]["text"]
        if mode == "full":
            ir = card["ir"]
        elif mode == "short":
            ir = short_ir(card, res["short_text"])
        else:
            ir = None
        state = render_state(card, res["struct"], container, fm, attack)
        if res["form"] == "yn":
            ctext = fcard.render_card(ir, st) if ir else None
            instr = fcard.render_instructions(st, question=qtext, wording=wtext)
            fields = {"state": state, "qtype": "noul", "instructions": instr, "options": None,
                      "gold": 1 if res["gold"] else 0, "card": ctext}
        else:
            texts = [o[1] for o in res["options"]]
            moved, task = None, None
            if ir:
                entries, rest, tk = fcard._split_choice_card(ir, st, texts)
                if entries:
                    raise Retry("option definition lines on an F9 choice row")
                moved = fcard.render_card(rest, st) if (rest["blocks"] or rest.get("title")) else None
                task = fcard.text_value(tk["text"]) if tk else None
            instr = fcard.render_instructions(st, question=qtext, wording=wtext, card_text=moved, task=task)
            fields = {"state": state, "qtype": "choice", "instructions": instr, "options": texts,
                      "gold": res["gold_text"], "card": None}
        ms = fcard.must_show(ir, question=qtext, wording=wtext)
        return fields, ms, qtext

    # -------------------------------------------------------------------------------------------- finish
    def finish(self, res, mode="full", container=None, style=None, wid=None, attack=None, ids=None, twin=None):
        card = self.card
        container = container if container is not None else self.pick_container()
        style = style or self.pick_style()
        wid = wid or self.pick_wording(res["form"])
        fields, ms, qtext = self.render(res, mode, container, style, wid, attack)
        rid = ids["id"]
        row = {"id": rid, "group_id": ids["group_id"], "call_id": ids["call_id"], "source": SOURCE, **fields,
               "role": "attacked" if (attack or res.get("attacked")) else "own"}
        row = {k: row[k] for k in ("id", "group_id", "call_id", "source", "state", "qtype", "instructions",
                                   "options", "gold", "role", "card")}
        tok = served_tokens(row)
        long_bin = (card["sampler"] == "S4" and res["struct"].get("bin") == 2) or (
            card["sampler"] == "S6" and res["struct"].get("bin") == 2)
        # A22 (tmp/repair/INFEASIBLE_length.md): a choice row with 10+ options (spec 2.1 buckets 10-19 / 20-60) needs a
        # table that holds its ids, so it takes the 4,000 per-row cap (F9 1.8 hard cap; A16 <= 7,900) like the long bins
        bigk = (res.get("plan") or {}).get("bucket") in ("10-19", "20-60")
        # repair r1 (A22 "keep every share and bucket"): record and record-set picks planned at 5-9 options failed the
        # 2,000 cap on most S3 / S4 tables while their 10+ draws passed under 4,000, so the 5-9 quota fell short
        bigk = bigk or ((res.get("plan") or {}).get("bucket") == "5-9" and res.get("form") in ("record", "set"))
        if not getattr(self, "skip_tok", False) and (tok > 4000 or (tok >= 2000 and not (long_bin or bigk))):
            self.ctx.note("token_redraw")
            self.last_tok = tok
            raise Retry(f"tokens {tok}")
        lc = fcard.loader_check(row, must_show=ms, seed="f9-g15", check_rows=CHECK_ROWS)
        if not lc["ok"]:
            self.ctx.note("loader_fail")
            raise Retry("loader_check: " + "; ".join(lc["problems"][:2]))
        q = res["q"]
        nc = negcount.count(qtext)
        if res["form"] == "yn" and nc.k_all >= 5:
            raise Retry("k_all >= 5")
        stated = sem_stated(card, mode, res.get("short_flags"))
        tabs = self._hash_tables(res["struct"])
        sh = structure_hash(tabs, stated, q, extra={"shown": sorted(res.get("shown") or [], key=id_key)})
        edge = res.get("edge")
        if edge is None:
            edge = self.live_flags(res) if mode == "full" else []
            res["edge"] = edge
        terms = card.get("terms") or {}
        tie_dec = bool(edge and "T24" in edge)
        dval = depth(q if q["op"] != "not" else q["inner"], terms, tie_dec)
        meta = {"family": "F9", "spec_id": SPEC_ID, "card_id": card["card_id"], "domain_pack": card["pack_id"],
                "sampler": card["sampler"], "gen_version": GEN_VERSION, "git_sha": git_sha(),
                "seed": ids["seed"], "structure_hash": sh, "difficulty_bin": None, "crowd_pg": None,
                "depth": dval, "deep": dval >= 4,
                "format_style": style, "wording_id": wid,
                "defs_style": {"full": card["defs_style"], "short": "short", "none": "none"}[mode],
                "twin_of": twin["of"] if twin else None, "twin_kind": twin["kind"] if twin else None,
                "text_source": None, "licence": LICENCE, "edge": edge, "subtype": subtype(q)}
        if card.get("persona_seed"):
            meta["persona_seed"] = card["persona_seed"]
        row["meta"] = meta
        side = {"id": rid, "structure_hash": sh, "sem_stated": stated, "frame": res["frame"], "form": res["form"],
                "q": q, "mode": mode, "container": container, "k_syn": nc.k_syn, "k_all": nc.k_all,
                "options": [[o[1], o[2]] for o in res.get("options") or []], "plan": res.get("plan"),
                "set_id": ids["group_id"], "attack": bool(attack or res.get("attacked")), "bin": res["struct"].get("bin"),
                "polarity_bad": ("yes" if uh("f9-bad", card["pack_id"], res["frame"]) < 0.5 else "no")
                if res["form"] == "yn" else None,
                "masked": bool(card.get("masked")) and res["form"] != "yn" and self._reads_masked(q),
                "swapped": bool(card.get("swap")) and res["form"] != "yn" and any(
                    "usual_meaning" in str(t) for t in edge + ["T30"] if False) or (
                    bool(card.get("swap")) and res["form"] != "yn" and self._swap_live(res)),
                "inverted": res["frame"] == "R_INV", "fewshot_card": bool(card.get("fewshot")),
                "short_flags": res.get("short_flags"), "placement": q.get("_pl") if isinstance(q, dict) else None,
                "decile": self._decile(res), "n_examples": self.n_examples(mode), "qtext": qtext}
        side["real_tokens"] = tok
        if self.g3 is not None:
            ok, why = self.g3(row, side, card)
            if not ok:
                self.ctx.note("g3_fail:" + why)
                raise Retry("G3: " + why)
        return row, side

    def n_examples(self, mode):
        if mode != "full":
            return 0
        c = self.card
        return sum(len(v) for v in (c.get("examples") or {}).values()) + len(c.get("fewshot_block") or [])

    def _swap_live(self, res):
        try:
            a = solve(self.card, res["struct"], res["q"], shown=res.get("shown"), alt=("E26", "usual_meaning"))
        except (Undefined, Reject, KeyError):
            return False
        return self._key(res, a, None) != self._key(res, res["gold"], None)

    def _reads_masked(self, q):
        m = self.card.get("masked")
        if not m:
            return False
        from f9solve_a import SolverA
        return m["col"] in json.dumps(q)

    def _decile(self, res):
        g = res["gold"]
        st = res["struct"]
        if not st.get("tables"):
            return None
        t = st["tables"][0]
        if t["role"] == "log":
            # repair r1 (S6 balance, 3.5: "the decisive event's line position"): an S6 component pick is decided by
            # the counts of all its lines, so it has no single decisive line; the component's first line (used
            # before) is not an event that decides the gold and sits early for any frequent component
            return None
        if isinstance(g, str) and g not in SPECIALS:
            ids = [r[0] for r in t["rows"]]
            if g in ids:
                return int(10 * ids.index(g) / max(1, len(ids)))
        return None

    def _hash_tables(self, st):
        out = []
        if st.get("pivot") is not None:
            pv = st["pivot"]
            marks = {tuple(m) for m in pv["marks"]}
            rows = [[e, p, Fraction_(pv["cells"][e][j]), (e, j) in marks] for e in pv["entities"]
                    for j, p in enumerate(pv["periods"])]
            return [{"role": "pivot", "cols": [{"name": "entity", "type": "id"}, {"name": "period", "type": "cat"},
                                               {"name": "value", "type": "num", "dp": 0},
                                               {"name": "marked", "type": "bool"}], "rows": rows}]
        for t in st["tables"]:
            cols = [hash_col(c) for c in t["cols"]]
            out.append({"role": t["role"], "cols": cols, "rows": [[hash_val(v, c) for v, c in zip(r, t["cols"])]
                                                                   for r in t["rows"]]})
        return out


def Fraction_(v):
    from fractions import Fraction
    return Fraction(v)


def hash_col(c):
    t = c["type"]
    if t == "text":
        t = "cat"
    if t == "list":
        return {"name": c["name"], "type": "list"}
    return {"name": c["name"], "type": t, "dp": c.get("dp"), "unit": c.get("unit"),
            "group": c["name"].split(".", 1)[0] if "." in c["name"] else "top"}


def hash_val(v, c):
    if c["type"] == "list" and v is not None:
        return [[hash_val(x, sc) for x, sc in zip(s, c["sub"])] for s in v]
    if c["type"] == "num" and v is not None:
        return to_frac(v)
    return v
