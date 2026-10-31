# Multimodal C1 preview: locked config (17 Oct 2026, round 2)

**Short version.** None of the text speed-ups were tested this round, so the text config stays exactly as it was. Voice is now tested on real recordings. It works, but it is weaker than the 17 Oct synthetic test suggested. Images stay at native resolution, and no image speed-up has been tested yet. Nothing in this preview is faster or cheaper than before. The H100 confirm should wait until the L4 trials can run.

Sources: `TRIALS.md`, `VOICE_REAL.md` / `.json`, `RESEARCH_PLAN.json`, the skeptic re-check (every number it re-derived matched), and `../opt_c1_20261017/results/` (the 17 Oct H100 session and the image cap test).

---

## 1. Text serving: what is locked

**No new flag or change is adopted.** All 18 L4 trials (T0a to T11) show `NOT RUN`. The first trial window has to stop the production server on od-l4b for about 40 minutes, and the permission system refused that step. Production was never touched: pid 1219 kept running and `/health` returned 200 throughout.

The locked text config is today's production server, S1:

- SGLang 0.5.20, BF16, C1 = Qwen3.5-4B + `q35_4b_main500k` merged.
- `--max-running 32 --max-mamba 128 --mem-fraction 0.8 --attention-backend triton`, extra_buffer, page size 1.
- Parity of S1 against the HF reference: **99.77% on 8,143 items, PASS** (SPEED-2, 13 Oct).

Checked offline this round. These are not adopted yet, but they are ready to try.

| item | what we know | is it proven on the GPU? |
|---|---|---|
| T4: send token ids, `--skip-tokenizer-init` | Token ids match exactly on all 8,143 decisions (11,957 sequences, 6,077,542 tokens, 0 mismatches). The client already sends ids, so the only possible gain is a little tokenizer-process overhead. | No |
| T5: LM-head slice to the 141 option tokens | In a CPU math test the logits match exactly (max diff 0.0) and the max probability change is 1.5e-7. Worth about 0.4 ms per call on an H100 (about 4.2 ms on the L4). | No. The patch has never run inside SGLang. |
| T8: block-FP8 checkpoint | Built and verified: 5.5 GB vs 9.3 GB, 2.64% weight error, the same bytes on both VMs, and SGLang reads its config correctly. | No. It has never been booted, and its parity is unknown. |

## 2. Voice front-end: what is locked

**Pipeline:** speech, then NVIDIA Nemotron Speech Streaming EN 0.6B (560 ms chunks, with a forced flush at the end of input), then the text goes to C1. For a whole uploaded file, use offline mode.

**End of turn:**
- **Default:** the client signals the end itself (push-to-talk, closing the stream, or a file upload).
- **Live microphone:** Silero VAD plus Smart Turn v3.2, waiting 0.5 s of silence before checking.
- **Parakeet EOU:** an optional "cautious" mode only.

All measurements below use real public recordings, run on CPU (od-cpu1).

| what | measured | target / note |
|---|---|---|
| WER vs model card, 560 ms mode | LibriSpeech clean 2.75% (card 2.46), other 4.98% (5.07), TED-LIUM 3.50% (3.54). AMI 12.44% at n=2000 (11.88). Earnings-22 11.61% at n=1500 (12.82, better than the card). | 11 of 15 cells are within 0.5 pt, and the card value is inside our 95% interval in 13 of 15. The streaming loop matches the card on normal-length clips. |
| 560 ms vs 160 ms chunks | 560 ms is better on every set, by +0.18 to +1.14 pt | 560 ms is locked |
| **Decision agreement, real speech** (SLURP, C1 on the gold transcript vs on the ASR transcript) | **89.2%** [86.2, 91.6], n=500. Headset 94.2%, far-field 84.6%. 99.1% when the transcript is exact. | **Target 97%: NOT met.** |
| Accuracy loss from ASR (SLURP) | 89.8% -> 82.0% (-7.8 pt). ASR WER on SLURP is 17.2%. | |
| End of turn, live mic (SLURP / AMI) | False cut 1.4% / 5.2%. p50 775 / 791 ms after speech ends. No decision within 2.5 s on 6.0% / 35.6% of clips. | AMI misses are high (see the warnings below) |
| Latency after speech, explicit end | **about 100 ms** (72 ms ASR flush + 28 ms C1) | Measured on the L4 on 17 Oct, but with **synthetic** audio. Not re-measured on real audio on a GPU. |
| Latency after speech, live mic | **about 0.9 s** p50 | Arithmetic: 775 + 72 + 28. Not measured end to end. |

**Warnings (from the skeptic):**
1. **Very short clips often come back empty.** In 560 ms streaming mode, AMI clips under 0.5 s return no text 58 times out of 69; offline mode fails on 28 of them. One-word answers like "yes" or "no" are exactly this case. Test short clips before relying on streaming mode for one-word answers. Offline mode handles them better.
2. **The AMI end-of-turn misses are only half explained.** Of the 35.6%, about 17.6 pt are clips where the voice detector never started. The other ~18 pt are cases where Smart Turn judged the turn "not finished", including 57 of 200 clips of 2 s or longer.
3. **Do not quote the 17 Oct "97% voice agreement".** It came from clean synthetic speech with 5.7% WER.
4. **SLURP audio is non-commercial (CC BY-NC 4.0).** Use it for evaluation only.

## 3. Image path: what is locked

**Native resolution, no token cap.** Capping and upscaling both lost accuracy on 17 Oct: cap64 scored 82.5 vs native 85.5, and upscaling scored 79.2.

- **Noise floor, measured (H100, 17 Oct, n=200):** the identical input (cap256 = native token counts, 0 mismatches) agreed with native only **98% (196/200, Wilson [95.0, 99.2])**. This held within one session and across sessions. The image path is not perfectly repeatable yet.
- **Same-server native-vs-native test (T10a):** not run.
- **Sample size problem:** even 200/200 only reaches a Wilson lower bound of 98.1%. **The 99.5% parity bar cannot be judged on 200 images.** A much larger image set is needed.
- **Latency:** native p50 **114.8 ms**, p95 187 ms per image decision (H100). A text-only call takes 32 ms.
- **Exact latency win:** **none measured.** T10b, T10c and T10d (keep features on device, 4 processor workers, client-side exact resize) were all not run.
- **Quality:** Vision Index 77.7 vs Jev 85.1 (base Qwen 73.6). This is a working preview, not a win.

## 4. Results table

| metric | before (measured) | after this round | L4 relative change | projected H100 (estimate, not measured) |
|---|---|---|---|---|
| Text batch-1 p50, server | 32.4 ms (H100, 17 Oct) | same, no change adopted | not measured | about 26-30 ms if the exact bundle and FP8 pass |
| Text batch-1 p99, server | 84 ms (H100) | same | not measured | better only if T1 finds GC pauses |
| Text throughput / cost at 100% use | about 320K/h, $0.0137 per 1K (Modal H100) | same | not measured | +21% / $0.0114 if block-FP8 passes alone; +7-10% with the margin gate |
| Text parity | 99.77% (S1, 8,143 items) | same | n/a | every change must keep a Wilson lower bound >= 99.5% |
| End-to-end from the laptop | 137 ms p50 (us-west; about 94 ms of it is network) | same | n/a | about 80-90 ms if hosted in us-east (arithmetic from netprobe) |
| Voice WER (560 ms) | card figures only | measured: matches the card (see section 2) | n/a | n/a |
| Voice decision agreement | 97% (synthetic, n=100) | **89.2% real speech** (n=500) | n/a | needs C2.1 training |
| Voice latency, explicit end | about 100 ms (L4, synthetic) | same, not re-measured | n/a | not measured on H100 |
| Image decision p50 | 114.8 ms (H100) | same | not measured | no exact win found yet |
| Image noise floor | 98% (n=200) | same | T10a not run | n/a |

## 5. H100 confirm proposal (GO point: needs the owner's OK)

**My advice is to wait.** The plan only lets arms that passed on the L4 go to the H100, and none has run. First unblock the L4 windows, then run `RUN_ORDER.sh` one window at a time, T0a first. That costs $0, but each window takes production down for about 35-45 min.

When the L4 results are in:

- **Modal account:** jaypatil-duke, one H100 session, region **'any'** (1.0x price; narrow regions cost 1.75x).
- **Budget:** hard stop **$1.90**; launch nothing new after $1.60. Expected about $1.5 (about $0.48 overhead + $0.30 reference + up to 3 arms at about $0.25 each).
- **Arms.** Each is checked on all 8,143 items against same-session S1, with batch-1 p50/p95/p99, c64 throughput and cost per 1K:
  - **A.** S1 BF16 reference, run fresh.
  - **B.** Exact bundle: only the L4 passers among T2 full-graph prefill, T3 GC fix, T4 ids / `/v1/score`, and T5 head slice.
  - **C.** Block-FP8, only if L4 parity was >= 99.2% alone or the margin gate passed on held-out data. The gate is judged offline against arm A.
  - **D.** A cache knob, only if it gave more than 5% throughput on the L4.
- **Adopt rule:** Wilson lower bound >= 99.5% on 8,143 items **and** a real gain (p50 or p99 at least 2 ms lower, or throughput at least 5% higher). Otherwise record the arm and drop it.

The other option is to skip the L4 and run arms A + B + C directly on the H100, within the same cap. It never touches production, but untested patches (T2, T5) may fail to boot, and money spent on an arm that fails is lost. I do not recommend it.

## 6. What moves to C2.1 (needs training; nothing here touches the current C2 run)

1. **ASR-noised transcripts in training** (WER 3-15%), to lift real-speech decision agreement from 89% toward 97%. Far-field speech is the weakest case.
2. **Short spoken answers:** fix or route around the empty transcripts on clips under 1 s (test offline mode for short clips, and lower the VAD start threshold).
3. **Images trained at a fixed token budget** (e.g. 128). That would make cap128 the native setting and save about 20 ms per image call. Training on image data is also the only way to close the 77.7 vs 85.1 Vision Index gap.
4. **Order-invariant choice training,** so the second option-order view can be dropped (47% of items use 2 views).
5. **Static-first prompt layout, compact JSON,** and context distillation of the definitions card.
6. **FP8 QAD** if block-FP8 lands at 99.2-99.4%. Re-fit the FP8 margin gate after C2, because thresholds are model-specific.
7. **Distilled 0.8B/2B first tier with deferral.** This is a cost experiment; no paper shows 99.5% agreement for such a student.
8. **After C2 trains:** re-run parity, attach the same voice and image stack, and re-run the real-audio and Vision Index tests on C2.

---

Small fix: `PROD_DOWNTIME.log` says pid 1219 "started 08:28Z". The skeptic found it started at 03:41:24Z, at VM boot. The conclusion that no window was opened is unchanged.
