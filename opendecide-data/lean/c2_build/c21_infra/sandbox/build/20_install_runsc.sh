#!/usr/bin/env bash
# 20_install_runsc.sh resolve|build: gVisor from the signed apt repo, pinned version, then cross-checked against
# the SHA-512 in pins.env. `runsc install` (legacy auto-download path) is NEVER used.
. "$(dirname "$0")/common.sh"
mode_check "${1:-}"; need_root; assert_build_vm
W="$(mktemp -d /var/tmp/runsc.XXXXXX)"; trap 'rm -rf "$W"' EXIT
KEY=/usr/share/keyrings/gvisor-archive-keyring.gpg
curl -fsS -m 30 "${GVISOR_APT_KEY_URL}" -o "$W/archive.key"
# SKEPTIC 18 Oct: the file must hold exactly ONE primary key and it must match the pin. (The old awk took the first `fpr` line only,
# so a second key appended to the file would have been trusted by `gpg --dearmor` below without being checked.)
fprs="$(gpg --show-keys --with-colons "$W/archive.key" | awk -F: '$1=="pub"{p=1; next} $1=="fpr" && p{print $10; p=0}')"
expect_eq "$(printf '%s\n' "${fprs}" | grep -c .)" "1" "number of primary keys in gVisor archive.key"
expect_eq "${fprs}" "${GVISOR_APT_KEY_FPR}" "gVisor apt key fingerprint"
gpg --dearmor <"$W/archive.key" >"$KEY"
echo "deb [arch=amd64 signed-by=${KEY}] ${GVISOR_APT_URL} ${GVISOR_APT_SUITE} main" >/etc/apt/sources.list.d/gvisor.list
apt-get update -qq
if [ "$1" = resolve ]; then
  apt-cache policy runsc | sed -n 1,6p
  curl -fsS -m 30 "${GVISOR_APT_URL}/dists/${GVISOR_APT_SUITE}/main/binary-amd64/Packages" | grep -E '^(Version|SHA256|SHA512|Filename):'
  exit 0
fi
# fetch the deb ourselves first and check both hashes, then let dpkg install that exact file
( cd "$W" && apt-get download "runsc=${GVISOR_VERSION}" )
deb="$(ls "$W"/runsc_*.deb)"
expect_eq "$(sha256_of "$deb")" "${GVISOR_DEB_SHA256}" "runsc deb sha256"
expect_eq "$(sha512_of "$deb")" "${GVISOR_DEB_SHA512}" "runsc deb sha512"
# SKEPTIC 18 Oct (F-2, Opus M6): the deb's postinst runs `runsc install --clobber=false` and reloads docker when /etc/docker/daemon.json
# exists. The recipe never uses the legacy installer, so refuse to install if anything created daemon.json before step 50.
[ ! -e /etc/docker/daemon.json ] || die "/etc/docker/daemon.json exists before runsc install (the runsc postinst would edit it)"
dpkg -i "$deb"
[ ! -e /etc/docker/daemon.json ] || die "runsc postinst created /etc/docker/daemon.json (step 50 owns that file)"
apt-mark hold runsc
# independent cross-check: the release bundle's SHA-512 matches pins.env (proves the pin is the upstream release)
curl -fsS -m 300 "${GVISOR_BUNDLE_URL}" -o "$W/gvisor.tar.bz2"
expect_eq "$(sha512_of "$W/gvisor.tar.bz2")" "${GVISOR_BUNDLE_SHA512}" "gvisor bundle sha512"
command -v runsc >/dev/null || die "runsc not on PATH after install"
ver="$(runsc --version | head -1)"   # --version only prints the version; does not start a sandbox
log "installed: ${ver}"
case "${ver}" in *"${GVISOR_VERSION%%.*}"*) ;; *) die "runsc version '${ver}' does not match ${GVISOR_VERSION}";; esac
# register the runtime by hand (no `runsc install`): daemon.json is written by 50_install_executor.sh
log "runsc installed; daemon.json is written in step 50"
