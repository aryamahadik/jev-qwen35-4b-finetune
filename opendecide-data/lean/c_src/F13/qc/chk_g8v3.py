"""G8v3 (PREREG A19 / A19.1 adopted) on F13 via the shared tool c_src/common/g8_aflite.py, unchanged (independent F13
checker, check:F13, c-lanes-v3; wrapper as the F12 checker's). The tool has no F13 adapter, so this wrapper registers
one at runtime (the tool file is not edited). F13 views = the tool's 'para' split (question = last paragraph of
`instructions` holding '?'; card = card + the other paragraphs; state as 120-word chunks, mean-pooled by the tool, as
F13 G0 10 "AFLite on (card + question + options) and on a mean of chunk embeddings of state"); opt_defs=True (any
option-definition line in `card` is shown next to the option). Choice part gated (p > 0.009); yes/no part
report-only (A19.1). Usage: chk_g8v3.py <pool path> <out path> [jobs]"""
import sys
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/common")
import g8_aflite as G  # noqa: E402

G.ADAPTERS["F13"] = dict(G._BASE, split="para", sep="\n\n", opt_defs=True, seed0=1300)
G.FAMILY_G8["F13"] = G.LEAN / "c_src/F13/qc/g8_candidates_r1.json"

if __name__ == "__main__":  # the tool's spawned MiniLM child re-imports this file as __mp_main__
    pool, out = sys.argv[1], sys.argv[2]
    jobs = sys.argv[3] if len(sys.argv) > 3 else "2"
    G.main(["run", "--family", "F13", "--pool", pool, "--out", out, "--jobs", jobs])
