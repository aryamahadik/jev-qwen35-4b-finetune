"""l1_look.l1reader: the read client of the L1 look. It IS grid_h100.reader.GridReader (same tokenizer, same P7 prompt-sha check, same readout, same
SGLang /generate calls, same pred-file format), with two differences that the sealed side needs:

  * a set may arrive IN MEMORY (spec["rows"], held to spec["rows_sha256"]) instead of as a data file: the sealed rows are never written under
    a data folder or a path the grid tools would have to guard;
  * the daemon never lets a message that could hold item text leave the process: an error is reported by its CLASS NAME only, and the process
    prints nothing but 'L1R:' lines (counts and seconds).

Runs under C1's PINNED35 stack (/opt/fastpath/bin/python), as grid_h100.reader does:  python -m l1_look.l1reader serve --spec <spec.json>
The readout is unchanged: choice rows read in the given order and the exact reversal and averaged in probability space, yes/no once, T = 1.0
as served (the temperature of the look is applied afterwards, on the laptop, by l1temp.apply_T).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from grid_h100 import common as C
from grid_h100 import reader as RD

dio, R, SH = RD.dio, RD.R, RD.SH


def say(msg: str):
    print("L1R: " + msg, flush=True)


class L1Reader(RD.GridReader):
    def init(self) -> dict:
        for s in self.specs:                                                # an in-memory set is bound to its hash before anything is read
            if s.get("rows") is not None:
                if C.canon_sha(s["rows"]) != s.get("rows_sha256"):
                    raise SystemExit("l1reader: the in-memory set differs from its hash")
                self.manifest[s["file"]] = {"sha256": s["rows_sha256"], "rows": len(s["rows"])}
        return super().init()

    def _prepare(self, spec):
        if spec.get("rows") is None:
            return super()._prepare(spec)
        C.check_names(spec["split"])
        if spec["perm_seed"] is not None:
            raise SystemExit("l1reader: an in-memory set is read in its given order (perm_seed None)")
        rows = spec["rows"]
        per_row = [RD.items_for_row(self.ro, r, spec["views"], None) for r in rows]
        flat = [it for items in per_row for it in items]
        R.render_items(self.ro, flat)
        for i in range(0, len(flat), 2000):
            R.tokenize_items(self.tok, flat[i:i + 2000])
        long = [it.n_tokens for it in flat if it.n_tokens >= SH.CONTEXT_LEN]
        if long:
            raise SystemExit(f"l1reader: {len(long)} prompt(s) over the context length in set {spec['split']}")
        chunks = []
        for i in range(0, len(rows), self.chunk):
            its = []
            for j, items in enumerate(per_row[i:i + self.chunk]):
                for it in items:
                    it.q = j
                    its.append(it)
            chunks.append((i, rows[i:i + self.chunk], its))
        return RD.SetData(spec, rows, chunks, sum(it.n_tokens for it in flat))


def _safe(e: BaseException) -> str:
    """A SystemExit message is authored by this code (a rule, a count); every other exception is reported by its class only."""
    return (str(e)[:300] if isinstance(e, SystemExit) else type(e).__name__)


def serve(spec: dict) -> int:
    """Control-file loop of grid_h100.reader.serve, with sanitised errors: ctl_dir/cmd_<k>.json -> res_<k>.json; ready.json after init."""
    ctl = Path(spec["ctl_dir"])
    ctl.mkdir(parents=True, exist_ok=True)
    gr = L1Reader(spec["c1_dir"], spec["data_dir"], spec["sets"], spec.get("manifest"), spec.get("recorded_check"), spec.get("port", C.PORT),
                  spec.get("workers", 16), spec.get("chunk", 8), log=lambda s: None)
    try:
        info = gr.init()
    except BaseException as e:  # noqa: BLE001
        C.write_json(ctl / "ready.json", {"ok": False, "error": _safe(e)})
        say("init failed")
        return 3
    C.write_json(ctl / "ready.json", {"ok": True, "info": info})
    say(f"ready sets {info.get('sets')} tokens {info.get('tokens')} init_s {info.get('init_s')}")
    k = 0
    while not (ctl / "quit").exists():
        f = ctl / f"cmd_{k}.json"
        if not f.exists():
            time.sleep(0.5)
            continue
        cmd = json.loads(f.read_text())
        try:
            res = gr.run_model(cmd)
            res["ok"] = True
            say(f"model {cmd.get('read_name')} done wall_s {res.get('wall_s')}")
        except BaseException as e:  # noqa: BLE001
            res = {"ok": False, "error": _safe(e), "read_name": cmd.get("read_name")}
            say(f"model {cmd.get('read_name')} failed {type(e).__name__}")
        C.write_json(ctl / f"res_{k}.json", res)
        k += 1
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["serve"])
    ap.add_argument("--spec", required=True)
    a = ap.parse_args(argv)
    return serve(json.loads(Path(a.spec).read_text()))


if __name__ == "__main__":
    sys.exit(main())
