import sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
from c2_kit import cards as CD
d = sys.argv[1]
rows=[json.loads(l) for l in open(d+'/rows.jsonl')]
rep = CD.token_report(rows)
print(json.dumps(rep, indent=1))
# by qtype and by state/field
import collections
