#!/usr/bin/env bash
# 00_preflight.sh: read-only checks. Safe to run first, runs nothing generated.
. "$(dirname "$0")/common.sh"
need_root
assert_build_vm
. /etc/os-release
expect_eq "${VERSION_ID}" "24.04" "Ubuntu release"
log "kernel $(uname -r) (gVisor systrap needs >= 5.6; recorded in the image manifest)"
[ -d /sys/fs/cgroup ] && [ -f /sys/fs/cgroup/cgroup.controllers ] || die "cgroup v2 not mounted (docker --pids-limit/--memory need it)"
free_gb=$(df --output=avail -BG / | tail -1 | tr -dc 0-9); [ "${free_gb}" -ge 20 ] || die "need >= 20 GB free, have ${free_gb}"
log "preflight ok; PINS_STATUS=${PINS_STATUS}"
