"""T63 record assembly: carriers, question wording (from a wording pool), lettered options, names, metadata, witness inputs.

Record keys follow the L-P pipeline (LP_COMMON/pipeline.py): row_id, family, head, sub_block, group_id, gold (= label), gold_letter,
options [{letter, label, text}], rendered {context, question, options_text, text}, slots, names, carriers, witness_inputs, meta, manifest.
The rendered text is the only thing a model sees; meta and manifest are generator-side (A1 / A2 hooks: template_id, wording_id, construction_id).
"""
import hashlib

from LP_COMMON import plan as plan_mod
from LP_COMMON import tokens, util

from . import config as C
from . import lic_format as LF
from . import render as R

LANG_OF_ECO = {"pip": "python", "npm": "javascript", "cargo": None, "go": "go"}
TEMPLATE_ID = {"NEAR": "t63.near.v1", "EXISTS": "t63.exists.v1", "LIC": C.LIC_TEMPLATE_ID}


def split_of(gid):
    base = gid.split("~r")[0]
    return "dev" if int(hashlib.sha256(("T63-split|" + base).encode()).hexdigest(), 16) % 10 == 0 else "train"


def row_names(spec, fmt=None):
    head = spec["head"]
    names = {"policy": list(C.POLICY[head]), "tool": [], "language": [], "runner": [], "carrier": list(C.CARRIERS[head])}
    if head == "NEAR":
        q = spec["query"]
        eco = next(r for r in spec["registries"] if r["id"] == q["registry"])["eco"]
        names["tool"] = [C.ECO_PROG[eco]]
        if LANG_OF_ECO[eco]:
            names["language"].append(LANG_OF_ECO[eco])
        names["carrier"].append(fmt)
        if fmt == "TBL-JSON":
            names["language"].append("json")
    elif head == "EXISTS":
        sub = spec["sub"]
        names["carrier"].append({"EX-A1": "REGISTRY_INDEX", "EX-A2": "LIB_EXPORTS", "EX-B1": "MODULE_EXPORTS"}.get(sub, "QUESTION_FORM"))
        if sub in ("EX-B1", "EX-B2"):
            lang = spec["lang"]
            names["language"].append({"python": "python", "node": "javascript", "go": "go"}[lang])
            names["runner"].append("runner.stdlib_export." + lang)
    names["carrier"] = sorted(set(names["carrier"]))
    for k in names:
        names[k] = sorted(set(names[k]))
    return names


def _options(labels, gold, rng):
    order = util.place_gold(list(labels), gold, rng.randrange(len(labels)), rng)
    return [{"letter": util.LETTERS[i], "label": lab, "text": lab} for i, lab in enumerate(order)]


def build_record(ctx, g, spec, member, construction_id, fmt=None, pair_id=None, twin_of=None, extra_meta=None, lic_index=None):
    head = spec["head"]
    form = C.QUESTION_FORM[head]
    rng = ctx.rng("rec", g["gid"], member)
    if head == "NEAR":
        context = R.render_near_context(spec, fmt)
        reg = next(r for r in spec["registries"] if r["id"] == spec["query"]["registry"])
        slots = {"pkg": spec["query"]["name"], "registry": "%s (%s)" % (reg["id"], reg["host"])}
        labels = ["YES", "NO"]
        sub = "NEAR"
    elif head == "EXISTS":
        context = R.render_exists_context(spec)
        sub = spec["sub"]
        if sub == "EX-A1":
            slots = {"name": spec["query_name"], "scope": "%s (%s)" % (spec["registry"]["id"], spec["registry"]["host"])}
        elif sub == "EX-A2":
            slots = {"name": "%s.%s" % (spec["query_module"], spec["query_symbol"]), "scope": "%s version %s" % (spec["library"], spec["version"])}
        else:
            slots = {"name": spec["query_name"], "scope": "%s module %s in the pinned toolchain image" % (R.LANG_WORD[spec["lang"]], spec["module"])}
        labels = ["YES", "NO"]
    else:
        context = R.render_lic_context(spec)
        slots = {"dep": spec["dep"], "project": spec["project"]}
        labels = list(C.LIC_LABELS)
        sub = "LIC"
    gold = spec["label"]
    lic_fmt = None
    if head == "LIC":
        # K10-F (Opus ruling Q7b): every LIC format choice (wording id, option order, template id, card layout, field order) is `lic_format.draw(seed, row index)`: it takes no label
        # and no licence cell, so the format cannot depend on them, and the row replays it from the (seed, index) recorded in meta.lic_format
        ws = ctx.pool["forms"][form]
        lic_fmt = LF.draw(ctx.seed, lic_index, len(ws), C.LIC_LABELS)
        wid, question = ws[lic_fmt["word_index"]]["id"], ws[lic_fmt["word_index"]]["text"].format(**slots)
        options = [{"letter": util.LETTERS[i], "label": lab, "text": lab} for i, lab in enumerate(lic_fmt["option_order"])]
    else:
        wid, question = ctx.picker.render(form, **slots)
        options = _options(labels, gold, rng)
    options_text = "\n".join("%s) %s" % (o["letter"], o["text"]) for o in options)
    text = "\n\n".join([context, question, options_text])
    rec = {
        "row_id": "%s-%s" % (g["gid"], "abcd"[member]), "family": C.FAMILY, "head": head, "sub_block": sub, "group_id": g["gid"],
        "gold": gold, "label": gold, "gold_letter": next(o["letter"] for o in options if o["label"] == gold), "options": options,
        "question_form": form, "slots": slots, "rendered": {"context": context, "question": question, "options_text": options_text, "text": text},
        "names": row_names(spec, fmt), "spec": spec,
        "witness_inputs": witness_inputs(spec, fmt),
        "meta": {"template_id": TEMPLATE_ID[head], "wording_id": wid, "construction_id": construction_id, "ladder": spec["level"],
                 "tokens": tokens.count(text), "split": split_of(g["gid"]), "pair_id": pair_id, "twin_of": twin_of, "fmt": fmt,
                 "reuse_group": g["gid"].split("~r")[0], "mech": spec.get("mech"), "sub_block": sub},
        "manifest": {"gold_method": "program", "solver_a_version": "t63.solver_a.v1", "pins": pins_of(spec)},
    }
    if lic_fmt is not None:
        rec["meta"]["lic_format"] = {"seed": ctx.seed, "index": lic_index, "n_wordings": len(ctx.pool["forms"][form]), "word_index": lic_fmt["word_index"]}
    if extra_meta:
        rec["meta"].update(extra_meta)
    return rec


def pins_of(spec):
    """Provenance of the toolchain behind the gold: only EXISTS-B rows depend on a pinned image (the stdlib export); every other T63 row is a program over its own spec."""
    if spec["head"] == "EXISTS" and spec["sub"] in ("EX-B1", "EX-B2"):
        return "image:%s;export:%s" % (spec.get("image_id"), spec.get("export_sha"))
    return "n/a:no_toolchain"


def witness_inputs(spec, fmt):
    head = spec["head"]
    if head == "NEAR":
        return {"head": "NEAR", "fmt": fmt}
    if head == "EXISTS":
        w = {"head": "EXISTS", "sub": spec["sub"]}
        if spec["sub"] in ("EX-B1", "EX-B2"):
            w.update(lang=spec["lang"], module=spec["module"], name=spec["query_name"], export_sha=spec["export_sha"])
        return w
    return {"head": "LIC", "table_sha": spec.get("table_sha")}
