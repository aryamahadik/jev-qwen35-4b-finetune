#!/usr/bin/env python3
"""G-block candidates and gold-free label chunks (PREREG_FINAL A39 b-e). CPU only; no network; no label is set here.

Inputs (read-only): texts/<domain>/texts.jsonl (A39 b texts) and cards/admitted.jsonl (41 admitted cards, A39 c).

Sampling (seed 20261013):
  - per domain, texts are drawn without replacement in a seeded shuffle; a domain quota water-fills toward
    TARGET_TOTAL (every domain gets min(its texts, Q), Q the smallest level reaching the target), so no domain is above
    the 20% cap and small domains are used whole;
  - each drawn text gets exactly ONE admitted card of its own domain, round-robin over a seeded shuffle of the domain's
    cards (so every card is used about equally: >= 200 times wherever the domain's texts allow). One card per text
    also means the two near-duplicate pairs of cards/ADMISSION.md never meet on one text (asserted);
  - a candidate whose prompt does not render cleanly or is over the 2,000-token cap is dropped and the same card goes
    to the next text in the shuffle (card balance is kept).

Candidate row (decoder_io raw row WITHOUT gold):
  {id, group_id (= text_id), domain, card_id, state (the text), instructions (the card question),
   qtype ("noul" yes/no | "choice"), options (choice: the card's options; yes/no: null), card}
  card = cygnet card string of "- label: definition" lines; choice: one line per option; yes/no: the definition of
  yes only ("- yes: ..."; lower-case, so decoder_io prints it whole under "Definitions:" and never glues it to the
  Yes/No option lines).
Render check: decoder_io (sha-pinned, imported read-only) in style cygnet + layout schema_branch_mark through
formats-1 loader_check (option block, card printed, train_decoder.check_rows) with an in-memory placeholder gold that
is never written; tokens = the mixer's count (pinned Qwen3.5-4B tokenizer on CYGNET_SYSTEM + "\\n" + user_msg).

Label chunks (TEACH-0 format, teach0/build.py): label/chunks/chunk_XXXX.json = a list of <= 50 items
  {qid, kind "yes/no"|"choice", text, question, options (choice only), definitions (the card string)},
opaque HMAC qids, a seeded order that mixes domains; label/key.json = {qid: candidate id} (never sent to a reader);
label/MANIFEST.json = chunk sha256s and counts. Writes go through c2_kit.paths (A38 guard, never-open guard, lean/).

  ../../../.venv/bin/python tools/build_candidates.py [--yesno-card yes|both] [--force]
      deterministic; --yesno-card both prints the admitted no definition too (default: yes only, as tasked);
      refuses to change the key once Haiku answers exist in label/haiku/ unless --force
"""
from __future__ import annotations

import hashlib
import hmac
import json
import math
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
C2 = LEAN / "c2_build"
GB = C2 / "gblock"
TEXTS = GB / "texts"
ADMITTED = GB / "cards" / "admitted.jsonl"
CAND_DIR = GB / "candidates"
CAND = CAND_DIR / "candidates.jsonl"
LABEL = GB / "label"
CHUNKS = LABEL / "chunks"
KEY = LABEL / "key.json"
for _p in (str(C2), str(LEAN), str(LEAN / "c_src" / "formats" / "formats-1")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
from c2_kit import paths as kp  # noqa: E402  (guarded writers, never-open rule)
from c2_kit import chunker as kc  # noqa: E402  (blind_read item guard: allowed fields, forbidden keys, paths)

SEED = 20261013
TARGET_TOTAL = 20000
DOMAIN_CAP = 0.20
MIN_PER_CARD = 200
TOK_MAX = 2000
CHUNK = 50
SOURCE = "c2_gblock"
NEAR_DUP_PAIRS = (("gb_office_help_1_c1", "gb_office_help_3_c1"), ("gb_sci_abstracts_2_c1", "gb_sci_abstracts_3_c1"))
TOKENIZER = Path.home() / ".cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots" / \
    "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a/tokenizer.json"
TOKENIZER_SHA = "5f9e4d4901a92b997e463c1f46055088b6cca5ca61a6522d1b9f64c4bb81cb42"   # = c_build/mixer.py pin
DECODER_IO_SHA = "908c08d752ce8896c2628a06f8a9d3153df8c76b657bf29daae44656f75f2948"  # A16 readout (formats-1 pin)
STYLE, LAYOUT = "cygnet", "schema_branch_mark"
QID_SECRET = hashlib.sha256(f"gblock|label|blind_read|{SEED}".encode()).hexdigest().encode()


def sha256_file(p: Path) -> str:
    return hashlib.sha256(kp.check_path(p).read_bytes()).hexdigest()


def read_jsonl(p: Path) -> list:
    with open(kp.check_path(p), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


# ---------------------------------------------------------------------------------------------------------- cards

YESNO_CARD = "yes"   # task spec: a yes/no card is the definition of yes; "both" adds the admitted "- no: ..." line


def card_string(card: dict) -> str:
    d = card["definitions"]
    if card["kind"] == "yes/no":
        return f"- yes: {d['yes']}" + (f"\n- no: {d['no']}" if YESNO_CARD == "both" else "")
    return "\n".join(f"- {o}: {d[o]}" for o in card["options"])


def load_cards() -> dict:
    cards = {}
    for c in read_jsonl(ADMITTED):
        cid, kind, opts, d = c["card_id"], c["kind"], c["options"], c["definitions"]
        assert cid not in cards, f"duplicate card {cid}"
        assert kind in ("yes/no", "choice"), (cid, kind)
        assert c["question"].strip() and "\n" not in c["question"], cid
        if kind == "yes/no":
            assert sorted(opts) == ["no", "yes"] and d.get("yes", "").strip(), cid
        else:
            assert 2 <= len(opts) <= 8 and len(set(opts)) == len(opts), cid
            assert set(d) == set(opts), (cid, "definitions != options")
            for o in opts:
                assert o.strip() == o and o and "\n" not in o and ": " not in o and not o.startswith("- "), (cid, o)
        for v in d.values():
            assert v.strip() and "\n" not in v, cid
        cards[cid] = c
    for a, b in NEAR_DUP_PAIRS:
        assert a in cards and b in cards and cards[a]["domain"] == cards[b]["domain"], (a, b)
    return cards


# ---------------------------------------------------------------------------------------------------------- render

def _dio():
    p = LEAN / "decoder_io.py"
    if sha256_file(p) != DECODER_IO_SHA:
        raise SystemExit("decoder_io.py is not the pinned A16 readout")
    import decoder_io as dio
    assert Path(dio.__file__).resolve() == p.resolve()
    return dio


class Renderer:
    """decoder_io cygnet + schema_branch_mark, the pinned tokenizer, formats-1 loader_check (all read-only)."""

    def __init__(self):
        from tokenizers import Tokenizer
        from fmt1 import card as fcard
        self.dio = _dio()
        self.fcard = fcard
        if sha256_file(TOKENIZER) != TOKENIZER_SHA:
            raise SystemExit("tokenizer.json is not the pinned Qwen3.5-4B snapshot")
        self.tok = Tokenizer.from_file(str(TOKENIZER))
        U = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.wide = [w for w in (a + b for a in U for b in U)
                     if len(self.tok.encode(w, add_special_tokens=False).ids) == 1]

    def check(self, row: dict) -> tuple:
        """(problems, tokens, prompt_sha256) of one gold-free candidate."""
        dio = self.dio
        saved = (dio.STYLE, dio.LAYOUT, dio.WIDE)
        dio.STYLE, dio.LAYOUT = STYLE, LAYOUT
        dio.WIDE = list(dio.LETTERS) + self.wide[: dio.MAX_OPTIONS - 26]
        try:
            msg = dio.user_msg(row)
            ntok = len(self.tok.encode(dio.CYGNET_SYSTEM + "\n" + msg).ids)
        finally:
            dio.STYLE, dio.LAYOUT, dio.WIDE = saved
        probs = []
        st = row["state"].rstrip()
        if f"{dio.UNTRUSTED[0]}\n{st}\n{dio.UNTRUSTED[1]}" not in msg:
            probs.append("text not shown whole between the markers")
        if msg.count(row["instructions"].rstrip()) < 2:
            probs.append("question not shown in schema and branch")
        if any(m in st for m in dio.UNTRUSTED):
            probs.append("text holds a marker string")
        # loader_check needs a gold: an in-memory placeholder (never written, never a label)
        ph = dict(row, gold=1 if row["qtype"] == "noul" else row["options"][0])
        res = self.fcard.loader_check(ph, check_rows=True)
        probs += res["problems"]
        if row["qtype"] == "choice":
            for o in row["options"]:
                if f"{o}: {self.dio.card_defs(row['card'])[o]}" not in msg:
                    probs.append(f"option {o!r} shown without its definition")
        return probs, ntok, hashlib.sha256(msg.encode()).hexdigest()


# ---------------------------------------------------------------------------------------------------------- build

def quota_level(sizes: dict, target: int) -> int:
    """Smallest Q with sum(min(n, Q)) >= target (or the largest domain if the texts run out)."""
    lo, hi = 0, max(sizes.values())
    while lo < hi:
        mid = (lo + hi) // 2
        if sum(min(n, mid) for n in sizes.values()) >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo


def make_row(text: dict, card: dict) -> dict:
    yn = card["kind"] == "yes/no"
    return {"id": f"{SOURCE}:{text['text_id']}:{card['card_id']}", "group_id": text["text_id"],
            "domain": text["domain"], "card_id": card["card_id"], "state": text["text"],
            "instructions": card["question"], "qtype": "noul" if yn else "choice",
            "options": None if yn else list(card["options"]), "card": card_string(card)}


def chunk_item(row: dict, qid: str) -> dict:
    """TEACH-0 item (teach0/build.py): qid, kind, text, question, options (choice only), definitions (card)."""
    it = {"kind": "yes/no" if row["qtype"] == "noul" else "choice", "text": row["state"],
          "question": row["instructions"]}
    if row["qtype"] == "choice":
        it["options"] = list(row["options"])
    it["definitions"] = row["card"]
    kc.check_item("blind_read", it)
    return {"qid": qid, **it}


def opaque_qid(secret: bytes, cid: str) -> str:
    return "q" + hmac.new(secret, cid.encode(), hashlib.sha256).hexdigest()[:10]


def make_chunks(rows: list, secret: bytes, order_seed: str, avoid: set = frozenset()) -> tuple:
    """(chunks [(name, items)], key {qid: candidate id}) in a seeded order; leak-checked."""
    ids = sorted(r["id"] for r in rows)
    by = {r["id"]: r for r in rows}
    random.Random(order_seed).shuffle(ids)
    key, chunks = {}, []
    for c in range(0, len(ids), CHUNK):
        items = []
        for cid in ids[c:c + CHUNK]:
            q = opaque_qid(secret, cid)
            if q in key or q in avoid:
                raise SystemExit("opaque qid collision")
            key[q] = cid
            items.append(chunk_item(by[cid], q))
        blob = json.dumps(items, ensure_ascii=False)
        for cid in ids[c:c + CHUNK]:
            r = by[cid]
            for s in (cid, r["group_id"], r["card_id"], SOURCE + ":"):
                if s in blob:
                    raise SystemExit(f"chunk would leak an internal id ({s[:40]})")
        chunks.append((f"chunk_{c // CHUNK:04d}", items))
    return chunks, key


def chunk_text(items: list) -> str:
    return json.dumps(items, ensure_ascii=False, indent=1) + "\n"


def main(force: bool = False):
    kp.require_a38()
    cards = load_cards()
    by_dom_cards = defaultdict(list)
    for c in cards.values():
        by_dom_cards[c["domain"]].append(c)
    texts, src_sha = {}, {}
    seen = set()
    for d in sorted(by_dom_cards):
        p = TEXTS / d / "texts.jsonl"
        rows = read_jsonl(p)
        src_sha[d] = sha256_file(p)
        for t in rows:
            assert t["domain"] == d and t["text"].strip(), t["text_id"]
            assert t["text_id"] not in seen, f"duplicate text_id {t['text_id']}"
            seen.add(t["text_id"])
        texts[d] = sorted(rows, key=lambda t: t["text_id"])
    dirs = sorted(x.name for x in TEXTS.iterdir() if x.is_dir())
    assert dirs == sorted(by_dom_cards), f"text domains {dirs} != card domains {sorted(by_dom_cards)}"
    sizes = {d: len(v) for d, v in texts.items()}
    Q = quota_level(sizes, TARGET_TOTAL)
    quota = {d: min(n, Q) for d, n in sizes.items()}

    R = Renderer()
    out, stats, drops = [], {}, []
    for d in sorted(texts):
        order = list(texts[d])
        random.Random(f"{SEED}|gblock|texts|{d}").shuffle(order)
        dc = sorted(by_dom_cards[d], key=lambda c: c["card_id"])
        random.Random(f"{SEED}|gblock|cards|{d}").shuffle(dc)
        ptr, kept, toks = 0, [], []
        for t in order:
            if len(kept) == quota[d]:
                break
            card = dc[ptr % len(dc)]
            row = make_row(t, card)
            probs, ntok, _ = R.check(row)
            try:
                chunk_item(row, "q0")
            except kc.ChunkError as e:
                probs.append(f"chunk item guard: {e}")
            if ntok > TOK_MAX:
                probs.append(f"{ntok} tokens > {TOK_MAX}")
            if probs:
                drops.append({"text_id": t["text_id"], "card_id": card["card_id"], "tokens": ntok,
                              "problems": probs[:4]})
                continue
            kept.append(row)
            toks.append(ntok)
            ptr += 1
        out += kept
        per_card = Counter(r["card_id"] for r in kept)
        stats[d] = {"texts": sizes[d], "quota": quota[d], "kept": len(kept),
                    "dropped": sum(1 for x in drops if cards[x["card_id"]]["domain"] == d),
                    "cards": {c["card_id"]: {"kind": c["kind"], "uses": per_card.get(c["card_id"], 0)}
                              for c in sorted(dc, key=lambda c: c["card_id"])},
                    "card_order": [c["card_id"] for c in dc],
                    "tokens_min_med_max": [min(toks), int(statistics.median(toks)), max(toks)] if toks else None}

    # ---- checks
    total = len(out)
    ids = [r["id"] for r in out]
    assert len(set(ids)) == total and len({r["group_id"] for r in out}) == total, "one card per text"
    by_text = defaultdict(set)
    for r in out:
        by_text[r["group_id"]].add(r["card_id"])
    for a, b in NEAR_DUP_PAIRS:
        assert not any(a in s and b in s for s in by_text.values()), (a, b)
    share = {d: stats[d]["kept"] / total for d in stats}
    assert max(share.values()) <= DOMAIN_CAP, share
    short = []
    for d, s in stats.items():
        for cid, c in s["cards"].items():
            if c["uses"] < MIN_PER_CARD:
                allow = len(texts[d]) // len(s["cards"])
                short.append({"card_id": cid, "uses": c["uses"], "domain_texts": len(texts[d]),
                              "cards_in_domain": len(s["cards"]), "texts_allow_per_card": allow})
                assert c["uses"] >= min(MIN_PER_CARD, allow), (cid, c["uses"], allow)

    # ---- chunks + key
    chunks, key = make_chunks(out, QID_SECRET, f"{SEED}|gblock|label|order")
    files = {f"{n}.json": chunk_text(items) for n, items in chunks}
    key_text = json.dumps(key, indent=1) + "\n"
    haiku = sorted((LABEL / "haiku").glob("*.json")) if (LABEL / "haiku").is_dir() else []
    if KEY.exists() and kp.check_path(KEY).read_text(encoding="utf-8") != key_text and haiku and not force:
        raise SystemExit("label/key.json would change while Haiku answers exist in label/haiku/: refusing "
                         "(rerun with --force only if those answers are discarded)")

    kp.write_jsonl(CAND, out)
    if CHUNKS.is_dir():
        for old in CHUNKS.glob("chunk_*.json"):
            if old.name not in files:
                old.unlink()
    for name, text in files.items():
        kp.write_text(CHUNKS / name, text)
    kp.write_text(KEY, key_text)
    manifest = {
        "what": "G-block gold-free label chunks (PREREG_FINAL A39 d), TEACH-0 item format",
        "seed": SEED, "chunk_size": CHUNK, "n_items": len(key), "n_chunks": len(chunks),
        "qid": "q + HMAC-SHA256(secret, candidate id)[:10]; order seeded; key in label/key.json (never sent)",
        "candidates_sha256": sha256_file(CAND), "key_sha256": sha256_file(KEY),
        "chunks": {n: {"n": len(items), "sha256": hashlib.sha256(files[f'{n}.json'].encode()).hexdigest(),
                       "yes_no": sum(1 for i in items if i["kind"] == "yes/no")} for n, items in chunks},
    }
    kp.write_json(LABEL / "MANIFEST.json", manifest)
    kinds = Counter(r["qtype"] for r in out)
    build = {
        "ruling": "PREREG_FINAL A39 (b-e)", "seed": SEED, "target_total": TARGET_TOTAL, "quota_level_Q": Q,
        "domain_cap": DOMAIN_CAP, "min_per_card": MIN_PER_CARD, "token_cap": TOK_MAX,
        "render": {"decoder_io_sha256": DECODER_IO_SHA, "style": STYLE, "layout": LAYOUT,
                   "tokenizer_sha256": TOKENIZER_SHA,
                   "token_count": "len(tok.encode(CYGNET_SYSTEM + '\\n' + user_msg(row))) (= c_build/mixer.py)",
                   "check": "formats-1 loader_check (placeholder gold in memory only) + markers + definitions"},
        "yes_no_card": {"yes": "'- yes: <definition of yes>' (the admitted card's yes definition only)",
                        "both": "'- yes: <yes definition>\\n- no: <no definition>'"}[YESNO_CARD],
        "near_dup_pairs": [list(p) for p in NEAR_DUP_PAIRS],
        "near_dup_rule": "one card per text, so no text carries both cards of a pair (asserted)",
        "total": total, "kinds": dict(kinds), "max_domain_share": round(max(share.values()), 4),
        "domains": {d: {**stats[d], "share": round(share[d], 4)} for d in sorted(stats)},
        "cards_below_min": short, "dropped": drops,
        "inputs": {"admitted_sha256": sha256_file(ADMITTED),
                   "texts_sha256": {d: src_sha[d] for d in sorted(src_sha)}},
        "outputs": {"candidates_sha256": manifest["candidates_sha256"], "key_sha256": manifest["key_sha256"],
                    "n_chunks": len(chunks)},
    }
    kp.write_json(CAND_DIR / "build_stats.json", build)
    print(f"candidates {total} ({dict(kinds)}); Q={Q}; max domain share {max(share.values()):.3f}; "
          f"dropped {len(drops)}; chunks {len(chunks)}; cards below {MIN_PER_CARD}: "
          f"{[(s['card_id'], s['uses']) for s in short]}")
    for d in sorted(stats):
        s = stats[d]
        print(f"  {d:16s} texts {s['texts']:5d} kept {s['kept']:5d} ({share[d]:.3f}) tokens {s['tokens_min_med_max']} "
              + " ".join(f"{c.split('_', 1)[1]}={v['uses']}" for c, v in s["cards"].items()))


if __name__ == "__main__":
    if "--yesno-card" in sys.argv:
        YESNO_CARD = sys.argv[sys.argv.index("--yesno-card") + 1]
        assert YESNO_CARD in ("yes", "both"), YESNO_CARD
    main(force="--force" in sys.argv)
