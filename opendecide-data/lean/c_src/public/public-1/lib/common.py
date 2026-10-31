"""public-1 shared code: seeds, ids, page split, golden_train dedupe index, token counts, row construction.

Rows follow C_DATA_SPEC v4 2.4 top-level keys exactly: id, group_id, call_id, source, state, qtype, instructions,
options, gold, role, card, meta. Yes/no rows use the shared raw format's qtype "noul" (gold 1 = yes, 0 = no, options
null); choice rows use qtype "choice" (gold = the option string). Labels are human gold mapped by program only.
"""
from __future__ import annotations

import hashlib
import json
import random
import sys
import urllib.parse
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parents[1]          # c_src/public/public-1
sys.path.insert(0, str(HERE / "lib"))
from textnorm import norm, sent_hashes, h64  # noqa: E402

SEED = 20261003                                      # A16 config seed, reused for every public-1 draw
GEN_VERSION = "public-1 v1.2 (6 Oct 2026; repair round 1, PREREG A29 a)"
SPEC_ID = "C_DATA_SPEC.md v4 3.2"
TMP = HERE / "tmp"
OUT = HERE / "out"
LOGS = HERE / "logs"
OVERHEAD_TOKENS = 160                                # prompt wrapper, option letters, card header (conservative)
MAX_ROW_TOKENS = 7900                                # spec 6 / G15
LONG_TOKENS = 2000


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def rng(*keys) -> random.Random:
    return random.Random(int(sha(f"{SEED}|" + "|".join(map(str, keys)))[:16], 16))


def stable_shuffle(items, *keys):
    items = list(items)
    rng(*keys).shuffle(items)
    return items


def norm_title(t: str) -> str:
    return norm(urllib.parse.unquote(t).replace("_", " "))


def is_dev_page(title: str) -> bool:
    """Spec 3.1: Wikipedia-based sets split train / mix-tuning dev by page title (10%), one rule for every set."""
    return int(sha("c-pub-page:" + norm_title(title))[:8], 16) % 10 == 0


def is_dev_record(dataset: str, key: str) -> bool:
    """Record-level 90/10 split for sets with no page (QuALITY articles, Qasper papers)."""
    return int(sha(f"c-pub-rec:{dataset}:{key}")[:8], 16) % 10 == 0


NEAR_DUP = 0.5                                       # v1.1 review item 3 (kept for the QC report; v1.2 rule below)


class GoldenIndex:
    """C1 golden_train: sentence hashes (>= 8 words, normalised; tmp/golden_index.npz), line hashes (>= 6 words) and
    word 10-gram hashes (tmp/golden_g10.npy). No text.
    v1.2 (repair round 1, A29 a; spec 3.1 v2 'unused records only' and the passage dedup against C1's sources): a
    text (paragraph, article paragraph, question or option) is usable only if
      - its normalised full text, no sentence of >= 8 words and no line of >= 6 words is in golden_train, and
      - it shares NO word 10-gram with golden_train (state, instructions, card and options of every row; a superset of
        the 7 named passage sources qnli, gd_answer_equiv, gd_hotpotqa_yesno, gd_feverous, gd_totto_claims, gd_wtq,
        boolq).
    The v1.1 rule ('>= 50% of a paragraph's 10-grams') let a paragraph that shares a short line or a few 10-grams with
    golden_train through; v1.2 drops any share. v1.2b: Wikipedia paragraphs are also checked in their shown form
    (title line + text): the first v1.2 qc_fix run found 3 MuSiQue paragraphs whose only shared 10-gram crossed the
    title line into the text. post_check() re-checks every rendered row (whole state, instructions, card, options)."""

    def post_check(self, rows) -> int:
        """v1.2b: rows whose rendered text (whole state, instructions, card or any option) fails bad(); count only."""
        n = 0
        for r in rows:
            if self.any_bad([r.get("state"), r.get("instructions"), r.get("card")] + list(r.get("options") or [])):
                n += 1
        return n

    def __init__(self):
        from grams import GramIndex
        z = np.load(TMP / "golden_index.npz")
        self.sent_all = set(z["sent_all"].tolist())
        self.full_all = set(z["full_all"].tolist())
        self.sent_named = set(z["sent_named"].tolist())
        self.line_all = set(z["line_all"].tolist())
        self.g10 = GramIndex(TMP / "golden_g10.npy")
        self._cache = {}

    def seen(self, text: str) -> bool:
        if h64(norm(text)) in self.full_all:
            return True
        if any(h in self.sent_all for h in sent_hashes(text)):
            return True
        for ln in (text or "").split("\n"):
            nl = norm(ln)
            if nl.count(" ") + 1 >= 6 and h64(nl) in self.line_all:
                return True
        return False

    def near_dup(self, text: str) -> bool:
        """v1.2: any shared word 10-gram (was: >= 50% of the text's 10-grams)."""
        return self.g10.coverage(text) > 0.0

    def bad(self, text: str) -> str | None:
        """None if the text is usable, else the reason ('sentence' or 'shared_10gram')."""
        if text not in self._cache:
            self._cache[text] = "sentence" if self.seen(text) else ("shared_10gram" if self.near_dup(text) else None)
        return self._cache[text]

    def any_bad(self, texts) -> str | None:
        for t in texts:
            w = self.bad(t) if t else None
            if w:
                return w
        return None


def para_hash(text: str) -> int:
    return h64(norm(text))


DEVX_SETS = ("squad2", "musique", "2wiki")


def write_devx(ds: str, paras) -> dict:
    """Everything a mix-tuning-dev row of `ds` shows: page titles, paragraph hashes and sentence hashes (no text)."""
    titles, ph, sh = set(), set(), set()
    for t, x in paras:
        titles.add(norm_title(t))
        ph.add(para_hash(x))
        sh.update(sent_hashes(x))
    d = {"dataset": ds, "titles": sorted(titles), "para_hashes": sorted(ph), "sent_hashes": sorted(sh)}
    (TMP / f"devx_{ds}.json").write_text(json.dumps(d))
    return {"titles": len(titles), "paragraphs": len(ph), "sentences": len(sh)}


class DevX:
    """Union over SQuAD 2.0, MuSiQue and 2Wiki of what the mix-tuning-dev rows show (spec 3.1 / 10 S7; review item 2).
    A train or reserve row may show no such title, paragraph or sentence."""

    def __init__(self):
        self.titles, self.paras, self.sents = set(), set(), set()
        for ds in DEVX_SETS:
            d = json.loads((TMP / f"devx_{ds}.json").read_text())
            self.titles |= set(d["titles"])
            self.paras |= set(d["para_hashes"])
            self.sents |= set(d["sent_hashes"])

    def blocked(self, title: str, text: str) -> bool:
        if norm_title(title) in self.titles or para_hash(text) in self.paras:
            return True
        return any(h in self.sents for h in sent_hashes(text))


def own_side(title: str, dev: bool) -> bool:
    """Review item 2: a shown non-required paragraph comes only from a page on the item's own side of the split."""
    return is_dev_page(title) == dev


_TOK = None


def ntok(text: str) -> int:
    global _TOK
    if _TOK is None:
        from tokenizers import Tokenizer
        _TOK = Tokenizer.from_file(str(TMP / "tokenizer.json"))
    return len(_TOK.encode(text).ids)


def row_tokens(row: dict) -> int:
    """Estimate (v1.0 method): state + instructions + card + options, plus overhead. G15 lengths use real_tokens."""
    parts = [row["state"] or "", row["instructions"] or "", row.get("card") or ""]
    if row.get("options"):
        parts.append("\n".join(row["options"]))
    return ntok("\n".join(parts)) + OVERHEAD_TOKENS


_RT = None
SNAP = Path.home() / ".cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"


def real_tokens(row: dict) -> int:
    """Real-tokenizer length of the trained and served prompt: chat template (system + user), decoder_io cygnet style,
    schema_branch_mark layout (the instructions and options are printed twice), identity option order."""
    global _RT
    if _RT is None:
        lean = HERE.parents[2]
        if str(lean) not in sys.path:
            sys.path.insert(0, str(lean))
        import decoder_io as dio
        from transformers import AutoTokenizer
        _RT = (dio, AutoTokenizer.from_pretrained(str(SNAP), local_files_only=True))
    dio, tok = _RT
    saved = (dio.STYLE, dio.LAYOUT)
    try:
        dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
        r = {k: row[k] for k in ("state", "qtype", "instructions", "options", "gold", "card")}
        lr = dio.as_letter_row(r)
        txt = dio.render_chat(tok, dio.CYGNET_SYSTEM, dio.user_msg(r, list(range(len(lr["options"])))))
    finally:
        dio.STYLE, dio.LAYOUT = saved
    return len(tok(txt, add_special_tokens=False)["input_ids"])


def make_row(*, ds: str, framing: str, key: str, group: str, state: str, instructions: str, options, gold, role: str,
             card, meta: dict) -> dict:
    rid = f"pub1-{ds}-{framing}-{sha(ds + '|' + framing + '|' + key)[:14]}"
    # v1.1 (review item 1, G15): decoder_io (cygnet, schema_branch_mark) prints a choice row's card only as
    # '- {option}: {definition}' lines, so a prose card on a choice row goes to the start of instructions (formats-1
    # render_row_text order: card text, then the wording / question); the card field stays None. Yes/no cards stay in
    # the card field (printed whole under 'Definitions:').
    authored = card
    if options is not None and card:
        instructions = f"{card}\n\n{instructions}"
        card = None
    meta = {**meta, "card_route": None if not authored else ("instructions" if options is not None else "card")}
    row = {
        "id": rid,
        "group_id": f"c_pub_{ds}:g:{group}",
        "call_id": "c_" + sha("call|" + rid)[:12],
        "source": f"c_pub_{ds}",
        "state": state,
        "qtype": "choice" if options is not None else "noul",
        "instructions": instructions,
        "options": options,
        "gold": gold,
        "role": role,
        "card": card,
        "meta": meta,
        "_card": authored,           # popped by assemble.py into tmp/row_cards.json (G15 must_show); never written out
    }
    if options is not None:
        assert isinstance(gold, str) and gold in options and len(set(options)) == len(options), rid
        assert not any("\n" in o or "\r" in o for o in options), rid  # an option line must stay one line (G15)
    else:
        assert gold in (0, 1), rid
    return row


def base_meta(*, family_block: str, dataset: str, record_id: str, licence: str, sa: bool, card_id: str,
              wording_id: str, defs_style: str, format_style: str, structure: str, edge: list, depth=None,
              twin_of=None, twin_kind=None, extra: dict | None = None) -> dict:
    m = {
        "family": "public",
        "block": family_block,
        "spec_id": SPEC_ID,
        "card_id": card_id,
        "domain_pack": None,
        "sampler": None,
        "gen_version": GEN_VERSION,
        "git_sha": None,             # filled by assemble.py (repo HEAD + builder code sha256)
        "seed": SEED,
        "structure_hash": sha("struct|" + structure)[:16],
        "difficulty_bin": None,      # G9 (scoring crowd on the free L4) fills these
        "crowd_pg": None,
        "depth": depth,
        "deep": False,
        "format_style": format_style,
        "wording_id": wording_id,
        "defs_style": defs_style,
        "twin_of": twin_of,
        "twin_kind": twin_kind,
        "text_source": {"dataset": dataset, "record_id": record_id, "split": "train"},
        "licence": licence,
        "share_alike": sa,
        "edge": edge,
        "dataset": dataset,
        "domain": f"c_pub_{family_block}",
    }
    if extra:
        m.update(extra)
    return m


def write_jsonl(path: Path, rows) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    h = hashlib.sha256(path.read_bytes()).hexdigest()
    return h


def licence_string(ds_key: str) -> str:
    fm = json.loads((LOGS / "fetch_manifest.json").read_text())
    recs = fm["licence_records"]
    dl = fm["downloads"]
    c = fm["commits"]
    if ds_key == "squad2":
        r = recs["squad2"]
        return (f"CC BY-SA 4.0 (share-alike) | record https://rajpurkar.github.io/SQuAD-explorer/ re-read "
                f"{r['read_utc']} sha256 {r['sha256'][:16]} | page repo rajpurkar/SQuAD-explorer@{c['squad_explorer'][:12]}"
                f" | data train-v2.0.json sha256 {dl['squad2']['archive_sha256'][:16]} | text: Wikipedia (CC BY-SA)")
    if ds_key == "musique":
        r = recs["musique_license"]
        f = [v for k, v in dl["musique"]["files"].items() if k.endswith("full_v1.0_train.jsonl")][0]
        return (f"CC BY 4.0 (annotations); rows treated as share-alike (Wikipedia paragraphs, CC BY-SA seed questions) | "
                f"record https://github.com/StonyBrookNLP/musique/blob/{c['musique'][:12]}/LICENSE re-read {r['read_utc']} "
                f"sha256 {r['sha256'][:16]} | data musique_full_v1.0_train.jsonl sha256 {f['sha256'][:16]} "
                f"(zip {dl['musique']['archive_sha256'][:16]})")
    if ds_key == "2wiki":
        r = recs["2wiki_license"]
        f = list(dl["2wiki"]["files"].values())[0]
        return (f"Apache-2.0 (annotations); Wikipedia text CC BY-SA (share-alike), Wikidata CC0 | record "
                f"https://github.com/Alab-NII/2wikimultihop/blob/{c['2wikimultihop'][:12]}/LICENSE re-read {r['read_utc']} "
                f"sha256 {r['sha256'][:16]} | data data_ids_april7 train.json sha256 {f['sha256'][:16]}")
    if ds_key == "quality":
        r = recs["quality_page"]
        return (f"CC BY 4.0 (annotations) | record https://nyu-mll.github.io/quality/ re-read {r['read_utc']} sha256 "
                f"{r['sha256'][:16]} | repo nyu-mll/quality@{c['quality'][:12]} | data QuALITY.v1.0.1.htmlstripped.train "
                f"sha256 {dl['quality']['archive_sha256'][:16]}")
    if ds_key == "qasper":
        r = recs["qasper_page_archived"]
        return (f"CC BY 4.0 (annotations) | record https://web.archive.org/web/20230414023335/https://allenai.org/data/qasper "
                f"re-read {r['read_utc']} sha256 {r['sha256'][:16]} | data qasper-train-dev-v0.3.tgz sha256 "
                f"{dl['qasper']['archive_sha256'][:16]}")
    raise KeyError(ds_key)


def assign_balanced(units, wordings, defs_styles, defs_weights, key):
    """Round-robin wordings and def styles over units (a unit = a contrast pair or a yes/no pair), so every wording
    sees each gold equally. Returns list of (unit, wording, defs_style)."""
    out = []
    r = rng("assign", key)
    order = stable_shuffle(range(len(units)), "assign-order", key)
    for j, i in enumerate(order):
        w = wordings[j % len(wordings)]
        d = r.choices(defs_styles, weights=defs_weights)[0]
        out.append((units[i], w, d))
    return out
