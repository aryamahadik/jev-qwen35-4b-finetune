# od-sbx executor (skeleton, stdlib only, host python3)

THREAT MODEL (read first). The code that runs here is Claude-authored synthetic code and program mutants, not an
adversarial LLM. The real risks are accidents (fork bombs, disk fill, infinite loops, accidental network calls,
`rm -rf`) and deliberate tampering with the verdict by the T56 test-gaming rows. The sandbox VM holds no data, no
credentials and no egress, so an escape is low-value. gVisor is a proportionate control, not a statement that anything
is "safe". gVisor shares the host kernel, does not stop hardware side channels, and relies on host cgroups for
resource limits (docs: gvisor.dev/docs/architecture_guide/security/).

Layers: disposable VM (blast radius) > host nftables (output DROP, metadata root-only) > docker + runsc (systrap) >
one container per run, `--network none`, read-only root, all capabilities dropped, uid 65534, tmpfs /work.

"Rootless": the WORKLOAD is unprivileged (uid 65534, no capabilities, no-new-privileges, no setuid). The docker
daemon is root by design (research codeexec.md C6: rootless adds complexity without protecting anything the VM does
not already protect). The docker group is empty; the executor runs under sudo via `/opt/od-sbx/bin/od-sbx`.

Modules
- config.py    limits, paths, toolchain table (single source for the argv and the self-test)
- dockercmd.py PURE function that builds the `docker run` argv (unit-testable without docker)
- runner.py    run one container, enforce the timeout from OUTSIDE (`docker kill`), cap output, run N times, compare
- verdict.py   verdict computed OUTSIDE the container from exit code + structured report + expected test ids
- fixtures.py  source text of the self-test fixtures (never executed outside the sandbox; staged per check)
- selftest.py  the self-test list ST-1 .. ST-7 (see ../IMAGE_RECIPE.md section 7: the skeptic reviews exactly this list)
- cli.py       `od-sbx selftest | run-batch | cleanup | treehash`
- od_sbx_launcher.py  root-owned entry point: `python3 -I od_sbx_launcher.py ...` (`-I` ignores PYTHONPATH, so the launcher sets sys.path)
- tests/       static + pure-function tests (no docker, no fixture is executed): `cd c21_infra && python3 -m pytest -c pytest.ini -p no:cacheprovider sandbox/executor/tests`

Nothing in this tree has been executed on a VM (18 Oct 2026). First execution happens only after the Sonnet skeptic review
and the Opus sign-off. (The static tests above were run on the Mac; they start no container.)
