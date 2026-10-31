import sys, pickle, collections
sys.dont_write_bytecode=True; sys.path.insert(0,'.')
from families.T43 import probes as PR
rows=pickle.load(open(sys.argv[1],'rb'))
labs={"fixes the bug":0,"does not fix the bug":1,"passes the target test but is still wrong":2}
c=collections.defaultdict(lambda:[0,0,0]); n=0
for r,st in rows:
    if st["head"]!="pv" or r["gold"] not in labs: continue
    f=PR.size_features(st)
    key=(st["kind"],f["hunks"],f["added"],f["removed"])
    c[key][labs[r["gold"]]]+=1
for k in sorted(c):
    t=sum(c[k]); 
    if t>=60: print(k,t,[round(x/t,3) for x in c[k]])
