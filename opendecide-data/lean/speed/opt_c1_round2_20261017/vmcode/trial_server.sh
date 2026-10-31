#!/bin/bash
# trial_server.sh <name> <port> [extra sglang args...]  -- a TRIAL server (never port 30000), same base command as the
# production server (fast_read serve = sglang_host.server_cmd + --attention-backend triton, 32/128/0.8) plus the extra flags.
# Env: TRIAL_MODEL=<dir> (default the merged C1), TRIAL_ENV="K=V K2=V2" extra env, TRIAL_PYPATH=<dir> prepended to PYTHONPATH.
NAME="$1"; PORT="$2"; shift 2
[ "$PORT" = 30000 ] && { echo "refusing port 30000"; exit 2; }
export CUDA_HOME=$HOME/sgl/lib/python3.12/site-packages/nvidia/cu13
mkdir -p ~/bin; ln -sf /usr/bin/g++-12 ~/bin/c++; ln -sf /usr/bin/g++-12 ~/bin/g++
export PATH=$HOME/bin:$HOME/sgl/bin:$CUDA_HOME/bin:$PATH
export CXX=g++-12 TORCH_CUDA_ARCH_LIST=8.9
mkdir -p ~/opt_r2/logs ~/opt_r2/pids
exec ~/od/bin/python -B ~/opt_r2/trial_launch.py --name "$NAME" --port "$PORT" -- "$@"
