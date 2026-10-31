# od-sbx pins: independent SKEPTIC re-observation (Sun 18 Oct 2026)

Observer: Sonnet skeptic (fresh, no access to the builder's notes beyond pins.env, IMAGE_RECIPE.md and build/*.sh).
Method: every value was re-fetched from the upstream source on 18 Oct 2026 from the Mac (curl, gpg, gcloud READ-ONLY
describe/list, Ubuntu archive index files, Docker Hub registry API, PyPI JSON, python.org, go.dev, nodejs.org, gvisor.dev).
The build VM `od-sbx-build` was left TERMINATED (not started, nothing executed on any VM, no generated code run, no docker
pull on the Mac). Scratch copies of downloads live only in the session scratchpad.
`PINS_STATUS` is still `CANDIDATE` (not set to FROZEN by this review; that is Opus's call).

Verdict: 1 pin CHANGED (`GVISOR_APT_SUITE`), everything else KEPT. 6 findings that are not pin values (section 3) need an
owner/Opus decision before the build; none of them blocks `resolve`.

## 1. Pin table

| Pin | Verdict | Evidence (independent) |
|---|---|---|
| GVISOR_VERSION 20261012.0 | KEPT | Apt `Packages` (suite release and suite 20261012) lists `Version: 20261012.0`, `Filename: pool/20261012.0/binary-amd64/runsc.deb`, Size 104563214. `Release` Date Fri 16 Oct 2026 20:51 UTC. Deb control file inside the downloaded .deb says Version 20261012.0. `strings runsc` shows `release-20261012.0`. |
| GVISOR_DEB_SHA256 7a440a03...a707ca | KEPT | Downloaded `pool/20261012.0/binary-amd64/runsc.deb` (104,563,214 bytes): sha256 = `7a440a035128a52f489b0bb76f60ac4df9cabe7cdf31dd5fd79a3e80f8a707ca`, equals pin and equals the Packages stanza. |
| GVISOR_DEB_SHA512 a81e1071...f7a3 | KEPT | Same file: sha512 = `a81e1071fa1e2fb49f639c58e827dfb10be74af3a68e44ffbba90ccb00c96c7a08b82677ef8c9ce94d4abe5b3bef766f662c43f544eed2c6f8b24e97de9af7a3`, equals pin. |
| GVISOR_BUNDLE_URL / GVISOR_BUNDLE_SHA512 9606445e...c5e | KEPT | URL returns HTTP 200. `.sha512` file at the URL +`.sha512` and my own sha512 of the downloaded 100,743,091-byte bz2 both equal `9606445eed5aedfcf05310e7ccef61d994089914c6622fc82624c24d2b18db1b2210f40e40a7be27b8b7772859de7d95c501b4eba66423053c960bf671377c5e`. Cross-check: sha512 of `runsc` in the bundle = sha512 of `/usr/bin/runsc` extracted from the deb (`e2616f19...fcd91`), so deb and bundle are the same binary. |
| GVISOR_APT_URL | KEPT | https://storage.googleapis.com/gvisor/releases serves `dists/*`, matches the repo line on gvisor.dev/docs/user_guide/install (`deb [arch=.. signed-by=..] https://storage.googleapis.com/gvisor/releases release main`). |
| GVISOR_APT_SUITE `release` | CHANGED to `20261012` | The gVisor install page says "apt installation of a specific point release is not supported" and that the date suite is the way to pin. The floating suite `release` currently lists ONLY the newest version in `Packages` (one stanza). When gVisor publishes its next release (weekly cadence: 20260928, 20261005, 20261012 all exist as suites), `apt-get download runsc=20261012.0` fails or the pin silently has to move. Suite `20261012` returns HTTP 200, its `Packages` is byte-identical to `release` today (cmp), and its InRelease is signed by the same key (Good signature, RSA 6F1DF85E..., Date 16 Oct 2026). The scripts only use the suite in two places (sources.list line and the `dists/<suite>/.../Packages` URL), both work with a date. Caveat: the page says a dated suite "may include point updates" (e.g. a 20261012.1); the script's `runsc=20261012.0` plus the deb hashes would then fail loudly, which is the safe direction. Last-resort fallback, immutable path: `pool/20261012.0/binary-amd64/runsc.deb` (hash-pinned) or the bundle. |
| GVISOR_APT_KEY_URL | KEPT | https://gvisor.dev/archive.key downloads (HTTP 200). |
| GVISOR_APT_KEY_FPR 6F1DF85E3A71C24918E727D56FC6D554E32BD943 | KEPT | `gpg --show-keys --with-colons` on the downloaded key: `fpr:::::::::6F1DF85E3A71C24918E727D56FC6D554E32BD943:`, RSA 4096, uid "The gVisor Authors <gvisor-bot@google.com>". Imported into a throwaway keyring: InRelease and Release.gpg (suite release) and InRelease (suite 20261012) all verify "Good signature" with that key. |
| DOCKER_IO_VERSION 29.1.3-0ubuntu3~24.04.2 | KEPT | Ubuntu archive Packages: present in noble-updates/universe AND noble-security/universe (the only 29.x; noble release pocket has 24.0.7). Filename pool/universe/d/docker.io-app/docker.io_29.1.3-0ubuntu3~24.04.2_amd64.deb. Depends: containerd (>= 1.2.6), iptables, libnftables1 (>= 1.0.2). |
| CONTAINERD_VERSION 2.2.1-0ubuntu1~24.04.3 | KEPT | noble-updates/main and noble-security/main both list it; Depends: runc. |
| RUNC_VERSION 1.3.4-0ubuntu1~24.04.1 | KEPT | noble-updates/main lists 1.3.4-0ubuntu1~24.04.1 (highest). noble-security/main lists the older 1.3.3-0ubuntu1~24.04.3, which is normal pocket lag; apt picks the pinned exact version from updates. Depends libc6 (>= 2.38) satisfied on noble. |
| NFTABLES_VERSION 1.0.9-1ubuntu0.1 | KEPT | noble-updates/main. Depends libnftables1 (= same version), pulled automatically. |
| host python3 3.12.3-0ubuntu2.1 (comment only) | KEPT | noble-updates and noble-security main list 3.12.3-0ubuntu2.1. |
| Ubuntu 24.04.5 / kernel 7.0.0-1014-gcp (recorded, not a pin) | KEPT (archive side only) | `linux-image-gcp` / `linux-image-gcp-7.0` = 7.0.0-1014.14~24.04.1 in noble-updates and noble-security, so the kernel string is the current archive one. Boot disk of `od-sbx-build` came from `ubuntu-2404-noble-amd64-v20261016` (family head today). The RUNNING kernel was not re-observed because the VM was not started (cost, and the task is a re-observation of upstream values). `uname -r` is recorded in IMAGE_MANIFEST.json at build time anyway. |
| PY_VERSION 3.12.15 / PY_TAG / PY_DIGEST sha256:34386ef0...07258 | KEPT | Docker Hub registry API, `library/python:3.12.15-slim-bookworm`: Content-Type OCI image index, `docker-content-digest` = pin, and sha256 of the returned index body = pin (10 manifests). amd64 child manifest sha256:2ed6491b93cd...179d; its config: `PYTHON_VERSION=3.12.15`, created 2026-10-06. python.org/ftp lists 3.12.15 as the newest 3.12 (3.12.14 before it); `Python-3.12.15.tar.xz` sha256 = `c2c43219...fd5a`, equals the `PYTHON_SHA256` baked into the image config. |
| NODE_VERSION 24.22.0 / NODE_TAG / NODE_DIGEST sha256:a5f4366e...daee5 | KEPT | Registry: digest header = pin = sha256 of body (6 manifests). amd64 child sha256:ec857ea6bb60...9cf7; config `NODE_VERSION=24.22.0`, created 2026-10-14. nodejs.org/dist/index.json: v24.22.0, date 2026-10-14, lts=Krypton, newest 24.x (v26.x are not LTS). Note the image keeps `YARN_VERSION=1.22.22` and `ENTRYPOINT docker-entrypoint.sh`; Dockerfile.node already deletes /opt/yarn*. |
| GO_VERSION 1.26.9 / GO_TAG / GO_DIGEST sha256:d9c68c2c...1453c | KEPT | Registry: digest = pin = body sha256 (10 manifests). amd64 child sha256:bcef992b77b1...9eff; config `GOLANG_VERSION=1.26.9`, created 2026-10-08. go.dev/dl json: go1.26.9 is `stable: true` and is the newest 1.26.x; newest overall is go1.27.2 (so 1.26 is the second-newest line, still supported, as the recipe says). |
| SH_REPO/TAG/DIGEST debian:bookworm-slim sha256:7c7b2c96...cc587 | KEPT | Registry: digest = pin = body sha256 (10 manifests). amd64 child sha256:a4672c0cb26f...ee91, created 2026-10-05. Mutable tag by design; the digest is the pin. |
| GO_TARBALL_SHA256 42d158b4...c2f8d | KEPT | go.dev/dl json, go1.26.9 linux/amd64 archive `go1.26.9.linux-amd64.tar.gz` = `42d158b4d8f7b61ac0a830567c940a86098fb7aac52e467a5ebec03ef5cc2f8d`. |
| NODE_TARBALL_SHA256 cc2f601c...5008 | KEPT | nodejs.org/dist/v24.22.0/SHASUMS256.txt line for `node-v24.22.0-linux-x64.tar.xz` = `cc2f601cee82d9a5a233302fe307abc600727035fd7d2c3a3571755989e95008`. |
| PYTEST_VERSION 9.1.1 | KEPT | PyPI JSON: 9.1.1 is the latest release, not yanked, uploaded 2026-06-19, requires_python >=3.10. Wheel `pytest-9.1.1-py3-none-any.whl` sha256 `37a86b45efb9a47a61a36449063e8e18d0cab3161329fc099eb21783169c4f0c`. Runtime deps (non-win32, py>=3.11): iniconfig>=1.0.1, packaging>=22, pluggy<2,>=1.5, pygments>=2.7.2. |
| REQUIREMENTS_LOCK | NOT YET PRODUCED | `vendor/requirements.lock` does not exist (only README). Independent proposal for the builder's `resolve` output to be compared against (wheels only, current latest, none yanked): pluggy 1.7.0 `7dd7b0d8832ba3cb632c306926ded123429211b83641b35dc5c41ad2d34f9bec`; iniconfig 2.3.1 `9121e2c1fdb355232495be3194c8dfe87ccc2d5dee45947b78e68f499790d7a7`; packaging 26.3 `d7193f7c8e4e93f444fde0262bf90af30e16fa0ad0ad44cb553c87339b23cd1c`; pygments 2.21.0 `2363c69b61c4a97c838da3b130dcd6468f4848992b21a82f2a63ec34377137d9`; pytest 9.1.1 hash above. All py3-none-any. If `resolve` on the VM yields different versions or hashes, stop and investigate. |

## 2. Infrastructure claims (egress deny, metadata server, rootless, no service account)

| Claim | Verdict | Evidence |
|---|---|---|
| Build VM has no service account, no scopes | KEPT | `gcloud compute instances describe od-sbx-build`: `serviceAccounts = None`. |
| Shielded VM, block-project-ssh-keys | KEPT | shieldedInstanceConfig secureBoot/vTPM/integrity all True; metadata items: `block-project-ssh-keys=TRUE` plus an instance-level `ssh-keys` entry (the user's own key, build VM only; scrubbed by step 60 from the disk, and not carried to od-sbx1 which is created without it). |
| `--max-run-duration` 6h, STOP; no extra disk; external IP | KEPT | scheduling maxRunDuration 21600 s, instanceTerminationAction STOP, one 40 GB pd-balanced boot disk, one ONE_TO_ONE_NAT access config, canIpForward False, tag `od-sbx-build`, label `purpose=c21-sandbox-build`. |
| `od-sbx-build-deny-internal` | KEPT | `firewall-rules describe`: EGRESS, priority 900, denied all, destination 10.128.0.0/9, target tag od-sbx-build, enabled, network default. The default subnet in us-east4 is 10.150.0.0/20 (inside 10.128.0.0/9), od-l4b/od-cpu1 live there. The rule does not touch 169.254.169.254 (correct, it cannot). Internet egress is intentionally open on the build VM. |
| VPC egress deny cannot block the metadata server | KEPT (documented upstream) | docs.cloud.google.com/firewall/docs/firewalls: packets to/from the metadata server are not subject to VPC firewall rules; "Google Cloud always allows communication between a VM instance and its corresponding metadata server" regardless of rules. So the claim that blocking 169.254.169.254 needs the in-guest `hostfw.nft` (output policy drop, only uid 0 allowed) is correct, and the design (no SA to steal, nftables drop for non-root, containers on `--network none`) is the right one. |
| `sbx-vpc`, `sbx-subnet`, deny rules, od-sbx1 | NOT YET CREATED (as stated) | `gcloud compute networks list` shows only `default`; instances: od-l4, od-cpu1, od-l4b, od-sbx-build. Nothing from section 8 of the recipe exists, matching "NOT RUN". |
| runsc install path (apt, signed, no legacy auto-install) | KEPT with a caveat (F-2 below) | Install page confirms apt repo and key URL. |
| "Rootless" | KEPT as an interpretation | Dockerd/runsc stay root by design; workload is uid 65534, cap-drop ALL, no-new-privileges, read-only root, `docker` group must be empty (`10_install_base.sh` asserts it). The recipe states this openly; Opus should accept or order rootless podman. |

## 3. Findings that are not pin values (decisions or script edits, none done by me except GVISOR_APT_SUITE)

F-1 (done, see table): floating apt suite. Fixed in pins.env.

F-2 (medium, script fix, not applied): the runsc deb's `postinst` (read from the downloaded .deb) does
`if [ -f /etc/docker/daemon.json ]; then runsc install --clobber=false; systemctl reload docker; fi`.
The recipe says the legacy `runsc install` is never used. In the planned order it does not fire, because step 50 writes
`/etc/docker/daemon.json` after step 20, and Ubuntu's docker.io does not ship one (not observed on a VM, so UNVERIFIED).
If any earlier step ever creates daemon.json, the postinst will edit it behind our back. Suggested guard in
`20_install_runsc.sh` build mode before `dpkg -i`: `[ ! -e /etc/docker/daemon.json ] || die "daemon.json exists before runsc install"`.

F-3 (medium, UNVERIFIED, first-run risk): Docker 29 uses the containerd image store by default on fresh installs (upstream
behaviour; I could not confirm Ubuntu's packaging default without a VM). With it, `docker image inspect .Id` is the
manifest/index digest, not the config digest, `docker save`/`load` round trips can change ids, and the `RepoDigests[0]`
assertion in `30_fetch_toolchains.sh` and the "run by image id" logic in `60_finalize_image.sh`/`dockercmd.py` should be
checked on the first `resolve`/build run (`docker info -f '{{.DriverStatus}}'`). If it bites, set `"features": {"containerd-snapshotter": false}`
in daemon.json (a build fix, not a pin change).

F-4 (medium, access path): od-sbx1 is created with `block-project-ssh-keys=TRUE`, no `ssh-keys` metadata and no
`enable-oslogin`. `gcloud compute ssh/scp --tunnel-through-iap` normally pushes the key to PROJECT metadata, which is
blocked, so login will fail. `oslogin.googleapis.com` is enabled on the project (observed), so adding
`--metadata block-project-ssh-keys=TRUE,enable-oslogin=TRUE` to the od-sbx1 command (plus roles/compute.osAdminLogin or
osLogin for the user) is the likely fix. Also confirm on first boot that sshd/NSS OS Login lookups work under `hostfw.nft`
(guest agent and sshd run as root and are allowed; any helper that runs as another uid and calls the metadata server would be dropped).

F-5 (low-medium, open item answered): `iap.googleapis.com` is NOT in the project's enabled services (enabled list shows
compute and oslogin only). IAP TCP forwarding may still work without enabling it (the firewall range 35.235.240.0/20 and
roles/iap.tunnelResourceAccessor are what matter), but this was not tested. Enabling an API is a state change I did not make;
decision for the orchestrator, or test with a scratch instance.

F-6 (low): `hostfw.nft` was not syntax-checked (no nft on the Mac). Run `nft -c -f /etc/od-sbx/hostfw.nft` on the build VM in
step 0 or 50 before enabling the unit; a syntax error in a oneshot unit with policy drop would leave the host with either no
firewall or (if partially applied after `flush ruleset`) a broken one. Contents read: policy drop on output/input/forward,
metadata allowed only for uid 0 (IPv4 and fd20:ce::254), DHCP udp 68->67 any uid, IAP range tcp/22 inbound. This matches the
recipe section 6.4. Residual note: IPv6 ND is not allowed on output, fine because the VM is IPv4-only.

Also noted, not changed: (a) the default network still has `default-allow-ssh` and `default-allow-rdp` from 0.0.0.0/0 (already
recipe open item 9; rdp is new information: 3389 open to the internet on `default`, affects od-l4b/od-cpu1/od-sbx-build);
(b) `60_finalize_image.sh` leaves the guest-agent-created user home directory in place but removes authorized_keys; that is
sufficient because no key survives, and od-sbx1 gets none from metadata.

## 4. What was NOT done

No VM was started, no docker image pulled, no script from build/ executed, `resolve` was not run on the build VM (its
output was reproduced from public endpoints instead, which is why section 1 records the raw upstream values). The kernel
actually running on the build VM, the docker image-store default (F-3) and nft syntax (F-6) therefore remain to be observed
by the `resolve`/preflight run on the VM. `PINS_STATUS` unchanged (CANDIDATE).
