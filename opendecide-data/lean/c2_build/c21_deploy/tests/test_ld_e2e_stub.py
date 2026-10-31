"""End-to-end CPU test of capacity_ladder.py / make_probe_body.py through the real round-2 harness (oc1) against oc1's model-free
StubSGLang. Needs the C1 tokenizer folder (backups/modal_models/q35_4b_main500k); skipped without it. No model, no GPU."""
import json
import os
import sys
from pathlib import Path

import pytest

SC = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SC))
import capacity_ladder as CL  # noqa: E402
import common as C  # noqa: E402

TOK = Path("/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k")
STAGE = C.LEAN / "speed" / "opt_c1_round2_20261017" / "stage"
WL = C.LEAN / "speed" / "workloads"
pytestmark = pytest.mark.skipif(not (TOK.exists() and STAGE.exists() and (WL / "N.jsonl").exists()), reason="C1 tokenizer / harness not present")


def test_capacity_ladder_against_stub(tmp_path, monkeypatch):
    monkeypatch.setenv("HF_HUB_OFFLINE", "1")
    monkeypatch.setenv("OC1_TMP", str(tmp_path))
    monkeypatch.setenv("LD_WINDOW", "W-stub")
    monkeypatch.setattr(C, "c2_busy", lambda: [])
    for name, n in (("N", 40), ("P", 120)):
        rows = [json.loads(l) for l in open(WL / f"{name}.jsonl")][:n]
        (tmp_path / f"{name}.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    for p in (str(STAGE), str(C.LEAN / "hosting"), str(C.LEAN)):
        sys.path.insert(0, p)
    from oc1.stubserver import StubSGLang
    srv = StubSGLang(port=0, service_ms=10.0).start()
    try:
        out = tmp_path / "cap.json"
        rc = CL.main(["--port", str(srv.port), "--tokenizer", str(TOK), "--work-dir", str(tmp_path), "--oc1-parent", str(STAGE),
                      "--phases", "ladder,open", "--concs", "1,4", "--runs", "1", "--open-fracs", "0.5", "--open-secs", "3", "--out", str(out)])
        d = json.loads(out.read_text())
        assert rc == 0 and d["tag_ladder"]["tag"] == "author-run"
        pts = {p["c"]: p for p in d["phases"]["ladder"]["points"]}
        assert pts[4]["dph"] > 1.5 * pts[1]["dph"]                      # 10 ms stub service, threads overlap
        lv = d["phases"]["open"]["levels"][0]
        assert lv["failed"] == 0 and lv["ok"] > 5
    finally:
        srv.close()
