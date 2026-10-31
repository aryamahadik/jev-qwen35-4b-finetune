"""grid_h100.common: constants, payer guard (owner-named profile only), money ledger (hard cap USD 15.00, PREREG A88), path guard, hashing.

Standard library only (imported on the laptop, in the Modal function process and in the reader process).

HARD RULES encoded here
  * Payer: a Modal profile is accepted ONLY if the owner named it at GO #1 in OWNER_GO1_PAYER.json (next to this file) and
    MODAL_PROFILE is exported with exactly that name. No file, an unreadable file, a profile that is not named: refuse.
    There is no default and no allow-list of accounts in code (the owner names it); MODAL_TOKEN_* overrides, `modal deploy` /
    `serve` / `shell`, --detach are refused (Ctrl-C on the laptop must stop the GPU).
  * Money: hard cap USD 15.00 (PREREG Record A88: "hard cap $15 for these post-training lines", the grid reads AND the GO #2 reads;
    never the personal card) for every call of this tool together (grid session(s) + the parity job): a launch is refused when
    spent + the call's estimate would pass USD 13.50 (stop-launch), the laptop cancels the GPU call at USD 14.60 (estimate), and the
    function timeout is set so that even a runaway container cannot cross USD 15.00. The cap can be LOWERED in the GO file, never
    raised from there (raising it is an edit of CAP_USD here, a new sha in A64_TOOLS.md and a new owner ruling). It was USD 4.00 /
    3.60 / 3.90 until the A88 edit of 18 Oct 2026. The GO #2 reads are not made by this tool: whatever they cost is added with
    Budget.add_extra so the one USD 15.00 ledger stays whole.
  * C2 training guard: the profiles named in PAYER_POLICY.json "c2_training_relay" are refused as payer until C2 TRAINING IS OVER
    (the final relay record exists) AND no segment of c2_segments.jsonl is still open on that profile; the profiles named in
    "never_payers" are refused always. Policy file missing / unreadable = refuse (fail closed). Account names live in
    PAYER_POLICY.json and OWNER_GO1_PAYER.json, never in this code.
  * Data: dev data only. safe_path() refuses any path that contains "ohs" (any case), "sealed", "c_spec/sealed_brief",
    "c_build/preread", "bench/external_quarantine", "bench/longbench_v2", "jev" outputs or ".claude"; split / model names that
    hold ohs / sealed / jev are refused too.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path


def _lean_root() -> Path:
    for c in (os.environ.get("OD_LEAN"), "/root/lean"):
        if c and (Path(c) / "decoder_io.py").exists():
            return Path(c)
    return Path(__file__).resolve().parents[3]          # lean/c2_build/train/grid_h100 -> lean


HERE = Path(__file__).resolve().parent
LEAN = _lean_root()
GO_FILE = HERE / "OWNER_GO1_PAYER.json"
POLICY_FILE = HERE / "PAYER_POLICY.json"
C2_SEGMENTS = LEAN / "c2_build" / "train" / "logs" / "c2_segments.jsonl"      # written by c2_chain.sh (read only here)
C2_FINAL = LEAN / "logs" / "relay_q35_4b_c2_final.json"                       # c2_chain.sh FINAL=logs/relay_${NAME}_final.json
LEDGER = HERE / "ledger.json"
RESULTS = HERE / "results"

# ------------------------------------------------------------------ identities (a test keeps them equal to the originals)
APP_NAME = "c2-grid-h100"
SRC_VOLUME = "opendecide"                    # the payer's account Volume: C2 run folder, C1 adapter, HF cache (mounted READ-ONLY)
OUT_VOLUME = "c2-grid-h100-reads"            # results (created if missing; the only thing this tool writes on Modal)
BASE = "Qwen/Qwen3.5-4B"
REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
C1_NAME = "q35_4b_main500k"
C1_ADAPTER_SHA256 = "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"
RUN_NAME, REF_NAME = "q35_4b_c2", "q35_4b_main500k_c2"
READ_TPL = "q35_4b_c2grid_{cand}"
SGLANG_IMAGE = "lmsysorg/sglang:v0.5.20-cu130"
SGLANG_VERSION = "0.5.20"
UV_PIN = "uv==0.12.23"
FASTPATH_PY = "/opt/fastpath/bin/python"
LAYOUT, STYLE = "schema_branch_mark", "cygnet"
PORT = 30000
HOST_TAG = "modal"                           # meta "host": ONE value over every read of the job (gate_dev.pipeline_check)
SERVER_ARGS = {"max_running_requests": 64, "max_mamba_cache_size": 400}      # H100 S1 arm (hosting/sglang_host SERVER_DEFAULTS)
C1_PIN_TOKENIZER = ("tokenizer.json", "tokenizer_config.json", "chat_template.jinja", "train_meta.json", "adapter_config.json")
C1_ADAPTER_DIR_CANDIDATES = ("/vol/models/q35_4b_main500k_init", "/vol/models/q35_4b_main500k")

# ------------------------------------------------------------------ money
CAP_USD = 15.00                              # PREREG Record A88 (18 Oct 2026): was 4.00 / 3.60 / 3.90 (A42-D 2.x)
STOP_LAUNCH_USD = 13.50                      # 0.90 x cap, as before
HARD_STOP_USD = 14.60                        # ~0.975 x cap, as before (cap - 0.4 of room)
# `modal billing rates` 17 Oct 2026 (hosting/sglang_host RATE_USD_H 3.95; speed/.../oc1/common.py RATES)
RATES = {"cpu_core_h": 0.0473, "mem_gib_h": 0.008, "gpu_h": {"H100": 3.95}}
FN_CPU, FN_MEM_GIB = 6.0, 40.0
REGION = "any"                               # x1.0; a narrow region costs x1.75 and is not used
CONTAINER_OVERHEAD_S = 45.0
FN_RATE_USD_H = round(RATES["gpu_h"]["H100"] + FN_CPU * RATES["cpu_core_h"] + FN_MEM_GIB * RATES["mem_gib_h"], 4)
# The function timeout: even a container that is never cancelled cannot take the total above the cap (rate x timeout + overhead).
SESSION_TIMEOUT_S = int(((CAP_USD - 0.10) / FN_RATE_USD_H) * 3600 - CONTAINER_OVERHEAD_S) // 60 * 60


def container_cost_usd(seconds: float, rate_h: float = FN_RATE_USD_H, overhead_s: float = CONTAINER_OVERHEAD_S) -> float:
    return (max(0.0, seconds) + overhead_s) / 3600.0 * rate_h


class BudgetExceeded(RuntimeError):
    pass


class Budget:
    """Running spend = closed segments (ledger file) + open segments (elapsed x rate). One ledger for every call of this tool,
    so the USD 4.00 cap is shared by the grid session(s) and the parity job.

      open(name, rate_h)     a container is up (call when the container reports it started; the overhead is charged at once)
      close(name, seconds)   it ended; seconds = the container's own measured wall seconds if known, else elapsed
      can_launch(est_usd)    False when spent + est_usd would pass STOP_LAUNCH_USD
      must_cancel()          True from HARD_STOP_USD on
    """

    def __init__(self, path=LEDGER, cap=CAP_USD, stop_launch=STOP_LAUNCH_USD, hard_stop=HARD_STOP_USD, clock=time.time,
                 overhead_s=CONTAINER_OVERHEAD_S, persist=True):
        if not (0 < stop_launch < hard_stop < cap <= CAP_USD + 1e-12):
            raise ValueError(f"budget: need 0 < stop_launch {stop_launch} < hard_stop {hard_stop} < cap {cap} <= {CAP_USD}")
        self.path, self.cap, self.stop_launch, self.hard_stop = Path(path), cap, stop_launch, hard_stop
        self.clock, self.overhead_s, self.persist = clock, overhead_s, persist
        self.closed, self.open_, self.extra = [], {}, []
        if persist and self.path.exists():
            d = json.loads(self.path.read_text())
            self.closed, self.extra = d.get("closed", []), d.get("extra", [])
            self.open_ = {k: (v["t0"], v["rate_h"]) for k, v in (d.get("open") or {}).items()}

    def spent_closed(self) -> float:
        return sum(c["usd"] for c in self.closed) + sum(e["usd"] for e in self.extra)

    def spent_open(self) -> float:
        now = self.clock()
        return sum(container_cost_usd(now - t0, r, self.overhead_s) for t0, r in self.open_.values())

    def spent(self) -> float:
        return self.spent_closed() + self.spent_open()

    def remaining(self) -> float:
        return self.cap - self.spent()

    def open(self, name: str, rate_h: float = FN_RATE_USD_H):
        if name in self.open_:
            raise ValueError(f"{name} already open")
        self.open_[name] = (self.clock(), rate_h)
        self.save()

    def close(self, name: str, seconds: float | None = None) -> float:
        t0, rate = self.open_.pop(name)
        elapsed = self.clock() - t0
        secs = elapsed if seconds is None else max(float(seconds), 0.0)
        usd = container_cost_usd(secs, rate, self.overhead_s)
        self.closed.append({"name": name, "usd": round(usd, 4), "seconds": round(secs, 1), "elapsed_s": round(elapsed, 1),
                            "rate_h": round(rate, 4), "utc": utc()})
        self.save()
        return usd

    def add_extra(self, name: str, usd: float):
        self.extra.append({"name": name, "usd": round(float(usd), 4)})
        self.save()

    def can_launch(self, est_usd: float) -> bool:
        return self.spent() + est_usd <= self.stop_launch + 1e-9

    def must_cancel(self) -> bool:
        return self.spent() >= self.hard_stop

    def check_launch(self, name: str, est_usd: float):
        if not self.can_launch(est_usd):
            raise BudgetExceeded(f"{name}: spent ${self.spent():.2f} + estimate ${est_usd:.2f} > stop-launch "
                                 f"${self.stop_launch:.2f} (cap ${self.cap:.2f})")

    def save(self):
        if not self.persist:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"cap_usd": self.cap, "stop_launch_usd": self.stop_launch, "hard_stop_usd": self.hard_stop,
                                   "closed": self.closed, "extra": self.extra,
                                   "open": {k: {"t0": v[0], "rate_h": v[1]} for k, v in self.open_.items()},
                                   "spent_closed_usd": round(self.spent_closed(), 4)}, indent=1))
        os.replace(tmp, self.path)

    def summary(self) -> dict:
        return {"spent_usd": round(self.spent(), 4), "closed_usd": round(self.spent_closed(), 4), "open_usd": round(self.spent_open(), 4),
                "cap_usd": self.cap, "stop_launch_usd": self.stop_launch, "hard_stop_usd": self.hard_stop,
                "n_closed": len(self.closed), "remaining_to_stop_launch_usd": round(self.stop_launch - self.spent(), 4)}


# ------------------------------------------------------------------ payer guard
class PayerRefused(SystemExit):
    pass


GO_KEYS = ("profile", "owner_words", "go", "written_utc")


def read_go(path: Path = GO_FILE) -> dict:
    """The owner's GO #1 payer record. Refuses when it is missing, unreadable, incomplete, or names an empty / odd profile."""
    p = Path(path)
    if not p.exists():
        raise PayerRefused(f"payer guard: {p.name} does not exist: the owner names the Modal profile at GO #1 (default: refuse)")
    try:
        go = json.loads(p.read_text())
    except (OSError, ValueError) as e:
        raise PayerRefused(f"payer guard: {p.name} is not readable JSON ({type(e).__name__})") from None
    if not isinstance(go, dict):
        raise PayerRefused("payer guard: the GO record must be a JSON object")
    miss = [k for k in GO_KEYS if not (isinstance(go.get(k), str) and go[k].strip())]
    if miss:
        raise PayerRefused(f"payer guard: the GO record lacks {miss} (profile, owner_words, go, written_utc)")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{1,63}", go["profile"].strip()) or go["profile"] != go["profile"].strip():
        raise PayerRefused(f"payer guard: {go['profile']!r} is not a plain Modal profile name")
    if go["profile"].lower() in ("default", "none", "null", "any", "*"):
        raise PayerRefused("payer guard: the owner must name a real profile (not a default / wildcard)")
    if "GO" not in go["go"].upper():
        raise PayerRefused(f"payer guard: 'go' must name the GO (e.g. 'GO #1'), got {go['go']!r}")
    if len(go["owner_words"].strip()) < 8:
        raise PayerRefused("payer guard: owner_words must hold the owner's own words naming the payer")
    cap = go.get("cap_usd")
    if cap is not None and not (isinstance(cap, (int, float)) and not isinstance(cap, bool) and 0 < cap <= CAP_USD):
        raise PayerRefused(f"payer guard: cap_usd {cap!r} in the GO record may only LOWER the {CAP_USD} cap")
    return go


def go_cap(go: dict) -> float:
    return float(go["cap_usd"]) if go.get("cap_usd") is not None else CAP_USD


def read_policy(path: Path | None = None) -> dict:
    """PAYER_POLICY.json: {"never_payers": [...], "c2_training_relay": [...]}. Fail closed: missing / unreadable / odd = refuse."""
    p = Path(path or POLICY_FILE)
    try:
        d = json.loads(p.read_text())
    except (OSError, ValueError) as e:
        raise PayerRefused(f"payer guard: {p.name} is missing or unreadable ({type(e).__name__}): refuse (fail closed)") from None
    for k in ("never_payers", "c2_training_relay"):
        v = d.get(k) if isinstance(d, dict) else None
        if not (isinstance(v, list) and v and all(isinstance(x, str) and x for x in v)):
            raise PayerRefused(f"payer guard: {p.name} must hold a non-empty list of profile names under {k!r}")
    return d


def open_c2_segments(seg_log: Path | None = None) -> list:
    """Segments that c2_chain.sh opened and has not closed yet: [{"seg", "profile", "start"}]. An unreadable log raises (refuse)."""
    p = Path(seg_log or C2_SEGMENTS)
    if not p.exists():
        return []
    opened, closed = {}, set()
    try:
        for line in p.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            key = (r.get("seg"), r.get("profile"), r.get("start"))
            if r.get("open"):
                opened[key] = r
            elif "end" in r:
                closed.add(key)
    except (OSError, ValueError, AttributeError) as e:
        raise PayerRefused(f"payer guard: {p.name} is unreadable ({type(e).__name__}): cannot tell whether C2 training runs: refuse") from None
    return [{"seg": k[0], "profile": k[1], "start": k[2]} for k in opened if k not in closed]


def c2_training_problem(profile: str, policy: dict, seg_log: Path | None = None, final_path: Path | None = None) -> str | None:
    """Why `profile` may not pay yet: it is a C2 training relay account and training is not over, or a segment is open on it."""
    if profile not in policy["c2_training_relay"]:
        return None
    for s in open_c2_segments(seg_log):
        if s["profile"] == profile:
            return f"C2 training segment {s['seg']!r} is still open on {profile!r} (c2_segments.jsonl)"
    if not Path(final_path or C2_FINAL).exists():
        return f"C2 training is not over ({Path(final_path or C2_FINAL).name} does not exist): {profile!r} is a C2 relay account"
    return None


def modal_cli_command(argv=None):
    argv = sys.argv if argv is None else argv
    if not argv:
        return None
    a0 = Path(argv[0])
    if a0.name == "modal" or (a0.name == "__main__.py" and a0.parent.name == "modal"):
        for a in argv[1:]:
            if not a.startswith("-"):
                return a
    return None


def payer_guard(env=None, argv=None, active=None, go_path: Path | None = None, policy_path: Path | None = None,
                seg_log: Path | None = None, final_path: Path | None = None) -> str:
    """Refuse unless MODAL_PROFILE is exported and is exactly the profile the owner named in the GO record. Returns it."""
    env = os.environ if env is None else env
    argv = sys.argv if argv is None else argv
    go = read_go(go_path or GO_FILE)
    policy = read_policy(policy_path)
    if go["profile"] in policy["never_payers"]:
        raise PayerRefused(f"payer guard: {go['profile']!r} is never a payer for this tool (PAYER_POLICY.json never_payers)")
    prof = env.get("MODAL_PROFILE")
    if not prof:
        raise PayerRefused("payer guard: export MODAL_PROFILE explicitly (the default profile is never used)")
    if prof in policy["never_payers"]:
        raise PayerRefused(f"payer guard: MODAL_PROFILE={prof!r} is never a payer for this tool (PAYER_POLICY.json never_payers)")
    if prof != go["profile"]:
        raise PayerRefused(f"payer guard: MODAL_PROFILE={prof!r} is not the profile the owner named at GO #1 ({go['profile']!r})")
    why = c2_training_problem(prof, policy, seg_log, final_path)
    if why:
        raise PayerRefused(f"payer guard: {why}: refuse (the grid reads start only after C2 training has ended)")
    bad = [k for k in ("MODAL_TOKEN_ID", "MODAL_TOKEN_SECRET") if env.get(k)]
    if bad:
        raise PayerRefused(f"payer guard: {bad} set in the environment would override the {prof} token: unset them")
    if active is None:
        try:
            import modal.config as _mc
            active = getattr(_mc, "_profile", prof)
        except Exception:  # noqa: BLE001 - no client: nothing else can pay
            active = prof
    if active != prof:
        raise PayerRefused(f"payer guard: the modal client's active profile is {active!r}, not {prof!r}")
    cmd = modal_cli_command(argv)
    if cmd is not None and cmd != "run":
        raise PayerRefused(f"payer guard: only `modal run` is allowed here (got `modal {cmd}`)")
    if any(a in ("--detach", "-d") for a in argv[1:]):
        raise PayerRefused("payer guard: --detach is refused (Ctrl-C on the laptop must stop the GPU)")
    return prof


# ------------------------------------------------------------------ path / name guard
FORBIDDEN_SUBSTRINGS = ("ohs", "sealed", "c_spec/sealed_brief", "c_build/preread", "bench/external_quarantine",
                        "bench/longbench_v2", ".claude", "jev_out", "jevbench", "decision_index")
FORBIDDEN_NAME_WORDS = ("ohs", "sealed", "jev", "quarantine", "longbench")


def path_problem(p) -> str | None:
    s = str(p).replace("\\", "/").lower()
    for w in FORBIDDEN_SUBSTRINGS:
        if w in s:
            return f"path {str(p)!r} contains {w!r}"
    return None


def safe_path(p) -> Path:
    bad = path_problem(p)
    if bad:
        raise SystemExit(f"refused: {bad} (OHS / sealed / quarantine / Jev data is never opened)")
    return Path(p)


def name_ok(name: str) -> bool:
    n = str(name).lower()
    return not any(w in n for w in FORBIDDEN_NAME_WORDS)


def check_names(*names) -> None:
    for n in names:
        if not name_ok(n):
            raise SystemExit(f"refused: split / model name {n!r} holds ohs / sealed / jev / quarantine / longbench")


# ------------------------------------------------------------------ io
def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha256_file(p, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def canon_sha(obj) -> str:
    return hashlib.sha256(canon(obj).encode()).hexdigest()


def read_jsonl(p) -> list:
    out = []
    with open(safe_path(p)) as f:
        for line in f:
            if line.strip():
                out.append(json.loads(line))
    return out


def write_json(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(obj, indent=1, default=str))
    os.replace(tmp, p)


def write_jsonl(p, rows):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    with open(tmp, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    os.replace(tmp, p)


def read_name(cand: str) -> str:
    return READ_TPL.format(cand=cand)
