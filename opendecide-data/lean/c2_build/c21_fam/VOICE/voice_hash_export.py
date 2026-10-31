"""TEMPLATE / TABLE HASH EXPORT for VOICE (plan 16.1; VOICE addendum v3.2 section 3 "a table or phrase-pool change after hash export v1.1 means a new
hash export and re-made variants for the changed table"). HASHES ONLY, NO TEXT: every string in the export is a sha256 digest, a path, an id or a key.

    python3 voice_hash_export.py --write | --check

Hashed: every .py file of the lane and of solver B; the closed code tables (symbol table, letter names, aliases, fillers, strata / band / share
constants, number-word tables, span-checker word lists ...); the dictated-NATURAL phrase table (every template, folder / file word, flag phrase) and the
disfluency table; the names manifest and namespace.py. One `template_hash` over all of it is stamped on every variant.
NOT BUILT (listed so that building it is a visible change): generator C (VGEN-C: PN-SWAP, HOMOPH-SWAP, BOUNDARY-SHIFT), the dictionary-licence record.
"""
import argparse
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(os.path.dirname(HERE), "GEN")
for _p in (HERE, GEN):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import gen_hash_export as GX                              # noqa: E402  (GEN/gen_hash_export.py: the shared helpers)

OUT = os.path.join(HERE, "HASH_EXPORT.json")
EXPORT_VERSION = "v1.1-skeptic-18oct"
MODULES = ("vcommon", "numwords", "verbalizer", "noiser", "disfluency", "span_check", "wer", "voice_check", "pool", "vgates")
SB_MODULES = ("vb_tables", "vb_numbers", "vb_hyp", "vb_check", "vb_denorm", "vb_wer")
UNBUILT = {"generators": ["VGEN-C (PN-SWAP, HOMOPH-SWAP, BOUNDARY-SHIFT)"], "records": ["dictionary licence record (V-C11)", "misaki lexicon licence re-check"],
           "gpu_steps": ["Kokoro round trip", "pinned Nemotron ASR", "V-D1..V-D4 measurements"]}


def code_files():
    out = [os.path.join(HERE, f) for f in sorted(os.listdir(HERE)) if f.endswith(".py")]
    sb = os.path.join(HERE, "solver_b")
    out += [os.path.join(sb, f) for f in sorted(os.listdir(sb)) if f.endswith(".py")]
    return out


def build_export(created=None):
    sys.path.insert(0, os.path.join(HERE, "solver_b"))
    import vcommon
    rel = lambda p: os.path.relpath(p, HERE).replace(os.sep, "/")           # noqa: E731
    code = {rel(p): GX.sha_file(p) for p in code_files()}
    # files of the other lanes' directories that voice_check / vcommon import: a change there is a change of the VOICE pipeline
    for p in (os.path.join(GEN, "stamp_hook.py"), os.path.join(GEN, "gen_common.py"), os.path.join(GX.C2_BUILD, "c21_infra", "pathskip.py")):
        code["shared/" + os.path.basename(p)] = GX.sha_file(p)
    tables = GX.module_tables(MODULES + SB_MODULES)
    tables.update({"vcommon.table_hashes." + k: v for k, v in vcommon.table_hashes().items()})
    pdir = os.path.join(HERE, "pools")
    with open(os.path.join(pdir, "natural_phrase_table.json"), "r", encoding="utf-8") as f:
        nat = json.load(f)
    with open(os.path.join(pdir, "disfluency_table.json"), "r", encoding="utf-8") as f:
        dis = json.load(f)
    pools = {
        "files": {fn: GX.sha_file(os.path.join(pdir, fn)) for fn in ("natural_phrase_table.json", "disfluency_table.json")},
        "natural_phrase_table": {"ops": GX.template_block(nat["ops"]), "folder_words": [GX.sha_text(w) for w in nat["folder_words"]],
                                 "file_words": [GX.sha_text(w) for w in nat["file_words"]],
                                 "flag_phrases": {k: GX.sha_text(v) for k, v in sorted(nat["flag_phrases"].items())},
                                 "table_sha256": GX.sha_obj({k: nat[k] for k in ("ops", "folder_words", "file_words", "flag_phrases")})},
        "disfluency_table": {k: [GX.sha_text(w) for w in v] if isinstance(v, list) else GX.sha_obj(v) for k, v in sorted(dis.items())
                             if k in ("fillers", "politeness", "repair_words", "false_start_max")},
    }
    exp = {"export": "VOICE template and table hash export (hashes only, no text)", "family": "VOICE", "version": EXPORT_VERSION, **GX.META,
           "code": code, "code_aggregate_sha256": GX.sha_obj(code), "tables": tables, "tables_aggregate_sha256": GX.sha_obj(tables), "pools": pools,
           "unbuilt": UNBUILT, "names": {os.path.basename(p): GX.sha_file(p) for p in GX.names_files()}}
    exp["template_hash"] = GX.sha_obj({"code": exp["code_aggregate_sha256"], "tables": exp["tables_aggregate_sha256"], "pools": pools, "names": exp["names"]})
    exp["export_sha256"] = GX.sha_obj(exp)
    exp["created_utc"] = created or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")      # outside export_sha256
    return exp


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    exp = build_export()
    if args.write:
        print("wrote", OUT, "file sha256", GX.write_export(exp, OUT), "template_hash", exp["template_hash"], "export_sha256", exp["export_sha256"])
        return 0
    if args.check:
        try:
            on_disk = json.load(open(OUT, "r", encoding="utf-8"))
        except OSError:
            print("no HASH_EXPORT.json")
            return 1
        on_disk.pop("created_utc", None)
        exp.pop("created_utc", None)
        print("CURRENT" if on_disk == exp else "STALE")
        return 0 if on_disk == exp else 1
    print(json.dumps({"template_hash": exp["template_hash"], "export_sha256": exp["export_sha256"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
