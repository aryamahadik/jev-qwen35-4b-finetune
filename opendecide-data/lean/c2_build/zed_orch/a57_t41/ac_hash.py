"""A57 C2-side hash compare against c2_build/sealed_hashes_ac/ (hash exports only). Counts only; nothing printed per hit text.
Verifies MANIFEST.json file shas, then reuses g13_c2.ohs4_hash_hits (same FORMAT.md compare) on an AC-backed Exports."""
import hashlib, json, sys
from collections import defaultdict
from pathlib import Path
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
import g13_c2 as G  # noqa: E402

AC = C2 / "sealed_hashes_ac"

def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

class ACExports(G.Exports):
    def __init__(self, root=AC):
        man = json.loads((root / "MANIFEST.json").read_text())
        for name, h in man["sha256"].items():
            if name == "source_keywords_prelim.jsonl":
                continue
            if sha_file(root / name) != h:
                raise G.ExportError(f"{name} differs from MANIFEST.json")
        self.manifest = man
        self.manifest_sha = sha_file(root / "MANIFEST.json")
        self.ng = {n: self._grams(root / f"ngrams{n}_sha256.npy") for n in (10, 12)}
        self.sets = defaultdict(set)
        for f in ("text_hashes.jsonl", "structure_hashes.jsonl", "keyword_hashes.jsonl"):
            for line in (root / f).read_text(encoding="utf-8").splitlines():
                if line.strip():
                    r = json.loads(line); self.sets[r["kind"]].add(r["hash"])
        for f, kinds in man["records"].items():
            if isinstance(kinds, dict):
                for k, n in kinds.items():
                    if len(self.sets[k]) != n:
                        raise G.ExportError(f"kind {k}: {len(self.sets[k])} != {n}")
        self.struct = {k[:-2]: self.sets[k[:-2] + "_R"] | self.sets[k[:-2] + "_U"]
                       for k in self.STRUCT_KINDS if k.endswith("_R")}

def check_texts(ex, texts, cut=False):
    """texts: {key: [text,...]} -> (hit keys by method, counts). cut=True for slotted templates."""
    units = [{"key": k, "texts": [("f", t) for t in ts], "template": cut} for k, ts in texts.items()]
    hits, rep = G.ohs4_hash_hits(units, ex)
    return hits, rep

def selftest(ex):
    t = "The quick brown fox jumps over the lazy dog while seven bakers sing loudly near the old harbour wall."
    assert G.sha_hex(G.norm(t)) == "bcae36e66bee28e419f6c66999314f636d9af10f99a082aa60217adbc3705862"
    assert G.gram_digests(G.words(t), 10)[0].hex() == "100f4b5d5ad9f8b1e0f70e122374bcb151ee5108e3323e981322588380a0121c"
    assert G.gram_digests(G.words(t), 12)[0].hex() == "b3bf0c9691b60f8273f9f31cc8fabae58029194949363bacec931eabbd2b257d"
    assert G.sha_hex("example keyword") == "867c3db642f0e99f2aea32ff92be5c9a543dd1c028c4b12b24e76e589719f679"
    return True
