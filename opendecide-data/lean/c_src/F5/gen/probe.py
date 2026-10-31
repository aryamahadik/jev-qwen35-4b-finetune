"""Hard-negation probe (G0 section 5, probe; spec section 10; report only, sizes F5 for round 2): 400 items = the 25
held-out cue templates x 16 items, on S1-S4 base shapes with held-out packs (the held-out packs S5 does not use) and
held-out styles. Every item contains its held-out template; no other question cue comes from that template's family
and the text holds no cue of that family either (checked on the rendered text); template ids are logged per item.
Yes rate 50% per template (8 / 8), so 50% per k as well. Probe items are single rows (no units).

  python -m gen.probe
"""
from __future__ import annotations

import collections
import json
import random
import re

from . import bank, gen, rows as R
from .build import make_row, side_record
from .common import OUT, SEED, TMP, negc, rng_for, sha, uhash, write_jsonl
from .forms import FRAMES, compose
from .packs import views
from .plan import plan_cards

FAMILY_TEXT = {  # surface entries of each family that may not appear in the item's text (rendered state)
    "C1": [r"\bnot\b", r"\bno\b", r"n't\b"], "C2": [r"it is not the case that", r"it is false that"],
    "C3": [r"\bfail", r"\bneglect", r"\bomit", r"did not manage"], "C5": [r"\black", r"\bwithout\b", r"free of"],
    "C6": [], "C8": [r"\bnone of\b", r"\bnot every\b", r"\bnot all\b", r"(?<![a-z])No [a-z ]+ that\b"],
    "C9": [r"no fewer than", r"no more than", r"not less than", r"not more than"],
    "C10": [r"no later than", r"no earlier than", r"not before", r"not after"], "C11": [r"other than", r"all except"],
    "C12": [r"must not", r"may not", r"is not permitted to", r"need not", r"does not have to", r"is not required to",
            r"cannot"], "C13": [r"neither", r"\bnor\b", r"not both"], "C14": [r"hardly", r"scarcely", r"\bfew\b"],
    "C15": [r"\bnever\b", r"no longer", r"\bstill\b"], "C16": [r"not only"]}


def sampler_for(atom):
    if atom.startswith("ev:"):
        return "S2"
    if atom in ("q",):
        return "S4"
    if atom.startswith("grp:") or atom == "has":
        return "S3"
    return "S1"


def kind_for(atom, H, card, rng, s):
    s.update(H.plan_slot(card, rng, s))
    if atom.startswith("ev:"):
        s["kind"] = {"renew": "ev_renew", "report": "ev_report", "file": "ev_file"}[atom[3:]]
    if s.get("_core", "").startswith("C3o"):
        s["kind"] = "valid"
    if atom == "deon":
        s["kind"] = "deon"
    if atom == "amt":
        s["kind"] = "amt"
    if atom.startswith("conn:") or atom == "any":
        s["kind"] = "out" if card["sampler"] == "S1" else s.get("kind")
    if atom == "has":
        s["has_base"] = True
    return s


def build():
    B = json.load(open(OUT / "cue_bank.json"))
    held = B["probe_holdout"]
    from .packs import heldout_split, PROBE_PACKS_PACKS4
    _, probe_pids = heldout_split()
    need = sorted({sampler_for(t.split("|")[2]) for t in held})
    cards = []
    others = [p for p in probe_pids if p not in PROBE_PACKS_PACKS4]
    pid_iter = iter(others * 4)
    for smp in need:
        for _ in range(2):
            pids = list(PROBE_PACKS_PACKS4) if smp == "S1" and _ == 0 else [next(pid_iter), next(pid_iter)]
            cs = plan_cards(2, split="heldout", samplers=[smp], seed_tag=f"pb-{smp}-{pids[0]}", shares={smp: 1.0},
                            held_pids=pids)
            for c in cs:
                c["world"] = "closed"
                c["inverted"] = False
                c["fams"] = {f: True for f in c["fams"]}
                if smp == "S2":
                    c["fams"]["C15"] = True
                c["card_id"] = c["card_id"].replace("-dv-", "-pb-")
                gen.H_for(c).card_setup(c)
                c["a_card"], c["p_card"], c["f_card"] = 0.5, 0.0, 0.0
            cards += cs
    by_s = collections.defaultdict(list)
    for c in cards:
        by_s[c["sampler"]].append(c)
    items, side, log, dump = [], [], collections.Counter(), []
    from fmt1 import pool as fpool
    for t in held:
        fam, core_id, atom, pos = t.split("|")
        smp = sampler_for(atom)
        rng = rng_for("probe", t)
        got = {0: 0, 1: 0}
        tries = 0
        while (got[0] < 8 or got[1] < 8) and tries < 6000:
            tries += 1
            card = rng.choice(by_s[smp])
            H = gen.H_for(card)
            s = {"i": tries, "pair": None, "role": None, "v": rng.randrange(2), "g": rng.randrange(2),
                 "attack": False, "tag": rng.choice(["good", "bad"]), "vk": 1, "two_lcore": False, "_core": core_id}
            try:
                s = kind_for(atom, H, card, rng, s)
                ctx = dict(card)
                ctx.update(H.slot_ctx(card, s, rng))
            except (IndexError, KeyError):
                continue
            if atom == "has" and smp == "S3":
                hp = [p for p in card["preds"] if p.startswith("has:")]
                if not hp:
                    continue
                ctx["base_pred"] = rng.choice(hp)
            try:
                r = H.build_structure(ctx, s, rng)
            except Exception:  # noqa: BLE001
                continue
            if r is None:
                continue
            M, P, info = r
            cores = H.cores(ctx, M, P, rng, s)
            if core_id == "C15.never" and M.get("base", {}).get("kind") == "ev":
                # "never" about a person with no such event gives the Yes items (an event base always has one)
                from . import s2
                from .forms import Core, NOT
                bs = M["base"]
                rem = s2.resolve(M)
                quiet = [p for p in card["people"] if not s2.events(rem, bs["kind_ev"], p, bs["item"])]
                if quiet and rng.random() < 0.5:
                    p = rng.choice(quiet)
                    cores["C15.never"] = Core("C15.never", ("C15",),
                                              f"{p} never {s2.event_vp(bs['kind_ev'], bs['item_txt'], 'past')}", None,
                                              NOT(["ev", bs["kind_ev"], p, bs["item_txt"], None, None]), 1, "down",
                                              lneg=("never",), rel="other", ptag=bs.get("tag"))
            if fam == "C2":
                cands = [c for c in cores.values() if c.k == 0 and not c.fam and c.lf == P]
                pre = ("C2f",)
            else:
                cands = [c for c in cores.values() if bank.family_of(c) == fam and bank.norm_tid(c.tid) == core_id
                         and bank.atom_kind(c.lf) == atom and (pos == "e" or c.matrix)]
                pre = ()
            if not cands:
                continue
            c = rng.choice(cands)
            if pos == "m" and fam != "C2":
                q = compose(c, "mq", (), "")
            else:
                fid = sorted(FRAMES)[int(uhash("pf", t, tries) * len(FRAMES))]
                q = compose(c, fid, pre)
            try:
                (g,) = H.solve(M, [q[1]])
            except Exception:  # noqa: BLE001
                continue
            g = int(g)
            if got[g] >= 8:
                continue
            doc = H.doc(M)
            sts = [st for st in fpool.styles(held_out=True) if R.can_render(doc, st)]
            if not sts:
                continue
            st = sts[int(uhash("ps", t, tries) * len(sts))]
            state_txt = None
            try:
                from fmt1.render import render_state
                state_txt = render_state(doc, st)
            except Exception:  # noqa: BLE001
                continue
            if any(re.search(p, state_txt, re.I) for p in FAMILY_TEXT.get(fam, [])):
                log["text_has_family_cue"] += 1
                continue
            base_id = f"{card['card_id']}-p{len(items):03d}"
            b = {"card": card, "ctx": ctx, "slot": s, "M": M, "P": P, "info": info, "cores": cores, "v": None,
                 "vcore": c.tid, "vn2": 0, "base_id": base_id, "rows": {"V": q}}
            keys = set(H.full_keys(card))
            params = H.sem_params(card, M)
            params["value_sets_full"] = [(a_, v_, params.get("vs_form", "case")) for a_, v_ in
                                         params.get("value_sets", [])]
            civ, defs_style, dv = R.card_ir(card, keys, params, short=False)
            w = card["wordings"][int(uhash("pw", t, tries) * len(card["wordings"]))]
            rid = f"f5pb-{sha(base_id + t)[:12]}-P"
            try:
                fields, res = R.render_row(st, doc, q[0], w["text"], g, civ, rid)
            except Exception:  # noqa: BLE001
                continue
            from .gates import served_tokens
            if served_tokens({"state": fields["state"], "qtype": "noul", "instructions": fields["instructions"],
                              "options": None, "gold": g, "card": fields["card"]}) >= 1900:
                log["length_cap"] += 1
                continue
            b["ids"] = {"V": rid}
            b["card_keys"], b["defs_style"] = sorted(keys), defs_style
            row = make_row(b, "V", {"V": rid, "A": rid}, fields, g, st, w, defs_style, True)
            row["role"] = "probe"
            row["meta"]["twin_of"] = None
            row["meta"]["twin_kind"] = None
            row["group_id"] = f"c_f5:pb:{sha(base_id)[:16]}"
            row["call_id"] = f"c_f5:pb:{sha(rid)[:12]}"
            sr = side_record(b, "V", row, q[0], q[2], q[3], q[4], q[5], None)
            sr["probe_template"] = t
            sr["row_type"] = "probe"
            items.append(row)
            side.append(sr)
            dump.append({"base_id": base_id, "sampler": card["sampler"], "inverted": False, "M": M, "P": P,
                         "ids": {"V": rid}, "v": None})
            got[g] += 1
            b["v"] = None
        log[f"done:{t}"] = got[0] + got[1]
    write_jsonl(OUT / "probe_hardneg.jsonl", items)
    write_jsonl(OUT / "probe_hardneg.F5_polarity.jsonl", side)
    write_jsonl(TMP / "probe_hardneg.bases.jsonl", dump)
    write_jsonl(OUT / "probe_hardneg.relations.jsonl", [])
    write_jsonl(OUT / "probe_hardneg.cards.jsonl", [__import__("gen.plan", fromlist=["x"]).card_summary(c)
                                                    for c in cards])
    print(json.dumps({"items": len(items), "log": dict(log)}, indent=1)[:2500])


if __name__ == "__main__":
    build()
