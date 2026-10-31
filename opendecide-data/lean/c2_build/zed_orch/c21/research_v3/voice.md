# C2.1 research v3: VOICE (spoken input to a text decision model)

Date of research: 18 Oct 2026. Scope: cascade ASR (locked: NVIDIA Nemotron Speech Streaming EN 0.6B) in front of the text decision model. Compared against plan v2 (`C2_1_PLAN_v2.md`, section "GENERAL ROWS (about 7K) AND VOICE (about 2K)" and "MULTIMODAL").

Tags: [vendor-run] = number from the model's maker or a seller; [author-run] = paper authors' own experiment; [independent] = third party with no stake; UNVERIFIED = could not confirm. "Fetched" = I read the page; "search result" = only seen in a search snippet (weaker).

Tool limit note: the shared web-search budget ran out near the end. Licence checks for AMI, VCTK, Fluent Speech Commands, STOP, Earnings-22 and pyroomacoustics/jiwer were not completed (marked UNVERIFIED).

---

## 1. What plan v2 says about voice (so this file only adds or corrects)

- Line ~164: "ASR-noised copies of existing decision rows: TTS then ASR, 3-15% WER, run on the free L4." About 2K rows of about 35-37K new rows.
- Line ~414: "Voice (Nemotron EN 0.6B streaming, explicit end of input) and native images, attached unchanged."
- Nothing on: which fields are spoken, gold handling, TTS engine or licence, speaker diversity, number/code spoken forms, real-speech eval, or text-vs-speech consistency metrics. Voice data is the only place where the input distribution is changed by a component (the ASR) that we do not train, so these gaps matter.

---

## 2. What is new since plan v2

1. Nemotron has a newer sibling and a pinned-checkpoint problem.
   - The EN 0.6B card lists the current checkpoint as 03/13/2026; an older checkpoint (5 Jan 2026) lives on branch `nemotron-speech-streaming-jan2026`. Fetched: https://huggingface.co/nvidia/nemotron-speech-streaming-en-0.6b (accessed 18 Oct 2026).
   - Successor "Nemotron 3.5 ASR Streaming 0.6B", 04 Jun 2026, 40 locales, licence OpenMDW-1.1. NVIDIA recommends the English-only model for English-only use. Fetched: https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b. So the locked EN 0.6B is still the right pick, but the checkpoint revision must be pinned: ASR-specific error patterns are what we train against.
2. ASR errors do not hit all words equally. SpeechEvalX (arXiv 2610.17619, 13 Oct 2026, fetched https://arxiv.org/abs/2610.17619 and https://arxiv.org/html/2610.17619) [author-run]: single-edit corruptions on tool-calling utterances (Qwen2.5-7B-Instruct) cost: negation 25.7 points, number 21.9, entity 17.1, intent cue 12.4, other slot value 9.5, function word 2.9, other non-critical 1.4. Real ASR (WER 6.3 / 7.2 / 8.1%) cut joint call accuracy from 82.3% (reference text) to 74.9 / 73.2 / 71.9%. Authors' point: WER does not predict harm; role does. (EDIT by refuter 18 Oct: the 25.7/21.9/17.1/12.4/9.5/2.9/1.4 table is verified, from 210 sources with single synthetic edits, Llama-3.1-8B as sensitivity agent; the WER values 6.3/7.2/8.1 belong to Whisper-large-v3 / SenseVoice-Small / Paraformer-large on TTS-made benchmark audio (VoiceAgentBench + BFCL Audio, 594 sources), not Nemotron and not real speech. The paper states no code/data licence.)
3. Voice-style input costs more than typed noise. HIVE (arXiv 2608.03970, fetched https://arxiv.org/html/2608.03970v1) [author-run, five 7-14B instruct models, math/code/multiple-choice, no agents; the voice-style inputs are text rewrites made by Qwen2.5-7B-Instruct, not audio]: voice-style rewrites average about -9.7 vs about -3.0 for keyboard noise (EDIT by refuter 18 Oct: -9.7 and -3.0 are geometric-mean accuracy ratios, about 6.2 raw points for voice, not raw points; the gap is essentially absent on the multiple-choice sets, which is the closest shape to our option-readout, so this is an upper bound for us); "spoken-succinct" -24.1, casual -7.4, filler-stripped -7.6; homophone swaps only -0.4. A LoRA self-distillation fix closed the spoken gap only by hurting clean accuracy (60.9 to 58.0 at high rank) or did nothing (low rank, 57.2 to 56.5). Warning for us: naive LoRA robustness training can trade clean accuracy, so keep clean twins and keep the voice share modest.
4. TTS-to-ASR round trips are a weak augmenter on their own. Speak & Spell (arXiv 2409.06263, fetched https://arxiv.org/html/2409.06263) [author-run, DSTC11 dialogue state tracking, Tacotron2 + Whisper-base]: JGA on low-accuracy ASR 29.88 (none) vs 29.94 (TTS-ASR) vs 32.39 (LLM phonetic-error augmentation); named-entity change rate 38.84% (TTS-ASR) vs 95.47% (LLM phonetic); unique-word growth 1.01x vs 1.81x. TTS-ASR errors were less diverse than real ones. (EDIT by refuter 18 Oct: Table 2 shows TTS-ASR slightly above baseline in all four environments, e.g. 34.87 to 35.07 high-accuracy, but the paper's significance table marks it non-significant in all four; EPA with open LLMs OPT-6.7B / LLaMA2-7B gets 31.82 / 31.54 low-accuracy, so every strong variant is LLM-written and barred by rule 27.) Their best method uses GPT-3.5, which our no-LLM-generated-data rule bars; a program version (section 6) is the substitute.
5. Noise models learned on one ASR do not transfer to another. ISNI (arXiv 2410.15609, fetched https://arxiv.org/html/2410.15609v1) [author-run]: an ASR-specific noise generator trained on one system lost to an in-domain one on every task; their ASR-agnostic generator corrupted tokens at P(z) = 0.15 (ASR-GLUE) and 0.21 (DSTC10), tuned on validation, not matched to WER. For us this cuts both ways: we have ONE locked ASR, so we should harvest its own confusions (strong match), but we must not claim robustness to other ASRs.
6. Code is a separate failure class. "Lost in Transcription" (arXiv 2601.15339, fetched https://arxiv.org/html/2601.15339v1) [author-run, Whisper + Indic ASR, TTS = Edge TTS]: camelCase/snake_case names split or dropped ("getUserInfo" to "get your info"), operators lost, "async" heard as "a sink", "realloc()" as "real lock open close parentheses". Retrieval Recall@5 92% to 87% under ASR. (Mostly Indic speech; English evidence is thin.)
7. Spoken-command timing facts for Nemotron. Daily (a voice-agent vendor; blog fetched https://www.daily.co/blog/building-voice-agents-with-nvidia-open-models/) [vendor-run]: Nemotron needs about 320 ms of trailing silence to finalise the last words; their server sends 200 ms plus 120 ms synthetic silence; 160 ms chunk size; P50 server latency 19 ms (RTX 5090) / 27 ms (DGX Spark). Our "explicit end of input" must therefore pad silence; training audio needs the same. (EDIT by refuter 18 Oct: Daily's formula is `(right_context + 1) * shift_frames * hop_samples = (1+1)*16*160 = 5120 samples = 320 ms` and Daily ran the 160 ms chunk (right context 1). The post never says how the figure changes with chunk size, but the formula contains right_context, and the EN card maps chunk 0.56 s to right context 6 and 1.12 s to 13. 320 ms is therefore proven only for the 160 ms chunk; for 560/1120 ms it may need to be larger. UNVERIFIED, measure it.)
8. Onset errors are elevated in streaming. "Beyond Fresh Starts" (arXiv 2608.22101, 22 Aug 2026, abstract fetched https://arxiv.org/abs/2608.22101) [author-run]: resetting recognizer state per turn hurts utterance-onset words; stateful carry-over cut onset WER 15-21% relative. First words ("don't", "yes") are decision-bearing, so onset errors deserve their own augmentation.
9. Speech eval frameworks that keep text gold exist. "From Text to Voice" (arXiv 2605.15104, 20 May 2026, fetched https://www.alphaxiv.org/abs/2605.15104) [author-run]: text benchmarks converted to audio with TTS plus DEMAND noise at SNR down to 5 dB; text-vs-voice gaps 1.8 (Qwen3-Omni) to 4.8 points (GPT-Realtime-1.5) on Confetti. VoiceAgentBench (arXiv 2510.07978) and VoiceBench (arXiv 2410.17196, TACL 2026) give the protocol shape. No licence or code link was stated on the From Text to Voice page.

---

## 3. Corrections to plan v2

C1. "ASR-noised copies of existing decision rows" is under-specified and unsafe as written.
- Only what a human says out loud should pass through TTS and ASR: the user's utterance (request, answer, policy question). The agent's proposed action, diff, tool output and file content are produced by software and stay as exact text. Noising a command or diff as if spoken would teach the model a distribution it never meets. (Design reasoning; no source says otherwise.)
- When a user does dictate a command, path or flag, it is a distinct stratum with its own spoken forms (section 6.3).

C2. "3-15% WER" is a bad selector and probably too easy.
- Clean Kokoro speech through Nemotron will likely land near 1-3% WER (UNVERIFIED; the card gives only read-speech numbers: LS-clean 2.32%, LS-other 4.84%, 1.12 s chunk [vendor-run]).
- Real conversational or far-field audio is much worse: AMI 11.73-18.29% depending on chunk (1.12 s to 0.08 s), Earnings22 12.52-13.16%, GigaSpeech 9.66-11.17% [vendor-run, HF Open ASR leaderboard setup, whisper-normalizer, no PnC]. Fetched card above.
- VoiceBench found real recordings harder than TTS for every model that was tested (VITA 2.15 vs 3.21 on CommonEval) [author-run; fetched https://arxiv.org/html/2410.17196]. (EDIT by refuter 18 Oct: verified that all six models score better on synthetic, but only VITA shows a big gap; the other five differ by 0.02-0.21 points, and the Whisper+LLM cascade 'Naive' is 4.04 real vs 4.22 synthetic. The cascade, which is our shape, is the least hurt.) TTS-derived WER understates what a person at a laptop produces.
- WER averages hide the failures that matter (SpeechEvalX). Use measured per-row WER bands for coverage, but gate gold on decision-bearing-span survival (section 6.4).

C3. Compute is not the limit, so 2K rows is a design choice, not a budget cap.
- E2E Networks benchmark on one L4, fp16, LibriSpeech, 100 samples [vendor-run, a GPU seller]: Nemotron streaming 0.6B 86.9x real time at batch 1, 258.9x at batch 8; WER 10.30% (NeMo-scored, they say about 2-3 points inflated vs normalised). Fetched https://www.e2enetworks.com/blog/benchmarking-asr-models-nvidia-l4-parakeet-whisper-nemotron (27 Mar 2026). Several thousand short utterances take minutes. Kokoro speed on L4 is UNVERIFIED but it is an 82M model.
- This fits the owner's "all data, no estimate cuts" memory: generate a large pool, then select (section 6.5).

C4. Pin the checkpoint (see 2.1) and the chunk size. v2 says only "Nemotron EN 0.6B streaming". The Jan 2026 branch and the Mar 2026 main differ; WER also moves with chunk size (card, avg WER 6.93% at 1.12 s, 7.07% at 0.56 s, 7.67% at 0.16 s, 8.43% at 0.08 s [vendor-run]). Ask the product which chunk size ships (open question Q2); train on a mix.

C5. Number form is unknown. The card says punctuation and capitalisation are supported, but says nothing about inverse text normalisation (digits vs "forty two"); a community port notes the ambiguity (search result only). EDIT by refuter 18 Oct: the EN card says ITN only as a NeMo pipeline capability and describes the output as "the English alphabet, spaces, and apostrophes" plus punctuation/capitalisation, with WER scored w/o PnC by whisper-normalizer (fetched card): a weak hint toward number WORDS, not proof. The 3.5 card says its training text was "normalized to have spoken forms in text with punctuation and capitalization" (fetched), which is a hint for the sibling, not for EN. Do not assume. First task of the voice lane: a probe of about 100 TTS utterances with numbers, versions, ports, dates, paths, to see what Nemotron emits (then match it). Until then train on both forms (section 6.3).

C6. Rule 27 and the NVIDIA licence deserve one explicit owner line.
- Nemotron is under the NVIDIA Open Model License (not on the owner's MIT/Apache/BSD/CC list). Reading the licence page (fetched https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/): commercial use allowed; "NVIDIA claims no ownership rights in outputs"; no general ban on using outputs to train other models; guardrail-bypass termination clause; redistribution needs a copy of the licence plus a Notice file. So transcripts as training inputs look allowed. Not legal advice.
- Nemotron's own training labels used LLMs: author comment on the NVIDIA HF blog says punctuation/capitalisation pseudo-labels came from Qwen-2.5-7B-Instruct (fetched https://huggingface.co/blog/nvidia/nemotron-speech-asr-scaling-voice-agents); the 3.5 card says Qwen3-32B added punctuation (fetched). That is a component we deploy, not a dataset we train on, but it touches the spirit of rule 27. Owner should confirm the ASR component is outside the rule (it was already locked).

---

## 4. Licences (what we may use, what we may not)

### 4.1 ASR
| Item | Licence | Verdict |
|---|---|---|
| Nemotron Speech Streaming EN 0.6B | NVIDIA Open Model License (card: "ready for commercial/non-commercial use") | Locked. See C6. |
| Nemotron 3.5 ASR Streaming 0.6B | OpenMDW-1.1 | Not adopted. |

### 4.2 TTS engines (data generation only; we ship no TTS)
| Engine | Code / weights | Notes | Verdict |
|---|---|---|---|
| Kokoro-82M v1.0 (hexgrad) | Apache-2.0 / Apache-2.0 (fetched https://huggingface.co/hexgrad/Kokoro-82M and https://github.com/hexgrad/kokoro) | Card: "trained exclusively on permissive/non-copyrighted audio data": public domain, Apache/MIT audio, CC BY sources (Koniwa CC BY 3.0 <1 h, SIWIS CC BY 4.0 <11 h), and "synthetic audio from closed TTS providers"; excludes open-TTS and voice-clone output. A few hundred hours. espeak-ng (GPL) only an English out-of-vocabulary fallback in misaki (misaki Apache-2.0, fetched https://github.com/hexgrad/misaki). | PRIMARY (EDIT by refuter 18 Oct: Kokoro is the best-documented choice, not the only Apache-weights engine; see Dia and Parler-TTS rows). One flag: closed-TTS synthetic audio in its training data (a TTS, not an LLM, but a competitor's output; owner to rule, Q4). |
| Chatterbox (Resemble AI) | MIT (fetched https://github.com/resemble-ai/chatterbox, https://huggingface.co/ResembleAI/chatterbox) | Zero-shot voice cloning; PerTh watermark on every file; training data "about 0.5 million hours" with no sources named; Llama 3 backbone credited. | OPTIONAL second engine for speaker/accent diversity, only if owner accepts unnamed data (Q4). Needs reference clips (4.4). |
| Piper (OHF-Voice/piper1-gpl) | GPL-3.0 engine (fetched https://github.com/OHF-voice/piper1-gpl); old rhasspy/piper MIT, archived Oct 2025 (search result) | Voices are per-MODEL_CARD: lessac -> Blizzard 2013 licence link (EDIT by refuter 18 Oct: I read the licence itself, https://www.cstr.ed.ac.uk/projects/blizzard/2013/lessac_blizzard2013/license.html: 'Research Purposes' only, commercial purposes excluded, no redistribution; the earlier 'maintainer reads it as research-only' was wrong: in discussion #271 the maintainer gave no reading, a user did, and the maintainer said Piper adds no licence and the end user must judge. Note the HF repo header says 'license: mit' while the per-voice cards say otherwise); ryan -> CC BY-NC-SA 4.0 (fetched card); libritts_r -> CC BY 4.0 but "fine-tuned from lessac" (fetched card), so it inherits the doubt. | DROP. Nothing it offers beats Kokoro. |
| F5-TTS | Code MIT, weights CC-BY-NC (Emilia) (EDIT by refuter 18 Oct: now fetched, README: 'The pre-trained models are licensed under the CC-BY-NC license due to the training data Emilia' https://github.com/SWivid/F5-TTS) | NC weights. | BARRED. |
| XTTS v2, Fish Audio S2 Pro, Voxtral TTS, Breeze TTS 2 | Non-commercial/research (EDIT by refuter 18 Oct: XTTS card names the Coqui Public Model License, a custom licence outside the owner's MIT/Apache/BSD/CC list, so barred on that ground alone; coqui.ai/cpml returned 404 so the NC wording is only via Cartesia; Fish, Voxtral, Breeze rest on Cartesia alone) | Per Cartesia's comparison, published 9 Oct 2026, fetched https://www.cartesia.ai/learn/open-source-tts. Cartesia sells a competing hosted TTS, so treat as secondary. | BARRED. |
| VibeVoice | MIT, but card says research use only | Same Cartesia page. | Skip. |
| Orpheus 3B | Apache-2.0 on a Llama backbone | Same page says read Meta's Llama licence. | Skip (LLM-based, extra licence). |
| Dia 1.6B (Nari Labs) (ADDED by refuter 18 Oct) | Apache-2.0 (fetched https://huggingface.co/nari-labs/Dia-1.6B; Cartesia page also lists Apache 2.0, commercial yes) | Card has no training-data statement; forbids voice resemblance of real people without permission. | Apache weights exist but data provenance undocumented; not preferred. Shows Kokoro is NOT the only Apache-weights engine. |
| Parler-TTS large v1 (ADDED by refuter 18 Oct) | Apache-2.0 (fetched https://huggingface.co/parler-tts/parler-tts-large-v1) | Card names parler-tts/mls_eng and libritts_r_filtered (LibriTTS-R is CC BY 4.0 per OpenSLR 141 as cited above) and speaker-description sets; I did not verify who wrote the descriptions (if an LLM, it is an LLM-made annotation set, check before use). | Possible second engine for voice diversity; UNVERIFIED on description provenance. Shows "only engine with Apache weights and documented permissive data" is not established. |

### 4.3 Real-speech and noise corpora
| Corpus | Licence | Use |
|---|---|---|
| LibriSpeech | CC BY 4.0 (fetched https://www.openslr.org/12/) | Harvest ASR confusions (6.3); overlaps Nemotron training data, so errors are understated. |
| LibriTTS-R | CC BY 4.0 (fetched https://www.openslr.org/141/) | Reference clips for Chatterbox cloning (if approved). |
| Common Voice | CC0-1.0 (EDIT by refuter 18 Oct: the cited MDC announcement page states NO licence and no access terms, it only points to per-dataset datasheets on GitHub; CC0 is not confirmed by any page I read), now only through Mozilla Data Collective with an account and terms; a secondhand report says terms forbid trying to identify speakers (search results, e.g. https://community.mozilladatacollective.com/common-voice-23-0-live-on-mozilla-data-collective/) | Real accents for confusion harvesting; do not use as clone references. UNVERIFIED which terms apply today. Also in Nemotron's training set. |
| VCTK 0.92 | UNVERIFIED: Edinburgh page lists a `license_text.txt` and no licence name (fetched https://datashare.ed.ac.uk/handle/10283/3443); a York catalogue says ODC-BY 1.0, a mirror says CC BY 4.0 (search results). Also in Nemotron training set. | Do not rely on it. |
| RIRS_NOISES (OpenSLR 28) | Apache-2.0 per the OpenSLR listing (fetched https://www.openslr.org/28/ 18 Oct; the listing applies it to the whole archive, which also holds real RIRs from RWCP, REVERB 2014, AIR and point-source noises from MUSAN, and states no separate terms for them; the licence file inside the archive was not read) | Use the simulated RIRs only. The reason (third-party real RIRs may carry their own terms) is a precaution, UNVERIFIED. |
| MUSAN (OpenSLR 17) | CC BY 4.0 per the OpenSLR listing (fetched https://www.openslr.org/17/ 18 Oct; the page states one licence for the whole resource and says nothing about per-file licences; the per-file claim stays UNVERIFIED) | Background noise/babble. |
| DEMAND | Zenodo page conflicts: description "CC BY-SA 3.0", Rights field "CC BY 4.0" (fetched https://zenodo.org/records/1227121) | Prefer MUSAN. If used, treat as BY-SA; we ship only text transcripts, not the audio. |
| SLURP audio | CC BY-NC (text CC BY 4.0) (search result) | BARRED for audio. |
| Speech-MASSIVE | CC BY-NC-SA 4.0 (search result) | BARRED. |
| MInDS-14 | CC BY 4.0 (search result, HF card) | Banking intents; not useful. |
| Google Speech Commands v0.02 | CC BY 4.0 (search result) | Keywords only; not useful. |
| Fluent Speech Commands, STOP | UNVERIFIED (STOP points to a separate LICENSE.txt I could not read) | Skip. |
| ASR-GLUE | No dataset licence stated, Google Drive link (fetched https://arxiv.org/html/2108.13048) | Do not use. |
| "Programming by Voice" spoken-code lines (Nowrin and Vertanen, CUI 2023) | No download link or licence found (fetched https://www.keithv.com/pub/progvoice/) | Cannot use; ask the authors if wanted (Q6). |
| VoiceBench | Repo Apache-2.0 (fetched https://github.com/MatthewCYM/VoiceBench); data licence UNVERIFIED; most audio from Google TTS | Protocol reference only. |

### 4.4 Tools
- audiomentations: MIT (fetched https://github.com/iver56/audiomentations). Has AddBackgroundNoise, ApplyImpulseResponse, Mp3Compression, Resample, BandPassFilter, TimeStretch, PitchShift, Gain, ClippingDistortion.
- NeMo-text-processing: Apache-2.0; pip works on Linux x86_64 only, conda for others (fetched https://github.com/NVIDIA/NeMo-text-processing). Optional: written-to-spoken for dates/money/time. For code tokens we need our own table anyway.
- CMUdict "BSD" and g2p_en "Apache-2.0" per secondary listings (Wikipedia, Gentoo; search results). UNVERIFIED against the official files. Needed for the program noiser (6.2).
- espeak-ng is GPL and only a fallback inside Kokoro/misaki; GPL on a data-generation tool does not obviously cover the audio it makes, but a Piper maintainer said he did not know (discussion #271, fetched). We ship no TTS, so risk is low. UNVERIFIED legally.
- Number verbalizer: write our own (about 100 lines, program-checked); do not depend on LGPL `num2words` inside our tree (misaki links to it; not checked).

---

## 5. Published numbers (all in one place)

| Claim | Number | Tag | Source (accessed 18 Oct 2026) |
|---|---|---|---|
| Nemotron EN 0.6B avg WER (8 sets, no PnC) by chunk | 1.12 s 6.93; 0.56 s 7.07; 0.16 s 7.67; 0.08 s 8.43 | vendor-run | HF card |
| Same, per set at 1.12 s | AMI 11.73, Earnings22 12.52, Gigaspeech 9.66, LS-clean 2.32, LS-other 4.84, SPGI 2.97, TEDLIUM 3.50, VoxPopuli 7.91 | vendor-run | HF card |
| Nemotron training data | 530k h (Riva 250k, YouTube-Commons 109.5k, YODAS2 102k, LibriLight 49.5k, Mosel 14k, Granary EN; plus LibriSpeech, Fisher, Switchboard, WSJ, VCTK, VoxPopuli, MLS, Common Voice, People's Speech, AMI ...) | vendor-run | HF card |
| Nemotron needs about 320 ms trailing silence; server latency P50 19 ms (RTX 5090) | as stated | vendor-run (Daily) | Daily blog |
| Nemotron on L4, batch 1 / 8 throughput | 86.9x / 258.9x real time | vendor-run (GPU seller) | E2E Networks blog |
| NVIDIA claim: up to 560 streams on H100 at 320 ms chunk vs 180 baseline | as stated | vendor-run | HF blog (5 Jan 2026) |
| Untrained 7B tool-calling agent: text 82.3% to 71.9-74.9% with ASR (WER 6.3-8.1%) | -7.4 to -10.4 points | author-run | SpeechEvalX |
| Loss by edit role | negation 25.7, number 21.9, entity 17.1, intent cue 12.4, slot 9.5, function word 2.9, other 1.4 | author-run | SpeechEvalX |
| Voice-style rewrite loss vs typed noise | about -9.7 vs about -3.0 average; succinct -24.1; homophone -0.4 | author-run | HIVE |
| VoiceBench cascade vs end-to-end (overall) | Whisper-large-v3 + GPT-4o 87.23; GPT-4o-Audio 86.42; Whisper + Llama-3.1-8B 79.06; best open end-to-end about 55 | author-run | VoiceBench paper |
| VoiceBench content perturbations (avg drop) | mispronunciation 20.34%, repair 12.55%, interjection 9.97%, pause 9.95%, repeat 9.30%, false start 3.26%, grammar error 2.68% | author-run | VoiceBench paper |
| VoiceBench: low-resource accents (Indian, Philippine) degrade more, more so on real speech; naive pipeline most robust to noise | qualitative | author-run | VoiceBench paper |
| ASR-GLUE WER by noise level (SST-2) | 18.35 / 30.76 / 34.86% (low / medium / high) | author-run | ASR-GLUE |
| Text vs voice gap, omni models | 1.8 to 4.8 points (Confetti) | author-run | From Text to Voice |
| Spoken-code: LM adaptation cut WER 27% relative (commercial recognizer) | -27% rel. | author-run | Programming by Voice |

---

## 6. Voice data recipe (proposed)

### 6.1 Scope and pools
- Source rows: only rows already in the training mix, program- or Claude-authored gold, with a natural-language user-utterance field. No voice-only items. Human-label replay rows excluded (A46 noise screen already treats them as risky).
- Spoken field(s): the user utterance. Everything else stays text.
- Candidate pool about 10-12K voice variants; keep about 3K (v2 had 2K). Cap 2 variants per source row. Voice share at most about 8% of new rows; the clean text twin of each source row is in the mix by construction.

### 6.2 Two generators (both programmatic)
A. Real round trip (about 55% of kept rows)
1. Spoken form via our verbalizer (6.3) -> Kokoro-82M, voices graded C or better in VOICES.md (af_heart A, af_bella A-, af_nicole B-, bf_emma B-, plus C+/C: af_aoede, af_kore, af_sarah, am_fenrir, am_michael, am_puck, bf_isabella, bm_fable, bm_george, af_alloy, af_nova; fetched https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md). Skip D-and-below voices (am_adam F+). Speed 0.85-1.25. Kokoro degrades on very short (<10-20 tokens) and very long (>400) inputs: keep utterances in range or chunk.
2. Optional Chatterbox with LibriTTS-R reference clips (needs Q4 approval) for accents and speaker count.
3. Acoustic chain (audiomentations MIT): MUSAN noise at SNR 25/15/10/5 dB, simulated RIRs, 8 kHz band-limit, Opus/MP3 at low bitrate, gain/clipping, small pitch shift. Convert 24 kHz to 16 kHz mono WAV.
4. Nemotron streaming at pinned revision, chunk size mixed (160 ms 40%, 560 ms 40%, 1120 ms 20% until Q2 is answered), at least 320 ms trailing silence for the 160 ms chunk (EDIT by refuter: proven only for that chunk; measure the minimum flush padding per chunk size on a probe, it may be larger for 560/1120 ms); 5% of variants clipped at start (0-300 ms) and 3% with only 0-160 ms trailing silence (onset/offset robustness; Beyond Fresh Starts, Daily).
5. Record raw ASR text exactly as emitted (case, punctuation, number form).

B. Program confusion-table noiser (about 45% of kept rows)
1. Harvest a word-level substitution/insertion/deletion table from Nemotron itself: run it on permissively licensed real speech with references (LibriSpeech CC BY 4.0, optionally Common Voice CC0 with the MDC terms checked) and on generator A output. Align with an edit-distance aligner; key entries by phoneme sequence (CMUdict/g2p, licence check pending).
2. Replay the table on text: P(corrupt) per eligible token (EDIT by refuter 18 Oct: the 0.10-0.20 figure borrowed from ISNI is NOT a measured ASR error rate; ISNI's P(z)=0.15 / 0.21 is a prior tuned on the downstream validation sets of an ASR-agnostic generator. Nemotron's own corpus WER is 2.3-18.3%, average 6.9%, so a flat 10-20% per token would put almost every generator-B row in the 10-20% WER bands and contradicts 6.5, where only 35% of rows are at 8% or more while B is 45% of rows. Set the rate by calibration to the 6.5 band targets, and treat 0.10-0.20 as an upper bound for the hard tail only), weighted toward closed-class and phonetically close words, never on decision-bearing spans unless the span survives the gold check (6.4). (The 55/45 split between generators A and B is a design choice with no source.) Include: dropped function words, doubled words (HF discussion #18 on repeated words, title only), homophones, number-word/digit swaps, merged or split identifiers, missing punctuation/case.
3. Why it is needed: round trips alone have low diversity (Speak & Spell). Why it is allowed: no model writes the text; a table plus rules does.

### 6.3 Spoken forms (text normalisation)
- Natural-language utterances: default (about 75% of kept rows).
- Dictated commands/paths/flags (about 20%): half "literal" ("rm dash r f slash tmp slash build") and half "natural" ("remove the build folder in temp"); the Programming by Voice study found experts speak more naturally, novices more syntactically (fetched keithv.com page), so keep both. Symbol table: `/` slash, `.` dot, `-` dash, `--` dash dash, `_` underscore, `~` tilde, `#` hash/pound, `:` colon, `=` equals, `*` star; camelCase and snake_case read as words or spelled; hashes and long IDs spelled letter by letter or abbreviated ("the commit starting with a-3-f"). No published standard exists (my search found none); this is our own table, tested by round-trip.
- Numbers/IDs (about 5% dedicated + everywhere else): cardinal ("one hundred twenty three"), digit-by-digit for ports/IDs/years where natural, ordinals, versions ("three point eleven"). Because Nemotron's ITN behaviour is unknown, keep both written forms in the training transcripts: whatever the probe shows is the majority form, and about 15% use the other form.
- Disfluency style (rule-based, not LLM): fillers ("um", "uh"), repeats, false starts, self-repairs ("delete the log, no, the cache folder"), dropped politeness; VoiceBench shows mispronunciation and repairs hurt most. Replaces HIVE's Qwen-based rewriter.

### 6.4 Gold handling
1. Gold is inherited from the source row (program gold unchanged).
2. Each source row carries (or gets, by program) a list of decision-bearing spans: negations and polarity words, numbers and quantities, and the entities/paths/flags/commands the gold depends on. If a row lacks metadata, fall back to: negation lexicon + all digits/number-words + tokens matching path/flag/identifier regex.
3. After ASR, align spoken reference vs hypothesis. If any decision-bearing span is deleted or altered beyond number-form equivalence, the variant is "altered": drop from training (consistent with the drop-only A46 posture), but log it. Reason: training on a transcript whose negation vanished with the original "deny" gold teaches the model to invent evidence. Roughly the SpeechEvalX high-loss roles.
4. Keep variants where only non-decision words changed, or the span is recoverable from context. These are what the model must learn to ignore.
5. Report per run: kept %, altered % by role, mean/median WER per band, voices, chunk sizes, noise mix. The altered rows form a dev-only stress set (they come from training-pool sources, so they are not eval sets).
6. No "ask" label is invented for altered rows; that would need a plan decision about the ask band.

### 6.5 WER bands (measured per row on the spoken field, whisper-normalizer style)
| Band | Share of kept rows | Rationale |
|---|---|---|
| < 3% | 30% | Clean near-field; baseline for pairing |
| 3-8% | 35% | Typical laptop mic plus accent; matches published conversational WER 7-10% |
| 8-15% | 25% | v2's upper band; real far-field/meeting-like (AMI 11.7-18.3%) |
| 15-25% | 10% | Hard tail; gold survival is low, so most altered rows land here |
| > 25% | 0% | Unrecoverable; excluded |
Short utterances make per-row WER coarse (one error in ten words is 10%): fill bands by corpus-level condition schedule, then verify with per-row measured WER. Run a 500-row pilot first to map (SNR, RIR, speed, codec) to WER, because TTS speech is easier than real speech.

### 6.6 Pilot A/B (cheap, on L4)
- Source tag ("[transcribed speech]") vs no tag in the prompt for voice rows. I found no study that tests this (UNVERIFIED benefit); one Mandarin result says prompt-only handling did not beat plain ASR output (search result). Test, do not assume.
- Whether to add a rule-based code-symbol ITN (spoken "dash dash force" to `--force`) in the product before the model, vs training on raw spoken form. Compare on the dictated-command stratum.

---

## 7. Real-speech eval plan (decisive evidence)

Why: TTS-based speech overstates robustness (VoiceBench real vs TTS), Nemotron trained on Common Voice, LibriSpeech, VCTK, AMI so public-corpus WER is optimistic, and no public real-speech benchmark exists for coding-agent decisions (VoiceAgentBench and BFCL-audio are TTS; searches found no human-spoken coding-agent set).

Three tiers (report only V2 for claims):
- V0 regression: paired text vs clean-TTS-ASR, every training run, cheap.
- V1 stress: TTS plus acoustic chain at fixed SNR/RIR grid (like From Text to Voice, SNR clean to 5 dB).
- V2 real: human recordings.

V2 design
1. Items: new Claude-authored scenario cards, program gold wherever possible, authored after the training data freeze and stored apart from all training pipelines; or, if the orchestrator can lawfully do it, spoken readings of held-out text items. I did not and must not read the sealed eval sets, so the choice of items is for the orchestrator.
2. Speakers: at least 12, spread over US, UK, Indian English, and at least two other L2 accents (VoiceBench: Indian and Philippine English degrade most); at least 2 devices (laptop mic, phone/earbuds); at least 2 rooms (quiet, office or cafe).
3. Two modes: read-aloud of exact text (clean WER, pairs perfectly) and "say it in your own words from the scenario" (ecological; a second person checks the transcript still matches the scenario's gold, else discard).
4. Dictated-command stratum: 20% of items include a command, path or flag spoken aloud, in each speaker's own style.
5. Size: target at least 500 paired items (text twin of each). My calculation: if about 6% of pairs disagree between text and speech, 80% power at alpha 0.05 to detect a 3-point accuracy gap needs about 520 pairs (McNemar); 1,000 pairs resolve about 2 points. Use a cluster bootstrap over speakers and items.
6. Consent and licence: written consent that allows research use; release as CC0/CC-BY only with explicit permission. Do not clone volunteer voices without separate consent.
7. Metrics, all paired text vs speech with the same model and prompt:
   - Flip rate (decision differs) with CI; accuracy gap with McNemar.
   - Harmful flips: allow where gold says deny (safety side) reported separately from over-block flips.
   - Calibration under speech: ECE and Brier text vs speech (C1 had ECE 3.3 on the text side-bench per memory; speech ECE should not blow up).
   - Flip rate by measured WER band and by error role (negation / number / entity / intent / other), using SpeechEvalX role rules.
   - Altered-span rate: how often ASR itself changed a decision-bearing span (not the model's fault; reported to attribute failures).
   - Operating-point stability: the three strict/balanced/permissive points keep their FPR/FNR targets under speech (v2 lists the points but not speech).
8. Pre-registered thresholds (my proposal, to be ruled): no more than 3 points accuracy loss at the 3-8% band, no more than 6 at 8-15%, harmful-flip rate not above 1.5x the text-side FPR, ECE within 2 points of text. Reference for what is plausible: untrained 7-8B agents lost 7-10 points at 6-8% WER (SpeechEvalX), so a 3-point target is ambitious but checkable.
9. Supplements (not training): VoiceBench CommonEval (200 human clips, from Common Voice) and SD-QA (553 clips, 11 accents) can calibrate ASR WER per accent for the chosen ASR; licence of the data UNVERIFIED, so keep out of the repository.

---

## 8. Concrete plan changes (summary; the defended ones are in the structured result)

1. Replace the one-line "ASR-noised copies, TTS then ASR, 3-15% WER" with sections 6.1-6.5.
2. Pin Nemotron revision and chunk size; pad at least 320 ms silence (160 ms chunk; measure for larger chunks); probe number form first.
3. Kokoro (Apache-2.0) as the TTS; drop Piper; F5/XTTS/Fish barred; Chatterbox only on owner ruling.
4. Gold: inherit unless a decision-bearing span changed; drop altered rows; log them.
5. Add the program confusion-table noiser harvested from the locked ASR.
6. Add V2 real-speech eval with paired metrics; make speech a gate in the C2.1 report, not an attachment.
7. Keep voice share at most about 8% of new rows and always paired with the clean text twin (HIVE shows LoRA robustness training can cost clean accuracy).

---

## 9. Open questions

Q1. Which input fields are spoken in the product (user utterance only, or also the confirm/deny answers)? I assumed utterance only. If confirm/deny short answers ("yes", "no", "stop", "don't") are spoken, short-utterance behaviour needs its own stratum and Kokoro's weakness on <10-token inputs matters.
Q2. Production chunk size and end-of-input policy (160 ms with 200 ms plus synthetic silence is Daily's recipe; ours is "explicit end of input").
Q3. Does Nemotron EN 0.6B (Mar 2026 checkpoint) emit digits or words? Probe pending; model card is silent.
Q4. Owner ruling on TTS provenance: Kokoro's closed-TTS synthetic audio; Chatterbox's unnamed 0.5M-hour data and Llama-3 backbone; and the LLM-labelled punctuation in Nemotron's own training data (rule 27 spirit).
Q5. Is the voice eval allowed to reuse held-out text items, or must it be a fresh set? Needs the orchestrator, since sealed sets are off limits to me.
Q6. Ask Nowrin and Vertanen for the spoken-code dataset licence (no release found); would give real programmer speech to calibrate the dictated-command stratum.
Q7. Which decision families have a natural user utterance at all? Code-only families get no voice variants.
Q8. Does the tag/no-tag and code-ITN pilot (6.6) fit the usage budget? It is small, L4 only.
Q9. UNVERIFIED items to close before data build: CMUdict and g2p_en official licences, AMI/Earnings-22/VCTK licences, MDC terms text for Common Voice, DEMAND true licence, Kokoro speed on L4.


---

## Verification (refuter)

Refuter pass, 18 Oct 2026. Method: re-fetched each cited primary page (cards, licence files, papers) and tried to refute. The web-search budget ran out during the pass, so only direct page fetches were used. Edits to this file are marked "EDIT by refuter". Tags: vendor-run / author-run / independent as above. Not legal advice.

### A. Proposed plan changes

| # | Change | Verdict | Why (one line) |
|---|---|---|---|
| 1 | Pin Nemotron EN 0.6B revision (13 Mar 2026 main, not Jan 2026 branch) and chunk size; pad 320 ms; 100-utterance probe; train on both digit and word forms, minority ~15% | KEPT with edit | Card dates, branch, four chunk sizes and avg WER 6.93/7.07/7.67/8.43 verified (https://huggingface.co/nvidia/nemotron-speech-streaming-en-0.6b, vendor-run); Daily's 320 ms is verified but only for its 160 ms chunk (formula has right_context), so "at least 320 ms" must be measured per chunk size; the card does not state digit vs word output, so the probe stands; the 15% minority share is a design choice with no source. Banner says release 12 Mar, card date 13 Mar: a one-day label mismatch, harmless. |
| 2 | Kokoro-82M default TTS; drop Piper; F5/XTTS/Fish barred; Chatterbox only on owner OK; owner line on Kokoro's closed-TTS audio | KEPT, wording "only engine" REFUTED | Kokoro Apache-2.0 code and weights, the closed-TTS synthetic audio bullet, and voice grades (all 16 listed grades match VOICES.md) verified; Piper engine GPL-3.0 (COPYING read), ryan CC BY-NC-SA 4.0, libritts_r fine-tuned from lessac, Blizzard 2013 licence is research-only (all read at source); F5 weights CC-BY-NC (README quote). But "Kokoro is the only engine with Apache weights and a documented permissive data policy" is not supported: Dia is Apache-2.0 and Parler-TTS is Apache-2.0 with named datasets. Keep Kokoro as default because it is the best documented, not because it is unique. Chatterbox MIT, 0.5M hours with no named sources, Llama backbone, PerTh watermark verified. XTTS/Fish/Voxtral/Breeze NC claims rest on Cartesia (a competing vendor) except XTTS, which is a custom licence and outside the owner's list anyway. |
| 3 | Spoken-field rule: only the user utterance goes through TTS/ASR; dictated commands are a ~20% separate stratum with own symbol table, literal and natural styles | KEPT | Evidence verified: code identifiers split ("getUserInfo" to "get use run foe"/"get your info", "async" to "a sink", "realloc()" to "real lock open close parentheses"; Recall@5 92% to 87%, arXiv 2601.15339, author-run, Indian-language speakers, Edge TTS); experts speak more naturally, novices more syntactically (keithv.com, author-run). The 20% share and the symbol table are our design (no source); English-speaker evidence for code dictation is thin. |
| 4 | Gold handling: inherit program gold only if decision-bearing spans survive; else drop and log to a dev-only stress set | KEPT | SpeechEvalX role table verified exactly (negation 25.7, number 21.9, entity 17.1, intent cue 12.4, slot 9.5, function word 2.9, other 1.4; https://arxiv.org/html/2610.17619, 13 Oct 2026, author-run). Caveats: single synthetic edits on 210 sources, untrained Qwen2.5-7B agent, TTS audio, ASRs other than Nemotron. The claim that a lost "not" with "deny" gold teaches evidence hallucination is the author's reasoning, not a measured result. arXiv 2409.06263 does not support this change (it is about dialogue state tracking). |
| 5 | Second program-only generator: confusion table harvested from locked Nemotron on LibriSpeech (+ optional Common Voice) and TTS round trips, phoneme-aware text noise, ~45% of voice rows, no LLM | KEPT with edits | Speak & Spell numbers verified (JGA 29.88 baseline, 29.94 TTS-ASR, 32.39 GPT-3.5; entity change 38.84% vs 95.47%; unique words 1.01x vs 1.81x; Whisper-base + Tacotron2; arXiv 2409.06263, author-run); TTS-ASR is non-significant in all four environments, which strengthens "weak alone". ISNI transfer failure verified for the neural NoisyGen (trained on DeepSpeech, tested on LF-MMI TDNN; arXiv 2410.15609, author-run), but ISNI is itself ASR-agnostic and beat the in-domain model in some settings, so "favours harvesting from our own ASR" is an inference with no direct test. The "0.10-0.20 per token" rate is not evidence-based and conflicts with the WER bands (see edit in 6.2). LibriSpeech CC BY 4.0 verified (https://www.openslr.org/12/). The 45% share is a design choice. Common Voice CC0 and MDC terms: UNVERIFIED. |
| 6 | Replace 3-15% WER with measured bands (30/35/25/10, >25% excluded); fill by condition schedule (MUSAN 25 to 5 dB, OpenSLR 28 RIRs, band limit, codec, speed 0.85-1.25), 500-row pilot, 5% onset-clipped, 3% short-silence | KEPT with edit | Card numbers verified incl. AMI 18.29/14.71/11.88/11.73 and Earnings22 13.16-12.52 by chunk, LS-clean 2.32 (vendor-run); VoiceBench real vs TTS gap verified but large only for VITA, small for the cascade (author-run); onset WER 15-21% relative reduction from stateful carry-over verified from the abstract (arXiv 2608.22101, 22 Aug 2026), but it was shown on two unnamed streaming models, so it is not proven for Nemotron. Band shares, SNR grid, clip/silence shares are design choices with no source. OpenSLR 28 Apache-2.0 is the listing's label for the whole archive; use simulated RIRs only (precaution, third-party terms UNVERIFIED). MUSAN CC BY 4.0 per OpenSLR 17 (single licence stated). Kokoro short (<10-20 tokens) and long (>400) weakness verified in VOICES.md; speed 0.85-1.25 untested. |
| 7 | Human-recorded paired text-vs-speech eval (V2) as a reported gate: >=500 pairs, >=12 speakers, accents, devices, rooms, read-aloud + own words, 20% dictated commands; flip rate, McNemar gap, harmful flips... | KEPT as design, numbers UNVERIFIED | No source supports the sizes; they are our calculation. I recomputed the McNemar normal approximation: with 6% discordant pairs, a 3-point gap needs about 520 pairs for 80% power at alpha 0.05, and 1,000 pairs resolve about 2.2 points; matches the text. But the 6% discordance is an assumption, and if several speakers read the same item the effective sample is smaller than 500 (needs the cluster bootstrap or a design-effect factor). Pre-registered thresholds (3/6 points, 1.5x FPR, ECE within 2) are proposals. The task text for this change was cut off after "harmful (allow-vs"; I verified only the visible part. |

### B. Licence and published-number checks that other changes rely on

- KEPT (verified at source): Kokoro Apache-2.0 (card metadata and README); Kokoro training-data bullets incl. "Synthetic audio generated by closed TTS models from large providers" and "No synthetic audio from open TTS models or custom voice clones"; Koniwa <1 h CC BY 3.0, SIWIS <11 h CC BY 4.0; "a few hundred hours" (vendor-run); Nemotron licence name NVIDIA Open Model License and "ready for commercial/non-commercial use"; NVIDIA licence: "Models are commercially usable", "NVIDIA claims no ownership rights in outputs", no general ban on training with outputs (the output-training clause applies to Cosmos models only), redistribution needs a copy of the agreement plus a Notice file (https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/); Nemotron 3.5 ASR: 06/04/2026, OpenMDW-1.1, 40 locales, "we would recommend Nemotron ASR Streaming (English) model for English-only", punctuation labels from Qwen3-32B; Nemotron training-label claim of Qwen-2.5-7B-Instruct punctuation pseudo-labels is a reply in the HF blog comments, not in the card (vendor-run, informal); Daily P50 ASR 19 ms (RTX 5090) / 27 ms (DGX Spark) (vendor-run); E2E L4 86.9x / 258.9x real time, WER 10.30%, 100 LibriSpeech clips, 27 Mar 2026, seller of GPUs (vendor-run); From Text to Voice 1.8 to 4.8 point gap, DEMAND noise to 5 dB, no licence stated (20 May 2026, author-run); HIVE numbers (see edit: ratios, not points); VoiceBench perturbation table and the Whisper+GPT-4o 87.23 / GPT-4o-Audio 86.42 / Whisper+Llama-3.1-8B 79.06 numbers (author-run).
- CORRECTED in place: HIVE metric and task description; Daily 320 ms scope; Piper/Blizzard reading (licence itself is research-only; the maintainer gave no reading); F5-TTS now primary-sourced; MUSAN per-file claim; OpenSLR 28 scope; Common Voice CC0 not confirmed by the cited page; ISNI rate mislabelled as evidence.
- REFUTED: "Kokoro is the only engine with Apache weights and a documented permissive data policy" (Dia and Parler-TTS are Apache-2.0; Parler names MLS and LibriTTS-R). "Maintainer thread reads Blizzard as research-only" (a user said it; the licence text itself does say research only).
- UNVERIFIED: Voxtral/Breeze/Fish licences (Cartesia only); XTTS NC wording (coqui.ai/cpml 404; custom licence is enough to bar it); Common Voice CC0 and MDC terms; DEMAND true licence (Zenodo page conflicts: description CC BY-SA 3.0, Rights field CC BY 4.0, re-confirmed); VCTK/AMI/Earnings-22 licences; CMUdict/g2p_en licences; espeak-ng GPL effect on generated audio; Kokoro speed on L4; whether Parler-TTS speaker descriptions were written by an LLM; whether Nemotron EN emits digits or words; flush padding for 560/1120 ms chunks; real RIR terms inside RIRS_NOISES.

### C. Net effect on the plan

Nothing proposed has to be dropped. Four edits to carry into plan v3: (1) do not write "320 ms" as a constant, make it a per-chunk-size probe result; (2) set generator-B noise rate by calibration to the band table, not 0.10-0.20; (3) call Kokoro the best-documented permissive TTS, not the only one, and consider Parler-TTS as a diversity candidate after a provenance check; (4) in the V2 sizing, state the discordance assumption and use item-level clustering.
