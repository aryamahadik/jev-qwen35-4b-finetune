#!/usr/bin/env bash
# post_session.sh: billing after, live apps/containers check (jaypatil-duke only)
cd "$(dirname "$0")/../../../.."   # opendecide-data
export MODAL_PROFILE=jaypatil-duke
H=lean/speed/opt_c1_round2_20261017/h100
date -u +%FT%TZ > $H/billing/after.utc
.venv/bin/modal billing summary --json > $H/billing/summary_after.json 2>&1
.venv/bin/modal billing report --for today --resolution h --show-resources --json > $H/billing/report_today_after.json 2>&1
echo "== apps"; .venv/bin/modal app list 2>&1 | head -20
echo "== containers"; .venv/bin/modal container list 2>&1 | head -20
