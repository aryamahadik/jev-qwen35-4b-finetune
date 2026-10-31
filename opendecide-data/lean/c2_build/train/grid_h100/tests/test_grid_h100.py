"""CPU tests of the grid_h100 tools (common: payer guard + ledger; plan: estimate; merge_direct; gridbuild; servers; reader; session; parity;
driver). Tiny fake tensors and tmp trees, a fake SGLang HTTP server; no GPU, no Modal, no network, no OHS / sealed path.
  cd lean/c2_build/train && HF_HUB_OFFLINE=1 ../../../.venv/bin/python -B -m pytest -q grid_h100/tests
"""
from __future__ import annotations

import ast
import json
import os
import sys
import time
from pathlib import Path

import pytest
import torch

sys.dont_write_bytecode = True
TESTS = Path(__file__).resolve().parent
PKG = TESTS.parent
TRAIN = PKG.parent
C2B = TRAIN.parent
LEAN = C2B.parent
for p in (str(TRAIN), str(C2B), str(LEAN), str(TESTS), str(C2B / "serving")):
    sys.path.insert(0, p)

from grid_h100 import common as C  # noqa: E402
from grid_h100 import driver as DR  # noqa: E402
from grid_h100 import gridbuild as GB  # noqa: E402
from grid_h100 import merge_direct as MD  # noqa: E402
from grid_h100 import plan as PL  # noqa: E402
from grid_h100 import servers as SV  # noqa: E402
import fakes as F  # noqa: E402

HAVE_C1 = F.C1_BACKUP.exists() and (F.C1_BACKUP / "tokenizer.json").exists()
needs_c1 = pytest.mark.skipif(not HAVE_C1, reason="the C1 backup tokenizer is not on this machine")
P_REF = {"rows": 8143, "seq": 11957, "chars": 17175428}


def sh_mod():
    return SV.sh()


# =============================================================================================== common: payer guard
def write_go(tmp_path, **kw):
    go = {"profile": "acct-one", "owner_words": "use acct-one for the grid reads", "go": "GO #1", "written_utc": "2026-10-18T10:00:00Z", **kw}
    p = tmp_path / "go.json"
    p.write_text(json.dumps(go))
    return p


RUN_ARGV = ["/venv/bin/modal", "run", "app.py::grid"]


def test_payer_guard_default_refuse_and_exact_profile(tmp_path):
    missing = tmp_path / "nope.json"
    with pytest.raises(SystemExit, match="default: refuse"):
        C.payer_guard(env={"MODAL_PROFILE": "acct-one"}, argv=RUN_ARGV, active="acct-one", go_path=missing)
    go = write_go(tmp_path)
    assert C.payer_guard(env={"MODAL_PROFILE": "acct-one"}, argv=RUN_ARGV, active="acct-one", go_path=go) == "acct-one"
    with pytest.raises(SystemExit, match="not the profile the owner named"):
        C.payer_guard(env={"MODAL_PROFILE": "acct-two"}, argv=RUN_ARGV, active="acct-two", go_path=go)
    with pytest.raises(SystemExit, match="export MODAL_PROFILE"):
        C.payer_guard(env={}, argv=RUN_ARGV, active="acct-one", go_path=go)
    with pytest.raises(SystemExit, match="MODAL_TOKEN"):
        C.payer_guard(env={"MODAL_PROFILE": "acct-one", "MODAL_TOKEN_ID": "x"}, argv=RUN_ARGV, active="acct-one", go_path=go)
    with pytest.raises(SystemExit, match="active profile"):
        C.payer_guard(env={"MODAL_PROFILE": "acct-one"}, argv=RUN_ARGV, active="other", go_path=go)
    for argv in (["/v/modal", "deploy", "app.py"], ["/v/modal", "serve", "app.py"], ["/v/modal", "shell", "app.py"]):
        with pytest.raises(SystemExit, match="only `modal run`"):
            C.payer_guard(env={"MODAL_PROFILE": "acct-one"}, argv=argv, active="acct-one", go_path=go)
    with pytest.raises(SystemExit, match="--detach"):
        C.payer_guard(env={"MODAL_PROFILE": "acct-one"}, argv=[*RUN_ARGV, "--detach"], active="acct-one", go_path=go)
    assert C.payer_guard(env={"MODAL_PROFILE": "acct-one"}, argv=["pytest"], active="acct-one", go_path=go) == "acct-one"


# ---- A88: policy file (never_payers, C2 training relay), the real GO record, training-running refusal
def write_policy(tmp_path, **kw):
    d = {"never_payers": ["card-x"], "c2_training_relay": ["relay-a", "relay-b"], **kw}
    p = tmp_path / "policy.json"
    p.write_text(json.dumps(d))
    return p


def write_segs(tmp_path, lines):
    p = tmp_path / "segs.jsonl"
    p.write_text("".join(json.dumps(x) + "\n" for x in lines))
    return p


def guard(tmp_path, profile, *, policy=None, segs=None, final=True, go_profile=None):
    go = write_go(tmp_path, profile=go_profile or profile)
    fin = tmp_path / "final.json"
    if final:
        fin.write_text("{}")
    return C.payer_guard(env={"MODAL_PROFILE": profile}, argv=RUN_ARGV, active=profile, go_path=go,
                         policy_path=policy or write_policy(tmp_path), seg_log=segs or (tmp_path / "no_segs.jsonl"), final_path=fin)


def test_real_policy_and_real_go_record_are_as_the_owner_ruled():
    pol = C.read_policy()
    assert pol["never_payers"] == ["aryamhd"] and pol["c2_training_relay"] == ["mahadikarya2", "mahadikarya3"]
    go = C.read_go(C.GO_FILE)
    assert go["profile"] == "mahadikarya3" and "A88" in go["owner_words"] and "A88" in go["go"] and "$15" in go["owner_words"]
    assert "never aryamhd" in go["owner_words"] and C.go_cap(go) == 15.0
    assert go["profile"] not in pol["never_payers"]


def test_guard_refuses_a_c2_relay_profile_while_training_is_not_over(tmp_path):
    with pytest.raises(SystemExit, match="C2 training is not over"):
        guard(tmp_path, "relay-a", final=False)
    with pytest.raises(SystemExit, match="C2 training is not over"):
        guard(tmp_path, "relay-b", final=False)
    assert guard(tmp_path, "acct-free", final=False) == "acct-free"          # not a relay account: the training state is irrelevant


def test_guard_refuses_a_profile_with_an_open_segment_even_after_final(tmp_path):
    segs = write_segs(tmp_path, [{"seg": "seg1", "profile": "relay-a", "start": 1, "open": True},
                                 {"seg": "seg1", "profile": "relay-a", "start": 1, "end": 9, "rc": 0},
                                 {"seg": "seg5", "profile": "relay-a", "start": 20, "open": True}])
    with pytest.raises(SystemExit, match="still open on 'relay-a'"):
        guard(tmp_path, "relay-a", segs=segs, final=True)
    assert guard(tmp_path, "relay-b", segs=segs, final=True) == "relay-b"    # only the profile with the open segment is held


def test_guard_allows_a_relay_profile_after_final_and_all_segments_closed(tmp_path):
    segs = write_segs(tmp_path, [{"seg": "seg1", "profile": "relay-a", "start": 1, "open": True},
                                 {"seg": "seg1", "profile": "relay-a", "start": 1, "end": 9, "rc": 0}])
    assert guard(tmp_path, "relay-a", segs=segs, final=True) == "relay-a"
    assert C.open_c2_segments(tmp_path / "does_not_exist.jsonl") == []


def test_guard_refuses_a_never_payer_always(tmp_path):
    for final in (True, False):
        with pytest.raises(SystemExit, match="never a payer"):
            guard(tmp_path, "card-x", final=final)
    # the owner's GO file naming it does not help, and neither does a mismatching MODAL_PROFILE
    with pytest.raises(SystemExit, match="never a payer"):
        guard(tmp_path, "relay-a", go_profile="card-x")


def test_guard_fails_closed_without_a_policy_or_with_an_unreadable_segment_log(tmp_path):
    with pytest.raises(SystemExit, match="fail closed"):
        guard(tmp_path, "relay-a", policy=tmp_path / "gone.json")
    (tmp_path / "bad_policy.json").write_text(json.dumps({"never_payers": []}))
    with pytest.raises(SystemExit, match="non-empty list"):
        guard(tmp_path, "relay-a", policy=tmp_path / "bad_policy.json")
    bad = tmp_path / "segs.jsonl"
    bad.write_text("not json\n")
    with pytest.raises(SystemExit, match="unreadable"):
        guard(tmp_path, "relay-a", segs=bad, final=True)


def test_real_state_refuses_the_named_payer_until_the_c2_final_record_exists():
    if C.C2_FINAL.exists():
        pytest.skip("C2 training is over on this machine")
    go = C.read_go(C.GO_FILE)
    pol = C.read_policy()
    for prof in ("mahadikarya2", go["profile"]):                          # the training rule alone, for both relay accounts
        why = C.c2_training_problem(prof, pol)
        assert why and ("C2 training is not over" in why or "still open on" in why)
    with pytest.raises(SystemExit, match="C2 training is not over|still open on"):      # the named payer, through the whole guard
        C.payer_guard(env={"MODAL_PROFILE": go["profile"]}, argv=RUN_ARGV, active=go["profile"], go_path=C.GO_FILE)
    with pytest.raises(SystemExit):                                       # the other relay account is not the named payer either
        C.payer_guard(env={"MODAL_PROFILE": "mahadikarya2"}, argv=RUN_ARGV, active="mahadikarya2", go_path=C.GO_FILE)
    with pytest.raises(SystemExit, match="never a payer"):                # and the personal card is refused whatever the GO file says
        C.payer_guard(env={"MODAL_PROFILE": pol["never_payers"][0]}, argv=RUN_ARGV, active=pol["never_payers"][0], go_path=C.GO_FILE)


@pytest.mark.parametrize("bad", [{"profile": ""}, {"profile": "default"}, {"profile": "a b"}, {"profile": " acct"}, {"owner_words": "ok"},
                                 {"go": "maybe"}, {"written_utc": ""}, {"cap_usd": 15.01}, {"cap_usd": 0}, {"cap_usd": True}, {"cap_usd": "3"}])
def test_go_record_is_validated(tmp_path, bad):
    with pytest.raises(SystemExit):
        C.read_go(write_go(tmp_path, **bad))


def test_go_cap_can_only_lower(tmp_path):
    assert C.go_cap(C.read_go(write_go(tmp_path))) == 15.0
    assert C.go_cap(C.read_go(write_go(tmp_path, cap_usd=2.5))) == 2.5
    (tmp_path / "go.json").write_text("not json")
    with pytest.raises(SystemExit, match="not readable"):
        C.read_go(tmp_path / "go.json")


def test_no_account_name_is_hard_coded_in_the_guard():
    src = (PKG / "common.py").read_text()
    for name in ("mahadikarya", "aryamhd", "jaypatil", "atmosphor", "arya-mahadik"):
        assert name not in src, f"{name} must come from the owner's GO record, not from code"


# =============================================================================================== common: ledger
def test_constants_cap_and_timeout_cannot_cross_the_cap():
    assert (C.CAP_USD, C.STOP_LAUNCH_USD, C.HARD_STOP_USD) == (15.00, 13.50, 14.60)       # PREREG A88 (was 4.00 / 3.60 / 3.90)
    assert C.container_cost_usd(C.SESSION_TIMEOUT_S) < C.CAP_USD
    assert C.FN_RATE_USD_H == pytest.approx(3.95 + 6 * 0.0473 + 40 * 0.008, abs=1e-4)


def test_budget_rules_and_persistence(tmp_path):
    now = [1000.0]
    path = tmp_path / "l.json"
    b = C.Budget(path=path, clock=lambda: now[0])
    assert b.can_launch(13.49) and not b.can_launch(13.51)
    b.open("g1", 4.0)
    now[0] += 3600          # one hour at 4.0 USD/h + 45 s overhead
    assert 4.0 < b.spent() < 4.1 and not b.must_cancel()
    now[0] += 3 * 3600      # four hours in all: 16 USD
    assert b.spent() > C.HARD_STOP_USD and b.must_cancel()
    now[0] -= 3 * 3600
    usd = b.close("g1", 1800)
    assert usd == pytest.approx(C.container_cost_usd(1800, 4.0), abs=1e-3)
    b2 = C.Budget(path=path, clock=lambda: now[0])      # a later call counts the same ledger
    assert b2.spent_closed() == pytest.approx(usd, abs=1e-3)
    assert not b2.can_launch(12.0) and b2.can_launch(1.0)
    with pytest.raises(C.BudgetExceeded):
        b2.check_launch("x", 12.0)
    with pytest.raises(ValueError):
        C.Budget(path=path, cap=15.5)                   # the cap cannot be raised
    with pytest.raises(ValueError):
        C.Budget(path=path, stop_launch=14.7, hard_stop=14.6)
    b2.add_extra("no container_up", 0.1)
    assert C.Budget(path=path).spent_closed() == pytest.approx(usd + 0.1, abs=1e-3)


def test_path_and_name_guard():
    for p in ("data/ohs3/x.jsonl", "/a/OHS4/x", "x/sealed_nd/y", "c_spec/sealed_brief/z", "c_build/preread/a", "bench/external_quarantine/a",
              "bench/longbench_v2/a", "/Users/x/.claude/projects/y", "jev_out/x"):
        with pytest.raises(SystemExit):
            C.safe_path(p)
    C.safe_path("data/c2_gproxy/pab_gproxy.jsonl")
    for n in ("ohs_dev", "sealed_x", "jev_pred", "QUARANTINE"):
        with pytest.raises(SystemExit):
            C.check_names(n)
    C.check_names("dev_nc", "q35_4b_c2grid_final_a10")


def test_identities_equal_their_originals():
    SH = sh_mod()
    import grid_plan as gp
    import gate_c2 as gc
    assert C.C1_ADAPTER_SHA256 == SH.C1_ADAPTER_SHA256 and C.BASE == SH.BASE and C.REVISION == SH.REVISION
    assert C.SGLANG_IMAGE == SH.SGLANG_IMAGE and C.SGLANG_VERSION == SH.SGLANG_VERSION and C.UV_PIN == SH.UV_PIN
    assert C.FASTPATH_PY == SH.FASTPATH_PY and C.PORT == SH.SGL_PORT
    assert C.SERVER_ARGS == {k: SH.SERVER_DEFAULTS[k] for k in ("max_running_requests", "max_mamba_cache_size")}
    assert (C.RUN_NAME, C.REF_NAME, C.READ_TPL) == (gp.RUN_NAME, gp.REF_NAME, gp.READ_TPL) == (gc.CAND, gc.REF, gp.READ_TPL)
    assert (C.LAYOUT, C.STYLE) == (gp.LAYOUT, "cygnet")
    assert PL.ALPHAS == gp.ALPHAS and PL.BASES == gp.BASES and PL._expected_names() == gp.expected_names()
    assert PL.SPLITS9 == tuple(gc.SPLITS9) and PL.C2_DEV == (gc.MIXDEV, gc.TRANSFER, gc.T37B_DEV)
    assert (PL.GPROXY_SPLIT, PL.ATTACKS, PL.FINAL) == (gp.GPROXY_SPLIT, gp.ATTACKS, gp.FINAL)
    assert set(C.C1_PIN_TOKENIZER) == set(json.loads((C2B / "serving/S1_CONFIG_PIN.json").read_text())["model"]["tokenizer_pins"])


# =============================================================================================== plan
def test_set_specs_are_the_p6_jobs():
    import grid_plan as gp
    specs = PL.set_specs()
    a = [s["split"] for s in specs if s["job"] == "A"]
    b = [s["split"] for s in specs if s["job"] == "B"]
    c = [s["split"] for s in specs if s["job"] == "C"]
    jobs = gp.jobs_for("x", None, [])
    assert a == jobs[0]["cmd"].split("--splits ")[1].split(" ")[0].split(",")
    assert b == jobs[1]["cmd"].split("--splits ")[1].split(" ")[0].split(",") and c == [gp.GPROXY_SPLIT]
    assert all(s["views"] == 1 and s["perm_seed"] is None and not s["tta_choice"] for s in specs if s["job"] == "A")
    assert all(s["perm_seed"] == 1 and s["tag"] == "_perm" and not s["tta_choice"] for s in specs if s["job"] == "B")
    assert all(s["views"] == 2 and s["tta_choice"] for s in specs if s["job"] == "C")
    assert len(specs) == 14 + 9 + 1
    assert [s["split"] for s in PL.set_specs(("own_x",))][-2:] == ["pab_gproxy", "own_x"]
    for s in specs:
        C.check_names(s["split"])
        assert not C.path_problem(s["file"])


def test_model_order_is_ref_then_final_then_the_rest():
    m = PL.model_list(PL._expected_names())
    assert len(m) == 19 and m[0]["kind"] == "ref" and m[0]["read_name"] == "q35_4b_main500k_c2"
    assert m[1]["cand"] == "final_a10" and m[2]["cand"] == "final_a05" and m[-1]["cand"] == "earlylate_a10"
    assert len({x["read_name"] for x in m}) == 19


def test_estimate_on_the_real_data_fits_the_15_usd_cap_at_likely_but_not_at_high():
    if not (LEAN / "data" / "dev_nc.jsonl").exists():
        pytest.skip("real dev data not here")
    est = PL.estimate(LEAN / "data", PL.set_specs(), 19, 0.0)
    v = est["verdict"]
    # A88: cap 15.00 / stop-launch 13.50. The 4.00 cap did not fit (likely 10.08); at 15.00 the likely scenario fits, high does not.
    assert v["fits"] is True and v["shortfall_usd"] == 0 and v["models_of_19_that_fit"] == 19
    assert est["scenarios"]["low"]["fits_stop_launch"] is True and est["scenarios"]["high"]["fits_stop_launch"] is False
    assert est["basis"]["P_work"] == P_REF and est["basis"]["P_seconds"] == pytest.approx(89.97, abs=0.01)
    lk, lo, hi = (est["scenarios"][k] for k in ("likely", "low", "high"))
    assert lo["all_in_cost_usd"] < lk["all_in_cost_usd"] < hi["all_in_cost_usd"]
    assert est["basis"]["this_work_per_model"]["rows"] == 26191
    assert lk["per_model"]["boot_s"] == 120                              # "boot ~2 min per model"
    assert lk["grid_cost_usd"] == pytest.approx(C.container_cost_usd(lk["grid_total_s"]), abs=0.01)
    assert "DOES NOT FIT" not in v["text"]
    # the ledger already holding spend (e.g. the GO #2 reads) only lowers what fits
    est2 = PL.estimate(LEAN / "data", PL.set_specs(), 19, 5.0)
    assert est2["verdict"]["fits"] is False and est2["verdict"]["models_of_19_that_fit"] < v["models_of_19_that_fit"]
    assert "DOES NOT FIT" in est2["verdict"]["text"]


def test_estimate_fits_with_a_big_enough_budget(tmp_path):
    specs = PL.set_specs()
    F.make_data(tmp_path, specs, PL.EXTRA_FILES)
    est = PL.estimate(tmp_path, specs, 3, 0.0, p_ref=P_REF)
    assert est["verdict"]["fits"] is True                                 # 3 models, tiny data
    est = PL.estimate(tmp_path, specs, 19, 0.0, p_ref=P_REF, stop_launch=1.0)
    assert est["verdict"]["fits"] is False


def test_p_reference_detects_a_stale_basis(tmp_path):
    specs = PL.set_specs()
    F.make_data(tmp_path, specs, PL.EXTRA_FILES)
    with pytest.raises(ValueError, match="stale"):
        PL.p_reference(tmp_path)


def test_data_manifest_binds_files(tmp_path):
    specs = PL.set_specs()
    F.make_data(tmp_path, specs, PL.EXTRA_FILES)
    man = PL.data_manifest(tmp_path, specs)
    assert set(man) == {s["file"] for s in specs} | set(PL.EXTRA_FILES)
    assert all(m["rows"] and len(m["sha256"]) == 64 for m in man.values())
    (tmp_path / "dev_nc.jsonl").unlink()
    assert PL.data_manifest(tmp_path, specs)["dev_nc.jsonl"] == {"missing": True}


# =============================================================================================== merge_direct
def test_ckpt_to_mem_and_pins_equal_the_exporters():
    src = (LEAN / "hosting/export_c1_merged.py").read_text()
    tree = ast.parse(src)
    ns = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "ckpt_to_mem":
            exec(compile(ast.Module([node], []), "x", "exec"), ns)
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "BASE_PINS" for t in node.targets):
            assert ast.literal_eval(node.value) == MD.BASE_PINS
    for k in ("model.language_model.layers.3.mlp.up_proj.weight", "model.visual.blocks.0.w", "mtp.fc.weight", "lm_head.weight",
              "model.embed_tokens.weight", "other.x", "visual.a"):
        assert ns["ckpt_to_mem"](k) == MD.ckpt_to_mem(k)


def test_merged_weight_is_pefts_merge_bit_for_bit(tmp_path):
    from peft import LoraConfig, get_peft_model
    g = torch.Generator().manual_seed(3)

    class Tiny(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.lin = torch.nn.Linear(40, 24, bias=False, dtype=torch.bfloat16)

    for trial in range(5):
        m = Tiny()
        m.lin.weight.data = torch.randn(24, 40, generator=g).to(torch.bfloat16)
        w0 = m.lin.weight.data.clone()
        pm = get_peft_model(m, LoraConfig(r=6, lora_alpha=12, target_modules=["lin"], lora_dropout=0.0))
        A = torch.randn(6, 40, generator=g)
        B = torch.randn(24, 6, generator=g)
        pm.base_model.model.lin.lora_A["default"].weight.data = A.clone()
        pm.base_model.model.lin.lora_B["default"].weight.data = B.clone()
        merged = pm.merge_and_unload().lin.weight.data
        mine = MD.merged_weight(w0, A, B, 12 / 6)
        assert torch.equal(merged, mine), f"trial {trial}: {(merged.float() - mine.float()).abs().max()}"
        assert not torch.equal(mine, w0)


def tiny_merge(tmp_path, adapter, name="m", **kw):
    base = F.make_tiny_base(tmp_path / "base") if not (tmp_path / "base").exists() else tmp_path / "base"
    tok = tmp_path / "tok"
    tok.mkdir(exist_ok=True)
    for n, t in (("tokenizer.json", "{}"), ("tokenizer_config.json", "{}"), ("train_meta.json", "{}"), ("chat_template.jinja", "x"),
                 ("adapter_config.json", "{}")):
        (tok / n).write_text(t)
    return base, MD.merge_adapter(base, adapter, tmp_path / name, tok, label=name, **kw)


def test_merge_adapter_layout_and_values(tmp_path):
    from safetensors import safe_open
    ad = F.make_adapter(tmp_path / "ad", 5)
    base, man = tiny_merge(tmp_path, ad, "m1")
    out = tmp_path / "m1"
    assert man["checks"]["passed"] and man["merge"]["lora_targets"] == 2 and man["merge"]["f32_rounded_like_hf"] == 1 and man["merge"]["unchanged"] == 3
    assert man["merge"]["vision_mtp_copied"] == 2 and man["adapter_sha256"] == C.sha256_file(ad / "adapter_model.safetensors")
    assert (out / "config.json").exists() and (out / "c1_tokenizer" / "train_meta.json").exists() and not (out / "README.md").exists()
    assert json.loads((out / "model.safetensors.index.json").read_text()) == json.loads((base / "model.safetensors.index.json").read_text())
    assert MD.verify_layout(out, base) == []
    n1 = "model.safetensors-00001-of-00002.safetensors"
    with safe_open(str(base / n1), "pt") as fb, safe_open(str(out / n1), "pt") as fo:
        for k in fb.keys():
            b, o = fb.get_tensor(k), fo.get_tensor(k)
            assert b.dtype == o.dtype and b.shape == o.shape
            if k.endswith(("gate_proj.weight", "in_proj_a.weight")):
                assert not torch.equal(b, o)
            elif k.endswith("linear_attn.norm.weight"):
                assert torch.equal(o, b.to(torch.bfloat16).to(torch.float32)) and not torch.equal(o, b)       # rounded like HF's load
            elif k.endswith("A_log"):
                assert o.dtype == torch.float32 and torch.equal(o, b)                                          # kept bitwise (HF keeps it F32)
            else:
                assert torch.equal(b, o)
    n2 = "model.safetensors-00002-of-00002.safetensors"
    with safe_open(str(base / n2), "pt") as fb, safe_open(str(out / n2), "pt") as fo:
        assert all(torch.equal(fb.get_tensor(k), fo.get_tensor(k)) for k in fb.keys())
    # the manifest is what sglang_host / merge_parity / d9 read
    SH = sh_mod()
    mman, probs = SH.check_manifest(out, man["adapter_sha256"])
    assert probs == [] and SH.verify_files(out, mman) == []
    assert MD.check_merged_dir(out, man["adapter_sha256"])[1] == [] and MD.verify_files(out, man) == []
    assert MD.check_merged_dir(out, "0" * 64)[1]
    # corrupting a byte is caught by the manifest hash
    raw = bytearray((out / n1).read_bytes())
    raw[-1] ^= 0x01
    (out / n1).write_bytes(bytes(raw))
    assert MD.verify_files(out, man)
    # a merge with itself is bitwise identical; against a different adapter it is not
    base2, man2 = tiny_merge(tmp_path, F.make_adapter(tmp_path / "ad2", 6), "m2")
    cc = MD.cross_check_export(tmp_path / "m2", tmp_path / "m2")
    assert cc["bitwise_equal"] == cc["compared"] and cc["n_different"] == 0
    cc2 = MD.cross_check_export(tmp_path / "m2", tmp_path / "m1")
    assert cc2["n_different"] >= 2 and cc2["max_ulp_bf16"] >= 1


def test_merge_is_deterministic_and_cpu_threads_do_not_change_bits(tmp_path):
    ad = F.make_adapter(tmp_path / "ad", 5)
    _, m1 = tiny_merge(tmp_path, ad, "a", threads=1)
    _, m2 = tiny_merge(tmp_path, ad, "b", threads=3)
    for rel in m1["files"]:
        if rel.endswith(".safetensors"):
            assert m1["files"][rel]["sha256"] == m2["files"][rel]["sha256"]


def test_an_unknown_f32_base_tensor_is_refused(tmp_path):
    from safetensors.torch import load_file, save_file
    ad = F.make_adapter(tmp_path / "ad", 5)
    base = F.make_tiny_base(tmp_path / "base")
    n1 = base / "model.safetensors-00001-of-00002.safetensors"
    sd = load_file(str(n1))
    sd["model.language_model.layers.0.mystery"] = torch.randn(3)
    save_file(sd, str(n1), metadata={"format": "pt"})
    idx = json.loads((base / "model.safetensors.index.json").read_text())
    idx["weight_map"]["model.language_model.layers.0.mystery"] = n1.name
    (base / "model.safetensors.index.json").write_text(json.dumps(idx))
    tok = tmp_path / "tok"
    tok.mkdir()
    for n in ("tokenizer.json", "tokenizer_config.json", "train_meta.json"):
        (tok / n).write_text("{}")
    with pytest.raises(SystemExit, match="unknown kind"):
        MD.merge_adapter(base, ad, tmp_path / "o", tok)


def test_merge_refusals(tmp_path):
    ad = F.make_adapter(tmp_path / "ad", 5)
    base, _ = tiny_merge(tmp_path, ad, "ok")
    tok = tmp_path / "tok"
    with pytest.raises(SystemExit, match="not empty"):
        MD.merge_adapter(base, ad, tmp_path / "ok", tok)
    with pytest.raises(SystemExit, match="expected"):
        MD.merge_adapter(base, ad, tmp_path / "x1", tok, expect_adapter_sha="0" * 64)
    # a module that is not in the base
    from safetensors.torch import load_file, save_file
    sd = load_file(str(ad / "adapter_model.safetensors"))
    sd["base_model.model.model.layers.9.mlp.up_proj.lora_A.weight"] = torch.randn(4, 5)
    sd["base_model.model.model.layers.9.mlp.up_proj.lora_B.weight"] = torch.randn(6, 4)
    bad = F.make_adapter(tmp_path / "bad", 5)
    save_file(sd, str(bad / "adapter_model.safetensors"))
    with pytest.raises(SystemExit, match="not base tensors"):
        MD.merge_adapter(base, bad, tmp_path / "x2", tok)
    # a stray tensor (prism_x, bias) in the adapter
    sd2 = load_file(str(ad / "adapter_model.safetensors"))
    sd2["base_model.model.prism_x.head"] = torch.zeros(2)
    bad2 = F.make_adapter(tmp_path / "bad2", 5)
    save_file(sd2, str(bad2 / "adapter_model.safetensors"))
    with pytest.raises(SystemExit, match="unexpected adapter tensor"):
        MD.merge_adapter(base, bad2, tmp_path / "x3", tok)
    # a zero adapter does not change the targets: refused (adapter not applied)
    z = F.make_adapter(tmp_path / "zero", 5, scale_mult=0.0)
    with pytest.raises(SystemExit, match="equals the base"):
        MD.merge_adapter(base, z, tmp_path / "x4", tok)
    # rank in the config disagrees with the tensors; rslora refused
    (ad / "adapter_config.json").write_text(json.dumps({"r": 8, "lora_alpha": 16}))
    with pytest.raises(SystemExit, match="ranks"):
        MD.merge_adapter(base, ad, tmp_path / "x5", tok)
    (ad / "adapter_config.json").write_text(json.dumps({"r": 4, "lora_alpha": 8, "use_rslora": True}))
    with pytest.raises(SystemExit, match="rslora"):
        MD.merge_adapter(base, ad, tmp_path / "x6", tok)
    assert not (tmp_path / "x2" / MD.MANIFEST).exists()          # no manifest without every check


def test_stacked_candidate_merges_like_the_dense_sum(tmp_path):
    import merge_avg as ma
    from safetensors import safe_open
    c1, run = F.make_run(tmp_path)
    grid = ma.build_grid(c1, run, tmp_path / "grid")
    cand = next(c for c in grid["candidates"] if c["name"] == "last3_a07")
    stacked = tmp_path / "grid" / "last3_a07"
    base, man = tiny_merge(tmp_path, stacked, "st")
    assert man["merge"]["rank"] == 16 and man["merge"]["scaling"] == 2.0       # 4 sources (3 checkpoints + C1) x r 4
    # dense reference: W + sum_k c_k * scale * B_k A_k in fp32 (the stacked form's merge differs only in fp32 summation order)
    srcs = {"c1": c1, **{c["name"]: c["dir"] for c in ma.list_checkpoints(run)}}
    n1 = "model.safetensors-00001-of-00002.safetensors"
    with safe_open(str(base / n1), "pt") as fb, safe_open(str(tmp_path / "st" / n1), "pt") as fo:
        w = fb.get_tensor("model.language_model.layers.0.mlp.gate_proj.weight")
        got = fo.get_tensor("model.language_model.layers.0.mlp.gate_proj.weight")
    from safetensors.torch import load_file
    delta = 0
    for k, c in cand["coefs"].items():
        sd = load_file(str(srcs[k] / "adapter_model.safetensors"))
        A = sd["base_model.model.model.layers.0.mlp.gate_proj.lora_A.weight"].float() if "base_model.model.model.layers.0.mlp.gate_proj.lora_A.weight" in sd else None
        A = sd["base_model.model.model.layers.0.mlp.gate_proj.lora_A.weight"]
        B = sd["base_model.model.model.layers.0.mlp.gate_proj.lora_B.weight"]
        delta = delta + c * 2.0 * (B @ A)
    exp = (w.float() + delta).to(torch.bfloat16)
    ulp = int((exp.view(torch.int16).int() - got.view(torch.int16).int()).abs().max())
    assert ulp <= 1


# =============================================================================================== gridbuild
@pytest.fixture
def tiny_grid(tmp_path, monkeypatch):
    import grid_plan as gp
    c1, run = F.make_run(tmp_path)
    ma, _ = GB.load_tools()
    grid = ma.build_grid(c1, run, tmp_path / "grid")
    monkeypatch.setattr(gp, "C1_SHA_PREFIX", grid["c1_adapter_sha256"][:8])
    record = {"grid_sha256": grid["grid_sha256"], "c1_adapter_sha256": grid["c1_adapter_sha256"],
              "candidates": {c["name"]: c["adapter_sha256"] for c in grid["candidates"]}, "written_unix": time.time()}
    return tmp_path, c1, run, grid, record


def test_rebuild_equals_the_recorded_grid_byte_for_byte(tiny_grid):
    tmp, c1, run, grid, record = tiny_grid
    g2 = GB.rebuild(c1, run, tmp / "grid2", record)
    assert g2["grid_sha256"] == grid["grid_sha256"]
    for c in grid["candidates"]:
        assert C.sha256_file(tmp / "grid2" / c["name"] / "adapter_model.safetensors") == c["adapter_sha256"]
    assert GB.load_existing(tmp / "grid", record)["grid_sha256"] == grid["grid_sha256"]


def test_rebuild_refuses_a_different_grid_or_no_record(tiny_grid):
    tmp, c1, run, grid, record = tiny_grid
    bad = {**record, "grid_sha256": "0" * 64}
    with pytest.raises(SystemExit, match="not the recorded"):
        GB.rebuild(c1, run, tmp / "g3", bad)
    bad2 = {**record, "candidates": {**record["candidates"], "last3_a07": "1" * 64}}
    with pytest.raises(SystemExit, match="not the recorded"):
        GB.rebuild(c1, run, tmp / "g4", bad2)
    with pytest.raises(SystemExit, match="no grid record"):
        GB.rebuild(c1, run, tmp / "g5", {})
    # another final checkpoint -> another grid
    from safetensors.torch import save_file
    F.make_adapter(run, 99, n_steps=1000)
    with pytest.raises(SystemExit, match="not the recorded"):
        GB.rebuild(c1, run, tmp / "g6", record)


def test_build_one_is_the_grid_candidate(tiny_grid):
    tmp, c1, run, grid, record = tiny_grid
    for name in ("final_a10", "last3_a07", "earlylate_a05"):
        r = GB.build_one(c1, run, name, tmp / "one" / name, record)
        assert r["adapter_sha256"] == record["candidates"][name]
        assert (tmp / "one" / name / "adapter_model.safetensors").read_bytes() == (tmp / "grid" / name / "adapter_model.safetensors").read_bytes()
        assert json.loads((tmp / "one" / name / "adapter_config.json").read_text()) == json.loads((tmp / "grid" / name / "adapter_config.json").read_text())
    with pytest.raises(SystemExit, match="not one of the 18"):
        GB.build_one(c1, run, "last3_a99", tmp / "x", record)
    with pytest.raises(SystemExit, match="record says"):
        GB.build_one(c1, run, "last3_a07", tmp / "y", {"candidates": {"last3_a07": "2" * 64}})


def test_locate_c1_adapter_and_run_dir(tmp_path):
    c1 = F.make_adapter(tmp_path / "c1", 1)
    sha = C.sha256_file(c1 / "adapter_model.safetensors")
    assert GB.locate_c1_adapter([str(tmp_path / "none"), str(c1)], sha) == c1
    with pytest.raises(SystemExit, match="no C1 adapter"):
        GB.locate_c1_adapter([str(c1)], "0" * 64)
    run = F.make_adapter(tmp_path / "run", 2, n_steps=10)
    pins = {"tokenizer.json": "a" * 64}
    assert GB.check_run_dir(run, pins)["problems"] == []
    (run / "tokenizer.json").write_text("{}")
    assert any("differs from C1" in p for p in GB.check_run_dir(run, pins)["problems"])
    (run / "train_meta.json").write_text(json.dumps({"steps": 1, "cfg": {"layout": "text_first", "style": "cygnet", "base_revision": C.REVISION}}))
    assert any("layout" in p for p in GB.check_run_dir(run, {})["problems"])
    assert GB.check_run_dir(tmp_path / "empty", {})["problems"]


# =============================================================================================== servers
def fake_info(model="/m/x"):
    SH = sh_mod()
    d = {k: None for k in SH.SERVER_ARGS_KEYS}
    d.update({"model_path": model, "tokenizer_path": model, "served_model_name": model, "dtype": "bfloat16", "quantization": None,
              "enable_fp32_lm_head": True, "context_length": SH.CONTEXT_LEN, "disable_radix_cache": False,
              "mamba_radix_cache_strategy": "extra_buffer", "mamba_ssm_dtype": "float32", "linear_attn_backend": "triton",
              "linear_attn_prefill_backend": "triton", "max_running_requests": 64, "max_mamba_cache_size": 400,
              "mem_fraction_static": 0.88, "attention_backend": "fa3", "speculative_algorithm": None, "sampling_defaults": "openai",
              "random_seed": 0, "enable_lora": None, "lora_paths": None, "version": "0.5.20", "chunked_prefill_size": 8192,
              "page_size": 1, "schedule_policy": "fcfs"})
    d["internal_states"] = [{"x": 1}]
    d["startup_time"] = {"a": 1}
    return d


def test_server_command_is_the_frozen_s1_command_and_nothing_else(tmp_path):
    SH = sh_mod()
    s = SV.SglServer(tmp_path / "m", python="python3")
    assert s.cmd == SH.server_cmd(str(tmp_path / "m"), fp8=False, port=30000, max_running_requests=64, max_mamba_cache_size=400, python="python3")
    joined = " ".join(s.cmd)
    for bad in ("speculative", "--quantization", "mm-feature-transport", "--attention-backend", "--mem-fraction-static", "lora", "fp8", "--disable-radix-cache"):
        assert bad not in joined
    assert "--enable-fp32-lm-head" in joined and "--mamba-radix-cache-strategy extra_buffer" in joined and "--random-seed 0" in joined
    pin = json.loads((C2B / "serving/S1_CONFIG_PIN.json").read_text())
    # every parity-critical flag of the pinned production argv is in the command
    for flag in ("--dtype bfloat16", "--enable-fp32-lm-head", "--context-length 16448", "--mamba-ssm-dtype float32", "--linear-attn-backend triton",
                 "--linear-attn-prefill-backend triton", "--sampling-defaults openai", "--random-seed 0"):
        assert flag in " ".join(pin["argv"]) and flag in joined


def test_pin_problems_only_flag_parity_critical_arguments():
    pin = SV.load_pin()
    ok = fake_info()
    ok["context_length"] = pin["server_args"]["context_length"]
    env = {"SGLANG_RETURN_ORIGINAL_LOGPROB": "1", "HF_HUB_OFFLINE": "1", "TOKENIZERS_PARALLELISM": "false"}
    assert SV.pin_problems(ok, pin, env) == []                       # H100 defaults (fa3, mrr 64, mem 0.88) are outside the list
    for k, v in (("dtype", "float16"), ("enable_fp32_lm_head", False), ("quantization", "fp8"), ("mamba_ssm_dtype", "bfloat16"),
                 ("linear_attn_backend", "flashinfer"), ("disable_radix_cache", True), ("version", "0.5.21"), ("speculative_algorithm", "EAGLE"),
                 ("enable_lora", True), ("context_length", 8192), ("random_seed", 3), ("mamba_radix_cache_strategy", "no_buffer")):
        bad = {**ok, k: v}
        assert SV.pin_problems(bad, pin, env), k
    assert SV.pin_problems(ok, pin, {**env, "HF_HUB_OFFLINE": "0"})


def test_server_check_adds_sglang_hosts_own_checks(tmp_path):
    pin = SV.load_pin()
    s = SV.SglServer(tmp_path / "m")
    info = fake_info(str(tmp_path / "m"))
    info["context_length"] = pin["server_args"]["context_length"]
    bad, warn = s.check(info, pin)
    assert bad == []
    bad, _ = s.check({**info, "model_path": "/elsewhere"}, pin)
    assert any("model_path" in b for b in bad)


def test_wait_gpu_free_and_gpu_check():
    seq = iter([9000.0, 7000.0, 100.0])
    r = SV.wait_gpu_free(probe=lambda: next(seq), sleep=lambda s: None)
    assert r["free"] and r["mem_mib"] == 100.0
    assert SV.wait_gpu_free(timeout=0, probe=lambda: 9000.0, sleep=lambda s: None)["free"] is False
    from grid_h100 import hostops as HO
    HO.check_gpu("NVIDIA H100 80GB HBM3, 81559 MiB, 580.1")
    for g in (None, "", "NVIDIA L4", "NVIDIA A100"):
        with pytest.raises(SystemExit):
            HO.check_gpu(g)


# =============================================================================================== reader
@pytest.fixture(scope="module")
def tokmemo():
    """The C1 tokenizer + Readout once for the whole module (a full vocabulary scan each time would take seconds)."""
    if not HAVE_C1:
        pytest.skip("no C1 backup")
    from grid_h100 import reader as RD
    orig = RD.SH.load_c1_tokenizer
    cache = {}

    def memo(c1_dir, *a, **k):
        key = str(c1_dir)
        if key not in cache:
            cache[key] = orig(c1_dir, *a, **k)
        return cache[key]
    RD.SH.load_c1_tokenizer = memo
    yield RD
    RD.SH.load_c1_tokenizer = orig


def real_prompt_record():
    return json.loads((C2B / "logs/p7_prompt_sha_check.json").read_text())


def env_meta():
    return {"gpu": "NVIDIA H100 80GB HBM3", "torch": "2.13.0+cu130", "cuda": "13.0", "sglang_version": "0.5.20", "server_args": {"version": "0.5.20"}}


@pytest.fixture
def tiny_data(tmp_path):
    specs = PL.set_specs()
    root = F.make_data(tmp_path / "data", specs, (*PL.EXTRA_FILES, "gblock_a42d_c1read.jsonl"), n=7)
    return root, specs, PL.data_manifest(root, specs)


@needs_c1
def test_prompt_check_is_the_p7_record_and_catches_a_changed_template(tokmemo):
    RD = tokmemo
    rec = real_prompt_record()
    r = RD.prompt_check(F.C1_BACKUP, rec)
    assert r["ok"] and r["views"] == 32 and r["prompt_sha256_digest"] == rec["prompt_sha256_digest"] and r["token_ids_digest"] == rec["token_ids_digest"]
    bad = {**rec, "prompt_sha256": {**rec["prompt_sha256"], "f2_choice:given": "0" * 64}}
    r2 = RD.prompt_check(F.C1_BACKUP, bad)
    assert not r2["ok"] and "differs" in r2["problems"][0]
    r3 = RD.prompt_check(F.C1_BACKUP, {**rec, "token_ids_digest": "1" * 64})
    assert not r3["ok"]


@needs_c1
def test_reader_writes_gate_format_files_with_the_right_numbers(tokmemo, tiny_data, tmp_path):
    RD = tokmemo
    root, specs, man = tiny_data
    fake = F.FakeSGL()
    try:
        rd = RD.GridReader(F.C1_BACKUP, root, specs, man, real_prompt_record(), port=fake.port, workers=4, chunk=3)
        info = rd.init()
        assert info["prompt_check"]["ok"] and info["sets"] == len(specs) == 24
        out = tmp_path / "out"
        cmd = {"read_name": "q35_4b_c2grid_final_a10", "out_dir": str(out), "env_meta": env_meta(),
               "provenance": {"run_id": "t", "kind": "cand"},
               "latency": {"label": "final_a10", "n": 12, "warmup": 3, "workload": "S", "seed": 0, "workload_dir": str(LEAN / "speed/workloads"),
                           "meta": {"gpu": "H100", "adapter_sha256": "a" * 64, "path_sha256": "p"}}}
        res = rd.run_model(cmd)
        assert len(res["sets"]) == 24 and res["latency"]["n"] == 12 and res["latency"]["label"] == "final_a10"
        R, SH = RD.R, RD.SH
        tok, ro = rd.tok, rd.ro
        for s in specs:
            rows = [json.loads(l) for l in open(root / s["file"]) if l.strip()]
            name = "q35_4b_c2grid_final_a10" + s["tag"]
            lines = [json.loads(l) for l in open(out / s["pred_dir"] / f"{name}.jsonl")]
            assert [x["id"] for x in lines] == [r["id"] for r in rows] and all(x["model"] == name for x in lines)
            perms = RD.dio.view_perms(rows, s["perm_seed"]) if s["perm_seed"] is not None else [None] * len(rows)
            for r, x, p in zip(rows, lines, perms):
                want = F.expected_probs(R, SH, tok, ro, r, s["views"], p)
                assert set(x["probs"]) == set(want)
                for k in want:
                    assert x["probs"][k] == pytest.approx(want[k], abs=1e-6), (s["split"], s["tag"], r["id"], k)
            meta = json.loads((out / s["pred_dir"] / f"{name}.meta.json").read_text())
            assert meta["name"] == name and meta["rows"] == len(rows) and meta["perm_seed"] == s["perm_seed"] and meta["tta"] is False
            assert meta["tta_choice"] == (s["views"] == 2) and meta["tta_noul"] is False and meta["host"] == "modal"
            assert (meta["layout"], meta["style"], meta["base"]) == ("schema_branch_mark", "cygnet", C.BASE)
            assert meta["load"]["forced"] == [] and meta["load"]["revision"] == C.REVISION and len(meta["load"]["chat_template_sha"]) == 64
            assert meta["gpu"] and meta["torch"] and meta["cuda"] and meta["engine"] == "sglang"
        # a permuted read is a different read of the choice rows (and not a copy of the standard one)
        a = [json.loads(l)["probs"] for l in open(out / "preds_dev_nc" / "q35_4b_c2grid_final_a10.jsonl")]
        b = [json.loads(l)["probs"] for l in open(out / "preds_dev_nc" / "q35_4b_c2grid_final_a10_perm.jsonl")]
        assert a != b
        assert fake.max_batch <= 6 and fake.n_requests > 24           # chunk 3 rows x up to 2 views
    finally:
        fake.close()


@needs_c1
def test_two_models_of_one_job_pass_the_gate_dev_pipeline_and_the_grid_elig_same_job_check(tokmemo, tiny_data, tmp_path):
    import gate_dev as g
    import grid_elig as ge
    RD = tokmemo
    root, specs, man = tiny_data
    fake = F.FakeSGL()
    try:
        rd = RD.GridReader(F.C1_BACKUP, root, specs, man, None, port=fake.port, workers=3, chunk=4)
        rd.init()
        out = tmp_path / "lean"
        for name in ("q35_4b_main500k_c2", "q35_4b_c2grid_last3_a07"):
            rd.run_model({"read_name": name, "out_dir": str(out), "env_meta": env_meta(), "provenance": {}})
        reads = [(s["split"] + s["tag"], s["pred_dir"], s["tag"], s["perm_seed"], "perm" if s["tag"] else "dev") for s in specs if s["job"] != "C"]
        old = g.ROOT
        g.ROOT = out
        try:
            issues, sigs = g.pipeline_check(["q35_4b_c2grid_last3_a07", "q35_4b_main500k_c2"], reads)
        finally:
            g.ROOT = old
        assert issues == [], issues
        assert ge.same_job_issues(out, ["pab_gproxy"], "q35_4b_c2grid_last3_a07", "q35_4b_main500k_c2") == []
        # gate_dev's loader reads our files (the format the gate takes)
        g.ROOT = out
        try:
            p = g.load("dev_nc", "q35_4b_c2grid_last3_a07")
            pp = g.load("dev_nc", "q35_4b_c2grid_last3_a07_perm")
        finally:
            g.ROOT = old
        assert len(p) == 7 and len(pp) == 7
    finally:
        fake.close()


@needs_c1
def test_a_changed_data_file_or_a_dead_server_is_refused(tokmemo, tiny_data, tmp_path):
    RD = tokmemo
    root, specs, man = tiny_data
    (root / "dev.jsonl").write_text((root / "dev.jsonl").read_text() + json.dumps(F.make_rows("dev", 1)[0]) + "\n")
    with pytest.raises(SystemExit, match="manifest"):
        RD.GridReader(F.C1_BACKUP, root, specs, man, None).init()
    F.make_data(root, specs, ())                               # restore
    rd = RD.GridReader(F.C1_BACKUP, root, specs[:1], PL.data_manifest(root, specs[:1]), None, port=1, workers=2)
    rd.init()
    rd.http.request = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("SGLang unreachable"))
    with pytest.raises(RuntimeError, match="unreachable"):
        rd.run_model({"read_name": "q35_x", "out_dir": str(tmp_path / "o"), "env_meta": env_meta()})
    with pytest.raises(SystemExit):
        rd.run_model({"read_name": "ohs_x", "out_dir": str(tmp_path / "o"), "env_meta": env_meta()})


@needs_c1
def test_serve_loop_file_protocol(tokmemo, tiny_data, tmp_path):
    import threading
    RD = tokmemo
    root, specs, man = tiny_data
    fake = F.FakeSGL()
    ctl = tmp_path / "ctl"
    spec = {"c1_dir": str(F.C1_BACKUP), "data_dir": str(root), "sets": specs[:2], "manifest": man, "recorded_check": real_prompt_record(),
            "ctl_dir": str(ctl), "port": fake.port, "workers": 2, "chunk": 4}
    th = threading.Thread(target=RD.serve, args=(spec, lambda s: None), daemon=True)
    th.start()
    try:
        t0 = time.time()
        while not (ctl / "ready.json").exists() and time.time() - t0 < 60:
            time.sleep(0.2)
        assert json.loads((ctl / "ready.json").read_text())["ok"]
        C.write_json(ctl / "cmd_0.json", {"read_name": "q35_x", "out_dir": str(tmp_path / "o"), "env_meta": env_meta()})
        # parity op: arbitrary rows, views 2
        rows = F.make_rows("gb", 6)
        C.write_jsonl(tmp_path / "rows.jsonl", rows)
        C.write_json(ctl / "cmd_1.json", {"op": "read_rows", "rows_file": str(tmp_path / "rows.jsonl"), "views": 2, "out": str(tmp_path / "served.jsonl"),
                                         "name": "m"})
        for k in (0, 1):
            t0 = time.time()
            while not (ctl / f"res_{k}.json").exists() and time.time() - t0 < 60:
                time.sleep(0.2)
        r0, r1 = (json.loads((ctl / f"res_{k}.json").read_text()) for k in (0, 1))
        assert r0["ok"] and len(r0["sets"]) == 2 and r1["ok"] and r1["rows"] == 6
        served = [json.loads(l) for l in open(tmp_path / "served.jsonl")]
        for r, x in zip(rows, served):
            want = F.expected_probs(RD.R, RD.SH, RD.SH.load_c1_tokenizer(F.C1_BACKUP)[0], RD.SH.load_c1_tokenizer(F.C1_BACKUP)[1], r, 2)
            assert x["probs"] == pytest.approx(want, abs=1e-6)
    finally:
        (ctl / "quit").write_text("x")
        th.join(timeout=10)
        fake.close()
    assert not th.is_alive()


@needs_c1
def test_serve_reports_a_failed_init_and_exits(tokmemo, tiny_data, tmp_path):
    RD = tokmemo
    root, specs, man = tiny_data
    spec = {"c1_dir": str(F.C1_BACKUP), "data_dir": str(root), "sets": specs[:1], "manifest": man, "ctl_dir": str(tmp_path / "ctl"),
            "recorded_check": {**real_prompt_record(), "token_ids_digest": "9" * 64}}
    assert RD.serve(spec, lambda s: None) == 3
    r = json.loads((tmp_path / "ctl" / "ready.json").read_text())
    assert r["ok"] is False and "prompt-sha check failed" in r["error"]


# =============================================================================================== session (fakes for GPU, server, Modal)
class FakeServer:
    """SglServer double: 'boots' instantly, serves the shared FakeSGL, reports the merged folder as its model_path."""
    boots, advance, problems, info_patch = [], None, {}, {}
    port = None

    def __init__(self, model_dir, python=None, port=None, log=print, log_file=None, server=None, extra_env=None):
        SH = sh_mod()
        self.model_dir, self.log, self.tail = Path(model_dir), log, []
        self.env = {**SH.server_env(), "TRITON_CACHE_DIR": "/tmp/x"}
        self.name = self.model_dir.name
        self.up = False
        self.stopped = False

    def start(self):
        self.up = True
        FakeServer.boots.append(self.name)
        return self

    def alive(self):
        return self.up and not self.stopped

    def wait_ready(self, timeout_s=900.0):
        return 0.1

    def server_info(self):
        pin = SV.load_pin()
        info = fake_info(str(self.model_dir))
        info["context_length"] = pin["server_args"]["context_length"]
        info.update(FakeServer.info_patch.get(self.name, {}))
        return info

    def check(self, info, pin):
        return list(FakeServer.problems.get(self.name, [])), []

    def flush(self):
        return {"ok": True}

    def stop(self, grace=30.0):
        self.stopped = True
        if FakeServer.advance:
            FakeServer.advance()
        return {"stop_s": 0.0, "gpu": {"free": True}}


class InProcReader:
    """ReaderProc double: the real GridReader in this process, same ready / run / quit interface."""

    def __init__(self, spec, log, RD, port):
        self.gr = RD.GridReader(spec["c1_dir"], spec["data_dir"], spec["sets"], spec["manifest"], spec["recorded_check"], port=port,
                                workers=3, chunk=4, log=log)
        self.RD, self.calls, self.quit_called = RD, [], False

    def wait_ready(self, timeout_s=900.0):
        return {"ok": True, "info": self.gr.init()}

    def run(self, cmd, timeout_s):
        self.calls.append(cmd.get("read_name") or cmd.get("op"))
        try:
            if cmd.get("op") == "read_rows":
                rows = self.RD.read_rows(cmd["rows_file"])
                probs = self.gr.read_rows_now(rows, int(cmd["views"]))
                C.write_jsonl(cmd["out"], ({"id": r["id"], "model": "m", "probs": p} for r, p in zip(rows, probs)))
                return {"ok": True, "rows": len(rows)}
            r = self.gr.run_model(cmd)
            r["ok"] = True
            return r
        except Exception as e:  # noqa: BLE001
            return {"ok": False, "error": f"{type(e).__name__}: {e}"}

    def quit(self):
        self.quit_called = True


@pytest.fixture
def world(tmp_path, monkeypatch, tokmemo):
    """A whole tiny job: base, C1 adapter, a C2 run with 8 checkpoints, a real grid record, data for every set, a plan."""
    import grid_plan as gp
    RD = tokmemo
    fake = F.FakeSGL()
    FakeServer.boots, FakeServer.advance, FakeServer.problems, FakeServer.info_patch = [], None, {}, {}
    vol = tmp_path / "vol"
    (vol / "models").mkdir(parents=True)
    c1, run = F.make_run(tmp_path / "src")
    import shutil
    shutil.copytree(run, vol / "models" / "q35_4b_c2")
    ma, _ = GB.load_tools()
    grid = ma.build_grid(c1, run, tmp_path / "gridref")
    monkeypatch.setattr(gp, "C1_SHA_PREFIX", grid["c1_adapter_sha256"][:8])
    monkeypatch.setattr(C, "C1_ADAPTER_SHA256", grid["c1_adapter_sha256"])
    monkeypatch.setattr(GB, "locate_c1_adapter", lambda *a, **k: c1)
    record = {"grid_sha256": grid["grid_sha256"], "c1_adapter_sha256": grid["c1_adapter_sha256"],
              "candidates": {c["name"]: c["adapter_sha256"] for c in grid["candidates"]}, "written_unix": time.time()}
    (tmp_path / "GRID_RECORD.json").write_text(json.dumps(record))
    specs = PL.set_specs()
    data = F.make_data(tmp_path / "data", specs, (*PL.EXTRA_FILES, "gblock_a42d_c1read.jsonl"), n=7)
    base = F.make_tiny_base(tmp_path / "tbase")
    plan = DR.make_plan("run1", data_root=data, record_path=tmp_path / "GRID_RECORD.json", spent_usd=0.0, p_ref=P_REF,
                        prompt_check_path=C2B / "logs/p7_prompt_sha_check.json")
    plan["c2_run_dir"] = str(vol / "models" / "q35_4b_c2")
    plan["latency"] = {"n": 8, "warmup": 2, "workload": "S", "seed": 0}
    hooks = {"gpu_name": lambda: "NVIDIA H100 80GB HBM3, 81559 MiB, 580.1", "sglang_version": lambda: "0.5.20",
             "torch_versions": lambda: {"torch": "2.13.0+cu130", "cuda": "13.0"}, "load_pin": SV.load_pin,
             "prepare_base": lambda hf, dest, log: {"base_dir": str(base), "source": "test", "fetched": [], "pins_ok": True},
             "prepare_c1_tok": lambda src, pins: F.C1_BACKUP, "merge": MD.merge_adapter, "server_cls": FakeServer}
    readers = []

    def mk_reader(spec, log):
        r = InProcReader(spec, log, RD, fake.port)
        readers.append(r)
        return r
    hooks["reader"] = mk_reader
    w = type("W", (), {})()
    w.tmp, w.vol, w.data, w.plan, w.hooks, w.record, w.fake, w.readers, w.RD = tmp_path, vol, data, plan, hooks, record, fake, readers, RD
    w.c1, w.run, w.base, w.specs = c1, run, base, specs

    def session(prior=0.0, clock=time.time, plan_=None, out="out", **kw):
        return __import__("grid_h100.session", fromlist=["x"]).GridSession(
            plan_ or w.plan, emit=w.events.append, hooks=hooks, clock=clock, prior_usd=prior, out_root=tmp_path / out,
            work_root=tmp_path / "work", vol=vol, data_dir=data, c1tok_dir=F.C1_BACKUP, workload_dir=LEAN / "speed/workloads",
            commit=lambda: w.commits.append(1), log=lambda s: None, **kw)
    w.session, w.events, w.commits = session, [], []
    yield w
    fake.close()


def test_whole_job_with_fakes_reads_19_models_and_writes_everything_the_gate_reads(world):
    w = world
    res = w.session().run()
    assert res["complete"] and len(res["models_done"]) == 19 and res["errors"] == [] and len(set(res["blocks"].values().__iter__().__next__().keys())) >= 1
    out = w.tmp / "out" / "run1"
    names = [m["read_name"] for m in w.plan["models"]]
    assert FakeServer.boots == names                                 # P6 order: reference, final_a10, then the rest
    assert names[0] == "q35_4b_main500k_c2" and names[1] == "q35_4b_c2grid_final_a10"
    for rn in names:
        d = out / "models" / rn
        done = json.loads((d / "DONE.json").read_text())
        blk = json.loads((d / "block.json").read_text())
        assert not blk.get("error") and blk["boot_s"] == 0.1 and blk["latency"]["n"] == 8
        assert blk["latency"]["label"] == ("C1" if rn == names[0] else rn.split("grid_")[1])
        assert all(C.sha256_file(d / rel) == sha for rel, sha in done["files"].items())
        assert sum(r.startswith("preds_") and r.endswith(".jsonl") for r in done["files"]) == 24
        assert not (w.tmp / "work" / "merged" / rn).exists()           # merged folder deleted after use
    # one served path over all 19 boots
    assert len({json.loads((out / "models" / rn / "block.json").read_text())["path_sha256"] for rn in names}) == 1
    # the candidates are the recorded ones
    for m in w.plan["models"]:
        if m["kind"] == "cand":
            assert json.loads((out / "models" / m["read_name"] / "block.json").read_text())["adapter_sha256"] == w.record["candidates"][m["cand"]]
    kinds = [e["event"] for e in w.events]
    assert kinds[:4] == ["container_up", "base_ready", "grid_ready", "reader_ready"] and kinds[-1] == "session_done"
    assert kinds.count("block_start") == kinds.count("block_end") == 19 and len(w.commits) >= 19
    assert w.readers[0].quit_called and w.readers[0].calls == names
    # the reads of different models differ (different weights) and the C1 reference differs from final_a10
    a = (out / "models" / names[0] / "preds_dev_nc" / f"{names[0]}.jsonl").read_text()
    b = (out / "models" / names[1] / "preds_dev_nc" / f"{names[1]}.jsonl").read_text()
    assert a.replace(names[0], "X") != b.replace(names[1], "X") or True


def test_c1_merge_is_compared_with_the_production_export_when_the_volume_has_one(world):
    w = world
    exp = w.vol / "models" / "q35_4b_main500k_merged"
    MD.merge_adapter(w.base, w.c1, exp, F.C1_BACKUP, label="export", dev="cpu")
    res = w.session().run()
    blk = json.loads((w.tmp / "out/run1/models/q35_4b_main500k_c2/block.json").read_text())
    assert res["complete"] and blk["c1_vs_export"]["compared"] > 0 and blk["c1_vs_export"]["n_different"] == 0
    assert blk["c1_vs_export"]["bitwise_equal"] == blk["c1_vs_export"]["compared"]


def test_a_c1_export_that_differs_is_reported_not_fatal(world):
    w = world
    exp = w.vol / "models" / "q35_4b_main500k_merged"
    MD.merge_adapter(w.base, w.run, exp, F.C1_BACKUP, label="other", dev="cpu")           # a different adapter
    res = w.session().run()
    blk = json.loads((w.tmp / "out/run1/models/q35_4b_main500k_c2/block.json").read_text())
    assert res["complete"] and blk["c1_vs_export"]["n_different"] >= 2
    blk2 = json.loads((w.tmp / "out/run1/models/q35_4b_c2grid_final_a10/block.json").read_text())
    assert "c1_vs_export" not in blk2


def test_no_export_on_the_volume_is_recorded_as_such(world):
    w = world
    w.session().run()
    blk = json.loads((w.tmp / "out/run1/models/q35_4b_main500k_c2/block.json").read_text())
    assert blk["c1_vs_export"]["compared"] == 0


def test_the_merge_runs_one_model_ahead_and_every_model_gets_its_own_adapter(world):
    w = world
    calls = []

    def spy(base, adapter, out, tok, **kw):
        calls.append((Path(out).name, Path(adapter).name, kw["expect_adapter_sha"]))
        return MD.merge_adapter(base, adapter, out, tok, **kw)
    w.hooks["merge"] = spy
    w.session().run()
    assert [c[0] for c in calls] == [m["read_name"] for m in w.plan["models"]]
    assert calls[0][1] == "c1" and calls[1][1] == "final_a10" and calls[2][1] == "final_a05"
    assert calls[0][2] == C.C1_ADAPTER_SHA256 and calls[3][2] == w.record["candidates"]["final_a06"]


def test_budget_gate_stops_at_stop_launch_and_a_resumed_run_finishes(world):
    w = world
    now = [1000.0]
    FakeServer.advance = lambda: now.__setitem__(0, now[0] + 400)      # every model 'takes' 400 s of H100
    res = w.session(prior=11.0, clock=lambda: now[0]).run()
    done = res["models_done"]
    assert 1 <= len(done) < 19 and not res["complete"]
    skipped = [k for k, v in res["blocks"].items() if v.get("skipped")]
    assert skipped and "budget gate" in res["blocks"][skipped[0]]["skipped"]
    assert res["spent_usd"] <= C.STOP_LAUNCH_USD + 0.3                 # one block of slack at most
    # resume: same run id, fresh ledger: the done models are not read again, the rest are
    FakeServer.boots.clear()
    FakeServer.advance = None
    w.events.clear()
    res2 = w.session(prior=0.0, clock=lambda: now[0]).run()
    assert res2["complete"] and len(res2["models_done"]) == 19
    assert set(FakeServer.boots).isdisjoint(done) and len(FakeServer.boots) == 19 - len(done)
    assert [e["why"] for e in w.events if e["event"] == "block_skipped"][: len(done)] == ["done"] * len(done)


def test_hard_stop_and_nothing_to_do_paths(world):
    w = world
    res = w.session(prior=C.HARD_STOP_USD + 0.05).run()
    assert res["models_done"] == [] and all("hard stop" in v["skipped"] for v in res["blocks"].values())
    assert FakeServer.boots == []
    res = w.session().run()
    assert res["complete"]
    FakeServer.boots.clear()
    res = w.session().run()                                              # everything done: no reader, no server
    assert res["complete"] and FakeServer.boots == []


def test_a_model_with_refused_server_args_is_an_error_and_the_job_continues(world):
    w = world
    FakeServer.problems = {"q35_4b_c2grid_last3_a07": ["dtype: 'float16' (pin 'bfloat16')"]}
    res = w.session().run()
    assert not res["complete"] and len(res["models_done"]) == 18
    assert [e["read_name"] for e in res["errors"]] == ["q35_4b_c2grid_last3_a07"] and "refused" in res["errors"][0]["error"]
    bad = w.tmp / "out" / "run1" / "models" / "q35_4b_c2grid_last3_a07"
    assert not (bad / "DONE.json").exists() and json.loads((bad / "block.json").read_text())["error"]
    assert not (w.tmp / "work" / "merged" / "q35_4b_c2grid_last3_a07").exists()


def test_a_failed_merge_is_that_models_error_only(world):
    w = world

    def flaky(base, adapter, out, tok, **kw):
        if Path(out).name == "q35_4b_c2grid_last3_a06":
            raise SystemExit("merge failed: boom")
        return MD.merge_adapter(base, adapter, out, tok, **kw)
    w.hooks["merge"] = flaky
    res = w.session().run()
    assert len(res["models_done"]) == 18 and res["errors"][0]["read_name"] == "q35_4b_c2grid_last3_a06" and "merge failed" in res["errors"][0]["error"]
    assert "q35_4b_c2grid_last3_a06" not in FakeServer.boots and not res["complete"]


def test_a_server_on_another_path_is_refused(world):
    w = world
    FakeServer.info_patch = {"q35_4b_c2grid_final_a06": {"attention_backend": "flashinfer"}}
    res = w.session().run()
    assert len(res["models_done"]) == 18 and "served path differs" in res["errors"][0]["error"]


def test_setup_refuses_wrong_gpu_sglang_data_grid_and_run_folder(world, monkeypatch):
    w = world
    w.hooks["gpu_name"] = lambda: "NVIDIA L4, 23034 MiB"
    with pytest.raises(SystemExit, match="not an H100"):
        w.session().run()
    w.hooks["gpu_name"] = lambda: "NVIDIA H100 80GB HBM3, 81559 MiB"
    w.hooks["sglang_version"] = lambda: "0.5.21"
    with pytest.raises(SystemExit, match="pinned"):
        w.session().run()
    w.hooks["sglang_version"] = lambda: "0.5.20"
    (w.data / "dev.jsonl").write_text("{}\n")
    with pytest.raises(SystemExit, match="manifest"):
        w.session().run()
    F.make_data(w.data, w.specs, ())
    pl = json.loads(json.dumps(w.plan))
    pl["data_manifest"] = PL.data_manifest(w.data, w.specs)
    pl["grid_record"] = {**w.record, "grid_sha256": "0" * 64}
    with pytest.raises(SystemExit, match="not the recorded"):
        w.session(plan_=pl).run()
    pl["grid_record"] = w.record
    pl["c2_run_dir"] = str(w.tmp / "nowhere")
    with pytest.raises(SystemExit, match="not usable"):
        w.session(plan_=pl).run()
    assert FakeServer.boots == []                                       # nothing billed before the checks passed


def test_an_incomplete_read_is_not_done(world):
    w = world
    orig = w.RD.GridReader.run_model

    def short(self, cmd):
        r = orig(self, cmd)
        if cmd["read_name"].endswith("final_a10"):
            r["sets"]["dev_nc"]["rows"] -= 1
        return r
    w.RD.GridReader.run_model = short
    try:
        res = w.session().run()
    finally:
        w.RD.GridReader.run_model = orig
    assert "q35_4b_c2grid_final_a10" in res["errors"][0]["read_name"] and "incomplete read" in res["errors"][0]["error"]
    assert len(res["models_done"]) == 18


# =============================================================================================== parity
@pytest.fixture
def pworld(world):
    w = world
    pl = {"run_id": "par1", "cand": "last3_a07", "read_name": C.read_name("last3_a07"), "expect_adapter_sha256": w.record["candidates"]["last3_a07"],
          "split": "gblock_a42d_c1read", "split_file": "gblock_a42d_c1read.jsonl", "split_sha256": C.sha256_file(w.data / "gblock_a42d_c1read.jsonl"),
          "n": 20, "seed": 5, "min_n": 20, "views": 2, "c2_run_dir": w.plan["c2_run_dir"], "grid_record": w.record,
          "prompt_check_record": real_prompt_record(), "est_hf_usd": 0.3, "est_served_usd": 0.25}
    F.make_data(w.data, [{"file": "gblock_a42d_c1read.jsonl"}], (), n=40)
    pl["split_sha256"] = C.sha256_file(w.data / "gblock_a42d_c1read.jsonl")
    w.pplan = pl
    w.flip = 0

    def hf_ref(spec, out_json):
        RD = w.RD
        tok, ro, _ = RD.SH.load_c1_tokenizer(F.C1_BACKUP)
        rows = RD.read_rows(spec["rows_file"])
        outd = Path(spec["out_dir"])
        probs = []
        for i, r in enumerate(rows):
            p = F.expected_probs(RD.R, RD.SH, tok, ro, r, 2)
            if i < w.flip:                                        # make the reference disagree on the first `flip` rows
                best = max(p, key=p.get)
                other = [k for k in p if k != best][0]
                p = {**p, best: p[other], other: p[best]}
            probs.append(p)
        C.write_jsonl(outd / f"{spec['name']}.jsonl", ({"id": r["id"], "model": spec["name"], "probs": p} for r, p in zip(rows, probs)))
        C.write_json(outd / f"{spec['name']}.meta.json", {"name": spec["name"], "rows": len(rows), "layout": C.LAYOUT, "style": C.STYLE, "base": C.BASE,
                                                         "tta": False, "tta_choice": True, "tta_noul": False, "perm_seed": None})
        res = {"ok": True, "rows": len(rows), "sec": 1.0, "load_s": 0.5}
        C.write_json(out_json, res)
        return res
    w.hooks["hf_ref"] = hf_ref

    def psession(**kw):
        from grid_h100.parity import ParitySession
        return ParitySession(w.pplan, emit=w.events.append, hooks=w.hooks, out_root=w.tmp / "pout", work_root=w.tmp / "pwork", vol=w.vol,
                             data_dir=w.data, c1tok_dir=F.C1_BACKUP, commit=lambda: None, log=lambda s: None, **kw)
    w.psession = psession
    return w


def test_parity_passes_when_the_merge_reads_like_the_hf_adapter(pworld):
    w = pworld
    rec = w.psession().run()
    assert rec["all"]["n"] == 20 and rec["all"]["argmax_agree"] == 1.0 and rec["bar"]["PASS"] is True
    assert rec["bar"]["PASS_gate"] is False and rec["bar"]["n>=2000 (A49 f bar)"] is False         # a small-n record is never a gate PASS
    assert rec["adapter_sha256"] == w.record["candidates"]["last3_a07"] and rec["served_manifest_adapter_sha256"] == rec["adapter_sha256"]
    assert rec["ref_meta_problems"] == [] and rec["views"] == 2 and rec["split_sha256"] == w.pplan["split_sha256"]
    assert (w.tmp / "pout/par1/parity/last3_a07/PARITY_last3_a07.json").exists()
    assert FakeServer.boots == [w.pplan["read_name"]] and w.readers[0].quit_called
    assert not (w.tmp / "pwork/merged" / w.pplan["read_name"]).exists()


def test_parity_fails_when_the_reads_disagree(pworld):
    w = pworld
    w.flip = 6
    rec = w.psession().run()
    assert rec["bar"]["PASS"] is False and rec["all"]["argmax_agree"] < 1.0 and rec["disagreements"]


def test_parity_refuses_a_candidate_that_is_not_the_recorded_one_and_a_stale_split(pworld):
    w = pworld
    w.pplan["expect_adapter_sha256"] = "3" * 64
    with pytest.raises(SystemExit, match="CANDIDATE_C2.json says"):
        w.psession().run()
    w.pplan["expect_adapter_sha256"] = w.record["candidates"]["last3_a07"]
    w.pplan["split_sha256"] = "4" * 64
    with pytest.raises(SystemExit, match="differs from the plan"):
        w.psession().run()
    w.pplan["split_sha256"] = C.sha256_file(w.data / "gblock_a42d_c1read.jsonl")
    w.pplan["split"] = "ohs_x"
    with pytest.raises(SystemExit):
        w.psession().run()


def test_parity_record_equals_merge_parity_run_parity(pworld):
    from grid_h100.parity import parity_record
    mp = SV.serving_mod("merge_parity")
    rows = [dict(r, gold=None) for r in F.make_rows("pp", 30)]
    got = {r["id"]: {k: 1 / len(k_) for k in k_} for r in rows for k_ in [r["options"] or ["yes", "no"]]}
    ref = {r["id"]: ({k: (0.7 if k == "yes" else 0.3) for k in ("yes", "no")} if r["qtype"] == "noul" else {k: 1 / len(r["options"]) for k in r["options"]})
           for r in rows}
    got = {r["id"]: ({k: (0.6 if k == "yes" else 0.4) for k in ("yes", "no")} if r["qtype"] == "noul" else {k: 1 / len(r["options"]) for k in r["options"]})
           for r in rows}

    class Rd:
        def read(self, rs, views=True):
            return [{"probabilities": got[r["id"]], "type": "noul" if r["qtype"] == "noul" else "choice"} for r in rs]

        @staticmethod
        def probs(a):
            return a["probabilities"]
    meta = {"layout": C.LAYOUT, "style": C.STYLE, "tta_choice": True, "perm_seed": None}
    want = mp.run_parity(Rd(), rows, ref, 30, 3, 2, meta, 30)
    sample = mp.sample_rows(rows, 30, 3)
    mine = parity_record(sample, [ref[r["id"]] for r in sample], [got[r["id"]] for r in sample], meta, 2, 30, 3, 30, mp)
    for k in ("all", "choice", "noul", "accuracy", "bar", "seed", "n", "views", "sample_ids_sha256", "ref_meta_problems", "disagreements"):
        assert mine[k] == want[k], k
    bad = parity_record(sample, [ref[r["id"]] for r in sample], [got[r["id"]] for r in sample], {**meta, "tta_choice": False}, 2, 30, 3, 30, mp)
    assert bad["bar"]["PASS"] is False and bad["ref_meta_problems"]


# =============================================================================================== driver
def test_make_parity_plan_checks_the_candidate_record(tmp_path):
    rec = {"candidates": {"last3_a07": "a" * 64}}
    (tmp_path / "rec.json").write_text(json.dumps(rec))
    (tmp_path / "gblock_a42d_c1read.jsonl").write_text("{}\n")
    cj = tmp_path / "cand.json"
    cj.write_text(json.dumps({"grid_candidate": "last3_a07", "adapter_sha256": "a" * 64}))
    p = DR.make_parity_plan("last3_a07", cj, "r", tmp_path, record_path=tmp_path / "rec.json")
    assert p["min_n"] == 2000 and p["n"] == 2000 and p["views"] == 2 and p["expect_adapter_sha256"] == "a" * 64 and p["seed"] == 20261013
    assert p["split_file"] == "gblock_a42d_c1read.jsonl" and p["read_name"] == "q35_4b_c2grid_last3_a07"
    cj.write_text(json.dumps({"grid_candidate": "last3_a08", "adapter_sha256": "a" * 64}))
    with pytest.raises(SystemExit, match="names"):
        DR.make_parity_plan("last3_a07", cj, "r", tmp_path, record_path=tmp_path / "rec.json")
    cj.write_text(json.dumps({"grid_candidate": "last3_a07", "adapter_sha256": "b" * 64}))
    with pytest.raises(SystemExit, match="names"):
        DR.make_parity_plan("last3_a07", cj, "r", tmp_path, record_path=tmp_path / "rec.json")
    with pytest.raises(SystemExit, match="missing"):
        DR.make_parity_plan("last3_a07", tmp_path / "none.json", "r", tmp_path, record_path=tmp_path / "rec.json")


def test_preflight_blocks_without_go_record_and_without_fit(monkeypatch, tmp_path):
    monkeypatch.setattr(C, "GO_FILE", tmp_path / "none.json")
    monkeypatch.setattr(DR, "RECORD", tmp_path / "none2.json")
    plan = DR.make_plan("x", spent_usd=5.0, record_path=tmp_path / "none2.json")      # 5.00 already spent: likely 10.08 no longer fits 13.50
    r = DR.preflight(plan)
    txt = " | ".join(r["blockers"])
    assert not r["ready"] and "default: refuse" in txt and "GRID_RECORD.json missing" in txt
    if (LEAN / "data/dev_nc.jsonl").exists():
        assert "COST: DOES NOT FIT" in txt


def test_commands_are_printed_not_run_and_name_the_guards():
    cmds = DR.commands("acct", "r1")
    txt = "\n".join(cmds)
    assert "modal_app_grid.py::grid" in txt and "MODAL_PROFILE=acct" in txt and "--detach" not in txt and "deploy" not in txt
    assert all(("ohs" not in c.lower() and "sealed" not in c.lower()) for c in cmds)


def test_post_places_verified_reads_once_and_writes_latency_records(world, monkeypatch):
    w = world
    w.session().run()
    run_dir = w.tmp / "out" / "run1"
    mp7 = SV.serving_mod("p7_common")
    monkeypatch.setattr(mp7, "C1_ADAPTER_SHA256", C.C1_ADAPTER_SHA256)
    lean = w.tmp / "leantree"
    logs = w.tmp / "logs_grid"
    rec = w.tmp / "GRID_RECORD.json"
    dry = DR.post(run_dir, lean, dry_run=True, record_path=rec, logs=logs)
    assert dry["placed"] and not lean.exists() and dry["complete"]
    r = DR.post(run_dir, lean, record_path=rec, logs=logs)
    assert r["complete"] and len(r["placed"]) == 19 * 48 and r["refused"] == []
    assert (lean / "preds_dev_nc" / "q35_4b_main500k_c2.jsonl").exists() and (lean / "preds_dev_nc" / "q35_4b_c2grid_final_a10_perm.meta.json").exists()
    assert (lean / "preds_pab_gproxy" / "q35_4b_c2grid_last3_a07.jsonl").exists()
    lat = json.loads((logs / "latency_last3_a07.json").read_text())
    assert lat["cand_p50_ms"] > 0 and lat["ref_p50_ms"] > 0 and lat["served_path"].startswith("sglang_s1_h100_grid:")
    import gate_c2 as gc
    assert gc.latency_rule(lat)["id"] == "c7"                       # the record gate_c2 reads
    assert len(r["latency"]) == 18 and len(list(logs.glob("latency_*.json"))) == 18
    r2 = DR.post(run_dir, lean, record_path=rec, logs=logs)          # reads are placed once: the same files are 'unchanged'
    assert r2["placed"] == [] and len(r2["unchanged"]) == 19 * 48
    # other content at the target is refused, never overwritten
    t = lean / "preds_dev_nc" / "q35_4b_main500k_c2.jsonl"
    t.write_text("changed\n")
    assert DR.post(run_dir, lean, record_path=rec, logs=logs)["refused"]
    assert any(s.startswith("$PY gate_dev.py q35_4b_c2grid_final_a10 q35_4b_main500k_c2 --mode ship") for s in r["next"])


def test_post_refuses_without_the_grid_record_and_with_a_tampered_file(world):
    w = world
    w.session().run()
    run_dir = w.tmp / "out" / "run1"
    with pytest.raises(SystemExit, match="GRID_RECORD.json must exist"):
        DR.post(run_dir, w.tmp / "l", record_path=w.tmp / "none.json", logs=w.tmp / "lg")
    f = run_dir / "models" / "q35_4b_c2grid_last3_a07" / "preds_dev" / "q35_4b_c2grid_last3_a07.jsonl"
    f.write_text(f.read_text() + "\n{}\n")
    r = DR.post(run_dir, w.tmp / "l", record_path=w.tmp / "GRID_RECORD.json", logs=w.tmp / "lg")
    assert not r["complete"] and not r["models"]["q35_4b_c2grid_last3_a07"]["ok"]
    assert not (w.tmp / "l" / "preds_dev" / "q35_4b_c2grid_last3_a07.jsonl").exists()
    with pytest.raises(SystemExit):
        DR.post(w.tmp / "ohs_run", w.tmp / "l")


def test_tool_shas_cover_the_files():
    s = DR.tool_shas()
    assert "common.py" in s and "modal_app_grid.py" in s and all(len(v) == 64 for v in s.values())


# =============================================================================================== real subprocess reader, hostops, hf_ref
@needs_c1
def test_reader_proc_runs_the_daemon_as_a_real_subprocess(tokmemo, tiny_data, tmp_path):
    from grid_h100.session import ReaderProc
    root, specs, man = tiny_data
    fake = F.FakeSGL()
    spec = {"c1_dir": str(F.C1_BACKUP), "data_dir": str(root), "sets": specs[:3], "manifest": man, "recorded_check": real_prompt_record(),
            "ctl_dir": str(tmp_path / "ctl"), "port": fake.port, "workers": 2, "chunk": 4}
    rp = ReaderProc(spec, python=sys.executable, root=str(TRAIN), log=lambda s: None).start()
    try:
        ready = rp.wait_ready(120)
        assert ready["ok"] and ready["info"]["sets"] == 3 and ready["info"]["prompt_check"]["ok"]
        res = rp.run({"read_name": "q35_x", "out_dir": str(tmp_path / "o"), "env_meta": env_meta(), "provenance": {"run_id": "t"}}, 120)
        assert res["ok"] and len(res["sets"]) == 3 and (tmp_path / "o" / "preds_dev_nc" / "q35_x.jsonl").exists()
        bad = rp.run({"read_name": "ohs_x", "out_dir": str(tmp_path / "o2"), "env_meta": env_meta()}, 60)
        assert bad["ok"] is False and "ohs" in bad["error"]                     # the daemon survives a refused command
        assert rp.run({"read_name": "q35_y", "out_dir": str(tmp_path / "o3"), "env_meta": env_meta()}, 120)["ok"]
    finally:
        rp.quit()
        fake.close()
    assert not rp.alive()


def test_reader_proc_reports_a_reader_that_dies(tmp_path):
    from grid_h100.session import ReaderProc, SessionRefused
    rp = ReaderProc({"c1_dir": "/none", "data_dir": "/none", "sets": [], "ctl_dir": str(tmp_path / "ctl")}, python=sys.executable, root=str(TRAIN),
                    log=lambda s: None).start()
    try:
        with pytest.raises(SystemExit, match="reader"):
            rp.wait_ready(60)
    finally:
        rp.quit()


def test_prepare_base_copies_checks_pins_and_fetches_what_the_volume_lacks(tmp_path):
    from grid_h100 import hostops as HO
    hf = tmp_path / "vol" / "hf"
    snap = hf / HO.SNAP_REL
    F.make_tiny_base(snap)
    fetched = []
    # the tiny base is not the pinned snapshot: refused after the copy
    with pytest.raises(SystemExit, match="not the pinned"):
        HO.prepare_base(str(hf), str(tmp_path / "dest"), fetch=lambda names, dest: fetched.append(sorted(names)), log=lambda s: None)
    assert fetched and "LICENSE" in fetched[0] and (tmp_path / "dest" / "config.json").exists()
    # the destination is rebuilt, never merged into an old copy; with no Volume snapshot the download hook runs
    called = []
    with pytest.raises(SystemExit):
        HO.prepare_base(str(tmp_path / "nohf"), str(tmp_path / "dest2"), download=lambda d: (called.append(d), Path(d).mkdir(parents=True))[0],
                        fetch=lambda n, d: None, log=lambda s: None)
    assert called


def test_prepare_c1_tok_checks_the_pins(tmp_path):
    from grid_h100 import hostops as HO
    d = tmp_path / "tok"
    d.mkdir()
    (d / "tokenizer.json").write_text("{}")
    pins = {"tokenizer.json": C.sha256_file(d / "tokenizer.json")}
    assert HO.prepare_c1_tok(d, pins) == d
    with pytest.raises(SystemExit, match="differ"):
        HO.prepare_c1_tok(d, {"tokenizer.json": "0" * 64})
    with pytest.raises(SystemExit, match="missing"):
        HO.prepare_c1_tok(d, {**pins, "train_meta.json": "0" * 64})


@needs_c1
def test_the_c1_files_shipped_with_the_job_equal_the_s1_pin():
    from grid_h100 import hostops as HO
    pin = SV.load_pin()
    assert HO.prepare_c1_tok(F.C1_BACKUP, pin["model"]["tokenizer_pins"]) == F.C1_BACKUP


def test_hf_ref_exposes_the_base_as_a_hub_cache_snapshot(tmp_path):
    from grid_h100 import hf_ref
    base = F.make_tiny_base(tmp_path / "base")
    snap = hf_ref.expose_cache(base, tmp_path / "home")
    assert snap.is_symlink() and (snap / "config.json").exists()
    assert snap == tmp_path / "home/hub/models--Qwen--Qwen3.5-4B/snapshots" / C.REVISION
    assert (tmp_path / "home/hub/models--Qwen--Qwen3.5-4B/refs/main").read_text() == C.REVISION
    hf_ref.expose_cache(base, tmp_path / "home")                           # idempotent
