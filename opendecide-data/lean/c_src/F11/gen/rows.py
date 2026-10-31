"""F11 row builder for program cards (S1-S4, S6; S5 program arm): items, questions, display, layout, meta.

Every row is laid out by fmt1 card.render_row_text (qtype noul / choice; choice_card 'move') and checked with fmt1
card.loader_check (G15 per-row part) before it is kept (A16.1 (g); F11-R5-A1).
"""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict

import lex
import items as I
from common import (FAMILY, GEN_VERSION, LICENCE_PROGRAM, SPEC_SHA256, canon, rng, sha256_text, toks, git_sha)
from fmt1 import card as fcard, pool
from tax import neighbours_of_cell, PRES, ABS, CardInvalid

PROSE_CONTAINERS = ("prose", "memo", "bullet_sop", "email_thread")
_GIT = git_sha()


YES_RATE = {}   # card_id -> per-card yes rate (G0 9: per card uniform 20-80%), set by build.assign_rates (G7)


class RowFail(ValueError):
    pass


def prose_styles(held_out=False):
    out = []
    for s in pool.styles(held_out=held_out):
        if s["container"] not in PROSE_CONTAINERS:
            continue
        if s["container"] == "email_thread" and s["skin"] != "email.single":
            continue
        if not s["container"] in ("prose", "memo", "bullet_sop", "email_thread"):
            continue
        out.append(s)
    return out


def f11_wordings():
    from common import FMT2
    out = []
    for l in open(FMT2 / "wordings" / "family_pools.jsonl"):
        w = json.loads(l)
        if w.get("family") == FAMILY:
            out.append(w)
    return out


class RowGen:
    def __init__(self, card, setname, *, held_out=False, n_target=60):
        self.card = card
        self.setname = setname
        self.r = rng("rows", setname, card.card_id)
        if card.records:
            import records as REC
            self.styles = REC.record_styles(held_out)
            self.md_styles = REC.record_styles(held_out, "markdown_table")
            self.r.shuffle(self.md_styles)
            self.md_styles = self.md_styles[:4]
        else:
            self.styles = prose_styles(held_out)
        self.r.shuffle(self.styles)
        self.styles = self.styles[:12]
        ws = f11_wordings()
        self.r.shuffle(ws)
        self.w_yn = [w for w in ws if set(w["forms"]) & {"any", "yn"}][:6]
        self.w_ch = [w for w in ws if set(w["forms"]) & {"any", "choice"}][:6]
        self.code_count = Counter()
        self.n_target = n_target
        self.cap = math.ceil(n_target / len(card.tax.codes)) + 1
        self.yes_rate = self.r.uniform(0.2, 0.8)
        self.yes_rate = YES_RATE.get(card.card_id, self.yes_rate)   # repair r1: assigned stratified rate (build.assign_rates)
        self.acc_yn = self.acc_yes = 0
        self.seq = 0
        self.mark_yes = Counter()
        self.others_pool = None
        self._prep_text()

    def want_yes(self):
        """Repair r1 (G7): low-discrepancy yes draw over the card's accepted base yes/no rows: P(yes) = clip(rate *
        (n + 1) - n_yes, 0, 1), so the card's realized yes share stays within one row of its rate (one draw per row)."""
        p = min(1.0, max(0.0, self.yes_rate * (self.acc_yn + 1) - self.acc_yes))
        return self.r.random() < p

    # ---------------------------------------------------------------------------------------------- text pools
    def _prep_text(self):
        c = self.card
        from attrs import value_words
        vw = value_words(c.attrs)
        self.vtoks = {t for w in vw for t in toks(w)}
        name_words = set()
        for nm in list(c.names) + list(c.swapped or []) + list(getattr(c, "gnames", []) or []):
            name_words |= {t for t in toks(nm)}
        self.name_toks = name_words
        bad_markers = (lex.PRIOR_MARKERS + lex.LATER_MARKERS + lex.HYPO_MARKERS + lex.GENERIC_MARKERS
                       + lex.HEDGE_ADVERBS + lex.BANNED_LATER_FINDING + lex.BANNED_PREP_ATTRIB + lex.BANNED_HABITUAL
                       + lex.NOT_STATED + lex.ATTACK_MARKERS + tuple(lex.HEDGE_VERBS) + ("may", "might", "could")
                       + lex.CORRECTION_MARKERS)
        inert = []
        for s in c.view["inert"]:
            T = toks(s)
            if set(T) & (self.vtoks | self.name_toks | {"present", "absent"}):
                continue
            low = " " + " ".join(T) + " "
            if any(" " + " ".join(toks(m)) + " " in low for m in bad_markers):
                continue
            if any(ch.isdigit() for ch in s) or ":" in s or "\n" in s:
                continue
            inert.append(s)
        if len(inert) < 3:
            for p in c.people[:4]:
                inert.append(f"{p} signed the shift log at the end of the day.")
        self.inert = inert
        self.people = [p for p in c.people if not set(toks(p)) & (self.vtoks | self.name_toks)]
        if len(self.people) < 3:
            raise CardInvalid("too few clean people names")
        c.people = self.people
        self.desigs = None

    def designators(self, n):
        from names import designators
        self.seq += 1
        return designators(self.card.prefix, n, self.card.card_id, self.setname, self.seq,
                           exclude=getattr(self.card, "example_desigs", ()))

    # ---------------------------------------------------------------------------------------------- items
    def eligible_cells(self, form):
        t = self.card.tax
        out = []
        for cell in t.table:
            out.append(cell)
        return out

    def draw_cell(self, *, want=None, missing=None, need_nb=1):
        """Uniform eligible cell (A23) under the per-card gold-code cap; want: a predicate on (cell, gold)."""
        t, A = self.card.tax, self.card.attrs
        wc = getattr(self.card, "worked_cells", None) or ()
        cells = [cl for cl in t.table if cl not in wc]
        for _ in range(4000):
            cell = self.r.choice(cells)
            it = I.Item(cell, missing)
            g = t.assign(cell, missing)
            if self.code_count[g] >= self.cap:
                continue
            if want and not want(cell, g):
                continue
            ns = I.n_s(t, A, it, g)
            if len(ns) < need_nb:
                continue
            return it, g
        raise RowFail("no eligible cell")

    def base_item(self, *, want=None, missing=None, need_nb=1, num_place=None):
        it, g = self.draw_cell(want=want, missing=missing, need_nb=need_nb)
        it.desig = self.designators(1)[0]
        I.fill_focal(self.card, it, self.r, num_place=num_place)
        return it, g

    def add_inert(self, it, p=0.3):
        if self.r.random() < p:
            it.inert.append(self.r.choice(self.inert))

    def others(self, it, n=2):
        return self.designators(n + 1)[1:]

    def add_lure(self, it, gold, *, target_in=None, kind=None, attr=None):
        """One lure (value differs from v) on a stated attribute; target_in: restrict the target to this set."""
        c, t = self.card, self.card.tax
        cands = []
        cell = t.resolve_cell(it.cell, it.missing)
        for i, c2 in neighbours_of_cell(c.attrs, cell, fixed=it.missing):
            if attr is not None and i != attr:
                continue
            if c.attrs[i].kind == "pres" and c2[i] != PRES:
                continue                        # a presence lure always shows the term (present)
            k2 = t.table[c2]
            if target_in is not None and k2 not in target_in:
                continue
            cands.append((i, c2[i]))
        self.r.shuffle(cands)
        for i, v in cands:
            fr = I.make_frame(c, it, i, v, self.r, kind=kind, others=self.others(it))
            if fr is None:
                continue
            it.frames.append(fr)
            return fr
        return None

    def add_echo(self, it, *, kind=None):
        c = self.card
        st = [i for i in range(len(c.attrs)) if it.stated(i) and not (c.attrs[i].kind == "pres" and it.cell[i] != PRES)]
        i = self.r.choice(st)
        fr = I.make_frame(c, it, i, it.cell[i], self.r, kind=kind, others=self.others(it))
        if fr is not None:
            it.frames.append(fr)
        return fr

    # ---------------------------------------------------------------------------------------------- render
    def pick_style(self):
        return self.r.choice(self.styles)

    def doc(self, it, sents, *, subj_label=None):
        lab = subj_label or self.r.choice(lex.SUBJECT_LABELS)
        texts = [s["text"] for s in sents]
        n = len(texts)
        cut = sorted(self.r.sample(range(1, n), min(n - 1, self.r.choice((0, 1, 2))))) if n > 2 else []
        paras, prev = [], 0
        for x in cut + [n]:
            paras.append(" ".join(texts[prev:x]))
            prev = x
        blocks = [{"type": "para", "text": f"{lab}: {it.desig}"}] + [{"type": "para", "text": p} for p in paras if p]
        return {"title": None, "meta": [], "blocks": blocks}

    def render(self, *, doc, qtype, question, render="base", route=None, options=None, wording=None, note=None,
               style=None):
        st = style or self.pick_style()
        cir = self.card.card_ir(render, route)
        f = fcard.render_row_text(st, doc=doc, question=question, qtype=qtype, card=cir, options=options,
                                  wording=wording, note=note)
        return f, st, cir

    # ---------------------------------------------------------------------------------------------- meta
    def meta(self, *, it, gold_code, form, style, wording, edge, subtype=None, twin_of=None, twin_kind=None,
             render="base", extra_struct=None, depth=None):
        c = self.card
        defs_style = {"oneline": "one_line", "table": "rubric_table", "group": "one_line", "list": "decision_list",
                      "key": "decision_list", "short": "short"}[c.form] + ("_examples" if c.examples else "")
        struct = {"tax": c.tax.to_spec(), "form": form, "render": render, "card_form": c.form,
                  "examples": len(c.examples), "worked": len(c.worked), **(extra_struct or {})}
        if it is not None:
            struct["cell"] = [None if i == it.missing else v for i, v in enumerate(it.cell)]
            struct["frames"] = sorted([fr["kind"], fr["attr"], fr["value"]] for fr in it.frames)
            struct["attack"] = bool(it.attack)
        d = depth if depth is not None else (self.depth(it, gold_code) if it is not None else 1)
        return {"family": FAMILY, "spec_id": SPEC_SHA256, "card_id": c.card_id, "domain_pack": c.pack_id,
                "sampler": c.sampler, "gen_version": GEN_VERSION, "git_sha": _GIT,
                "seed": int(sha256_text(canon(struct) + self.setname)[:12], 16),
                "structure_hash": sha256_text(canon(struct))[:32], "difficulty_bin": None, "crowd_pg": None,
                "depth": d, "deep": d >= 6, "format_style": style["id"], "wording_id": wording["id"] if wording else None,
                "defs_style": defs_style, "twin_of": twin_of, "twin_kind": twin_kind, "text_source": None,
                "licence": LICENCE_PROGRAM, "edge": sorted(set(edge)), "subtype": subtype,
                "persona_seed": c.persona_seed}

    def depth(self, it, gold):
        c, t = self.card, self.card.tax
        cell = t.resolve_cell(it.cell, it.missing)
        d = 0
        for i in range(len(c.attrs)):
            if any(t.table[c2] != gold for j, c2 in neighbours_of_cell(c.attrs, cell) if j == i):
                d += 1
        if c.shape == "box" and c.form != "short":
            F, red = t.fits[cell]
            if red:
                d += 1
            if len(F) == 2:
                d += 1
            for k in range(len(t.codes)):
                cd = t.codes[k]
                if cd.rule and t.in_box(k, cell) and not red:
                    d += 1      # the rule's condition decided: removing it would change gold
                    break
        if c.shape == "group":
            gv = cell[t.ai[t.gattr]]
            home = [gi for gi, g in enumerate(t.groups) if gv in g["vals"]][0]
            if t.group_of(cell) != home:
                d += 1
        if it.missing is not None:
            d += 1
        return d
