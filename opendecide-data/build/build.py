#!/usr/bin/env python3
"""OpenDecide v1.0-rc build driver (DESIGN 13).

    python3 build/build.py --stage all --seed 20260925
    python3 build/build.py --stage normalise            # one step: name, sNN, or sNN_name
    python3 build/build.py --stage all --lofo A         # leave-one-family-out train variant (passed to the steps)
    python3 build/build.py --rehydrate                   # restore idonly state/question text (build/rehydrate.py)
    python3 build/build.py --list                        # show steps, status and checkpoints

Steps are the files build/steps/sNN_<name>.py, run in numeric order as separate processes (so each stays under the
per-process RAM budget) with the project venv's python (.venv/bin/python) when it exists. Every step writes a
checkpoint to data/interim/checkpoints/<step>.json. With --stage all, a step whose checkpoint matches its code,
config, seed, flags and outputs is skipped (use --force to re-run). Steps named in config.yaml `build.steps` that do
not exist yet are skipped with a warning. The driver stops at the first failing step (exit code 1).

authored_by: llm:claude:foundation-engineer-1
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path

BUILD_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BUILD_DIR))
import common  # noqa: E402

STEP_RE = re.compile(r"^s(\d\d)_([a-z0-9_]+)\.py$")


def discover_steps() -> list[tuple[int, str, Path]]:
    """[(number, "sNN_name", path)] for every step file, sorted by number then name."""
    out = []
    for p in sorted(common.STEPS_DIR.glob("s[0-9][0-9]_*.py")):
        m = STEP_RE.match(p.name)
        if m:
            out.append((int(m.group(1)), p.stem, p))
    out.sort(key=lambda t: (t[0], t[1]))
    return out


def expected_steps() -> list[str]:
    return list(common.cfg("build", "steps", default=[]))


def resolve_stage(stage: str, steps: list[tuple[int, str, Path]]) -> list[tuple[int, str, Path]]:
    """Match --stage against 'sNN_name', 'sNN', 'NN' or 'name'."""
    s = stage.strip().lower()
    hits = [t for t in steps if s in (t[1], f"s{t[0]:02d}", f"{t[0]:02d}", str(t[0]), t[1].split("_", 1)[1])]
    if hits:
        return hits
    known = [n for n in expected_steps() if s in (n, n[:3], n[1:3], n.split("_", 1)[1])]
    if known:
        raise SystemExit(f"step {known[0]} is in the plan but build/steps/{known[0]}.py does not exist yet")
    raise SystemExit(f"unknown stage {stage!r}; available: {[t[1] for t in steps]}")


def interpreter(override: str | None) -> str:
    if override:
        return override
    if common.VENV_PYTHON.exists():
        return str(common.VENV_PYTHON)
    return sys.executable


def run_step(py: str, name: str, path: Path, seed: int, flags: list[str], log) -> int:
    cmd = [py, str(path), "--seed", str(seed), *flags]
    env = dict(os.environ)
    env[common.SEED_ENV] = str(seed)
    env["PYTHONPATH"] = str(BUILD_DIR) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    env.setdefault("TOKENIZERS_PARALLELISM", "false")
    log.info("run %s: %s", name, " ".join(cmd[1:]))
    t0 = time.time()
    rc = subprocess.call(cmd, cwd=str(common.ROOT), env=env)
    log.info("%s finished rc=%d in %.1fs", name, rc, time.time() - t0)
    return rc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="OpenDecide build driver (DESIGN 13)")
    ap.add_argument("--stage", default=None, help="all | step name (e.g. normalise, s02, s02_normalise)")
    ap.add_argument("--seed", type=int, default=None, help="master seed (default: config master_seed = 20260925)")
    ap.add_argument("--lofo", choices=list(common.cfg("build", "lofo_families", default=["A", "B", "E", "G"])),
                    default=None, help="emit the leave-one-family-out train variant for this family")
    ap.add_argument("--rehydrate", action="store_true",
                    help="restore idonly text: runs build/rehydrate.py, or passes --rehydrate to the steps with --stage")
    ap.add_argument("--force", action="store_true", help="re-run steps even when their checkpoint is current")
    ap.add_argument("--from", dest="from_stage", default=None, help="with --stage all: start at this step")
    ap.add_argument("--python", default=None, help="interpreter for the steps (default: .venv/bin/python)")
    ap.add_argument("--list", action="store_true", help="list steps and checkpoint status, then exit")
    ap.add_argument("--dry-run", action="store_true", help="print the steps that would run, then exit")
    args = ap.parse_args(argv)

    seed = int(args.seed if args.seed is not None else common.cfg("master_seed"))
    os.environ[common.SEED_ENV] = str(seed)
    common.ensure_dirs()
    log = common.get_logger("build")
    steps = discover_steps()
    present = {t[1] for t in steps}
    flags: list[str] = []
    if args.lofo:
        flags += ["--lofo", args.lofo]
    if args.rehydrate and args.stage:
        flags.append("--rehydrate")
    ck_flags = {"lofo": args.lofo, "rehydrate": bool(args.rehydrate and args.stage)}

    if args.list:
        for name in expected_steps() + sorted(present - set(expected_steps())):
            path = common.STEPS_DIR / f"{name}.py"
            if not path.exists():
                print(f"{name:24s} missing")
                continue
            ok, why = common.checkpoint_is_current(name, step_file=path, seed=seed)
            print(f"{name:24s} {'current' if ok else 'stale: ' + why}")
        return 0

    if args.rehydrate and not args.stage:
        script = BUILD_DIR / "rehydrate.py"
        if not script.exists():
            log.warning("build/rehydrate.py does not exist yet; nothing to rehydrate")
            return 0
        return run_step(interpreter(args.python), "rehydrate", script, seed, [], log)

    if not args.stage:
        ap.error("--stage is required (or --list / --rehydrate)")
    if seed != int(common.cfg("master_seed")):
        log.warning("seed %d differs from the master seed %s: this is not the canonical build", seed,
                    common.cfg("master_seed"))
    py = interpreter(args.python)
    log.info("build start: stage=%s seed=%d lofo=%s python=%s", args.stage, seed, args.lofo, py)

    if args.stage.strip().lower() == "all":
        for name in expected_steps():
            if name not in present:
                log.warning("step %s is not implemented yet (build/steps/%s.py missing); skipped", name, name)
        todo = steps
        if args.from_stage:
            first = resolve_stage(args.from_stage, steps)[0]
            todo = [t for t in steps if (t[0], t[1]) >= (first[0], first[1])]
        for num, name, path in todo:
            if not args.force:
                ok, why = common.checkpoint_is_current(name, step_file=path, seed=seed)
                ck = common.read_checkpoint(name) or {}
                same_flags = all((ck.get("args") or {}).get(k) == v for k, v in ck_flags.items())
                if ok and same_flags:
                    log.info("skip %s (checkpoint current)", name)
                    continue
                log.info("%s needs a run (%s)", name, why or "flags changed")
            if args.dry_run:
                log.info("dry run: would run %s", name)
                continue
            rc = run_step(py, name, path, seed, flags, log)
            if rc != 0:
                log.error("step %s failed (rc=%d); stopping", name, rc)
                return 1
        log.info("build finished")
        return 0

    for num, name, path in resolve_stage(args.stage, steps):
        if args.dry_run:
            log.info("dry run: would run %s", name)
            continue
        rc = run_step(py, name, path, seed, flags, log)
        if rc != 0:
            log.error("step %s failed (rc=%d)", name, rc)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
