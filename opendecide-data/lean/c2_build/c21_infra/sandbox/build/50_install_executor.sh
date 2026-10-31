#!/usr/bin/env bash
# 50_install_executor.sh build: docker daemon config, host firewall unit (installed + enabled, NOT started here, so the
# build VM keeps its egress until step 60), executor, toolchain images loaded into the docker store.
. "$(dirname "$0")/common.sh"
mode_check "${1:-}"; [ "$1" = build ] || die "no resolve mode"; need_root; assert_build_vm
command -v nft >/dev/null || die "nft missing (run 10_install_base.sh)"
# SKEPTIC 18 Oct (F-6, Opus M6): a syntax error in a policy-drop oneshot unit leaves the VM with no firewall or a half-applied one.
# `nft -c` parses and checks the ruleset WITHOUT applying it (the build VM keeps its egress).
nft -c -f "${SBX_SRC}/host/hostfw.nft" || die "hostfw.nft does not pass nft -c"
python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "${SBX_SRC}/host/docker-daemon.json" || die "docker-daemon.json is not valid JSON"
install -d -m 0755 /etc/docker /etc/od-sbx "${SBX_ROOT}/executor" "${SBX_ROOT}/bin" /var/lib/od-sbx /srv/od-sbx
install -d -m 0700 /srv/od-sbx/stage
install -m 0644 "${SBX_SRC}/host/docker-daemon.json" /etc/docker/daemon.json
install -m 0644 "${SBX_SRC}/host/hostfw.nft" /etc/od-sbx/hostfw.nft
install -m 0644 "${SBX_SRC}/host/od-sbx-hostfw.service" /etc/systemd/system/od-sbx-hostfw.service
install -m 0644 "${SBX_SRC}/host/od-sbx-selftest.service" /etc/systemd/system/od-sbx-selftest.service
# SKEPTIC 18 Oct (M4, Opus 10.1): /out and /in are bind mounts of STAGE_ROOT; on the 40 GB boot disk one 60 s suite run could write
# many 64 MB files and fill the disk mid-batch. Mount STAGE_ROOT as a size-capped tmpfs (512 MiB: it must stay BELOW the 1g container memory limit, because pages written through a
# bind mount of a host tmpfs are charged to the container's memory cgroup, so a cap at or above the limit is never reached before an OOM
# kill and ST-4.7 could not pass; /in is bounded by the 256m /work copy). fstab + nofail so a mount problem
# can never block boot (ST-4.7 then fails loudly because findmnt will not show a tmpfs at that path).
grep -q ' /srv/od-sbx/stage ' /etc/fstab || \
  echo 'tmpfs /srv/od-sbx/stage tmpfs mode=0700,uid=0,gid=0,size=512M,nr_inodes=100k,nosuid,nodev,nofail 0 0' >>/etc/fstab
systemctl daemon-reload
rm -rf "${SBX_ROOT}/executor/od_sbx"; cp -r "${SBX_SRC}/executor/od_sbx" "${SBX_ROOT}/executor/od_sbx"
install -m 0644 "${SBX_SRC}/executor/od_sbx_launcher.py" "${SBX_ROOT}/executor/od_sbx_launcher.py"
find "${SBX_ROOT}/executor" -name __pycache__ -prune -exec rm -rf {} +
chown -R root:root "${SBX_ROOT}"; chmod -R go-w "${SBX_ROOT}"
# M1: `python3 -I` ignores PYTHONPATH (-I implies -E), so the wrapper runs the launcher FILE, which sets sys.path itself.
printf '#!/bin/sh\nexec /usr/bin/python3 -I %s/executor/od_sbx_launcher.py "$@"\n' "${SBX_ROOT}" >"${SBX_ROOT}/bin/od-sbx"
chmod 0755 "${SBX_ROOT}/bin/od-sbx"
# the launcher must really import the package under -I (treehash needs no docker and runs nothing generated)
th="$(/usr/bin/python3 -I "${SBX_ROOT}/executor/od_sbx_launcher.py" treehash "${SBX_ROOT}/executor")"
[ "${#th}" = 64 ] || die "launcher self-check failed (treehash='${th}')"
# daemon.json sets runsc as the default runtime; restart so the images load under the final config
systemctl restart docker
for n in python node go sh; do zstd -dc "${SBX_ROOT}/images/od-sbx-${n}.tar.zst" | docker load; done
info="$(docker info --format '{{.DefaultRuntime}} {{json .Runtimes}}')"
case "${info}" in runsc\ *) ;; *) die "runsc is not the default docker runtime (${info})";; esac
# F-3 (Opus M6): the image store decides what `.Id` means; daemon.json pins overlay2 + classic store. Assert it, step 60 records it.
drv="$(docker info --format '{{.Driver}}')"; need "docker storage driver" "${drv}"
expect_eq "${drv}" "overlay2" "docker storage driver"
ds="$(docker info --format '{{json .DriverStatus}}')"
case "${ds}" in *containerd*) die "docker is using the containerd image store (daemon.json features not applied): ${ds}";; esac
# smoke test of the final stack BEFORE the image is baked: runsc must start a container on this kernel (open item 6). This runs only
# the image's own python on a literal, nothing generated. The build VM has no hostfw yet, but --network none applies anyway.
pyid="$(docker image inspect --format '{{.Id}}' "od-sbx/python:${PINS_STATUS,,}")"; need "python image id" "${pyid}"
smoke="$(docker run --rm --runtime runsc --network none --read-only --cap-drop ALL --user 65534:65534 "${pyid}" python -c 'print(6*7)')"
expect_eq "${smoke}" "42" "runsc smoke test"
systemctl enable od-sbx-hostfw.service od-sbx-selftest.service
log "executor installed under ${SBX_ROOT}; hostfw + selftest units enabled (not started)"
