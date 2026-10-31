"""G7 with spec-list metadata (repair3, reported beside the checker's g7.py): g7.main() unchanged except that
qc_lib.meta_feats is replaced by specmeta.meta_feats_spec, so the metadata features are the spec 8 G6 (d) list (what
the model sees in the prompt) and no hidden sidecar tag (decisive mechanism, polarity tag, decile, ...); the unigram /
bigram text features and every null are the checker's. Writes qc/g7_specmeta_<name>.json. Usage: g7_specmeta.py <name>"""
import json, sys
import qc_lib as L
import specmeta
L.meta_feats = specmeta.meta_feats_spec
import g7
g7.L.meta_feats = specmeta.meta_feats_spec
res = g7.main()
res["metadata_features"] = "spec 8 G6 (d) list only (qc/specmeta.py); no sidecar tags"
(L.QC / f"g7_specmeta_{g7.NAME}.json").write_text(json.dumps(res, indent=1))
print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk != "fails_top"})
                  for k, v in res.items()}))
