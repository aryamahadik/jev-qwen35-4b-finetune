"""Row assembly for T57: carriers, prompt text, names, metadata and probe features. Wording comes from the pools:
question forms T57-Q-* (>= 50 each), the task-card frame T57-TC-FRAME, comment pools T57-CM-NEUTRAL / T57-CM-FIXED.
Hidden-suite content never enters a rendered row (except the TESTSEL options, by design)."""
import difflib
import re

from LC_COMMON import codeview as V
from LC_COMMON import ir as I
from LC_COMMON import render as R
from LC_COMMON import tokens

from . import config as C
from . import facts as F
from .base import FAMILY, COMMENT_PREFIX, insert_comment, diff_text, files_of
from LC_COMMON.names_guard import default_guard

LETTERS = "ABCD"
FORM_SLOTS = {"T57-Q-VERDICT": ["ask", "lang"], "T57-Q-BEST4": ["ask", "lang"], "T57-Q-TESTSEL": ["ask", "lang"],
              "T57-Q-LOCALISE": ["ask", "lang"], "T57-Q-VERDICT-REASON": ["ask", "lang"],
              "T57-TC-FRAME": ["facts"], "T57-CM-NEUTRAL": ["name"], "T57-CM-FIXED": ["name"]}
ALL_FORMS = list(FORM_SLOTS)
LANG_NAME = {"python": "Python", "javascript": "JavaScript", "typescript": "TypeScript", "go": "Go", "bash": "bash"}
DEFAULT_ASK = {"VERDICT": "Does the patch make the failing test pass without breaking the tests that pass?",
               "BEST4": "Which patch correctly fixes the bug?", "TESTSEL": "Which test detects the fix?",
               "LOCALISE": "Which function contains the bug?",
               "REASON": "Why is the patch incorrect?"}
REASON_OPTIONS = ["PARTIAL", "REGRESSION", "NOFIX"]
_IDENT = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")


def shown_source(task, spec):
    """Source blocks the model sees: whole files, restricted to the files that matter for the question (the bug function's
    file, the files of the visible test's call closure and of every shown patch); LOCALISE shows the whole module."""
    lo, lang = task["buggy_lo"], task["lang"]
    fns = I.functions(lo)
    if spec["head"] == "LOCALISE":
        need = set(range(len(lo["files"])))
    else:
        need = {fns[task["bug_fn"]]["file"]}
        if spec["head"] == "TESTSEL":
            # the visible test is not shown; the model judges the four OPTION tests, so every function they call (and what
            # those call) must be in the shown source, or the question cannot be answered from the row (build-review fix 18 Oct)
            hidden = {c["name"]: c for c in task["hidden"]["cases"]}
            roots = [st["fn"] for n in (spec.get("options") or []) for st in hidden[n]["steps"]]
        else:
            roots = [s["fn"] for s in task["visible"]["steps"]]
        stack, seen = list(roots), set()
        while stack:
            n = stack.pop()
            if n in seen or n not in fns:
                continue
            seen.add(n)
            need.add(fns[n]["file"])
            stack += [x[1] for _, x in I.walk(fns[n]["body"]) if x[0] in ("fcall", "mcall")]
        for c in spec["cands"]:
            for path in c["files"]:
                stem = path.rsplit(".", 1)[0]
                if stem in lo["files"]:
                    if c["files"][path] != files_of(lo, lang).get(path):
                        need.add(lo["files"].index(stem))
    blocks = [b for b in V.src_blocks(lo, lang) if b["path"] in ("go.mod",) or b["path"].rsplit(".", 1)[0] in {lo["files"][k] for k in need}]
    shown = [f["name"] for f in lo["funcs"] if f["file"] in need]
    return blocks, shown


def comment_text(picker, kind, name):
    """kind 'neutral' | 'fixed' -> text of a one-line source comment from the pool."""
    form = "T57-CM-FIXED" if kind == "fixed" else "T57-CM-NEUTRAL"
    wid, text = picker.render(form, name=name)
    return wid, text.replace("\n", " ")


def with_comment(task, cand, text, lang):
    """Candidate copy whose patched tree carries a one-line comment above the first changed line."""
    before = files_of(task["buggy_lo"], lang)
    new_files, line = insert_comment(cand["files"], before, lang, text)
    dtext, changed, hunks, nf = diff_text(before, new_files)
    c = dict(cand)
    c.update({"files": new_files, "diff": dtext, "changed": changed, "hunks": hunks, "n_files": nf, "comment": text,
              "comment_line": line})
    return c


def style_feats(cand):
    """Style-only features of one patch (K5-K9): length, lines, hunks, comment ratio, identifier statistics."""
    lines = cand["diff"].splitlines()
    add = [x[1:] for x in lines if x.startswith("+") and not x.startswith("+++")]
    rem = [x[1:] for x in lines if x.startswith("-") and not x.startswith("---")]
    idents = _IDENT.findall("\n".join(add))
    comment_lines = sum(1 for x in add if x.strip().startswith(("#", "//")))
    return {"chars": len(cand["diff"]), "lines": len(lines), "added": len(add), "removed": len(rem), "hunks": cand["hunks"],
            "files": cand["n_files"], "comment_lines": comment_lines, "comment_ratio": comment_lines / max(1, len(add)),
            "n_idents": len(idents), "mean_ident_len": (sum(map(len, idents)) / len(idents)) if idents else 0.0,
            "digits": sum(ch.isdigit() for ch in "\n".join(add)), "has_comment": 1.0 if cand.get("comment") else 0.0}


def medoid_feature(cands):
    """Mean edit distance (1 - ratio) of each option's diff to the other options' diffs."""
    out = []
    for i, c in enumerate(cands):
        others = [d for j, d in enumerate(cands) if j != i]
        out.append(sum(1 - difflib.SequenceMatcher(None, c["diff"], o["diff"]).ratio() for o in others) / max(1, len(others)))
    return out


def row_names(head, lang, carriers):
    runners = [C.RUNNER[lang], "runner.domain_enumerator." + lang]
    names = {"policy": [C.DEFS_CARD["VERDICT" if head == "REASON" else head]], "tool": [], "language": [lang],
             "runner": sorted(set(runners)), "carrier": sorted(carriers)}
    default_guard().assert_ok(FAMILY, names)
    return names


def build_row(spec, picker, row_id, label, manifest, variant="primary", visible_result=None, reason_head=False):
    head, task = spec["head"], spec["task"]
    lang = task["lang"]
    form = C.QUESTION_FORM[head] if not reason_head else "T57-Q-VERDICT-REASON"
    wid, question = picker.render(form, ask=DEFAULT_ASK["REASON" if reason_head else head], lang=LANG_NAME[lang])
    blocks, shown_fns = shown_source(task, spec)
    fids, frame = picker.render("T57-TC-FRAME", facts="\n".join(F.facts_for(task["buggy_lo"], shown_fns)))
    carriers, parts = {}, [frame]
    carriers["TASK_CARD"] = {"frame_wording": fids, "text": frame}
    carriers["SRC_FILE"] = blocks
    parts.append(V.src_text(blocks))
    if head != "TESTSEL":
        vpath, vtext = R.render_tests(task["ref_lo"], lang, {"cases": [task["visible"]]}, task["ids"].module_stem("vt"))
        carriers["VISIBLE_TEST"] = {"path": vpath, "text": vtext}
        parts.append("### %s\n%s" % (vpath, vtext))
    comments = []
    if head in ("VERDICT", "TESTSEL"):
        c = spec["cands"][0]
        carriers["PATCH_DIFF"] = c["diff"]
        parts.append(c["diff"])
        if c.get("comment"):
            comments.append(c["comment_line"])
    elif head == "BEST4":
        carriers["PATCH_DIFF"] = [{"option": LETTERS[i], "diff": c["diff"]} for i, c in enumerate(spec["cands"])]
        for i, c in enumerate(spec["cands"]):
            parts.append("Patch %s:\n%s" % (LETTERS[i], c["diff"]))
            if c.get("comment"):
                comments.append(c["comment_line"])
        carriers["OPTIONS"] = ["%s" % LETTERS[i] for i in range(4)]
    if head == "TESTSEL":
        opts = ["%s.\n%s" % (LETTERS[i], b) for i, b in enumerate(spec["test_blocks"])]
        carriers["OPTIONS"] = opts
        parts.append("\n".join(opts))
    elif head == "LOCALISE":
        opts = ["%s. %s" % (LETTERS[i], n) for i, n in enumerate(spec["options"])]
        carriers["OPTIONS"] = opts
        parts.append("\n".join(opts))
    elif reason_head:
        carriers["OPTIONS"] = ["%s. %s" % (LETTERS[i], n) for i, n in enumerate(spec["reason_options"])]
        parts.append("\n".join(carriers["OPTIONS"]))
    if comments:
        carriers["COMMENT_DECOY"] = comments
    if visible_result is not None:
        carriers["VISIBLE_RESULT"] = visible_result
        parts.append(visible_result)
    carriers["QUESTION_FORM"] = {"form": form, "wording_id": wid, "text": question}
    parts.append(question)
    prompt = "\n\n".join(parts)
    cands = spec["cands"]
    meta = {
        "head": head, "lang": lang, "module_id": task["id"], "base_module": task["id"], "task_uid": task["uid"],
        "norm_hash": I.norm_hash(task["buggy_lo"]), "tokens": tokens.count(prompt), "wording_id": wid, "form": form,
        "variant": variant, "reason_head": reason_head, "layout": "PENDING_L0_MAPPING", "cdom": task["cdom"],
        "bug_fn": task["bug_fn"], "bug_op": (task["site"].get("sites") or [task["site"]])[0]["op"], "multi": task["multi"],
        "n_files": len(task["buggy_lo"]["files"]), "twin_of": spec.get("twin_of"), "pair_id": spec.get("pair_id"),
        "pair_kind": spec.get("pair_kind"), "ir": I.size_metrics(task["buggy_lo"]),
        "cands": [{"kind": c["kind"], "cls_exec": (manifest.get("cand_classes") or [None] * len(cands))[k],
                   "style": style_feats(c), "comment_kind": c.get("comment_kind"), "decoy": bool(c.get("decoy"))}
                  for k, c in enumerate(cands)],
        "medoid": medoid_feature(cands) if len(cands) > 1 else None,
        "options": spec.get("options"), "opt_roles": spec.get("opt_roles"), "opt_flags": spec.get("opt_flags"),
        "gold_index": spec.get("gold_index"),
        "altfix": spec.get("altfix"), "src_lines": sum(b["text"].count("\n") for b in blocks),
        "task_chars": len(frame), "slots": {"ask": DEFAULT_ASK["REASON" if reason_head else head], "lang": LANG_NAME[lang]},
    }
    names = row_names(head, lang, set(carriers) - {"QUESTION_FORM"})
    row = {"row_id": row_id, "family": FAMILY, "head": ("REASON" if reason_head else head), "lang": lang, "label": label,
           "question_form": form, "wording_id": wid, "carriers": carriers, "prompt_text": prompt, "names": names,
           "b_inputs": {"task_uid": task["uid"], "candidate_files": [c["files"] for c in cands], "options": spec.get("options"),
                        "visible_case": task["visible"]["name"]},
           "meta": meta, "manifest": manifest}
    return row
