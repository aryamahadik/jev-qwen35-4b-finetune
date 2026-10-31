#!/usr/bin/env python3
"""G-block fix5 (PREREG_FINAL A39 c/d): re-render five yes/no cards with BOTH definition lines. CPU only; no network;
no label is set or read here.

Why: build_candidates.py printed a yes/no card as the '- yes: ...' line only. For five admitted cards the 'no' definition
holds edge rules that a reader (and later the model) must see:
  gb_recipes_3_c0, gb_sci_abstracts_2_c0, gb_gov_news_2_c0, gb_volunteer_posts_3_c0, gb_news_1_c0.

What it does (deterministic, idempotent):
  (1) every candidate of those 5 cards in candidates/candidates.jsonl gets a REPLACEMENT: same text, same card, id
      suffixed '_b2', card = '- yes: <yes def>\\n- no: <no def>' (the replay format; build_candidates card_string with
      YESNO_CARD="both"). Each replacement is checked with decoder_io exactly like the build (cygnet + schema_branch_mark,
      formats-1 loader_check, pinned tokenizer, 2,000-token cap) plus: both definition lines printed whole;
      -> candidates/fix5_candidates.jsonl
  (2) the old candidate ids of those cards are marked SUPERSEDED (candidates/superseded_fix5.json). candidates.jsonl,
      label/key.json, label/chunks/ and label/MANIFEST.json are NOT touched (their hashes stay valid); tools/route.py
      drops superseded ids from accepted_haiku.jsonl and from the Opus queue.
  (3) gold-free TEACH-0 chunks for the replacements, 50 per chunk, NEW opaque qids (own HMAC secret, asserted disjoint from
      label/key.json and label/opus_queue/key.json): label/fix5/chunks/chunk_XXXX.json, label/fix5/key.json
      ({qid: replacement id}, never sent to a reader), label/fix5/MANIFEST.json.

  ../../../.venv/bin/python tools/fix5.py [--dry-run] [--force]
    --dry-run  build and check in memory, print the counts, write nothing
    --force    overwrite an existing label/fix5/key.json even if its content would change while fix5 Haiku answers exist
Writes go through c2_kit.paths (A38 guard, never-open guard, lean/ only).
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
import build_candidates as B  # noqa: E402  (paths, seed, Renderer, chunk item format, qid scheme)
from build_candidates import kp, kc  # noqa: E402

FIX5_CARDS = ("gb_recipes_3_c0", "gb_sci_abstracts_2_c0", "gb_gov_news_2_c0", "gb_volunteer_posts_3_c0",
              "gb_news_1_c0")
SUFFIX = "_b2"
FIX5_DIR = B.LABEL / "fix5"
FIX5_CAND = B.CAND_DIR / "fix5_candidates.jsonl"
SUPERSEDED = B.CAND_DIR / "superseded_fix5.json"
FIX5_STATS = B.CAND_DIR / "fix5_stats.json"
FIX5_CHUNKS = FIX5_DIR / "chunks"
FIX5_KEY = FIX5_DIR / "key.json"
FIX5_MANIFEST = FIX5_DIR / "MANIFEST.json"
FIX5_SECRET = hashlib.sha256(f"gblock|fix5|blind_read|{B.SEED}".encode()).hexdigest().encode()
FIX5_ORDER = f"{B.SEED}|gblock|fix5|order"


def build_replacements(cands: list, cards: dict) -> tuple:
    """(old rows of the 5 cards, replacement rows). Pure; the old card string must be the yes-only render."""
    for cid in FIX5_CARDS:
        c = cards[cid]
        assert c["kind"] == "yes/no", cid
        assert c["definitions"].get("yes", "").strip() and c["definitions"].get("no", "").strip(), cid
    old = sorted((r for r in cands if r["card_id"] in FIX5_CARDS), key=lambda r: r["id"])
    new = []
    for r in old:
        c = cards[r["card_id"]]
        yes_only = f"- yes: {c['definitions']['yes']}"
        assert r["card"] == yes_only and r["qtype"] == "noul" and r["options"] is None, \
            f"{r['id']}: not the yes-only render the build wrote"
        assert r["id"].startswith(B.SOURCE + ":") and not r["id"].endswith(SUFFIX), r["id"]
        n = dict(r)   # same key order: id, group_id, domain, card_id, state, instructions, qtype, options, card
        n["id"] = r["id"] + SUFFIX
        n["card"] = B.card_string(c)   # YESNO_CARD == "both" (set in main): '- yes: ..\n- no: ..'
        assert n["card"] == f"- yes: {c['definitions']['yes']}\n- no: {c['definitions']['no']}"
        assert {k: v for k, v in n.items() if k not in ("id", "card")} == \
            {k: v for k, v in r.items() if k not in ("id", "card")}, "text/card fields must stay identical"
        new.append(n)
    return old, new


def render_check(R, rows: list, cards: dict) -> tuple:
    """(kept rows, drops, token stats). Same checks as the build + both definition lines shown whole."""
    dio = R.dio
    kept, drops, toks = [], [], []
    for r in rows:
        probs, ntok, _ = R.check(r)
        try:
            B.chunk_item(r, "q0")
        except kc.ChunkError as e:
            probs.append(f"chunk item guard: {e}")
        if ntok > B.TOK_MAX:
            probs.append(f"{ntok} tokens > {B.TOK_MAX}")
        d = cards[r["card_id"]]["definitions"]
        saved = (dio.STYLE, dio.LAYOUT, dio.WIDE)
        dio.STYLE, dio.LAYOUT = B.STYLE, B.LAYOUT
        dio.WIDE = list(dio.LETTERS) + R.wide[: dio.MAX_OPTIONS - 26]
        try:
            msg = dio.user_msg(r)
        finally:
            dio.STYLE, dio.LAYOUT, dio.WIDE = saved
        block = f"Definitions:\n- yes: {d['yes']}\n- no: {d['no']}\n\n{r['instructions'].rstrip()}"
        if block not in msg:
            probs.append("definitions block (yes line then no line) not printed whole before the question")
        if msg.count(f"- no: {d['no']}") != 1 or msg.count(f"- yes: {d['yes']}") != 1:
            probs.append("a definition line is printed more or less than once")
        if probs:
            drops.append({"id": r["id"], "tokens": ntok, "problems": probs[:4]})
            continue
        kept.append(r)
        toks.append(ntok)
    return kept, drops, toks


def main(argv):
    dry = "--dry-run" in argv
    force = "--force" in argv
    kp.require_a38()
    B.YESNO_CARD = "both"   # the replay format: '- yes: ..' then '- no: ..'
    cards = B.load_cards()
    for cid in FIX5_CARDS:
        assert cid in cards, cid
    # inputs must be the built label set (their hashes are not changed by this step)
    man = json.loads(kp.check_path(B.LABEL / "MANIFEST.json").read_text(encoding="utf-8"))
    cand_sha = B.sha256_file(B.CAND)
    if cand_sha != man["candidates_sha256"] or B.sha256_file(B.KEY) != man["key_sha256"]:
        raise SystemExit("fix5: candidates.jsonl / label/key.json differ from label/MANIFEST.json")
    cands = B.read_jsonl(B.CAND)
    ids = {r["id"] for r in cands}
    old, new = build_replacements(cands, cards)
    assert len(old) == len(new) > 0 and not ({r["id"] for r in new} & ids), "replacement ids collide"

    R = B.Renderer()
    kept, drops, toks_new = render_check(R, new, cards)
    # tokens the 'no' line adds, against the old (yes-only) render
    old_by_id = {r["id"]: r for r in old}
    tok_delta = [nt - R.check(old_by_id[r["id"][:-len(SUFFIX)]])[1] for r, nt in zip(kept, toks_new)]
    if drops:
        raise SystemExit(f"fix5: {len(drops)} replacements failed the render/token check, e.g. {drops[:3]}; "
                         "not writing anything (a failed replacement would silently lose a row)")

    # ---- consistency of the active set: old superseded, new in; still one card per text, ids unique
    sup_ids = sorted(r["id"] for r in old)
    sup = set(sup_ids)
    active = [r for r in cands if r["id"] not in sup] + kept
    assert len({r["id"] for r in active}) == len(active), "ids not unique after the swap"
    assert len({r["group_id"] for r in active}) == len(active), "one card per text broken by the swap"
    assert len(active) == len(cands), (len(active), len(cands))
    for a, b in B.NEAR_DUP_PAIRS:   # unchanged by construction (choice cards), asserted anyway
        by_text = defaultdict(set)
        for r in active:
            by_text[r["group_id"]].add(r["card_id"])
        assert not any(a in s and b in s for s in by_text.values()), (a, b)

    # ---- chunks + key (new opaque qids)
    old_qids = set(json.loads(kp.check_path(B.KEY).read_text(encoding="utf-8")))
    oq = B.LABEL / "opus_queue" / "key.json"
    if oq.exists():
        old_qids |= set(json.loads(kp.check_path(oq).read_text(encoding="utf-8")))
    chunks, key = B.make_chunks(kept, FIX5_SECRET, FIX5_ORDER, avoid=old_qids)
    assert not (set(key) & old_qids) and len(key) == len(kept)
    assert set(key.values()) == {r["id"] for r in kept}
    files = {f"{n}.json": B.chunk_text(items) for n, items in chunks}
    key_text = json.dumps(key, indent=1) + "\n"
    per_card = Counter(r["card_id"] for r in kept)
    per_domain = Counter(r["domain"] for r in kept)
    print(f"fix5: {len(kept)} replacements for {len(old)} superseded ids; per card {dict(sorted(per_card.items()))}")
    print(f"  tokens new min/med/max {min(toks_new)}/{sorted(toks_new)[len(toks_new) // 2]}/{max(toks_new)}; "
          f"added by the no line min/med/max {min(tok_delta)}/{sorted(tok_delta)[len(tok_delta) // 2]}/{max(tok_delta)}; "
          f"cap {B.TOK_MAX}; render failures 0")
    print(f"  chunks {len(chunks)} (sizes {sorted({len(i) for _, i in chunks})}); qids new and disjoint from "
          f"{len(old_qids)} existing ones")
    if dry:
        return

    haiku = sorted((FIX5_DIR / "haiku").glob("*.json")) if (FIX5_DIR / "haiku").is_dir() else []
    if FIX5_KEY.exists() and kp.check_path(FIX5_KEY).read_text(encoding="utf-8") != key_text and haiku and not force:
        raise SystemExit("label/fix5/key.json would change while fix5 Haiku answers exist: refusing (--force to override)")

    kp.write_jsonl(FIX5_CAND, kept)
    kp.write_json(SUPERSEDED, {
        "ruling": "PREREG_FINAL A39 (c/d); see FIX5.md",
        "what": "Candidate ids replaced by *_b2 re-renders that print both the yes and the no definition. Superseded ids "
                "stay in candidates.jsonl, label/key.json and label/chunks/ (hashes unchanged) but must never reach "
                "accepted_haiku.jsonl or the Opus queue (tools/route.py filters them).",
        "cards": list(FIX5_CARDS), "replacement_suffix": SUFFIX, "n_superseded": len(sup_ids),
        "per_card": dict(sorted(Counter(r["card_id"] for r in old).items())),
        "inputs": {"candidates_sha256": cand_sha, "label_key_sha256": man["key_sha256"]},
        "fix5_candidates_sha256": B.sha256_file(FIX5_CAND),
        "superseded_ids": sup_ids,
    })
    if FIX5_CHUNKS.is_dir():
        for stale in FIX5_CHUNKS.glob("chunk_*.json"):
            if stale.name not in files:
                stale.unlink()
    for name, text in files.items():
        kp.write_text(FIX5_CHUNKS / name, text)
    kp.write_text(FIX5_KEY, key_text)
    manifest = {
        "what": "G-block fix5 gold-free label chunks (PREREG_FINAL A39; FIX5.md), TEACH-0 item format",
        "seed": B.SEED, "chunk_size": B.CHUNK, "n_items": len(key), "n_chunks": len(chunks),
        "qid": "q + HMAC-SHA256(fix5 secret, replacement id)[:10]; order seeded; key in label/fix5/key.json (never sent)",
        "candidates_file": "candidates/fix5_candidates.jsonl",
        "candidates_sha256": B.sha256_file(FIX5_CAND), "key_sha256": B.sha256_file(FIX5_KEY),
        "superseded_sha256": B.sha256_file(SUPERSEDED),
        "chunks": {n: {"n": len(items), "sha256": hashlib.sha256(files[f"{n}.json"].encode()).hexdigest(),
                       "yes_no": sum(1 for i in items if i["kind"] == "yes/no")} for n, items in chunks},
    }
    kp.write_json(FIX5_MANIFEST, manifest)
    kp.write_json(FIX5_STATS, {
        "ruling": "PREREG_FINAL A39; FIX5.md", "cards": list(FIX5_CARDS), "n_replacements": len(kept),
        "per_card": dict(sorted(per_card.items())), "per_domain": dict(sorted(per_domain.items())),
        "render": {"decoder_io_sha256": B.DECODER_IO_SHA, "style": B.STYLE, "layout": B.LAYOUT,
                   "tokenizer_sha256": B.TOKENIZER_SHA, "token_cap": B.TOK_MAX,
                   "check": "build_candidates.Renderer.check (formats-1 loader_check, markers, definitions) + chunk "
                            "item guard + definitions block 'Definitions:\\n- yes: ..\\n- no: ..' printed whole once",
                   "failures": 0},
        "tokens_new_min_med_max": [min(toks_new), sorted(toks_new)[len(toks_new) // 2], max(toks_new)],
        "tokens_added_min_med_max": [min(tok_delta), sorted(tok_delta)[len(tok_delta) // 2], max(tok_delta)],
        "n_chunks": len(chunks), "chunk_sizes": dict(Counter(len(i) for _, i in chunks)),
        "outputs": {"fix5_candidates_sha256": manifest["candidates_sha256"], "key_sha256": manifest["key_sha256"],
                    "superseded_sha256": manifest["superseded_sha256"]},
    })
    print(f"wrote {FIX5_CAND.name}, {SUPERSEDED.name}, {len(chunks)} chunks in {FIX5_CHUNKS}, key, manifest, stats")


if __name__ == "__main__":
    main(sys.argv[1:])
