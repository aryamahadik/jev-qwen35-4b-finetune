# od-sbx base image: reviewed RECIPE (L-0 day-1 task 3, Sun 18 Oct 2026)

STATUS (updated 18 Oct, builder): image `od-sbx-base-20261018` was BUILT from this recipe; first self-test on od-sbx1 was 44/46 (ST-6.3, ST-6.6 FAIL, Go).
Cause CONFIRMED (TMPDIR=/work vs cmd/go's "ignoring go.mod in system temp root"); fix PROPOSED in section 10.5 (TMPDIR=/work/.tmp), awaiting a fresh skeptic
and Opus. UPDATE: the fix was reviewed (SOUND), REBUILT as `od-sbx-base-20261018-r2` and the self-test on od-sbx1 PASSED 46/46 (10.4 checklist, BUILD_RECORD.md section 8); pins.env untouched.
Original status: RECIPE SIGNED for the image build (Opus, Sun 18 Oct 2026, section 10.4); pins FROZEN. Nothing in this directory has
been executed on any machine yet. No generated code has run. The build scripts refuse `build` mode unless
`PINS_STATUS=FROZEN` in `pins.env`. Gate path: Sonnet skeptic (fresh) on this recipe and on the self-test list ->
Opus sign-off -> image build -> self-test on od-sbx1 -> Opus sign-off before first execution (target Wed 21 Oct).
Sources: research_v3/codeexec.md section 5.4 (+ corrections C1, C6, C7, C8), plan section 8 (od-sbx1 block), LANE_L-0.

## 1. What exists today

| Item | State |
|---|---|
| Project / zone | `system-one-509903` / `us-east4-c` (same as od-l4b) |
| Build VM | `od-sbx-build`, `e2-standard-2` (2 vCPU, 8 GB), CPU only, Ubuntu 24.04.5 LTS, kernel `7.0.0-1014-gcp`, 40 GB pd-balanced boot disk only (no data disk), label `purpose=c21-sandbox-build`, tag `od-sbx-build`, Shielded VM (Secure Boot, vTPM, integrity monitoring), `--no-service-account --no-scopes`, metadata `block-project-ssh-keys=TRUE`, `--max-run-duration=6h` with `--instance-termination-action=STOP` |
| Firewall rule (added to keep the build VM from reaching od-l4b / od-cpu1) | `od-sbx-build-deny-internal`: egress DENY all to `10.128.0.0/9`, priority 900, target tag `od-sbx-build`, network `default`. Verified: the build VM cannot reach od-l4b (10.150.0.2). Internet egress works (needed for downloads). The `default` network also has `default-allow-ssh` from 0.0.0.0/0; the build VM has an ephemeral external IP and only key-based SSH. |
| Candidate pins observed | see section 2 (pulled from go.dev, nodejs.org, python.org, gVisor apt repo, Docker Hub registry API, PyPI) |
| Only commands run on the VM | `uname`, `df`, `curl` of version metadata, `apt-get update`, `apt-cache policy`, `gpg --show-keys`. No install, no pull, no execution. |
| Written | this file, `pins.env`, `build/*.sh`, `images/*`, `host/*`, `executor/` skeleton, `vendor/README.md` |
| Checks done on the files | `bash -n` on all scripts; `ast.parse` on all Python (parse only, no import, no run) |

The VM is STOPPED when idle (see section 11 for start/stop commands). A stopped VM costs the 40 GB disk only
(list price roughly 4 USD/month, not measured; compute about 0.07 USD/hour while running, from list price).

## 2. Pins (candidate; each row is re-observed by the skeptic with the command in the last column)

| Component | Candidate pin | How to re-observe |
|---|---|---|
| gVisor runsc | release `20261012.0`; deb sha256 `7a440a03...a707ca`, sha512 `a81e1071...f7a3` (full values in pins.env); bundle `gvisor.tar.bz2` sha512 `9606445e...c5e` | `build/20_install_runsc.sh resolve` prints Packages stanza; bundle `.sha512` at `storage.googleapis.com/gvisor/releases/release/20261012.0/x86_64/gvisor.tar.bz2.sha512` |
| gVisor apt key | fingerprint `6F1D F85E 3A71 C249 18E7 27D5 6FC6 D554 E32B D943` | `gpg --show-keys --with-fingerprint` on `https://gvisor.dev/archive.key` (script aborts on mismatch) |
| Python | 3.12.15 (python.org lists 3.12.15; security-only branch) via `python:3.12.15-slim-bookworm@sha256:34386ef0cb08...07258` | `build/30_fetch_toolchains.sh resolve` |
| Node.js | 24.22.0 (LTS "Krypton", dist index dated 2026-10-14) via `node:24.22.0-bookworm-slim@sha256:a5f4366e8346...daee5`; `node-v24.22.0-linux-x64.tar.xz` sha256 `cc2f601c...5008` (cross-check) | `resolve` + `https://nodejs.org/dist/v24.22.0/SHASUMS256.txt` |
| Go | 1.26.9 via `golang:1.26.9-bookworm@sha256:d9c68c2c5116...1453c`; `go1.26.9.linux-amd64.tar.gz` sha256 `42d158b4...c2f8d` (cross-check) | `resolve` + `https://go.dev/dl/?mode=json&include=all` |
| bash / coreutils | from `debian:bookworm-slim@sha256:7c7b2c96...cc587` (bash 5.2, GNU coreutils) | `resolve` |
| pytest | 9.1.1 plus its dependencies, wheels only, hash-locked in `vendor/requirements.lock` | `resolve` writes `vendor/requirements.proposed.txt` |
| Host packages | docker.io `29.1.3-0ubuntu3~24.04.2`, containerd `2.2.1-0ubuntu1~24.04.3`, runc `1.3.4-0ubuntu1~24.04.1`, nftables `1.0.9-1ubuntu0.1`, apt-held | `build/10_install_base.sh resolve` |

Notes. (a) Node 24 and Go 1.26 are the pins the research file recommended (C1); Go 1.27.2 exists, 1.26.x stays within the
two-newest support rule and the plan asked for 1.26.x. (b) Python 3.12 is security-only, fine for a pin. (c) The
digests are INDEX (multi-arch manifest list) digests; the build pulls by digest, then asserts `RepoDigests` equals the
pin, then records the resolved single-arch image id in `IMAGE_MANIFEST.json`; the executor runs by image id only.
(d) Debian bookworm is the common base of the four toolchain images, so GNU coreutils output is the same across rows
(research C8).

## 3. The build machine

Created with (already run):

    gcloud compute firewall-rules create od-sbx-build-deny-internal --network default --direction EGRESS --priority 900 \
      --action DENY --rules all --destination-ranges 10.128.0.0/9 --target-tags od-sbx-build
    gcloud compute instances create od-sbx-build --zone us-east4-c --machine-type e2-standard-2 \
      --image-family ubuntu-2404-lts-amd64 --image-project ubuntu-os-cloud --boot-disk-size 40GB --boot-disk-type pd-balanced \
      --no-service-account --no-scopes --shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring \
      --labels purpose=c21-sandbox-build --tags od-sbx-build --metadata block-project-ssh-keys=TRUE \
      --max-run-duration=6h --instance-termination-action=STOP

`common.sh: assert_build_vm` makes every build script refuse to run unless: instance name is `od-sbx-build`,
`block-project-ssh-keys=TRUE`, the metadata service-accounts listing is empty, and exactly one disk is attached.
The build VM holds no data and no credentials: nothing from the Mac except this directory is copied to it.
Copy-in: `gcloud compute scp --recurse sandbox od-sbx-build:~/sandbox --zone us-east4-c` (internet-facing SSH with keys;
the scp-over-IAP flag is for the sandbox VMs, section 8).

## 4. Build order (every step is a script; `resolve` mode prints, `build` mode changes the VM)

Run as root on the build VM with `SBX_SRC=~/sandbox`:

| Step | Script | Does | Mode |
|---|---|---|---|
| 0 | `build/00_preflight.sh` | build-VM guard, Ubuntu 24.04, cgroup v2, disk space | read-only |
| 1 | `build/10_install_base.sh` | exact-version docker.io/containerd/runc/nftables + jq, zstd, bzip2; `apt-mark hold`; docker group must be empty | resolve, build |
| 2 | `build/20_install_runsc.sh` | gVisor signed apt repo, key fingerprint check, `apt-get download runsc=20261012.0`, sha256 AND sha512 of the deb checked against pins, `dpkg -i`, cross-check against the bundle sha512; legacy `runsc install` never used | resolve, build |
| 3 | `build/30_fetch_toolchains.sh` | resolve: digests + `requirements.proposed.txt`. build: `docker pull name@digest`, assert digest, hash-checked wheel download | resolve, build |
| 4 | `build/40_build_toolchain_images.sh` | four derived images from `images/Dockerfile.*`, built `--network=none`, saved as `.tar.zst` under `/opt/od-sbx/images` | build |
| 5 | `build/50_install_executor.sh` | `/etc/docker/daemon.json` (runsc default), executor to `/opt/od-sbx/executor`, nftables unit and self-test unit installed and ENABLED (not started), images `docker load`ed | build |
| 6 | `build/60_finalize_image.sh` | writes `/opt/od-sbx/IMAGE_MANIFEST.json`, scrubs keys/history/machine-id/apt lists, powers off | build |

Freeze procedure: skeptic runs both `resolve` commands independently and compares; Opus signs; then `PINS_STATUS=FROZEN`,
`vendor/requirements.proposed.txt` is copied to `vendor/requirements.lock`, and the hash of `pins.env` is recorded in the manifest.
The `resolve` of step 3 runs `pip download` inside the pinned python image (no host Python code from the internet
runs); it is the only step that executes anything fetched, and it executes pip only.

## 5. What ends up in the image

    /opt/od-sbx/executor/od_sbx/*.py     stdlib-only executor (host python3 3.12.3 from Ubuntu; never runs inside a sandbox)
    /opt/od-sbx/executor/od_sbx_launcher.py   M1: sets sys.path itself (`python3 -I` ignores PYTHONPATH); in the hashed tree
    /opt/od-sbx/bin/od-sbx               root-only wrapper (sudo): `python3 -I /opt/od-sbx/executor/od_sbx_launcher.py "$@"`
    /opt/od-sbx/images/od-sbx-{python,node,go,sh}.tar.zst   + loaded into the docker store, run by IMAGE ID
    /opt/od-sbx/wheels, requirements.lock   vendored pytest wheels with hashes (also installed in the python image)
    /opt/od-sbx/IMAGE_MANIFEST.json      versions, digests, image ids, executor tree hash, pins.env hash
    /etc/docker/daemon.json              runsc default runtime (systrap), no bridge, iptables off, no-new-privileges
    /etc/od-sbx/hostfw.nft               host firewall; unit od-sbx-hostfw.service enabled
    od-sbx-selftest.service              runs ST-1..ST-7 at every start; writes /var/lib/od-sbx/selftest.json
    Not present: pip index access at run time, npm/npx/corepack/yarn, Go module proxy, any credentials, any SSH key.

Toolchain images (all run as `65534:65534`, `WORKDIR /work`):
- python: `PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 TZ=UTC LANG=C.UTF-8`, pytest wheels installed from local files with
  `--require-hashes --no-deps`, pip/setuptools/wheel removed, trusted `/etc/od-sbx/pytest.ini` (the patch cannot replace it),
  `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `PYTHONNOUSERSITE=1` (HOME=/work would otherwise make /work/.local a user site searched before site-packages). Suites
  run as `python -s -P -m pytest ...` (S3). `unittest` is stdlib, available for the P-3 OHS-5 transfer slice.
- node: npm, npx, corepack and yarn removed; `node --test` only (junit reporter written to `/out`).
- go: `GOFLAGS=-mod=vendor GOPROXY=off GOTOOLCHAIN=local GOENV=off GOSUMDB=off CGO_ENABLED=0`, `GOCACHE`/`GOPATH` under `/work`, `TMPDIR=/work/.tmp`
  (F-GO1, section 10.5: never `/work` itself, cmd/go ignores a go.mod in the temp root) (no `GOTMPDIR`: go fails if that directory does not exist). The std build cache is PRE-WARMED at image build into `/opt/gocache-seed`
  (`images/gowarm`, M3) and copied into the run's tmpfs before the command (`config.SEEDS`; go tmpfs 512m, UNMEASURED: ST-6.3 and ST-6.6 are the controls).
- sh: debian bookworm-slim (bash 5.2, GNU coreutils), `LC_ALL=C`; starter allow-list of external commands in
  `images/allowlist_sh_commands.txt` (L-C finalises it; the generator lint reads it).

## 6. Hardening (maps to codeexec 5.4 items 1 to 7 and corrections C6, C7)

Host / VPC (applied at od-sbx1 creation, section 8; NOT in the image because firewall rules are VPC objects):
1. Own VPC `sbx-vpc`, custom subnet, no peering, no Cloud NAT, no Private Google Access, no VPN, no shared VPC.
2. Instance: CPU only, no external IP, `--no-service-account --no-scopes`, `block-project-ssh-keys=TRUE`, no data disk,
   Secure Boot, boot disk from the custom image, `--max-run-duration` + `--instance-termination-action=DELETE`.
3. VPC firewall: egress DENY `0.0.0.0/0` and `::/0` priority 1000; ingress allow tcp:22 from `35.235.240.0/20` only.
4. Metadata server is exempt from VPC rules (Google doc), so: (a) no service account exists to steal (ST-1.6);
   (b) `hostfw.nft` in the image sets the OUTPUT policy to DROP and allows only loopback, established replies, DHCP renewal
   on udp/67, and uid 0 to 169.254.169.254 / fd20:ce::254 (the guest agent). Non-root uids cannot reach the metadata
   server or resolve DNS (ST-1.2, ST-1.4). Input is policy drop except IAP range on tcp/22. (c) every sandbox runs
   `--network none`, so there is no network namespace path at all (ST-2.x).
5. The image never pulls: all four toolchain images and all wheels are inside the custom image.
6. IAP-tunnelled scp in, results out; no bucket, no registry.
7. Re-image per batch: delete and recreate from the same image; a batch is at most 5000 executions or 3600 s
   (`cli.py`); every batch manifest records image id, runsc version line and kernel release.

Per execution (`dockercmd.py`, one container per run, never reused):
`docker run --runtime runsc --network none --ipc none --hostname od-sbx --read-only --cap-drop ALL --security-opt no-new-privileges
--pids-limit 256 --memory 1g --memory-swap 1g --cpus 1 --ulimit nofile=256 --ulimit fsize=67108864 --ulimit core=0
--user 65534:65534 --tmpfs /work:rw,exec,nosuid,nodev,size=256m,uid=65534,gid=65534,mode=0700
--mount bind /in (ro) --mount bind /out (rw, owned by 65534) --pull never --log-driver none --stop-timeout 0`, env `TMPDIR=/work/.tmp` (S1, F-GO1: a fresh
directory made by the run prelude `cp -R /in/. /work/ && mkdir /work/.tmp`; the name `.tmp` is executor-owned: a patch or overlay key under it makes the row unstageable, i.e. REJECTED and counted, never run),
image by id; 10 s wall clock (60 s for suites) enforced by `docker kill` from the executor; stdout and stderr capped at
64 KB each while the full stream is still hashed; exit code and signal recorded (OOM read from `docker inspect`);
2 runs per execution, 3 for will-this-test-fail rows; an exit-code or stdout-hash mismatch drops the row and increments
a manifest counter (never silent).

"Rootless" (task wording): interpreted as an unprivileged WORKLOAD (uid 65534, no capabilities, no_new_privs, read-only
root, no setuid reachable) plus an EMPTY docker group so no human or agent account holds docker.sock; the dockerd and
runsc supervisor remain root by design per research C6 (rootless podman-in-gVisor is an open gVisor issue and adds no
protection the disposable VM does not already give). If Opus wants a rootless daemon anyway, the fallback is rootless
podman with crun (plan fallback 2), which then replaces `dockercmd.py` only.

Verdict integrity (`verdict.py`, `runner.sanitize`): computed outside the container from exit code + a report read
back after the run + the EXPECTED id set from a collect-only run of the PRISTINE hidden suite in a fresh container.
The executor deletes `conftest.py`, `pytest.ini`, `tox.ini`, `setup.cfg`, `pyproject.toml`, `sitecustomize.py`,
`usercustomize.py`, `*.pth`, `go.work`, `.npmrc`, `package.json` from a patch tree before a verdict run; the hidden suite
is copied in afterwards from the pristine copy. Reports with a DOCTYPE/ENTITY, duplicate ids, missing ids or extra ids are
TAMPERED; no report is NO_REPORT; exit 0 with a failed testcase is TAMPERED.

## 7. Executor self-test list (the Sonnet skeptic reviews EXACTLY this list; code in `executor/od_sbx/selftest.py`, fixtures in `fixtures.py`)

Run at every VM start by `od-sbx-selftest.service`; `run-batch` refuses unless `selftest.json` says PASS for the current
manifest hash. Any failure aborts the batch. `i` = informational. Rule: a "must be blocked" check passes only on a specific signal
(marker printed by the probe, named exit code); a probe that crashed or printed nothing FAILS. `run-batch` also re-runs ST-1.5, ST-1.6,
ST-1.7 and the stage-tmpfs check at batch start (`selftest.host_guards`). `executor/tests/test_sandbox_static.py` asserts that this table
and `selftest.CHECKS` list the same ids.

| ID | Check | Expected |
|---|---|---|
| ST-1.1 | host: TCP to a public IP (1.1.1.1:443) | curl rc 6, 7 or 28 (a missing curl, rc 127, FAILS) |
| ST-1.2 | host: curl the metadata server as uid 65534 | curl rc 6, 7 or 28 |
| ST-1.3 | host: metadata as root | succeeds (guest agent path) and the instance name starts `od-sbx` |
| ST-1.4 | host: DNS lookup as uid 65534 | `getent` rc 2 (lookup failed; 126/127 FAILS) |
| ST-1.5 | host: `nft list chain inet od_sbx output` | contains `policy drop` |
| ST-1.6 | host: metadata `service-accounts/` | HTTP 200 with an empty body, or 404 |
| ST-1.7 | host: docker group members | none |
| ST-2.1 to 2.4 | container: TCP 1.1.1.1:443; TCP 169.254.169.254:80; UDP DNS to 8.8.8.8:53; unix socket `/var/run/docker.sock` | all refused: the probe prints `BLOCKED <errno>` itself (a crashed probe FAILS) |
| ST-2.5 | container: `socket.if_nameindex()` | exactly `IFACES lo` (empty or crashed FAILS, S2) |
| ST-3.1 to 3.3 | container: write outside /work; write /proc/sys; write /in | all refused (`BLOCKED <errno>` printed by the probe) |
| ST-3.4 | container: mount | libc returns -1 (`MOUNT_RC -1 <errno>`) |
| ST-3.5i | container: ptrace(ATTACH) of an own forked child | recorded only. The old probe attached to PID 1, which is the probe itself (the command is exec'd as init), so it was always EPERM and proved nothing; gVisor implements in-sandbox ptrace, so success is plausible and harmless |
| ST-3.6 | container: unshare | refused (`BLOCKED`) |
| ST-3.7 | container: ids and capabilities | uid/gid 65534, CapEff 0, NoNewPrivs 1 |
| ST-3.8 | container: write /work and /out | succeeds (control) |
| ST-4.1 | fork bomb | stops at pids limit or timeout; `docker info` answers; no leftover container |
| ST-4.2 | memory bomb | OOM-killed; host responsive |
| ST-4.3 | disk fill | stops at the tmpfs size (`DISK_STOPPED True`; any other kill does not count) |
| ST-4.4 | infinite loop | TIMEOUT, killed from outside within timeout + grace + 5 s |
| ST-4.5 | 1 GB stdout | kept exactly 64 KB, `truncated` set |
| ST-4.6 | one 80 MB file | cannot be written (`FSIZE_STOPPED`, fsize limit) |
| ST-4.7 | `/out` fill with 63 MiB files; `findmnt -T /srv/od-sbx/stage` | stops at ENOSPC (512 MiB tmpfs cap, M4; see 10.3); stage dir is a tmpfs mount; host responsive |
| ST-5.0 | control: correct patch + hidden suite | PASS |
| ST-5.1 | patch calls `os._exit(0)` at import | not PASS |
| ST-5.2 | conftest forcing outcomes and exit status | stripped; wrong patch is FAIL |
| ST-5.3 | `__eq__` overload | visible suite PASS, pristine hidden suite in a fresh container FAIL |
| ST-5.4 | forged JUnit naming only some ids, exit 0 | TAMPERED or NO_REPORT |
| ST-5.5i | forged JUnit naming exactly the hidden ids (KNOWN GAP probe) | recorded only |
| ST-5.6 | wrong patch + shadow modules (`pytest.py`, `_pytest/`, user-site `pluggy`) forging the exact ids | stripped, real pytest runs, verdict FAIL (S3) |
| ST-6.1 to 6.4 | deterministic fixture on python, node, go, sh, run twice | identical exit and stdout hash, exit 0, and the stdout shows the temp dir `/work/.tmp` (F-GO1) |
| ST-6.5 | nondeterministic fixture | detected, dropped, counter incremented |
| ST-6.6 | vendored `go test` with `t.TempDir()` as a suite | exit 0 inside the 60 s suite limit on the pre-warmed cache (M3) |
| ST-7.1 | four image ids vs manifest | equal |
| ST-7.2 | `runsc --version` line vs manifest | equal |
| ST-7.3 | `python -V`, `pytest --version`, `node -v`, `go version`, bash version vs pins | equal |
| ST-7.4 | executor `.py` tree hash vs manifest | equal |
| ST-7.5 | workload sees a gVisor kernel (`/proc/version` differs from host kernel) | true |
| ST-7.6 | `docker info` storage driver vs manifest | equal (`overlay2`, classic store, F-3) |

## 8. Image creation and the two instances (DONE for the image `od-sbx-base-20261018-r2` and od-sbx1, see BUILD_RECORD.md sections 2, 8 and 8.1; od-sbx-s is NOT created: SIGNOFF_OPUS.md section 3 lists what it needs)

After `60_finalize_image.sh` powers the build VM off (from the Mac):

    gcloud compute images create od-sbx-base-<YYYYMMDD> --source-disk od-sbx-build --source-disk-zone us-east4-c \
      --family od-sbx-base --labels purpose=c21-sandbox
    # check the image carries UEFI_COMPATIBLE (needed for Secure Boot); it should inherit from the Ubuntu disk.

Sandbox VPC and instance (flag names confirmed present in `gcloud compute instances create --help`: `--max-run-duration`,
`--instance-termination-action` accepts DELETE and STOP, `--no-address`, `--no-service-account`, `--shielded-secure-boot`):

    gcloud compute networks create sbx-vpc --subnet-mode=custom
    gcloud compute networks subnets create sbx-subnet --network sbx-vpc --region us-east4 --range 10.200.0.0/24 \
      --no-enable-private-ip-google-access
    gcloud compute firewall-rules create sbx-egress-deny-v4 --network sbx-vpc --direction EGRESS --priority 1000 --action DENY --rules all --destination-ranges 0.0.0.0/0
    gcloud compute firewall-rules create sbx-egress-deny-v6 --network sbx-vpc --direction EGRESS --priority 1000 --action DENY --rules all --destination-ranges ::/0
    gcloud compute firewall-rules create sbx-ingress-iap --network sbx-vpc --direction INGRESS --priority 1000 --action ALLOW --rules tcp:22 --source-ranges 35.235.240.0/20
    gcloud compute instances create od-sbx1 --zone us-east4-c --machine-type n2-standard-4 --image od-sbx-base-20261018-r2 \
      --subnet sbx-subnet --no-address --no-service-account --no-scopes --shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring \
      --metadata block-project-ssh-keys=TRUE,enable-oslogin=TRUE --labels purpose=c21-sandbox --tags od-sbx,od-sbx1 \
      --max-run-duration=1h30m --instance-termination-action=DELETE
    # (the command above is the one actually run for r2; the first version of this recipe had no enable-oslogin, integrity monitoring or tags)
    # od-sbx-s: same image, same VPC, own instance, own sealed layer later (plan section 3/8); not created by this lane.

C2 (Opus sign-off, SIGNOFF_OPUS.md): sandbox VMs are created from the image NAME, `--image od-sbx-base-20261018-r2`, NEVER from `--image-family od-sbx-base`
(a family follows its newest image, so a later image would be picked up without a self-test or sign-off), and never from the DEPRECATED `od-sbx-base-20261018`
(44/46, Go broken). Run batches only on a boot whose own self-test is PASS for manifest `29474351...`; start the batch soon after boot (the 1h30m DELETE timer runs
beside the 3600 s batch cap) and copy results out before the VM deletes itself.

Data in/out: `gcloud compute scp --tunnel-through-iap <batch.tar.zst> od-sbx1:` and results back the same way; if the flag
misbehaves, fallback is `gcloud compute ssh --tunnel-through-iap od-sbx1 --command 'cat > ...' < file`.
Open: a custom-mode VPC needs the IAP API enabled and the IAP-tunnel IAM role for the user (UNVERIFIED in this project).

## 9. Open questions and known gaps for the skeptic

1. Forged report with the exact hidden ids (ST-5.5i). CLOSED AS A DECISION (Opus ruling in 10.1, 18 Oct): the per-run id nonce does not help
   (code under test runs in the same process and uid as pytest), so ST-5.5i stays informational and the T56 labelling rules in 10.1
   (pristine hidden suite in a fresh container + clean static lint; tamper rows labelled by generator intent) are what protects labels.
2. `go run .` with `GOFLAGS=-mod=vendor` and a module with zero dependencies: the fixture ships an empty
   `vendor/modules.txt`; whether Go accepts that is untested. First self-test run decides; adjust the fixture, not the pin.
3. `NoNewPrivs` and `CapEff` lines under gVisor's `/proc/self/status` may differ in format from Linux; ST-3.7 is
   string-matched and may need one adjustment on first run.
4. DHCP renewal: allowed on udp/67 to the metadata address (any uid). A re-image per hour makes lease expiry moot; kept
   so a longer debug session does not lose its address.
5. chrony/NTP is blocked for non-root by the metadata drop; the GCE host clock keeps the VM in sync for a batch this short.
6. `runsc` `--platform=systrap` on kernel `7.0.0-1014-gcp` is untested (nothing run today). Fallback order if it fails:
   `--platform=ptrace` (slower), nsjail in the same VM, rootless podman with crun (plan section 8), Firecracker only on a
   nested-virt machine type.
7. SWE-smith under runsc for P1 is a separate test (LANE_L-0 day 2-4), not part of this image gate.
8. `--log-driver none` with an attached `docker run`: believed to keep stdout/stderr streaming; ST-4.5 and every
   ST-2/3 check would expose a failure immediately.
9. The default network on `system-one-509903` has `default-allow-ssh` from the whole internet on tcp/22 (pre-existing; also
   covers od-l4b and od-cpu1). Not changed here; flagged to the orchestrator.
10. Docker Hub and PyPI are the only third parties besides gVisor/Ubuntu/python.org; all are pinned by digest or hash.
    Index digests could in principle be re-pointed upstream; the pin protects against that (pull fails on mismatch).

## 10. Review and sign-off (blank until done)

- [ ] Sonnet skeptic (fresh): re-observed every pin in section 2; read all `build/*.sh`, `host/*`, `images/*`; reviewed the
      section 7 list against `selftest.py` line by line. Findings: ______
- [x] Opus sign-off on the recipe (before the image build): SIGNED Sun 18 Oct 2026 (Opus, second pass), `PINS_STATUS=FROZEN`.
      Reasons (detail in 10.4): every isolation property holds in the files (no egress at VPC, host nftables and container level;
      metadata server for uid 0 only; docker group empty at build, boot and every batch start; workload uid 65534, cap-drop ALL,
      no-new-privileges, read-only root, runsc, image by id; /work and /out size-capped); the executor starts under `python3 -I`
      (launcher tested); M1-M6, S1-S6, F-2/F-3/F-6 and K1-K7 are really in the tree; one dockerd start blocker found and fixed
      at sign-off (O1, `icc`); tests 674 + 30 pass, `bash -n` clean. Decisions: STRIP_MODULES kept as is, ST-3.5i stays
      informational, /out tmpfs 512M. Binding conditions for the build in 10.4.
      Earlier the same day (first pass): NOT SIGNED. Pins are ACCEPTED unchanged
      (including the skeptic's dated suite `20261012`), but the recipe has blocking defects M1-M6 (section 10.1), so
      `PINS_STATUS` stays CANDIDATE: FROZEN unlocks build mode, and a build now would bake a non-starting executor.
      Re-sign path: fix M1-M6 (fold S1-S6 in too, since a later fix means a rebuild) -> fresh Sonnet pass on the diff
      only -> Opus freezes. Note: PINS_SKEPTIC.md covered pins + infra but not "section 7 vs selftest.py line by line";
      that review was done here and found M3, M4, S2, S3.

### 10.1 Opus findings on the recipe (18 Oct 2026)

Must fix before freeze (all are baked into the image):
- M1 (blocker, confirmed locally on Python 3.12): `python3 -I` implies `-E`, so `PYTHONPATH` is ignored. The
  `/opt/od-sbx/bin/od-sbx` wrapper, `od-sbx-selftest.service` and the step-60 `treehash` call all fail with
  "No module named od_sbx". Fix: a root-owned launcher file that does `sys.path.insert(0, "/opt/od-sbx/executor")` and
  calls `od_sbx.cli.main`, run as `python3 -I <launcher>` in all three places.
- M2 (confirmed): in `60_finalize_image.sh`, `--arg x "$(cmd)"` does not trip `set -e`, so a failed command writes an
  empty executor hash, image id or runsc line into the manifest. Fix: assign each value to a variable first and assert it
  is non-empty.
- M3: Go 1.20+ ships no precompiled std. Every run starts with an empty GOCACHE on tmpfs, so `go run`/`go test`
  recompiles runtime/fmt/testing on 1 vCPU under gVisor inside the 10 s / 60 s limits. Expect ST-6.3 and every Go row to
  time out. Fix: pre-warm the std build cache in `Dockerfile.go`, then measure which run-time path works (read-only
  cache, or a seeded copy that fits tmpfs + 1 GB memory). Add a control: a cold vendored `go test` must finish well
  inside 60 s and `go run` inside 10 s.
- M4: `/out` is a bind mount on the 40 GB boot disk with no size cap (the tmpfs caps `/work` only). One 60 s suite run can
  write many 64 MB files and fill the disk mid-batch. Fix: mount `STAGE_ROOT` as a size-capped host tmpfs (a systemd
  .mount unit in the image, e.g. 1 GiB), and add ST-4.7 "/out fill stops at the cap; host responsive".
- M5: the GCE guest agent's default `[Accounts] groups` list includes `docker` (verify on the build VM). The operator's
  account then gets docker.sock at SSH login, after the boot-time ST-1.7 has passed. Fix: write
  `/etc/default/instance_configs.cfg` with `groups = adm,dip,lxd,plugdev,video` in step 10, assert the docker group is
  empty again in step 60, and have `run-batch` re-run ST-1.5/1.6/1.7 at batch start.
- M6: apply the skeptic's F-2 guard (no daemon.json before `dpkg -i`) and F-6 (`nft -c -f` before enabling the unit),
  and record the docker storage driver (F-3) in IMAGE_MANIFEST.json.

Should fix now (cheap; executor and image code, so a later fix means a rebuild):
- S1: `/tmp` is read-only. Go `t.TempDir()` and node `os.tmpdir()` fail. Set `TMPDIR=/work` in BASE_ENV. (SUPERSEDED by F-GO1, section 10.5: `TMPDIR=/work/.tmp`.)
- S2: ST-2.5 accepts empty output, so a crashed probe passes. Use `socket.if_nameindex()` and require `lo` exactly.
- S3: with `python -m pytest`, a patch file `/work/pytest.py` replaces pytest. Run suites as `python -P -m pytest`, strip
  `pytest.py`, `_pytest/`, `pluggy/` and `py.py`, and add ST-5.6 (shadow-module patch is not PASS).
- S4: `parse_junit` checks `<!DOCTYPE` only as UTF-8 bytes, so a UTF-16 report bypasses the check. Reject any report
  that is not strict UTF-8.
- S5: disable unattended-upgrades and apt-daily on the build VM in step 10 (a kernel can change mid-build), and record
  the host python3 version in the manifest.
- S6: add `Wants=network-online.target` to `od-sbx-selftest.service`.

Ruling on open item 9.1 (ST-5.5i): the per-run id nonce does NOT close the gap. Code under test runs in the same process
and uid as pytest, so at run time it can read `test_hidden.py` or inspect the session, then write the exact ids,
whatever they are called. No report format makes in-process results unforgeable, so drop the nonce plan and keep
ST-5.5i informational. T56 labels:
- An executor PASS alone is never a gold label.
- An "honest" row needs PASS on the pristine hidden suite in a fresh container AND a clean static lint (no exit at
  import, no write to `/out`, no read of test files, no tampering with sys.modules, gc, inspect, frames, ctypes or
  builtins, no always-true `__eq__`).
- A "tamper" row takes its label from the generator's declared intent, confirmed by not-PASS or a lint hit.
- Any disagreement drops the row and is counted. Wire this before T56 rows run (gate 4).

Not blocking: F-4/F-5 access path (with project keys blocked, gcloud writes instance-level ssh-keys, so login likely
works; IAP is checked on first boot). The runner is serial (about 1 run/s), so the 3600 s cap, not 5000 executions, will
end a batch. `default-allow-ssh`/`-rdp` on `default` stays with the orchestrator. `requirements.lock` must come from VM
`resolve` and match PINS_SKEPTIC.md section 1 exactly (name, version, sha256) before it is written.
### 10.2 Sonnet skeptic pass on the 10.1 fixes (Sun 18 Oct 2026, fresh Sonnet; read-only on the VM side: nothing was run anywhere)

Finding zero: when this pass started NONE of M1-M6, S1-S6, F-2, F-3, F-6 was in the tree (every build script, unit and executor file still had
its 17 Oct 23:0x timestamp, older than section 10.1). This pass therefore APPLIED them, so section 10.1 is now implemented but has had no
independent second read; it needs the "fresh Sonnet pass on the diff only" that 10.1 asks for, then Opus freezes. Original files are in the
session scratchpad (`sandbox_orig`) for diffing. Tests: `executor/tests/test_sandbox_static.py` (22 tests, Mac only, no container; also runs the
rest of c21_infra: 674 passed).

| Item | State | Where |
|---|---|---|
| M1 launcher | fixed; test proves `python3 -I -m od_sbx` with PYTHONPATH fails and the launcher file works under `-I` | `executor/od_sbx_launcher.py`, steps 50/60, `od-sbx-selftest.service` |
| M2 empty manifest values | fixed: assign, `need`, jq empty-string guard | step 60, `common.sh` |
| M3 Go std cache | pre-warm + seeded copy implemented; UNMEASURED (seed size, copy time, 512m tmpfs vs 1g memory). Also removed `GOTMPDIR` (go fails if the dir does not exist) | `Dockerfile.go`, `images/gowarm`, `config.SEEDS/TMPFS_WORK`, ST-6.6 |
| M4 /out cap | 1 GiB tmpfs via fstab (now 512 MiB, see 10.3) (`nofail`), ST-4.7, mount re-check at batch start | step 50, selftest |
| M5 docker group | agent `groups` override, removal of existing members, asserts in 10, 60 and at every `run-batch` | steps 10, 60, `selftest.host_guards` |
| M6 / F-2 / F-3 / F-6 | daemon.json guard before `dpkg -i`; classic overlay2 store pinned (minimal daemon.json written after runsc in step 30, full file in 50), driver recorded and ST-7.6; `nft -c` in 50 and 60 | steps 20, 30, 50, 60, `host/docker-daemon.json` |
| S1 TMPDIR | fixed (env + all four Dockerfiles; fixtures print/use the temp dir). Value `/work` broke every Go row at first boot; now `/work/.tmp`, see 10.5 | `config.BASE_ENV` |
| S2 ST-2.5 | fixed (`if_nameindex`, exactly `lo`) and generalised: every "must be blocked" probe now needs its own BLOCKED marker | `fixtures.py`, `selftest.py` |
| S3 shadow modules | `python -s -P`, `PYTHONNOUSERSITE=1`, strip list, ST-5.6; `cli` rejects python suite jobs without `-s -P` | `config.STRIP_*`, `runner.sanitize_report` |
| S4 report encoding | fixed: NUL bytes, UTF-16/32 BOM, non-utf-8 declaration, strict decode (UTF-16 ASCII text is *valid* UTF-8 with NULs, so a decode alone would not have worked) | `verdict._strict_utf8_text` |
| S5 apt/unattended-upgrades | masked in step 10; host python3 version in manifest; step 60 asserts newest installed kernel == running kernel | steps 10, 60 |
| S6 network-online | fixed (also stale `selftest.json` removed at start; timeout 900 s) | `od-sbx-selftest.service` |

New problems found by this pass (all fixed unless marked OPEN):
- N1 `30_fetch_toolchains.sh` compared `RepoDigests[0]` to `docker.io/library/python@sha256:..`; docker stores `python@sha256:..`, so the first build would die. Now compares the digest part against all entries.
- N2 ST-3.5 was vacuous (it attached to PID 1 = the probe itself; always EPERM). Now ST-3.5i, informational, probes an own child. DECISION FOR OPUS: gVisor allows in-sandbox ptrace, so a hard "ptrace fails" expectation would be wrong or meaningless.
- N3 Many ST-1/2/3/4 checks passed on a crashed probe or a missing tool (ST-1.1/1.2 any nonzero rc, ST-1.4, ST-2.x, ST-3.x, ST-4.3 accepted any SIGNALED, ST-4.6 accepted no output). Now fail-closed (specific rc or marker). ST-1.6 also read a 404 page as non-empty; now reads the HTTP code.
- N4 The hidden suite was merged into the patch tree BEFORE sanitizing (stripping the suite's own conftest/package.json/go.work and not guaranteeing that the suite wins over a patch file of the same name). Now `overlay=` copies the pristine suite after sanitizing; jobs carry `suite_files`. Stripped paths are recorded per run and counted.
- N5 Container names built from row ids could be invalid for docker; now sanitised. Leftover containers from an aborted batch would collide on names; `run-batch` and `cleanup` remove them. `cleanup` no longer `rm -rf`s the tmpfs mount point.
- N6 User site: with HOME=/work, `/work/.local/lib/python3.12/site-packages` is searched BEFORE site-packages; the strip list alone would not have stopped a patch from shadowing pytest (fixed by `PYTHONNOUSERSITE=1` + `-s`).
- N7 `ENTRYPOINT docker-entrypoint.sh` of the node image sat in front of the executor's `sh -c`; reset. The gVisor apt key check read only the first `fpr` line; now exactly one primary key is required. `docker info | grep -q` under `pipefail` could SIGPIPE; replaced with a variable. Added: runsc smoke run in step 50 (the image's own python on a literal, before the image is baked), `--hostname od-sbx` for determinism, DHCP reply allowed on the input chain (source-pinned) because the policy drop could eat a broadcast lease reply.
- OPEN (not fixed, not blocking): F-4/F-5 access path (OS Login, IAP API not enabled) and `default-allow-ssh/rdp` as already noted; the image carries the build VM's sshd host keys into od-sbx1 and od-sbx-s (not removed because an image without host keys that the guest agent does not regenerate would lock the operator out; check on first boot); `pip uninstall ... || true` in `Dockerfile.python` hides a failure (pip would stay in the image; no network, so low); the first-boot DHCP path under `hostfw.nft` and `runsc --platform=systrap` on kernel 7.0 are only testable on the VM (the step-50 smoke run covers runsc at build time); the guest-agent default `groups` list and config file name are from documentation, to be confirmed on the build VM before step 10.

### 10.3 Second Sonnet read of the 10.2 changes (Sun 18 Oct 2026, fresh Sonnet "skeptic 2"; nothing was run on any VM, no docker, no model API)

Method: diffed every file under `sandbox/` against the pre-10.2 originals, checked each change against 10.1 (M1-M6, S1-S6) and
PINS_SKEPTIC.md (F-2, F-3, F-6), read the full executor/build code (not only the diff), and tried to break the strip/overlay logic with
hostile tree keys (reproduced locally, no container). Result: every 10.1 item is really implemented; no change loosened egress, the
metadata rule (still uid 0 only), the docker group (stricter), rootless/uid 65534, cap-drop/no-new-privs, `--network none`, runsc, or the /work
tmpfs flags. The only looser knob is the Go `/work` tmpfs (512m, needed for the seed) and the new narrow input rule for DHCP replies
(`ip saddr 169.254.169.254 udp sport 67 udp dport 68`). Problems found in the 10.2 work (all fixed here, tests added, 29 static tests + 674 others pass):

- K1 (real, reproduced): the strip rules judged the RAW key. `conftest.py/x/..` has the textual name `..` (no rule matched) but `stage()` resolves
  it to the file `conftest.py`; the same for `package.json/x/..`, `go.work/...`, `pytest.py/x/..`. That bypassed S3 and T56-3. Now every key is
  normalised (`runner.norm_key`, posix normpath; absolute, `..` and NUL keys are rejected with `StageError`) before sanitizing, overlaying and staging.
- K2 (real, reproduced): "the suite always wins" was false for alias spellings: `./test_hidden.py` was written AFTER the suite's entry and won; a patch file
  `test_hidden.py/x` or a file where the suite needs a directory made `stage()` raise and aborted the whole batch. `_drop_overlay_conflicts` removes
  aliases and file/dir clashes (recorded in `stripped`), and `run-batch` now rejects an unstageable row (`rejected_unstageable_tree` counter) and continues.
- K3: a run dir leaked onto the new tmpfs whenever `run_once` or `stage` raised (an exception path now costs capacity, M4). Removed in `finally`.
- K4: the stage cap equalled the container memory limit (both 1 GiB). Bytes written through a bind mount of a host tmpfs are charged to the container's
  memory cgroup, so ENOSPC could not be reached before an OOM kill and ST-4.7 would likely fail on its first run (a later fix = rebuild). Cap is now
  512 MiB (`/in` is bounded by the 256m `/work` copy anyway). This is reasoning, not a measurement; Opus may revert the single `size=` token in step 50.
- K5: `ensure_classic_store` wrote `/etc/docker/daemon.json` without making `/etc/docker` (Docker >= 23 no longer creates `key.json`, so the directory may not exist).
- K6: for Go suites `.gocache` and `.gopath` (executor-owned, seeded) are no longer taken from the patch.
- K7: `c21_infra/pytest.ini` testpaths now include `sandbox/executor/tests`, so a plain `pytest` there runs the static tests.

Still OPEN (unchanged, need the VM): Go seed size, copy time and memory (512m tmpfs + seed + compiler + sentry inside 1g; ST-6.3/ST-6.6 decide), guest-agent
`groups` file name and default list, `nft -c` result for `hostfw.nft`, the first-boot DHCP path under the firewall, runsc systrap on kernel 7.0, whether
`findmnt` prints the tmpfs SIZE (only FSTYPE/TARGET are checked at batch start; the cap itself is proven by ST-4.7), ssh host keys carried into od-sbx1/od-sbx-s,
`pip uninstall ... || true`. Note for L-C: `STRIP_MODULES` removes any path component named `py`, `packaging`, `pygments`, `pluggy`, `iniconfig`, `pytest`, `_pytest`
from python verdict runs; rows built from real repos with such a directory will be stripped (recorded in `stripped`, counted) and then FAIL or be dropped.

### 10.4 Opus sign-off, second pass (Sun 18 Oct 2026): SIGNED, pins FROZEN

Read in full: this file, `pins.env`, PINS_SKEPTIC.md, every `build/*.sh` (+ `lock_from_pip_hash.py`), `host/*`, `images/*` (Dockerfiles,
gowarm, trusted ini, allow-list) and every executor module. Ran: `bash -n` on all scripts (clean); `c21_infra/tests` 674 passed;
`sandbox/executor/tests` 30 passed (29 + the O1 test below); strip/overlay rules probed locally with hostile keys (pure functions,
no container). Nothing was run on a VM, no docker, no Modal, no model API.

Isolation, checked against the files: (1) egress: sbx-vpc deny v4+v6 at 1000, no external IP/NAT/PGA; `hostfw.nft` output policy
drop (only lo, established, DHCP from port 68 which non-root cannot bind, and uid 0 to the metadata address); every run `--network
none` plus runsc `--network=none`; extra nft tables cannot loosen this (a drop in any base chain is final). (2) Metadata: uid 0 only,
no service account (ST-1.2/1.3/1.6). (3) docker group: emptied in step 10, asserted in 10 and 60, ST-1.7 at boot, re-checked by
`run-batch`. (4) Workload: uid 65534, cap-drop ALL, no-new-privileges (per run and daemon default), read-only root (docker's
hosts/resolv files are ro too), `--ipc none` (no /dev/shm), pids/memory/cpu/nofile/fsize/core limits. (5) runsc: default runtime
and explicit `--runtime runsc`, image by id, `--pull never`, smoke run in step 50, ST-7.5. (6) Writable space: /work tmpfs
256m (go 512m), /out on the 512M stage tmpfs, no host-disk path (log driver none, ro root). (7) Executor: launcher works under
`-I` (tested), runs nothing generated on the host, parses reports only after the container is removed, rejects DTDs and non-UTF-8.

- O1 (start blocker, FIXED at sign-off): `host/docker-daemon.json` had `"iptables": false` together with `"icc": false`; dockerd
  rejects that pair ("ICC=false uses iptables to function") and would not have restarted in step 50. ICC is moot here (bridge none,
  every run `--network none`), so the key was removed; nothing is loosened. Guard: `test_daemon_json_can_start_dockerd_and_keeps_the_isolation_keys`.

Decisions on the 10.3 open questions:
- STRIP_MODULES: KEEP as is (any path component or `X.py`, python verdict runs only). pytest's prepend import mode puts the basedir
  of each pristine test file on sys.path and that basedir can be at any depth, so a top-level-only rule would be unsound; the seven
  names are pytest 9.1.1's own import closure on 3.12. Do NOT widen it to stdlib names (the in-process gap of 10.1 makes that
  moot; the lint is the control). Binding for L-C / T56 labelling: (a) a row that is not a declared tamper row and whose verdict
  run has ANY `stripped` entry is DROPPED and counted, never labelled FAIL (stripping changed the code under test); (b) repos that
  are, or vendor, pytest/_pytest/py/pluggy/iniconfig/packaging/pygments are out of scope for python verdict rows on this image
  (P1 needs its own design); (c) a repo's test-support files (conftest.py, test-dir `__init__.py`, pytest/tox/setup.cfg/pyproject
  config, node `package.json`, go `go.mod` and `vendor/`) travel in `suite_files` (pristine), never in `files`; (d) the T56 static
  lint also rejects binary/non-UTF-8 patch files (a `pygments.*.so` is NOT caught by the strip rule), patch files named like a
  stdlib top-level module, and Go `TestMain`/patch `*_test.go`.
- ST-3.5i: stays INFORMATIONAL. Inside gVisor, ptrace is the sentry's emulation on sentry-managed tasks; a uid-65534 task with no
  capabilities can at most trace its own descendants in its own PID namespace, which gives nothing that in-process code does not
  already have. A hard "must fail" would fail a correct sandbox. The guards that matter are ST-3.4/3.6/3.7/7.5 and ST-2.x. The
  recorded result is read at the post-build sign-off; anything beyond the own child (e.g. a PID outside its tree) reopens it.
- /out stage tmpfs: 512M (not 1G). Under memcg, tmpfs pages are charged to the writer's cgroup; if gVisor's writes land in the
  container cgroup, a 1G cap behind a 1g memory limit is reached only after an OOM kill, so ST-4.7 could not pass. 512M passes
  whether or not the charge happens, and is far above legit use (reports read back at most 8 MiB; /in is bounded by /work).

Binding conditions of this sign-off:
1. Build order: 00 -> 10 build -> 20 build -> 30 resolve -> compare -> 30 build -> 40 -> 50 -> 60 (30 resolve needs docker, so the
   lock is written after the freeze). `vendor/requirements.proposed.txt` must equal PINS_SKEPTIC.md section 1 exactly (5 lines:
   pytest 9.1.1, pluggy 1.7.0, iniconfig 2.3.1, packaging 26.3, pygments 2.21.0, same sha256). Any difference: stop, do not edit pins.
2. Any edit to `pins.env` after this point sets CANDIDATE again and needs a new Opus sign-off. Executor/fixture edits before step 50
   are allowed only if listed in the post-build sign-off, which reviews the built tree hash and the self-test log.
3. The "Opus sign-off before first execution" below is still required; this sign-off covers the BUILD only.

Not blocking (fold into the first rebuild if the self-test needs one; all fail closed today):
- R1: ST-3.7 matches `NoNewPrivs:\t1` in /proc/self/status; gVisor may not print that line (open item 3). Read it with
  `prctl(PR_GET_NO_NEW_PRIVS)` instead (and keep CapEff from /proc).
- R2: `stage()` turns only clash errors into StageError; ENOSPC/ENAMETOOLONG on a huge or odd tree aborts the batch instead of
  rejecting one row.
- R3: add `RequiresMountsFor=/srv/od-sbx/stage` to `od-sbx-selftest.service` (a `nofail` mount is not ordered before local-fs.target;
  `run-batch` re-checks the mount, so this is ordering hygiene only).
- R4: `read_back` refuses a symlinked final component only; keep job `report` a bare file name (or reject `/` in cli).
- R5: replace `pip uninstall ... || true` with an assert that pip is gone.
- Residual, fails loudly at build time: `DOCKER_BUILDKIT=0` needs the legacy builder in docker.io 29.1.3; if it is gone, install the
  pinned Ubuntu `docker-buildx` and build with BuildKit `--network=none` (rebuild, no pin change to the toolchains).

- [x] Image built; self-test PASS on od-sbx1 (log attached): REBUILT 18 Oct with the 10.5 fix as `od-sbx-base-20261018-r2` (family `od-sbx-base`); self-test on od-sbx1 PASS 46/46
      (`SELFTEST_od-sbx1_20261018_r2.json`; manifest sha256 `29474351959951a20815e8e8645b6fa3df0888df6a553f9399ebfc85871d71c8`, executor tree hash `defbb2e49ae9589fc82b2c53d988b70ccedf7e9c0c226d7de38e47ee6eefa753`,
      `rebuild_logs/`, `BUILD_RECORD.md` section 8). The first image `od-sbx-base-20261018` (44/46, ST-6.3 and ST-6.6) is DEPRECATED, not deleted. od-sbx-s NOT created: awaits the Opus sign-off.
- [x] Opus sign-off before first execution of rows: SIGNED Sun 18 Oct 2026 15:44 EDT for image `od-sbx-base-20261018-r2` on od-sbx1, with conditions C1 to C6: see `SIGNOFF_OPUS.md`
      (C1 evidence in BUILD_RECORD.md section 8.1, open items N1 to N7 in section 9, the C3 pytest/go/node timing assessment in section 10). It does NOT cover sealed data or od-sbx-s (its section 3).

### 10.5 First-boot finding F-GO1 and APPLIED fix (r2) (Sun 18 Oct 2026, builder; skeptic pass 1 NOT SOUND (D1, D1b), pass 2 SOUND, reports in SKEPTIC_F-GO1_pass1.md and SKEPTIC_F-GO1_pass2.md; rebuilt as `od-sbx-base-20261018-r2`, self-test 46/46; Opus SIGNED, SIGNOFF_OPUS.md)

Finding. The first self-test of `od-sbx-base-20261018` on od-sbx1 failed ST-6.3 (`go run .` x2) and ST-6.6 (vendored `go test`) with
`go: go.mod file not found in current directory or any parent directory` and `pattern ./...: directory prefix . does not contain main module`.
44 of 46 checks passed (everything else, including all isolation and verdict checks). Cause, CONFIRMED three ways:
1. Files: `config.BASE_ENV["TMPDIR"] == "/work"` (S1) and the Go fixtures put `go.mod` at the `/work` root (cwd of every run).
2. Go source in the od-sbx go image (`/usr/local/go/src/cmd/go/internal/modload/init.go:541-547`, go1.26.9): `else if search.InDir(modRoot, os.TempDir()) == "." {`
   then `fmt.Fprintf(os.Stderr, "go: warning: ignoring go.mod in system temp root %v\n", os.TempDir())` and the module root is discarded (golang.org/issue/26708).
3. One cheap test on od-sbx1 (18:36Z, one container with the executor's flags: runsc, `--network none`, read-only root, cap-drop ALL, uid 65534, 512m /work
   tmpfs, seeded GOCACHE; the same fixture layout, literal programs only). `TMPDIR=/work`: `go env GOMOD` = `/dev/null`, `go run` prints the warning then
   `go.mod file not found`, `go test ./...` prints the warning then `directory prefix . does not contain main module` (the exact ST-6.3 / ST-6.6 messages).
   `TMPDIR=/work/.tmp` (directory created beforehand): `GOMOD=/work/go.mod`, `go run` prints `3 ok /work/.tmp`, `go test -count=1 ./...` passes with
   `t.TempDir()` in 2 s on the seeded cache (so M3's seed + 512m tmpfs + 1g memory works for this fixture), and the empty `vendor/modules.txt` is accepted
   (closes open item 9.2). Script and output: `F-GO1_test_on_od-sbx1.sh` / `F-GO1_test_on_od-sbx1.out` in this directory.

Change (applied in r2; smallest, uniform for ALL toolchains; the recipe forbids none of it):
- `config.WORK_TMP = "/work/.tmp"`; `BASE_ENV["TMPDIR"] = WORK_TMP`; `config.RESERVED_TOP = {".tmp"}`.
- `dockercmd.build_run_argv` prelude: `cp -R /in/. /work/ && mkdir /work/.tmp [&& go seed copy] && exec "$@"`. The directory is created fresh in every container,
  before the command, by the executor.
- `runner._reject_reserved` (called in `run_once` right after `norm_key`, before sanitize/overlay/stage; skeptic finding D1, revision 2): a patch OR overlay key whose first
  path component is `.tmp` raises `StageError`, for kind `run` AND `suite`, every toolchain. `cli.run_batch` turns that into `{"row_id", "rejected": ...}` plus the counter
  `rejected_unstageable_tree`, no execution is counted, the batch goes on: the row is DROPPED for both kinds, never run on an altered tree. (Revision 1 stripped the entries and
  recorded them in `stripped`; that was only enforceable for suite rows by 10.4 rule (a), and `cli` merely counted it for run rows. Removed, with its tests.) Keys are already
  normalised (K1), so `./.tmp/x` and `a/../.tmp` are caught; `a/.tmp/x`, `.tmpx` and `tmp/y` are not top level and pass untouched.
  The same function also folds in the executor-owned Go names `.gocache` / `.gopath` (config.STRIP_GO_TOP_DIRS): a Go run-row PATCH and any Go OVERLAY with such a top-level key are
  rejected the same way. A Go SUITE patch keeps the K6 behaviour of 10.3 (stripped by `sanitize_report`, recorded in `stripped`, then 10.4 rule (a) drops the honest row), because
  K6 is signed off and because a declared tamper row that ships a poisoned cache can then still be executed and labelled by intent; both ends are "the cache is never taken from the patch".
- `selftest.st6`: ST-6.1 to 6.4 additionally require that the LAST stdout line equals `/work/.tmp` EXACTLY (`selftest.last_line`, not a substring match). Every fixture now prints its temp dir
  alone on the last line (python `tempfile.gettempdir()`, node `os.tmpdir()`, go `os.TempDir()`, sh `$TMPDIR`) and creates a file in it where it can (python/node `mkdtemp`, sh `touch "$TMPDIR/x"`;
  go writes via `t.TempDir()` in ST-6.6). No check id is added or removed, so the section 7 table and `selftest.CHECKS` still list the same 46 ids.
- Four Dockerfiles: COMMENT-ONLY edit (the baked `TMPDIR=/work` is stale and always overridden by the executor's `--env`). Image content is unchanged, so no step 40 rerun.
- Tests: `executor/tests/test_sandbox_static.py` 30 -> 37. S1 test rewritten; new: prelude order, reserved `.tmp` key raises `StageError` (4 toolchains x run/suite x patch/overlay x 5 spellings), look-alike names pass,
  Go dirs (run patch and overlay rejected, suite patch stripped, other toolchains and nested names untouched), a load-bearing check (with `_reject_reserved` patched out the same rows reach `stage()`), the REAL
  `cli.run_batch` writes `rejected` + `rejected_unstageable_tree` = 3 for a run row, a suite row and a Go run row, executions = 2 (only the good row), and the exact-last-line self-test check.
  Mutation run (removing the check, limiting it to suite rows, `continue` instead of `raise`, skipping overlays, not rejecting Go run rows): each is caught by 2 or 3 of the new tests.

S1 properties kept: every write stays inside the size-capped `/work` tmpfs (no new mount, same 256m/512m cap), root stays read-only, `--network none`, cap-drop ALL,
no-new-privileges, uid 65534, nothing new on the host. The temp dir is part of the tmpfs, so it counts against the same cap and the same memory limit as before.
Alternatives rejected: (a) TMPDIR only for Go (non-uniform; python/node/sh would keep an untested special case); (b) running Go from `/work/src` (changes the cwd and
path contract for every Go row and the `argv` the generators emit); (c) `GOTMPDIR` (does not move `os.TempDir()`, the check is on `os.TempDir()`); (d) changing the four
Dockerfile ENVs (would need a step 40 rerun and new image ids for no runtime effect).

Consequences for L-C and the T56 lint (the new directory is visible to the code under test):
- EVERY run (all four toolchains, run and suite) now starts with an EMPTY directory `/work/.tmp` next to the sources, and Go rows already had `/work/.gocache` (the ~61 MB seed) and
  `.gopath`. Rows whose behaviour or expected output depends on listing the working directory see it: `ls -A`, `ls -a`, `find .`, `tree`, `du`, `os.listdir('.')`, `os.scandir`,
  `glob('.*')` / `glob('*')` with dotfiles, `Path('.').iterdir()`, `readdir`, `fs.readdirSync('.')`, `filepath.Walk` / `WalkDir`. The label is MEASURED on this image, so the row stays
  self-consistent, but a task statement that says "the directory is empty" or an assertion on an exact listing is then wrong: L-C should not generate such rows (or must filter
  `.tmp` and `.gocache` in the spec and the hidden checks), and the T56 lint should flag directory-listing calls on `.` / cwd in generated code.
- T56 lint additions (extends 10.4 (d)): reject at lint time any patch or suite file whose top-level path component is `.tmp`, and for Go any top-level `.gocache` / `.gopath`. The
  executor rejects them at run time anyway (`rejected_unstageable_tree`), so a lint miss costs a counted dropped row, never a wrong label.
- `os.TempDir()`, `tempfile.gettempdir()`, `os.tmpdir()` and `$TMPDIR` all print `/work/.tmp` now (they printed `/work`); rows that print the temp dir are measured on this image like any other.

Rebuild notes (followed for r2, corrected by the skeptic and Opus; keep for the next rebuild): the executor tree hash changes, so step 50 and 60 rerun (images unchanged, step 40 not needed). The existing `od-sbx-build`
disk is in its scrubbed, post-step-50 state: `od-sbx-hostfw` and `od-sbx-selftest` are ENABLED there, so at its next boot the firewall comes up (output DROP for non-root, SSH only from
the IAP range): reach it with `gcloud compute ssh --tunnel-through-iap od-sbx-build` (untested on the build VM); step 50/60 need no internet. Order:
1. At the first login run `sudo systemctl stop od-sbx-selftest` (it is enabled and has run once at boot against the OLD manifest; it `Requires=docker.service`, so step 50's `systemctl
   restart docker` would otherwise stop/restart it in the middle of the build and start the whole self-test again). Then remove any container it left behind, AS ROOT (the docker
   group is empty, so a plain `docker ps` as the login user shows and removes nothing and the leftovers would be baked into the image, ST-4.1):
   `sudo /opt/od-sbx/bin/od-sbx cleanup` (or `sudo sh -c 'docker ps -aq --filter label=od-sbx=1 | xargs -r docker rm -f -v'`), and check `sudo docker ps -aq | wc -l` prints 0.
2. Copy the first build's logs (`~/buildlogs/*`) back to the Mac, then delete the old tree and artifacts: `sudo rm -rf /home/*/sandbox /home/*/buildlogs /home/*/manifest_copy.json`. Steps 50 and 60 source `${SBX_SRC}/pins.env` (common.sh lines 9-10: `. "${SBX_SRC}/pins.env"`) and step 60 records
   its sha256, so exactly ONE tree may exist and it must be the new one.
3. Copy the new tree to `/tmp`, not to `$HOME`: `gcloud compute scp --recurse --tunnel-through-iap sandbox od-sbx-build:/tmp/` (verify `pins.env` sha256 first) and run
   `sudo env SBX_SRC=/tmp/sandbox bash /tmp/sandbox/build/50_install_executor.sh build`, then the same with `60_finalize_image.sh`. Step 60 scrubs `/tmp/*` and `/var/tmp/*` itself, so
   nothing of the tree or logs is left in the image. Create `/tmp/buildlogs` first, write the logs there and scp the step-50 log back to the Mac before step 60; capture step 60's output from the
   ssh session (it disappears with the scrub). Run step 60 as the LAST command of its ssh session and add nothing after it that writes under `$HOME` (last time a `tee ~/manifest_copy.json` appended to the step 60 command put a file into the image).
4. Before step 60 check `ls -A ~` shows no `sandbox`, `buildlogs` or `manifest_copy.json`.
5. (Opus C6, SIGNOFF_OPUS.md) Right before step 60, as its own earlier command: `sudo systemctl stop od-sbx-hostfw`. With the firewall running on the build VM, step 60's final `systemctl poweroff`
   hangs at `google-shutdown-scripts.service` (the stub resolver runs as a non-root uid and hostfw drops its DNS), as happened for r2 (the image was cut after a forced `instances stop`, ACCEPTED by
   Opus as the image of record). Stopping the unit only flushes the RUNTIME ruleset; it stays ENABLED in the disk, so every instance still boots with the firewall (ST-1.5 checks it). It also removes the
   ~40 s per `sudo` delay. Any edit to `pins.env`, the executor or the host files means a new image, a new self-test and a new Opus sign-off (C6).

## 11. Operating the build VM

    gcloud compute instances start od-sbx-build --zone us-east4-c
    gcloud compute ssh od-sbx-build --zone us-east4-c
    gcloud compute instances stop od-sbx-build --zone us-east4-c        # when idle; leaves the 40 GB disk
    gcloud compute instances delete od-sbx-build --zone us-east4-c      # after the image is created and signed

The 6 hour `--max-run-duration` stops the VM by itself if forgotten. The firewall rule `od-sbx-build-deny-internal` is
deleted together with the VM.

## 12. Names-only list for the manifest (identifiers planned by this lane; names only, no values)

VMs: od-sbx-build, od-sbx1, od-sbx-s. Network objects: sbx-vpc, sbx-subnet, sbx-egress-deny-v4, sbx-egress-deny-v6,
sbx-ingress-iap, od-sbx-build-deny-internal. Images: od-sbx-base (family), od-sbx/python, od-sbx/node, od-sbx/go, od-sbx/sh.
Toolchains/runners: python, node, go, sh; pytest, node:test, go test, unittest (stdlib). Units: od-sbx-hostfw,
od-sbx-selftest. Tables/labels: purpose=c21-sandbox-build, purpose=c21-sandbox. No fake names, no data, no rows.
