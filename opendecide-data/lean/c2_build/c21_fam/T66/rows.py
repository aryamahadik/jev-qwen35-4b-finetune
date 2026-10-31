"""T66 record assembly (MERGE / SEMVER / MSG): rendered context, question wording, lettered options (two options, shuffled), names, metadata, witness
manifest. Record keys follow the L-P pipeline (LP_COMMON/pipeline.py). The rendered text is all a model sees; spec, meta and manifest are generator-side."""
import hashlib

from LP_COMMON import plan as plan_mod
from LP_COMMON import tokens, util

from . import config as C
from . import semver as SV

TEMPLATE_ID = {"MERGE": "t66.merge.v1", "SEMVER": "t66.semver.v1", "MSG": "t66.msg.v1"}
SLOT_OF = {"MERGE": lambda s: {"stem": s["stem"]}, "SEMVER": lambda s: {"api": s["api"]}, "MSG": lambda s: {"stem": s["stem"]}}


def split_of(module_group):
    base = module_group.split("~r")[0]
    return "dev" if int(hashlib.sha256(("T66-split|" + base).encode()).hexdigest(), 16) % 10 == 0 else "train"


def names_of(spec):
    head = spec["head"]
    car = {"MERGE": ["CONFLICT_VIEW", "RESOLUTION", "SIDE_TEST_A", "SIDE_TEST_B", "QUESTION_FORM"],
           "SEMVER": ["API_PAIR", "CALLER_SNIPPETS", "QUESTION_FORM"] + (["BUMP_FIELD"] if spec.get("bump") else []),
           "MSG": ["DIFF", "COMMIT_MESSAGE", "QUESTION_FORM"]}[head]
    return {"policy": list(C.POLICY[head]), "tool": [], "language": [spec.get("lang", "python")], "runner": ["runner.python_isolated"] if head != "MSG" else [],
            "carrier": sorted(set(car))}


def context_of(spec):
    head = spec["head"]
    if head == "MERGE":
        return "\n\n".join([C.DEFS["MERGE"], "Conflict view of %s.py:\n%s" % (spec["stem"], spec["view"].rstrip("\n")),
                            "Tests of side A (%s):\n%s" % (spec["test_a"]["name"], spec["test_a"]["text"].rstrip("\n")),
                            "Tests of side B (%s):\n%s" % (spec["test_b"]["name"], spec["test_b"]["text"].rstrip("\n")),
                            "Proposed resolution of %s.py:\n%s" % (spec["stem"], spec["resolution"].rstrip("\n"))])
    if head == "SEMVER":
        parts = [C.DEFS["SEMVER"], "Old API (%s.py):\n%s" % (spec["stem"], spec["old"].rstrip("\n")), "New API (%s.py):\n%s" % (spec["stem"], spec["new"].rstrip("\n")),
                 "Callers written against the old API (%s):\n%s" % (spec["callers_name"], spec["callers"].rstrip("\n"))]
        if spec.get("bump"):
            parts.append("Declared version bump: %s" % spec["bump"])
        return "\n\n".join(parts)
    return "\n\n".join([C.DEFS["MSG"], "Diff:\n%s" % spec["diff"].rstrip("\n"), "Commit message: %s" % spec["message"]])


def pins_of(spec):
    """Image the execution witnesses ran on (MERGE / SEMVER); MSG rows are constructed (the hunk probe ran at spec build)."""
    w = spec.get("witness")
    if spec["head"] == "MERGE" and w:
        return "image:%s" % w["A"].get("image")
    if spec["head"] == "SEMVER" and w:
        return "image:%s" % w["new"].get("image")
    return "n/a:construction"


def level_of(spec):
    m = spec.get("mech") or {}
    flags = [v for v in m.values() if v in ("low", "high")]
    return plan_mod.ladder_level(sum(1 for f in flags if f == "low"), sum(1 for f in flags if f == "high"))


def build_record(ctx, g, spec, member, construction_id, pair_id=None, twin_of=None, extra_meta=None):
    head = spec["head"]
    form = C.QUESTION_FORM[head]
    rng = ctx.rng("t66rec", g["gid"], member)
    wid, question = ctx.picker.render(form, **SLOT_OF[head](spec))
    gold = spec["label"]
    labels = list(C.LABELS[head])
    order = util.place_gold(labels, gold, rng.randrange(2), rng)
    options = [{"letter": util.LETTERS[i], "label": lab, "text": lab} for i, lab in enumerate(order)]
    options_text = "\n".join("%s) %s" % (o["letter"], o["text"]) for o in options)
    context = context_of(spec)
    text = "\n\n".join([context, question, options_text])
    level = level_of(spec)
    rec = {"row_id": "%s-%s" % (g["gid"], "abcdefgh"[member]), "family": C.FAMILY, "head": head, "sub_block": head, "group_id": g["gid"], "gold": gold, "label": gold,
           "gold_letter": next(o["letter"] for o in options if o["label"] == gold), "options": options, "question_form": form, "slots": SLOT_OF[head](spec),
           "rendered": {"context": context, "question": question, "options_text": options_text, "text": text}, "names": names_of(spec), "spec": spec,
           "witness_inputs": {"head": head, "lang": spec.get("lang", "python")},
           "meta": {"template_id": TEMPLATE_ID[head], "wording_id": wid, "construction_id": construction_id, "ladder": level, "tokens": tokens.count(text),
                    "split": split_of(spec.get("module_group", g["gid"])), "pair_id": pair_id, "twin_of": twin_of, "reuse_group": spec.get("module_group", g["gid"]).split("~r")[0],
                    "mech": spec.get("mech"), "sub_block": head, "lang": spec.get("lang", "python")},
           "manifest": {"gold_method": "execution" if head != "MSG" else "construction", "solver_a_version": "t66.solver_a.v1", "pins": pins_of(spec),
                        "witness": spec.get("witness"), "strength": spec.get("strength")}}
    if extra_meta:
        rec["meta"].update(extra_meta)
    return rec
