"""T67 record assembly: rendered context, question wording, lettered options (ALLOW / ASK / BLOCK shuffled per row), G10 decision spans, names,
metadata, head rows (reason, tier). Record keys follow the L-P pipeline (LP_COMMON/pipeline.py)."""
import hashlib
import re

from LP_COMMON import plan as plan_mod
from LP_COMMON import tokens, util

from . import config as C
from . import engine, render as R, userturn as UT

LABEL_TEXT = {"ALLOW": "ALLOW: run it as proposed", "ASK": "ASK: ask the user first", "BLOCK": "BLOCK: do not run it"}
REASON_TEXT = {r: r for r in C.REASONS}
TIER_TEXT = {"soft": "soft: the user can clear it by naming the operation and the target", "hard": "hard: the user cannot clear it", "na": "na: no consent is involved"}
TEMPLATE_ID = {"PLAN_JSON": "t67.plan.v1", "K8S_MANIFEST": "t67.k8s.v1", "CI_WORKFLOW": "t67.ci.v1", "MIGRATION_SQL": "t67.sql.v1"}
ASK_SLOT = {"GATE": "the host runs the change as proposed", "REASON": "the reason class of the decision", "TIER": "the consent tier of the decision"}


def split_of(spec_family, dev_only=False):
    if dev_only:
        return "dev"                                  # the held-out-operator slice is dev-only: never trained (T67-B9, GV9)
    base = spec_family.split("~r")[0]
    return "dev" if int(hashlib.sha256(("T67-split|" + base).encode()).hexdigest(), 16) % 10 == 0 else "train"


def spec_level(spec, lock_table=None):
    """Ladder level from the mechanism flags: M-HIDE, M-REPL, M-INDIR, M-SIZE, M-FORM and M-LANE (a flag only when the lane / environment decides:
    LOW = named in the user turn, HIGH = only in the card's lists)."""
    m = spec["mech"]
    flags = [m.get("hide"), m.get("repl"), m.get("indir"), m.get("size"), m.get("form")]
    lane_matters = spec["carrier"] == "MIGRATION_SQL"
    if not lane_matters and spec["carrier"] != "CI_WORKFLOW":
        res = engine.evaluate(dict(spec, naming={"ops": set(), "targets": set()}), lock_table)
        lane_matters = any(mm.rule in ("X02", "X03") and mm.label != "ALLOW" for mm in res.members)
    if lane_matters:
        flags.append("low" if m.get("lane_named") else "high")
    low = sum(1 for f in flags if f == "low")
    high = sum(1 for f in flags if f == "high")
    return plan_mod.ladder_level(low, high)


def names_of(spec):
    c = spec["carrier"]
    names = {"policy": [spec["card"]["card_id"], "defs_card.t67.migration" if c == "MIGRATION_SQL" else "defs_card.t67.iac"], "tool": [], "language": list(C.LANG_OF[c]),
             "runner": [], "carrier": [c, "carrier.user_turn", "QUESTION_FORM", "OPTIONS"]}
    if C.PROG_OF[c]:
        names["tool"].append(C.PROG_OF[c])
    if C.FMT_OF[c]:
        names["carrier"].append(C.FMT_OF[c])
    if c != "MIGRATION_SQL":
        names["carrier"].append("SESSION_NOTES")
    else:
        names["carrier"].append("TABLE_STATS_CARD")
    for k in names:
        names[k] = sorted(set(names[k]))
    return names


def _spans(text, spec, decisive, slots):
    spans = []
    ut_start = text.find("User: ")
    ut_end = text.find("\n\n", ut_start) if ut_start >= 0 else -1
    region = text[ut_start:ut_end] if ut_start >= 0 else ""
    taken = []

    def add(a, b, role):
        if all(b <= x or a >= y for x, y, _r in taken):
            taken.append((a, b, role))
    for key in ("op_word", "target"):
        v = slots.get(key)
        if v:
            k = region.find(v)
            if k >= 0:
                add(ut_start + k, ut_start + k + len(v), "authority")
    for it in spec.get("items", ()):
        for m in re.finditer(re.escape(it["address"]), text):
            add(m.start(), m.end(), "entity_path_flag")
    for pat, role in ((r"\b(?:0\.0\.0\.0/0|::/0)", "entity_path_flag"), (r"\"port\": \"?\d{2,5}", "number"), (r"\bapproximate rows: [\d,]+", "number"),
                      (r"\bport: \d{2,5}", "number")):
        for m in re.finditer(pat, text):
            add(m.start(), m.end(), role)
    if not taken:
        m = re.search(r"Proposed (?:call|write): [^\n]+", text)
        add(m.start(), m.end(), "entity_path_flag")
    taken.sort()
    return {"spans": [{"start": a, "end": b, "text": text[a:b], "role": r} for a, b, r in taken]}


def _options(labels, texts, gold, rng):
    order = util.place_gold(list(labels), gold, rng.randrange(len(labels)), rng)
    return [{"letter": util.LETTERS[i], "label": lab, "text": texts[lab]} for i, lab in enumerate(order)]


def build_record(ctx, g, spec, member, cell, decisive, style, pair_id=None, twin_of=None, group_kind="single", head="GATE", construction_id=None, extra_meta=None):
    rng = ctx.rng("t67rec", g["gid"], member, head)
    form = C.QUESTION_FORMS[head]
    ut_text, ut_wid, naming, slots, cell = UT.make_turn(ctx.picker, cell, decisive)
    spec = dict(spec, user_turn={"cell": cell, "op": decisive["op"] if decisive else None, "target": decisive["target"] if decisive else None,
                                 "lane_named": spec["mech"].get("lane_named")}, naming=naming)
    lane_line = ("Environment: %s." % spec["mech"]["lane_named"]) if spec["mech"].get("lane_named") else None
    if spec["carrier"] == "MIGRATION_SQL" and lane_line:
        lane_line = "Environment: %s." % {"contained": "dev"}.get(spec["mech"]["lane_named"], spec["mech"]["lane_named"])
    context, blocks = R.render_context(spec, style, ctx.rng("t67ctx", g["gid"]), ut_text, lane_line)
    # the artifact and the user turn are fixed per (spec, style): the renderer RNG is seeded by the group, so every cell shares the artifact
    gold = engine.gold(spec, ctx.lock_table)
    qw, question = ctx.picker.render(form, ask=ASK_SLOT[head])
    if head == "GATE":
        options = _options(C.LABELS, LABEL_TEXT, gold["label"], rng)
        gold_label = gold["label"]
    elif head == "REASON":
        options = _options(C.REASONS, REASON_TEXT, gold["reason"], rng)
        gold_label = gold["reason"]
    else:
        options = _options(C.TIERS, TIER_TEXT, gold["tier"], rng)
        gold_label = gold["tier"]
    options_text = "\n".join("%s) %s" % (o["letter"], o["text"]) for o in options)
    text = "\n\n".join([context, question, options_text])
    res = engine.evaluate(spec, ctx.lock_table)
    level = spec_level(spec, ctx.lock_table)
    rec = {
        "row_id": "%s-%s-%s" % (g["gid"], "abcd"[member], head[0].lower()), "family": C.FAMILY, "head": "T67-" + head, "sub_block": spec["block"], "group_id": g["gid"],
        "gold": gold_label, "label": gold_label, "gold_letter": next(o["letter"] for o in options if o["label"] == gold_label), "options": options,
        "question_form": form, "slots": dict(slots, **({} if head != "GATE" else {})), "rendered": {"context": context, "question": question, "options_text": options_text, "text": text},
        "names": names_of(spec), "spec": spec, "gold_triple": gold, "decisive": decisive,
        "decision_spans": _spans(text, spec, decisive, slots),
        "witness_inputs": {"carrier": spec["carrier"], "head": head},
        "meta": {"template_id": TEMPLATE_ID[spec["carrier"]], "wording_id": qw, "construction_id": construction_id or ("%s:%s" % (spec["block"], "+".join(res.rules))),
                 "ladder": level, "tokens": tokens.count(text), "split": split_of(g["gid"], bool(style.get("held_out"))), "pair_id": pair_id, "twin_of": twin_of, "group_kind": group_kind,
                 "cell": cell, "user_wording_id": ut_wid, "rules": list(res.rules), "single_trigger": res.single_trigger, "reuse_group": g["gid"].split("~r")[0],
                 "heldout_operator": style.get("held_out"), "dev_only": bool(style.get("held_out")), "head": head, "mech": dict(spec["mech"]), "hard": gold["tier"] == "hard",
                 "sub_block": spec["block"], "spec_id": spec["spec_id"]},
        "manifest": {"gold_method": "rule_table", "rule_table_sha": engine.RULE_TABLE_SHA, "solver_a_version": "t67.engine.v1", "validator": "round_trip_parse_only"},
    }
    if head != "GATE":
        rec["head_row"] = True
    if extra_meta:
        rec["meta"].update(extra_meta)
    rec["slots"] = {k: v for k, v in slots.items()}
    return rec
