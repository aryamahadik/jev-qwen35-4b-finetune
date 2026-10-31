"""G6 with spec-list metadata (repair3): the independent checker's g6.py run unchanged except that qc_lib.meta_feats
is replaced by specmeta.meta_feats_spec (the spec 8 (d) list only; no hidden sidecar tags), per the round-1 ruling.
Parts (a)-(c) are the checker's code and inputs, unchanged. Writes qc/g6_specmeta.json (g6.py writes qc/g6.json;
that file is moved aside first and restored after). Usage: g6_specmeta.py [qc_sample]"""
import json, shutil, sys
import qc_lib as L
import specmeta
L.meta_feats = specmeta.meta_feats_spec
import g6
g6.L.meta_feats = specmeta.meta_feats_spec
keep = L.QC / "g6.json"; bak = L.QC / "tmp/g6.json.bak_specmeta"
if keep.exists():
    shutil.copy(keep, bak)
try:
    g6.main()
    d = json.loads(keep.read_text()); d["metadata_features"] = "spec 8 (d) list only (qc/specmeta.py); no sidecar tags"
    (L.QC / "g6_specmeta.json").write_text(json.dumps(d, indent=1))
finally:
    if bak.exists():
        shutil.copy(bak, keep)
