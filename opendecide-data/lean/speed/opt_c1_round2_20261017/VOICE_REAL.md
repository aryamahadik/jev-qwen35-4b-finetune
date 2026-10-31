# VOICE_REAL: real-audio tests of the voice cascade (Track B, 17 Oct 2026)

Run on `od-cpu1` (c3-standard-8, Xeon Platinum 8481C Sapphire Rapids, 8 vCPU = 4 cores x 2 HT, AMX-bf16, **CPU only**; no GPU, no Modal, no paid API). All data are public; this file holds counts and rates only, no row text. Machine-readable twin: `VOICE_REAL.json`.

## Recommendation (locked voice config)

- **ASR model:** keep NVIDIA Nemotron Speech Streaming EN 0.6B (NVIDIA Open Model License, commercial use permitted). Our streaming loop reproduces the card at 560 ms: LibriSpeech clean +0.29 pt, other -0.09, TED-LIUM -0.04 (all within 0.5 pt, n=500 each). AMI is +1.78 pt at n=500 and +0.56 pt at n=2000 (card inside our CI); Earnings-22 is -1.31 pt at n=500 and -1.21 pt at n=1500 (we are BETTER than the card; offline mode matches it, +0.07 pt). So the strict +-0.5 pt rule is missed on AMI at n=500 (sampling: 3.6k reference words) and on Earnings-22 (in the favourable direction); nothing points to a broken loop.
- **Chunk mode:** 560 ms (att_context [70,6]) with a forced flush at end of input. On identical utterances 160 ms is worse than 560 ms in every set (ls_clean +0.35, ls_other +0.18, tedlium +0.56, ami +1.14, earnings22 +1.01 pt; the paired 95% interval excludes zero in tedlium, earnings22 and touches zero in ls_clean), the same ordering as the card. On this CPU, bf16, one thread: 560 ms chunks take 249 ms per 560 ms of audio (0.44x real time); 160 ms chunks take 225 ms per 160 ms (1.4x, not real time). Use offline mode for whole-file uploads. The flush is needed: the card's loop drops the last partial chunk (see the ablation).
- **End of turn:** default = an explicit end signal (client closes the stream, push-to-talk, file upload): no wait, no false cuts. For a live microphone use Silero VAD + Smart Turn v3.2 (BSD-2, CPU, 43 ms per call on one idle thread) with stop_secs = 0.5 s as the locked default: SLURP false cut 1.4%, latency p50 775 ms / p90 1103 ms, no decision within 2.5 s 6.0%; AMI false cut 5.2%, latency p50 791 ms / p90 1015 ms, no decision within 2.5 s 35.6%. A faster setting (stop 0.2 s) trades latency for cuts: SLURP false cut 5.6%, latency p50 453 ms / p90 664 ms, no decision within 2.5 s 6.0%; AMI false cut 11.6%, latency p50 463 ms / p90 675 ms, no decision within 2.5 s 35.0%. Silero alone at 0.5 s is worse than with Smart Turn on conversational speech (AMI false cut 11.8% vs 5.2%).
- **Latency budget (arithmetic across machines):** live microphone with Silero + Smart Turn at 0.5 s: about 775 ms p50 to the end-of-turn decision (measured here, SLURP) + about 72 ms ASR flush + about 28 ms C1 (both L4 p50 from the 17 Oct synthetic-audio step) = roughly 0.9 s after the user stops; with an explicit end signal only the last two terms remain (about 100 ms). On CPU instead of the L4 the ASR flush chunk is 240 ms (bf16, one thread) / 103 ms (4 threads).
- **Parakeet Realtime EOU 120M:** not recommended as the primary method. It cuts least (SLURP 0.4%, AMI 0.4%) but decides late: SLURP latency p50 1091 ms / p90 2911 ms with a noise-floor tail (751 / 1551 ms with digital silence), 5.6% (SLURP) and 13.6% (AMI) not decided within 2.5 s, and it is a second always-on streaming model (72 ms of one thread per 160 ms chunk). The vendor figure (p50 160 ms on TTS audio) is not reproduced on real speech. Keep it as an optional 'cautious' mode.
- **Decision agreement (real audio):** gold vs ASR transcript on SLURP, scenario level n=500: 89.2% [86.17, 91.63] -> the >= 97% target is NOT met. Close-talk (headset) 94.19%, far-field 84.56%; 99.1% when the transcript is exact, 70.9% with 3+ word errors. Accuracy falls 7.8 pt (89.8% -> 82.0%) because ASR WER on SLURP is 17.18%. Intent level (60 options, n=150): agreement 89.33% [83.38, 93.33], accuracy 84.67% -> 78.0%. The 97% seen on 17 Oct was synthetic Kokoro speech with 5.7% WER; do not quote it for noisy or far-field speech.

## 1. ASR sanity: WER of Nemotron Speech Streaming EN 0.6B vs its model card

Loop = the model-card streaming recipe through transformers 5.17 (`NemotronAsrStreamingForRNNT`), plus an explicit end-of-input flush (zero-pad the last real chunk, then one silent chunk). Normaliser = whisper-normalizer 0.1.12 (the one named on the card), corpus-level WER, 95% interval = bootstrap over utterances. Utterances = a seeded random sample of the test set (500 per set; s160 uses the first 150 of the same shuffled order). 'card' = the card's OpenASR WER at the same chunk size (the card has no number for offline; the 1.12 s column is shown). Pass = |delta| <= 0.5 pt (brief) or card value inside our 95% interval (sampling-aware).

| set | mode (dtype) | n utts | WER % [95% CI] | card % | delta pt | within 0.5 pt | card in CI |
|---|---|---|---|---|---|---|---|
| LibriSpeech test-clean | s560 (fp32) | 500 | 2.75 [2.26, 3.31] | 2.46 | +0.29 | yes | yes |
| LibriSpeech test-clean | s160 (bf16) | 150 | 3.04 [2.13, 3.99] | 2.56 | +0.48 | yes | yes |
| LibriSpeech test-clean | offline (fp32) | 500 | 2.59 [2.11, 3.11] | 2.32 | +0.27 | yes | yes |
| LibriSpeech test-other | s560 (bf16) | 500 | 4.98 [4.33, 5.67] | 5.07 | -0.09 | yes | yes |
| LibriSpeech test-other | s160 (bf16) | 150 | 4.50 [3.43, 5.75] | 5.57 | -1.07 | NO | yes |
| LibriSpeech test-other | offline (fp32) | 500 | 4.77 [4.13, 5.49] | 4.84 | -0.07 | yes | yes |
| TED-LIUM 3 test | s560 (bf16) | 500 | 3.50 [3.03, 3.97] | 3.54 | -0.04 | yes | yes |
| TED-LIUM 3 test | s160 (bf16) | 150 | 3.84 [2.92, 4.87] | 3.77 | +0.07 | yes | yes |
| TED-LIUM 3 test | offline (fp32) | 500 | 3.15 [2.71, 3.60] | 3.50 | -0.35 | yes | yes |
| AMI IHM test | s560 (bf16) | 500 | 13.66 [12.12, 15.58] | 11.88 | +1.78 | NO | NO |
| AMI IHM test | s160 (bf16) | 150 | 14.67 [11.71, 18.23] | 14.71 | -0.04 | yes | yes |
| AMI IHM test | offline (fp32) | 500 | 12.97 [11.28, 15.01] | 11.73 | +1.24 | NO | yes |
| Earnings-22 test | s560 (bf16) | 500 | 11.51 [10.48, 12.57] | 12.82 | -1.31 | NO | NO |
| Earnings-22 test | s160 (bf16) | 150 | 12.51 [10.64, 14.75] | 13.01 | -0.50 | yes | yes |
| Earnings-22 test | offline (fp32) | 500 | 12.59 [11.59, 13.61] | 12.52 | +0.07 | yes | yes |

**Summary: 11 of 15 cells are within 0.5 pt of the card; the card value lies inside our 95% interval in 13 of 15.** Misses: ls_other/s160 (-1.07, n=150); ami/s560 (+1.78, n=500); ami/offline (+1.24, n=500); earnings22/s560 (-1.31, n=500). All three LibriSpeech/TED-LIUM s560 cells (the locked mode) pass; the misses are on the two noisy-domain sets (see the larger samples below) and on small-n s160/offline cells.

Larger independent samples for the two sets that missed at n=500 (s560, bf16):

| set | n utts | ref words | WER % [95% CI] | card % | delta pt | card in CI |
|---|---|---|---|---|---|---|
| ami_big | 2000 | 15407 | 12.44 [11.66, 13.24] | 11.88 | +0.56 | yes |
| earnings22_big | 1500 | 26915 | 11.61 [11.03, 12.25] | 12.82 | -1.21 | NO |

bf16 (AMX) vs fp32 on identical utterances (why mixed dtypes do not matter):

| set (s560) | n | identical hypotheses | WER main run | WER other dtype |
|---|---|---|---|---|
| ls_clean | 150 | 143 | 2.69 (fp32) | 2.65 (bf16) |
| ami | 500 | 479 | 13.66 (bf16) | 13.63 (fp32) |
| earnings22 | 500 | 461 | 11.51 (bf16) | 11.58 (fp32) |

Chunk mode, paired on the same 150 utterances per set (delta with bootstrap 95% CI; positive = first is worse):

| set | WER s160 | WER s560 | WER offline | s160 - s560 [CI] | offline - s560 [CI] |
|---|---|---|---|---|---|
| LibriSpeech test-clean | 3.04 | 2.69 | 2.72 | +0.35 [+0.00, +0.78] | +0.03 [-0.18, +0.28] |
| LibriSpeech test-other | 4.50 | 4.32 | 4.17 | +0.18 [-0.28, +0.67] | -0.15 [-0.60, +0.27] |
| TED-LIUM 3 test | 3.84 | 3.28 | 3.08 | +0.56 [+0.18, +0.98] | -0.20 [-0.64, +0.29] |
| AMI IHM test | 14.67 | 13.53 | 11.16 | +1.14 [-0.53, +2.65] | -2.38 [-4.00, -0.82] |
| Earnings-22 test | 12.51 | 11.50 | 12.67 | +1.01 [+0.12, +2.03] | +1.17 [+0.30, +2.05] |

Why the flush matters (same utterances, s560, bf16): the card's loop drops the final partial chunk. LibriSpeech test-other n=150: 6.97% without flush vs 4.32% with flush; TED-LIUM 3 test n=150: 5.32% without flush vs 3.28% with flush.

Sanity check of our .nemo -> HF conversion of Parakeet Realtime EOU 120M: its own transcripts reach 3.38% WER on 60 LibriSpeech test-clean utterances (160 ms chunks), so the converted weights are intact.

## 2. Decision agreement on SLURP test (real spoken commands)

500 distinct SLURP test utterances (one random recording each; seeded). ASR = Nemotron s560 (fp32): WER 17.18% against the gold transcript (headset 12.71%, far-field 21.07%; condition inferred, see caveats), 43.2% of utterances exact after normalisation.

C1 = Qwen3.5-4B + merged `q35_4b_main500k`, BF16, HF transformers on CPU, served readout A5 (identity + reversed option order averaged), layout schema_branch_mark. Each utterance becomes one API-v1-style choice question (state `Customer message:` + transcript). The gold row uses the gold transcript; the ASR row uses the raw ASR text (with its punctuation and capitals). Same question, same options; only the text differs. Labels are SLURP's official scenario (18 options, short descriptions) and scenario_action intent (60 options, no descriptions).

| level | n | agreement gold vs ASR (Wilson 95%) | flips | accuracy gold transcript | accuracy ASR transcript | accuracy change | max abs dp p50 / p95 / max |
|---|---|---|---|---|---|---|---|
| scenario, 18 options | 500 | **89.2%** [86.17, 91.63] | 54 | 89.8% | 82.0% | -7.8 pt | 0.0058 / 0.7592 / 0.9417 |
| intent, 60 options | 150 | **89.33%** [83.38, 93.33] | 16 | 84.67% | 78.0% | -6.7 pt | 0.0093 / 0.6878 / 0.9361 |

Target >= 97% agreement: **NOT met** on this set. Breakdown (scenario level):

| slice | n | agreement % | accuracy gold / ASR % |
|---|---|---|---|
| headset recordings | 241 | 94.19 [90.49, 96.51] | 88.8 / 85.89 |
| far-field recordings | 259 | 84.56 [79.65, 88.45] | 90.73 / 78.38 |
| ASR word errors: 0 | 216 | 99.1 | |
| ASR word errors: 1-2 | 198 | 86.4 | |
| ASR word errors: 3-plus | 86 | 70.9 | |

Of the 54 flips, the gold-transcript decision was the correct one in 42 and the ASR-transcript decision in 3. Most frequent flips (gold -> ASR label): qa->general (4), lists->calendar (2), email->general (2), play->general (2), social->general (2), general->play (2).

## 3. End of turn (CPU timings)

Reference speech end = last word end from CTC forced alignment of the gold transcript (wav2vec2-base-960h, 20 ms steps). Each clip is followed by a 2.5 s tail: noise at the clip's own noise floor (primary) or digital zeros. Latency = decision time minus reference end (stream time, plus idle-machine CPU compute: Smart Turn 43.4 ms, EOU 71.7 ms, Silero 0.175 ms; single thread). False cut = decision before the last word started (at least one word lost). Miss = no decision within the 2.5 s tail (Smart Turn's 3 s silence fallback therefore counts as a miss). (a) = Silero VAD (p>=0.5, 0.2 s of speech to start) -> after `stop` s of silence run Smart Turn v3.2 on the audio since speech start; complete (p>0.5) fires, incomplete waits (fallback 3 s). VAD-only fires at every VAD stop. (b) = Parakeet Realtime EOU 120M, first `<EOU>` token, 160 ms chunks.

### SLURP test (500 clips; short commands)

| method | tail | decided | false cut % | miss % | latency p50 / p90 / p95 ms | decided in 0-1 s, no cut % |
|---|---|---|---|---|---|---|
| Silero+SmartTurn stop 0.2 s | noise | 470/500 | 5.6 | 6.0 | 453.0 / 664.0 / 731.0 | 87.6 |
| Silero+SmartTurn stop 0.3 s | noise | 466/500 | 4.8 | 6.8 | 555.0 / 795.0 / 893.0 | 86.6 |
| Silero+SmartTurn stop 0.5 s | noise | 470/500 | 1.4 | 6.0 | 775.0 / 1103.0 / 1196.0 | 77.0 |
| Silero only 0.2 s | noise | 499/500 | 8.2 | 0.2 | 404.0 / 612.0 / 657.0 | 91.4 |
| Silero only 0.5 s | noise | 499/500 | 2.0 | 0.2 | 736.0 / 1056.0 / 1137.0 | 84.6 |
| Silero only 0.8 s | noise | 499/500 | 1.2 | 0.2 | 1044.0 / 1425.0 / 1572.0 | 38.4 |
| Parakeet EOU 120M | noise | 472/500 | 0.4 | 5.6 | 1091.0 / 2911.0 / 3151.0 | 41.6 |
| Silero+SmartTurn stop 0.2 s | zeros | 469/500 | 5.6 | 6.2 | 403.0 / 513.0 / 562.0 | 87.4 |
| Silero+SmartTurn stop 0.3 s | zeros | 476/500 | 4.8 | 4.8 | 503.0 / 629.0 / 672.0 | 88.8 |
| Silero+SmartTurn stop 0.5 s | zeros | 477/500 | 1.4 | 4.6 | 695.0 / 819.0 / 864.0 | 92.6 |
| Silero only 0.2 s | zeros | 499/500 | 8.2 | 0.2 | 356.0 / 465.0 / 513.0 | 91.6 |
| Silero only 0.5 s | zeros | 499/500 | 2.0 | 0.2 | 652.0 / 776.0 / 820.0 | 96.8 |
| Silero only 0.8 s | zeros | 499/500 | 1.2 | 0.2 | 940.0 / 1065.0 / 1108.0 | 75.0 |
| Parakeet EOU 120M | zeros | 486/500 | 0.4 | 2.8 | 751.0 / 1551.0 / 1931.0 | 71.8 |

### AMI IHM test (500 segments; conversational, many 1-2 word backchannels)

| method | tail | decided | false cut % | miss % | latency p50 / p90 / p95 ms | decided in 0-1 s, no cut % |
|---|---|---|---|---|---|---|
| Silero+SmartTurn stop 0.2 s | noise | 325/500 | 11.6 | 35.0 | 463.0 / 675.0 / 737.0 | 51.0 |
| Silero+SmartTurn stop 0.3 s | noise | 326/500 | 8.6 | 34.8 | 571.0 / 791.0 / 861.0 | 54.0 |
| Silero+SmartTurn stop 0.5 s | noise | 322/500 | 5.2 | 35.6 | 791.0 / 1015.0 / 1283.0 | 51.4 |
| Silero only 0.2 s | noise | 412/500 | 21.2 | 17.6 | 408.0 / 628.0 / 700.0 | 59.6 |
| Silero only 0.5 s | noise | 412/500 | 11.8 | 17.6 | 728.0 / 940.0 / 1024.0 | 64.8 |
| Silero only 0.8 s | noise | 412/500 | 6.4 | 17.6 | 1030.0 / 1259.0 / 1323.0 | 29.2 |
| Parakeet EOU 120M | noise | 432/500 | 0.4 | 13.6 | 1591.0 / 2849.0 / 3080.0 | 25.2 |
| Silero+SmartTurn stop 0.2 s | zeros | 313/500 | 11.6 | 37.4 | 383.0 / 527.0 / 651.0 | 48.6 |
| Silero+SmartTurn stop 0.3 s | zeros | 324/500 | 8.6 | 35.2 | 487.0 / 623.0 / 783.0 | 53.6 |
| Silero+SmartTurn stop 0.5 s | zeros | 315/500 | 5.2 | 37.0 | 687.0 / 894.0 / 1306.0 | 52.6 |
| Silero only 0.2 s | zeros | 398/500 | 21.2 | 20.4 | 324.0 / 468.0 / 553.0 | 57.0 |
| Silero only 0.5 s | zeros | 398/500 | 11.8 | 20.4 | 632.0 / 772.0 / 897.0 | 65.4 |
| Silero only 0.8 s | zeros | 398/500 | 6.4 | 20.4 | 930.0 / 1097.0 / 1232.0 | 53.4 |
| Parakeet EOU 120M | zeros | 438/500 | 0.4 | 12.4 | 671.0 / 1951.0 / 2571.0 | 58.0 |

Validation of the EOU harness on clean read speech (first 100 LibriSpeech test-clean sample clips, long ones): Parakeet EOU false cut 1.0%, latency p50 941.0 ms (zeros) / 1291.0 ms (noise). Smart Turn / VAD cut those long multi-clause clips at ordinary pauses, which is why the rest of this section uses short-command and conversational sets.

## 4. CPU compute on the idle VM (c3-standard-8)

| item | 1 thread | 4 threads (one per physical core) |
|---|---|---|
| Smart Turn v3.2 (int8 ONNX, 8 s window) per call | 43.4 ms p50 (features 3.5 + model 40.0) | 42.9 ms |
| Silero VAD per 32 ms window | 0.175 ms | 0.192 ms |
| Parakeet EOU 120M per 160 ms chunk (fp32) | 71.7 ms p50, 86.5 p95 | 33.2 ms p50 |
| Nemotron s560 per 560 ms chunk (bf16) | 248.6 ms p50, 264.2 p95; last (flush) chunk 240.5 | 107.6 ms; flush 102.7 |
| Nemotron s160 per 160 ms chunk (bf16) | 224.9 ms p50 | 94.5 ms |
| Nemotron offline, 3.23 s clip (bf16) | 411.3 ms | 180.1 ms |
| Nemotron s560 per 560 ms chunk (fp32) | 544.3 ms p50, 579.3 p95; last (flush) chunk 548.9 | 180.7 ms; flush 167.1 |
| Nemotron s160 per 160 ms chunk (fp32) | 276.6 ms p50 | 103.3 ms |
| Nemotron offline, 3.23 s clip (fp32) | 908.7 ms | 357.5 ms |

Reading: on this CPU the 560 ms mode runs faster than real time on one thread in bf16 (0.44x), the 160 ms mode does not (1.4x). These are CPU figures; the L4 figures of 17 Oct (ASR flush p50 72 ms) are a different machine.

## 5. Deviations and caveats

- Sampling: 500 seeded random utterances per set (s160: first 150 of the same shuffled order; AMI and Earnings-22 got larger independent samples of 2000 and 1500). Intervals are bootstrap over utterances, so they ignore speaker/recording correlation.
- dtype: s560 on LibriSpeech test-clean is fp32; the other s560 sets and all s160 are bf16 (AMX) to fit the CPU budget; offline is fp32. bf16 vs fp32 on identical utterances: see the dtype table (WER differences <= 0.07 pt).
- Offline mode is compared with the card's 1.12 s column (the card has no fully offline number). The HF offline path is slightly worse than 560 ms streaming on Earnings-22 (139 of 500 utterances worse, 60 better); not investigated further.
- Streaming runs one stream per process: transformers' streaming generate does not support a batch of streams (a batched trial returned corrupt text, 1 of 16 identical), so CPU RTFs in the WER tables come from a loaded VM and are only indicative; the idle-VM timings in section 4 are the CPU figures.
- TED-LIUM comes from sanchit-gandhi/tedlium-data because the Open-ASR-leaderboard dataset no longer ships tedlium; the 1155-utterance filtering matches the Open-ASR test size. Reference cleanup for TED-LIUM follows the ESB script as I remember it (remove <unk>, re-attach " '"); not diffed against that script.
- SLURP: audio licence is CC BY-NC 4.0 (the brief says CC BY 4.0, which is true for the text only); used for evaluation only. Gold intent = official scenario_action (60 values, 18 scenarios); the HF copy's own intent column has 18 non-official legacy values and was ignored. Headset/far-field labels are inferred from row order within a slurp_id (supported by the 12.7% vs 21.1% WER gap), not read from file names.
- C1 here is the HF reference path on CPU (BF16, torch fallback kernels for the gated delta rule, padding multiple 64), not the L4 SGLang server. The prompt wording and the short scenario descriptions are my construction (no Jev data); other wording would move the absolute accuracy but the gold-vs-ASR comparison uses identical prompts. The 60-option intent level has no descriptions and a smaller n.
- End of turn: reference speech end comes from forced alignment (20 ms steps, a few tens of ms of error). Streams are one clip plus a synthetic 2.5 s tail, so false cuts only count pauses inside the clip, not the next speaker. The Smart Turn / VAD state machine is my reading of the pipecat smart-turn repo (VAD stop event -> model on audio since speech start; 3 s silence fallback), not pipecat's own code. VAD needs 0.2 s of speech to start, so AMI backchannels (1-2 words) are often never detected: this limit matters for very short spoken answers.
- The first 100 LibriSpeech test-clean clips used to validate the EOU harness are the longest in the file (the dataset is length-sorted), so VAD/Smart Turn rows on that set are not meaningful and are shown only for the EOU check.
- Parakeet EOU was converted by us from the .nemo file with the converter functions shipped in transformers (it is the same cache-aware FastConformer-RNNT family); 3.38% WER on 60 LibriSpeech clips shows the weights are intact, but the conversion is not the vendor's own runtime.
- Housekeeping: gcp_run.sh once pulled a probe log into c2_build/zed_orch/logs (gcp_r2_probe1.log); I deleted that file. gcp_run.sh also writes its job scripts and logs under ~/jobs on the VM. Everything else is under ~/opt_r2/voice on od-cpu1 (a sibling of other agents' files in ~/opt_r2, which were not touched). I paused (SIGSTOP/SIGCONT) and restarted only my own jobs. od-cpu1 was left running; od-l4b and the production server were never touched.

## 6. Sources, revisions, licences

- **librispeech_test_clean_other**: hf-audio/open-asr-leaderboard (config librispeech, parquet); revision `de79e57adf9983993bcc72586d7313460825f5eb`; licence: CC BY 4.0 (LibriSpeech, OpenSLR 12); the HF card carries no licence field
- **ami_ihm_test**: hf-audio/open-asr-leaderboard (config ami, parquet; ESB/Open-ASR segmentation of AMI IHM test); revision `de79e57adf9983993bcc72586d7313460825f5eb`; licence: CC BY 4.0 (AMI corpus); the HF card carries no licence field
- **earnings22_test**: hf-audio/open-asr-leaderboard (config earnings22, parquet); revision `de79e57adf9983993bcc72586d7313460825f5eb`; licence: CC BY-SA 4.0 per the upstream Earnings-22 release (revdotcom/speech-datasets); the HF card carries no licence field (not re-verified here)
- **tedlium3_test**: sanchit-gandhi/tedlium-data (split test; TED-LIUM release 3). The Open-ASR-leaderboard repo no longer ships a tedlium folder on main, so this public copy is used; revision `8083dbe64f82e17b6be070a02b9239e9b847b6ce`; licence: CC BY-NC-ND 3.0 (TED-LIUM; confirmed on the distil-whisper/tedlium card); the HF card of the copy has no licence field; 314 'ignore_time_segment_in_scoring' gap rows removed (-> 1155, the Open-ASR/ESB test size); '<unk>' removed and " '" re-attached in the reference following the ESB convention (from memory, not diffed against that script)
- **slurp_test**: marcel-gohsen/slurp (audio + transcripts, split test, 13078 recordings) joined by slurp_id to the official metadata pswietojanski/slurp dataset/slurp/test.jsonl; revision `HF 6ee060bbac668abfd2f32d8fefb980d1699c32b5; GitHub 8eb16545762b`; licence: text/annotations CC BY 4.0; AUDIO CC BY-NC 4.0 (official LICENSE.txt). The task brief says CC BY 4.0: that holds for the text only; the recordings are non-commercial. Used here only for evaluation, nothing redistributed.; gold intent = official scenario + '_' + action (60 distinct values over train/dev/test, 18 scenarios); the HF 'intent' column is a legacy field with 18 extra non-official values and was not used
- **nemotron_asr**: repo: nvidia/nemotron-speech-streaming-en-0.6b; revision: ebe59e5a817142986528bbbee5dba8db7b38ed50; licence: NVIDIA Open Model License (commercial use permitted); runtime: transformers 5.17.0 NemotronAsrStreamingForRNNT, torch 2.14.0 CPU
- **parakeet_eou**: repo: nvidia/parakeet_realtime_eou_120m-v1; revision: a7e2b4629593dce0ec19f600e00e9904353fda2d; licence: NVIDIA Open Model License; runtime: .nemo converted by us to the HF NemotronAsrStreaming layout with transformers' own converter functions (same cache-aware FastConformer-RNNT family; att_context [70,1]); first <EOU> (id 1024) in the greedy output
- **smart_turn**: repo: pipecat-ai/smart-turn-v3 (smart-turn-v3.2-cpu.onnx, 8 MB int8); revision: f766f81d3cfdf7737ac64aad813d91bbfd56bf93; licence: BSD-2-Clause; code: pipecat-ai/smart-turn 4786657e242d (inference.py recipe: Whisper feature extractor, 8 s window, p>0.5 = complete)
- **silero_vad**: repo: silero-vad 6.2.3 wheel (silero_vad.onnx, 32 ms windows); licence: MIT (upstream snakers4/silero-vad; the wheel metadata has no licence field)
- **wav2vec2_aligner**: repo: facebook/wav2vec2-base-960h; revision: 22aad52d435eb6dbaf354bdad9b0da84ce7d6156; licence: Apache-2.0; use: CTC forced alignment of the gold transcript -> reference speech end (20 ms resolution)
- **c1**: base: Qwen/Qwen3.5-4B @ 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a; adapter: q35_4b_main500k sha256 507d1c29690579f9...; load: decoder_io.load + merge_and_unload, BF16, layout schema_branch_mark, style cygnet, no PRISM-X; readout A5 = predict(tta_choice=True)
- Normaliser / statistics: whisper-normalizer 0.1.12 EnglishTextNormalizer (the version named on the Nemotron model card); corpus-level WER (sum of word errors / sum of reference words), 95% interval = bootstrap over utterances (2000 resamples)

## 7. Files

`scripts/` (prep, ASR runner, end-of-turn runner, C1 SLURP runner, analysis), `results/pulled/` (per-utterance outputs: hypotheses, timings, decisions; no audio), `assets/samples/*/manifest.jsonl` (the sampled utterance ids with public references), `RESEARCH_PLAN.json` (input).
