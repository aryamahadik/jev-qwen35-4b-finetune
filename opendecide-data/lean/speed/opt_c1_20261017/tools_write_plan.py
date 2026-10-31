"""Write run_plan.json: the machine-readable run plan (phases, commands, per-phase cost estimate, acceptance rules, status).

  ../../../.venv/bin/python tools_write_plan.py [--region any]
Everything printed or written is counts, numbers and command lines; no row text.
"""
import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from oc1 import common as C  # noqa: E402
from oc1 import configs as K  # noqa: E402
from oc1 import plan as PL  # noqa: E402

PY = "../../../.venv/bin/python"
MODAL = "../../../.venv/bin/modal"


def commands(region):
    env = f"MODAL_PROFILE={C.PROFILE}"
    return {
        "preflight (done)": f"{env} {MODAL} run modal_app.py::preflight",
        "export merged checkpoint (done, identical to S1's)": f"{env} {MODAL} run modal_app.py::export",
        "CPU dry run of the Python side (done)": f"{env} {MODAL} run modal_app.py::dryrun",
        "voice CPU smoke (see status)": f"{env} {MODAL} run modal_app.py::voicesmoke",
        "network probe, CPU (optional, USD 0.02)": f"{env} {MODAL} run modal_app.py::netprobe --regions any,us,us-east",
        "voice on a GPU (USD ~0.1, BEFORE the session)": f"{env} {MODAL} run modal_app.py::voicegpu --gpu L4",
        "print the session plan, start nothing": f"OC1_REGION={region} {env} {MODAL} run modal_app.py::session --plan-only",
        "THE H100 SESSION (needs the GO)": f"OC1_REGION={region} {env} {MODAL} run modal_app.py::session",
        "post-process (laptop, CPU)": f"{PY} -m oc1.report results/session_<ts>/volume/session_<ts>",
        "reconcile the bill": f"{env} {MODAL} billing report --for today --resolution h --show-resources",
        "stop everything and confirm 0 containers": f"{env} {MODAL} app list   # every row must read stopped; also: modal container list",
        "optional INT8 SmoothQuant calibration (L4, USD ~0.1)": f"{env} {MODAL} run modal_app.py::smoothgpu",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", default="any")
    ap.add_argument("--tests", default="")
    a = ap.parse_args()
    plan = PL.default_plan(a.region)
    est = PL.estimate(plan)
    b = C.Budget()
    out = {
        "task": "C1 optimisation tests, 17 Oct 2026 (build phase: nothing on a GPU has run)",
        "payer": C.PROFILE, "cap_usd": C.CAP_USD, "stop_launch_usd": C.STOP_LAUNCH_USD, "hard_stop_usd": C.HARD_STOP_USD,
        "spent_so_far": b.summary(),
        "model": {"c1": C.C1_MODEL, "adapter_sha256": C.C1_ADAPTER_SHA256, "merged": C.MERGED_NAME,
                  "merged_identical_to_speed2": True, "sglang": C.SGLANG_VERSION, "image": C.SGLANG_IMAGE},
        "plan": plan, "estimate": est,
        "configs": {n: {"desc": c.desc, "priority": c.priority, "flags": c.extra, "dropped": c.drop, "env_keys": sorted(c.env),
                        "measures": c.measures, "quantized": c.fp8, "note": c.note} for n, c in K.CONFIGS.items()},
        "order": K.order(), "commands": commands(a.region),
        "acceptance": {"parity_bar_argmax_agree": 0.995, "accuracy_diff_pt": 0.3, "accuracy_diff_pt_quantized": 1.0,
                       "reference": "bf16 S1 of the SAME session (gate), SPEED-2's stored S1 answers as a second check",
                       "rule": "a change that fails the bar is reported and never adopted; flips are listed with their margins"},
        "tests": a.tests,
    }
    Path(HERE / "run_plan.json").write_text(json.dumps(out, indent=1, default=str))
    print(PL.render(plan))
    print(f"wrote {HERE / 'run_plan.json'}")


if __name__ == "__main__":
    main()
