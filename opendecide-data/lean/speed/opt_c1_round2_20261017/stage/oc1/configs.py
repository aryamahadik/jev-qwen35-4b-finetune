"""oc1.configs: the server CONFIGS of the optimisation session (stdlib only).

Findings from the CPU preflight of 17 Oct 2026 (results/preflight_*.json, results/inspect_*.json; SGLang 0.5.20 in
lmsysorg/sglang:v0.5.20-cu130; its launch_server --help lists 492 flags) that shape the configs:
  * chunked prefill: `--chunked-prefill-size -1` disables it (documented).
  * prefill CUDA graphs: `--cuda-graph-backend-prefill {full,breakable,tc_piecewise,disabled}`; "breakable is the CUDA
    default but not multimodal-compatible" and a multimodal arch is "piecewise-incompatible until validated", so S1
    (a Qwen3_5ForConditionalGeneration checkpoint) is on the multimodal-breakable allowlist, so its prefill graphs are the
    DEFAULT; the arm is a control (`disabled`), plus explicit tc_piecewise. `--language-only` is the encoder/prefill/decode
    disaggregation switch (not a plain text-only mode) and is NOT used.
  * prefix cache: the UNIFIED radix tree is the default tree cache in 0.5.20 (SGLANG_ENABLE_UNIFIED_RADIX_TREE is a
    deprecated no-op), S1's `--mamba-radix-cache-strategy extra_buffer` is the hybrid (GDN state) cache. So "+unified radix"
    is S1 itself; the arms here are ablations (`--disable-radix-cache`) and a strategy variant (`no_buffer`).
  * /v1/score exists (label_token_ids + apply_softmax = softmax over the label tokens ONLY, single-item mode = each item
    is query+item as its own prompt; `--enable-mis` is the multi-item mode and needs flashinfer, radix cache off).
  * quantization: `--quantization w8a8_fp8` = per-channel static weights + dynamic per-token activations, computed ONLINE
    from the BF16 checkpoint (SGLang's own path; no ignore list, so it also quantizes in_proj_ba and the vision tower). The
    "careful" arm keeps SGLang's path but wraps W8A8Fp8Config.get_quant_method with an ignore list (oc1/pypatch/sitecustomize.py,
    switched on by env, inherited by SGLang's spawned processes): vision tower, in_proj_ba (= in_proj_a + in_proj_b, fused by
    SGLang), MTP stay BF16; lm_head / embeddings are not linears. No checkpoint is written, so the leave-one-group sweep is
    just another ignore list. INT8: the same hook with OC1_ONLINE_MODE=int8 (per-channel int8 weights, per-token int8
    activations, SGLang's own w8a8_int8 kernels); SmoothQuant = the BF16 -> BF16 transform of oc1/smooth.py served that way.
    SGLang fuses q/k/v -> qkv_proj, gate/up -> gate_up_proj, in_proj_qkv/in_proj_z -> in_proj_qkvz, in_proj_b/in_proj_a -> in_proj_ba.

A Config is data only: flags (appended to S1's command), env, model folder, readout, which measurements to run. The
S1 command itself is replicated from hosting/sglang_host.server_cmd (a test asserts equality with the original).
"""
from __future__ import annotations

import shlex
from dataclasses import dataclass, field

from . import common as C

PORT = 30000
CONTEXT_LEN = 16384 + 64          # decoder_io.MAX_LEN + 64 (sglang_host.CONTEXT_LEN)
S1_DEFAULTS = {"max_running_requests": 64, "max_mamba_cache_size": 400}
SERVER_ENV = {"SGLANG_RETURN_ORIGINAL_LOGPROB": "1", "HF_HUB_OFFLINE": "1", "TOKENIZERS_PARALLELISM": "false"}


def s1_cmd(model_path, python: str = "python3", port: int = PORT, max_running_requests: int = 64,
           max_mamba_cache_size: int = 400, context_length: int = CONTEXT_LEN) -> list:
    """Arm S1's launch command (hosting/sglang_host.server_cmd with fp8=False, no optional args)."""
    return [python, "-m", "sglang.launch_server", "--model-path", str(model_path), "--host", "127.0.0.1",
            "--port", str(int(port)), "--dtype", "bfloat16", "--enable-fp32-lm-head",
            "--context-length", str(int(context_length)),
            "--mamba-radix-cache-strategy", "extra_buffer", "--mamba-ssm-dtype", "float32",
            "--linear-attn-backend", "triton", "--linear-attn-prefill-backend", "triton",
            "--max-running-requests", str(int(max_running_requests)),
            "--max-mamba-cache-size", str(int(max_mamba_cache_size)),
            "--random-seed", "0", "--sampling-defaults", "openai", "--log-level", "warning"]


@dataclass
class Config:
    name: str
    desc: str
    extra: list = field(default_factory=list)        # flags appended to S1's command
    env: dict = field(default_factory=dict)
    model: str = "merged"                            # merged | fp8_careful | fp8_leave_* | int8_sq (folder under /out/models)
    drop: list = field(default_factory=list)         # S1 flags removed (flag only, or flag + value)
    readouts: list = field(default_factory=lambda: ["generate"])
    measures: list = field(default_factory=lambda: ["parity_sub", "latency", "throughput"])
    needs_flags: list = field(default_factory=list)  # must appear in `launch_server --help`
    est_boot_s: int = 150
    est_measure_s: int = 120
    fp8: bool = False                                # FP8 parity bar (1.0 pt accuracy) applies
    priority: int = 5                                # lower runs earlier
    note: str = ""

    def cmd(self, model_path, python="python3", port=PORT, **kw) -> list:
        cmd = s1_cmd(model_path, python, port, **kw)
        for d in self.drop:
            while d in cmd:
                i = cmd.index(d)
                j = i + 2 if i + 1 < len(cmd) and not cmd[i + 1].startswith("--") else i + 1
                del cmd[i:j]
        return cmd + list(self.extra)

    def server_env(self, base=None) -> dict:
        import os
        env = {k: v for k, v in (os.environ if base is None else base).items() if k not in ("PYTHONPATH", "VIRTUAL_ENV")}
        env.update(SERVER_ENV)
        env.setdefault("TRITON_CACHE_DIR", "/tmp/oc1_triton")     # later boots of the session reuse the compiled kernels
        env.update(self.env)
        return env

    def shell(self, model_path, python="python3") -> str:
        return shlex.join(self.cmd(model_path, python))


def build_configs() -> dict:
    cs = [
        Config("s1", "S1 baseline: merged BF16, fp32 lm head, unified radix cache with the hybrid (GDN) extra_buffer strategy, "
                     "breakable prefill CUDA graphs (the 0.5.20 default for Qwen3_5ForConditionalGeneration), SGLang defaults",
               measures=["parity_full", "latency", "throughput", "prefix", "score_readout", "vision", "voice_c1", "e2e"],
               est_boot_s=170, est_measure_s=620, priority=0,
               note="the reference every other config is gated against, in the same session"),
        Config("s1_vision", "S1 again, image arms only (second session: the first session's native arm failed on an encoding bug, now fixed)",
               measures=["throughput", "vision"], est_boot_s=120, est_measure_s=170, priority=0,
               note="same flags as s1; in-container baseline for vit_graph's image latency and for the leave-one-group arms' throughput"),
        Config("chunk_off", "S1 + --chunked-prefill-size -1 (no prompt chunking)",
               extra=["--chunked-prefill-size", "-1"], needs_flags=["--chunked-prefill-size"], priority=1),
        Config("gdn_flashinfer", "GDN prefill/decode kernels from FlashInfer instead of Triton (needs the prefix cache OFF: "
                                 "the extra_buffer strategy requires the triton backend)",
               drop=["--mamba-radix-cache-strategy", "--linear-attn-backend", "--linear-attn-prefill-backend"],
               extra=["--disable-radix-cache", "--linear-attn-backend", "flashinfer", "--linear-attn-prefill-backend", "flashinfer"],
               needs_flags=["--linear-attn-backend", "--linear-attn-prefill-backend", "--disable-radix-cache"],
               measures=["parity_sub", "latency", "throughput"], priority=2,
               note="24 of C1's 32 layers are GDN: the prefill kernel is the main compute; loses prefix reuse (see radix_off)"),
        Config("fp8_w8a8_online", "S1 + --quantization w8a8_fp8 (online per-channel weights, dynamic per-token activations)",
               extra=["--quantization", "w8a8_fp8"], needs_flags=["--quantization"], fp8=True, priority=3,
               note="quantizes EVERY linear incl. in_proj_ba and the vision tower; lm_head/embeddings stay BF16"),
        Config("fp8_careful", "FP8 W8A8 careful (online): per-channel weights, dynamic per-token activations on every linear EXCEPT "
                              "the vision tower, in_proj_ba (= in_proj_a/in_proj_b) and MTP; lm_head and embed_tokens are not linears",
               extra=["--quantization", "w8a8_fp8"], env=patch_env("fp8", CAREFUL_IGNORE), fp8=True, priority=4,
               needs_flags=["--quantization"], note="SGLang's own online w8a8_fp8 path + oc1/pypatch (ignore list); no checkpoint is written"),
        Config("graph_off", "S1 + --cuda-graph-backend-prefill disabled (control: what S1's default breakable prefill graphs give)",
               extra=["--cuda-graph-backend-prefill", "disabled"], needs_flags=["--cuda-graph-backend-prefill"],
               priority=5),
        Config("radix_off", "S1 + --disable-radix-cache (ablation: what the unified/mamba prefix cache is worth)",
               extra=["--disable-radix-cache"], drop=["--mamba-radix-cache-strategy"], needs_flags=["--disable-radix-cache"],
               measures=["parity_sub", "latency", "throughput", "prefix"], priority=6,
               note="mamba strategy flag dropped (it needs the cache)"),
        Config("sched_big", "S1 + --schedule-policy lpm --max-prefill-tokens 32768 (more prefill per step, cache-aware order)",
               extra=["--schedule-policy", "lpm", "--max-prefill-tokens", "32768"],
               needs_flags=["--schedule-policy", "--max-prefill-tokens"], measures=["parity_sub", "latency", "throughput", "prefix"],
               priority=7),
        Config("vit_graph", "S1 + SGLANG_VIT_ENABLE_CUDA_GRAPH=1 (CUDA graph for the vision encoder): image-decision latency only",
               env={"SGLANG_VIT_ENABLE_CUDA_GRAPH": "1"}, measures=["vision"], est_measure_s=150, priority=8,
               note="text path untouched; only run if the S1 block's vision arm worked and budget remains"),
        Config("graph_tc_piecewise", "S1 + --cuda-graph-backend-prefill tc_piecewise (torch.compile + piecewise)",
               extra=["--cuda-graph-backend-prefill", "tc_piecewise"], needs_flags=["--cuda-graph-backend-prefill"],
               est_boot_s=360, priority=8, note="not allowlisted for this multimodal arch; explicit choice skips the cascade; may refuse to boot"),
        Config("int8_online", "W8A8 INT8 (online, no smoothing): per-channel int8 weights, dynamic per-token int8 activations, same ignore list as fp8_careful",
               extra=["--quantization", "w8a8_fp8"], env=patch_env("int8", CAREFUL_IGNORE), fp8=True, priority=9,
               needs_flags=["--quantization"], note="control for int8_sq: plain round-to-nearest"),
        Config("int8_sq", "SmoothQuant W8A8 INT8: the BF16 checkpoint is smoothed (activation outliers moved into the weights and the "
                          "preceding RMSNorm) by oc1.smooth, then served as int8_online",
               model="smooth", extra=["--quantization", "w8a8_fp8"], env=patch_env("int8", CAREFUL_IGNORE), fp8=True, priority=9,
               needs_flags=["--quantization"], note="needs the smoothed checkpoint (calibration pass on a dev subset)"),
        Config("radix_nobuf", "S1 with --mamba-radix-cache-strategy no_buffer (needs --disable-overlap-schedule)",
               drop=["--mamba-radix-cache-strategy"],
               extra=["--mamba-radix-cache-strategy", "no_buffer", "--disable-overlap-schedule"],
               measures=["parity_sub", "latency", "throughput", "prefix"], priority=11),
    ]
    for g in FP8_GROUP_REGEX:
        cs.append(Config(f"fp8_leave_{g}", f"FP8 careful with the '{g}' linears kept in BF16 (leave-one-group sweep)",
                         extra=["--quantization", "w8a8_fp8"], env=patch_env("fp8", CAREFUL_IGNORE + FP8_GROUP_REGEX[g]),
                         fp8=True, priority=10, needs_flags=["--quantization"], measures=["parity_sub", "latency", "throughput"],
                         est_measure_s=140))
    return {c.name: c for c in cs}


# The "careful" ignore list (regexes searched in SGLang's module prefix): vision tower, the fused in_proj_ba (= in_proj_a +
# in_proj_b, 32-dim and precision-sensitive), MTP, lm_head, embeddings. SGLang fuses q/k/v -> qkv_proj, gate/up -> gate_up_proj,
# in_proj_qkv/in_proj_z -> in_proj_qkvz, in_proj_b/in_proj_a -> in_proj_ba (qwen3_5.py / qwen3_next.py, preflight 17 Oct).
CAREFUL_IGNORE = [r"visual", r"in_proj_ba", r"in_proj_a\b", r"in_proj_b\b", r"(^|\.)mtp\.", r"lm_head", r"embed_tokens"]
# leave-one-group sweep (module-name regexes in SGLang's namespace; the first FP8 boot's report must show each matches > 0)
FP8_GROUP_REGEX = {
    "attn": [r"self_attn\.(qkv_proj|o_proj)"],
    "gdn_in": [r"linear_attn\.in_proj_qkvz"],
    "gdn_out": [r"linear_attn\.out_proj"],
    "mlp_in": [r"mlp\.gate_up_proj"],
    "mlp_down": [r"mlp\.down_proj"],
}
PYPATCH_DIR_REMOTE = "/root/oc1/pypatch"
QUANT_REPORT = "/tmp/oc1_quant_report.jsonl"


def patch_env(mode: str, ignore: list) -> dict:
    """Env that switches oc1/pypatch/sitecustomize.py on in SGLang's processes (see that file)."""
    import json as _json
    return {"OC1_ONLINE_MODE": mode, "OC1_IGNORE": _json.dumps(ignore), "OC1_REPORT": QUANT_REPORT,
            "PYTHONPATH": PYPATCH_DIR_REMOTE}


CONFIGS = build_configs()


def supported(cfg: Config, flags: dict | None) -> tuple:
    """(ok, reason): every flag the config needs appears in the server's --help flag table (None = unknown = ok)."""
    if not flags:
        return True, "flag table unknown (preflight not loaded)"
    miss = [f for f in cfg.needs_flags if f not in flags]
    return (not miss), (f"missing flags {miss}" if miss else "all flags present")


def order(names=None, budget_priority_max: int = 99) -> list:
    cs = [CONFIGS[n] for n in (names or CONFIGS)]
    return [c.name for c in sorted(cs, key=lambda c: (c.priority, c.name)) if c.priority <= budget_priority_max]
