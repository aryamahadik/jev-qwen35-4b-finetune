"""F11 question forms for program cards: taxonomy choice, code-assignment yes/no, inverted, coarse, group yes/no;
plus the row twins (neg / dneg units, attack, inert, attr_flip). G0 sections 2 (display, question forms), 5, 9."""
from __future__ import annotations

import copy

import lex
import items as I
from common import toks
from fmt1 import card as fcard, pool
from rows import RowGen, RowFail
from tax import neighbours_of_cell, all_cells

NONE_SHARE = 0.30


STACKED_KV_SKINS = ("kv.aligned_colon",)   # repair r1: never holds a multi-record table (G2)


class FormGen(RowGen):
    # ---------------------------------------------------------------------------------------------- yes/no
    def yn_spec(self, *, missing=None):
        c, t, r = self.card, self.card.tax, self.r
        want_yes = self.want_yes()
        it, g = self.base_item(missing=missing, need_nb=1)
        A = c.attrs
        ns = I.n_s(t, A, it, g)
        nall = I.n_all(t, A, it, g)
        edge = []
        if want_yes:
            K = g
            # >= 1 lure targeting N_s(v)
            if not self.add_lure(it, g, target_in=set(ns)):
                raise RowFail("no lure")
        else:
            outside = [k for k in range(len(t.codes)) if k != g and k not in nall]
            use_out = r.random() < 0.30 and outside and c.form != "short"
            if use_out:
                K = r.choice(outside)
                # nearest cell assigned K (Hamming over stated attributes); one differing stated attribute
                cell = t.resolve_cell(it.cell, it.missing)
                best, bd = [], 99
                for c2, k2 in t.table.items():
                    if k2 != K:
                        continue
                    if it.missing is not None and c2[it.missing] != cell[it.missing]:
                        continue
                    d = sum(1 for i in range(len(A)) if c2[i] != cell[i])
                    if d < bd:
                        best, bd = [c2], d
                    elif d == bd:
                        best.append(c2)
                if not best:
                    raise RowFail("asked code has no cell on the stated attributes")
                c2 = r.choice(best)
                diff = [i for i in range(len(A)) if c2[i] != cell[i] and it.stated(i)
                        and not (A[i].kind == "pres" and c2[i] != 0)]
                if not diff:
                    raise RowFail("asked code shares the focal cell")
                i = r.choice(diff)
                fr = I.make_frame(c, it, i, c2[i], r, others=self.others(it))
                if fr is None:
                    fr = I.make_frame(c, it, i, c2[i], r, kind="OTHER", others=self.others(it))
                if fr is None:
                    raise RowFail("no asked-value frame")
                it.frames.append(fr)
                if I.frame_target(t, it, fr) == g or I.frame_target(t, it, fr) not in ns:
                    if not self.add_lure(it, g, target_in=set(ns)):
                        raise RowFail("no lure")
            else:
                okK = [k for k in sorted(ns) if any(not (A[i].kind == "pres" and v != 0) for i, v in ns[k])]
                if not okK:
                    raise RowFail("no askable neighbour")
                K = r.choice(okK)
                i, v = r.choice([(i, v) for i, v in ns[K] if not (A[i].kind == "pres" and v != 0)])
                fr = I.make_frame(c, it, i, v, r, others=self.others(it))
                if fr is None:
                    fr = I.make_frame(c, it, i, v, r, kind="OTHER", others=self.others(it))
                if fr is None:
                    raise RowFail("no asked-value frame")
                it.frames.append(fr)
        # extra frames: same distribution for yes and no rows
        for _ in range(r.choice((0, 0, 1, 1, 2))):
            if r.random() < 0.5:
                self.add_lure(it, g)
            else:
                self.add_echo(it)
        self.add_inert(it)
        return {"form": "yn", "item": it, "gold_code": g, "K": K, "n_frame": 0, "edge": edge}

    # ---------------------------------------------------------------------------------------------- choice
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

    def choice_spec(self, *, missing=None):
        c, t, r = self.card, self.card.tax, self.r
        it, g = self.base_item(missing=missing, need_nb=2)
        A = c.attrs
        nall = I.n_all(t, A, it, g)
        if len(nall) < 2:
            raise RowFail("|N(v)| < 2")
        n = len(t.codes)
        full = r.random() < 0.5 or n < 11
        none_shown = False
        none_gold = False
        if full:
            shown = list(range(n))
        else:
            m = r.randint(8, min(15, n - 3))
            none_shown = r.random() < NONE_SHARE
            if none_shown:
                none_gold = r.random() < 1.0 / (m + 1)
            nb = sorted(nall)
            r.shuffle(nb)
            shown = [] if none_gold else [g]
            shown += nb[:r.randint(2, 3)]
            # decoy cluster: one non-gold code outside N(v) and 2-3 of its code neighbours
            cn = t.code_neighbours()
            outside = [k for k in range(n) if k != g and k not in nall]
            if outside:
                D = r.choice(outside)
                shown.append(D)
                dn = [k for k in cn[D] if k != g and k not in shown]
                r.shuffle(dn)
                shown += dn[:r.randint(2, 3)]
            shown = [k for k in dict.fromkeys(shown) if not (none_gold and k == g)]
            rest = [k for k in range(n) if k not in shown and k != g]
            r.shuffle(rest)
            while len(shown) < m and rest:
                shown.append(rest.pop())
            shown = shown[:m] if len(shown) > m else shown
            if not none_gold and g not in shown:
                shown[0] = g
            if not any(k in nall for k in shown):
                raise RowFail("no close distractor shown")
        # lures / echoes
        edge = []
        p_lure = 0.9 if c.sampler == "S2" else (1.0 if c.form == "short" else 0.6)
        if r.random() < p_lure:
            tgt = set(k for k in nall if k in shown)
            if c.form == "short":
                tgt = set(k for k in nall if k in shown)
            for _ in range(r.choice((1, 1, 2))):
                if not self.add_lure(it, g, target_in=tgt or None):
                    self.add_lure(it, g)
        if r.random() < 0.25:
            self.add_echo(it)
        self.add_inert(it)
        r.shuffle(shown)
        return {"form": "choice", "item": it, "gold_code": g, "shown": shown, "none_shown": none_shown,
                "none_gold": none_gold, "full": full, "label": self.label_form(), "edge": edge}

    # ---------------------------------------------------------------------------------------------- inverted
    def inverted_spec(self):
        c, t, r = self.card, self.card.tax, self.r
        A = c.attrs
        nrep = r.randint(3, 6)
        none_shown = r.random() < NONE_SHARE
        none_gold = none_shown and r.random() < 1.0 / (nrep + 1)
        for _ in range(200):
            K = r.randrange(len(t.codes))
            if self.code_count[K] >= self.cap:
                continue
            kcells = [cl for cl, k in t.table.items() if k == K]
            base = r.choice(kcells)
            nbs = [(i, c2) for i, c2 in neighbours_of_cell(A, base) if t.table[c2] != K]
            if len(nbs) < nrep:
                continue
            r.shuffle(nbs)
            cells = [c2 for _, c2 in nbs[:nrep - (0 if none_gold else 1)]]
            if len(set(cells)) != len(cells):
                continue
            if not none_gold:
                cells.append(base)
            break
        else:
            raise RowFail("no inverted draw")
        r.shuffle(cells)
        desigs = self.designators(len(cells))
        reps = []
        for cell, d in zip(cells, desigs):
            it = I.Item(cell)
            it.desig = d
            I.fill_focal(c, it, r)
            reps.append(it)
        if r.random() < 0.6:
            saved = c.frame_kinds
            if c.records:
                c.frame_kinds = [k for k in saved if k != "OTHER"]
            try:
                for j in r.sample(range(len(reps)), r.choice((1, 2)) if len(reps) > 1 else 1):
                    it = reps[j]
                    g_j = t.table[it.cell]
                    ns = I.n_s(t, A, it, g_j)
                    if ns:
                        self.add_lure(it, g_j, target_in=set(ns))
            finally:
                c.frame_kinds = saved
        gold_idx = None if none_gold else next(j for j, it in enumerate(reps) if t.table[it.cell] == K)
        return {"form": "inverted", "K": K, "reps": reps, "none_shown": none_shown, "none_gold": none_gold,
                "gold_idx": gold_idx, "label": "code" if r.random() < 0.5 else "name", "edge": [],
                "gold_code": K}

    # ---------------------------------------------------------------------------------------------- S3 coarse / group yes-no
    def coarse_spec(self):
        c, t, r = self.card, self.card.tax, self.r
        it, g = self.base_item(need_nb=1)
        if r.random() < 0.6:
            self.add_lure(it, g)
        self.add_inert(it)
        return {"form": "coarse", "item": it, "gold_code": g, "group": t.group_assign(it.cell, it.missing),
                "edge": [], "label": "name"}

    def gyn_spec(self):
        c, t, r = self.card, self.card.tax, self.r
        if c.shape == "key":
            return self.gyn_key_spec()
        it, g = self.base_item(need_nb=1)
        G_true = t.group_assign(it.cell, it.missing)
        want_yes = self.want_yes()
        ng = len(t.groups)
        if want_yes:
            G = G_true
        else:
            G = r.choice([x for x in range(ng) if x != G_true])
            # the asked group's value in a lure frame (unless a scope note moved the report out of G)
            ga = t.ai[t.gattr]
            gv = it.cell[ga]
            if gv not in t.groups[G]["vals"]:
                v = r.choice(sorted(t.groups[G]["vals"]))
                fr = I.make_frame(c, it, ga, v, r, others=self.others(it))
                if fr is not None:
                    it.frames.append(fr)
        ns = I.n_s(t, c.attrs, it, g)
        if ns:
            self.add_lure(it, g, target_in=set(ns))
        self.add_inert(it)
        return {"form": "gyn", "item": it, "gold_code": g, "G": G, "n_frame": 0, "edge": [], "yes": G == G_true}

    def gyn_key_spec(self):
        """S5 program arm group yes/no: is the report in named couplet G's group (the key walk passes G)?"""
        c, t, r = self.card, self.card.tax, self.r
        it, g = self.base_item(need_nb=1)
        passed = sorted({t.couplets[n]["group"] for n in t.groups_of(it.cell, it.missing)})
        other = [x for x in sorted(t.groups) if x not in passed]
        want_yes = self.want_yes()
        pool = passed if (want_yes and passed) or not other else other
        G = r.choice(pool)
        ns = I.n_s(t, c.attrs, it, g)
        if ns:
            self.add_lure(it, g, target_in=set(ns))
        self.add_inert(it)
        return {"form": "gyn", "item": it, "gold_code": g, "G": G, "n_frame": 0, "edge": [], "yes": G in passed}

    # ---------------------------------------------------------------------------------------------- emit
    def emit(self, spec, *, rid, gid, cid, role="base", twin_of=None, twin_kind=None, style=None, wording=None):
        c, t, r = self.card, self.card.tax, self.r
        f = spec["form"]
        fill = c.fill
        note_parts = []
        render = "base"
        route = None
        options = None
        edge = list(spec.get("edge", []))
        if spec.get("item") is not None:
            it = spec["item"]
            sents = ([] if c.records else I.realize(c, it, r)) if "sents" not in spec else spec["sents"]
            spec["sents"] = sents
            if it.attack and not c.records:
                sents = list(sents)
                sents.insert(1 + r.randrange(len(sents)), {"text": it.attack, "frame": "ATTACK", "attr": None})
            if spec.get("doc") is not None and not it.attack:
                doc = spec["doc"]
            elif c.records:
                import records as REC
                doc = REC.record_doc(self, it, spec)
            else:
                doc = self.doc(it, sents, subj_label=spec.setdefault("subj", r.choice(lex.SUBJECT_LABELS)))
                if not it.attack:
                    spec["doc"] = doc
            for fr in it.frames:
                tg = I.frame_target(t, it, fr)
                edge.append("echo" if tg == spec["gold_code"] else {
                    "OTHER": "lure_other_entity", "PRIOR": "lure_prior", "LATER": "lure_later",
                    "HYPO": "lure_hypothetical", "HEDGED": "lure_hedged", "GENERIC": "lure_generic",
                    "NEG": "lure_negated", "COMMENT": "lure_comment"}[fr["kind"]])
            if it.missing is not None:
                edge.append("missing_default")
        wording = wording or spec.get("wording")
        if f in ("yn", "gyn"):
            qtype = "noul"
            wording = wording or r.choice(self.w_yn)
            nf = spec["n_frame"]
            if f == "yn":
                Kt = c.ids[spec["K"]] if c.form != "short" else c.names[spec["K"]]
                if c.form != "short" and spec.setdefault("ylabel", r.choice(("code", "name"))) == "name":
                    Kt = c.names[spec["K"]]
                qk = ("yn", "yn_neg", "yn_dneg")[nf]
                question = lex.Q[qk].format(K=Kt, **fill)
                note_parts.append(lex.ROW_SEM["SEM-39"].format(K=Kt, **fill))
                hit = spec["K"] == spec["gold_code"]
                marked = t.codes[spec["K"]].mark
            else:
                Gt = c.gnames[spec["G"]]
                qk = ("gyn", "gyn_neg", "gyn_dneg")[nf]
                question = lex.Q[qk].format(G=Gt, **fill)
                note_parts.append(lex.ROW_SEM["SEM-39-G"].format(G=Gt))
                hit = spec["yes"]
                marked = all(t.codes[k].mark for k in t.groups[spec["G"]]["leaves"])
            gold = 1 if (hit != (nf == 1)) else 0
            spec["polar_bad"] = bool(marked) != (nf == 1)
        elif f == "choice":
            qtype = "choice"
            wording = wording or r.choice(self.w_ch)
            lf = spec["label"]
            render = {"masked": "masked", "swapped": "swapped"}.get(lf, "base")
            edge += [lf] if lf in ("masked", "swapped") else []
            options = [c.code_label(k, lf) for k in spec["shown"]]
            if spec["none_shown"]:
                options.insert(spec.setdefault("none_pos", r.randrange(len(options) + 1)), lex.NONE_CODES)
            gold = lex.NONE_CODES if spec["none_gold"] else c.code_label(spec["gold_code"], lf)
            if spec["none_gold"]:
                edge.append("none_gold")
            question = lex.Q["choice"].format(**fill)
            if c.form == "oneline":
                other = {}
                for k in spec["shown"]:
                    other[k] = None if lf == "masked" else (c.names[k] if lf == "code" else c.ids[k])
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
        elif f == "inverted":
            qtype = "choice"
            wording = wording or r.choice(self.w_ch)
            lf = spec["label"]
            Kt = c.ids[spec["K"]] if lf == "code" else c.names[spec["K"]]
            refs = spec.setdefault("refs", fcard.case_refs(r.choice([x["id"] for x in pool.inverted_all(
                "inverted_case_ref")]), len(spec["reps"]), f"{c.card_id}|{rid}"))
            blocks = []
            for ref, it in zip(refs, spec["reps"]):
                lab = spec.setdefault("rep_lab", {}).setdefault(it.desig, r.choice(lex.SUBJECT_LABELS))
                blocks.append({"type": "para", "text": ref})
                blocks.append({"type": "para", "text": f"{lab}: {it.desig}"})
                if c.records:
                    import records as REC
                    rsp = spec.setdefault("rep_rec", {}).setdefault(it.desig, {})
                    blocks.append(REC.record_block(self, it, rsp, allow_other=False))
                    continue
                ss = spec.setdefault("rep_sents", {}).get(it.desig) or I.realize(c, it, r)
                spec["rep_sents"][it.desig] = ss
                blocks.append({"type": "para", "text": " ".join(s["text"] for s in ss)})
            doc = {"title": None, "meta": [], "blocks": blocks}
            options = list(refs)
            if spec["none_shown"]:
                options.insert(spec.setdefault("none_pos", r.randrange(len(options) + 1)), lex.NONE_REPORTS)
            gold = lex.NONE_REPORTS if spec["none_gold"] else refs[spec["gold_idx"]]
            question = lex.Q["inverted"].format(K=Kt, **fill)
            note_parts.append(lex.ROW_SEM["SEM-39"].format(K=Kt, **fill))
            note_parts.append(lex.ROW_SEM["SEM-51"].format(**fill))
            note_parts.append(lex.ROW_SEM["SEM-51-NONE"].format(K=Kt, none=lex.NONE_REPORTS, **fill)
                              if spec["none_shown"] else lex.ROW_SEM["SEM-51-ONE"].format(K=Kt, **fill))
            if spec["none_gold"]:
                edge.append("none_gold")
        elif f == "coarse":
            qtype = "choice"
            wording = wording or r.choice(self.w_ch)
            order = spec.setdefault("gorder", r.sample(range(len(t.groups)), len(t.groups)))
            options = [c.gnames[g] for g in order]
            gold = c.gnames[spec["group"]]
            question = lex.Q["coarse"].format(**fill)
        else:
            raise ValueError(f)
        if c.records and f == "inverted" and not (style or spec.get("style")):
            style = r.choice(self.md_styles)
        st = style or spec.get("style") or self.pick_style()
        spec["style"] = st
        if c.records and spec.get("item") is not None and st.get("skin") in STACKED_KV_SKINS and \
                any(b.get("type") == "table" for b in doc.get("blocks", [])):
            # repair r1 (G2): this skin renders a multi-record table as stacked key-value blocks with no record
            # boundary but a blank line (solver B reads one record); multi-record containers use other skins
            raise RowFail("multi-record table in a stacked key-value skin")
        spec["wording"] = wording
        fields, st, cir = self.render(doc=doc, qtype=qtype, question=question, render=render, route=route,
                                      options=options, wording=wording["text"], note=" ".join(note_parts) or None,
                                      style=st)
        row = {"id": rid, "group_id": gid, "call_id": cid, "source": "c_f11", "state": fields["state"],
               "qtype": qtype, "instructions": fields["instructions"], "options": options if qtype == "choice" else None,
               "gold": gold, "role": role, "card": fields["card"]}
        res = fcard.loader_check(row, must_show=fcard.must_show(cir, question=question, wording=wording["text"],
                                                                note=" ".join(note_parts) or None))
        if not res["ok"]:
            raise RowFail("loader_check: " + "; ".join(res["problems"][:2]))
        it = spec.get("item")
        subtype = {"inverted": "inverted", "coarse": "coarse"}.get(f)
        extra = {"q": f, "K": spec.get("K"), "G": spec.get("G"), "n_frame": spec.get("n_frame"),
                 "shown": spec.get("shown"), "none": [spec.get("none_shown"), spec.get("none_gold")],
                 "label": spec.get("label")}
        if f == "inverted":
            extra["reps"] = [list(x.cell) for x in spec["reps"]]
        row["meta"] = self.meta(it=it, gold_code=spec["gold_code"], form=f, style=st, wording=wording, edge=edge,
                                subtype=subtype, twin_of=twin_of, twin_kind=twin_kind, render=render,
                                extra_struct=extra, depth=None if it is not None else 1)
        if c.form == "short":
            row["meta"]["edge"] = sorted(set(row["meta"]["edge"]) | {"short_card"})
        row["_spec"] = spec
        return row
