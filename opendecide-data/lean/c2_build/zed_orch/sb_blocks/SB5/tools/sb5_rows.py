"""SB5 row builder (A58 c 5, d): UCI 293 pool -> C2 yes/no rows (qtype noul, gold 1/0, card = yes/no definitions).
Reads work/pool.json; writes work/candidates.jsonl (1.5 x 750 cut to 1,124 = 281 per label x answer cell) and work/owndev.jsonl (150).
Deterministic, CPU only, seed 20261013. Usage: python -B sb5_rows.py"""
import json, sys
from collections import Counter
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from sb5_lib import *

P = json.load(open(WORK / "pool.json", encoding="utf-8"))
kept = {r["rid"]: r for r in P["kept"]}
dev_ids = set(P["dev_ids"])

WORDINGS = {  # question polarity -> 5 self-contained one-sentence wordings (written for this project)
    "neg": ["Does the writer of this tweet express a negative opinion or feeling?",
            "Is the overall opinion or feeling in this tweet negative?",
            "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
            "Is the sentiment of this Arabic tweet negative?",
            "Does the tweet show the writer holding a negative view of, or a negative feeling about, something?"],
    "pos": ["Does the writer of this tweet express a positive opinion or feeling?",
            "Is the overall opinion or feeling in this tweet positive?",
            "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
            "Is the sentiment of this Arabic tweet positive?",
            "Does the tweet show the writer holding a positive view of, or a positive feeling about, something?"]}
DEFS = {
    "neg": ("The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).",
            "The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."),
    "pos": ("The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.",
            "The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.")}
def card(pol):
    y, n = DEFS[pol]
    return f"- yes: {y}\n- no: {n}"

LEX = {"negation": "لا ما لم لن ليس ليست ليسوا مش مو بدون غير عدم ولا", "hypothetical": "لو ليت اذا لولا",
       "quantifier": "كل جميع كلهم كلها", "reported_speech": "قال قالت يقول قالوا صرح"}
LEXN = {k: set(norm_tokens(v)) for k, v in LEX.items()}
def edges(text):
    tk = set(norm_tokens(text))
    return sorted(k for k, v in LEXN.items() if tk & v)

LIC = ("CC BY 4.0 (UCI Machine Learning Repository dataset 293, https://archive.ics.uci.edu/dataset/293/twitter+data+set+for+arabic+sentiment+analysis, "
       "DOI 10.24432/C5F31B; N. Abdulla, Twitter Data set for Arabic Sentiment Analysis, 2013; tweets and human polarity labels); "
       "question and definition wording: CC0 1.0 (Claude-authored)")
G1 = {"zip_sha256": "a29250a60a18e1f02daf4ae4c4425113734d7cb79f353330815621c4ea4cd347",
      "rar_sha256": "12c1e8135e62f1fb8a0be14ad0c1a8bfe31f9411b0530c4d425924461f99b9f4", "record": "zed_orch/sb_blocks/SB5/G1_RECORD.json"}

def make(rec, yes, dev):
    lab = rec["label"]
    qpol = lab if yes else ("neg" if lab == "pos" else "pos")
    wid = h("word", rec["rid"]) % 5
    rid = f"c2_sb5:{rec['rid']}:{qpol}"
    gid = f"c2_sb5:{sha(rec['rid'])[:12]}"
    meta = {"family": "SB5", "spec_id": "A58.SB5", "card_id": f"sb5_{qpol}", "domain_pack": None, "sampler": "S5" if dev else "SB5",
            "gen_version": "sb5 1.0 (17 Oct 2026)", "git_sha": "uncommitted", "seed": SEED, "structure_hash": sha(rec["text"])[:16],
            "difficulty_bin": None, "crowd_pg": None, "depth": 0, "deep": False, "format_style": "real-text/card",
            "wording_id": f"sb5-{qpol}-{wid}", "defs_style": "same", "twin_of": None, "twin_kind": None, "text_source": "uci293",
            "licence": LIC, "edge": edges(rec["text"]), "qform": "POLARITY_YN", "dev_only": bool(dev),
            "c2": {"author_mode": "T", "skin_id": None, "register": "real-text", "lexicon_ids": [], "haiku_task_id": None,
                   "haiku_prompt_sha": None, "twin_kind": None, "twin_of": None, "closed_world": False},
            "domain": "arabic_tweet", "task_id": None,
            "sb5": {"uci_rid": rec["rid"], "orig_label": "positive" if lab == "pos" else "negative", "question_polarity": qpol,
                    "encoding": rec["enc"], "file_sha256_16": rec["file_sha"], "provenance": G1}}
    return {"id": rid, "group_id": gid, "call_id": gid, "source": "c2_sb5", "state": rec["text"], "qtype": "noul",
            "instructions": WORDINGS[qpol][wid], "options": None, "gold": 1 if yes else 0, "role": "base", "card": card(qpol),
            "meta": meta, "domain": "arabic_tweet"}

cand, dev = [], []
for lab in ("pos", "neg"):
    pool = sorted((r for r in kept.values() if r["label"] == lab and r["rid"] not in dev_ids), key=lambda r: h("cand", r["rid"]))[:562]
    pool.sort(key=lambda r: h("q", r["rid"]))
    cand += [make(r, i < 281, False) for i, r in enumerate(pool)]
    dv = sorted((kept[i] for i in dev_ids if kept[i]["label"] == lab), key=lambda r: h("q", r["rid"]))
    dev += [make(r, i < (37 if lab == "pos" else 38), True) for i, r in enumerate(dv)]
cand.sort(key=lambda r: h("order", r["id"])); dev.sort(key=lambda r: h("order", r["id"]))
for name, rows in (("candidates", cand), ("owndev", dev)):
    with open(WORK / f"{name}.jsonl", "w", encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
st = {"candidates": len(cand), "owndev": len(dev),
      "cand_cells": dict(Counter((r["meta"]["sb5"]["orig_label"], r["gold"]) for r in cand)),
      "dev_cells": dict(Counter((r["meta"]["sb5"]["orig_label"], r["gold"]) for r in dev)),
      "wording_share_max": max(Counter(r["meta"]["wording_id"] for r in cand).values()) / len(cand),
      "wordings": len(set(r["meta"]["wording_id"] for r in cand)),
      "overlap_cand_dev": len({r["meta"]["sb5"]["uci_rid"] for r in cand} & {r["meta"]["sb5"]["uci_rid"] for r in dev}),
      "edge": dict(Counter(e for r in cand for e in r["meta"]["edge"]))}
json.dump({k: {str(a): b for a, b in v.items()} if isinstance(v, dict) else v for k, v in st.items()}, open(WORK / "rows_stats.json", "w"), indent=1)
print(json.dumps({k: {str(a): b for a, b in v.items()} if isinstance(v, dict) else v for k, v in st.items()}, indent=1))
