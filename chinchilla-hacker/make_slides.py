"""Step 6: build the slide deck (16:9 PDF) from results.json and figures/*.png.

Writes slides.html (self-contained: fonts and figures embedded) and prints it to
chinchilla_hacker_slides.pdf with headless Chrome.
"""
import base64
import html
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json")))
CHROME = next((p for p in ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                            "/Applications/Google Chrome 2.app/Contents/MacOS/Google Chrome",
                            "/Applications/Chromium.app/Contents/MacOS/Chromium"] if os.path.exists(p)), "google-chrome")


def b64(path):
    return base64.b64encode(open(os.path.join(HERE, path), "rb").read()).decode()


def fig(name, h=None, w=None):
    style = (f"max-height:{h}in;" if h else "") + (f"max-width:{w}in;" if w else "")
    return f'<img class="fig" style="{style}" src="data:image/png;base64,{b64("figures/" + name)}" alt="{name}">'


def sci(x):
    e = len(str(int(x))) - 1
    m = x / 10**e
    return f"10<sup>{e}</sup>" if abs(m - 1) < 0.05 else f"{m:.1f}×10<sup>{e}</sup>"


def human(n):
    for unit, v in (("T", 1e12), ("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if n >= v:
            return f"{n / v:.0f}{unit}" if n / v >= 10 else f"{n / v:.1f}{unit}"
    return f"{n:.0f}"


a1, a2, a3, P = R["approach1"], R["approach2"], R["approach3"], R["paper"]
meta = R["meta"]
iso = R["isoflop"]
per = a2["per_budget"]
tpp = [f["D_opt"] / f["N_opt"] for f in per]
H = R.get("head_to_head")
COS = sorted(R.get("cosine") or [], key=lambda r: r["cycle"])
budgets = R["budgets"]
live = open(os.path.join(HERE, "runs", "live_demo_output.txt")).read().strip() \
    if os.path.exists(os.path.join(HERE, "runs", "live_demo_output.txt")) else ""


def ci(r, k):
    lo, hi = r[k + "_ci"]
    return f'<span class="ci">[{lo:.2f}, {hi:.2f}]</span>'


slides = []


def slide(kicker, title, body, cls=""):
    slides.append((kicker, title, body, cls))


# 1 ------------------------------------------------------------------ title
slide("Hacker role · paper-reading seminar", "", f"""
<div class="title-wrap">
  <h1>Chinchilla on a <span class="o">Laptop</span></h1>
  <p class="sub">We rebuilt the core experiment of Hoffmann et al. (2022), <i>Training Compute-Optimal Large Language
  Models</i>, with {meta['runs']} tiny transformers trained from scratch on a MacBook.</p>
  <div class="stats">
    <div><b>{meta['runs']}</b><span>training runs</span></div>
    <div><b>{meta['seconds'] / 3600:.1f} h</b><span>on an Apple M4 laptop</span></div>
    <div><b>3 / 3</b><span>of the paper's approaches implemented</span></div>
    <div><b class="o">a = {a2['a']:.2f}</b><span>our N<sub>opt</sub> ∝ C<sup>a</sup> (paper 0.49, Kaplan 0.73)</span></div>
  </div>
  <p class="cite">arXiv 2203.15556 · DeepMind · NeurIPS 2022</p>
</div>""", "title")

# 2 ------------------------------------------------------------------ question
slide("The paper's question", "Fixed compute: how big a model, and how much data?", f"""
<div class="cols">
  <div>
    <div class="eq">C ≈ 6 · N · D</div>
    <p class="eq-key"><b>C</b> training FLOPs &nbsp; <b>N</b> parameters &nbsp; <b>D</b> training tokens</p>
    <p>With C fixed, every extra parameter means fewer tokens. So where is the sweet spot, and how does it move
    when C grows?</p>
  </div>
  <div class="rules">
    <div class="rule k"><span class="who">Kaplan et al. (2020)</span><span class="law">N<sub>opt</sub> ∝ C<sup>0.73</sup>, D<sub>opt</sub> ∝ C<sup>0.27</sup></span>
      <span class="what">Spend new compute mostly on size. GPT-3, Gopher and MT-NLG all trained on ~300B tokens.</span></div>
    <div class="rule p"><span class="who">Hoffmann et al. (2022)</span><span class="law">N<sub>opt</sub> ∝ C<sup>0.50</sup>, D<sub>opt</sub> ∝ C<sup>0.50</sup></span>
      <span class="what">Grow size and data equally: about 20 tokens per parameter.</span></div>
    <div class="rule c"><span class="who">The proof</span><span class="law">Chinchilla 70B · 1.4T tokens</span>
      <span class="what">Same compute as Gopher (280B · 300B tokens), yet better on nearly every benchmark:
      MMLU 67.5% vs 60.0%.</span></div>
  </div>
</div>""")

# 3 ------------------------------------------------------------------ paper scale
slide("The paper's result, on its own fitted law", "At Gopher's budget, a 4× smaller model wins", f"""
{fig("fig_paper_scale.png", h=4.35)}
<p class="cap">Paper Eq. 2: L = 1.69 + 406.4/N<sup>0.34</sup> + 410.7/D<sup>0.28</sup>, with C = 6ND. Left: Gopher and Chinchilla share
one budget. Chinchilla sits near the bottom of the curve; Gopher is far to the right. Right: the 2021 giants all sit above
the compute-optimal line. Eq. 2 alone prefers ~32B here; Approaches 1 and 2 say ~67B, so the paper trained 70B.</p>""")

# 4 ------------------------------------------------------------------ setup
slide("What we built", "The same experiment, 10<sup>10</sup>× smaller", f"""
<div class="pipe">
  <div><b>Data</b><span>TinyStories (GPT-4 version), first 200 MB → 197M characters. Character-level, 76 symbols.</span></div>
  <div><b>Models</b><span>nanoGPT-style GPT. 21 shapes, 17K → 6.3M parameters (2–8 layers, width 24–256). Context 64.</span></div>
  <div><b>Compute</b><span>Each run gets an exact FLOP budget, counted as in the paper's Appendix F. Tokens = budget ÷ FLOPs per token.</span></div>
  <div><b>Recipe</b><span>AdamW; cosine learning rate decays 10× and ends when the run ends. One pass over the data. Each run keeps its best of up to 3 batch sizes.</span></div>
</div>
<table class="cmp">
  <tr><th></th><th>Paper</th><th>Us</th></tr>
  <tr><td>Compute budgets (IsoFLOP)</td><td>9 · 6×10<sup>18</sup> – 3×10<sup>21</sup> FLOPs</td><td>{len(budgets)} · {sci(budgets[0])} – {sci(budgets[-1])} FLOPs</td></tr>
  <tr><td>Model sizes</td><td>70M – 16B parameters</td><td>{human(min(r['params'] for r in iso))} – {human(max(r['params'] for r in iso))} parameters</td></tr>
  <tr><td>Training runs</td><td>400+ on TPUs</td><td>{meta['runs']} on one laptop ({meta['seconds'] / 3600:.1f} h)</td></tr>
  <tr><td>Data</td><td>MassiveText, word-piece tokens</td><td>TinyStories, characters (~4 per word-piece token)</td></tr>
</table>""")

# 5 ------------------------------------------------------------------ lr pilot
slide("Step 0 · a fair start", "Give every model size a good learning rate", f"""
<div class="cols wide-left">
  {fig("fig_lr.png", h=4.6)}
  <div class="side">
    <p>If big models get a bad learning rate, they look worse than they are, and the "best size" slides down. So before the
    sweep we tried <b>6 learning rates × 5 sizes</b> at 10<sup>13</sup> FLOPs.</p>
    <p>8e-3 was best, or within about 0.01 of best, for widths up to 128. Wider models went unstable at 8e-3, so they get
    8e-3 × 128 / width.</p>
    <p class="muted">The paper tuned its schedule too; Appendix B shows a mismatched schedule biases the answer.</p>
  </div>
</div>""")

# 6 ------------------------------------------------------------------ isoflop curves
best = ", ".join(f"{human(f['N_opt'])}" for f in per)
slide("Approach 2 · IsoFLOP profiles · paper §3.2, Fig. 3", "Same compute, different sizes: every curve dips", f"""
<div class="cols wide-left">
  {fig("fig_iso_curves.png", h=4.75)}
  <div class="side">
    <p>Each colour is one compute budget. <b>Every dot in a colour used exactly the same FLOPs.</b></p>
    <p><b>Left of the dip:</b> the model is too small to use its data.<br><b>Right of the dip:</b> the budget runs out
    before the big model has read enough.</p>
    <p>A parabola in log N gives each ★: the best size for that budget.<br><span class="mono">{best}</span></p>
  </div>
</div>""")

# 7 ------------------------------------------------------------------ scaling
slide("Approach 2 · the result", "The best size grows like √C, not C<sup>0.73</sup>", f"""
{fig("fig_iso_scaling.png", h=4.1)}
<div class="nums">
  <div><span>our N<sub>opt</sub> ∝ C<sup>a</sup></span><b class="o">a = {a2['a']:.2f}</b>{ci(a2, 'a')}</div>
  <div><span>our D<sub>opt</sub> ∝ C<sup>b</sup></span><b class="o">b = {a2['b']:.2f}</b>{ci(a2, 'b')}</div>
  <div><span>Chinchilla paper</span><b class="p">0.49 / 0.51</b></div>
  <div><span>Kaplan et al.</span><b class="g">0.73 / 0.27</b></div>
  <div><span>best characters per parameter</span><b>{min(tpp):.0f}–{max(tpp):.0f}</b><span class="ci">≈ {min(tpp) / 4:.0f}–{max(tpp) / 4:.0f} tokens</span></div>
</div>""")

# 7b ------------------------------------------------------------------ attempt 1
A1 = R["attempt1"]["approach2"]
DG = R.get("diagnostics") or []
gain = max((d["loss64"] - d["loss_small"] for d in DG), default=0)
slide("What went wrong first", "Our first attempt fell into Kaplan's trap", f"""
{fig("fig_batch_fix.png", h=3.7)}
<p class="cap">Attempt 1 used one batch size (4,096 characters) for every run. At small budgets the bigger models then got only 300–700
optimizer steps and looked far worse than they are, so the best size looked too small there: <b class="g">a = {A1['a']:.2f}</b>, close to
Kaplan's 0.73. Re-running with a smaller batch (same model, compute and data) lowered the loss by up to <b>{gain:.2f}</b>. Attempt 2 trains
each (model, budget) with up to three batch sizes and keeps the best: <b class="o">a = {a2['a']:.2f}</b>. Setup choices like this are what the paper blames for Kaplan's answer.</p>""")

# 8 ------------------------------------------------------------------ envelope
slide("Approach 1 · minimum over training curves · paper §3.1, Fig. 2", "Which run is lowest at each FLOP count?", f"""
{fig("fig_envelope.png", h=4.1)}
<p class="cap">Left: all {len(iso)} training curves (orange = small model, purple = big), plotted against compute spent; black = their lower
envelope. Middle and right: the winning run's size and characters at each FLOP count. Result: <b class="o">a = {a1['a']:.2f}</b> {ci(a1, 'a')},
<b class="o">b = {a1['b']:.2f}</b> {ci(a1, 'b')}; paper 0.50 / 0.50. Our runs all end at 4 budgets, so just past each one only unfinished
runs remain (the jumps), which tilts this estimate toward Kaplan. The paper spread its run ends over many FLOP counts.</p>""")

# 9 ------------------------------------------------------------------ parametric
slide("Approach 3 · parametric fit · paper §3.3, Fig. 4", "Fit the loss itself: L(N, D) = E + A/N<sup>α</sup> + B/D<sup>β</sup>", f"""
{fig("fig_parametric.png", h=3.55)}
<div class="nums">
  <div><span>ours</span><b class="o mono small">L = {a3['E']:.2f} + {a3['A']:.4g}/N<sup>{a3['alpha']:.2f}</sup> + {a3['B']:.4g}/D<sup>{a3['beta']:.2f}</sup></b></div>
  <div><span>paper</span><b class="p mono small">L = 1.69 + 406.4/N<sup>0.34</sup> + 410.7/D<sup>0.28</sup></b></div>
  <div><span>a = β / (α + β)</span><b class="o">{a3['a']:.2f}</b><span class="ci">paper 0.46</span></div>
</div>
<p class="cap">Same recipe as the paper: Huber loss (δ = 10<sup>−3</sup>) on log-loss, L-BFGS from the paper's grid of 4,500 starting points.
Average error {100 * a3['mean_abs_err']:.1f}%. E is the loss no model can beat on this data.</p>""")

# 10 ------------------------------------------------------------------ summary
rows = "".join(f"<tr><td>{n}</td><td class='o'>{r['a']:.2f} {ci(r, 'a')}</td><td class='p'>{P['a'][k]:.2f}</td>"
               f"<td class='o'>{r['b']:.2f} {ci(r, 'b')}</td><td class='p'>{P['b'][k]:.2f}</td></tr>"
               for n, k, r in [("1 · Training-curve envelope", "approach1", a1), ("2 · IsoFLOP profiles", "approach2", a2),
                               ("3 · Parametric fit", "approach3", a3)])
slide("Paper Table 2, rebuilt", "Three approaches: two match the paper", f"""
<div class="cols wide-left">
  {fig("fig_summary.png", h=4.7)}
  <div class="side">
    <table class="t2">
      <tr><th>Approach</th><th>our a</th><th>paper</th><th>our b</th><th>paper</th></tr>
      {rows}
      <tr class="g"><td>Kaplan et al. 2020</td><td>—</td><td>0.73</td><td>—</td><td>0.27</td></tr>
    </table>
    <p class="muted small">Brackets: 10th–90th percentile over 100 refits on 80% of the runs (the paper's method).</p>
    <p>Approaches 2 and 3 sit next to the paper. Approach 1 is higher: our runs all end at 4 budgets, so between them its
    envelope is made of unfinished runs (the mid-schedule bias again). <b>Best estimate: model size and data grow together.</b></p>
  </div>
</div>""")

# 11 ------------------------------------------------------------------ head to head
if H:
    g, c = H["gopher"], H["chinchilla"]
    sg, sc = (html.escape(x["samples"][0][:210]) + "…" for x in (g, c))
    tries = len(H.get("gopher_lrs") or [])
    slide("The headline test · paper §4", "Mini-Gopher vs mini-Chinchilla: same compute", f"""
{fig("fig_head_to_head.png", h=3.2)}
<p class="cap small">Gopher : Chinchilla = 280B : 70B parameters, so mini-Gopher gets 4× the parameters of our compute-optimal model and
~4× fewer characters. It got {tries} tries (batch sizes × learning rates); we show its best.</p>
<div class="samples">
  <div><h4>mini-Gopher · {human(g['params'])} params · {human(g['tokens'])} chars · loss {g['val_loss']:.3f}</h4><p>{sg}</p></div>
  <div class="win"><h4>mini-Chinchilla · {human(c['params'])} params · {human(c['tokens'])} chars · loss {c['val_loss']:.3f}</h4><p>{sc}</p></div>
</div>""")

# 12 ------------------------------------------------------------------ cosine
if COS:
    m = COS[0]
    worst = max(COS, key=lambda r: r["val_loss"])
    slide("One reason Kaplan got 0.73 · paper Appendix B, Fig. A1", "Judging a model mid-schedule makes it look worse", f"""
{fig("fig_cosine.png", h=3.75)}
<p class="cap">One model ({human(m['params'])} params, {human(m['tokens'])} characters), five cosine cycle lengths. Only the matched schedule has
finished decaying when the run ends; at {worst['cycle']:g}× too long the final loss is <b>{worst['val_loss'] - m['val_loss']:+.3f}</b>.
Kaplan et al. read losses part-way through one long schedule. At small budgets the big models are judged earliest, so the best
size looks too small there and the exponent comes out too steep. Later work (Pearce &amp; Song 2024; Porian et al. 2024) adds
other causes: non-embedding parameter counts, warmup and tuning at small scale.</p>""")

# 13 ------------------------------------------------------------------ live demo
if live:
    slide("Live demo", "Run it in class in about a minute", f"""
<div class="cols wide-right">
  <div class="side">
    <p class="mono cmd">python live_demo.py</p>
    <p>Trains two models from scratch on the laptop, each with the same 3×10<sup>12</sup> FLOPs:</p>
    <p><b>mini-Gopher</b>: 4× the parameters, fewer characters.<br><b class="o">mini-Chinchilla</b>: near the compute-optimal size.</p>
    <p class="muted">Recorded output shown here; the numbers vary slightly between runs.</p>
  </div>
  <pre class="term">{html.escape(live)}</pre>
</div>""")

# 14 ------------------------------------------------------------------ evidence
slide("Read with care", "What kind of evidence is this?", f"""
<div class="cols">
  <div>
    <h3 class="ok">What we reproduced</h3>
    <ul>
      <li>IsoFLOP curves have a clear minimum at every budget.</li>
      <li>Approaches 2 and 3 give a = {a2['a']:.2f} and {a3['a']:.2f}, next to the paper's 0.49 and 0.46 and far from Kaplan's 0.73. Approach 1 gives {a1['a']:.2f} (slide 9 says why).</li>
      <li>At equal compute, the smaller model trained on more data wins.</li>
      <li>A cosine schedule longer than the run hurts.</li>
    </ul>
  </div>
  <div>
    <h3 class="warn">Where we differ, and why</h3>
    <ul>
      <li><b>Controlled but tiny:</b> we set N and D ourselves (interventional), but our compute is 10<sup>10</sup>× below Chinchilla's.</li>
      <li><b>One domain:</b> children's stories, character-level. The best ratio ({min(tpp):.0f}–{max(tpp):.0f} characters/param) depends on data and tokenizer; the exponent is what transfers.</li>
      <li><b>Setup matters at this scale:</b> with one fixed batch we measured a = {A1['a']:.2f} (slide 8); letting each run use its best batch changed the answer.</li>
      <li><b>One seed per run</b>, and only {len(budgets)} budgets, so the exponents carry real error bars.</li>
      <li><b>Approach 3 is fragile:</b> a 2024 replication (Besiroglu et al., Epoch AI) found the paper's own Eq. 2 fit inconsistent with its other two approaches.</li>
    </ul>
  </div>
</div>""")

# 15 ------------------------------------------------------------------ code
slide("The code", "About 470 lines run the whole experiment", """
<table class="files">
  <tr><td class="mono">prepare_data.py</td><td>Download 200 MB of TinyStories and encode characters.</td></tr>
  <tr><td class="mono">model.py</td><td>Tiny GPT. Backbone written after Karpathy's nanoGPT (MIT).</td></tr>
  <tr><td class="mono">flops.py</td><td>Compute counted exactly as in the paper's Appendix F.</td></tr>
  <tr><td class="mono">train.py</td><td>One run: exact FLOP budget, matched cosine schedule, one pass over data.</td></tr>
  <tr><td class="mono">sweep.py</td><td>The experiments: lr pilot, IsoFLOP grid, Gopher vs Chinchilla, schedule test.</td></tr>
  <tr><td class="mono">analyze.py</td><td>Approaches 1, 2, 3 (with the paper's bootstrap), all figures, results.json.</td></tr>
  <tr><td class="mono">demo.html</td><td>Interactive page: trade-off explorer, our results, paper-scale calculator, the code.</td></tr>
  <tr><td class="mono">live_demo.py</td><td>One-minute live run for class.</td></tr>
</table>
<p class="muted small">Experiment (data, model, FLOP counting, training, grids): ~470 lines. The three approaches: ~200 lines. The rest draws the
figures, the page and these slides.</p>
<p class="muted small credits">Paper: Hoffmann et al. 2022, arXiv 2203.15556. Backbone: github.com/karpathy/nanoGPT.
Data: TinyStories (Eldan &amp; Li 2023), huggingface.co/datasets/roneneldan/TinyStories.</p>""")


FONTS = [("Plex", "IBMPlexSans-Regular.ttf", 400), ("Plex", "IBMPlexSans-Medium.ttf", 500),
         ("Plex", "IBMPlexSans-SemiBold.ttf", 600), ("Plex", "IBMPlexSans-Bold.ttf", 700),
         ("PlexMono", "IBMPlexMono-Regular.ttf", 400), ("PlexMono", "IBMPlexMono-Medium.ttf", 500)]
font_css = "".join(f"@font-face{{font-family:{f};font-weight:{w};src:url(data:font/ttf;base64,{b64('assets/fonts/' + p)})}}"
                   for f, p, w in FONTS)
font_css += f"@font-face{{font-family:Brico;font-weight:200 800;src:url(data:font/ttf;base64,{b64('assets/fonts/BricolageGrotesque.ttf')})}}"

CSS = font_css + """
@page { size: 13.333in 7.5in; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; background: #fff; }
body { font-family: Plex, sans-serif; color: #1b2230; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.slide { width: 13.333in; height: 7.5in; padding: 0.5in 0.7in 0.55in; position: relative; overflow: hidden;
         page-break-after: always; break-after: page; background: #fcfdff; display: flex; flex-direction: column; }
.kicker { font: 500 12.5pt PlexMono, monospace; letter-spacing: 0.05em; text-transform: uppercase; color: #e8590c; }
h2 { font-family: Brico, Plex, sans-serif; font-weight: 700; font-size: 31pt; line-height: 1.08; letter-spacing: -0.01em;
     margin: 6px 0 16px; }
p, li { font-size: 15.5pt; line-height: 1.42; margin: 0 0 10px; }
.foot { position: absolute; left: 0.7in; right: 0.7in; bottom: 0.22in; display: flex; justify-content: space-between;
        font: 400 10pt PlexMono, monospace; color: #8b93a3; border-top: 1px solid #e3e7ef; padding-top: 6px; }
.o { color: #e8590c; } .p { color: #3b5bdb; } .g { color: #8a919e; }
.muted { color: #5d6678; } .small, .small p { font-size: 12.5pt; }
.mono { font-family: PlexMono, monospace; }
sup, sub { font-size: 0.62em; line-height: 0; }
.fig { display: block; max-width: 100%; margin: 0 auto; object-fit: contain; }
.cap { font-size: 13.5pt; color: #3d4556; margin-top: 12px; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 0.45in; align-items: start; }
.cols.wide-left { grid-template-columns: 1.55fr 1fr; align-items: center; }
.cols.wide-right { grid-template-columns: 1fr 2fr; align-items: center; }
.side p { font-size: 15pt; }
.ci { font: 400 11.5pt PlexMono, monospace; color: #8b93a3; }
/* title */
.slide.title { background: #fcfdff; justify-content: center; }
.slide.title h2 { display: none; }
.title-wrap h1 { font-family: Brico, sans-serif; font-weight: 700; font-size: 68pt; line-height: 0.98; letter-spacing: -0.025em; margin: 10px 0 20px; }
.title-wrap .sub { font-size: 19pt; max-width: 10.4in; color: #1b2230; }
.stats { display: grid; grid-template-columns: repeat(4, 1fr); border-top: 1px solid #dde2ec; border-bottom: 1px solid #dde2ec; margin-top: 28px; }
.stats div { padding: 16px 18px 16px 0; display: flex; flex-direction: column; gap: 4px; }
.stats div + div { padding-left: 18px; border-left: 1px solid #dde2ec; }
.stats b { font: 500 26pt PlexMono, monospace; }
.stats span { font-size: 12.5pt; color: #5d6678; }
.cite { font: 400 11.5pt PlexMono, monospace; color: #8b93a3; margin-top: 22px; }
/* question */
.eq { font: 500 44pt PlexMono, monospace; margin: 10px 0 6px; }
.eq-key { font-size: 13pt; color: #5d6678; margin-bottom: 22px; }
.eq-key b { font-family: PlexMono, monospace; color: #1b2230; }
.rules { display: grid; gap: 12px; }
.rule { border: 1px solid #dde2ec; border-radius: 10px; padding: 12px 16px; display: grid; gap: 2px; background: #fff; }
.rule .who { font: 500 11.5pt PlexMono, monospace; text-transform: uppercase; letter-spacing: 0.04em; }
.rule .law { font: 500 19pt PlexMono, monospace; }
.rule .what { font-size: 13.5pt; color: #3d4556; }
.rule.k .who, .rule.k .law { color: #8a919e; } .rule.p .who, .rule.p .law { color: #3b5bdb; } .rule.c .who, .rule.c .law { color: #e8590c; }
/* setup */
.pipe { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 22px; }
.pipe div { border: 1px solid #dde2ec; border-radius: 10px; padding: 14px 16px; background: #fff; position: relative; }
.pipe div + div::before { content: "→"; position: absolute; left: -12px; top: 42%; transform: translateX(-50%); color: #e8590c; font: 700 16pt Plex; }
.pipe b { display: block; font: 500 12pt PlexMono, monospace; text-transform: uppercase; letter-spacing: 0.05em; color: #e8590c; margin-bottom: 6px; }
.pipe span { font-size: 13pt; line-height: 1.4; display: block; }
table { border-collapse: collapse; width: 100%; }
th, td { text-align: left; padding: 8px 12px; border-bottom: 1px solid #e3e7ef; font-size: 14pt; vertical-align: top; }
th { font: 500 11pt PlexMono, monospace; text-transform: uppercase; letter-spacing: 0.05em; color: #5d6678; }
.cmp td:first-child { color: #5d6678; }
.cmp td:nth-child(3) { color: #e8590c; font-weight: 500; }
/* numbers strip */
.nums { display: flex; flex-wrap: wrap; gap: 10px 34px; margin-top: 14px; align-items: baseline; }
.nums div { display: flex; flex-direction: column; }
.nums span { font-size: 11.5pt; color: #5d6678; }
.nums b { font: 500 21pt PlexMono, monospace; }
.nums b.small { font-size: 15pt; }
.t2 td, .t2 th { font-size: 12.5pt; padding: 7px 8px; }
.t2 td:first-child, .t2 th { white-space: nowrap; }
.t2 .ci { font-size: 8.5pt; display: block; white-space: nowrap; }
/* samples */
.samples { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 12px; }
.samples div { border: 1px solid #dde2ec; border-radius: 10px; padding: 12px 14px; background: #fff; }
.samples div.win { border-color: #e8590c; }
.samples h4 { margin: 0 0 6px; font: 500 10.5pt PlexMono, monospace; color: #5d6678; text-transform: uppercase; letter-spacing: 0.03em; }
.samples p { font: 400 11.5pt/1.5 PlexMono, monospace; margin: 0; }
/* live demo */
.cmd { font-size: 17pt !important; background: #1b2230; color: #fff; padding: 8px 14px; border-radius: 8px; display: inline-block; }
pre.term { background: #151b28; color: #e7eaf2; font: 400 9.4pt/1.45 PlexMono, monospace; padding: 16px 18px; border-radius: 10px;
           white-space: pre-wrap; margin: 0; max-height: 5.4in; overflow: hidden; }
/* evidence */
h3 { font: 500 12.5pt PlexMono, monospace; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 10px; }
h3.ok { color: #0f9f75; } h3.warn { color: #c2410c; }
ul { margin: 0; padding-left: 20px; }
li { font-size: 14pt; margin-bottom: 9px; }
.files td { font-size: 14pt; padding: 8px 12px; }
.files td:first-child { width: 2.3in; color: #e8590c; }
.credits { margin-top: 16px; }
"""


def main():
    n = len(slides)
    body = "".join(
        f'<section class="slide {cls}"><div class="kicker">{k}</div>' + (f"<h2>{t}</h2>" if t else "") + b
        + f'<div class="foot"><span>Chinchilla on a Laptop · Hacker team</span><span>{i + 1} / {n}</span></div></section>'
        for i, (k, t, b, cls) in enumerate(slides))
    page = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Chinchilla on a Laptop</title><style>{CSS}</style></head><body>{body}</body></html>'
    out_html = os.path.join(HERE, "slides.html")
    open(out_html, "w").write(page)
    out_pdf = os.path.join(HERE, "chinchilla_hacker_slides.pdf")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--no-sandbox",
                    f"--print-to-pdf={out_pdf}", "--virtual-time-budget=5000", "file://" + out_html],
                   check=True, capture_output=True)
    print(f"wrote {out_pdf} ({n} slides)")


if __name__ == "__main__":
    main()
