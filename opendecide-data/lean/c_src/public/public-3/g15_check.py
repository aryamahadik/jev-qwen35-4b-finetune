#!/usr/bin/env python3
"""public-3 v1.1 G15 loader round-trip (spec G15; review-public3 fixes 1-2). Counts only, never prints row text.

Per output file (rows_r1, reserve, mtdev):
  - train_decoder.check_rows on the whole file (pinned A16 trainer c2c2d1d6);
  - formats-1's fmt1.card.loader_check on every row (decoder_io 908c08d7, cygnet + schema_branch_mark, random option
    order): option block exactly decoder_io's, every choice card line a '- {option}: {definition}' line of a shown
    option, yes/no cards printed whole with no '- Yes: ' / '- No: ' line, gold letter maps back, and every line of the
    row's moved guidance (the instructions text before the question wording) is in the prompt;
  - gold-letter round trip under 4 renders (cygnet / od x schema_branch_mark / text_first), random permutation;
  - every choice card line visible: each card line's definition text appears in the rendered cygnet prompt;
  - JSON-style states parse;
  - real-tokenizer length of the rendered prompt (cygnet system + user message, Qwen3.5 tokenizer in tmp/): max <= 7,900.
Writes logs/g15_check.json."""
from __future__ import annotations

import json
import random
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[2]
sys.path.insert(0, str(HERE / "lib"))
sys.path.insert(0, str(LEAN / "c_src" / "formats" / "formats-1"))
sys.path.insert(0, str(LEAN))
from common3 import LOGS, OUT, TMP, progress  # noqa: E402
import pools as P  # noqa: E402
from fmt1 import card as fcard  # noqa: E402

FILES = ("public3_rows_r1.jsonl", "public3_reserve.jsonl", "public3_mtdev.jsonl")
JSON_STYLES = {st["id"] for pool in (P.XED_STYLES, P.MAMS_STYLES, P.SAR_STYLES, P.POST_STYLES) for st in pool
               if st["wrap"].lstrip().startswith("{")}


def guide_of(r):
    """The guidance moved into instructions: every instructions line before the last (the question wording)."""
    lines = r["instructions"].split("\n")
    return "\n".join(lines[:-1]) if r["qtype"] == "choice" and len(lines) > 1 else ""


def main():
    dio = fcard._dio()
    td = fcard._td()
    from tokenizers import Tokenizer
    tok = Tokenizer.from_file(str(TMP / "tokenizer.json"))
    rep = {"decoder_io_sha256": fcard.DECODER_IO_SHA256, "train_decoder_sha256": fcard.TRAIN_DECODER_SHA256,
           "loader": "c_src/formats/formats-1/fmt1/card.py loader_check (cygnet, schema_branch_mark)", "files": {}}
    for name in FILES:
        rows = [json.loads(l) for l in open(OUT / name, encoding="utf-8")]
        st = Counter()
        td.check_rows(rows)                                      # raises on any unusable row
        st["check_rows_ok"] = len(rows)
        maxtok = 0
        for r in rows:
            g = guide_of(r)
            res = fcard.loader_check(r, must_show=[g] if g else [], seed="public3-g15", check_rows=False)
            if res["ok"]:
                st["loader_check_ok"] += 1
            else:
                st["loader_check_fail"] += 1
                for pr in res["problems"]:
                    st["problem:" + pr[:60]] += 1
            st[f"moved_guidance_rows:{r['qtype']}"] += bool(g)
            if r["meta"]["format_style"] in JSON_STYLES:
                try:
                    json.loads(r["state"])
                    st["json_state_ok"] += 1
                except ValueError:
                    st["json_state_bad"] += 1
            opts = ["Yes", "No"] if r["qtype"] == "noul" else r["options"]
            gold = ("Yes" if r["gold"] == 1 else "No") if r["qtype"] == "noul" else r["gold"]
            rnd = random.Random(f"public3-g15-4|{r['id']}")
            for style in ("cygnet", "od"):
                for layout in ("schema_branch_mark", "text_first"):
                    perm = list(range(len(opts)))
                    rnd.shuffle(perm)
                    saved = (dio.STYLE, dio.LAYOUT)
                    try:
                        dio.STYLE, dio.LAYOUT = style, layout
                        prompt = dio.user_msg(r, perm)
                    finally:
                        dio.STYLE, dio.LAYOUT = saved
                    if style == "od" and r["qtype"] == "noul":
                        ok = prompt.rstrip().endswith("Answer Yes or No.")
                    else:
                        letter = dio.label(perm.index(opts.index(gold)))
                        lines = prompt.split("\n")
                        ok = any(ln == f"{letter}. {gold}" or ln.startswith(f"{letter}. {gold}: ") for ln in lines)
                    st[f"gold_roundtrip_{style}_{layout}_{'ok' if ok else 'FAIL'}"] += 1
                    if style == "cygnet" and layout == "schema_branch_mark":
                        if r["card"]:
                            vis = all(" ".join(ln.split(": ", 1)[-1].split()) in " ".join(prompt.split())
                                      for ln in r["card"].split("\n") if ln.strip())
                            st[f"card_text_visible_{r['qtype']}_{'ok' if vis else 'FAIL'}"] += 1
                        n = len(tok.encode(dio.CYGNET_SYSTEM + "\n" + prompt).ids)
                        maxtok = max(maxtok, n)
        st["max_rendered_tokens_cygnet_sbm"] = maxtok
        assert maxtok <= 7900
        rep["files"][name] = dict(sorted(st.items()))
    (LOGS / "g15_check.json").write_text(json.dumps(rep, indent=1))
    bad = {n: {k: v for k, v in f.items() if "FAIL" in k or "fail" in k or "bad" in k or k.startswith("problem")}
           for n, f in rep["files"].items()}
    progress("g15_check: " + json.dumps({n: {"rows": f["check_rows_ok"], "loader_ok": f.get("loader_check_ok", 0),
                                              "max_tokens": f["max_rendered_tokens_cygnet_sbm"]}
                                          for n, f in rep["files"].items()}) + " problems " + json.dumps(bad))
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
