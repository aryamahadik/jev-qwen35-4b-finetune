"""snapcmp.py A.json B.json [--ignore k1,k2]: diff of two SGLang /server_info dumps minus volatile fields. Exit 0 = equal."""
import json, sys
VOL = {"last_gen_throughput", "memory_usage", "startup_time", "uptime", "pid", "port", "nccl_port", "effective_max_running_requests_per_dp"}
def norm(d, ign):
    if isinstance(d, dict):
        return {k: norm(v, ign) for k, v in d.items() if k not in VOL and k not in ign}
    if isinstance(d, list):
        return [norm(x, ign) for x in d]
    return d
def flat(d, pre=""):
    out = {}
    if isinstance(d, dict):
        for k, v in d.items():
            out.update(flat(v, f"{pre}{k}."))
    elif isinstance(d, list) and d and isinstance(d[0], dict):
        for i, v in enumerate(d):
            out.update(flat(v, f"{pre}{i}."))
    else:
        out[pre.rstrip(".")] = d
    return out
def diff(a, b, ign=()):
    fa, fb = flat(norm(a, set(ign))), flat(norm(b, set(ign)))
    return {k: (fa.get(k, "<absent>"), fb.get(k, "<absent>")) for k in sorted(set(fa) | set(fb)) if fa.get(k, "<absent>") != fb.get(k, "<absent>")}
if __name__ == "__main__":
    a, b = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
    ign = sys.argv[4].split(",") if len(sys.argv) > 4 and sys.argv[3] == "--ignore" else []
    d = diff(a, b, ign)
    if not d:
        print("SERVER_INFO_EQUAL"); sys.exit(0)
    print("SERVER_INFO_DIFF", len(d))
    for k, (x, y) in list(d.items())[:60]:
        print(f"  {k}: {str(x)[:90]} -> {str(y)[:90]}")
    sys.exit(1)
