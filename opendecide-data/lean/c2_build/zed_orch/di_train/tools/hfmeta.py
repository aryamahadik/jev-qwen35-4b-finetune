import json,sys
from net import gj
for ds in sys.argv[1:]:
    try:
        d=gj(f"https://huggingface.co/api/datasets/{ds}?blobs=false")
        print(ds, "| sha",d.get("sha","")[:10],"| lic",[t for t in d.get("tags",[]) if t.startswith("license")], "| files",[s["rfilename"] for s in d.get("siblings",[])][:16])
        cd=d.get("cardData") or {}
        print("   configs:",[ (c.get("config_name"),c.get("data_files")) for c in (cd.get("configs") or [])][:8])
    except Exception as e: print(ds,"ERR",e)
