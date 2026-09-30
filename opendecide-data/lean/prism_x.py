"""PRISM-X: a trusted control plane added to a pretrained Qwen3.5 decision model (arms H, I, J of PRISM_X.md).

Everything here is ADDED next to the backbone; nothing of the backbone is taken over (test F took over 4 of 16 memory
heads and lost 5.9 pp). Every new part starts at zero, so at step 0 the model's candidate logits are exactly the arm-E
model's; a part only switches on if training finds it useful. train_decoder.py checks that equality before step 0.

Token roles (authority levels) come from the PRISM v2 prompt (decoder_io.LAYOUT = "schema_branch_mark"):
  SYS 0       system prompt and chat-template tokens before the user message                    trusted
  SCHEMA 1    rules, question, option definitions, before the text                              trusted
  DATA 2      the untrusted text, from the START marker to the END marker                       untrusted
  QUESTION 3  the note after the text, the repeated question, the answer slot                   trusted words, but
              computed after the text, so their hidden states already carry it
Trusted prefix = SYS + SCHEMA. By causality its hidden states cannot depend on any untrusted token.

Parts:
  H1  authority signal: a learned vector per (layer, role), added to the residual stream at the input of EVERY decoder
      layer, scaled by that token's hidden-state RMS (so one learning rate fits every layer). Zero-init table.
      ISE (arXiv:2410.09102) adds a role embedding once at the input; re-adding it at every layer is our extension,
      aimed at the "markers alone fade" result of PRISM arm C.
  H2  shadow memory: per Gated DeltaNet layer, S extra memory heads, copied from the layer's slowest-forgetting heads.
      They write only during the trusted prefix (write strength beta = 0 and log-decay g = 0 on every later token,
      the test-F mechanism), so the untrusted text can read them but can never write, overwrite or erase them. Their
      output is added to the layer output through a per-head gate tanh(gamma), gamma = 0 at init. All 16 original
      heads stay untouched. Only the gate is zero (the copies are not), so the gradient reaches the gate at step 0.
  I   option-query head: one trusted query per option = mean of the final hidden states over that option's line in
      the schema ("X. name: definition") and over the question (and, for yes/no rows, the definitions card). These
      positions come before the text, so the untrusted text cannot steer which evidence is looked for. Each query
      attends over the text tokens (plus a learned null slot) and a small scorer adds a score to that option's letter
      logit. The scorer's last layer is zero-init.
  J   latent decision loop: the per-option decision state z is refined T times (T = 1..loop_steps). Each step re-queries
      the text with a query built from the trusted query and z (input injection), compares options with a small
      self-attention across options, and makes a residual update. Training draws T per step (seeded by the step, so
      resume stays exact); inference uses T = loop_steps, or stops early per row once the margin of
      softmax(letter logits + score) reaches loop_exit_margin.

The module lives outside the model (module global PX), so PEFT never wraps or saves it; train_decoder saves it next to
the adapter as prism_x.json + prism_x.safetensors, and decoder_io.load() re-installs it when those files exist.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

SYS, SCHEMA, DATA, QUESTION = 0, 1, 2, 3
N_ROLES = 4
LAYOUT = "schema_branch_mark"  # the only prompt layout with a trusted schema, marked text and a trusted branch

DEFAULTS = {
    "authority": False,        # H1
    "shadow_heads": 0,         # H2: extra protected heads per Gated DeltaNet layer (0 = off)
    "shadow_pick": "slow",     # "slow": copy the heads with the slowest decay (they hold the most of the prefix); "first"
    "option_head": False,      # I
    "loop_steps": 0,           # J: max refinement steps (needs option_head)
    "loop_exit_margin": 0.0,   # J at inference: stop a row once top1 - top2 probability >= this (0 = always loop_steps)
    "temp_head": False,        # K: per-row confidence temperature tau = exp(0.75 tanh(w.f)), w = 0 at init (tau = 1)
    "loop_ensemble": False,    # K at inference: average the probabilities of loop steps 1..T (needs loop_steps)
    "counterfactual": False,   # L: also score the question with the text removed; subtract tanh(alpha) x that prior
    "policy_compiler": False,  # Omega-1: per layer, the trusted-schema summary emits FiLM (scale, shift) for text tokens
    "compiler_dim": 128,       # width of the compiled policy code
    "compiler_bound": 0.0,     # > 0: cap the FiLM scale and shift at +-bound via bound*tanh (O1 unbounded grew to |W| 13)
    "action_tower": False,     # Omega-4: CLM-style two-tower score <A q_i, B c> (trusted option vs decision state)
    "head_dim": 256,           # width of the option head
    "head_heads": 4,           # attention heads in the option head
    "lr_authority": 1e-3,      # absolute learning rates (the run's cosine schedule multiplies all of them)
    "lr_gate": 3e-3,
    "lr_shadow": 2e-5,         # full-rank copies of pretrained weights: a small rate, like full fine-tuning
    "lr_head": 3e-4,
    "lr_compiler": 3e-4,
}
PRESETS = {
    "H": {"authority": True, "shadow_heads": 2},
    "I": {"authority": True, "shadow_heads": 2, "option_head": True},
    "J": {"authority": True, "shadow_heads": 2, "option_head": True, "loop_steps": 4},
    "K": {"authority": True, "shadow_heads": 2, "option_head": True, "loop_steps": 4, "temp_head": True,
          "loop_ensemble": True},
    "L": {"authority": True, "shadow_heads": 2, "option_head": True, "counterfactual": True},  # I + counterfactual
    "O1": {"authority": True, "shadow_heads": 2, "option_head": True, "policy_compiler": True},  # I + compiler
    "O4": {"authority": True, "shadow_heads": 2, "option_head": True, "action_tower": True},     # I + action tower
    "O1b": {"authority": True, "shadow_heads": 2, "option_head": True, "policy_compiler": True,  # I + capped compiler
            "compiler_bound": 0.1, "lr_compiler": 1e-4},
}

PX = None  # the installed PrismX (one model at a time)
STATE = {"enabled": True, "train_T": None, "fired_auth": 0, "fired_shadow": 0, "fired_head": 0, "last_T": None,
         "restore_layout": None}  # (LAYOUT, STYLE) to put back when a loaded PRISM-X model is uninstalled
CTX = {"roles": None, "blocked": None, "head": None}
_HANDLES = []


def resolve(spec):
    """cfg value -> full config dict, or None. Accepts None/False, a preset name ("H", "I", "J"), or a dict that may name
    a "preset" and override any key."""
    if not spec:
        return None
    if isinstance(spec, str):
        spec = {"preset": spec}
    spec = dict(spec)
    preset = spec.pop("preset", None)
    if preset is not None and preset not in PRESETS:
        raise ValueError(f"prism_x: unknown preset {preset!r} (known: {sorted(PRESETS)})")
    unknown = set(spec) - set(DEFAULTS)
    if unknown:
        raise ValueError(f"prism_x: unknown keys {sorted(unknown)}")
    cfg = {**DEFAULTS, **PRESETS.get(preset, {}), **spec}
    if cfg["loop_steps"] and not cfg["option_head"]:
        raise ValueError("prism_x: loop_steps (J) needs option_head (I)")
    if cfg["temp_head"] and not cfg["option_head"]:
        raise ValueError("prism_x: temp_head (K) needs option_head (I)")
    if cfg["loop_ensemble"] and not cfg["loop_steps"]:
        raise ValueError("prism_x: loop_ensemble (K) needs loop_steps (J)")
    if cfg["head_dim"] % cfg["head_heads"]:
        raise ValueError("prism_x: head_dim must be divisible by head_heads")
    if cfg["action_tower"] and not cfg["option_head"]:
        raise ValueError("prism_x: action_tower (Omega-4) needs option_head (I)")
    if not (cfg["authority"] or cfg["shadow_heads"] or cfg["option_head"] or cfg["counterfactual"] or cfg["policy_compiler"]):
        raise ValueError("prism_x: no part is switched on")
    return cfg


def active_for(body) -> bool:
    return PX is not None and STATE["enabled"] and PX.owner is body


def _on() -> bool:
    return PX is not None and STATE["enabled"]


def _w(mod):
    """Effective weight of a Linear: through a PEFT LoRA wrapper, base weight + the active adapters' deltas (so a run
    that starts from a trained adapter copies the heads it actually has, not the pre-LoRA ones)."""
    if not hasattr(mod, "get_base_layer"):
        return mod.weight
    w = mod.get_base_layer().weight
    if not getattr(mod, "merged", False) and not getattr(mod, "disable_adapters", False):
        for a in getattr(mod, "active_adapters", []) or []:
            if a in getattr(mod, "lora_A", {}):
                w = w + mod.get_delta_weight(a).to(w.dtype)
    return w


def _text_config(model):
    base = model.get_base_model() if hasattr(model, "get_base_model") else model
    cfg = base.config
    return getattr(cfg, "text_config", None) or cfg


def _layers(model):
    dec = [m for m in model.modules() if type(m).__name__.endswith("DecoderLayer")]
    gdn = [m for m in model.modules() if type(m).__name__.endswith("GatedDeltaNet")]
    return dec, gdn


# ---------------------------------------------------------------- H2: shadow memory

def _gated_rmsnorm(h, gate, weight, eps):
    """Exactly Qwen3_5RMSNormGated.forward (norm, weight, then * silu(gate) in fp32)."""
    dt = h.dtype
    hf = h.float()
    hf = hf * torch.rsqrt(hf.pow(2).mean(-1, keepdim=True) + eps)
    hf = weight.to(dt) * hf.to(dt)
    hf = hf * F.silu(gate.float())
    return hf.to(dt)


class ShadowHeads(nn.Module):
    """S write-protected copies of one Gated DeltaNet layer's value heads (with their key/query heads, conv channels,
    decay, write strength, output gate and output columns). Weights are fp32 masters, cast to the input dtype."""

    def __init__(self, la, S, pick="slow", idx=None):
        super().__init__()
        Hv, Hk, dk, dv = la.num_v_heads, la.num_k_heads, la.head_k_dim, la.head_v_dim
        rep = Hv // Hk
        if idx is None:
            with torch.no_grad():  # decay speed at a = 0 is exp(A_log) * softplus(dt_bias); small = long memory
                rate = la.A_log.detach().float().exp() * F.softplus(la.dt_bias.detach().float())
                idx = torch.argsort(rate)[:S] if pick == "slow" else torch.arange(S)
            idx = sorted(int(i) for i in idx)
        assert len(idx) == S and max(idx) < Hv, (idx, S, Hv)
        self.idx, self.S, self.dk, self.dv = list(idx), S, dk, dv
        self.act, self.eps = la.activation, la.layer_norm_epsilon
        key_dim = la.key_dim
        kh = [j // rep for j in idx]
        q_rows = torch.cat([torch.arange(h * dk, (h + 1) * dk) for h in kh])
        v_rows = torch.cat([torch.arange(j * dv, (j + 1) * dv) for j in idx])
        rows = torch.cat([q_rows, key_dim + q_rows, 2 * key_dim + v_rows])
        assert la.conv1d.bias is None, "shadow memory assumes a bias-free conv1d (Qwen3.5)"
        cp = lambda t: nn.Parameter(t.detach().float().clone())
        self.w_qkv = cp(_w(la.in_proj_qkv)[rows])
        self.conv_w = cp(la.conv1d.weight[rows, 0, :])
        self.w_z = cp(_w(la.in_proj_z)[v_rows])
        self.w_b = cp(_w(la.in_proj_b)[idx])
        self.w_a = cp(_w(la.in_proj_a)[idx])
        self.A_log = cp(la.A_log[idx])
        self.dt_bias = cp(la.dt_bias[idx])
        self.norm_w = cp(la.norm.weight)
        self.w_out = cp(_w(la.out_proj)[:, v_rows])
        self.gate = nn.Parameter(torch.zeros(S))  # tanh(0) = 0: the layer output is unchanged at init

    def forward(self, x, attention_mask, blocked, mod):
        x = mod.apply_mask_to_padding_states(x, attention_mask)
        B, T, _ = x.shape
        dt, S, dk, dv = x.dtype, self.S, self.dk, self.dv
        qkv = F.linear(x, self.w_qkv.to(dt)).transpose(1, 2).contiguous()
        qkv = mod.causal_conv1d_fn(qkv, self.conv_w.to(dt), None, activation=self.act).transpose(1, 2)
        q, k, v = torch.split(qkv, [S * dk, S * dk, S * dv], dim=-1)
        q, k, v = q.reshape(B, T, S, dk), k.reshape(B, T, S, dk), v.reshape(B, T, S, dv)
        beta = F.linear(x, self.w_b.to(dt)).sigmoid()
        g = -self.A_log.float().exp() * F.softplus(F.linear(x, self.w_a.to(dt)).float() + self.dt_bias.float())
        blk = blocked[:, :, None]
        beta = beta.masked_fill(blk, 0.0)  # no write after the trusted prefix
        g = g.masked_fill(blk, 0.0)        # no decay/erase after the trusted prefix (exp(0) = 1 keeps the state)
        core, _ = mod.torch_chunk_gated_delta_rule(q, k, v, g=g, beta=beta, initial_state=None,
                                                   output_final_state=False, use_qk_l2norm_in_kernel=True)
        z = F.linear(x, self.w_z.to(dt))
        core = _gated_rmsnorm(core.reshape(-1, dv), z.reshape(-1, dv), self.norm_w, self.eps).reshape(B, T, S, dv)
        core = core * torch.tanh(self.gate).to(dt)[None, None, :, None]
        return F.linear(core.reshape(B, T, S * dv), self.w_out.to(dt))


# ---------------------------------------------------------------- I + J: option-query head and latent loop

class OptionHead(nn.Module):
    def __init__(self, d, r=256, nh=4, loop=0, temp=False, action=False):
        super().__init__()
        self.r, self.nh, self.loop, self.temp, self.action = r, nh, loop, temp, action
        self.ln_q = nn.LayerNorm(2 * d)
        self.q = nn.Linear(2 * d, r)
        self.k = nn.Linear(d, r, bias=False)
        self.v = nn.Linear(d, r, bias=False)
        self.null_k = nn.Parameter(torch.zeros(r))  # always-attendable slot: a row with no text tokens stays finite
        self.null_v = nn.Parameter(torch.zeros(r))
        self.c = nn.Linear(d, r)  # the answer-slot state (it has read everything, trusted and untrusted)
        self.inp = nn.Linear(4 * r, r)
        self.ln_s = nn.LayerNorm(r)
        self.s1 = nn.Linear(r, r)
        self.s2 = nn.Linear(r, 1)
        nn.init.zeros_(self.s2.weight)  # score = 0 at init: letter logits unchanged
        nn.init.zeros_(self.s2.bias)
        if loop:
            self.step = nn.Embedding(loop + 1, r)
            nn.init.normal_(self.step.weight, std=0.02)
            self.ln_a = nn.LayerNorm(r)
            self.qz = nn.Linear(r, r)
            self.mix = nn.MultiheadAttention(r, nh, batch_first=True)
            self.u1 = nn.Linear(3 * r, 2 * r)
            self.u2 = nn.Linear(2 * r, r)
            nn.init.normal_(self.u2.weight, std=1e-3)  # small, not zero: no double-zero dead start
            nn.init.zeros_(self.u2.bias)
        if action:  # Omega-4: two-tower match of the trusted option query and the decision state; A = 0 at init
            self.at_a = nn.Linear(r, r, bias=False)
            self.at_b = nn.Linear(r, r, bias=False)
            nn.init.zeros_(self.at_a.weight)
        if temp:  # K: confidence temperature from the decision states and the answer slot; 0 -> tau = exp(0) = 1
            self.tq = nn.Linear(2 * r, 1)
            nn.init.zeros_(self.tq.weight)
            nn.init.zeros_(self.tq.bias)

    def _xattn(self, q, K, V, dmask):
        """q [B,N,r] attends over the text tokens (K, V [B,T,r], dmask [B,T] True = text token) plus the null slot."""
        B, N, r = q.shape
        h, dh = self.nh, r // self.nh
        Kf = torch.cat([self.null_k.expand(B, 1, r), K], 1).view(B, -1, h, dh).transpose(1, 2)
        Vf = torch.cat([self.null_v.expand(B, 1, r), V], 1).view(B, -1, h, dh).transpose(1, 2)
        m = torch.cat([torch.ones(B, 1, dtype=torch.bool, device=q.device), dmask], 1)[:, None, None, :]
        e = F.scaled_dot_product_attention(q.view(B, N, h, dh).transpose(1, 2), Kf, Vf, attn_mask=m)
        return e.transpose(1, 2).reshape(B, N, r)

    def _score(self, z):
        return self.s2(F.gelu(self.s1(self.ln_s(z)))).squeeze(-1)

    def forward(self, hs, ctx, base, T, exit_margin=0.0):
        """hs [B,L,d] final hidden states; base [B,N] letter logits (padded options = -inf).
        Returns (scores [B,N] to add, tau [B] or None, per-step scores [T+1 x [B,N]])."""
        with torch.autocast(device_type=hs.device.type, enabled=False):
            Ts = ctx["schema_len"]
            hq = hs[:, :Ts].float()
            opt = torch.bmm(ctx["pool_opt"], hq)                                  # [B,N,d] mean over each option line
            ins = torch.bmm(ctx["pool_ins"], hq)                                  # [B,1,d] mean over question (+card)
            N = opt.shape[1]
            q = self.q(self.ln_q(torch.cat([opt, ins.expand(-1, N, -1)], -1)))   # trusted-only query per option
            K = F.linear(hs, self.k.weight.to(hs.dtype)).float()
            V = F.linear(hs, self.v.weight.to(hs.dtype)).float()
            c = self.c(hs[torch.arange(hs.shape[0], device=hs.device), ctx["last"]].float())[:, None, :].expand(-1, N, -1)
            e = self._xattn(q, K, V, ctx["dmask"])
            z = F.gelu(self.inp(torch.cat([q, e, q * e, c], -1)))
            scores = [self._score(z)]
            for t in range(1, T + 1):
                zn = self.ln_a(z)
                et = self._xattn(q + self.qz(zn) + self.step.weight[t], K, V, ctx["dmask"])
                m, _ = self.mix(zn, zn, zn, key_padding_mask=ctx["opt_pad"], need_weights=False)
                z = z + self.u2(F.gelu(self.u1(torch.cat([zn, et, m], -1))))
                scores.append(self._score(z))
            if self.action:
                tower = (self.at_a(q) * self.at_b(c)).sum(-1) / math.sqrt(self.r)
                scores = [x + tower for x in scores]
            tau = None
            if self.temp:
                real = (~ctx["opt_pad"]).float()[..., None]
                zbar = (z * real).sum(1) / real.sum(1).clamp_min(1.0)
                tau = torch.exp(0.75 * torch.tanh(self.tq(torch.cat([zbar, c[:, 0]], -1)).squeeze(-1)))
            if self.training or exit_margin <= 0 or T == 0:
                STATE["last_T"] = T
                return scores[-1], tau, scores
            # adaptive exit: per row, the first step whose decision margin reaches exit_margin (else the last step)
            S = torch.stack(scores[1:], 0)                                        # [T,B,N]
            p = torch.softmax(base.float()[None] + S, -1).topk(min(2, N), -1).values
            margin = p[..., 0] - (p[..., 1] if N > 1 else 0)
            ok = margin >= exit_margin
            first = torch.where(ok.any(0), ok.float().argmax(0), torch.full_like(ok[0], T - 1, dtype=torch.long))
            STATE["last_T"] = (first + 1).tolist()
            return S[first, torch.arange(S.shape[1], device=S.device)], tau, scores


# ---------------------------------------------------------------- the control plane

class PrismX(nn.Module):
    def __init__(self, cfg, d, n_layers, gdn, shadow_idx=None):
        super().__init__()
        self.cfg, self.d, self.n_layers = cfg, d, n_layers
        self.authority = nn.Parameter(torch.zeros(n_layers, N_ROLES, d)) if cfg["authority"] else None
        S = int(cfg["shadow_heads"] or 0)
        self.shadows = nn.ModuleList([ShadowHeads(la, S, cfg["shadow_pick"], None if shadow_idx is None else shadow_idx[i])
                                      for i, la in enumerate(gdn)]) if S else None
        self.head = OptionHead(d, cfg["head_dim"], cfg["head_heads"], int(cfg["loop_steps"] or 0),
                               bool(cfg["temp_head"]), bool(cfg.get("action_tower"))) if cfg["option_head"] else None
        if cfg.get("policy_compiler"):  # Omega-1: shared encoder of the trusted summary, per-layer zero-init FiLM maps
            r = int(cfg["compiler_dim"])
            self.comp_ln = nn.LayerNorm(d)
            self.comp_down = nn.Linear(d, r)
            self.comp_layer = nn.Parameter(torch.zeros(n_layers, r))
            self.comp_up = nn.Parameter(torch.zeros(n_layers, r, 2 * d))
        else:
            self.comp_up = None
        # L: per question type (yes/no, choice) strength of the no-evidence prior subtraction; tanh(0) = 0 at init
        self.cf_alpha = nn.Parameter(torch.zeros(2)) if cfg.get("counterfactual") else None
        object.__setattr__(self, "owner", None)  # plain attribute: never register the backbone as a submodule

    def meta(self):
        return {"version": 1, "cfg": self.cfg, "d": self.d, "n_layers": self.n_layers,
                "shadow_idx": [s.idx for s in self.shadows] if self.shadows is not None else None}


def _auth_hook(i):
    def pre(module, args, kwargs):
        if not _on() or PX.authority is None:
            return None
        h = args[0] if args else kwargs["hidden_states"]
        roles = CTX["roles"]
        if roles is None or tuple(roles.shape) != tuple(h.shape[:2]):
            raise RuntimeError(f"PRISM-X: token roles {None if roles is None else tuple(roles.shape)} do not match "
                               f"hidden states {tuple(h.shape[:2])}; call cand_logits (it builds them)")
        rms = h.detach().float().pow(2).mean(-1, keepdim=True).sqrt()
        h = h + (PX.authority[i][roles] * rms).to(h.dtype)
        STATE["fired_auth"] += 1
        if args:
            return (h,) + tuple(args[1:]), kwargs
        kwargs["hidden_states"] = h
        return args, kwargs
    return pre


def _compile_delta(i, h):
    """Omega-1 policy compilation at decoder layer i. The trusted-schema summary s (mean of this layer's hidden states
    over SCHEMA tokens: by causality it cannot depend on the untrusted text) is compiled into a scale g and a shift b,
    applied only to tokens after the trusted prefix: h + (h * g + b * RMS(h)). comp_up = 0 at init, so the delta is 0."""
    w = CTX["schema_w"]
    s = torch.einsum("bt,btd->bd", w, h.float())
    code = F.gelu(PX.comp_down(PX.comp_ln(s)) + PX.comp_layer[i])
    g, b = (code @ PX.comp_up[i]).chunk(2, -1)
    bound = float(PX.cfg.get("compiler_bound") or 0.0)
    if bound > 0:  # O1b: the compiled policy may only nudge the text's states (tanh(0) = 0 keeps the zero init)
        g, b = bound * torch.tanh(g), bound * torch.tanh(b)
    m = CTX["blocked"][..., None].to(torch.float32)
    rms = h.detach().float().pow(2).mean(-1, keepdim=True).sqrt()
    return ((h.float() * g[:, None, :] + b[:, None, :] * rms) * m).to(h.dtype)


def _compile_hook(i):
    def pre(module, args, kwargs):
        if not _on() or PX.comp_up is None:
            return None
        h = args[0] if args else kwargs["hidden_states"]
        if CTX.get("schema_w") is None or tuple(CTX["schema_w"].shape) != tuple(h.shape[:2]):
            raise RuntimeError("PRISM-X: trusted-schema weights missing or wrong shape")
        with torch.autocast(device_type=h.device.type, enabled=False):
            h = h + _compile_delta(i, h)
        STATE["fired_comp"] = STATE.get("fired_comp", 0) + 1
        if args:
            return (h,) + tuple(args[1:]), kwargs
        kwargs["hidden_states"] = h
        return args, kwargs
    return pre


def _shadow_hook(i):
    def post(module, args, kwargs, output):
        if not _on() or PX.shadows is None:
            return None
        x = kwargs["hidden_states"] if "hidden_states" in kwargs else args[0]
        if x.shape[1] == 1 and kwargs.get("cache_params") is not None:
            raise RuntimeError("PRISM-X shadow memory does not support cached one-token decoding")
        blocked = CTX["blocked"]
        if blocked is None or tuple(blocked.shape) != tuple(x.shape[:2]):
            raise RuntimeError("PRISM-X: write-block mask missing or wrong shape")
        STATE["fired_shadow"] += 1
        return output + PX.shadows[i](x, kwargs.get("attention_mask"), blocked, sys.modules[type(module).__module__])
    return post


def install(model, cfg, dev, shadow_idx=None):
    """Attach PRISM-X to `model` (a PEFT model or a plain/merged HF model). Call AFTER get_peft_model, so PEFT never
    wraps the new weights. Returns a summary dict."""
    global PX
    _remove()
    import decoder_io
    if decoder_io.WRITEBLOCK:
        raise RuntimeError("PRISM-X and the test-F write-block patch cannot run together")
    tc = _text_config(model)
    dec, gdn = _layers(model)
    if len(dec) != tc.num_hidden_layers:
        raise RuntimeError(f"PRISM-X: found {len(dec)} decoder layers, config says {tc.num_hidden_layers}")
    if cfg["shadow_heads"] and not gdn:
        raise RuntimeError("PRISM-X shadow memory needs Gated DeltaNet layers (Qwen3.5)")
    PX = PrismX(cfg, tc.hidden_size, len(dec), gdn, shadow_idx).to(dev)
    object.__setattr__(PX, "owner", decoder_io._parts(model)[0])  # the body cand_logits runs (identity check)
    if cfg["authority"]:
        for i, layer in enumerate(dec):
            _HANDLES.append(layer.register_forward_pre_hook(_auth_hook(i), with_kwargs=True))
    if cfg.get("policy_compiler"):  # registered after the authority hook, so it sees the authority-tagged states
        for i, layer in enumerate(dec):
            _HANDLES.append(layer.register_forward_pre_hook(_compile_hook(i), with_kwargs=True))
    if cfg["shadow_heads"]:
        for i, la in enumerate(gdn):
            _HANDLES.append(la.register_forward_hook(_shadow_hook(i), with_kwargs=True))
    STATE.update(enabled=True, train_T=None, last_T=None)
    n = sum(p.numel() for p in PX.parameters())
    return {"cfg": cfg, "params": n, "decoder_layers": len(dec), "deltanet_layers": len(gdn),
            "shadow_idx_first_layers": [s.idx for s in PX.shadows][:3] if PX.shadows is not None else None}


def _remove():
    global PX
    for h in _HANDLES:
        h.remove()
    _HANDLES.clear()
    PX = None
    CTX.update(roles=None, blocked=None, head=None)


def uninstall():
    """Removes the control plane and, if maybe_load changed the prompt layout, puts the previous one back."""
    _remove()
    if STATE["restore_layout"] is not None:
        import decoder_io
        decoder_io.LAYOUT, decoder_io.STYLE = STATE["restore_layout"]
        STATE["restore_layout"] = None


def param_groups():
    """Optimizer groups with their own absolute learning rates (the run's schedule multiplies each)."""
    if PX is None:
        return []
    c, groups = PX.cfg, []
    if PX.authority is not None:
        groups.append({"name": "px_authority", "params": [PX.authority], "lr": c["lr_authority"]})
    if PX.shadows is not None:
        groups.append({"name": "px_gate", "params": [s.gate for s in PX.shadows], "lr": c["lr_gate"]})
        groups.append({"name": "px_shadow", "params": [p for s in PX.shadows for n, p in s.named_parameters() if n != "gate"],
                       "lr": c["lr_shadow"]})
    if PX.head is not None:
        groups.append({"name": "px_head", "params": list(PX.head.parameters()), "lr": c["lr_head"]})
    if PX.cf_alpha is not None:
        groups.append({"name": "px_cf", "params": [PX.cf_alpha], "lr": c["lr_gate"]})
    if PX.comp_up is not None:
        groups.append({"name": "px_compiler", "params": [PX.comp_up, PX.comp_layer] + list(PX.comp_ln.parameters())
                       + list(PX.comp_down.parameters()), "lr": c["lr_compiler"]})
    return groups


def stats():
    """Small numbers for the training log: are the new parts switching on?"""
    if PX is None:
        return None
    out = {}
    with torch.no_grad():
        if PX.authority is not None:
            out["auth_rms"] = round(float(PX.authority.pow(2).mean().sqrt()), 5)
        if PX.shadows is not None:
            g = torch.stack([torch.tanh(s.gate) for s in PX.shadows]).abs()
            out["gate_mean"], out["gate_max"] = round(float(g.mean()), 4), round(float(g.max()), 4)
        if PX.comp_up is not None:
            out["comp_w"] = round(float(PX.comp_up.norm()), 5)
        if PX.cf_alpha is not None:
            out["cf_alpha"] = [round(float(x), 4) for x in torch.tanh(PX.cf_alpha)]
        if PX.head is not None:
            out["head_w"] = round(float(PX.head.s2.weight.norm()), 5)
            if PX.head.temp:
                out["tau_w"], out["tau_last"] = round(float(PX.head.tq.weight.norm()), 5), STATE.get("last_tau")
    return out


# ---------------------------------------------------------------- per-batch context (roles, spans)

def row_char_spans(row, perm, text):
    """Character spans inside the chat text: {"base", "data": (s, e), "opt": [(s, e) per displayed option],
    "ins": [(s, e), ...]} (ins = question in the schema, plus the definitions card on yes/no rows)."""
    import decoder_io
    r = decoder_io.as_letter_row(row)
    parts = decoder_io.cygnet_parts(r, perm)
    msg = "\n".join(s for _, s in parts)
    if msg != decoder_io.cygnet_msg(r, perm):
        raise RuntimeError(f"PRISM-X: cygnet_parts disagrees with cygnet_msg on row {row.get('id')}")
    base = text.find(msg)
    if base < 0:
        raise RuntimeError(f"PRISM-X: user message not found verbatim in the chat text (row {row.get('id')}); "
                           "rows with a caller-built _prompt are not supported")
    sp, pos = {"base": base, "opt": [], "ins": []}, base
    for tag, s in parts:
        if tag == "data":
            sp["data"] = (pos, pos + len(s))
        elif tag in ("opt", "ins"):
            sp[tag].append((pos, pos + len(s)))
        pos += len(s) + 1
    n = len(r["options"])
    if len(sp["opt"]) != n or "data" not in sp:
        raise RuntimeError(f"PRISM-X: found {len(sp['opt'])} option lines for {n} options (row {row.get('id')})")
    return sp


def prepare(rows, perms, texts, offsets, attn_mask, dev):
    """Builds token roles, the write-block mask and the option-head pooling for one cand_logits batch; sets CTX."""
    import decoder_io
    if decoder_io.LAYOUT != LAYOUT or decoder_io.STYLE != "cygnet":
        raise RuntimeError(f"PRISM-X needs STYLE='cygnet' and LAYOUT='{LAYOUT}' (got {decoder_io.STYLE!r}, {decoder_io.LAYOUT!r})")
    B, L = attn_mask.shape
    real = attn_mask.bool()
    st, en = offsets[..., 0], offsets[..., 1]
    roles = torch.full((B, L), QUESTION, dtype=torch.long)
    spans = [row_char_spans(r, p, t) for r, p, t in zip(rows, perms, texts)]
    for i, sp in enumerate(spans):
        s = st[i]
        ri = torch.where(s < sp["base"], SYS, torch.where(s < sp["data"][0], SCHEMA,
                         torch.where(s < sp["data"][1], DATA, QUESTION)))
        ri = torch.where(real[i], ri, torch.full_like(ri, QUESTION))
        # Roles never go back down along the sequence. This also places any token whose offset is (0, 0) (e.g. a chat
        # special token typed inside the untrusted text) by its position, so the text can never mint a trusted token.
        roles[i] = torch.cummax(ri, 0).values
    blocked = roles >= DATA  # everything from the first text token on (text, question branch, answer slot, pads)
    CTX["roles"], CTX["blocked"] = roles.to(dev), blocked.to(dev)
    sch = ((roles == SCHEMA) & real).float()  # Omega-1: weights of the trusted-schema summary (mean over SCHEMA)
    CTX["schema_w"] = (sch / sch.sum(1, keepdim=True).clamp_min(1.0)).to(dev)
    CTX["head"] = None
    if PX is not None and PX.head is not None:
        N = max(len(sp["opt"]) for sp in spans)
        overlap = lambda i, a, b: real[i] & (st[i] < b) & (en[i] > a) & (en[i] > st[i])
        schema_len = 1
        pool_opt = torch.zeros(B, N, L)
        pool_ins = torch.zeros(B, 1, L)
        opt_pad = torch.ones(B, N, dtype=torch.bool)
        for i, sp in enumerate(spans):
            for j, (a, b) in enumerate(sp["opt"]):
                m = overlap(i, a, b)
                if not bool(m.any()):
                    raise RuntimeError(f"PRISM-X: option {j} of row {rows[i].get('id')} has no tokens")
                pool_opt[i, j, m] = 1.0 / float(m.sum())
                opt_pad[i, j] = False
            mi = torch.zeros(L, dtype=torch.bool)
            for a, b in sp["ins"]:
                mi |= overlap(i, a, b)
            if bool(mi.any()):
                pool_ins[i, 0, mi] = 1.0 / float(mi.sum())
            used = torch.nonzero(pool_opt[i].sum(0) + pool_ins[i, 0] > 0)
            schema_len = max(schema_len, int(used.max()) + 1)
        CTX["head"] = {"pool_opt": pool_opt[:, :, :schema_len].to(dev), "pool_ins": pool_ins[:, :, :schema_len].to(dev),
                       "schema_len": schema_len, "opt_pad": opt_pad.to(dev), "n": [len(sp["opt"]) for sp in spans],
                       "dmask": ((roles == DATA) & real).to(dev), "last": (attn_mask.sum(1) - 1).to(dev)}
    STATE["fired_auth"] = STATE["fired_shadow"] = STATE["fired_comp"] = 0


def apply_head(hs, logits):
    """Adds the option-head scores to each row's letter logits (list of 1-D tensors, displayed order)."""
    if PX is None or PX.head is None or not STATE["enabled"]:
        return logits
    ctx = CTX["head"]
    B, N = len(logits), ctx["pool_opt"].shape[1]
    base = torch.full((B, N), float("-inf"), device=hs.device)
    for i, l in enumerate(logits):
        if len(l) != ctx["n"][i]:
            raise RuntimeError(f"PRISM-X: row {i} has {len(l)} letter logits but {ctx['n'][i]} option lines")
        base[i, :len(l)] = l.detach().float()
    L = int(PX.cfg["loop_steps"] or 0)
    training = PX.owner.training  # follows model.train() / model.eval() (PX is not a submodule of the model)
    PX.train(training)
    T = (STATE["train_T"] or L) if training else L
    s, tau, steps = PX.head(hs, ctx, base, T, 0.0 if training else float(PX.cfg["loop_exit_margin"] or 0.0))
    STATE["fired_head"] += 1
    STATE["last_tau"] = None if tau is None else round(float(tau.detach().mean()), 4)
    ens = (not training) and bool(PX.cfg.get("loop_ensemble")) and T >= 1
    out = []
    for i, l in enumerate(logits):
        n, ti = len(l), (1.0 if tau is None else tau[i])
        if ens:  # K: average the probabilities of every loop step (a small ensemble of decision states)
            P = torch.stack([torch.softmax((l.float() + st[i, :n]) / ti, -1) for st in steps[1:]]).mean(0)
            out.append(torch.log(P.clamp_min(1e-30)))
        else:
            out.append((l.float() + s[i, :n]) / ti)
    return out


def check_fired(n_forwards=1):
    """After one training forward: every hook must have fired once per layer."""
    if PX is None:
        return
    if PX.authority is not None and STATE["fired_auth"] < PX.n_layers * n_forwards:
        raise RuntimeError(f"PRISM-X authority hook fired {STATE['fired_auth']} times, expected {PX.n_layers}")
    if PX.comp_up is not None and STATE.get("fired_comp", 0) < PX.n_layers * n_forwards:
        raise RuntimeError(f"PRISM-X compiler hook fired {STATE.get('fired_comp')} times, expected {PX.n_layers}")
    if PX.shadows is not None and STATE["fired_shadow"] < len(PX.shadows) * n_forwards:
        raise RuntimeError(f"PRISM-X shadow hook fired {STATE['fired_shadow']} times, expected {len(PX.shadows)}")


# ---------------------------------------------------------------- save / load

def save(out_dir):
    if PX is None:
        return
    from safetensors.torch import save_file
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    import decoder_io
    (out_dir / "prism_x.json").write_text(json.dumps({**PX.meta(), "layout": decoder_io.LAYOUT, "style": decoder_io.STYLE}, indent=2))
    save_file({k: v.detach().float().contiguous().cpu() for k, v in PX.state_dict().items()}, str(out_dir / "prism_x.safetensors"))


def load_weights(src_dir):
    from safetensors.torch import load_file
    sd = load_file(str(Path(src_dir) / "prism_x.safetensors"))
    missing, unexpected = PX.load_state_dict(sd, strict=False)
    if missing or unexpected:
        raise RuntimeError(f"PRISM-X weights do not match: missing {missing[:5]}, unexpected {unexpected[:5]}")


def maybe_load(model, adapter_dir, dev):
    """Re-installs PRISM-X from an adapter directory that has prism_x.json (else leaves the model alone)."""
    p = Path(adapter_dir) / "prism_x.json"
    if not p.exists():
        return None
    meta = json.loads(p.read_text())
    import decoder_io
    uninstall()
    STATE["restore_layout"] = (decoder_io.LAYOUT, decoder_io.STYLE)
    decoder_io.LAYOUT, decoder_io.STYLE = meta["layout"], meta["style"]
    info = install(model, resolve(meta["cfg"]), dev, shadow_idx=meta.get("shadow_idx"))
    load_weights(adapter_dir)
    PX.eval()
    return info


# ---------------------------------------------------------------- L: counterfactual evidence

def null_rows(rows):
    """The same questions with the untrusted text removed (the markers stay, empty): what the model would answer on
    the rules and question alone. Used as a per-question prior."""
    return [{**r, "state": ""} for r in rows]


def counterfactual(logits, rows, null_logits):
    """logits - tanh(alpha[qtype]) * log_softmax(null logits). The null pass runs without gradient, so only alpha
    learns from it (no co-adaptation of the two passes). alpha = 0 at init: logits unchanged."""
    if PX is None or PX.cf_alpha is None or null_logits is None:
        return logits
    a = torch.tanh(PX.cf_alpha)
    return [l - a[0 if r["qtype"] == "noul" else 1] * torch.log_softmax(n.detach().float(), -1)
            for l, r, n in zip(logits, rows, null_logits)]
