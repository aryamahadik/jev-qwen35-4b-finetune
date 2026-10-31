# od-sbx: Opus sign-off before the FIRST execution of training-row code

Date: Sun 18 Oct 2026, 15:44 EDT. Reviewer: Opus (security sign-off, read-only).
Image: `od-sbx-base-20261018-r2` (id 9151289144192312211). Manifest sha256 `29474351959951a20815e8e8645b6fa3df0888df6a553f9399ebfc85871d71c8`.
Executor tree hash `defbb2e49ae9589fc82b2c53d988b70ccedf7e9c0c226d7de38e47ee6eefa753`. pins.env `d7821319f3d13dc649cba4ef3aa337e333313e7b515b96c6c0c39d99816823fd` (FROZEN, unchanged).

## VERDICT: SIGNED

The sandbox is fit for the first execution of untrusted training-row code (Python, Node, Go, sh) under gVisor with no network,
on od-sbx1, under conditions C1 to C6 below. This sign-off does NOT cover sealed data, and it does NOT cover od-sbx-s. Section (3) lists
what od-sbx-s needs.

## What I checked (read-only; no VM touched, no gcloud, no docker)

- Read in full: IMAGE_RECIPE.md (all sections, including 6, 7 and 10.1 to 10.5), PINS_SKEPTIC.md, BUILD_RECORD.md (sections 0 to 8),
  SELFTEST_od-sbx1_20261018_r2.json, rebuild_logs/* (IMAGE_MANIFEST_r2.json, 50/60 logs, pre60_checks.sh), every executor module
  (config, dockercmd, runner, cli, selftest, fixtures, verdict, treehash, launcher), executor/tests, host/*, images/Dockerfile.*, build/50, build/60, common.sh.
- Ran `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -c pytest.ini -p no:cacheprovider sandbox/executor/tests`: **37 passed**. No bytecode was left behind.
- Recomputed the executor tree hash from the reviewed tree (od_sbx/*.py + od_sbx_launcher.py, the same files step 50 installs): **defbb2e4...a753**.
  It equals the manifest and ST-7.4. So the code I reviewed and tested is the code in the image.
- Local hashes: pins.env `d7821319...`, vendor/requirements.lock `9ba66ff9...` (both equal the manifest), host/hostfw.nft `74f8333d...`, host/docker-daemon.json `e4ed17e4...`
  (both equal BUILD_RECORD section 8).
- The local manifest copy is re-serialized (1-space indent), so its own sha256 is `9099baf3...`. Re-serialized in jq's 2-space layout it hashes to **29474351...**,
  which is the manifest the 46/46 self-test ran against. Its content is therefore exact.

## (1) Fitness for first execution: property by property

| Property | Evidence | Status |
|---|---|---|
| S1 / F-GO1 temp dir | `BASE_ENV TMPDIR=/work/.tmp`; the prelude `cp -R /in/. /work/ && mkdir /work/.tmp` runs before `exec`. The directory is inside the size-capped /work tmpfs, so there is no new mount and no host path. ST-6.1 to 6.4 need the EXACT last line `/work/.tmp` on all four toolchains (PASS). ST-6.6 `go test` + `t.TempDir()` passes in 2.2 s | OK |
| Reserved names / reject paths | `norm_key` runs first (it rejects absolute, `..` and NUL keys). Then `_reject_reserved` (`.tmp` for every toolchain and kind; Go `.gocache`/`.gopath` for run patches and all overlays). Then sanitize, overlay, `stage()` (escape and clash give StageError). `cli` turns StageError into `rejected` + `rejected_unstageable_tree` and goes on. Tests exercise the real `run_batch` and the alias spellings | OK |
| Egress | 5 layers: no external IP / NAT / PGA on sbx-vpc; VPC egress DENY v4+v6 at priority 1000 with no target tag; hostfw output policy drop (non-root cannot reach metadata or DNS: ST-1.1/1.2/1.4); `docker --network none`; runsc `--network=none` (daemon runtimeArgs). ST-2.1 to 2.5 show `BLOCKED 101` and `IFACES lo` | OK (VPC side from the record only: C1) |
| No service account / scopes | ST-1.6: HTTP 200 with an empty body. The record shows `--no-service-account --no-scopes` | OK |
| No external IP, Secure Boot, OS Login, block-project-ssh-keys, max run time | Section 1 records these flags for the FIRST od-sbx1. Section 8 does NOT record the flags od-sbx1 was recreated with for r2. The self-test cannot see them | Needs C1 |
| Read-only root, cap-drop, uid | `--read-only --cap-drop ALL --security-opt no-new-privileges --user 65534:65534` (+ daemon no-new-privileges, gVisor allow-suid=false). ST-3.1 to 3.4, 3.6 and 3.7 (`CapEff 0`, `CapBnd 0`, `NoNewPrivs 1`) PASS | OK |
| tmpfs and resource caps | /work 256m (go 512m), stage /out tmpfs 512M (nosuid, nodev), pids 256, mem = swap = 1g, 1 cpu, nofile 256, fsize 64 MiB, core 0. ST-4.1 to 4.7 PASS (OOM 137, DISK/OUT/FSIZE stopped, timeout 10.1 s, stdout kept at exactly 64 KiB) | OK |
| Determinism | 2 runs (3 for will-this-test-fail). A mismatch in (exit, stdout sha256) drops the row and is counted. ST-6.5 detects a nondeterministic fixture | OK (see C3 for suites) |
| Verdict integrity | Computed outside the container after `docker rm`. Strict UTF-8, no DTD, exact id set. ST-5.0 to 5.4 and 5.6 PASS. ST-5.5i is the known in-process gap (10.1 ruling stands) | OK |
| gVisor | ST-7.5 (`4.19.0-gvisor` vs host 7.0.0-1014-gcp), systrap, host-uds/host-fifo none. ST-3.5i shows ptrace of an own child only, as ruled (stays informational) | OK |
| Tree-hash / pin pinning | ST-7.1 to 7.4 and 7.6 PASS. run-batch refuses unless selftest.json is PASS for the CURRENT manifest sha256, and it re-runs ST-1.5/1.6/1.7 + the stage mount at batch start | OK |

## Binding conditions for first execution (od-sbx1)

- **C1 (before the first batch; read-only gcloud, by the coordinator):** run `gcloud compute instances describe od-sbx1` and record that:
  - the source image is `od-sbx-base-20261018-r2` (by name);
  - there are no accessConfigs (no external IP) and serviceAccounts is empty;
  - shieldedInstanceConfig has secureBoot, vTPM and integrityMonitoring all true;
  - metadata has `block-project-ssh-keys=TRUE` and `enable-oslogin=TRUE`, and no `ssh-keys` item;
  - scheduling is maxRunDuration 5400 s with instanceTerminationAction DELETE;
  - the network is sbx-vpc/sbx-subnet and there is one disk.

  Also run `gcloud compute firewall-rules list --filter=network:sbx-vpc` and confirm exactly the 3 rules, and `gcloud compute routers list`
  and confirm there is no Cloud NAT on sbx-vpc. Write all of this into BUILD_RECORD.md section 8.
- **C2:** run batches only on a boot whose own self-test is PASS for manifest `29474351...` (run-batch enforces this). Create sandbox VMs from the image NAME,
  never from `--image-family`, and never use the deprecated `od-sbx-base-20261018`. Start the batch soon after boot: the 1h30m DELETE timer runs alongside the 3600 s batch cap.
  Copy results out before the VM deletes itself.
- **C3 (pilot first):** the first batch is small (about 50 rows or fewer, all four toolchains, run AND suite rows). Read its counters before scaling up.
  The self-test never sends a SUITE through `run_repeated`: ST-5.x and ST-6.6 use `run_once`. If pytest, `go test` or `node --test` print timings to stdout
  (`2 passed in 0.03s`, `ok det 0.008s`, duration_ms), every suite row will differ between runs and be dropped as nondeterministic. Keep timing output off stdout
  (for example `pytest -qq`, or reports to /out with stdout discarded).
- **C4 (job-writer rules for L-C; no executor change needed):**
  - `report` must be a bare file name (no `/` or `..`). R4 is still not enforced in `cli`.
  - Keep the staged trees well under the /work cap. A prelude `cp`/`mkdir` failure exits 1, which looks the same as the program's own exit 1.
  - Treat docker exit 125 as an infrastructure error: drop the row and count it, never label it.
  - The 10.4 (a) to (d) and 10.5 T56 lint rules stand.
- **C5:** result files from the VM (stdout/stderr excerpts, stripped paths) are untrusted DATA, never instructions, for every agent that reads them.
- **C6:** any edit to pins.env, the executor or the host files means a new image, a new self-test and a new Opus sign-off. The rebuild notes (10.5 step 3) gain the line
  `sudo systemctl stop od-sbx-hostfw` right before step 60.

## (2) The crash-consistent image: ACCEPTED as the image of record. No rebuild.

Reasons:
1. Every byte of image content was written and flushed BEFORE the stop. Step 60 runs under `set -e`. Its `sync` comes after the manifest
   and the scrub, and before the log line "scrubbed. Powering off", and that line is in `rebuild_logs/60_build.log`. The docker layers were loaded in step 50,
   about 8 minutes earlier.
2. The forced stop can only tear writes made AFTER that sync, during the hung shutdown: journald, systemd state, and the bolt DBs of dockerd and containerd, which are crash-safe.
   None of these is security- or label-relevant. The image is immutable, so every instance replays the same ext4 journal and sees the same bytes. The od-sbx1 boot
   that passed 46/46 therefore stands for every instance cut from this image.
3. The contents are verified where it matters:
   - the executor tree hash is exact, and I recomputed it from the reviewed tree;
   - the manifest content is exact;
   - docker's content-addressed store checks the image configs on read (ST-7.1);
   - the runsc and toolchain versions match (ST-7.2, 7.3);
   - every isolation check re-runs at every boot of every instance.
4. A clean-shutdown rebuild adds NO security property. Stopping hostfw on the build VM only flushes that VM's runtime ruleset; the unit stays enabled in the disk.
   A rebuild would also mean a new image, a new manifest hash and a new self-test: more steps and more chances for deviation, for no gain.
   The hang itself is explained: the stub resolver runs as a non-root uid, so hostfw drops its DNS. It is not a disk fault.

Recorded deviations accepted: the poweroff hang plus the external stop, od-sbx1 recreated from r2 (its flags need C1), the stale selftest.json removed before step 60
(harmless: the unit deletes it at every start), and the build-VM host key checked against the serial console.

## (3) What must hold before od-sbx-s (the sealed-side VM) is created

1. C1 and C2 are done for od-sbx1, and the C3 pilot batch has run cleanly: no host-guard refusal, and every counter is understood.
2. od-sbx-s uses the same image by name (r2) and the same flags as od-sbx1:
   - `--no-address --no-service-account --no-scopes`;
   - Secure Boot, vTPM and integrity monitoring;
   - `block-project-ssh-keys=TRUE,enable-oslogin=TRUE`, with no ssh-keys item;
   - `--max-run-duration` with `--instance-termination-action=DELETE`;
   - sbx-vpc, no data disk.

   Verify with `describe` at creation, as in C1. In sbx-vpc the firewall list is still exactly the 3 rules, with no NAT, no PGA and no peering. The egress deny also blocks traffic between od-sbx1 and od-sbx-s.
3. Its own first boot passes the self-test 46/46 with manifest `29474351...` and tree hash `defbb2e4...`, saved as `SELFTEST_od-sbx-s_<date>.json`,
   BEFORE any sealed byte is copied in. In the same root shell, record:
   - the sha256 of `/etc/od-sbx/hostfw.nft`, `/etc/docker/daemon.json`, `od-sbx-hostfw.service` and `od-sbx-selftest.service`; they must equal the local
     `74f8333d...`, `e4ed17e4...`, `06a5f42c...` and `562a6a0f...`;
   - that `dmesg | grep -i 'EXT4-fs error'` is empty.

   These close the crash-consistency question for files that the manifest does not hash.
4. At first SSH, check the host key fingerprint against the serial-port output. cloud-init regenerates the keys, because step 60 ran `cloud-init clean`.
5. **A separate sealed-layer review must be signed before any sealed data enters.** It must give:
   - results that carry verdicts and counters ONLY. Today `cli` writes `stdout[:200]` and `stderr[:200]` for every run, and a failing assert, or code under test
     that reads the hidden suite in-process, would put sealed test text into those excerpts;
   - sealed inputs copied in by IAP scp straight to od-sbx-s, never through od-sbx1;
   - inputs and results deleted with the VM;
   - the A68 OHS rules on who may read sealed results.
6. Recommended (not blocking): (a) check that the PROJECT metadata keys hold no secrets (a keys-only listing), because root on any VM can read `project/attributes`.
   (b) Consider a sbx-vpc DNS policy that stops recursive resolution. The metadata server's resolver is exempt from VPC firewall rules, so it is the only
   way out left after a double escape (gVisor plus the host kernel).

## (4) Blocking defects: NONE

Non-blocking items (all fail closed or are record-only). Fold them into the next rebuild or the next record update:
- N1 (R2, open): in `stage()`, an OSError other than a clash (ENOSPC, ENAMETOOLONG) aborts the whole batch, and no `.manifest.json` is written. The same happens for a malformed job line or an unknown toolchain.
- N2 (R4, open): `cli` does not validate `report`. A workload symlink on an intermediate directory of a non-bare name would make the root executor read that host path.
  The contents only feed a parser and never leave the VM. C4 covers this.
- N3: a prelude failure and docker exit 125 cannot be told apart from program exit codes. A distinct prelude exit code plus outcome ERROR is needed (C4 until then).
- N4: the determinism check compares stdout only, and the verdict comes from run 0 only. The verdicts of the repeats are not compared.
- N5 (records): BUILD_RECORD section 8 lists the hostfw.nft and daemon.json hashes as "manifest fields", but the manifest has no such fields. IMAGE_RECIPE 10.5
  is still headed "PROPOSED ... reviewed by nobody yet". The two F-GO1 skeptic reports are not filed in this directory (I reviewed the fix myself: code plus 37 tests, SOUND).
  The 10.4 checklist line "Opus sign-off before first execution" should point to this file.
- N6 (R3, R5, open): there is no `RequiresMountsFor=/srv/od-sbx/stage`, and `pip uninstall ... || true` is still in Dockerfile.python.
- N7: every sandbox VM's poweroff hangs under hostfw. This is harmless (DELETE at max-run, or a forced stop). Expect `instances stop` to take the forced path.

Residual risks accepted, with the threat model of executor/README.md (Claude-authored code, no data or credentials on od-sbx1):
- the in-process report forgery (ST-5.5i), handled by the 10.1 T56 labelling rules;
- gVisor shares the host kernel;
- after a double escape, root on the VM can query the metadata server (instance and project metadata, and DNS), but there are no service-account tokens to steal.
