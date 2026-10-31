"""Synthetic strings only: is MiniLM-L6 blind to letter case, and to tokens past 256 word pieces?"""
import json, sys
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/common")
import g8_aflite as T
import numpy as np
if __name__ == "__main__":
    base = "Option alpha applies to the north region"
    long = " ".join(["word%d" % (i % 50) for i in range(300)])
    texts = [base, base.upper(), base.title(), long, long + " [ref]", long + " entirely different ending sentence"]
    E = T._encode_worker(texts)
    cos = lambda a, b: float(E[a] @ E[b])
    out = {"cos_lower_vs_upper": round(cos(0, 1), 6), "cos_lower_vs_title": round(cos(0, 2), 6),
           "max_abs_diff_upper": float(np.abs(E[0] - E[1]).max()),
           "cos_long_vs_long_plus_token_after_300_words": round(cos(3, 4), 6),
           "cos_long_vs_long_plus_sentence": round(cos(3, 5), 6)}
    print(json.dumps(out)); open("case_check.json", "w").write(json.dumps(out, indent=1))
