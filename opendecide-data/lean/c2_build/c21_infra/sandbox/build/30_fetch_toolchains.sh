#!/usr/bin/env bash
# 30_fetch_toolchains.sh resolve|build
#  resolve: print the current index digest of each pinned tag, and write vendor/requirements.proposed.txt
#           (pytest + its dependencies with sha256 hashes). Changes nothing frozen. The skeptic re-runs this.
#  build:   pull each image BY DIGEST (never by tag), confirm the digest, download the wheels with
#           --require-hashes against the frozen vendor/requirements.lock, verify, stage under /opt/od-sbx.
# Nothing here executes toolchain code except `pip download`, run inside the pinned python image.
. "$(dirname "$0")/common.sh"
mode_check "${1:-}"; need_root; assert_build_vm
command -v docker >/dev/null || die "run 10_install_base.sh first"

declare -A REPO=( [py]="${PY_REPO}" [node]="${NODE_REPO}" [go]="${GO_REPO}" [sh]="${SH_REPO}" )
declare -A TAG=(  [py]="${PY_TAG}"  [node]="${NODE_TAG}"  [go]="${GO_TAG}"  [sh]="${SH_TAG}" )
declare -A DIG=(  [py]="${PY_DIGEST}" [node]="${NODE_DIGEST}" [go]="${GO_DIGEST}" [sh]="${SH_DIGEST}" )

if [ "$1" = resolve ]; then
  for k in py node go sh; do
    # docker buildx imagetools is not installed; use the registry HTTP API for the index digest
    name="${REPO[$k]#docker.io/}"
    tok="$(curl -fsS "https://auth.docker.io/token?service=registry.docker.io&scope=repository:${name}:pull" | jq -r .token)"
    d="$(curl -fsSI -H "Authorization: Bearer ${tok}" \
        -H 'Accept: application/vnd.oci.image.index.v1+json, application/vnd.docker.distribution.manifest.list.v2+json' \
        "https://registry-1.docker.io/v2/${name}/manifests/${TAG[$k]}" | tr -d '\r' | awk 'tolower($1)=="docker-content-digest:"{print $2}')"
    printf '%-4s %s:%s observed=%s pinned=%s %s\n' "$k" "${REPO[$k]}" "${TAG[$k]}" "$d" "${DIG[$k]}" \
      "$([ "$d" = "${DIG[$k]}" ] && echo SAME || echo DIFFERENT)"
  done
  # wheels: resolve inside the pinned python image (network on, build VM has no data)
  docker pull "${PY_REPO}@${PY_DIGEST}" >/dev/null
  mkdir -p "${SBX_SRC}/vendor"
  docker run --rm --user 65534 -e HOME=/tmp -e PIP_DISABLE_PIP_VERSION_CHECK=1 --tmpfs /tmp:rw,exec,size=512m \
    "${PY_REPO}@${PY_DIGEST}" sh -c \
    "python -m pip download --only-binary=:all: --dest /tmp/w pytest==${PYTEST_VERSION} >/dev/null && python -m pip hash /tmp/w/*.whl" \
    | python3 -I "${SBX_SRC}/build/lock_from_pip_hash.py" >"${SBX_SRC}/vendor/requirements.proposed.txt"
  log "wrote vendor/requirements.proposed.txt ($(wc -l <"${SBX_SRC}/vendor/requirements.proposed.txt") wheels); review, then copy to requirements.lock"
  exit 0
fi

# ---- build mode ----
ensure_classic_store
install -d -m 0755 "${SBX_ROOT}" "${SBX_ROOT}/wheels" "${SBX_ROOT}/images"
for k in py node go sh; do
  docker pull "${REPO[$k]}@${DIG[$k]}" >/dev/null
  # SKEPTIC 18 Oct: docker normalises familiar names, so RepoDigests holds `python@sha256:..` (no `docker.io/library/` prefix) and the
  # old string compare against `docker.io/library/python@sha256:..` would fail on the first build. Compare the DIGEST part, and
  # require that some RepoDigests entry carries it (not just entry 0).
  rds="$(docker image inspect --format '{{range .RepoDigests}}{{println .}}{{end}}' "${REPO[$k]}@${DIG[$k]}")"
  need "RepoDigests of ${k}" "${rds}"
  printf '%s\n' "${rds}" | sed 's/.*@//' | grep -qx -- "${DIG[$k]}" || die "digest of ${k}: none of '${rds}' ends in ${DIG[$k]}"
  log "pulled ${k}: ${rds}"
done
[ -s "${SBX_SRC}/${REQUIREMENTS_LOCK}" ] || die "${REQUIREMENTS_LOCK} missing (run resolve, review, freeze)"
grep -q -- '--hash=sha256:' "${SBX_SRC}/${REQUIREMENTS_LOCK}" || die "lock file has no hashes"
cp "${SBX_SRC}/${REQUIREMENTS_LOCK}" "${SBX_ROOT}/requirements.lock"
docker run --rm --user 0 -e HOME=/tmp -e PIP_DISABLE_PIP_VERSION_CHECK=1 --tmpfs /tmp:rw,exec,size=512m \
  -v "${SBX_ROOT}/requirements.lock:/req.lock:ro" -v "${SBX_ROOT}/wheels:/out" \
  "${PY_REPO}@${PY_DIGEST}" python -m pip download --require-hashes --only-binary=:all: --no-deps -r /req.lock -d /out
( cd "${SBX_ROOT}/wheels" && sha256sum -- *.whl >SHA256SUMS )
log "wheels: $(ls "${SBX_ROOT}/wheels"/*.whl | wc -l) files vendored"
