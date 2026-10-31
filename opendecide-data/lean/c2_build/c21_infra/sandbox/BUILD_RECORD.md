# od-sbx base image: BUILD RECORD (builder run, Sun 18 Oct 2026)

Built exactly per `IMAGE_RECIPE.md` sections 4-10.4 with the FROZEN `pins.env` (sha256 `d7821319f3d13dc649cba4ef3aa337e333313e7b515b96c6c0c39d99816823fd`, unchanged before and after).
Nothing generated ran anywhere. Only the recipe's own scripts and its fixed self-test programs ran. No Modal, no model API.
Not touched: od-l4b, od-cpu1, od-l4, any C2 file, HANDOFF.md, PREREG_FINAL.md, pins.env, anything named ohs/sealed, ~/.claude.

## 0. Result in one line

IMAGE BUILT (`od-sbx-base-20261018`, READY). Build steps 00 to 60 all passed. Self-test on od-sbx1: **FAIL, 2 of 46 checks (ST-6.3, ST-6.6, both Go)**; 44 pass (incl. every ST-1, ST-2, ST-3, ST-4, ST-5, ST-7). Per the task rule (a failing self-test = STOP, no workaround) **od-sbx-s was NOT created**, no fix was tried, and all VMs are stopped.

## 1. VMs, zones, state at the end of this run

| VM | Zone | Type | State now | Notes |
|---|---|---|---|---|
| od-sbx-build | us-east4-c | e2-standard-2 | TERMINATED | ran 17:46Z to 18:05Z (powered itself off at the end of step 60). Disk (40 GB) kept. Not deleted. |
| od-sbx1 | us-east4-c | n2-standard-4 | TERMINATED (stopped by me) | created 18:08Z from the image, `--max-run-duration=1h30m --instance-termination-action=DELETE` (as in recipe section 8). Disk kept. Internal IP 10.200.0.2, no external IP. |
| od-sbx-s | (none) | | NOT CREATED | stopped at the self-test failure on od-sbx1 (task rule). |

od-sbx1 flags: `--subnet sbx-subnet --no-address --no-service-account --no-scopes --shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --metadata block-project-ssh-keys=TRUE,enable-oslogin=TRUE --labels purpose=c21-sandbox --tags od-sbx,od-sbx1`.
(`enable-oslogin=TRUE` is the F-4 fix and the task asked for it; the network tags `od-sbx`, `od-sbx1` are extra, no rule references them yet. The sbx-vpc rules have no target tag, so they cover every instance in the VPC.)
Other running VMs were untouched: od-cpu1 and od-l4b RUNNING, od-l4 TERMINATED, throughout.

## 2. GCP objects created

| Kind | Name | Detail |
|---|---|---|
| Custom image | **od-sbx-base-20261018** (family `od-sbx-base`, label `purpose=c21-sandbox`) | id 7043273612827604159, READY, archive 2,572,632,768 bytes, disk 40 GB, guestOsFeatures include UEFI_COMPATIBLE, source disk `od-sbx-build` |
| VPC | sbx-vpc | custom mode |
| Subnet | sbx-subnet | us-east4, 10.200.0.0/24, Private Google Access off |
| Firewall | sbx-egress-deny-v4 | EGRESS DENY all 0.0.0.0/0, priority 1000 |
| Firewall | sbx-egress-deny-v6 | EGRESS DENY all ::/0, priority 1000 |
| Firewall | sbx-ingress-iap | INGRESS ALLOW tcp:22 from 35.235.240.0/20, priority 1000 |
| Instance | od-sbx1 | see section 1 |

Pre-existing and unchanged: `od-sbx-build-deny-internal`, the `default` network rules (default-allow-ssh/rdp still open to 0.0.0.0/0, orchestrator item 9.9 in the recipe).
No Cloud NAT, no peering, no VPN, no IAP/API enablement was needed: IAP tunnelling (`--tunnel-through-iap`) and OS Login SSH worked without enabling `iap.googleapis.com` (answers recipe F-5 and F-4).

## 3. Build steps (build VM, Ubuntu 24.04.5 LTS, kernel 7.0.0-1014-gcp; logs on the VM under `~/buildlogs`, also inside the image at /home/aryamahadik/buildlogs)

| Step | Result | Note |
|---|---|---|
| copy-in | OK | `gcloud compute scp --recurse sandbox od-sbx-build:~/`; 39 files, `pins.env` sha256 identical on both sides |
| 00 preflight | OK | kernel 7.0.0-1014-gcp, cgroup v2, disk |
| 10 build | OK | exact docker.io / containerd / runc / nftables installed and `apt-mark hold`; unattended-upgrades and apt-daily masked; `/etc/default/instance_configs.cfg` written (`groups = adm,dip,lxd,plugdev,video`); docker group present and EMPTY (`docker:x:113:`). The guest agent config file on this image is `instance_configs.cfg.distro`; the default list was not read, the override was written as the recipe says. |
| 20 build | OK | runsc deb sha256 AND sha512 matched the pins, bundle sha512 matched, key fingerprint matched, daemon.json absent before and after `dpkg -i`, `runsc version release-20261012.0`, held |
| 30 resolve | OK | all four index digests SAME as pinned; `requirements.proposed.txt` 5 lines |
| lock compare | **MATCH** | proposed lock equals PINS_SKEPTIC.md section 1 exactly (name, version, sha256, 5 lines), checked by `diff` against the five lines taken from that file; then copied to `vendor/requirements.lock` (sha256 `9ba66ff9ae203788524229055082845454b8cd5d55bb7fbfff1dc4d225f5bd5c`) |
| 30 build | OK | four base images pulled by digest and verified; 5 wheels downloaded with `--require-hashes` |
| 40 | OK | legacy builder (`DOCKER_BUILDKIT=0`) IS present in docker.io 29.1.3 (deprecation notice only), so **no docker-buildx install was needed and none was done**. Four images built with `--network=none`. Go std cache seed = **61 MB** (`gocache-seed MB: 61`). The step took about 13 min (17:50Z to 18:02Z), 8 of them `zstd -19` on the Go image. |
| 50 | OK | nft -c passed, daemon.json installed, stage tmpfs fstab line, executor installed, launcher self-check OK, 4 images `docker load`ed, default runtime runsc, storage driver overlay2 (classic store), runsc smoke test printed `42`, hostfw and selftest units ENABLED not started |
| 60 | OK | gates passed (docker group empty, newest kernel == running kernel, nft -c, fstab line), manifest written (no empty values), scrub, power off |

One deviation by me, harmless: after step 60 had scrubbed the disk I ran `cat /opt/od-sbx/IMAGE_MANIFEST.json | tee ~/manifest_copy.json` in the same ssh command (the poweroff had not yet killed the session), so a copy of the manifest sits in `/home/aryamahadik/manifest_copy.json` inside the image. The image's `/home/aryamahadik` also still holds `sandbox/` (the recipe tree) and `buildlogs/` (as noted by the skeptic, step 60 scrubs only keys and history). No credential, no key, no data in any of them.

## 4. Digests, versions, hashes (all from the manifest and the logs; manifest sha256 on od-sbx1: `b2ebb0f2bfa6f42a24e434e7acff13b610f8a51fc8661a7f6bc8f77186f250fb`)

Host: Ubuntu 24.04.5 LTS, kernel 7.0.0-1014-gcp, host python3 3.12.3-0ubuntu2.1, built_utc 2026-10-18T18:04:04Z.

| Item | Value |
|---|---|
| docker.io | 29.1.3-0ubuntu3~24.04.2 (held) |
| containerd | 2.2.1-0ubuntu1~24.04.3 (held) |
| runc | 1.3.4-0ubuntu1~24.04.1 (held) |
| nftables | 1.0.9-1ubuntu0.1 (held) |
| runsc | `runsc version release-20261012.0` (spec 1.2.1), package 20261012.0 (held), platform systrap, `--network=none` |
| **docker storage driver** | **overlay2, classic image store** (`containerd-snapshotter` off; DriverStatus: extfs backing, d_type true, native overlay diff). Recorded in the manifest, ST-7.6 PASS. |
| pytest and deps | pytest 9.1.1, pluggy 1.7.0, iniconfig 2.3.1, packaging 26.3, pygments 2.21.0 (wheels, hash-locked) |
| pins.env sha256 | d7821319f3d13dc649cba4ef3aa337e333313e7b515b96c6c0c39d99816823fd |
| requirements.lock sha256 | 9ba66ff9ae203788524229055082845454b8cd5d55bb7fbfff1dc4d225f5bd5c |
| executor .py tree sha256 | 16072abbf1c84bcf921e4e8b2c4312b169f77d7e3653520250f8d48df34b3800 |
| /etc/od-sbx/hostfw.nft sha256 | 74f8333da8e0326306e4917b6854a285f3d465e4845241e54e4c363aa0375e6a |
| /etc/docker/daemon.json sha256 | e4ed17e4cce090081381e336aaec5c64ddf4f574db7db358038a33f4ed533cb6 |

| Toolchain | Version | Base index digest (pinned, pulled and verified) | od-sbx image id (run by this id) | Saved tarball sha256 |
|---|---|---|---|---|
| python | 3.12.15 | sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258 | sha256:399fa829976e8100f3533045ed9a5324a5937f0edf9ca68bf28b931500d70dae | 856d067b0090d581a7b7c503099d3f07a013be11f8b90b37443f21022308c3e3 |
| node | 24.22.0 | sha256:a5f4366e834695d5f363b920c104953a535d3a9864d1bdf74566a0ebe01daee5 | sha256:a682619db7bdeedde8e14f5151826c26761c8312b8cf226b5855e62d09a3eaa8 | 2772f2b1ec82f639e9027f435a6da92d668f311d1cc149000df01c5f20d7068d |
| go | 1.26.9 | sha256:d9c68c2c51161e12fd77e4c6320687c9cd86e1af1e3ad6e6cd63ff970641453c | sha256:e8e24ab35a4845dfaec253a20786cd3af52469e41e8b1a68a84a9bdcb01d4dc0 | bc9309a9ab38eccd5cd17927d6ee75a8dd38b2afb2e3a14538d96e81ba330b13 |
| sh (bash 5.2) | debian bookworm-slim | sha256:7c7b2c966bc9ee8cedfeef67e0e279108992c77681fa595db4a9d65c06ccc587 | sha256:e2a348b252e119320b3432f5c10f5fd7d448ec17f626fee77828e1dd6f449665 | 7064c7c7b63cbaff23c0cca88d15cf75db0d297bdfc050488087b1fb200508d6 |

gVisor pins (all checked by the scripts): deb sha256 `7a440a03...a707ca`, deb sha512 `a81e1071...f7a3`, bundle sha512 `9606445e...c5e`, key fingerprint `6F1DF85E3A71C24918E727D56FC6D554E32BD943`, dated apt suite `20261012`.
Wheels sha256 (SHA256SUMS on the VM) equal the lock: iniconfig 9121e2c1...d7a7, packaging d7193f7c...cd1c, pluggy 7dd7b0d8...9bec, pygments 2363c69b...37d9, pytest 37a86b45...4f0c.

## 5. Self-test on od-sbx1 (first boot of the image, 18:09Z, ran in 113.7 s, `od-sbx-selftest.service`; raw result: `SELFTEST_od-sbx1_20261018.json`)

Status **FAIL**, failed 2, n 46, manifest_sha256 equals the manifest above, kernel 7.0.0-1014-gcp, counters `dropped_nondeterministic: 1` (that is ST-6.5, which works as intended).

PASS (44): ST-1.1 to 1.7, ST-2.1 to 2.5, ST-3.1 to 3.4, ST-3.6 to 3.8, ST-4.1 to 4.7, ST-5.0 to 5.4, ST-5.6, ST-6.1, 6.2, 6.4, 6.5, ST-7.1 to 7.6, plus informational ST-3.5i and ST-5.5i.

| ID | Result | Detail |
|---|---|---|
| ST-6.3 | **FAIL** | determinism go x2: `exit=1`, stderr ends `/work` then `go: go.mod file not found in current directory or any parent directory` (both runs identical, so it fails every time, not flaky) |
| ST-6.6 | **FAIL** | vendored `go test`: outcome NONZERO after 0.6 s, `pattern ./...: directory prefix . does not contain main module or its selected dependencies` |

Informational results for the post-build sign-off:
- ST-3.5i: `PTRACE_CHILD_RC 0 0` (ptrace of an own child succeeds inside gVisor; as ruled, informational).
- ST-5.5i: forged report with the exact hidden ids gave verdict PASS (the known in-process gap, as ruled).
- ST-3.7: the string match worked on first run (`CapEff 0`, `CapBnd 0`, `NoNewPrivs 1` all printed by gVisor), so R1 is not needed.
- ST-4.7: `/srv/od-sbx/stage` is `tmpfs 512M`, OUT_STOPPED True. ST-4.2 OOM rc 137. ST-4.3 DISK_STOPPED True. ST-4.4 wall 10.1 s. ST-4.5 kept 65536 of 51,773,440 bytes.
- ST-7.5: container `/proc/version` = `Linux version 4.19.0-gvisor ...` vs host 7.0.0-1014-gcp.
- ST-5.6: stripped `pytest.py`, `.local/.../pluggy/__init__.py`, `_pytest/__init__.py`, verdict FAIL as required.
- Open item 6 (runsc systrap on kernel 7.0) is answered: it runs, ST-2..ST-7 all work.
- Open item 3 (NoNewPrivs line under gVisor) answered: it is printed.

### Cause of the two Go failures: CONFIRMED later the same day (see IMAGE_RECIPE.md 10.5: Go source `modload/init.go:541-547` plus one container test on od-sbx1). The paragraph below is the original hypothesis, which was right.

Both messages fit one cause: **S1 (`TMPDIR=/work`) collides with a Go rule**. `cmd/go` treats a `go.mod` whose directory is the system temp root (`os.TempDir()`, i.e. `$TMPDIR`) as non-existent and prints `go: warning: ignoring go.mod in system temp root /work` followed by `go.mod file not found`. The stderr tail stored by the self-test is cut to the last 100 bytes, so only `/work` of the warning line is left, which is exactly what the record shows. The Go fixtures put `go.mod` at `/work` and `TMPDIR` is `/work` (`config.BASE_ENV`, all four Dockerfiles). It would hit every real Go row, not only the fixture, so it is an executor/design change (for example `TMPDIR=/work/tmp` for Go with the directory made in the prelude, or run Go from a subdirectory of `/work`), not a pin change. Per binding condition 2 of 10.4, an executor edit means a rebuild and must be listed in the post-build sign-off. Opus decides. Also note the recipe's open item 9.2 (empty `vendor/modules.txt`) was NOT the failure as far as the messages show, and the Go prewarm/seed copy itself is not implicated (seed 61 MB; ST-6.6 failed in 0.6 s, so the 512m tmpfs and 1g memory question is still unmeasured).

## 6. Other observations from the first boot (for the post-build sign-off)

- hostfw came up before networking and the VM got its DHCP lease and IAP SSH worked: the first-boot DHCP path under `hostfw.nft` is fine. ST-1.1 to 1.7 all pass (ST-1.3 name `od-sbx1`; ST-1.6 service-accounts listing HTTP 200 with an empty body).
- SSH host keys were regenerated at first boot by cloud-init (new fingerprints, files dated 18:08), so the build VM's host keys are not reused.
- docker group on od-sbx1 after the OS Login session: `docker:x:113:` (empty). `instance_configs.cfg` carries the override. Zero leftover containers after the self-test.
- OS Login works through IAP: login as uid 1682845740 (account mahadikarya2@gmail.com, user dir /home/mahadikarya2_gmail_com) and `sudo` works. BUT `google-oslogin-cache.service` FAILED at boot ("Failure getting users, quitting"), and name lookups from the non-root OS Login user (`getent group docker`, `id -un`) are very slow or time out, because the NSS module calls the metadata server as a non-root uid and `hostfw.nft` drops that (same effect as ST-1.2, by design). Use `sudo` and numeric ids; the cache failure is cosmetic for the executor (runs as root) but makes plain `getent` calls from the operator account hang for minutes. `sudo` prints `unable to resolve host od-sbx1...` on every call (no DNS), harmless.
- The stage tmpfs mounts at boot through fstab (512M). The self-test unit is `failed` after a FAIL result, as designed, so `run-batch` refuses to run.

## 7. What is needed next (decisions for Opus / orchestrator, none taken here)

1. Go fix for the TMPDIR collision (section 5), then a REBUILD of the image from step 50 (executor/fixtures change the tree hash; per 10.4 an edit before step 50 needs listing in the post-build sign-off). The base layers (steps 10 to 40: packages, runsc, toolchain images, Go cache seed) do not need to change unless the fix touches the Dockerfiles (they set `TMPDIR=/work` too). The build VM `od-sbx-build` is TERMINATED with its disk, but its disk is now the scrubbed state; the simplest rebuild path is a fresh pass of the recipe on it (it is idempotent apart from `ensure_classic_store` and the lock) or a new build VM.
2. After the rebuild: recreate od-sbx1 and create od-sbx-s from the new image, run the self-test on both, stop all VMs.
3. Delete the old image `od-sbx-base-20261018` (or keep it as evidence) and note the image/family choice: the family `od-sbx-base` currently points to this image.
4. od-sbx1 has the 1h30m `--max-run-duration` with DELETE; since I stopped it, the instance still exists and can be deleted when the evidence is no longer wanted.

## 8. REBUILD r2 with the F-GO1 fix (Sun 18 Oct 2026, builder; fix reviewed SOUND by the skeptic, rebuild ordered by the coordinator)

Result: **`od-sbx-base-20261018-r2` built, self-test on od-sbx1 PASS 46/46** (failed 0, 118.5 s; raw: `SELFTEST_od-sbx1_20261018_r2.json`, manifest copy: `rebuild_logs/IMAGE_MANIFEST_r2.json`).
`pins.env` unchanged (`d7821319f3d13dc649cba4ef3aa337e333313e7b515b96c6c0c39d99816823fd`). od-cpu1 and od-l4b untouched. od-sbx-s NOT created (waits for Opus).

| Item | Value |
|---|---|
| Image | `od-sbx-base-20261018-r2`, id 9151289144192312211, family `od-sbx-base`, label `purpose=c21-sandbox`, READY, archive 2,571,707,392 bytes, UEFI_COMPATIBLE |
| Old image | `od-sbx-base-20261018` marked DEPRECATED (replacement r2), not deleted |
| Manifest sha256 | `29474351959951a20815e8e8645b6fa3df0888df6a553f9399ebfc85871d71c8` (built_utc 2026-10-18T19:16:44Z) |
| Executor tree hash | `defbb2e49ae9589fc82b2c53d988b70ccedf7e9c0c226d7de38e47ee6eefa753` (manifest, on disk and ST-7.4 agree) |
| Image ids | python `sha256:399fa829976e8100f3533045ed9a5324a5937f0edf9ca68bf28b931500d70dae`, node `sha256:a682619db7bdeedde8e14f5151826c26761c8312b8cf226b5855e62d09a3eaa8`, go `sha256:e8e24ab35a4845dfaec253a20786cd3af52469e41e8b1a68a84a9bdcb01d4dc0`, sh `sha256:e2a348b252e119320b3432f5c10f5fd7d448ec17f626fee77828e1dd6f449665` (all identical to the first build: step 40 was not rerun) |
| Other manifest fields | requirements.lock `9ba66ff9...bd5c`, storage overlay2, `runsc version release-20261012.0`, kernel 7.0.0-1014-gcp |
| Files the manifest does NOT hash (sha256 of the copy on od-sbx1, equal to the local file; corrected 18 Oct, N5) | `/etc/od-sbx/hostfw.nft` `74f8333da8e0326306e4917b6854a285f3d465e4845241e54e4c363aa0375e6a`; `/etc/docker/daemon.json` `e4ed17e4cce090081381e336aaec5c64ddf4f574db7db358038a33f4ed533cb6`; local `host/od-sbx-hostfw.service` `06a5f42cf67a66ca3b5459c450a43f3236de9a1ca80a0d681fe35e21fd0ec717` and `host/od-sbx-selftest.service` `562a6a0f47bab03d3625afe680fe107c6aa3b73cc3159dca738ffc36ed5fd13d` (the two unit files were NOT read back from od-sbx1 yet: Opus condition (3).3 asks for that on od-sbx-s) |
| ST-6.1 to 6.4 | exit 0, last line exactly `/work/.tmp` for python, node, go, sh; ST-6.6 `go test` OK in 2.2 s; ST-3.7, ST-4.7, ST-7.x pass; informational ST-3.5i `PTRACE_CHILD_RC 0 0`, ST-5.5i PASS (known gap), as before |

What was done, per the 10.5 rebuild notes: build VM booted, reached over IAP (its SSH host keys had been regenerated by cloud-init; I checked the offered ED25519 fingerprint against the serial console
line printed by cloud-init at that boot, then dropped only the stale `google_compute_known_hosts` entry of that instance); `od-sbx-selftest` had already failed against the old manifest and was stopped, `od-sbx cleanup` run as
root (0 containers), first-build logs copied to `build_logs_first_build/`, `/home/*/{sandbox,buildlogs,manifest_copy.json}` removed, new tree copied to `/tmp/sandbox` (54 files, `pins.env` sha256 verified), step 50 run
with `SBX_SRC=/tmp/sandbox` (log `rebuild_logs/50_build.log`, state checks `rebuild_logs/pre60_checks.sh`), step 60 run as the last command of its ssh session (`rebuild_logs/60_build.log`). Image homes checked on od-sbx1: no
sandbox, buildlogs or manifest copy; `/tmp` has only systemd private dirs.
Two things to know:
1. One extra hygiene step: I removed `/var/lib/od-sbx/selftest.json` (left by the build VM's boot-time self-test against the OLD manifest) before step 60. The unit deletes it at every start anyway.
2. With the host firewall up on the build VM (it is enabled in the disk and runs at boot), step 60's `systemctl poweroff` HUNG at `google-shutdown-scripts.service` stop ("no limit", 7 min; the guest agent's shutdown-script runner
   evidently cannot finish with output DROP for non-root). Step 60 had completed (manifest written, scrub, `sync`); I stopped the VM with `gcloud compute instances stop` and cut the image from that (crash-consistent) disk. The
   first image came from a clean poweroff because the firewall was not running then. The 46/46 self-test, including the hash and version checks ST-7.x, is the verification of the contents. If a clean shutdown is wanted for
   the image of record, the rebuild notes need one more line: `sudo systemctl stop od-sbx-hostfw` right before step 60 (it flushes the ruleset and does not touch the files).
Also noted: with hostfw active on the build VM every `sudo` took about 40 s (hostname lookup); use one `sudo bash -s` per batch of checks.

### 8.1 Opus condition C1: read-only evidence (Sun 18 Oct 2026 19:48Z; nothing started or modified, od-sbx1 stays TERMINATED)

Commands: `gcloud compute instances describe od-sbx1 --zone us-east4-c` (selected fields), `gcloud compute disks describe od-sbx1`, `gcloud compute firewall-rules list --filter=network:sbx-vpc`,
`gcloud compute routers list`, plus read-only `vpn-gateways|vpn-tunnels|target-vpn-gateways list`, `networks describe sbx-vpc`, `networks subnets describe sbx-subnet`, `networks peerings list`, `addresses list`.

| C1 item | Observed | OK |
|---|---|---|
| Source image by name | boot disk `od-sbx1`: `sourceImage .../global/images/od-sbx-base-20261018-r2`, `sourceImageId 9151289144192312211` | yes |
| No external IP / no service account | `networkInterfaces[0].accessConfigs` count 0, `ipv6AccessConfigs` count 0, `serviceAccounts` count 0 (no such key in the describe) | yes |
| Shielded VM | `enableSecureBoot: true`, `enableVtpm: true`, `enableIntegrityMonitoring: true` | yes |
| Metadata | items: `block-project-ssh-keys=TRUE`, `enable-oslogin=TRUE`; NO `ssh-keys` item | yes |
| Scheduling | `maxRunDuration 5400 s`, `instanceTerminationAction: DELETE`, `provisioningModel STANDARD`, `automaticRestart true`, `preemptible false` | yes |
| Network / disk | `network sbx-vpc`, `subnetwork sbx-subnet`, `networkIP 10.200.0.3`; ONE disk (boot, 40 GB, `autoDelete true`, `pd-standard`); `canIpForward false`; `deletionProtection false` | yes |
| Other | machine type n2-standard-4, created 2026-10-18T19:28:22Z, status TERMINATED, label `purpose=c21-sandbox`, tags `od-sbx`, `od-sbx1` (tags are unused by any rule) | |

`firewall-rules list --filter=network:sbx-vpc` returns EXACTLY 3 rules (all enabled, no target tags):
```
NAME                NETWORK  DIRECTION  PRIORITY  ALLOW   DENY  SRC              DST        TAGS  DISABLED
sbx-egress-deny-v4  sbx-vpc  EGRESS     1000              all                    0.0.0.0/0        False
sbx-egress-deny-v6  sbx-vpc  EGRESS     1000              all                    ::/0             False
sbx-ingress-iap     sbx-vpc  INGRESS    1000      tcp:22        35.235.240.0/20                   False
```
`gcloud compute routers list` (all regions): `Listed 0 items.` (re-checked with `--format=value(name)`: 0 routers), so there is no Cloud Router and therefore NO Cloud NAT anywhere in the project.
Also: vpn-gateways 0, vpn-tunnels 0, target-vpn-gateways 0, peerings on sbx-vpc 0, reserved addresses 0, `sbx-vpc` custom mode (`autoCreateSubnetworks false`), REGIONAL routing, one subnet `sbx-subnet`
10.200.0.0/24 with `privateIpGoogleAccess: false`, `privateIpv6GoogleAccess: DISABLE_GOOGLE_ACCESS`, IPv4 only.
Images: `od-sbx-base-20261018-r2` READY, family `od-sbx-base`, not deprecated; `od-sbx-base-20261018` READY, DEPRECATED (replacement r2). Instances: od-cpu1 and od-l4b RUNNING (default network, untouched), od-l4 / od-sbx-build / od-sbx1 TERMINATED.
C1 result: all items hold. Condition C2 (create from the image NAME, never the family) is now written into IMAGE_RECIPE.md section 8.

## 9. Open items from the Opus sign-off (SIGNOFF_OPUS.md, Sun 18 Oct 15:44 EDT); none is blocking

Conditions C1 to C6 are binding for od-sbx1 (C1 done above, C2 in the recipe, C3 assessed in section 10, C4 and C5 are rules for L-C and for every reader of result files, C6 = any edit to pins.env, the executor or the host files
needs a new image, a new self-test and a new Opus sign-off; the rebuild notes now carry `sudo systemctl stop od-sbx-hostfw` before step 60). od-sbx-s needs the separate list in SIGNOFF_OPUS.md section 3 (same flags and image name,
own first-boot 46/46 saved as `SELFTEST_od-sbx-s_<date>.json` with the hostfw.nft / daemon.json / unit-file hashes and an empty `dmesg | grep -i 'EXT4-fs error'`, host key check against the serial console, and a signed sealed-layer review BEFORE any sealed byte enters).

| ID | Item | State |
|---|---|---|
| N1 (R2) | `stage()`: an OSError other than a clash (ENOSPC, ENAMETOOLONG) aborts the whole batch and no `.manifest.json` is written; the same for a malformed job line or an unknown toolchain | OPEN, fail-closed; fold into the next executor change |
| N2 (R4) | `cli` does not validate `report`; a workload symlink on an intermediate directory of a non-bare name would make the root executor read that host path (contents only feed a parser and never leave the VM) | OPEN; C4: `report` must be a bare file name |
| N3 | a prelude failure (`cp`/`mkdir`) and docker exit 125 look like program exit codes; a distinct prelude exit code plus outcome ERROR is needed | OPEN; C4: treat 125 as an infrastructure error, drop and count |
| N4 | the determinism check compares stdout only, and the verdict comes from run 0 only (verdicts of the repeats are not compared) | OPEN; Option B in section 10 would close it for suites |
| N5 | records: manifest-field wording for hostfw.nft / daemon.json, 10.5 still headed PROPOSED, skeptic reports not filed, 10.4 checklist line not pointing to the sign-off | CLOSED 18 Oct (section 8 table row split, 10.5 heading "APPLIED (r2)", `SKEPTIC_F-GO1_pass1.md` and `_pass2.md` filed as builder summaries of the relayed reports, 10.4 points to SIGNOFF_OPUS.md) |
| N6 (R3, R5) | no `RequiresMountsFor=/srv/od-sbx/stage` in `od-sbx-selftest.service`; `pip uninstall ... || true` still in `Dockerfile.python` | OPEN; next rebuild |
| N7 | every sandbox VM's poweroff hangs under hostfw (guest-agent shutdown scripts); harmless: DELETE at max-run or a forced `instances stop` | OPEN, accepted; expect the forced path |

Recommended, not blocking (SIGNOFF_OPUS.md 3.6): check that PROJECT metadata holds no secrets (a keys-only listing), and consider a sbx-vpc DNS policy that stops recursive resolution.

## 10. C3 assessment (builder, Sun 18 Oct; PROPOSAL ONLY, no executor or image file was edited; a skeptic must review any edit, then rebuild + new sign-off per C6)

Question: do pytest, `go test` and `node --test` print timings to stdout, and does the determinism check compare raw stdout?

**Yes to the second.** `runner.run_repeated` marks a row deterministic iff `len({(r.exit_code, r.stdout_sha256) for r in runs}) == 1` (2 runs, 3 for will-this-test-fail rows). `stdout_sha256` is a SHA-256 over ALL stdout bytes
(also past the 64 KB cap). Stderr is not compared. `cli.run_batch` drops a non-deterministic row before any verdict is computed (`dropped_nondeterministic`). `verdict.py` itself never looks at stdout, only at the report, but it is
never reached for a dropped row. The self-test does not cover this: ST-5.x and ST-6.6 use `run_once`, and ST-6.1 to 6.5 send only trivial `run` fixtures through `run_repeated`. So suite determinism is untested until the pilot.

**What the tools print** (measured with toy 2-test suites on the Mac: pytest 9.0.2 with the image's own `pytest.trusted.ini`, Node v22.23.1; Go is not installed on the Mac, its line comes from the od-sbx1 test in `F-GO1_test_on_od-sbx1.out`; the image has pytest 9.1.1, Node 24.22.0, Go 1.26.9, so the pilot must re-confirm):

| Toolchain | Argv as the recipe implies | Timing on stdout? | Evidence |
|---|---|---|---|
| pytest | `python -s -P -m pytest -c /etc/od-sbx/pytest.ini --rootdir=/work --junitxml=/out/junit.xml ...` (ini has `-q`) | YES: `2 passed in 0.03s`, `2 failed, 1 passed in 0.04s` | 3 identical invocations gave 2 distinct hashes (pass) and 2 distinct (fail) |
| pytest, one extra `-q` (effective `-qq`) | same + `-q` | NO: the summary line is gone, only dots (+ failure text) remain | 3 runs, 1 hash, for a passing and for a failing suite |
| node | `node --test` (non-TTY default reporter = TAP) | YES: `duration_ms: 19.45` per test, `# duration_ms 152.3` | 3 runs, 3 hashes. `--test-reporter=spec`: `✔ a (18.0ms)`, `ℹ duration_ms 110.2`. `--test-reporter=junit` to stdout: `time="0.017223"` |
| node, junit to a file | `node --test --test-reporter=junit --test-reporter-destination=/out/junit.xml` | NO: stdout is 0 bytes | 3 runs, the empty hash (`da39a3ee`); the XML itself differs per run but is not compared |
| go | `go test ./...` | YES: `ok  <TAB>det<TAB>0.008s` for every package, `FAIL<TAB>pkg<TAB>0.005s`; `-v` adds `--- PASS: T (0.00s)`; `-json` adds `"Time"` and `"Elapsed"` | line seen on od-sbx1. NO flag removes the elapsed time from the `ok` line |
| go, json to a file | `sh -c 'go test -json -count=1 ./... > /out/go.json'` | NO: stdout empty (UNMEASURED on the image) | the cli's `go.json` report is by design written under `/out` |

So, if jobs follow the recipe's own design (reports under `/out`), only pytest still leaks its summary line to stdout. A job that skips the redirect or the reporter flags leaks too. The danger is not a wrong label, it is silent bias: a suite row survives only if
both runs print the same rounded timing, so surviving suite rows skew to FAST suites. The drop is counted, so the C3 pilot will show the rate.
Related: a pytest `--collect-only` run for `expected_ids` prints the ids plus `N tests collected in 0.01s` with the image ini; with `-q -q` it prints per-file counts (`test_t.py: 2`), which are useless. Run collection once with `run_once` and ignore the last two lines.
`-p no:terminal` is NOT an option with the trusted ini (its `-q` addopt then fails: `unrecognized arguments: -q`; changing the ini means a step 40 rebuild).

**Options** (all keep S1: no env, mount or image change):

- **A. No executor change (what C3 asks for the pilot).** Fix it in the job argv, exact forms: python `["python","-s","-P","-m","pytest","-c","/etc/od-sbx/pytest.ini","-q","--rootdir=/work","--junitxml=/out/junit.xml", <files>]`;
  node `["node","--test","--test-reporter=junit","--test-reporter-destination=/out/junit.xml", <files>]`; go `["sh","-c","go test -json -count=1 ./... > /out/go.json"]`. Optional guard in `cli._suite_argv_ok`: require a `-q` after the `-s -P` prefix.
  Cost: nothing to rebuild. Risk: relies on L-C discipline; a slip drops rows (counted), and the fast-suite bias is only visible in the counters.
- **B. Recommended if the guard should live in code: compare verdicts, not stdout, for suite rows.** `run_repeated(..., det_key=None)` (default key unchanged: `(exit_code, stdout_sha256)`); `cli.run_batch` passes, for `kind == "suite"` rows that have a `report` and
  `expected_ids`, a key per run = `(exit_code, outcome, V.compute(...).verdict, tuple(sorted(parsed_report.items())))` using the same `parse_junit` / `parse_go_json` it already calls. Stdout and stderr stay recorded (excerpts) but are no longer part of equality for those rows, so
  timings, test ordering text and temp paths cannot drop a row, while a flaky verdict (pass in one run, fail in the next), a different id set or a different exit code still does. Run rows and suite rows without `expected_ids` keep the raw-stdout rule. It also closes N4 for suites.
  Size: about 3 lines in `runner.py`, about 20 in `cli.py`, 5 tests (same verdict + different stdout = deterministic; different verdict = not; run rows unchanged; no `expected_ids` falls back; mutation guard) and optionally a new check ST-6.7
  (a pytest suite with the image's default `-q` through `run_repeated` must be deterministic), which would make the check list 47 and touch the section 7 table and its test. Needs: skeptic, rebuild from step 50 (tree hash changes), new self-test, new Opus sign-off (C6).
- **C. Normalise timing tokens before hashing: not recommended.** Only for `kind="suite"`, on a line-buffered second hash in `_Capped`. Exact patterns: pytest `(?m)^(=*\s*(?:\d+ \w+(?:, )?)+ in )\d+(?:\.\d+)?s(?: \(\d+:\d\d:\d\d\))?(\s*=*)$` and `(?m)^(\d+ tests? collected in )\d+(?:\.\d+)?s$`;
  go `(?m)^((?:ok|FAIL)\s+\S+\t)\d+(?:\.\d+)?s(?:\t.*)?$`, `(?m)^(\s*--- (?:PASS|FAIL|SKIP): \S+ \()\d+(?:\.\d+)?s\)$`, json `"Time":"[^"]+"` and `"Elapsed":[0-9.eE+-]+`;
  node TAP `(?m)^(\s*duration_ms: )\d+(?:\.\d+)?$` and `(?m)^(# duration_ms )\d+(?:\.\d+)?$`, spec `\(\d+(?:\.\d+)?(?:ms|s)\)` and `(?m)^(ℹ duration_ms )\d+(?:\.\d+)?$`, junit-on-stdout `time="[0-9.]+"`.
  Why not: it covers only the reporters listed (any other format, locale or version change re-breaks it), it can hide real output nondeterminism of the program, and it needs a line-buffered hash. B compares what is actually labelled.

Recommendation: run the C3 pilot with A (zero change, and it measures the real drop rate on the image); decide on B afterwards, or now if you want the guard enforced in code. The coordinator decides; nothing was edited.

