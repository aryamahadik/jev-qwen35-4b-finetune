"""A54 (c): merge the admitted held-out (dev-only) question wordings of T01 and T31 into pools_v2 (freeze-v2 style:
backup first, append the wording rows and the lexicon forms with their two real G-LEX votes, re-pin the changed files'
sha256 in MANIFEST.json, add a heldout_a54 block). Source of truth: the overlay's registry (a54_heldout_overlay) over
haiku/heldout/ADMITTED.json + the 14 G-LEX answer files. T07's pools are a sha-checked v1+redo2+redo3 layer stack (its
merged_pools.py); its merge is a separate layer and is not done here.
Run from lean/c2_build:  ../../.venv/bin/python -B zed_orch/a54_merge_heldout_pools.py T01 T31"""
import dataclasses, hashlib, json, shutil, sys
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE / "zed_orch"))
import gen_full_c2 as G  # noqa: E402
import a54_heldout_overlay as OV  # noqa: E402


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def repin(obj, old, new):
    n = 0
    if isinstance(obj, dict):
        for k, v in obj.items():
            if v == old and "sha" in k:
                obj[k] = new; n += 1
            else:
                n += repin(v, old, new)
    elif isinstance(obj, list):
        for v in obj:
            n += repin(v, old, new)
    return n


def merge(fam):
    pools = HERE / "families" / fam / "pools_v2"
    bk = pools / "_backup_a54"
    if bk.exists():
        raise SystemExit(f"{fam}: pools_v2/_backup_a54 exists: already merged")
    adm = {(r["qform"], r["text"]): r for r in OV.admitted_rows(fam)}
    with G.loader_patch(fam), OV.patched(fam):
        with G.PL.open_family(fam) as kit:
            reg, ctx = kit.ctx.lexicon, kit.ctx
            fj = {f["form_id"]: f for f in reg.to_json()["forms"]}
            new = [(sid, sk) for sid, sk in sorted(ctx.skins.items()) if sk.kind == "wording" and sk.held_out]
            forms = [fj[sk.lexicon_ids[0]] for _s, sk in new]
            skins = [(sid, sk) for sid, sk in new]
    files = {"T01": ("wordings.jsonl", "lexicon_registry.json"), "T31": ("wordings.json", "lexicon.json")}[fam]
    bk.mkdir()
    for n in (*files, "MANIFEST.json"):
        shutil.copy2(pools / n, bk / n)
    old = {n: sha(pools / n) for n in files}
    lex = json.loads((pools / files[1]).read_text())
    have = {f["form_id"] for f in lex["forms"]}
    assert not any(f["form_id"] in have for f in forms), "form already in the registry"
    lex["forms"] += forms
    (pools / files[1]).write_text(json.dumps(lex, ensure_ascii=False, indent=1) + "\n")
    if fam == "T01":
        rows = []
        for k, (sid, sk) in enumerate(skins):
            f = next(x for x in forms if x["form_id"] == sk.lexicon_ids[0])
            rows.append({"pid": f"t01h.wording.{sk.qform}.{f['form_id'].split('#')[1]}", "group": "wordings",
                         "task_id": sk.haiku_task_id, "prompt_sha": sk.haiku_prompt_sha, "held_out": True, "text": sk.text,
                         "lexkind": "question", "qform": sk.qform, "sem": f["sem_id"], "slots": f["slots"],
                         "form_id": f["form_id"], "sem_id": f["sem_id"], "kind": "question",
                         "g_lex": {"status": "admitted", "required": 2, "reads": f["extractions"]}})
        with open(pools / files[0], "a", encoding="utf-8") as fh:
            fh.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    else:
        w = json.loads((pools / files[0]).read_text())
        for sid, sk in skins:
            d = json.loads(json.dumps(dataclasses.asdict(sk), default=list))
            d["form_id"] = sk.lexicon_ids[0]
            d.pop("lexicon_ids", None) if "lexicon_ids" not in w["wordings"][0] else None
            w["wordings"].append(d)
        w["count"] = len(w["wordings"])
        (pools / files[0]).write_text(json.dumps(w, ensure_ascii=False, indent=1) + "\n")
    man = json.loads((pools / "MANIFEST.json").read_text())
    pinned = {n: repin(man, old[n], sha(pools / n)) for n in files}
    man["heldout_a54"] = {"ruling": "PREREG A54", "added_wordings": len(skins), "files_before": old,
                          "files_after": {n: sha(pools / n) for n in files}, "repinned": pinned,
                          "source": "families/%s/haiku/heldout/ADMITTED.json + extract answers (2/2 G-LEX)" % fam}
    (pools / "MANIFEST.json").write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n")
    return {"family": fam, "added": len(skins), "sha_before": old, "sha_after": man["heldout_a54"]["files_after"],
            "manifest_sha": sha(pools / "MANIFEST.json"), "repinned": pinned}


if __name__ == "__main__":
    for f in sys.argv[1:]:
        print(json.dumps(merge(f)), flush=True)
