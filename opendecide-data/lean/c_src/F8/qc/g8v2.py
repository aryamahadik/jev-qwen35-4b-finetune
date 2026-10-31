"""G8v2 (PREREG A19) on F8 via the shared tool c_src/common/g8_aflite.py, unchanged. The shared tool has no F8 adapter,
so this wrapper registers one at runtime (the tool file is not edited): F8 views are those of qc/g8.py (question =
last '?' paragraph of `instructions`, card = card + other paragraphs, state; options on choice rows; gold by option
text). Report-only while c_build/g8v2/A19_ADOPTED is absent. Linux only (the tool forks workers).
Usage: g8v2.py <pool path> <out path> [jobs]"""
import sys
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/common")
import g8_aflite as G  # noqa: E402

G.ADAPTERS["F8"] = dict(G._BASE, split="para", sep="\n\n", seed0=8800)
G.FAMILY_G8["F8"] = G.LEAN / "c_src/F8/qc/g8_candidates_r1.json"

if __name__ == "__main__":  # the tool's spawned MiniLM child re-imports this file as __mp_main__
    pool, out = sys.argv[1], sys.argv[2]
    jobs = sys.argv[3] if len(sys.argv) > 3 else "16"
    G.main(["run", "--family", "F8", "--pool", pool, "--out", out, "--jobs", jobs])
