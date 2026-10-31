#!/usr/bin/env bash
# 60_finalize_image.sh build: write IMAGE_MANIFEST.json, scrub the disk, power off. Run last, on the build VM.
# The Mac then creates the custom image from the stopped boot disk (see IMAGE_RECIPE.md section 8).
. "$(dirname "$0")/common.sh"
mode_check "${1:-}"; [ "$1" = build ] || die "no resolve mode"; need_root; assert_build_vm
M="${SBX_ROOT}/IMAGE_MANIFEST.json"
LAUNCH="${SBX_ROOT}/executor/od_sbx_launcher.py"

# ---- gates (fail before anything is written) ----
# M5 (Opus 10.1): the guest agent must not have put anyone into the docker group since step 10.
[ -z "$(docker_group_members)" ] || die "docker group is not empty: $(docker_group_members | tr '\n' ' ')"
grep -qx 'groups = adm,dip,lxd,plugdev,video' /etc/default/instance_configs.cfg || die "instance_configs.cfg lost its groups override"
# the newest installed kernel must be the running one (an image that boots a different kernel than the recorded one is not what was reviewed)
kern="$(uname -r)"; need kernel "${kern}"
newest="$(ls /boot/vmlinuz-* | sed 's|/boot/vmlinuz-||' | sort -V | tail -1)"; need "newest installed kernel" "${newest}"
expect_eq "${newest}" "${kern}" "newest installed kernel vs running kernel"
# F-6: the unit's ruleset must still parse
nft -c -f /etc/od-sbx/hostfw.nft || die "/etc/od-sbx/hostfw.nft does not pass nft -c"
mnt="$(grep -c ' /srv/od-sbx/stage tmpfs ' /etc/fstab || true)"; expect_eq "${mnt}" "1" "stage tmpfs line in /etc/fstab"

# ---- manifest values: assign first, assert non-empty (M2: a failing $(cmd) inside `jq --arg` does NOT trip set -e) ----
img_id() { docker image inspect --format '{{.Id}}' "od-sbx/$1:${PINS_STATUS,,}"; }
built_utc="$(date -u +%FT%TZ)"; need built_utc "${built_utc}"
os="$(. /etc/os-release; echo "$PRETTY_NAME")"; need os "${os}"
runsc_line="$(runsc --version | head -1)"; need runsc_line "${runsc_line}"
dockerv="$(dpkg-query -W -f='${Version}' docker.io)"; need docker_io "${dockerv}"
containerdv="$(dpkg-query -W -f='${Version}' containerd)"; need containerd "${containerdv}"
runcv="$(dpkg-query -W -f='${Version}' runc)"; need runc "${runcv}"
nftv="$(dpkg-query -W -f='${Version}' nftables)"; need nftables "${nftv}"
pyhost="$(dpkg-query -W -f='${Version}' python3)"; need host_python3 "${pyhost}"                    # S5: the executor runs on this
pinsh="$(sha256_of "${SBX_SRC}/pins.env")"; need pins_env_sha256 "${pinsh}"
lockh="$(sha256_of "${SBX_ROOT}/requirements.lock")"; need requirements_lock_sha256 "${lockh}"
exech="$(/usr/bin/python3 -I "${LAUNCH}" treehash "${SBX_ROOT}/executor")"; need executor_py_tree_sha256 "${exech}"   # M1: via the launcher
expect_eq "${#exech}" "64" "executor tree hash length"
stor="$(docker info --format '{{.Driver}}')"; need docker_storage_driver "${stor}"                      # F-3 / M6
expect_eq "${stor}" "overlay2" "docker storage driver"
pyid="$(img_id python)"; need python_image_id "${pyid}"
ndid="$(img_id node)";   need node_image_id "${ndid}"
goid="$(img_id go)";     need go_image_id "${goid}"
shid="$(img_id sh)";     need sh_image_id "${shid}"
for v in "${pyid}" "${ndid}" "${goid}" "${shid}"; do case "${v}" in sha256:*) ;; *) die "image id '${v}' is not sha256:...";; esac; done
need GVISOR_VERSION "${GVISOR_VERSION}"; need PYTEST_VERSION "${PYTEST_VERSION}"

jq -n \
  --arg built_utc "${built_utc}" --arg kernel "${kern}" --arg os "${os}" \
  --arg runsc "${runsc_line}" --arg gv "${GVISOR_VERSION}" \
  --arg docker "${dockerv}" --arg containerd "${containerdv}" --arg runc "${runcv}" --arg nft "${nftv}" \
  --arg pyhost "${pyhost}" --arg storage "${stor}" \
  --arg pins "${pinsh}" --arg lock "${lockh}" --arg exec "${exech}" \
  --arg py "${PY_VERSION}" --arg pyd "${PY_DIGEST}" --arg pyid "${pyid}" \
  --arg nd "${NODE_VERSION}" --arg ndd "${NODE_DIGEST}" --arg ndid "${ndid}" \
  --arg go "${GO_VERSION}" --arg god "${GO_DIGEST}" --arg goid "${goid}" \
  --arg shd "${SH_DIGEST}" --arg shid "${shid}" --arg pytest "${PYTEST_VERSION}" \
  '{built_utc:$built_utc, kernel:$kernel, os:$os, runsc_version_line:$runsc, gvisor_release:$gv,
    docker_io:$docker, containerd:$containerd, runc:$runc, nftables:$nft, host_python3:$pyhost, docker_storage_driver:$storage,
    pins_env_sha256:$pins, requirements_lock_sha256:$lock, executor_py_tree_sha256:$exec, pytest:$pytest,
    toolchains:{
      python:{version:$py, base_digest:$pyd, image_id:$pyid},
      node:{version:$nd, base_digest:$ndd, image_id:$ndid},
      go:{version:$go, base_digest:$god, image_id:$goid},
      sh:{base_digest:$shd, image_id:$shid}}}' >"$M"
# the written manifest must carry no empty string (belt and braces for M2)
jq -e '[.. | strings | select(length == 0)] | length == 0' "$M" >/dev/null || die "IMAGE_MANIFEST.json contains an empty value"
chmod 0644 "$M"; log "wrote ${M}"
# --- scrub (no credentials or history may enter the image) ---
rm -f /home/*/.ssh/authorized_keys /home/*/.ssh/known_hosts /root/.ssh/authorized_keys /root/.bash_history /home/*/.bash_history
rm -rf /home/*/.gnupg /root/.gnupg /var/tmp/* /tmp/* /var/lib/apt/lists/* /var/cache/apt/archives/*.deb
docker image prune -f >/dev/null
cloud-init clean --logs 2>/dev/null || true
truncate -s 0 /etc/machine-id; rm -f /var/lib/dbus/machine-id
journalctl --rotate >/dev/null 2>&1; journalctl --vacuum-time=1s >/dev/null 2>&1 || true
sync
log "scrubbed. Powering off; the Mac creates the image from the stopped disk."
systemctl poweroff
