"""A20 a adoption test 2: G8v2 on F5, local vs remote -> same pass/fail and real shares within the seed spread."""
import json
import sys

loc, rem = (json.load(open(p)) for p in sys.argv[1:3])
TIMING = {"seconds", "jobs", "cache"}
out = {"pass_local": loc["pass"], "pass_remote": rem["pass"], "same_pass": loc["pass"] == rem["pass"],
       "pool_sha256_same": loc["pool_sha256"] == rem["pool_sha256"], "parts": {}}
ok = out["same_pass"] and out["pool_sha256_same"]
for part, lp in loc["parts"].items():
    rp = rem["parts"][part]
    sd = max(lp["partition_seed_spread"]["sd"], rp["partition_seed_spread"]["sd"])
    tol = round(2 * sd, 4)
    d = {"share_local": lp["real"]["share"], "share_remote": rp["real"]["share"],
         "delta_share": round(rp["real"]["share"] - lp["real"]["share"], 4), "seed_sd": sd, "tolerance_2sd": tol,
         "seed_shares_local": lp["partition_seed_spread"]["shares"],
         "seed_shares_remote": rp["partition_seed_spread"]["shares"],
         "acc_local": lp["real"]["acc"], "acc_remote": rp["real"]["acc"],
         "threshold_local": lp["threshold"], "threshold_remote": rp["threshold"],
         "pass_local": lp["pass"], "pass_remote": rp["pass"]}
    d["share_within_spread"] = abs(d["delta_share"]) <= tol
    d["same_part_pass"] = lp["pass"] == rp["pass"]
    ok = ok and d["share_within_spread"] and d["same_part_pass"]
    out["parts"][part] = d
out["identical_json_except_timing"] = ({k: v for k, v in loc.items() if k not in TIMING} ==
                                       {k: v for k, v in rem.items() if k not in TIMING})
out["seconds_local"], out["seconds_remote"] = loc.get("seconds"), rem.get("seconds")
out["jobs_local"], out["jobs_remote"] = loc.get("jobs"), rem.get("jobs")
out["pass"] = ok
print(json.dumps(out, indent=1))
