# STRIPPED EXCERPT: research_v3/voice.md sections 6-7 (voice data recipe and real-speech eval plan)
Stripped for clean-room lanes (18 Oct 2026). Design content copied; quoted benchmark strings, item text, example IDs and ID patterns replaced with [removed]. Paper, model-card and dataset URLs kept. Removals in this file: 0.

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
