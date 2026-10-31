"""Pure builder for the per-execution `docker run` argv. No I/O, no docker needed to test it."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .config import BASE_ENV, LABEL, LIMITS, NOBODY, WORK_TMP, Limits


@dataclass(frozen=True)
class RunPlan:
    name: str                    # unique container name, e.g. od-sbx-<batch>-<row>-<rep>
    image_id: str                # sha256:... from IMAGE_MANIFEST, never a tag
    in_dir: str                  # host dir, mounted read-only at /in, copied into /work first
    out_dir: str                 # host dir (owned by 65534), mounted rw at /out for reports
    argv: Sequence[str]          # the command to exec inside /work
    extra_env: Sequence[tuple[str, str]] = ()
    tmpfs_work: str | None = None            # per-toolchain override of Limits.tmpfs_work (config.TMPFS_WORK)
    seed: tuple[str, str] | None = None      # (image path, path under /work) copied before the command (config.SEEDS, Go cache)


def build_run_argv(p: RunPlan, lim: Limits = LIMITS) -> list[str]:
    a = [
        "docker", "run",
        "--name", p.name, "--label", LABEL,
        "--runtime", "runsc", "--network", "none", "--ipc", "none",
        "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
        "--pids-limit", str(lim.pids),
        "--memory", lim.memory, "--memory-swap", lim.memory, "--cpus", lim.cpus,
        "--ulimit", f"nofile={lim.nofile}:{lim.nofile}",
        "--ulimit", f"fsize={lim.fsize_bytes}:{lim.fsize_bytes}",
        "--ulimit", "core=0:0",
        "--user", f"{NOBODY}:{NOBODY}",
        "--tmpfs", f"/work:rw,exec,nosuid,nodev,size={p.tmpfs_work or lim.tmpfs_work},uid={NOBODY},gid={NOBODY},mode=0700",
        "--hostname", "od-sbx",                 # a random container-id hostname would make `hostname`-printing rows nondeterministic
        "--mount", f"type=bind,src={p.in_dir},dst=/in,readonly",
        "--mount", f"type=bind,src={p.out_dir},dst=/out",
        "--workdir", "/work", "--pull", "never", "--log-driver", "none", "--stop-timeout", "0",
    ]
    for k, v in sorted({**BASE_ENV, **dict(p.extra_env)}.items()):
        a += ["--env", f"{k}={v}"]
    # copy staged inputs into the tmpfs, create the temp dir (F-GO1: TMPDIR is /work/.tmp, never /work itself; a reserved name that
    # runner.run_once rejects in every tree, so this mkdir cannot clash and a failure here is loud), then exec the command (so the
    # command is PID-1 child of sh via exec)
    prelude = f"cp -R /in/. /work/ && mkdir {WORK_TMP}"
    if p.seed:
        src, dst = p.seed
        prelude += f" && mkdir -p {dst} && cp -R {src}/. {dst}/"
    a += [p.image_id, "sh", "-c", prelude + ' && exec "$@"', "sh", *p.argv]
    return a
