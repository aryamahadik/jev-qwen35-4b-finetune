"""G15 loader round-trip (C_DATA_SPEC v4 8 G15), independent re-run on public-2's current rows, reserve and dev.
Pinned A16 trainer/readout (train_decoder c2c2d1d6, decoder_io 908c08d7), served prompt cygnet / schema_branch_mark.
1. train_decoder.check_rows(file, kd=0.5) accepts every row (raises otherwise);
2. each row rendered by decoder_io.user_msg under a seeded random permutation; the 'Options:' block is parsed back
   from the PROMPT TEXT, the line showing the gold option gives the displayed letter, and that letter is mapped back
   through train_decoder.inverse_perm to a canonical option: it must be the canonical gold (100%); the repeated
   'Options: ...' branch line must show the same letter for the gold;
3. nothing in the card is hidden: yes/no rows print the card whole; on choice rows every non-empty card line is a
   '- {shown option}: {definition}' line;
4. relation units: rows per call_id <= 3, and <= 2 when a row has >= 2,000 tokens;
5. real-tokenizer length of the chat render (Qwen/Qwen3.5-4B, CYGNET system) <= 7,900 for every row.
"""
import hashlib
import random
import sys
from collections import Counter

from qclib import FILES, LEAN, QC, load_all, sha256_file, write_gate

PINS = {"train_decoder.py": "c2c2d1d623ccd53f64254fb41400f5c952b4e1324d11550a01f170ab25ba04ef",
        "decoder_io.py": "908c08d752ce8896c2628a06f8a9d3153df8c76b657bf29daae44656f75f2948"}


def main():
    for f, want in PINS.items():
        assert sha256_file(LEAN / f) == want, f"{f} is not the A16 pin"
    sys.path.insert(0, str(LEAN))
    import decoder_io as dio
    import train_decoder as td
    dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", local_files_only=True)
    data = load_all()
    nums, bad, calls, long_calls = {}, [], Counter(), set()
    samples = {}
    for fn in FILES:
        rows = data[fn]
        td.check_rows(rows, kd=0.5)
        probs, toks = Counter(), []
        for r in rows:
            rid = r["id"]
            p = []
            lr = dio.as_letter_row(r)
            opts, gold = lr["options"], lr["gold"]
            rng = random.Random(int.from_bytes(hashlib.sha256(f"p2-qc-g15:{rid}".encode()).digest()[:8], "big"))
            perm = list(range(len(opts)))
            rng.shuffle(perm)
            prompt = dio.user_msg(r, perm)
            lines = prompt.split("\n")
            defs = dio.card_defs(r.get("card"))
            try:
                i0 = lines.index("Options:") + 1
            except ValueError:
                i0 = None
                p.append("no_options_block")
            letter = None
            if i0 is not None:
                block = lines[i0:i0 + len(opts)]
                for j, ln in enumerate(block):
                    lab = dio.label(j) + ". "
                    if not ln.startswith(lab):
                        p.append("option_line_letter")
                        break
                    txt = ln[len(lab):]
                    if txt == gold or (gold in defs and txt == f"{gold}: {defs[gold]}"):
                        letter = j if letter is None else -1
                if letter is None or letter < 0:
                    p.append("gold_not_shown_once")
                else:
                    back = [i for i, d in enumerate(td.inverse_perm(perm)) if d == letter]
                    if len(back) != 1 or opts[back[0]] != gold:
                        p.append("letter_maps_to_wrong_option")
                    br = [x for x in lines if x.startswith("Options: ")]
                    # exact branch line (an option may itself contain '; ', so no split): the entry at the
                    # displayed letter is the gold
                    shown = [opts[i] for i in perm]
                    exp = "Options: " + "; ".join(f"{dio.label(i)}. {o}" for i, o in enumerate(shown))
                    if not br or br[-1] != exp or shown[letter] != gold:
                        p.append("branch_letter")
            card = r.get("card")
            if card:
                if r["qtype"] == "noul":
                    if f"Definitions:\n{card}" not in prompt:
                        p.append("yn_card_not_whole")
                else:
                    for ln in card.split("\n"):
                        if ln.strip() and not (ln.startswith("- ") and ": " in ln
                                               and ln[2:].split(": ", 1)[0] in r["options"]):
                            p.append("choice_card_line_hidden")
                            break
            n = len(tok(dio.render_chat(tok, dio.CYGNET_SYSTEM, prompt), add_special_tokens=False)["input_ids"])
            toks.append(n)
            if n > 7900:
                p.append("over_7900_tokens")
            calls[r["call_id"]] += 1
            if n >= 2000:
                long_calls.add(r["call_id"])
            key = f"{r['source']}|{r['meta']['framing']}"
            if fn == "rows_r1" and len(samples.setdefault(key, [])) < 20:
                samples[key].append(rid)
            for x in p:
                probs[x] += 1
            if p:
                bad.append([fn, rid, p])
        toks.sort()
        nums[fn] = {"rows": len(rows), "check_rows_kd0.5": "pass", "rows_with_problems": sum(1 for b in bad if b[0] == fn),
                    "problems": dict(probs), "tokens_max": toks[-1], "tokens_median": toks[len(toks) // 2],
                    "rows_ge_2000_tokens": sum(t >= 2000 for t in toks), "rows_over_7900": sum(t > 7900 for t in toks)}
    over3 = sum(1 for v in calls.values() if v > 3)
    long_over2 = sum(1 for c in long_calls if calls[c] > 2)
    nums["call_ids"] = {"distinct": len(calls), "max_rows_per_call_id": max(calls.values()),
                        "units_over_3_rows": over3, "long_units_over_2_rows": long_over2}
    nums["gold_round_trip_match_rate"] = 1 - len(bad) / sum(len(v) for v in data.values())
    ok = not bad and not over3 and not long_over2
    write_gate("G15", ok, nums, bad_ids=bad[:20], sample_ids_20_per_framing=samples,
               pins={k: v[:16] for k, v in PINS.items()}, prompt="cygnet / schema_branch_mark",
               tokenizer="Qwen/Qwen3.5-4B (local cache); dio.render_chat(tok, CYGNET_SYSTEM, user_msg)")
    print("G15", ok, {k: (v.get("rows_with_problems") if isinstance(v, dict) else v) for k, v in nums.items()})


if __name__ == "__main__":
    main()
