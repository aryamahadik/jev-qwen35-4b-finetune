"""trial_launch.py --name N --port P -- <extra sglang args>: start a trial SGLang server (own pidfile/log), wait for health,
save its /server_info and the diff against the production snapshot (only the intended flags may differ)."""
import argparse, json, os, signal, subprocess, sys, time, pathlib
_o = pathlib.Path.exists
def _s(self, *a, **k):
    try: return _o(self, *a, **k)
    except PermissionError: return False
pathlib.Path.exists = _s
H = pathlib.Path.home(); W = H / "opt_r2"
sys.path[:0] = [str(H / "lean" / "hosting"), str(H / "lean"), str(W)]
import sglang_host as SH
import snapcmp
ap = argparse.ArgumentParser(); ap.add_argument("--name", required=True); ap.add_argument("--port", type=int, required=True)
ap.add_argument("--boot-timeout", type=int, default=1500)
a, extra = ap.parse_known_args()
extra = [x for x in extra if x != "--"]
model = os.environ.get("TRIAL_MODEL", str(H / "models" / "q35_4b_main500k_merged"))
cmd = SH.server_cmd(model, fp8=False, port=a.port, max_running_requests=32, max_mamba_cache_size=128,
                    mem_fraction_static=0.8, python=str(H / "sgl" / "bin" / "python"))
cmd += ["--attention-backend", "triton"]
for fl in os.environ.get("DROP_FLAGS", "").split():       # base flags the trial REPLACES (flag + its value, if any)
    while fl in cmd:
        i = cmd.index(fl)
        j = i + 2 if i + 1 < len(cmd) and not cmd[i + 1].startswith("--") else i + 1
        del cmd[i:j]
cmd += extra
env = SH.server_env()
for kv in os.environ.get("TRIAL_ENV", "").split():
    k, v = kv.split("=", 1); env[k] = v
if os.environ.get("TRIAL_PYPATH"):
    env["PYTHONPATH"] = os.environ["TRIAL_PYPATH"]
(W / "results" / a.name).mkdir(parents=True, exist_ok=True)
log = open(W / "logs" / f"{a.name}.server.log", "ab")
t0 = time.time()
p = subprocess.Popen(cmd, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
(W / "pids" / f"{a.name}.pid").write_text(str(p.pid))
(W / "pids" / "current_trial.pid").write_text(str(p.pid))
print("launched trial", a.name, "pid", p.pid, "port", a.port, flush=True)
print(" ".join(cmd), flush=True)
import urllib.request
def get(path, t=10):
    return urllib.request.urlopen(f"http://127.0.0.1:{a.port}{path}", timeout=t).read()
ok = False
while time.time() - t0 < a.boot_timeout:
    if p.poll() is not None:
        print("SERVER EXITED rc", p.returncode, "see", W / "logs" / f"{a.name}.server.log", flush=True); sys.exit(3)
    try:
        get("/health"); ok = True; break
    except Exception:
        time.sleep(4)
if not ok:
    os.killpg(os.getpgid(p.pid), signal.SIGTERM); print("BOOT TIMEOUT"); sys.exit(4)
boot = round(time.time() - t0, 1)
info = json.loads(get("/server_info", 30))
(W / "results" / a.name).mkdir(parents=True, exist_ok=True)
json.dump(info, open(W / "results" / a.name / "server_info.json", "w"), indent=1)
print("BOOT_OK", a.name, boot, "s", flush=True)
ref = W / "snap" / "T0_server_info.json"
if not ref.exists():
    ref = W / "snap" / "prod_server_info_first.json"
d = snapcmp.diff(json.load(open(ref)), info)
d = {k: v for k, v in d.items() if "port" not in k.split(".")[-1] or True}
print("DIFF vs", ref.name, len(d), flush=True)
for k, (x, y) in list(d.items())[:40]:
    print(f"  {k}: {str(x)[:70]} -> {str(y)[:70]}")
