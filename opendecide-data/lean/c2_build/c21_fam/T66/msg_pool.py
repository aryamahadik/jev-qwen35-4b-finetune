"""T66 MSG production commit-message pool: file format, the dev / holdout split, normalisation and the overlay onto the wording pool.

pools/msg_messages.json (built from msg_pool_src.py):
  {"version": 1, "family": "T66", "head": "MSG", "test_only": false, "split_seed": ..., "kinds": {KIND: {"templates": [{"id", "text", "style": "I"|"N", "split": "dev"|"dev2"|"holdout"}]}}}
KIND = CH-1 .. CH-10 (realised ones) or fmt / comment / doc (the trivial hunk kinds). Style I names the function / values of the change ({fn} ...), style N is identifier-free.

SPLIT (fixed, seeded hash): inside every (kind, style) the templates are ranked by sha256(SPLIT_SEED | kind | normalised text); even ranks are "dev", odd ranks "dev2". The halves are
therefore balanced per (kind, style) and a template's half does not depend on where it stands in the source. The first holdout run (Sun 18 Oct) was spent on the old "holdout" half, which is now
dev material and is called "dev2"; the label "holdout" is reserved for a freshly written half (a separate file in this format, `--msg-pool`, templates labelled "holdout").

Use:  Ctx(..., msg_split="dev" | "dev2" | "holdout" | "all")  (generator.py)  or  wording_pool(base_pool, "dev")  for a pool file in the wording-pool format (what the agreement harness takes).
"""
import copy
import hashlib
import json
import os
import re

from . import msg_spec as MSG

FAMDIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATH = os.path.join(FAMDIR, "pools", "msg_messages.json")
SPLIT_SEED = "T66-MSG-split-v1"
# sha256 of the shipped pool file; being an UPPER_CASE constant it lands in the HASH_EXPORT tables (the export covers wording_pool.json only), so a changed message pool = a new export
MSG_POOL_SHA256 = hashlib.sha256(open(DEFAULT_PATH, "rb").read()).hexdigest() if os.path.exists(DEFAULT_PATH) else None
SPLITS = ("dev", "dev2", "holdout", "all")             # dev / dev2: the two hash halves of this file (both are dev material now); holdout: reserved for a freshly written half
KINDS = tuple(MSG.CH_REALISED) + tuple(MSG.TRIV_IDS)
STYLES = ("I", "N")
_PREFIX = re.compile(r"^[a-z]+(\([^)]*\))?!?:\s*")
_PUNCT = re.compile(r"[\"'`,.;:!?()\[\]]")


def form_of_kind(kind, style):
    """The wording-pool form a kind / style lives in (the generator's picker works on these)."""
    return MSG.form_of(kind, style) if kind in MSG.CH_REALISED else "T66-M-TRIV-%s" % kind


def norm_text(text):
    """Normalised template text: lower case, conventional-commit prefix (fix:, feat(x):, ...) removed, whitespace collapsed, trailing punctuation removed. Slots are kept as {name}."""
    t = " ".join(text.lower().split())
    t = _PREFIX.sub("", t)
    return t.rstrip(" .!;")


def tokens_of(text):
    """Tokens for the cross-kind similarity check: lower case, punctuation stripped, slots kept as {name}; the prefix words (fix, feat ...) are KEPT (conservative)."""
    t = _PUNCT.sub(" ", " ".join(text.lower().split()).replace("{", "\x00").replace("}", "\x01"))
    t = t.replace("\x00", "{").replace("\x01", "}")
    return set(w for w in t.split() if w)


def jaccard(a, b):
    ta, tb = tokens_of(a), tokens_of(b)
    return len(ta & tb) / float(len(ta | tb)) if ta | tb else 1.0


def split_ranks(kind, texts):
    """-> {text: "dev" | "dev2"} for the templates of one (kind, style): rank by hash, even rank dev, odd rank dev2."""
    keyed = sorted(texts, key=lambda t: hashlib.sha256(("%s|%s|%s" % (SPLIT_SEED, kind, norm_text(t))).encode("utf-8")).hexdigest())
    return {t: ("dev" if i % 2 == 0 else "dev2") for i, t in enumerate(keyed)}


def build_doc(parsed):
    """parsed: {kind: {style: [text]}} (msg_pool_src.parse) -> the JSON document."""
    kinds = {}
    for kind in KINDS:
        tpls = []
        for style in STYLES:
            texts = parsed[kind][style]
            sp = split_ranks(kind, texts)
            for i, t in enumerate(texts):
                tpls.append({"id": "%s-%s-%02d" % (kind, style, i + 1), "text": t, "style": style, "split": sp[t]})
        kinds[kind] = {"name": MSG.CH_NAMES.get(kind, "trivial hunk: " + kind), "slots": list(MSG.KIND_SLOTS[kind]), "templates": tpls}
    return {"version": 1, "family": "T66", "head": "MSG", "test_only": False, "split_seed": SPLIT_SEED,
            "note": "Claude-authored commit messages for the T66 MSG head (production pool, one section per change kind and per trivial hunk kind). Style I names the changed function / values, style N is "
                    "identifier-free intent. dev / dev2 halves are fixed by a seeded hash (msg_pool.split_ranks); a half labelled holdout is written separately and run against Solver B once.",
            "kinds": kinds}


def dump(doc, f):
    json.dump(doc, f, indent=1, ensure_ascii=True)
    f.write("\n")


def load(path=None):
    with open(path or DEFAULT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def templates(doc, split="all"):
    """-> {kind: {style: [template dict]}} restricted to the half (all = every template of the file)."""
    if split not in SPLITS:
        raise ValueError("split must be one of %s" % (SPLITS,))
    out = {}
    for kind, body in doc["kinds"].items():
        for t in body["templates"]:
            if split == "all" or t["split"] == split:
                out.setdefault(kind, {}).setdefault(t["style"], []).append(t)
    return out


def forms_of(doc, split="all"):
    """-> {form id: [{"id", "text"}]} for the generator's picker (T66-M-CH-1-I ..., T66-M-TRIV-fmt)."""
    forms = {}
    for kind, by_style in templates(doc, split).items():
        for style, ts in by_style.items():
            f = form_of_kind(kind, style)
            forms.setdefault(f, []).extend({"id": t["id"], "text": t["text"]} for t in ts)
    return forms


def wording_pool(base_pool, msg_doc, split="all"):
    """The base wording pool (question frames of MERGE / SEMVER / MSG) with the 19 MSG change forms REPLACED by the commit-message templates of the chosen half."""
    forms_new = forms_of(msg_doc, split)
    missing = [f for f in MSG.FORMS_MSG if not forms_new.get(f)]
    if missing:
        raise ValueError("the message pool has no templates for %d MSG forms in split %r (first: %s)" % (len(missing), split, missing[0]))
    pool = copy.deepcopy(base_pool)
    for f in MSG.FORMS_MSG:
        pool["forms"].pop(f, None)
    pool["forms"].update(forms_new)
    pool["msg_split"] = split
    return pool


def main(argv=None):
    """CLI: write the wording-pool-format file of one half (what solver_b/agree.py --msg-pool takes).
    python3 -m T66.msg_pool --split dev|holdout|all --out PATH   (run from c21_fam/)"""
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="dev", choices=SPLITS)
    ap.add_argument("--out", required=True)
    ap.add_argument("--msg-pool", default=None, help="message pool file (default pools/msg_messages.json)")
    a = ap.parse_args(argv)
    with open(os.path.join(FAMDIR, "pools", "wording_pool.json"), "r", encoding="utf-8") as f:
        base = json.load(f)
    pool = wording_pool(base, load(a.msg_pool), a.split)
    with open(a.out, "w", encoding="utf-8") as f:
        dump(pool, f)
    print("wrote %s (split %s): %s" % (a.out, a.split, {k: len(v) for k, v in pool["forms"].items() if k.startswith("T66-M-")}))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
