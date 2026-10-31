"""A54: T07's fourth pool layer pools/heldout_a54/ (wordings_add.json, lexicon_add.json, MANIFEST.json), sha-checked by
merged_pools.load() like redo2 / redo3. The 9 admitted held-out (dev-only) question wordings (authoring task
T07-author_wording-b3433fbc-000; G-LEX reads T07-extract_lex-57ea7527-000 / 9261e31a-000, 2/2). Source: the overlay's
registry over haiku/heldout/ADMITTED.json + the two answer files. Run once from lean/c2_build:
  ../../.venv/bin/python -B zed_orch/a54_merge_t07_layer.py"""
import hashlib, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE / "zed_orch"))
import gen_full_c2 as G  # noqa: E402
import a54_heldout_overlay as OV  # noqa: E402

FAM = "T07"
T07 = HERE / "families" / FAM
OUT = T07 / "pools" / "heldout_a54"


def sha_f(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    if OUT.exists():
        raise SystemExit("pools/heldout_a54 already exists")
    adm = {r["value"]: r for r in json.loads((OV.held_dir(FAM) / "ADMITTED.json").read_text())["admitted"]}
    with G.loader_patch(FAM), OV.patched(FAM):
        with G.PL.open_family(FAM) as kit:
            reg = kit.ctx.lexicon
            fj = {f["form_id"]: f for f in reg.to_json()["forms"]}
            new = [(sid, sk) for sid, sk in sorted(kit.ctx.skins.items()) if sk.kind == "wording" and sk.held_out
                   and sk.text in adm]
    words, forms = [], []
    for sid, sk in new:
        fid = sk.lexicon_ids[0]
        f = fj[fid]
        piece = adm[sk.text]["piece_id"]
        words.append({"wording_id": "T07-word-" + hashlib.sha256(piece.encode()).hexdigest()[:12], "piece_id": piece,
                      "internal_id": piece.split("#")[0], "form_id": fid, "qform": sk.qform, "held_out": True,
                      "text": sk.text, "haiku_task_id": sk.haiku_task_id, "haiku_prompt_sha": sk.haiku_prompt_sha})
        forms.append({"form_id": fid, "sem_id": f["sem_id"], "kind": "question", "text": sk.text,
                      "origin": "haiku_wording_a54", "piece_id": piece, "qform": sk.qform, "held_out": True,
                      "source": "haiku", "haiku_task_id": sk.haiku_task_id, "extractions": f["extractions"],
                      "status": "admitted"})
    assert len(words) == len(forms) == 9 and all(f["status"] == "admitted" for f in forms), len(words)
    OUT.mkdir()
    (OUT / "wordings_add.json").write_text(json.dumps({"family": FAM, "version": "a54", "n": len(words), "items": words},
                                                      ensure_ascii=False, indent=1) + "\n")
    (OUT / "lexicon_add.json").write_text(json.dumps({"family": FAM, "version": "a54", "pool": "lexicon", "forms": forms},
                                                     ensure_ascii=False, indent=1) + "\n")
    ex = OV.held_dir(FAM) / "extract" / "answers"
    man = {"family": FAM, "version": "a54", "g0_sha256": json.loads((T07 / "pools" / "redo3" / "MANIFEST.json").read_text())["g0_sha256"],
           "status": "held-out wording supplement (PREREG A54), dev and sealed side only; no G13-seed scan", "ready": True,
           "inputs": {"answer_sha256": {p.stem: sha_f(p) for p in sorted(ex.glob("*.json"))},
                      "admitted_sha256": sha_f(OV.held_dir(FAM) / "ADMITTED.json"),
                      "authoring_answers": {p.stem: sha_f(p) for p in sorted((OV.held_dir(FAM) / "answers").glob("*.json"))},
                      "baseline_manifest_sha256": {"v1": sha_f(T07 / "pools" / "MANIFEST.json"),
                                                   "redo2": sha_f(T07 / "pools" / "redo2" / "MANIFEST.json"),
                                                   "redo3": sha_f(T07 / "pools" / "redo3" / "MANIFEST.json")}},
           "pool_files": {n: {"sha256": sha_f(OUT / n)} for n in ("wordings_add.json", "lexicon_add.json")},
           "merge_rule": "wordings: + wordings_add.json items; lexicon: + lexicon_add.json forms (status admitted only); "
                         "ids and texts must be new (merged_pools.merge_heldout)",
           "counts": {"wordings": len(words), "forms": len(forms),
                      "by_qform": {q: sum(1 for w in words if w["qform"] == q) for q in sorted({w['qform'] for w in words})}}}
    (OUT / "MANIFEST.json").write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps({"files": man["pool_files"], "manifest_sha": sha_f(OUT / "MANIFEST.json"), "counts": man["counts"]}))


main()
