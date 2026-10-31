#!/bin/bash
# usage: start_server.sh <serve args...>   (runs on od-l4b)
export CUDA_HOME=$HOME/sgl/lib/python3.12/site-packages/nvidia/cu13
mkdir -p ~/bin; ln -sf /usr/bin/g++-12 ~/bin/c++; ln -sf /usr/bin/g++-12 ~/bin/g++
export PATH=$HOME/bin:$HOME/sgl/bin:$CUDA_HOME/bin:$PATH
export CXX=g++-12
export TORCH_CUDA_ARCH_LIST=8.9
cd ~/reads
~/od/bin/python -B fast_read.py stop >/dev/null 2>&1
sleep 2
: > ~/jobs/sglang_server.log
~/od/bin/python -B fast_read.py serve "$@"
echo rc=$?
