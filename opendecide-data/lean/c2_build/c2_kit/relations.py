"""c2_kit/relations.py: the relation emitter and G-TW (C2_DATA_SPEC 4.1 overlay, 6.3 G-TW; bar 100%).

Relations and their unit rules (spec 4.1; train_decoder.make_units groups rows by call_id):
  complement       yes/no pair, gold(Q) = 1 - gold(not-Q) under the card's closed-world sentence; same call_id,
                   relation "complement". Kinds: syntactic (exactly one negation cue more or less, negcount k_all),
                   implicit (one implicit cue: fail to, lack ...; k_syn unchanged), antonym / option_framing (no added
                   cue; the two question forms are a declared complement pair of the family).
  minimal-edit twin exactly one INPUT slot differs and the gold flips exactly as the construction predicted; own
                   call_id, meta.twin_of = the base row (no relation term). The rest of the row is identical once the
                   changed slot's spans and the spans of the derived slots that depend on it are masked; same skin,
                   wording and slot forms.
  equiv            same facts (plugin.canonical equal), another register or container, same gold and option set;
                   same call_id, relation "equiv".
  inv (attack)     the same row plus one inert attack line; same facts and gold; same call_id, relation "inv".
  premise removal  one input slot removed, gold becomes the abstain key; own call_id.
A relation unit holds at most 3 rows. Each check raises GTWError; the caller drops the whole unit (never a relabel).

Twin gold mix (review fix): a minimal-edit twin of a choice row mirrors its base. Flipping the one failing check of a
"which check fails" row lands on "none", so twins of the common "one check fails" bases pile up on the abstain key
(measured: 70-85% of twin rows, about 40% of all rows against a 20-30% G0 target). abstain_twin_kept() thins the twins
that move the gold ONTO the abstain key with a family constant, from the row key only; the family sets the constant so
the abstain share over ALL emitted rows (base + twin + equiv + inv) meets its G0 target, and tests it there.

  em = RelationEmitter(plugin)
  em.base(rr)
  em.complement(rr, rr_c, spec)            em.twin(rr, rr_t, spec, spec_t, "AMOUNT", predicted)
  em.equiv(rr, rr_e, spec, spec)           em.inv(rr, rr_x, spec)
  rows, rels = em.finalize()               # rels: [{"a", "b", "type"}] in train_decoder's relation format
"""
from __future__ import annotations

from . import paths  # noqa: F401
import negcount  # noqa: E402
from .distractors import uhash  # noqa: E402
from .plugin import Spec  # noqa: E402
from . import slots as S  # noqa: E402
from .rows import sha  # noqa: E402

MAX_UNIT = 3
TEXT_FIELDS = ("state", "instructions", "card")


class GTWError(AssertionError):
    """A twin or complement breaks G-TW (drop the unit)."""


def abstain_twin_kept(row_key: str, base_answer, twin_answer, abstain_key, keep: float) -> bool:
    """False for the twins thinned out: a twin whose gold moves onto the abstain key from another answer is kept with
    probability `keep` (a label-blind uniform draw from the row key); every other twin is kept."""
    if twin_answer != abstain_key or base_answer == abstain_key:
        return True
    return uhash(row_key, "abstain_twin") < keep


def slot_diff(a: Spec, b: Spec) -> set:
    """Input slots whose value differs (or exists on one side only). Structure, question form, sampler and card
    must be identical: a twin changes one VALUE, nothing else."""
    for k in ("family", "sampler", "card_id", "qform", "closed_world"):
        if getattr(a, k) != getattr(b, k):
            raise GTWError(f"twin changes {k}")
    if a.structure != b.structure:
        raise GTWError("twin changes the hidden structure")
    out = set(a.slots) ^ set(b.slots)
    for k in set(a.slots) & set(b.slots):
        sa, sb = a.slots[k], b.slots[k]
        if (sa.kind, sa.params, S.canonical(sa)) != (sb.kind, sb.params, S.canonical(sb)):
            out.add(k)
    return out


def affected(spec: Spec, changed: set) -> set:
    """The changed slots plus every derived slot that depends on one of them."""
    out = set(changed)
    for d, deps in (spec.derived_deps or {}).items():
        if set(deps) & changed:
            out.add(d)
    return out


def masked(rr, fld: str, slots: set) -> str:
    text = rr.text(fld)
    spans = sorted((sp.start, sp.end) for sp in rr.spans if sp.field == fld and sp.slot in slots)
    out, pos = [], 0
    for a, b in spans:
        if a < pos:
            continue
        out += [text[pos:a], "\x00"]
        pos = b
    out.append(text[pos:])
    return "".join(out)


def twin_text_problems(ra, rb, slots: set) -> list:
    probs = []
    if (ra.skin_id, ra.wording_id, ra.attack_id) != (rb.skin_id, rb.wording_id, rb.attack_id):
        probs.append("twin uses another skin, wording or attack line")
    for k in set(ra.forms) | set(rb.forms):
        if k not in slots and ra.forms.get(k) != rb.forms.get(k):
            probs.append(f"slot {k} is written in another form")
    for fld in TEXT_FIELDS:
        if masked(ra, fld, slots) != masked(rb, fld, slots):
            probs.append(f"{fld} differs outside the changed slot")
    if ra.row["qtype"] != rb.row["qtype"]:
        probs.append("qtype differs")
    elif ra.row["qtype"] == "choice" and ra.option_set and ra.option_set.meta.get("kind") == "closed":
        if ra.row["options"] != rb.row["options"]:
            probs.append("closed option set differs")
    return probs


class RelationEmitter:
    def __init__(self, plugin):
        self.plugin = plugin
        self.rows: dict = {}
        self.order: list = []
        self.edges: list = []         # (a, b, type)
        self.links: dict = {}         # partner id -> (base id, twin kind, role)
        self.root = None

    def _add(self, rr):
        rid = rr.row["id"]
        if rid in self.rows:
            raise GTWError(f"duplicate row id {rid}")
        self.rows[rid] = rr
        self.order.append(rid)
        return rid

    def base(self, rr):
        if self.root is not None:
            raise GTWError("one base per emitter")
        self.root = self._add(rr)
        return self.root

    def _link(self, base, partner, kind, role):
        if base.row["id"] not in self.rows:
            raise GTWError("emit the base row first")
        pid = self._add(partner)
        self.links[pid] = (base.row["id"], kind, role)
        return pid

    # ---------------------------------------------------------------------------------------- relations
    def complement(self, ra, rb, spec: Spec):
        q = self.plugin.QFORMS
        qa, qb = q[ra.row["meta"]["qform"]], q[rb.row["meta"]["qform"]]
        probs = []
        if ra.row["qtype"] != "noul" or rb.row["qtype"] != "noul":
            probs.append("complements are yes/no pairs")
        if qa.predicate != qb.predicate or qa.polarity == qb.polarity:
            probs.append("question forms are not a complement pair (same predicate, opposite polarity)")
        if not spec.closed_world:
            probs.append("complement without a closed-world card")
        sent = self.plugin.CLOSED_WORLD_SENTENCE
        for r in (ra, rb):
            if sent not in "\n".join(r.text(f) for f in TEXT_FIELDS):
                probs.append("closed-world sentence missing from a row")
        if ra.row["state"] != rb.row["state"] or ra.row["card"] != rb.row["card"]:
            probs.append("complement rows differ outside the question")
        if ra.row["gold"] + rb.row["gold"] != 1:
            probs.append(f"gold(Q) = {ra.row['gold']}, gold(not-Q) = {rb.row['gold']}")
        neg = qa if qa.polarity == -1 else qb
        ka, kb = negcount.count(ra.row["instructions"]), negcount.count(rb.row["instructions"])
        if neg.complement_kind == "syntactic" and abs(ka.k_all - kb.k_all) != 1:
            probs.append(f"syntactic complement: negation cues {ka.k_all} vs {kb.k_all} (need a difference of 1)")
        if neg.complement_kind == "implicit" and (abs(ka.k_all - kb.k_all) != 1 or ka.k_syn != kb.k_syn):
            probs.append("implicit complement: one implicit cue, no syntactic one")
        if neg.complement_kind in ("antonym", "option_framing") and ka.k_all != kb.k_all:
            probs.append(f"{neg.complement_kind} complement adds a negation cue")
        if probs:
            raise GTWError("complement: " + "; ".join(probs))
        pid = self._link(ra, rb, "complement", "complement")
        self.edges.append((ra.row["id"], pid, "complement"))

    def twin(self, ra, rb, spec_a: Spec, spec_b: Spec, changed_slot: str, predicted):
        diff = slot_diff(spec_a, spec_b)
        probs = []
        if diff != {changed_slot}:
            probs.append(f"slot diff {sorted(diff)} != [{changed_slot}]")
        ga, gb = self.plugin.solve_a(spec_a), self.plugin.solve_a(spec_b)
        if gb != predicted:
            probs.append(f"gold {gb!r} != predicted {predicted!r}")
        if ga == gb:
            probs.append("gold does not flip")
        if ra.answer != ga or rb.answer != gb:
            probs.append("row gold differs from solver A")
        probs += twin_text_problems(ra, rb, affected(spec_b, {changed_slot}))
        if probs:
            raise GTWError("twin: " + "; ".join(probs))
        self._link(ra, rb, "minimal_edit", "twin")

    def premise_removal(self, ra, rb, spec_a: Spec, spec_b: Spec, removed_slot: str, abstain_key):
        diff = slot_diff(spec_a, spec_b)
        probs = []
        if diff != {removed_slot} or removed_slot in spec_b.slots:
            probs.append(f"premise removal must drop exactly {removed_slot}")
        if self.plugin.solve_a(spec_b) != abstain_key or rb.answer != abstain_key:
            probs.append("gold is not the abstain key")
        if probs:
            raise GTWError("premise removal: " + "; ".join(probs))
        self._link(ra, rb, "premise_removal", "premise_removal")

    def equiv(self, ra, rb, spec_a: Spec, spec_b: Spec):
        probs = []
        if self.plugin.canonical(spec_a) != self.plugin.canonical(spec_b):
            probs.append("facts differ")
        if ra.answer != rb.answer or ra.row["qtype"] != rb.row["qtype"]:
            probs.append("gold or qtype differs")
        if ra.row["qtype"] == "choice" and sorted(ra.row["options"]) != sorted(rb.row["options"]):
            probs.append("option sets differ")
        if ra.skin_id == rb.skin_id and ra.register == rb.register:
            probs.append("equiv partner uses the same skin and register")
        if probs:
            raise GTWError("equiv: " + "; ".join(probs))
        pid = self._link(ra, rb, "equiv", "equiv")
        self.edges.append((ra.row["id"], pid, "equiv"))

    def inv(self, ra, rb, spec: Spec):
        probs = []
        if not rb.attack_id or ra.attack_id:
            probs.append("inv partner carries exactly one attack line, the clean row none")
        if ra.answer != rb.answer:
            probs.append("attack changed the gold")
        if ra.skin_id != rb.skin_id or ra.wording_id != rb.wording_id:
            probs.append("attack twin changes the skin or wording")
        if ra.row["qtype"] == "choice" and ra.row["options"] != rb.row["options"]:
            probs.append("attack twin changes the options")
        if probs:
            raise GTWError("inv: " + "; ".join(probs))
        pid = self._link(ra, rb, "attack", "attack")
        self.edges.append((ra.row["id"], pid, "inv"))

    # ---------------------------------------------------------------------------------------- finalize
    def finalize(self) -> tuple:
        parent = {rid: rid for rid in self.order}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for a, b, _ in self.edges:
            parent[find(a)] = find(b)
        units: dict = {}
        for rid in self.order:
            units.setdefault(find(rid), []).append(rid)
        src = self.rows[self.root].row["source"] if self.root else None
        group = self.rows[self.root].row["group_id"] if self.root else None
        out = []
        for members in units.values():
            if len(members) > MAX_UNIT:
                raise GTWError(f"relation unit of {len(members)} rows (max {MAX_UNIT})")
            cid = f"{src}:{sha('|'.join(sorted(members)))[:12]}"
            for rid in members:
                rr = self.rows[rid]
                rr.row["call_id"] = cid
                rr.row["group_id"] = group
        for rid in self.order:
            rr = self.rows[rid]
            if rid in self.links:
                base, kind, role = self.links[rid]
                rr.row["role"] = role
                for m in (rr.row["meta"], rr.row["meta"]["c2"]):
                    m["twin_of"], m["twin_kind"] = base, kind
            out.append(rr.row)
        rels = [{"a": a, "b": b, "type": t} for a, b, t in self.edges]
        return out, rels
