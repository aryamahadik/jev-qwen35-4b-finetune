#!/usr/bin/env bash
# 40_build_toolchain_images.sh build: derive the four od-sbx toolchain images FROM the digest-pinned bases.
# Derived builds run with --network=none: everything they need (wheels) is already local.
. "$(dirname "$0")/common.sh"
mode_check "${1:-}"; [ "$1" = build ] || die "no resolve mode"; need_root; assert_build_vm
IMG="${SBX_SRC}/images"
CTX="$(mktemp -d /var/tmp/odctx.XXXXXX)"; trap 'rm -rf "$CTX"' EXIT
cp -r "${SBX_ROOT}/wheels" "$CTX/wheels"; cp "${SBX_ROOT}/requirements.lock" "$CTX/requirements.lock"
cp "${SBX_SRC}/images/allowlist_sh_commands.txt" "${SBX_SRC}/images/pytest.trusted.ini" "$CTX/"
cp -r "${SBX_SRC}/images/gowarm" "$CTX/gowarm"      # M3: module used only to pre-warm the Go std build cache (Dockerfile.go)
build() {  # name, dockerfile, buildargs...
  local n="$1" f="$2"; shift 2
  DOCKER_BUILDKIT=0 docker build --network=none --pull=false --no-cache -t "od-sbx/${n}:${PINS_STATUS,,}" -f "${IMG}/${f}" "$@" "$CTX"
}
build python Dockerfile.python --build-arg "BASE=${PY_REPO}@${PY_DIGEST}"
build node   Dockerfile.node   --build-arg "BASE=${NODE_REPO}@${NODE_DIGEST}"
build go     Dockerfile.go     --build-arg "BASE=${GO_REPO}@${GO_DIGEST}"
build sh     Dockerfile.sh     --build-arg "BASE=${SH_REPO}@${SH_DIGEST}"
for n in python node go sh; do
  docker save "od-sbx/${n}:${PINS_STATUS,,}" | zstd -q -19 -o "${SBX_ROOT}/images/od-sbx-${n}.tar.zst"
  log "saved ${n}: id=$(docker image inspect --format '{{.Id}}' "od-sbx/${n}:${PINS_STATUS,,}")"
done
