"""G8v3 (PREREG A19 / A19.1 adopted; c_build/g8v2/A19_ADOPTED exists) on F8 via the shared tool
c_src/common/g8_aflite.py, unchanged (independent F8 checker, check:F8, c-lanes-v3). The tool has no F8 adapter, so this
wrapper registers one at runtime (the tool file is not edited); the adapter is the one the earlier F8 checker wrapper
(qc/g8v2.py) used: 'para' split (question = last '?' paragraph of `instructions`; card = card + other paragraphs;
state), options on choice rows, gold by option text, partition seed 8800.
Choice part gates (p > 0.009); yes/no part is report-only (A19.1). Usage: chk_g8v3.py <pool path> <out path> [jobs]"""
import sys
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/common")
import g8_aflite as G  # noqa: E402

G.ADAPTERS["F8"] = dict(G._BASE, split="para", sep="\n\n", seed0=8800)
G.FAMILY_G8["F8"] = G.LEAN / "c_src/F8/qc/g8_candidates_r1.json"

if __name__ == "__main__":  # the tool's spawned MiniLM child re-imports this file as __mp_main__
    pool, out = sys.argv[1], sys.argv[2]
    jobs = sys.argv[3] if len(sys.argv) > 3 else "2"
    G.main(["run", "--family", "F8", "--pool", pool, "--out", out, "--jobs", jobs])
