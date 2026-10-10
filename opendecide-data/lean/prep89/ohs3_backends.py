"""Model backends for the OHS-3 OpenDecide run and server.

  real    the pre-registered adapter on a GPU (the L4 VM or the H100), loaded like od_gcp.py predict: decoder_io.load
          with the config's base / revision / layout / style (a conflict with the adapter's train_meta raises),
          adapter sha256 (and for a PRISM-X model the prism_x.safetensors sha256) checked against the config first,
          base commit checked after load, then merge_and_unload.
  tiny    CPU dry run: a tiny RANDOM Qwen3 (1 layer, hidden 32, seed 0) with the REAL 4B-E tokenizer, read in the
          adapter's train_meta layout (schema_branch_mark / cygnet) through the real decoder_io prompt, Readout,
          cand_logits and to_probs code (as hosting/test_direct_host_local.py). Answers are noise; the code path is real.
  tiny_px CPU dry run of the 2B path: a tiny random Qwen3 (2 layers, seed 1) with the REAL 2B tokenizer and layout
          (backups/gcp_models/q35_2b_armI_1600) and a PRISM-X control plane installed with prism_x.install (the config's
          prism_x parts; seeded non-zero weights so it changes the answer). Read eagerly through the real decoder_io /
          prism_x code (token roles, option head). Shadow heads (H2) need Qwen3.5 Gated DeltaNet layers, which this
          transformers version lacks on the Mac, so the dry config names authority + option head only.
  oracle  CPU dry run, SYNTHETIC file only: decoder_io.cand_logits is replaced by logits planted from the synthetic gold
          (known accuracy, a position bias so the 2-view average matters); to_probs and a5_read are the real code.
Every backend checks the PRISM-X state of the loaded model against the config (ohs3_lib.check_prism_x).
"""
from __future__ import annotations

import hashlib
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ohs3_lib as L  # noqa: E402

TINY_TOKENIZER_DIR = L.REPO / "backups" / "gcp_models" / "q35_4b_pxE"  # tokenizer + train_meta only
TINY_TOKENIZER_DIR_2B = L.REPO / "backups" / "gcp_models" / "q35_2b_armI_1600"  # the 2B tokenizer + train_meta only


def lean_dio():
    if str(L.LEAN) not in sys.path:
        sys.path.insert(0, str(L.LEAN))
    import decoder_io
    return decoder_io


def gpu_info():
    import torch
    if not torch.cuda.is_available():
        return {"gpu": None, "torch": torch.__version__}
    return {"gpu": torch.cuda.get_device_name(0), "torch": torch.__version__, "cuda": torch.version.cuda}


def load_real(m, models_dir):
    import torch
    dio = lean_dio()
    if not torch.cuda.is_available():
        raise SystemExit("backend real needs CUDA (the L4 VM or the H100)")
    adapter = Path(models_dir) / m["name"]
    sha = L.sha256_file(adapter / "adapter_model.safetensors")
    if sha != m["adapter_sha256"]:
        raise SystemExit(f"{m['name']}: adapter sha256 {sha[:16]} != pre-registered {m['adapter_sha256'][:16]}")
    px_sha = L.check_prism_x_file(m, adapter)  # the 2B: prism_x.safetensors sha256 == the config's (None for the 4B)
    dio.STYLE = m.get("style") or "cygnet"
    model, tok, info = dio.load(m["base"], "cuda", adapter=str(adapter), revision=m["revision"], layout=m["layout"],
                                style=m.get("style"), force=False, return_info=True)
    commit = getattr(getattr(model, "config", None), "_commit_hash", None)
    if commit is not None and commit != m["revision"]:
        raise SystemExit(f"loaded base commit {commit}, pre-registered {m['revision']}")
    model = model.merge_and_unload()
    model.eval()
    if (dio.LAYOUT, dio.STYLE) != (m["layout"], m["style"]):
        raise SystemExit(f"layout/style {(dio.LAYOUT, dio.STYLE)} != pre-registered {(m['layout'], m['style'])}")
    pxc = L.check_prism_x(m, dio, model)  # the 2B (PRISM-X I): control plane active after the merge; 4B: none
    ro = dio.Readout(tok)
    return {"dio": dio, "model": model, "ro": ro, "dev": "cuda", "tok": tok,
            "info": {"backend": "real", "adapter_sha256": sha, "prism_x_sha256": px_sha, "base_commit": commit,
                     "load": info, "prism_x": pxc,
                     "path": "eager (PRISM-X)" if pxc["active"] else "eager", **gpu_info()}}


def load_tiny(m, tokenizer_dir=TINY_TOKENIZER_DIR, seed=0, layers=1, check=True):
    import torch
    from transformers import AutoTokenizer, Qwen3Config, Qwen3ForCausalLM
    dio = lean_dio()
    info = dio.resolve_prompt([str(tokenizer_dir)], m["base"], None, None, m["revision"])
    dio.LAYOUT, dio.STYLE = info["layout"], info["style"]
    if (dio.LAYOUT, dio.STYLE) != (m["layout"], m["style"]):
        raise SystemExit(f"tiny: layout/style {(dio.LAYOUT, dio.STYLE)} != config {(m['layout'], m['style'])}")
    sha = L.sha256_file(Path(tokenizer_dir) / "adapter_model.safetensors")
    tok = AutoTokenizer.from_pretrained(str(tokenizer_dir))
    tok.padding_side = "right"
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    torch.manual_seed(seed)
    model = Qwen3ForCausalLM(Qwen3Config(vocab_size=len(tok), hidden_size=32, intermediate_size=64,
                                         num_hidden_layers=layers, num_attention_heads=2, num_key_value_heads=1,
                                         head_dim=16, max_position_embeddings=32768, tie_word_embeddings=False)).eval()
    ro = dio.Readout(tok)
    pxc = L.check_prism_x(m, dio, model) if check else None
    return {"dio": dio, "model": model, "ro": ro, "dev": "cpu", "tok": tok,
            "info": {"backend": "tiny", "prism_x": pxc, "note": f"random {layers}-layer Qwen3 (seed {seed}) + real tokenizer "
                                                f"({Path(tokenizer_dir).name}); answers are noise",
                     "tokenizer_dir_adapter_sha256": sha, "sha_matches_config": sha == m["adapter_sha256"],
                     "layout": dio.LAYOUT, "style": dio.STYLE}}


def load_tiny_px(m, tokenizer_dir=TINY_TOKENIZER_DIR_2B, seed=1, scale=0.5):
    """The 2B code path on CPU: tiny random Qwen3 + the real 2B tokenizer/layout + PRISM-X (config parts) installed and
    active, read eagerly. Load it AFTER any other model of the process (decoder_io.load uninstalls PRISM-X; prism_x
    keeps one control plane per process), as the cascade host does with the real models."""
    import torch
    spec = m.get("prism_x")
    if not spec:
        raise SystemExit("tiny_px: the config model names no prism_x")
    be = load_tiny(m, tokenizer_dir, seed=seed, layers=2, check=False)
    import prism_x
    pinfo = prism_x.install(be["model"], prism_x.resolve(spec), "cpu")
    g = torch.Generator().manual_seed(seed)
    with torch.no_grad():  # trained-looking (non-zero) parts, so the control plane changes the answer
        for _, p in prism_x.PX.named_parameters():
            p.copy_(torch.randn(p.shape, generator=g) * scale)
    prism_x.PX.eval()
    be["info"].update(backend="tiny_px", prism_x_install={k: pinfo[k] for k in ("params", "decoder_layers")},
                      prism_x=L.check_prism_x(m, be["dio"], be["model"]), path="eager (PRISM-X)")
    return be


class OracleDIO:
    """A decoder_io stand-in whose cand_logits plants answers from the synthetic gold (rows carry gold in the batch
    path). Everything else (to_probs, STYLE) is decoder_io's own."""

    def __init__(self, dio, acc_noul=0.95, acc_choice=0.80, seed=11):
        self._dio, self.acc, self.seed = dio, {"noul": acc_noul, "choice": acc_choice}, seed
        self.GRAPHS = None
        dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"

    def __getattr__(self, k):
        return getattr(self._dio, k)

    def cand_logits(self, model, ro, rows, dev, perms=None):
        import torch
        out = []
        for r, p in zip(rows, perms or [None] * len(rows)):
            if "gold" not in r or "id" not in r:
                raise RuntimeError("oracle backend: rows without gold/id (served requests) are not supported")
            u = int(hashlib.sha256(f"{self.seed}:{r['id']}".encode()).hexdigest(), 16) / 2 ** 256
            right = u < self.acc[r["qtype"]]
            rnd = random.Random(f"{self.seed}:{r['id']}:noise")
            if r["qtype"] == "noul":  # cygnet: displayed order [Yes, No] unless a perm says otherwise
                truth = r["gold"] if right else 1 - r["gold"]
                strength = rnd.uniform(0.5, 3.0)
                lg = [strength if truth == 1 else 0.0, 0.0 if truth == 1 else strength]
                if p is not None:
                    lg = [lg[i] for i in p]
            else:
                opts = r["options"] if p is None else [r["options"][i] for i in p]
                target = r["gold"] if right else rnd.choice([o for o in r["options"] if o != r["gold"]])
                lg = [(2.5 if o == target else 0.0) + (0.8 if i == 0 else 0.0) + rnd.uniform(0, 0.3)
                      for i, o in enumerate(opts)]
            out.append(torch.tensor(lg, dtype=torch.float32))
        return out


def load_oracle(m, root):
    L.require_synthetic(root)
    dio = OracleDIO(lean_dio())
    return {"dio": dio, "model": None, "ro": None, "dev": "cpu", "tok": None,
            "info": {"backend": "oracle", "note": "SYNTHETIC ONLY: logits planted from the synthetic gold"}}


def load_backend(kind, m, root, models_dir=None):
    if kind == "real":
        return load_real(m, models_dir or (L.LEAN / "models"))
    if kind == "tiny":
        L.require_synthetic(root) if root is not None else None
        return load_tiny(m)
    if kind == "tiny_px":
        L.require_synthetic(root) if root is not None else None
        return load_tiny_px(m)
    if kind == "oracle":
        return load_oracle(m, root)
    raise SystemExit(f"unknown backend {kind}")
