"""Step 5: build demo.html, the interactive page, from demo_template.html + results.json + our own code.

The code shown on the page is read from the .py files here, so it always matches what actually ran.
Writes demo.html (open it in any browser) and demo_publish.html (the same page without the
<html>/<head>/<body> wrapper, for hosting as an artifact).
"""
import ast
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def grab(path, names):
    """Source of the named top-level functions/assignments in a file, in file order."""
    src = open(os.path.join(HERE, path)).read()
    parts = []
    for node in ast.parse(src).body:
        name = getattr(node, "name", None)
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
        if name in names:
            start = node.lineno - 1
            lines = src.splitlines()
            while start > 0 and lines[start - 1].lstrip().startswith("#"):  # keep the comment above it
                start -= 1
            parts.append("\n".join(lines[start: node.end_lineno]))
    return "\n\n\n".join(parts)


CODE = [
    {"title": "flops.py", "note": "Compute, counted exactly as in the paper's Appendix F. A run's token count is its budget divided by FLOPs per token.",
     "code": grab("flops.py", ["forward_flops_per_sequence", "train_flops_per_token"])},
    {"title": "train.py", "note": "One run: fixed FLOPs, one pass over fresh data, and a cosine schedule that decays 10× and ends exactly when the run ends.",
     "code": grab("train.py", ["lr_at", "run"])},
    {"title": "sweep.py", "note": "The IsoFLOP grid: for every budget, a window of model sizes around the expected optimum.",
     "code": grab("sweep.py", ["LADDER", "BUDGETS", "guess_opt", "stage_isoflop", "stage_gopher", "stage_cosine"])},
    {"title": "approach 2", "note": "Paper §3.2: fit a parabola to each IsoFLOP curve, take its minimum, then fit N_opt ∝ C^a across budgets.",
     "code": grab("analyze.py", ["isoflop_fits", "approach2"])},
    {"title": "approach 1", "note": "Paper §3.1: for each FLOP count, which run's (smoothed) training curve is lowest?",
     "code": grab("analyze.py", ["envelope", "approach1"])},
    {"title": "approach 3", "note": "Paper §3.3 and Appendix D.2: Huber loss (δ = 10⁻³) on log-loss, L-BFGS from the paper's grid of starting points.",
     "code": grab("analyze.py", ["_objective", "fit_parametric"])},
]


def main():
    results = json.load(open(os.path.join(HERE, "results.json")))
    page = open(os.path.join(HERE, "demo_template.html")).read()
    safe = lambda obj: json.dumps(obj).replace("</", "<\\/")  # noqa: E731
    page = page.replace("/*__DATA__*/null", safe(results)).replace("/*__CODE__*/[]", safe(CODE))
    open(os.path.join(HERE, "demo_publish.html"), "w").write(page)
    cut = page.index("</style>") + len("</style>")
    doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
           + page[:cut] + "\n</head>\n<body>\n" + page[cut:] + "\n</body>\n</html>\n")
    open(os.path.join(HERE, "demo.html"), "w").write(doc)
    print(f"wrote demo.html ({len(doc) / 1e3:.0f} KB)")


if __name__ == "__main__":
    main()
