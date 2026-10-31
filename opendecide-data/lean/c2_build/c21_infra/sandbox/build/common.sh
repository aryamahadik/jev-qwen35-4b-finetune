#!/usr/bin/env bash
# Shared helpers for the od-sbx image build. Source, do not execute.
# Runs ONLY on the build VM od-sbx-build (egress allowed, no data, no service account).
set -euo pipefail
umask 022

SBX_SRC="${SBX_SRC:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"   # the sandbox/ directory copied to the VM
SBX_ROOT=/opt/od-sbx
# shellcheck source=../pins.env
. "${SBX_SRC}/pins.env"

log()  { printf '[%s] %s\n' "$(date -u +%H:%M:%SZ)" "$*"; }
die()  { printf 'FATAL: %s\n' "$*" >&2; exit 1; }
need_root() { [ "$(id -u)" = 0 ] || die "run with sudo"; }

# mode: "resolve" (network, proposes values, writes nothing frozen) or "build" (needs PINS_STATUS=FROZEN).
mode_check() {
  case "${1:-}" in
    resolve) ;;
    build) [ "${PINS_STATUS}" = FROZEN ] || die "pins.env is ${PINS_STATUS}; build mode needs FROZEN (skeptic + Opus)";;
    *) die "usage: $0 resolve|build";;
  esac
}

md() { curl -fsS -m 10 -H 'Metadata-Flavor: Google' "http://169.254.169.254/computeMetadata/v1/$1"; }

# Refuse to run anywhere except the build VM: name, label, no service account, no extra disk.
assert_build_vm() {
  [ "$(md instance/name)" = od-sbx-build ] || die "not od-sbx-build"
  [ "$(md instance/attributes/block-project-ssh-keys 2>/dev/null || true)" = TRUE ] || die "block-project-ssh-keys not TRUE"
  local sa; sa="$(md instance/service-accounts/ 2>/dev/null || true)"
  [ -z "${sa//[$'\n ']/}" ] || die "a service account is attached: ${sa}"
  local ndisk; ndisk="$(md instance/disks/ | grep -c .)"
  [ "${ndisk}" = 1 ] || die "expected exactly 1 disk (boot), found ${ndisk}"
}

sha256_of() { sha256sum "$1" | cut -d' ' -f1; }
sha512_of() { sha512sum "$1" | cut -d' ' -f1; }
expect_eq() { [ "$1" = "$2" ] || die "$3: got '$1' expected '$2'"; }
# SKEPTIC 18 Oct (M2): `--arg x "$(cmd)"` does not trip `set -e`, so a failed command silently became an empty value.
# Always assign to a variable first (the assignment DOES trip `set -e`), then assert it is non-empty: need NAME "$NAME".
need() { [ -n "${2:-}" ] || die "empty value for $1"; }

# docker group members, one per line (empty output = empty group). Used by steps 10, 50 and 60 (M5).
docker_group_members() { getent group docker | cut -d: -f4 | tr ',' '\n' | grep -v '^$' || true; }

# SKEPTIC 18 Oct (F-3, Opus M6): Docker 29 uses the containerd image store on fresh installs, where `.Id`, RepoDigests and
# save/load round trips behave differently. Pin the classic overlay2 store for steps 30-40 with a MINIMAL daemon.json written AFTER
# the runsc deb is installed (F-2: its postinst must not see a daemon.json). Step 50 replaces it with host/docker-daemon.json,
# which carries the same two keys. Skipped if a daemon.json already exists (re-run after step 50).
ensure_classic_store() {
  if [ ! -e /etc/docker/daemon.json ]; then
    install -d -m 0755 /etc/docker      # Docker >= 23 no longer needs /etc/docker/key.json, so the packaged directory may not exist yet
    printf '{\n  "storage-driver": "overlay2",\n  "features": { "containerd-snapshotter": false }\n}\n' >/etc/docker/daemon.json
    systemctl restart docker
  fi
  local drv; drv="$(docker info --format '{{.Driver}}')"
  expect_eq "${drv}" "overlay2" "docker storage driver (classic store)"
}
