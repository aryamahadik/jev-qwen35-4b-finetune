#!/usr/bin/env bash
# 10_install_base.sh resolve|build: host packages (docker.io, containerd, runc, nftables, tools).
. "$(dirname "$0")/common.sh"
mode_check "${1:-}"; need_root; assert_build_vm
export DEBIAN_FRONTEND=noninteractive
if [ "$1" = build ]; then
  # SKEPTIC 18 Oct (S5, Opus 10.1): unattended-upgrades / apt-daily can change the kernel or hold the dpkg lock mid-build.
  # Stop and mask them FIRST (build mode only; resolve stays read-mostly), then wait for any running apt/dpkg to finish.
  systemctl stop unattended-upgrades.service apt-daily.service apt-daily-upgrade.service apt-daily.timer apt-daily-upgrade.timer 2>/dev/null || true
  systemctl mask unattended-upgrades.service apt-daily.service apt-daily-upgrade.service apt-daily.timer apt-daily-upgrade.timer >/dev/null 2>&1 || true
  for u in unattended-upgrades.service apt-daily.service apt-daily-upgrade.service; do
    st="$(systemctl is-enabled "$u" 2>/dev/null || true)"
    [ "$st" = masked ] || die "$u is '$st', expected masked"
  done
  # step 60 asserts that the newest installed kernel is the running one (a kernel change mid-build would bake the wrong record)
fi
apt-get -o DPkg::Lock::Timeout=300 update -qq
if [ "$1" = resolve ]; then
  for p in docker.io containerd runc nftables; do printf '%s %s\n' "$p" "$(apt-cache policy "$p" | sed -n 3p)"; done
  exit 0
fi
apt-get -o DPkg::Lock::Timeout=300 install -y --no-install-recommends \
  "docker.io=${DOCKER_IO_VERSION}" "containerd=${CONTAINERD_VERSION}" "runc=${RUNC_VERSION}" "nftables=${NFTABLES_VERSION}" \
  ca-certificates curl gnupg jq bzip2 zstd tar xz-utils python3
apt-mark hold docker.io containerd runc nftables
systemctl enable docker.service >/dev/null

# SKEPTIC 18 Oct (M5, Opus 10.1): the GCE guest agent's default `[Accounts] groups` list includes `docker`, so the operator's
# account would get docker.sock (root-equivalent) at SSH login, AFTER the boot-time ST-1.7 has passed. Override the list.
# UNVERIFIED on the VM: confirm the agent's default list first with `grep -r docker /etc/default/instance_configs.cfg* /usr/share/google*`
# and `systemctl status google-guest-agent` (service name). Step 60 and run-batch re-assert that the docker group is empty.
install -d -m 0755 /etc/default
cat >/etc/default/instance_configs.cfg <<'CFG'
[Accounts]
groups = adm,dip,lxd,plugdev,video
CFG
chmod 0644 /etc/default/instance_configs.cfg
grep -qx 'groups = adm,dip,lxd,plugdev,video' /etc/default/instance_configs.cfg || die "instance_configs.cfg was not written"
for svc in google-guest-agent.service google-guest-agent; do
  if systemctl cat "$svc" >/dev/null 2>&1; then systemctl restart "$svc" && break; fi
done
# if the agent already put an account into the docker group (it re-syncs users after docker.io appears), remove them now
for m in $(docker_group_members); do gpasswd -d "$m" docker >/dev/null; log "removed $m from the docker group"; done
# docker group stays EMPTY: nobody gets docker.sock by group (sock = root-equivalent). The executor runs under sudo.
getent group docker >/dev/null && [ -z "$(docker_group_members)" ] || die "docker group is not empty"
log "base packages installed and held"
