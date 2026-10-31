"""public-2 G15 loader round-trip (C_DATA_SPEC.md v4 G15; recipe v4 data checks 2 and 4) on rows, reserve and dev.

Runs the pinned A16 trainer and readout as programs (train_decoder.py c2c2d1d6, decoder_io.py 908c08d7) in the trained
and served prompt (OD_STYLE=cygnet, LAYOUT=schema_branch_mark, as runs/q35_4b_c_r1.json):
  1. train_decoder.check_rows(all rows, kd=0.5) accepts every row;
  2. every row rendered by decoder_io.user_msg under a seeded random option order: the option block is decoder_io's,
     and the gold letter maps back to the gold option in the schema option list AND in the repeated 'Options:' line;
  3. card visibility: yes/no rows print the card whole under 'Definitions:'; on choice rows every non-empty card line
     is a '- {option}: {definition}' line of a shown option (one per option), so nothing in the card is hidden;
  4. nothing of the v1 card is lost: every non-empty line of the candidate's original card (tmp/cand_*.jsonl) is in the
     prompt (a definition line '- X: d' as the option line 'X: d');
  5. the formats-1 shared check fmt1.card.loader_check (same pins) passes with that must_show list;
  6. every call_id holds 1 row; real chat-render tokens <= 7,900 (and < 2,000: no long rows).
Writes out/g15_report.json and tmp/fix/g15_samples.txt (20 rendered prompts per dataset x framing, for reading).
"""
from __future__ import annotations

import hashlib
import json
import random
import sys
from collections import Counter, defaultdict

from p2_common import HERE, LEAN, OUT, TMP, sha256_file

TRAIN_DECODER_SHA256 = "c2c2d1d623ccd53f64254fb41400f5c952b4e1324d11550a01f170ab25ba04ef"
DECODER_IO_SHA256 = "908c08d752ce8896c2628a06f8a9d3153df8c76b657bf29daae44656f75f2948"
FILES = ("rows_r1", "reserve_r1", "dev_mt_r1")


def _norm(s):
    return " ".join(str(s).split())


def main():
    for p, want in ((LEAN / "train_decoder.py", TRAIN_DECODER_SHA256), (LEAN / "decoder_io.py", DECODER_IO_SHA256)):
        got = sha256_file(p)
        if got != want:
            raise SystemExit(f"{p.name} sha256 {got[:12]} is not the A16 pin {want[:12]}")
    sys.path.insert(0, str(LEAN))
    import decoder_io as dio
    import train_decoder as td
    dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
    sys.path.insert(0, str(LEAN / "c_src" / "formats" / "formats-1"))
    from fmt1 import card as fcard
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", local_files_only=True)

    orig_card = {}
    for n in ("cand_hybridqa", "cand_wikisql", "cand_drop", "cand_uci"):
        for line in open(TMP / f"{n}.jsonl"):
            c = json.loads(line)
            orig_card[c["id"]] = c.get("card")

    rep = {"pins": {"train_decoder": TRAIN_DECODER_SHA256[:16], "decoder_io": DECODER_IO_SHA256[:16],
                    "style": dio.STYLE, "layout": dio.LAYOUT, "kd": 0.5}, "files": {}}
    samples = defaultdict(list)
    all_calls = Counter()
    for fn in FILES:
        rows = [json.loads(l) for l in open(OUT / f"{fn}.jsonl")]
        td.check_rows(rows, kd=0.5)  # raises on any unusable row
        probs = Counter()
        bad_ids = []
        toks = []
        routes = Counter()
        for r in rows:
            all_calls[r["call_id"]] += 1
            rid = r["id"]
            p = []
            rng = random.Random(int.from_bytes(hashlib.sha256(f"p2-g15:{rid}".encode()).digest()[:8], "big"))
            if r["qtype"] == "choice":
                opts = list(r["options"])
                gold = r["gold"]
            else:
                opts, gold = ["Yes", "No"], ("Yes" if r["gold"] == 1 else "No")
            perm = list(range(len(opts)))
            rng.shuffle(perm)
            prompt = dio.user_msg(r, perm)
            defs = dio.card_defs(r.get("card"))
            shown = [opts[i] for i in perm]
            labs = [dio.label(i) for i in range(len(opts))]
            head = (f"Definitions:\n{r['card']}\n\n" if r["qtype"] == "noul" and r.get("card") else "") \
                + r["instructions"].rstrip() + "\n\nOptions:\n"
            if not prompt.startswith(head):
                p.append("head")
                lines = []
            else:
                lines = prompt[len(head):].split("\n")[:len(opts)]
            want = [f"{labs[j]}. {o}" + (f": {defs[o]}" if o in defs else "") for j, o in enumerate(shown)]
            if lines != want:
                p.append("option_block")
            j = perm.index(opts.index(gold))  # the displayed letter of the gold option
            if not (lines and (lines[j] == f"{labs[j]}. {gold}" or lines[j].startswith(f"{labs[j]}. {gold}: "))):
                p.append("gold_letter_schema")
            branch = [x for x in prompt.split("\n") if x.startswith("Options: ")]
            if not branch or branch[-1] != "Options: " + "; ".join(f"{labs[i]}. {o}" for i, o in enumerate(shown)):
                p.append("branch_options")
            elif f"; {labs[j]}. {gold};" not in "; " + branch[-1][len("Options: "):] + ";":
                p.append("gold_letter_branch")
            # 3) card visibility
            if r.get("card"):
                if r["qtype"] == "noul":
                    if f"Definitions:\n{r['card']}" not in prompt:
                        p.append("yn_card_not_whole")
                    if any(k in ("Yes", "No") for k in defs):
                        p.append("yn_card_glued_line")
                else:
                    keys = []
                    for ln in r["card"].split("\n"):
                        if not ln.strip():
                            continue
                        if not (ln.startswith("- ") and ": " in ln and ln[2:].split(": ", 1)[0] in opts):
                            p.append("choice_card_line_hidden")
                            break
                        keys.append(ln[2:].split(": ", 1)[0])
                    if len(keys) != len(set(keys)):
                        p.append("choice_card_dup_option")
            # 4) every line of the v1 card is in the prompt
            oc = orig_card.get(rid)
            must = []
            if oc:
                np_ = _norm(prompt)
                for ln in oc.split("\n"):
                    if not ln.strip():
                        continue
                    t = ln[2:] if (r["qtype"] == "choice" and ln.startswith("- ") and ": " in ln
                                   and ln[2:].split(": ", 1)[0] in opts) else ln
                    must.append(t)
                    if _norm(t) not in np_:
                        p.append("v1_card_line_missing")
                        break
            elif rid not in orig_card:
                p.append("no_candidate")
            # 5) shared formats-1 check
            fr = fcard.loader_check(r, must_show=["\n".join(must)] if must else [], perm=perm, check_rows=False)
            if not fr["ok"]:
                p.append("fmt1_loader_check:" + fr["problems"][0][:60])
            # 6) tokens
            n = len(tok(dio.render_chat(tok, dio.CYGNET_SYSTEM, prompt), add_special_tokens=False)["input_ids"])
            toks.append(n)
            if n > 7900:
                p.append("over_7900")
            routes[str(r["meta"].get("card_route"))] += 1
            key = (r["source"], r["meta"]["framing"])
            if fn == "rows_r1" and len(samples[key]) < 20:
                samples[key].append((rid, n, prompt))
            for x in p:
                probs[x] += 1
            if p:
                bad_ids.append((rid, p))
        rep["files"][fn] = {"rows": len(rows), "check_rows_kd0.5": "pass", "rows_with_problems": len(bad_ids),
                            "problems": dict(probs), "bad_ids": bad_ids[:10], "tokens_max": max(toks),
                            "tokens_median": sorted(toks)[len(toks) // 2], "rows_ge_2000": sum(t >= 2000 for t in toks),
                            "card_route": dict(routes)}
    multi = {k: v for k, v in all_calls.items() if v > 1}
    rep["call_ids"] = {"distinct": len(all_calls), "with_more_than_1_row": len(multi)}
    rep["ok"] = all(v["rows_with_problems"] == 0 for v in rep["files"].values()) and not multi
    json.dump(rep, open(OUT / "g15_report.json", "w"), indent=1)
    (TMP / "fix").mkdir(exist_ok=True)
    with open(TMP / "fix" / "g15_samples.txt", "w") as f:
        for key in sorted(samples):
            for rid, n, pr in samples[key]:
                f.write(f"\n{'=' * 100}\n{key} {rid} tokens={n}\n{'=' * 100}\n{pr}\n")
    print(json.dumps({k: (v if k != "files" else {f: {kk: vv for kk, vv in d.items() if kk != "bad_ids"}
                                                  for f, d in v.items()}) for k, v in rep.items()}))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
