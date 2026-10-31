import sys,os,json,time
sys.path.insert(0,os.path.dirname(__file__))
from net import get,sha
SRC=sys.argv[1]
F=[("logical_entailment","google-deepmind/logical-entailment-dataset","159e76834434c0d29b3588ce8b94e6004697f455",["data/train.txt","LICENSE","README.md"]),
   ("temporal_nli","kunalkukreja21/temporal-expressions-evaluation-lm","384ebf53ed5b4c53cc035c5f48d4d4693c06c509",["data/cs1_train.csv","data/cs2_train.csv","data/cs3_train.csv","LICENSE","README.md"]),
   ("perspectrum","CogComp/perspectrum","b42c27b85f20f2a35c0a0895698fa242ccf160ab",["data/dataset/perspectrum_with_answers_v1.0.json","data/dataset/dataset_split_v1.0.json","data/dataset/perspective_pool_v1.0.json","data/dataset/license.txt","data/dataset/README.md","README.md"])]
pins={}
for name,repo,c,files in F:
    os.makedirs(f"{SRC}/{name}",exist_ok=True); pins[name]={"repo":repo,"commit":c,"files":{}}
    for f in files:
        u=f"https://raw.githubusercontent.com/{repo}/{c}/{f}"
        b=get(u,timeout=180); out=f"{SRC}/{name}/"+f.replace("/","__")
        open(out,"wb").write(b); pins[name]["files"][f]={"url":u,"sha256":sha(b),"bytes":len(b)}
        print(name,f,len(b),sha(b)[:12],flush=True)
json.dump(pins,open(f"{SRC}/../SRC_PINS.json","w"),indent=1)
