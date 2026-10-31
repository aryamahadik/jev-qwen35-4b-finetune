ARG BASE
FROM ${BASE}
# F-GO1 (18 Oct): the TMPDIR=/work baked below is STALE and unused: the executor passes --env TMPDIR=/work/.tmp (config.WORK_TMP) on every run, which
# wins over image ENV. Do not run these images by hand (cmd/go ignores a go.mod in /work when TMPDIR=/work). Changing the ENV here would need step 40.
ENV TZ=UTC LANG=C LC_ALL=C HOME=/work TMPDIR=/work
# starter allow-list of external commands (L-C finalises it); informational copy used by the generator lint
COPY allowlist_sh_commands.txt /etc/od-sbx-allowlist_sh_commands.txt
WORKDIR /work
USER 65534:65534
