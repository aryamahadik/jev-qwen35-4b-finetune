"""G8v3 (PREREG A19 / A19.1 adopted) on F9 via the shared tool c_src/common/g8_aflite.py, unchanged (independent F9
checker, check:F9, c-lanes-v3). The tool has no F9 adapter, so this wrapper registers one at runtime (the tool file is
not edited). F9 views = the tool's 'para' split (question = last paragraph of `instructions` holding '?'; card = card +
the other paragraphs; state); opt_defs=False (F9 options carry no definitions: G0 1.10, choice rows have card null).
Choice part gates (p > 0.009); yes/no part is report-only (A19.1). Usage: chk_g8v3.py <pool path> <out path> [jobs]"""
import sys
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/common")
import g8_aflite as G  # noqa: E402

G.ADAPTERS["F9"] = dict(G._BASE, split="para", sep="\n\n", opt_defs=False, seed0=9100)
G.FAMILY_G8["F9"] = G.LEAN / "c_src/F9/qc/g8_candidates_r1.json"

if __name__ == "__main__":  # the tool's spawned MiniLM child re-imports this file as __mp_main__
    pool, out = sys.argv[1], sys.argv[2]
    jobs = sys.argv[3] if len(sys.argv) > 3 else "2"
    G.main(["run", "--family", "F9", "--pool", pool, "--out", out, "--jobs", jobs])
