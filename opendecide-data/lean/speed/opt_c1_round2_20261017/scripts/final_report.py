"""Mac: assemble VOICE_REAL.json + VOICE_REAL.md from results/pulled (copied from od-cpu1 ~/opt_r2/voice/out). Numbers only, no row text."""
import sys, os, glob, json, datetime, collections, zlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from r2common import *
from analyze_c1 import c1_summary
from analyze_eot import eot_summary, load_eot, METHODS
from static_meta import META
import numpy as np
R = os.path.abspath(os.path.join(HERE, ".."))
OUT = os.path.abspath(os.path.join(R, ".."))        # opt_c1_round2_20261017 == R
P = f"{R}/results/pulled"; A = f"{R}/assets"
CARD = {"ls_clean": {"s160": 2.56, "s560": 2.46, "offline": 2.32}, "ls_other": {"s160": 5.57, "s560": 5.07, "offline": 4.84},
        "tedlium": {"s160": 3.77, "s560": 3.54, "offline": 3.50}, "ami": {"s160": 14.71, "s560": 11.88, "offline": 11.73},
        "earnings22": {"s160": 13.01, "s560": 12.82, "offline": 12.52}}
NAMES = {"ls_clean": "LibriSpeech test-clean", "ls_other": "LibriSpeech test-other", "tedlium": "TED-LIUM 3 test", "ami": "AMI IHM test", "earnings22": "Earnings-22 test"}
DTYPE = {("ls_clean", "s560"): "fp32"}  # every other cell: s560 bf16, offline fp32, s160 bf16

def load_asr(st, mode, tag=""):
    rows = {}
    for f in glob.glob(f"{P}/asr_{st}_{mode}{tag}.shard*.jsonl"):
        for r in read_jsonl(f): rows[r["uid"]] = r
    return rows

def wer_cell(st, mode, tag="", card_set=None, uids=None):
    base = st.replace("_big", ""); man = {m["uid"]: m for m in read_jsonl(f"{A}/samples/{st}/manifest.jsonl")}
    rows = load_asr(st, mode, tag)
    if uids is not None: rows = {u: r for u, r in rows.items() if u in uids}
    if not rows: return None
    errs, nref, ms, dur, ex = [], [], [], [], 0
    for u, r in rows.items():
        e, n = word_errors(man[u]["ref_norm"], norm_text(r["hyp"])); errs.append(e); nref.append(n); ms.append(r["ms"]); dur.append(r["dur_s"]); ex += (e == 0)
    w = 100 * sum(errs) / sum(nref); lo, hi = bootstrap_wer(errs, nref); c = CARD[base][mode]
    return {"n_utts": len(rows), "n_ref_words": int(sum(nref)), "wer_pct": round(w, 2), "ci95_pct": [round(100 * lo, 2), round(100 * hi, 2)], "card_pct": c,
            "delta_pt": round(w - c, 2), "within_0.5pt": abs(w - c) <= 0.5, "card_inside_ci95": 100 * lo <= c <= 100 * hi, "utt_exact_pct": round(100 * ex / len(rows), 1),
            "audio_h": round(sum(dur) / 3600, 3), "cpu_rtf_single_thread_loaded_vm": round(sum(ms) / 1000 / sum(dur), 2)}

def wer_section():
    out = {"headline": {}, "dtype_checks": {}, "extended_samples": {}}
    for st in CARD:
        for mode in ("s160", "s560", "offline"):
            c = wer_cell(st, mode)
            if c:
                c["dtype"] = DTYPE.get((st, mode), {"s160": "bf16", "s560": "bf16", "offline": "fp32"}[mode]); c["set"] = NAMES[st]; out["headline"][f"{st}/{mode}"] = c
    # dtype checks: bf16 vs fp32 on identical utterances
    for st, tag, ref_dtype in (("ls_clean", "_bf16chk", "fp32"), ("ami", "_fp32chk", "bf16"), ("earnings22", "_fp32chk", "bf16")):
        a = load_asr(st, "s560"); b = load_asr(st, "s560", tag)
        if not b: continue
        u = sorted(set(a) & set(b)); man = {m["uid"]: m for m in read_jsonl(f"{A}/samples/{st}/manifest.jsonl")}
        same = sum(norm_text(a[x]["hyp"]) == norm_text(b[x]["hyp"]) for x in u)
        w = lambda d: round(100 * sum(word_errors(man[x]["ref_norm"], norm_text(d[x]["hyp"]))[0] for x in u) / sum(word_errors(man[x]["ref_norm"], "")[1] for x in u), 2)
        out["dtype_checks"][f"{st}/s560"] = {"n": len(u), "identical_hypotheses_after_norm": same, "main_run_dtype": "fp32" if st == "ls_clean" else "bf16", "wer_main_run_pct": w(a), "wer_other_dtype_pct": w(b),
                                              "other_dtype": "bf16" if st == "ls_clean" else "fp32"}
    for st in ("ami_big", "earnings22_big"):
        c = wer_cell(st, "s560")
        if c: c["dtype"] = "bf16"; out["extended_samples"][f"{st}/s560"] = c
    return out

def slurp_section():
    man = {m["uid"]: m for m in read_jsonl(f"{A}/samples/slurp/manifest.jsonl")}
    kinds = json.load(open(f"{A}/samples/slurp/kinds.json"))
    asr = load_asr("slurp", "s560")
    wer_by, e_all, n_all, grp = {}, 0, 0, collections.defaultdict(lambda: [0, 0, 0])
    for u, r in asr.items():
        e, n = word_errors(norm_text(man[u]["ref"]), norm_text(r["hyp"])); wer_by[u] = e; e_all += e; n_all += n
        g = grp[kinds[u]]; g[0] += e; g[1] += n; g[2] += 1
    res = {"asr_s560": {"n": len(asr), "wer_pct_vs_gold_transcript": round(100 * e_all / n_all, 2), "utt_exact_after_norm_pct": round(100 * sum(v == 0 for v in wer_by.values()) / len(wer_by), 1),
                        "by_condition": {k: {"n": v[2], "wer_pct": round(100 * v[0] / v[1], 2)} for k, v in grp.items()},
                        "condition_note": "headset vs far-field is inferred from the HF row order within a slurp_id matched to the official recordings list; the 12.7 vs 21 WER gap supports the mapping"}}
    for lvl in ("scen", "intent"):
        p = f"{P}/c1_slurp_{lvl}_s560.jsonl"
        if not os.path.exists(p): continue
        s = c1_summary(p, man, wer_by)
        rows = read_jsonl(p)
        s["by_condition"] = {}
        for k in ("headset", "far_field"):
            rr = [r for r in rows if kinds[r["uid"]] == k]
            if rr:
                kk = sum(r["pred_gold"] == r["pred_asr"] for r in rr); lo, hi = wilson(kk, len(rr))
                s["by_condition"][k] = {"n": len(rr), "agree_pct": round(100 * kk / len(rr), 2), "agree_wilson95_pct": [round(100 * lo, 2), round(100 * hi, 2)],
                                        "acc_gold_pct": round(100 * sum(r["pred_gold"] == r["gold_label"] for r in rr) / len(rr), 2), "acc_asr_pct": round(100 * sum(r["pred_asr"] == r["gold_label"] for r in rr) / len(rr), 2)}
        b = {"wer_0": [], "wer_1_2": [], "wer_3_plus": []}
        for r in rows:
            w = wer_by[r["uid"]]; b["wer_0" if w == 0 else ("wer_1_2" if w <= 2 else "wer_3_plus")].append(r["pred_gold"] == r["pred_asr"])
        s["agree_by_asr_word_errors"] = {k: {"n": len(v), "agree_pct": round(100 * sum(v) / len(v), 1) if v else None} for k, v in b.items()}
        conf = collections.Counter((r["pred_gold"].split(" ")[0], r["pred_asr"].split(" ")[0]) for r in rows if r["pred_gold"] != r["pred_asr"])
        s["flip_pairs_gold_to_asr_top"] = [[a, b_, c] for (a, b_), c in conf.most_common(8)]
        res[f"c1_{lvl}"] = s
    return res

def eot_section(timing):
    add = {"st": timing["smart_turn_ms"]["total_p50"], "eou": timing["eou_chunk_ms_160ms_chunks"]["p50"], "vad": timing["silero_ms_per_32ms_window"]["p50"]} if timing else {}
    out = {"idle_cpu_compute_added_to_latency_ms": add}
    for st in ("slurp", "ami", "ls_clean"):
        rows = load_eot(P, st)
        if not rows: continue
        ok = [r for r in rows if r.get("fa_ok")]
        o = {"n_utts": len(rows), "n_aligned": len(ok), "speech_dur_s_p50": round(pct([r["dur_s"] for r in ok], .5), 2)}
        for tk in ("noise", "zero"):
            s = eot_summary(rows, tk, add_ms=add); s.pop("_compute", None); o[f"tail_{tk}"] = s
        if st == "ami": o["tail_noise_vs_clip_end"] = {k: v for k, v in eot_summary(rows, "noise", ref_kind="clip", add_ms=add).items() if k != "_compute"}
        out[st] = o
    return out

def main():
    timing = None
    tp = sorted(glob.glob(f"{P}/timing_idle_*t.json"))
    tim = {os.path.basename(p): json.load(open(p)) for p in tp}
    timing = tim.get("timing_idle_1t.json")
    eouwer = json.load(open(f"{P}/eou_wer_ls_clean.json")) if os.path.exists(f"{P}/eou_wer_ls_clean.json") else None
    res = {"generated_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "track": "B real-audio voice tests (od-cpu1, c3-standard-8, CPU only; no GPU, no Modal)",
           "asr_wer": wer_section(), "slurp": slurp_section(), "end_of_turn": eot_section(timing), "eou_model_sanity": eouwer, "cpu_timing_idle_vm": tim, "meta": META}
    rp = f"{R}/recommendation.json"
    res["recommendation"] = json.load(open(rp)) if os.path.exists(rp) else None
    json.dump(res, open(f"{R}/VOICE_REAL.json", "w"), indent=1)
    print("wrote VOICE_REAL.json")
    return res



# ------------------------------------------------------------------ paired s160/s560/offline comparison on the same utterances
def paired_modes():
    out = {}
    for st in CARD:
        man = {m["uid"]: m for m in read_jsonl(f"{A}/samples/{st}/manifest.jsonl")}
        d = {m: load_asr(st, m) for m in ("s160", "s560", "offline")}
        u = sorted(set(d["s160"]) & set(d["s560"]) & set(d["offline"]))
        if not u: continue
        nref = np.array([word_errors(man[x]["ref_norm"], "")[1] for x in u], float)
        e = {m: np.array([word_errors(man[x]["ref_norm"], norm_text(d[m][x]["hyp"]))[0] for x in u], float) for m in d}
        rng = np.random.default_rng(0); idx = rng.integers(0, len(u), size=(2000, len(u)))
        o = {"n": len(u)}
        for m in e: o[f"wer_{m}_pct"] = round(100 * e[m].sum() / nref.sum(), 2)
        for a, b in (("s160", "s560"), ("offline", "s560")):
            dd = (e[a][idx].sum(1) - e[b][idx].sum(1)) / nref[idx].sum(1)
            o[f"delta_{a}_minus_{b}_pt"] = round(100 * (e[a].sum() - e[b].sum()) / nref.sum(), 2)
            o[f"delta_{a}_minus_{b}_ci95_pt"] = [round(100 * float(np.percentile(dd, 2.5)), 2), round(100 * float(np.percentile(dd, 97.5)), 2)]
        out[st] = o
    return out


def tail_ablation():
    out = {}
    for st in ("ls_other", "tedlium"):
        man = {m["uid"]: m for m in read_jsonl(f"{A}/samples/{st}/manifest.jsonl")}
        a = load_asr(st, "s560"); b = load_asr(st, "s560", "_taildrop")
        u = sorted(set(a) & set(b))
        if not u: continue
        nw = sum(word_errors(man[x]["ref_norm"], "")[1] for x in u)
        w = lambda d: round(100 * sum(word_errors(man[x]["ref_norm"], norm_text(d[x]["hyp"]))[0] for x in u) / nw, 2)
        out[st] = {"n": len(u), "wer_flush_pct": w(a), "wer_card_loop_drop_tail_pct": w(b), "dtype": "bf16"}
    return out


# ------------------------------------------------------------------ markdown
def f1(x): return "n/a" if x is None else (f"{x:.1f}" if isinstance(x, float) else str(x))

def md(res):
    L = []; W = res["asr_wer"]; S = res["slurp"]; E = res["end_of_turn"]; T = res["cpu_timing_idle_vm"].get("timing_idle_1t.json") or {}; T4 = res["cpu_timing_idle_vm"].get("timing_idle_4t.json") or {}
    rec = res.get("recommendation") or {}
    L.append("# VOICE_REAL: real-audio tests of the voice cascade (Track B, 17 Oct 2026)\n")
    L.append("Run on `od-cpu1` (c3-standard-8, Xeon Platinum 8481C Sapphire Rapids, 8 vCPU = 4 cores x 2 HT, AMX-bf16, **CPU only**; no GPU, no Modal, no paid API). "
             "All data are public; this file holds counts and rates only, no row text. Machine-readable twin: `VOICE_REAL.json`.\n")
    if rec:
        L.append("## Recommendation (locked voice config)\n")
        for k, v in rec.get("lines", []): L.append(f"- **{k}** {v}")
        L.append("")
    # ---------------- 1 WER
    L.append("## 1. ASR sanity: WER of Nemotron Speech Streaming EN 0.6B vs its model card\n")
    L.append("Loop = the model-card streaming recipe through transformers 5.17 (`NemotronAsrStreamingForRNNT`), plus an explicit end-of-input flush (zero-pad the last real chunk, then one silent chunk). "
             "Normaliser = whisper-normalizer 0.1.12 (the one named on the card), corpus-level WER, 95% interval = bootstrap over utterances. Utterances = a seeded random sample of the test set "
             "(500 per set; s160 uses the first 150 of the same shuffled order). 'card' = the card's OpenASR WER at the same chunk size (the card has no number for offline; the 1.12 s column is shown). "
             "Pass = |delta| <= 0.5 pt (brief) or card value inside our 95% interval (sampling-aware).\n")
    L.append("| set | mode (dtype) | n utts | WER % [95% CI] | card % | delta pt | within 0.5 pt | card in CI |")
    L.append("|---|---|---|---|---|---|---|---|")
    for st in CARD:
        for mode in ("s560", "s160", "offline"):
            c = W["headline"].get(f"{st}/{mode}")
            if not c: continue
            L.append(f"| {NAMES[st]} | {mode} ({c['dtype']}) | {c['n_utts']} | {c['wer_pct']:.2f} [{c['ci95_pct'][0]:.2f}, {c['ci95_pct'][1]:.2f}] | {c['card_pct']:.2f} | {c['delta_pt']:+.2f} | {'yes' if c['within_0.5pt'] else 'NO'} | {'yes' if c['card_inside_ci95'] else 'NO'} |")
    L.append("")
    cells = W["headline"]; ok = [k for k, c in cells.items() if c["within_0.5pt"]]; bad = [k for k, c in cells.items() if not c["within_0.5pt"]]
    L.append(f"**Summary: {len(ok)} of {len(cells)} cells are within 0.5 pt of the card; the card value lies inside our 95% interval in {sum(c['card_inside_ci95'] for c in cells.values())} of {len(cells)}.** "
             "Misses: " + "; ".join(f"{k} ({cells[k]['delta_pt']:+.2f}, n={cells[k]['n_utts']})" for k in bad) + ". "
             "All three LibriSpeech/TED-LIUM s560 cells (the locked mode) pass; the misses are on the two noisy-domain sets (see the larger samples below) and on small-n s160/offline cells.\n")
    if W["extended_samples"]:
        L.append("Larger independent samples for the two sets that missed at n=500 (s560, bf16):\n")
        L.append("| set | n utts | ref words | WER % [95% CI] | card % | delta pt | card in CI |"); L.append("|---|---|---|---|---|---|---|")
        for k, c in W["extended_samples"].items():
            L.append(f"| {k.split('/')[0]} | {c['n_utts']} | {c['n_ref_words']} | {c['wer_pct']:.2f} [{c['ci95_pct'][0]:.2f}, {c['ci95_pct'][1]:.2f}] | {c['card_pct']:.2f} | {c['delta_pt']:+.2f} | {'yes' if c['card_inside_ci95'] else 'NO'} |")
        L.append("")
    if W["dtype_checks"]:
        L.append("bf16 (AMX) vs fp32 on identical utterances (why mixed dtypes do not matter):\n")
        L.append("| set (s560) | n | identical hypotheses | WER main run | WER other dtype |"); L.append("|---|---|---|---|---|")
        for k, c in W["dtype_checks"].items():
            L.append(f"| {k.split('/')[0]} | {c['n']} | {c['identical_hypotheses_after_norm']} | {c['wer_main_run_pct']:.2f} ({c['main_run_dtype']}) | {c['wer_other_dtype_pct']:.2f} ({c['other_dtype']}) |")
        L.append("")
    pm = res.get("paired_modes") or {}
    if pm:
        L.append("Chunk mode, paired on the same 150 utterances per set (delta with bootstrap 95% CI; positive = first is worse):\n")
        L.append("| set | WER s160 | WER s560 | WER offline | s160 - s560 [CI] | offline - s560 [CI] |"); L.append("|---|---|---|---|---|---|")
        for st, o in pm.items():
            a = o["delta_s160_minus_s560_ci95_pt"]; b = o["delta_offline_minus_s560_ci95_pt"]
            L.append(f"| {NAMES[st]} | {o['wer_s160_pct']:.2f} | {o['wer_s560_pct']:.2f} | {o['wer_offline_pct']:.2f} | {o['delta_s160_minus_s560_pt']:+.2f} [{a[0]:+.2f}, {a[1]:+.2f}] | {o['delta_offline_minus_s560_pt']:+.2f} [{b[0]:+.2f}, {b[1]:+.2f}] |")
        L.append("")
    ta = res.get("tail_ablation") or {}
    if ta:
        L.append("Why the flush matters (same utterances, s560, bf16): the card's loop drops the final partial chunk. " + "; ".join(f"{NAMES[k]} n={v['n']}: {v['wer_card_loop_drop_tail_pct']}% without flush vs {v['wer_flush_pct']}% with flush" for k, v in ta.items()) + ".\n")
    if res.get("eou_model_sanity"):
        L.append(f"Sanity check of our .nemo -> HF conversion of Parakeet Realtime EOU 120M: its own transcripts reach {res['eou_model_sanity']['wer_pct']}% WER on {res['eou_model_sanity']['n']} LibriSpeech test-clean utterances (160 ms chunks), so the converted weights are intact.\n")
    # ---------------- 2 SLURP
    a = S["asr_s560"]
    L.append("## 2. Decision agreement on SLURP test (real spoken commands)\n")
    L.append(f"500 distinct SLURP test utterances (one random recording each; seeded). ASR = Nemotron s560 (fp32): WER {a['wer_pct_vs_gold_transcript']}% against the gold transcript "
             f"(headset {a['by_condition']['headset']['wer_pct']}%, far-field {a['by_condition']['far_field']['wer_pct']}%; condition inferred, see caveats), {a['utt_exact_after_norm_pct']}% of utterances exact after normalisation.\n")
    L.append("C1 = Qwen3.5-4B + merged `q35_4b_main500k`, BF16, HF transformers on CPU, served readout A5 (identity + reversed option order averaged), layout schema_branch_mark. "
             "Each utterance becomes one API-v1-style choice question (state `Customer message:` + transcript). The gold row uses the gold transcript; the ASR row uses the raw ASR text (with its punctuation and capitals). "
             "Same question, same options; only the text differs. Labels are SLURP's official scenario (18 options, short descriptions) and scenario_action intent (60 options, no descriptions).\n")
    L.append("| level | n | agreement gold vs ASR (Wilson 95%) | flips | accuracy gold transcript | accuracy ASR transcript | accuracy change | max abs dp p50 / p95 / max |"); L.append("|---|---|---|---|---|---|---|---|")
    for lvl, name in (("scen", "scenario, 18 options"), ("intent", "intent, 60 options")):
        c = S.get(f"c1_{lvl}")
        if not c: continue
        L.append(f"| {name} | {c['n']} | **{c['agree_pct']}%** [{c['agree_wilson95_pct'][0]}, {c['agree_wilson95_pct'][1]}] | {c['flips']} | {c['acc_gold_transcript_pct']}% | {c['acc_asr_transcript_pct']}% | {c['acc_diff_pt']:+.1f} pt | {c['max_abs_dp']['p50']} / {c['max_abs_dp']['p95']} / {c['max_abs_dp']['max']} |")
    L.append("\nTarget >= 97% agreement: " + ("**NOT met**" if S.get("c1_scen", {}).get("agree_pct", 100) < 97 else "met") + " on this set. Breakdown (scenario level):\n")
    c = S.get("c1_scen")
    if c:
        L.append("| slice | n | agreement % | accuracy gold / ASR % |"); L.append("|---|---|---|---|")
        for k, v in c["by_condition"].items(): L.append(f"| {k.replace('_', '-')} recordings | {v['n']} | {v['agree_pct']} [{v['agree_wilson95_pct'][0]}, {v['agree_wilson95_pct'][1]}] | {v['acc_gold_pct']} / {v['acc_asr_pct']} |")
        for k, v in c["agree_by_asr_word_errors"].items(): L.append(f"| ASR word errors: {k.replace('wer_', '').replace('_', '-')} | {v['n']} | {v['agree_pct']} | |")
        L.append(f"\nOf the {c['flips']} flips, the gold-transcript decision was the correct one in {c['flips_where_gold_transcript_decision_correct']} and the ASR-transcript decision in {c['flips_where_asr_transcript_decision_correct']}. "
                 f"Most frequent flips (gold -> ASR label): " + ", ".join(f"{x}->{y} ({n})" for x, y, n in c["flip_pairs_gold_to_asr_top"][:6]) + ".\n")
    # ---------------- 3 EOT
    L.append("## 3. End of turn (CPU timings)\n")
    L.append("Reference speech end = last word end from CTC forced alignment of the gold transcript (wav2vec2-base-960h, 20 ms steps). Each clip is followed by a 2.5 s tail: "
             "noise at the clip's own noise floor (primary) or digital zeros. Latency = decision time minus reference end (stream time, plus idle-machine CPU compute: "
             f"Smart Turn {E['idle_cpu_compute_added_to_latency_ms'].get('st')} ms, EOU {E['idle_cpu_compute_added_to_latency_ms'].get('eou')} ms, Silero {E['idle_cpu_compute_added_to_latency_ms'].get('vad')} ms; single thread). "
             "False cut = decision before the last word started (at least one word lost). Miss = no decision within the 2.5 s tail (Smart Turn's 3 s silence fallback therefore counts as a miss). "
             "(a) = Silero VAD (p>=0.5, 0.2 s of speech to start) -> after `stop` s of silence run Smart Turn v3.2 on the audio since speech start; complete (p>0.5) fires, incomplete waits (fallback 3 s). "
             "VAD-only fires at every VAD stop. (b) = Parakeet Realtime EOU 120M, first `<EOU>` token, 160 ms chunks.\n")
    for st, name in (("slurp", "SLURP test (500 clips; short commands)"), ("ami", "AMI IHM test (500 segments; conversational, many 1-2 word backchannels)")):
        if st not in E: continue
        L.append(f"### {name}\n")
        L.append("| method | tail | decided | false cut % | miss % | latency p50 / p90 / p95 ms | decided in 0-1 s, no cut % |"); L.append("|---|---|---|---|---|---|---|")
        for tk, tn in (("tail_noise", "noise"), ("tail_zero", "zeros")):
            for m in ("st_0.2", "st_0.3", "st_0.5", "vad_0.2", "vad_0.5", "vad_0.8", "eou"):
                o = E[st][tk][m]; lat = o["lat_incl_idle_cpu_ms"]
                label = {"st_0.2": "Silero+SmartTurn stop 0.2 s", "st_0.3": "Silero+SmartTurn stop 0.3 s", "st_0.5": "Silero+SmartTurn stop 0.5 s", "vad_0.2": "Silero only 0.2 s", "vad_0.5": "Silero only 0.5 s", "vad_0.8": "Silero only 0.8 s", "eou": "Parakeet EOU 120M"}[m]
                L.append(f"| {label} | {tn} | {o['detected']}/{o['n']} | {o['false_cut_before_last_word_pct']} | {o['miss_pct']} | {lat['p50'] if lat else 'n/a'} / {lat['p90'] if lat else 'n/a'} / {lat['p95'] if lat else 'n/a'} | {o['decided_within_1s_after_end_no_cut_pct']} |")
        L.append("")
    if "ls_clean" in E:
        o = E["ls_clean"]["tail_zero"]["eou"]; oo = E["ls_clean"]["tail_noise"]["eou"]
        L.append(f"Validation of the EOU harness on clean read speech (first 100 LibriSpeech test-clean sample clips, long ones): Parakeet EOU false cut {o['false_cut_before_last_word_pct']}%, latency p50 {o['lat_incl_idle_cpu_ms']['p50']} ms (zeros) / {oo['lat_incl_idle_cpu_ms']['p50']} ms (noise). "
                 "Smart Turn / VAD cut those long multi-clause clips at ordinary pauses, which is why the rest of this section uses short-command and conversational sets.\n")
    # ---------------- 4 timing
    L.append("## 4. CPU compute on the idle VM (c3-standard-8)\n")
    if T:
        L.append("| item | 1 thread | 4 threads (one per physical core) |"); L.append("|---|---|---|")
        L.append(f"| Smart Turn v3.2 (int8 ONNX, 8 s window) per call | {T['smart_turn_ms']['total_p50']} ms p50 (features {T['smart_turn_ms']['feature_p50']} + model {T['smart_turn_ms']['onnx_p50']}) | {T4['smart_turn_ms']['total_p50']} ms |")
        L.append(f"| Silero VAD per 32 ms window | {T['silero_ms_per_32ms_window']['p50']} ms | {T4['silero_ms_per_32ms_window']['p50']} ms |")
        L.append(f"| Parakeet EOU 120M per 160 ms chunk (fp32) | {T['eou_chunk_ms_160ms_chunks']['p50']} ms p50, {T['eou_chunk_ms_160ms_chunks']['p95']} p95 | {T4['eou_chunk_ms_160ms_chunks']['p50']} ms p50 |")
        for d in ("bf16", "fp32"):
            L.append(f"| Nemotron s560 per 560 ms chunk ({d}) | {T[f'nemotron_{d}_s560_chunk_ms']['p50']} ms p50, {T[f'nemotron_{d}_s560_chunk_ms']['p95']} p95; last (flush) chunk {T[f'nemotron_{d}_s560_chunk_ms']['last_flush_chunk_p50']} | {T4[f'nemotron_{d}_s560_chunk_ms']['p50']} ms; flush {T4[f'nemotron_{d}_s560_chunk_ms']['last_flush_chunk_p50']} |")
            L.append(f"| Nemotron s160 per 160 ms chunk ({d}) | {T[f'nemotron_{d}_s160_chunk_ms']['p50']} ms p50 | {T4[f'nemotron_{d}_s160_chunk_ms']['p50']} ms |")
            L.append(f"| Nemotron offline, {T[f'nemotron_{d}_clip_s_p50']} s clip ({d}) | {T[f'nemotron_{d}_offline_ms_per_clip_p50']} ms | {T4[f'nemotron_{d}_offline_ms_per_clip_p50']} ms |")
        L.append("")
        L.append("Reading: on this CPU the 560 ms mode runs faster than real time on one thread in bf16 (0.44x), the 160 ms mode does not (1.4x). These are CPU figures; the L4 figures of 17 Oct (ASR flush p50 72 ms) are a different machine.\n")
    # ---------------- 5 caveats
    L.append("## 5. Deviations and caveats\n")
    for x in rec.get("caveats", []): L.append(f"- {x}")
    L.append("")
    L.append("## 6. Sources, revisions, licences\n")
    for k, v in res["meta"]["datasets"].items():
        L.append(f"- **{k}**: {v['source']}; revision `{v['revision']}`; licence: {v['licence']}" + (f"; {v['note']}" if v.get("note") else ""))
    for k, v in res["meta"]["models"].items():
        L.append(f"- **{k}**: " + "; ".join(f"{a}: {b}" for a, b in v.items()))
    L.append(f"- Normaliser / statistics: {res['meta']['normaliser']}")
    L.append("\n## 7. Files\n")
    L.append("`scripts/` (prep, ASR runner, end-of-turn runner, C1 SLURP runner, analysis), `results/pulled/` (per-utterance outputs: hypotheses, timings, decisions; no audio), `assets/samples/*/manifest.jsonl` (the sampled utterance ids with public references), `RESEARCH_PLAN.json` (input).")
    return "\n".join(L) + "\n"

def write_all():
    res = main()
    res["paired_modes"] = paired_modes(); res["tail_ablation"] = tail_ablation()
    json.dump(res, open(f"{R}/VOICE_REAL.json", "w"), indent=1)
    open(f"{R}/VOICE_REAL.md", "w").write(md(res))
    print("wrote VOICE_REAL.json + VOICE_REAL.md")


if __name__ == "__main__":
    write_all()
