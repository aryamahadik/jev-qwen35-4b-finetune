#!/usr/bin/env python3
"""G15 loader round-trip for public-3 (independent checker, prep5/B4; counts only, never prints row text).

Re-runs the builder's g15_check.main() unchanged (read before use: train_decoder.check_rows on every file, formats-1
loader_check, gold-letter round trip under 4 renders with a random permutation, card text visible, JSON states parse,
real-tokenizer max <= 7,900) with its output redirected to qc/g15_check.json (the builder's logs are not touched),
then adds the spec G15 relation-unit rules the builder script does not test: every call_id unit has <= 3 rows, a unit
with a row >= 2,000 tokens has <= 2 rows; decoder_io / train_decoder / tokenizer sha256 equal the pinned A16 readout,
the A16 trainer and the mixer's TOKENIZER_SHA. Pass = no FAIL / fail / bad / problem counter, check_rows_ok ==
loader_check_ok == rows for every file, unit rules hold. Writes qc/g15.json."""
import contextlib, hashlib, io, json, sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
P3 = HERE.parent
LEAN = P3.parents[2]
sys.path.insert(0, str(P3))
sys.path.insert(0, str(P3 / "lib"))
import g15_check as G  # noqa: E402

TOKENIZER_SHA = "5f9e4d4901a92b997e463c1f46055088b6cca5ca61a6522d1b9f64c4bb81cb42"   # c_build/mixer.py TOKENIZER_SHA


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    G.LOGS = HERE
    G.progress = lambda *a, **k: None
    with contextlib.redirect_stdout(io.StringIO()):
        G.main()
    rep = json.load(open(HERE / "g15_check.json"))
    prob = []
    pins = {"decoder_io": sha(LEAN / "decoder_io.py") == G.fcard.DECODER_IO_SHA256,
            "train_decoder": sha(LEAN / "train_decoder.py") == G.fcard.TRAIN_DECODER_SHA256,
            "tokenizer": sha(G.TMP / "tokenizer.json") == TOKENIZER_SHA}
    prob += [f"pin {k}" for k, v in pins.items() if not v]
    files = {}
    from tokenizers import Tokenizer
    tok = Tokenizer.from_file(str(G.TMP / "tokenizer.json"))
    dio = G.fcard._dio()
    for name, st in rep["files"].items():
        rows = [json.loads(l) for l in open(G.OUT / name)]
        bad = {k: v for k, v in st.items() if "FAIL" in k or "fail" in k or "bad" in k or k.startswith("problem")}
        units = defaultdict(list)
        for r in rows:
            units[r["call_id"]].append(r)
        big_units = 0
        for u in units.values():
            if any(len(tok.encode(dio.CYGNET_SYSTEM + "\n" + dio.user_msg(r, list(range(len(r["options"] or [0, 1])))))
                   .ids) >= 2000 for r in u) and len(u) > 2:
                big_units += 1
        f = {"rows": len(rows), "check_rows_ok": st.get("check_rows_ok"), "loader_check_ok": st.get("loader_check_ok"),
             "gold_roundtrip_ok_min": min(v for k, v in st.items() if k.startswith("gold_roundtrip") and k.endswith("_ok")),
             "fail_counters": bad, "max_rendered_tokens_cygnet_sbm": st["max_rendered_tokens_cygnet_sbm"],
             "call_id_units": len(units), "max_rows_per_unit": max(len(u) for u in units.values()),
             "units_ge2000tok_over_2_rows": big_units}
        if bad or not (f["check_rows_ok"] == f["loader_check_ok"] == f["gold_roundtrip_ok_min"] == len(rows)) \
                or f["max_rows_per_unit"] > 3 or big_units or f["max_rendered_tokens_cygnet_sbm"] > 7900:
            prob.append(name)
        files[name] = f
    out = {"gate": "G15", "pass": not prob, "problems": prob, "pins": pins, "files": files,
           "detail": "qc/g15_check.json (builder g15_check.main, output redirected)"}
    (HERE / "g15.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out)[:2000])


if __name__ == "__main__":
    main()
