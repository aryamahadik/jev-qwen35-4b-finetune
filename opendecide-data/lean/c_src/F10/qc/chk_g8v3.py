"""G8v3 (PREREG A19 / A19.1 adopted) on F10 via the shared tool c_src/common/g8_aflite.py, unchanged (independent F10
checker, check:F10, c-lanes-v3). The tool has no F10 adapter, so this wrapper registers one at runtime (the tool file
is not edited). F10 views = the tool's 'para' split (question = last paragraph of `instructions` holding '?'; card =
card + the other paragraphs; state); opt_defs=True because decoder_io prints each term's card definition on its option
line when the card defines it (full-card choice rows), so the option view is what the model sees.
Choice part gates (p > 0.009); yes/no part is report-only (A19.1). Usage: chk_g8v3.py <pool path> <out path> [jobs]"""
import sys
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/common")
import g8_aflite as G  # noqa: E402

G.ADAPTERS["F10"] = dict(G._BASE, split="para", sep="\n\n", opt_defs=True, seed0=10100)
G.FAMILY_G8["F10"] = G.LEAN / "c_src/F10/qc/g8_candidates_r1.json"

if __name__ == "__main__":  # the tool's spawned MiniLM child re-imports this file as __mp_main__
    pool, out = sys.argv[1], sys.argv[2]
    jobs = sys.argv[3] if len(sys.argv) > 3 else "2"
    G.main(["run", "--family", "F10", "--pool", pool, "--out", out, "--jobs", jobs])
