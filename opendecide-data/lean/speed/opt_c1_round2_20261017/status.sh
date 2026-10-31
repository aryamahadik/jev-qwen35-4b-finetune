#!/usr/bin/env bash
./vm.sh od-cpu1 'cd ~/opt_r2/voice/out; python3 - <<PY
import glob,collections
c=collections.OrderedDict()
for f in sorted(glob.glob("*.jsonl")):
    k=f.split(".shard")[0].replace(".jsonl",""); c[k]=c.get(k,0)+sum(1 for _ in open(f))
print("  ".join(f"{k}:{v}" for k,v in c.items()))
PY
uptime | sed "s/.*load/load/"; grep -h done ~/jobs/r2_voice_asr2.log ~/jobs/r2_voice_eot.log 2>/dev/null | tail -4; tail -n 2 ~/jobs/r2_voice_c1.log'
