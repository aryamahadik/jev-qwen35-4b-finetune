"""Row assembly for T42c: carriers, prompt text, names, metadata. The question wording comes from a wording pool.

Carriers (names on the frozen list): SRC_FILE, CALL_SPEC, PROGRAM_PAIR, DOMAIN_DECL, TEST_FILE, OPTIONS, QUESTION_FORM.
The rendered prompt is carriers joined in a fixed order; the mapping into C2's rendered layout (cygnet +
schema_branch_mark) is L-0's (field mapping pending), so `layout` is recorded as PENDING_L0_MAPPING.
"""
from LC_COMMON import codeview as V
from LC_COMMON import ir as I
from LC_COMMON import tokens

from . import config as C
from .base import row_names

LETTERS = "ABCD"
FORM_SLOTS = {"T42c-Q-OUT4": ["ask", "lang", "result"], "T42c-Q-EQV2": ["ask", "lang", "domain"], "T42c-Q-TFAIL2": ["ask", "lang"]}
LANG_NAME = {"python": "Python", "javascript": "JavaScript", "typescript": "TypeScript", "go": "Go", "bash": "bash"}
DEFAULT_ASK = {"OUT4": "What is the outcome of the final call?",
               "EQV2": "Do the two versions give the same result for every input in the declared domain?",
               "TFAIL2": "Will the test fail?"}


def slots_for(spec):
    lang = spec["lang"]
    s = {"ask": DEFAULT_ASK[spec["head"]], "lang": LANG_NAME[lang]}
    if spec["head"] == "OUT4":
        s["result"] = "RET" if lang == "bash" else "result"
    if spec["head"] == "EQV2":
        s["domain"] = spec["domain_text"]
    return s


def _src_for_out4(spec):
    lo = spec["lo"]
    keep = {c["fn"] for c in spec["calls"]}
    pr = V.prune_module(lo, keep)
    return V.src_blocks(pr, spec["lang"])


def _all_blocks(carriers):
    out = []
    if "SRC_FILE" in carriers:
        out += carriers["SRC_FILE"]
    for p in carriers.get("PROGRAM_PAIR", []):
        out += p["blocks"]
    return out


def build_row(spec, picker, row_id, label, manifest, layout_note="PENDING_L0_MAPPING"):
    head, lang = spec["head"], spec["lang"]
    form = C.QUESTION_FORM[head]
    wid, question = picker.render(form, **slots_for(spec))
    carriers = {}
    parts = []
    if head == "OUT4":
        blocks = _src_for_out4(spec)
        carriers["SRC_FILE"] = blocks
        parts.append(V.src_text(blocks))
        ret_ty = spec["ret_type"]
        carriers["CALL_SPEC"] = V.call_text(spec["lo"], lang, spec["calls"], ret_ty)
        parts.append(carriers["CALL_SPEC"])
        opts = ["%s. %s" % (LETTERS[i], o["text"]) for i, o in enumerate(spec["options"])]
        carriers["OPTIONS"] = opts
        parts.append("\n".join(opts))
    elif head == "EQV2":
        carriers["PROGRAM_PAIR"] = [{"name": p["name"], "blocks": p["blocks"]} for p in spec["shown"]]
        for p in spec["shown"]:
            parts.append("Version %s:\n%s" % (p["name"], p["text"]))
        carriers["DOMAIN_DECL"] = spec["domain_text"]
        parts.append("Domain: " + spec["domain_text"])
    else:
        carriers["SRC_FILE"] = spec["shown"]
        parts.append(spec["src_text"])
        carriers["TEST_FILE"] = {"path": spec["test_path"], "text": spec["test_text"]}
        parts.append("### %s\n%s" % (spec["test_path"], spec["test_text"]))
    carriers["QUESTION_FORM"] = {"form": form, "wording_id": wid, "text": question}
    parts.append(question)
    prompt = "\n\n".join(parts)
    meta = dict(spec["meta"])
    meta.update({
        "head": head, "lang": lang, "module_id": spec["lo"]["id"], "base_module": spec.get("group", spec["lo"]["id"]),
        "norm_hash": I.norm_hash(spec["lo"]), "trace_steps": manifest.get("steps_final"), "trace_bin": manifest.get("bin_final"),
        "trace_bin_planned": spec.get("bin_ir"), "tokens": tokens.count(prompt), "wording_id": wid,
        "form": form, "layout": layout_note, "seed": spec["seed"], "slots": slots_for(spec),
        "ir": I.size_metrics(spec["lo"]), "src_lines": sum(b["text"].count("\n") for b in _all_blocks(carriers)),
    })
    if head == "EQV2":
        meta.update({"domain_size": spec["domain_size"], "domain_text": spec["domain_text"]})
    if head == "OUT4":
        meta.update({"options": [{"text": o["text"], "kind": o["kind"], "obs": o["obs"]} for o in spec["options"]],
                     "gold_index": spec["gold_index"], "ret_type": spec["ret_type"]})
    if head == "OUT4":
        winputs = {"calls": spec["calls"], "mode": "last", "ret_type": spec["ret_type"]}
    elif head == "EQV2":
        tg = spec["target"]
        winputs = {"function": tg["fn"], "mode": tg["mode"], "domain": tg["domain"] if tg["mode"] == "pure" else tg["seq_domain"],
                   "snapshot": tg.get("snapshot")}
    else:
        winputs = {"test_path": spec["test_path"], "stem": spec["stem"]}
    row = {"row_id": row_id, "family": C.FAMILY, "head": head, "lang": lang, "label": label, "question_form": form,
           "wording_id": wid, "carriers": carriers, "prompt_text": prompt, "names": row_names(head, lang),
           "witness_inputs": winputs, "meta": meta, "manifest": manifest}
    return row


def permuted_row(row, rng, new_id, picker=None):
    """Order-invariance copy of an OUT4 row: same content, a random NON-IDENTITY permutation of the options (the gold
    letter changes with it). No new execution is needed; the manifest is shared and marked."""
    import copy
    opts = row["meta"]["options"]
    n = len(opts)
    for _ in range(100):
        perm = list(range(n))
        rng.shuffle(perm)
        if perm != list(range(n)):
            break
    new = copy.deepcopy(row)
    new["row_id"] = new_id
    new_opts = [opts[k] for k in perm]
    gi = [i for i, o in enumerate(new_opts) if o["kind"] == "GOLD"][0]
    new["meta"]["options"] = new_opts
    new["meta"]["gold_index"] = gi
    new["meta"]["perm_copy"] = True
    new["meta"]["perm_of"] = row["row_id"]
    new["meta"]["perm"] = perm
    new["label"] = LETTERS[gi]
    new["carriers"]["OPTIONS"] = ["%s. %s" % (LETTERS[i], o["text"]) for i, o in enumerate(new_opts)]
    old_block = "\n".join(row["carriers"]["OPTIONS"])
    new["prompt_text"] = row["prompt_text"].replace(old_block, "\n".join(new["carriers"]["OPTIONS"]))
    if picker is not None:                       # the copy takes its own wording so no wording exceeds 2% of the family
        wid, question = picker.render(row["question_form"], **row["meta"]["slots"])
        new["prompt_text"] = new["prompt_text"].replace(row["carriers"]["QUESTION_FORM"]["text"], question)
        new["carriers"]["QUESTION_FORM"] = {"form": row["question_form"], "wording_id": wid, "text": question}
        new["wording_id"] = wid
        new["meta"]["wording_id"] = wid
    return new


def reversed_row(row, new_id, picker=None):
    """Order-invariance copy of a binary EQV2 row: the two programs swap places (for 2 options a random non-identity
    permutation IS the reversal). Same label, same witnesses."""
    import copy
    new = copy.deepcopy(row)
    a, b = new["carriers"]["PROGRAM_PAIR"]
    new["carriers"]["PROGRAM_PAIR"] = [{"name": "A", "blocks": b["blocks"]}, {"name": "B", "blocks": a["blocks"]}]
    def txt(p):
        return V.src_text(p["blocks"])
    old = row["carriers"]["PROGRAM_PAIR"]
    old_text = "Version A:\n%s\n\nVersion B:\n%s" % (txt(old[0]), txt(old[1]))
    new_text = "Version A:\n%s\n\nVersion B:\n%s" % (txt(new["carriers"]["PROGRAM_PAIR"][0]), txt(new["carriers"]["PROGRAM_PAIR"][1]))
    new["prompt_text"] = row["prompt_text"].replace(old_text, new_text)
    new["row_id"] = new_id
    new["meta"]["perm_copy"] = True
    new["meta"]["perm_of"] = row["row_id"]
    new["meta"]["perm"] = [1, 0]
    if picker is not None:
        wid, question = picker.render(row["question_form"], **row["meta"]["slots"])
        new["prompt_text"] = new["prompt_text"].replace(row["carriers"]["QUESTION_FORM"]["text"], question)
        new["carriers"]["QUESTION_FORM"] = {"form": row["question_form"], "wording_id": wid, "text": question}
        new["wording_id"] = wid
        new["meta"]["wording_id"] = wid
    return new
