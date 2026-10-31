#!/bin/bash
set -x
mkdir -p ~/jobs
curl -LsSf https://astral.sh/uv/install.sh | sh || echo UV_INSTALL_FAILED
export PATH=$HOME/.local/bin:$PATH
which uv && uv --version
uv venv ~/sgl --python 3.12 || echo UV_VENV_FAILED
. ~/sgl/bin/activate
uv pip install "sglang==0.5.20" 2>&1 | tail -60
echo "rc=$?"
python -c "import sglang, torch; print('sglang', sglang.__version__, 'torch', torch.__version__, torch.version.cuda)"
echo INSTALL_DONE
