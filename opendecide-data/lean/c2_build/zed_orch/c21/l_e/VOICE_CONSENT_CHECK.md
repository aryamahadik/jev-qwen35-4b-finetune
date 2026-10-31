# VOICE_CONSENT_CHECK: does the VOICE_REAL.md record cover eval-only reuse of the real-speech set?

Source read: `/Users/aryamahadik/Documents/jev/opendecide-data/lean/speed/opt_c1_round2_20261017/VOICE_REAL.md` (17 Oct 2026). No audio or transcripts were opened or quoted.

## Verdict

**Partly covered.** The record covers eval-only use of the SLURP real-speech audio as a stated use and licence fact. It contains no speaker-consent record at all, and it does not assess whether internal evaluation at a commercial company falls within the CC BY-NC 4.0 licence.

## Relevant lines

Section 5 (line 157):

> "SLURP: audio licence is CC BY-NC 4.0 (the brief says CC BY 4.0, which is true for the text only); used for evaluation only. ..."

Section 6, slurp_test (line 170):

> "licence: text/annotations CC BY 4.0; AUDIO CC BY-NC 4.0 (official LICENSE.txt). The task brief says CC BY 4.0: that holds for the text only; the recordings are non-commercial. Used here only for evaluation, nothing redistributed."

Line 162 (housekeeping) confirms that results files hold per-utterance text and timings, with no audio.

## What the record covers

- **Eval-only use:** stated twice (lines 157 and 170): "used for evaluation only" and "Used here only for evaluation, nothing redistributed."
- **Licence identified from the official LICENSE.txt:** CC BY-NC 4.0 for the audio. The text-vs-audio licence split is flagged, so the brief's error is not carried forward.
- **No redistribution:** stated. Outputs are per-utterance hypotheses, timings and decisions with no audio.

## Gaps

1. **No speaker or recording consent record.** The file has no statement on how the SLURP recordings were collected, whether speakers consented, or what the dataset's own consent terms are. The only permission basis is the CC BY-NC 4.0 licence.
2. **Commercial-use question not assessed.** NC means non-commercial. The record says "for evaluation only" but does not say whether an internal benchmark run at a commercial company counts as non-commercial use. This needs an owner or legal ruling before the SLURP-based numbers (89.2% agreement, line 75) are used in any external or commercial document.
3. **Derived numbers.** The record does not say whether the SLURP-derived agreement and accuracy figures may be published. Only raw audio redistribution is ruled out.
4. **Other real-speech sets (for completeness):** AMI (CC BY 4.0), LibriSpeech (CC BY 4.0), Earnings-22 (CC BY-SA 4.0, "not re-verified", line 168) and TED-LIUM (CC BY-NC-ND 3.0, line 169) are listed with licences. TED-LIUM is NC-ND, which carries the same commercial-use question as SLURP. The file does not say whether it is eval-only, but it is used only for WER measurement.

## Suggested status for the L-E gate

- Eval-only reuse of SLURP audio inside this project: **covered by the record's own statement**, pending the owner's confirmation that internal evaluation is acceptable under CC BY-NC 4.0.
- Any external, commercial or published use of SLURP-derived numbers: **not covered**. Needs an owner decision.
- Speaker consent: **no record**. Relies entirely on the dataset licence.
