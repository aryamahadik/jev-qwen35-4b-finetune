"""G8v3 (PREREG A19 / A19.1 adopted) on F12 via the shared tool c_src/common/g8_aflite.py, unchanged (independent F12
checker, check:F12, c-lanes-v3; wrapper as the F9 checker's). The tool has no F12 adapter, so this wrapper registers
one at runtime (the tool file is not edited). F12 views = the tool's 'para' split (question = last paragraph of
`instructions` holding '?'; card = card + the other paragraphs; state); opt_defs=True (masked / swapped C-OUT and C-ACT
options carry option-definition lines in `card`, which the model sees next to the option, G0 8.1).
Choice part gates (p > 0.009); yes/no part is report-only (A19.1). Usage: chk_g8v3.py <pool path> <out path> [jobs]"""
import sys
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/common")
import g8_aflite as G  # noqa: E402

G.ADAPTERS["F12"] = dict(G._BASE, split="para", sep="\n\n", opt_defs=True, seed0=1200)
G.FAMILY_G8["F12"] = G.LEAN / "c_src/F12/qc/g8_candidates_r1.json"

if __name__ == "__main__":  # the tool's spawned MiniLM child re-imports this file as __mp_main__
    pool, out = sys.argv[1], sys.argv[2]
    jobs = sys.argv[3] if len(sys.argv) > 3 else "2"
    G.main(["run", "--family", "F12", "--pool", pool, "--out", out, "--jobs", jobs])
