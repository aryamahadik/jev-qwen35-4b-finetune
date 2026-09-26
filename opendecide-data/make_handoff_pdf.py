"""Build OpenDecide_handoff.pdf: everything done and learned so far, for continuing in a new session."""
import json
import re
from pathlib import Path
from xml.sax.saxutils import escape as esc

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, KeepTogether

HERE = Path(__file__).resolve().parent
LEAN = HERE / "lean"
REPO = HERE.parent
OUT = HERE / "OpenDecide_handoff.pdf"

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=16, spaceAfter=6, textColor=colors.HexColor("#1d3557"))
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=12.5, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor("#1d3557"))
B = ParagraphStyle("B", parent=ss["BodyText"], fontSize=9.5, leading=12.5, alignment=TA_LEFT)
SM = ParagraphStyle("SM", parent=B, fontSize=8, leading=10)
CODE = ParagraphStyle("CODE", parent=B, fontName="Courier", fontSize=7.8, leading=9.6, backColor=colors.HexColor("#f4f4f4"),
                      leftIndent=6, rightIndent=6, borderPadding=4)
CELL = ParagraphStyle("CELL", parent=B, fontSize=7.8, leading=9.4)


def P(t, s=B):
    return Paragraph(t, s)


def bullets(items, s=B):
    return [Paragraph((("&nbsp;&nbsp;&nbsp;&nbsp;&ndash; " + i[len("&nbsp;&nbsp;- "):]) if i.startswith("&nbsp;&nbsp;- ") else ("&bull; " + i)), s) for i in items]


def code(t):
    return Paragraph(esc(t).replace("\n", "<br/>").replace("  ", "&nbsp;&nbsp;"), CODE)


def table(rows, widths, header=True, font=7.8):
    data = [[Paragraph(str(c), ParagraphStyle("c", parent=CELL, fontSize=font, leading=font + 1.6)) for c in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#999999")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]
    if header:
        st += [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef6"))]
    t.setStyle(TableStyle(st))
    return t


# ---------------- load results ----------------
res = json.loads((LEAN / "results/results.json").read_text())
M = res["models"]
stats = json.loads((LEAN / "data/stats.json").read_text())
v01_lines = [l.replace("|P(A)+P(not A)−1|", "P(A)+P(not A)-1").replace("|ΔP|", "dP").replace("−", "-").replace("↓", "(lower better)").replace("↑", "(higher better)")
             for l in (LEAN / "archive_v01/RESULTS_v01.md").read_text().splitlines() if l.startswith("| ")]


def f(m, k, pct=True):
    v = M.get(m, {}).get(k)
    if v is None:
        return "-"
    if isinstance(v, dict) and "v" in v:
        g = (lambda x: f"{100 * x:.1f}") if pct else (lambda x: f"{x:.3f}")
        return f"{g(v['v'])} [{g(v['lo'])}-{g(v['hi'])}]"
    if isinstance(v, float):
        return f"{100 * v:.1f}" if pct else f"{v:.3f}"
    return str(v)


MODELS = [("edge_zeroshot", "GLiClass Edge 32.7M, untrained"), ("base_zeroshot", "GLiClass modern-base 151M, untrained"),
          ("edge_A0", "Edge fine-tuned A0 (base rows only)"), ("edge_A3", "Edge fine-tuned A3 (ours: + consistency + robustness)")]
METRICS = [("Choice accuracy, in-domain (%)", "choice_acc_ID", True), ("Choice accuracy, zero-shot (%)", "choice_acc_ZS", True),
           ("Yes/no acc., base question, ID (%)", "noul_base_acc_ID", True), ("Yes/no acc., base question, ZS (%)", "noul_base_acc_ZS", True),
           ("Yes/no acc., negated question (unseen style), ID (%)", "noul_neg_acc_ID", True),
           ("Yes/no acc., negated question (unseen style), ZS (%)", "noul_neg_acc_ZS", True),
           ("Complement violation |P(A)+P(not A)-1| (lower better)", "complement_violation", False),
           ("Contradiction rate (%) (lower better)", "complement_contradiction_rate", True),
           ("Pairs summing to 1 +/-0.05 (%)", "complement_within_0.05", True),
           ("Paraphrase flip rate (%) (lower better)", "paraphrase_flip_rate", True),
           ("Double-negation drift (lower better)", "double_negation_drift", False),
           ("Brier, yes/no core (lower better)", "brier_noul_core", False), ("ECE, yes/no core (lower better)", "ece_noul_core", False),
           ("Coverage @1% error, cross-fitted (%)", "coverage@1%_crossfit", True),
           ("Injection attack success, held-out families C+D (%) (lower better)", "inj_ASR_pooled", True),
           ("Choice acc. under injection C / same items clean (%)", None, True),
           ("Echo-control choice acc. (%)", "inj_E_choice_acc", True),
           ("Distractor choice acc. / same items clean (%)", None, True)]

story = []
# ---------------- title ----------------
story += [P("OpenDecide: handoff document", ParagraphStyle("T", parent=ss["Title"], fontSize=20)),
          P("Everything done and learned so far, so the work can continue in a new chat or folder. Date: 25 Sep 2026.", B),
          P("Machine: Apple M4 MacBook, 16 GB RAM. Project root: <font name='Courier'>" + esc(str(HERE)) + "</font> "
            "(note: the folder name '551 CONTAINERS ' has a trailing space; always quote paths).", SM), Spacer(1, 8)]

story += [P("1. The one-paragraph summary", H1),
          P("We are a student startup team looking for an AI result we can publish, get attention for, and raise money on, with about "
            "$30/month of Modal GPU credit. The top priority was TypeSafe AI's <b>Jev</b>, a closed, fast 'System One' model. Jev answers "
            "typed questions about a text (yes/no, pick-one, score) with probabilities instead of generated text. Deep research showed we "
            "cannot beat Jev across the board with $30. We can beat it on its documented weaknesses, with an open, small, trainable "
            "model. So we built a <b>lean benchmark</b> (11-20k train rows, 1,915 eval rows) and fine-tuned the open "
            "<b>GLiClass Edge</b> model (32.7M params) on the Mac. Our fine-tuned model (A3) cuts held-out prompt-injection success from 80% "
            "(untrained) and 61% (plain fine-tune) to <b>22%</b>. It stays robust to distractor text and improves consistency and "
            "calibration. It still fails on negations phrased in a style it never saw in training. <b>Jev has NOT been run yet</b> because "
            "no API key was available. All code, data and 515 validated Jev requests are ready; running Jev costs about $0.005.", B)]

# ---------------- Jev ----------------
story += [P("2. What Jev is (verified facts)", H1)] + bullets([
    "<b>Who:</b> TypeSafe AI (typesafe.ai). Launched 15 Sep 2026 with a $40M seed led by DCVC. Founders: Diogo Almeida (CEO, ex-OpenAI, "
    "InstructGPT), Erik Gafni (CTO), Sasha Sheng (COO). Forbes headline: $200M valuation (article body not verified).",
    "<b>What:</b> the input is state (text/JSON) plus named questions. Question types: <b>Noul</b> (yes/no, returns P(yes)), "
    "<b>Choice</b> (up to 255 options, returns a distribution; larger sets use a two-stage method) and <b>Score</b> (2-10 levels). "
    "All questions are answered in parallel and in isolation. The model is jev-1.13.0; the limit is 64k tokens per request "
    "(32k for state plus the longest question).",
    "<b>Claims:</b> 70-500 ms (typically about 100 ms). $0.042 per 1M input tokens, output free. 193.6x faster and 444.6x cheaper on "
    "TypeSafe's own workflows; the 'accuracy' there is agreement with frontier LLMs, about 67.8%. Architecture, parameter count and "
    "training data are all undisclosed. The training method is called RLCD (RL for Calibrated Decisions). Closed: no weights, "
    "no paper.",
    "<b>Its own docs list 9 failure modes</b> (docs.typesafe.ai/model-jaggedness/jev-1.13): literal reading; math/numbers; "
    "dates; indirection (double negatives, multi-hop); large irrelevant state; adversarial content; contradictory "
    "instructions/criteria; <b>structural invariants</b>, e.g. P(refund)=0.72 and P(not refund)=0.47 in the same call (sum 1.19); "
    "and it cannot generate text.",
    "<b>Community audits (Sep 2026):</b>",
    "&nbsp;&nbsp;- AbdelStark/jev-benchmarks: Banking77/AG News/Emotion pilot. Jev 91% vs GLiNER2.5 70% on AG News, but Emotion Brier "
    "0.846 vs 0.668, and zero probability on the true label 16% of the time. Also measures coverage at a fixed error rate.",
    "&nbsp;&nbsp;- jujumilk3/jev-calibration-audit: P(x)+P(not x) ranges 0.71-1.42.",
    "&nbsp;&nbsp;- zkousama/jagged: injection drops Jev from 96.5% to 26.5%.",
    "&nbsp;&nbsp;- Independent tests: a fine-tuned 310M ModernBERT beat Jev by 12 points on one topic task. Jev scores 62.6% on "
    "phishing with one question, but 95% when the task is split into 5 questions combined by a logistic regression.",
    "&nbsp;&nbsp;- Index of audits: Yifan-Lan/awesome-jev-robustness.",
    "<b>Access:</b> Python SDK <font name='Courier'>typesafe-sdk==0.7.1</font> (installed in the venv); the key is the env var "
    "<font name='Courier'>TYPESAFE_API_KEY</font>. Direct signups were paused on 22 Sep; OpenRouter and Vercel AI Gateway also list "
    "Jev. Read TypeSafe's terms (docs.typesafe.ai/legal.md) before publishing comparisons. Never train on Jev outputs.",
])

# ---------------- research ----------------
story += [P("3. Research conclusions", H1), P("<b>Can $30 beat Jev?</b>", B)] + bullets([
    "Not zero-shot across arbitrary questions. That is Jev's moat: two years of work and proprietary data. An open Qwen3-4B "
    "reproduction still trails it (0.845 vs 0.883 agreement).",
    "An 'open Jev clone' is already crowded: Laya (421M), OpenJev repos, GLiClass, and kyegomez/open-jev (consistency loss, "
    "no weights).",
    "<b>Winnable claims:</b> an open, local model (tens of ms, no US-only API) that can be fine-tuned, is better calibrated, is more "
    "logically consistent, is more robust to injection, and (as a stretch) fills tool-call arguments, which Jev cannot do.",
    "<b>Benchmark novelty:</b> a benchmark alone is NOT new. Community audits already cover negation, paraphrase, injection and "
    "coverage. What remains open is an open <i>trained</i> model that fixes these failures, plus one harness that covers them all.",
    "<b>Compute:</b> $30 on Modal buys about 7.6 H100-hours, 12-14 A100-hours or 37.5 L4-hours. It is Modal's free Starter allowance "
    "and renews monthly. Our training ran on the M4 Mac instead (Modal credit untouched).",
    "<b>Funding playbook:</b> benchmark numbers alone rarely fund a company. Mem0's $24M rested on 41k GitHub stars and usage, not only "
    "LoCoMo. Independent verification matters: Poetiq claimed 75%, but ARC Prize verified 54%. Irreproducible claims kill "
    "credibility (Reflection 70B). No startup named 'Memorable' was found.",
])
story += [P("<b>Six vetted ideas (ranked)</b>, from about 47 screened. The full report is in reports/ (see section 8).", B)]
story += [table([["#", "Idea", "Number to beat / status", "GPU"],
                 ["1", "OpenDecide: an open Jev-style decision model that fixes Jev's weaknesses (what we built)", "Beat Jev on consistency, injection, calibration, local latency", "~$15-25"],
                 ["2", "Tariff (HS) code classifier grounded in past US customs (CROSS) rulings, plus the first export-control (ECCN) benchmark", "HSCodeComp best agent 46.83% (10-digit); ATLAS 40% (10-digit) / 57.5% (6-digit)", "~$12-20"],
                 ["3", "SheetTRM: a tiny recursive model for spreadsheet table and cell detection", "SpreadsheetLLM 78.9% F1; 0.937 cell-type F1", "~$25-30"],
                 ["4", "SECReviewBench: predict SEC comment letters from draft filings", "No baseline exists", "~$10-17 + API"],
                 ["5", "FlashTRM: string transforms by example with a tiny recursive model", "PROSE: FlashFill 33%, fine-tuned 33B 82%", "~$20-28"],
                 ["6", "Hinglish / code-mixed customer-service agent benchmark", "Private benchmark: 66% (small) vs 90% (frontier)", "~$20-25 + $100-250 API"]],
                [0.25 * inch, 3.0 * inch, 2.55 * inch, 1.0 * inch])]
story += [Spacer(1, 4), P("<b>Other plans reviewed (from Codex/ChatGPT):</b>", B)] + bullets([
    "'Logic-consistent System One model' (GLiClass Edge + consistency/Brier losses + SystemOneBench): the right direction, and its "
    "facts check out. However, its SystemOneBench is not new (audits exist), 1-p consistency can be hard-coded (the claim must be "
    "consistency on freely worded, independently scored questions), 32.7M params is weak zero-shot, and its six ideas were all one "
    "bet. <b>We merged it into our build.</b>",
    "'Jev at 1M labels' (shortlist-then-rerank: GTE-ModernBERT + ANN + reranker): buildable, but this is prior art (BLINK 2020 "
    "retrieves the top 64 of about 6M entities; Microsoft XMC works at 1.3M labels). The projected numbers were unrealistic "
    "(BLINK zero-shot recall@64 was about 82%; the best P@1 at 1.3M labels is in the mid-50s). It also picks the wrong fight: "
    "rerankers are crowded. <b>Recommendation:</b> use that architecture for tariff codes (about 17-19k US codes) instead.",
])

# ---------------- decisions ----------------
story += [P("4. Decisions and working preferences", H1)] + bullets([
    "<b>Chosen:</b> idea A (OpenDecide, lean). The runner-up is tariff codes (B), which has the clearest paying customer.",
    "<b>User preference:</b> keep explanations short and simple (beginner); use FEW agents. A roughly 130-agent build was stopped "
    "for taking too long. Ask before any big fan-out.",
    "<b>Full research-grade spec</b> (140 KB, 28 reviewer points fixed) is in DESIGN.md: 24k train / 4.9k eval rows, 1,494 Jev calls, "
    "and about 104 person-hours of human verification. Its build was only partially done (loaders, keys, some banks). The lean "
    "version below is what actually ran.",
])

# ---------------- what was built ----------------
story += [PageBreak(), P("5. What was built (lean benchmark v0.2)", H1),
          P("All in <font name='Courier'>opendecide-data/lean/</font>. Python venv: <font name='Courier'>opendecide-data/.venv</font> "
            "(torch 2.14, transformers 4.57.6, gliclass 0.1.17, typesafe-sdk 0.7.1, sentence-transformers, reportlab).", B)]
story += [table([["File", "Purpose"],
                 ["build_data.py", "Builds data/: train.jsonl, dev.jsonl, eval.jsonl, *_relations.jsonl, eval_calls.jsonl, stats.json (seed 20260925)"],
                 ["gliclass_io.py", "Serialises rows for GLiClass (one row = one forward pass), scoring, latency"],
                 ["train.py", "Fine-tuning. Recipes A0 (base rows only) and A3 (all rows + consistency loss: (pA+pB-1)^2 and (pA-pB)^2). Step-matched"],
                 ["eval_local.py", "Runs a local model on eval or dev; writes preds/NAME.jsonl (+ latency)"],
                 ["run_jev.py", "Runs Jev: 1 call per state, questions bundled, resumable; writes preds/jev.jsonl"],
                 ["score.py", "All metrics with bootstrap CIs; writes results/RESULTS.md and results.json"],
                 ["README.md", "Benchmark description, reproduce commands, limitations"],
                 ["models/", "edge_A0, edge_A3 (v0.2); edge_A0_v01, edge_A3_v01 (v0.1). base_A3 was NOT finished (stopped)"],
                 ["data/eval_v0.1.sha256", "Frozen hashes: the eval set is byte-identical between v0.1 and v0.2"],
                 ["archive_v01/", "v0.1 predictions and results table"]],
                [1.5 * inch, 5.3 * inch])]
story += [Spacer(1, 6), P("<b>Dataset design</b>", H2)] + bullets([
    "<b>Sources (human labels):</b> Banking77, CLINC150 plus (with out-of-scope), MultiNLI (train), DBpedia-14 and Women's Clothing "
    "reviews (train, added in v0.2), SMS Spam and Twitter Financial News Sentiment (zero-shot eval only). Filler text: wikitext-103 "
    "validation (train) and test (eval).",
    f"<b>Eval: {stats['eval_rows']} rows / {stats['eval_calls']} Jev calls.</b>",
    "&nbsp;&nbsp;- ID: 200 states x 5 questions.",
    "&nbsp;&nbsp;- ZS: 95 x 5.",
    "&nbsp;&nbsp;- INJ: 60 items x 3 arms (C authority re-label, D argue, E echo control) x 2 questions.",
    "&nbsp;&nbsp;- DIST: 40 x 2.",
    "&nbsp;&nbsp;- Each core state asks a Choice question; a yes/no question about a label (50% gold); its negation in an "
    "<b>unseen style</b> ('Would someone who says that ... be mistaken?'); a paraphrase; and a double negation ('Would it be a "
    "mistake to deny that ...?').",
    f"<b>Train v0.2: {stats['train_rows']} rows.</b> Base rows; 7 negation wordings (prefix, judge, statement); clause negation "
    "('the customer is NOT asking about X'); double negation; paraphrase; train-only injection families (A override, B fake system, "
    "G fake output) with 1:1 echo controls; distractor filler. Dev: 600 rows with dev-only wordings.",
    "<b>Rules:</b>",
    "&nbsp;&nbsp;- Eval wordings, negation style, injection families, containers and filler corpus are disjoint from train "
    "(asserted in code).",
    "&nbsp;&nbsp;- Eval texts are de-duplicated against train (exact match and MiniLM cosine >= 0.95).",
    "&nbsp;&nbsp;- Every row is scored alone; links exist only in relations files.",
    "&nbsp;&nbsp;- Gold for every variant follows a fixed rule.",
    "&nbsp;&nbsp;- Held-out injections sit inside forwarded, quoted or retrieved-note containers and always target a wrong label.",
])

# ---------------- results ----------------
story += [PageBreak(), P("6. Results so far (v0.2; Jev pending)", H1),
          P(f"All models scored on the same {res['n_rows_scored']} rows in {res['n_groups']} groups. Brackets are 95% bootstrap CIs over groups. "
            "A0 and A3 are step-matched (same number of training steps and seed), so the A0-vs-A3 gap isolates the effect of the "
            "consistency and robustness data and loss.", SM)]
hdr = ["Metric"] + [m for m, _ in MODELS]
rows_ = [hdr]
for label, key, pct in METRICS:
    if key is None and "injection C" in label:
        rows_.append([label] + [f"{f(m, 'inj_C_choice_acc')} / {f(m, 'inj_C_clean_choice_acc')}" for m, _ in MODELS])
    elif key is None:
        rows_.append([label] + [f"{f(m, 'dist_choice_acc')} / {f(m, 'dist_clean_choice_acc')}" for m, _ in MODELS])
    else:
        rows_.append([label] + [f(m, key, pct) for m, _ in MODELS])
story += [table(rows_, [2.2 * inch] + [1.15 * inch] * 4, font=7.2)]
story += [Spacer(1, 4), P("Models: " + "; ".join(f"<b>{m}</b> = {d}" for m, d in MODELS) + ".", SM)]
lat = M.get("edge_zeroshot", {}).get("latency", {})
story += [P("<b>Latency (batch 1, M4):</b> Edge 32.7M: about 7 ms/question on CPU (median; p95 about 9 ms). Modern-base 151M: about "
            "70-120 ms (measured while training ran, so inflated). Whole 1,915-row eval with Edge: about 18 s including model load. "
            "Jev claims 70-500 ms per call over the network.", SM)]
story += [P("<b>What the numbers say</b>", H2)] + bullets([
    "<b>Injection robustness is the headline win.</b> Held-out attack success is 80% untrained, 61% for plain fine-tuning (A0) and "
    "<b>22% for A3</b>, on attack families and containers never seen in training. Echo controls stay at 98%, so the model did NOT "
    "learn a shortcut of avoiding whatever label is named.",
    "<b>Distractor robustness:</b> A3 keeps 87.5% vs 92.5% clean; A0 drops from 97.5% to 70%.",
    "<b>Consistency:</b> A3 beats A0 on complement violation (0.41 vs 0.67), contradictions (54% vs 78%), paraphrase flips "
    "(10% vs 16%), Brier (0.274 vs 0.320) and ECE. Choice accuracy is unchanged (87 vs 89, CIs overlap).",
    "<b>Main failure:</b> negations in the unseen style are still below chance (ID 44.5%, ZS 31.6%). Small encoders do not "
    "generalise to a new way of saying 'not'. v0.1 even learned a 'negative word means flip' shortcut that broke double negatives; "
    "v0.2 fixed that (drift 0.53 to 0.12) by adding clause-negation and double-negation training rows.",
    "<b>Zero-shot tasks</b> (spam, finance sentiment) are near chance for every local model. These models need task data. Jev will "
    "likely win zero-shot, as expected.",
    "<b>Coverage at 1% error</b> is about 0-2% for all local models: none is reliable enough yet to automate safely at 1% error.",
])
story += [P("<b>v0.1 results (before the fix), for the record</b>", H2)]
v01 = [[c.strip() for c in l.strip("|").split("|")] for l in v01_lines if not set(l.replace("|", "").strip()) <= set("-")]
v01 = [r for r in v01 if len(r) >= 5]
story += [table([[r[0].replace("↓", "(lower better)")] + r[1:5] for r in v01][:23], [2.2 * inch] + [1.15 * inch] * 4, font=6.8)]

# ---------------- next steps ----------------
story += [PageBreak(), P("7. How to continue (exact steps)", H1), P("<b>A. Get the Jev comparison (the stated goal)</b>", B),
          code(f'cd "{LEAN}"\n'
               'echo "TYPESAFE_API_KEY=your_key" > ../.env          # or export TYPESAFE_API_KEY=...\n'
               '../.venv/bin/python run_jev.py                     # 515 calls, ~$0.005, resumable (JEV_LIMIT=20 for a test)\n'
               '../.venv/bin/python score.py --models edge_zeroshot base_zeroshot edge_A0 edge_A3 jev\n'
               'open results/RESULTS.md'),
          P("<b>B. Finish the bigger model (optional, about 30-60 min on the M4, or cheap on Modal)</b>", B),
          code('../.venv/bin/python train.py --base knowledgator/gliclass-modern-base-v3.0 --recipe A3 --lr 2e-5 --out base_A3\n'
               '../.venv/bin/python eval_local.py --model models/base_A3 --name base_A3 --latency\n'
               '../.venv/bin/python score.py'),
          P("<b>C. Rebuild or retrain from scratch</b>", B),
          code('../.venv/bin/python build_data.py        # eval stays byte-identical: shasum -a 256 -c data/eval_v0.1.sha256\n'
               '../.venv/bin/python train.py --recipe A3 --out edge_A3   # ~13 min on M4\n'
               '../.venv/bin/python train.py --recipe A0 --out edge_A0\n'
               '../.venv/bin/python eval_local.py --model models/edge_A3 --name edge_A3 [--split dev]')]
story += [P("<b>D. Recommended next improvements</b>", B)] + bullets([
    "Fix unseen-style negation: more negation classes in train (while keeping one held-out class for the claim); undecidable 'trap' "
    "pairs (NLI neutral / CondaQA 'don't know') so 1-p shortcuts are penalised; try modern-base 151M; consider a per-type "
    "temperature fitted on dev.",
    "Add fresh, never-published eval items (removes 'Jev saw the public test sets' doubts). Add the AbdelStark Banking77 replay as "
    "a harness check that Jev reproduces about 87%.",
    "Report per the pre-registered framing: win on injection robustness, local latency and fine-tunability; state honestly where "
    "Jev wins (zero-shot breadth).",
    "If you pivot to tariff codes: CROSS rulings on HF (flexifyai/cross_rulings_hts_dataset_for_tariffs, about 18.7k rows), "
    "HSCodeComp and ATLAS; first check shortlist recall@64 with GTE-ModernBERT; kill the idea if it is below 90%.",
])
story += [P("8. File map (absolute paths)", H1)]
story += [table([["Path", "What"],
                 [esc(str(REPO / "reports/JEV model and research startup ideas.md")), "Deep-research report (Jev, open models, $30 compute, funding, 6 ideas + dropped list), with a 25-Sep update"],
                 [esc(str(REPO / "research_notes/JEV model and research startup ideas/")), "Raw research notes incl. codex_claims_verification.md"],
                 [esc(str(HERE / "DESIGN.md")), "Full research-grade dataset spec (v1.0-rc) + build deviations + review log"],
                 [esc(str(HERE / "design/")), "Scout notes (datasets, licences, formats, audits), 3 design proposals, design_plan.py"],
                 [esc(str(HERE / "lean/")), "The lean benchmark that actually ran: code, data, models, preds, results"],
                 [esc(str(HERE / "assets/labels/keys/")), "Natural-language label names for all datasets (used by lean)"],
                 [esc(str(HERE / "build/")), "Partial full-spec pipeline (env, lock, banking77 loader); not needed for lean"]],
                [3.7 * inch, 3.1 * inch], font=7)]
story += [Spacer(1, 6), P("<b>Caveats:</b> the eval is small (295 core groups; per-dataset CIs are wide). There are no trap pairs "
                          "yet. The public test sets may be in Jev's training data. Propositions come from label names, not "
                          "hand-written descriptions. Licences: train uses commercial-friendly sources (DBpedia, MNLI and wikitext "
                          "are share-alike); SMS/TFNS are eval-only.", SM)]


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.drawString(0.6 * inch, 0.45 * inch, "OpenDecide handoff | 25 Sep 2026")
    canvas.drawRightString(7.9 * inch, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(str(OUT), pagesize=letter, leftMargin=0.6 * inch, rightMargin=0.6 * inch, topMargin=0.6 * inch,
                        bottomMargin=0.7 * inch, title="OpenDecide handoff", author="OpenDecide team")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("wrote", OUT)
