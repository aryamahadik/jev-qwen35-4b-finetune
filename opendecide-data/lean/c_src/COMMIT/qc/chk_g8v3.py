"""G8v3 (PREREG A19 / A19.1 adopted) on COMMIT via the shared tool c_src/common/g8_aflite.py, unchanged (independent
COMMIT checker, check:COMMIT, c-lanes-v3). The tool has no COMMIT adapter, so this wrapper registers one at runtime (the
tool file is not edited). Views = the tool's 'para' split (question = last paragraph of `instructions` holding '?';
card = card + other paragraphs; state). Choice rows: the card text is dropped from the card view (strip_card_choice:
decoder_io shows choice rows only the option definition lines, A16.1 g) and opt_defs=True (decoder_io prints each
option's card definition on its option line), so every view is what the model sees.
Choice part gates (p > 0.009); yes/no part is report-only (A19.1). Usage: chk_g8v3.py <pool path> <out path> [jobs]"""
import sys
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/common")
import g8_aflite as G  # noqa: E402

G.ADAPTERS["COMMIT"] = dict(G._BASE, split="para", sep="\n\n", strip_card_choice=True, opt_defs=True, seed0=13100)
G.FAMILY_G8["COMMIT"] = G.LEAN / "c_src/COMMIT/qc/g8_family_none.json"
G.OUTDIR = G.LEAN / "c_src/COMMIT/tmp/chk/g8"  # keep run cache and embeddings inside c_src/COMMIT
G.CACHE = G.OUTDIR / "cache"

if __name__ == "__main__":  # the tool's spawned MiniLM child re-imports this file as __mp_main__
    pool, out = sys.argv[1], sys.argv[2]
    jobs = sys.argv[3] if len(sys.argv) > 3 else "2"
    G.main(["run", "--family", "COMMIT", "--pool", pool, "--out", out, "--jobs", jobs])
