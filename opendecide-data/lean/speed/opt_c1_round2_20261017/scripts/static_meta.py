"""Static metadata for the report: dataset/model revisions and licences (verified from the sources named in each entry on 17 Oct 2026)."""
META = {
 "datasets": {
  "librispeech_test_clean_other": {"source": "hf-audio/open-asr-leaderboard (config librispeech, parquet)", "revision": "de79e57adf9983993bcc72586d7313460825f5eb",
      "licence": "CC BY 4.0 (LibriSpeech, OpenSLR 12); the HF card carries no licence field", "n_split": {"test.clean": 2620, "test.other": 2939}},
  "ami_ihm_test": {"source": "hf-audio/open-asr-leaderboard (config ami, parquet; ESB/Open-ASR segmentation of AMI IHM test)", "revision": "de79e57adf9983993bcc72586d7313460825f5eb",
      "licence": "CC BY 4.0 (AMI corpus); the HF card carries no licence field", "n_split": 12643, "n_eligible_after_empty_norm_ref_filter": 11653},
  "earnings22_test": {"source": "hf-audio/open-asr-leaderboard (config earnings22, parquet)", "revision": "de79e57adf9983993bcc72586d7313460825f5eb",
      "licence": "CC BY-SA 4.0 per the upstream Earnings-22 release (revdotcom/speech-datasets); the HF card carries no licence field (not re-verified here)", "n_split": 2741, "n_eligible_after_filter": 2737},
  "tedlium3_test": {"source": "sanchit-gandhi/tedlium-data (split test; TED-LIUM release 3). The Open-ASR-leaderboard repo no longer ships a tedlium folder on main, so this public copy is used", "revision": "8083dbe64f82e17b6be070a02b9239e9b847b6ce",
      "licence": "CC BY-NC-ND 3.0 (TED-LIUM; confirmed on the distil-whisper/tedlium card); the HF card of the copy has no licence field",
      "n_split": 1469, "n_eligible": 1155, "note": "314 'ignore_time_segment_in_scoring' gap rows removed (-> 1155, the Open-ASR/ESB test size); '<unk>' removed and \" '\" re-attached in the reference following the ESB convention (from memory, not diffed against that script)"},
  "slurp_test": {"source": "marcel-gohsen/slurp (audio + transcripts, split test, 13078 recordings) joined by slurp_id to the official metadata pswietojanski/slurp dataset/slurp/test.jsonl", "revision": "HF 6ee060bbac668abfd2f32d8fefb980d1699c32b5; GitHub 8eb16545762b",
      "licence": "text/annotations CC BY 4.0; AUDIO CC BY-NC 4.0 (official LICENSE.txt). The task brief says CC BY 4.0: that holds for the text only; the recordings are non-commercial. Used here only for evaluation, nothing redistributed.",
      "note": "gold intent = official scenario + '_' + action (60 distinct values over train/dev/test, 18 scenarios); the HF 'intent' column is a legacy field with 18 extra non-official values and was not used"},
 },
 "models": {
  "nemotron_asr": {"repo": "nvidia/nemotron-speech-streaming-en-0.6b", "revision": "ebe59e5a817142986528bbbee5dba8db7b38ed50", "licence": "NVIDIA Open Model License (commercial use permitted)", "runtime": "transformers 5.17.0 NemotronAsrStreamingForRNNT, torch 2.14.0 CPU"},
  "parakeet_eou": {"repo": "nvidia/parakeet_realtime_eou_120m-v1", "revision": "a7e2b4629593dce0ec19f600e00e9904353fda2d", "licence": "NVIDIA Open Model License",
      "runtime": ".nemo converted by us to the HF NemotronAsrStreaming layout with transformers' own converter functions (same cache-aware FastConformer-RNNT family; att_context [70,1]); first <EOU> (id 1024) in the greedy output"},
  "smart_turn": {"repo": "pipecat-ai/smart-turn-v3 (smart-turn-v3.2-cpu.onnx, 8 MB int8)", "revision": "f766f81d3cfdf7737ac64aad813d91bbfd56bf93", "licence": "BSD-2-Clause", "code": "pipecat-ai/smart-turn 4786657e242d (inference.py recipe: Whisper feature extractor, 8 s window, p>0.5 = complete)"},
  "silero_vad": {"repo": "silero-vad 6.2.3 wheel (silero_vad.onnx, 32 ms windows)", "licence": "MIT (upstream snakers4/silero-vad; the wheel metadata has no licence field)"},
  "wav2vec2_aligner": {"repo": "facebook/wav2vec2-base-960h", "revision": "22aad52d435eb6dbaf354bdad9b0da84ce7d6156", "licence": "Apache-2.0", "use": "CTC forced alignment of the gold transcript -> reference speech end (20 ms resolution)"},
  "c1": {"base": "Qwen/Qwen3.5-4B @ 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a", "adapter": "q35_4b_main500k sha256 507d1c29690579f9...", "load": "decoder_io.load + merge_and_unload, BF16, layout schema_branch_mark, style cygnet, no PRISM-X; readout A5 = predict(tta_choice=True)"},
 },
 "normaliser": "whisper-normalizer 0.1.12 EnglishTextNormalizer (the version named on the Nemotron model card); corpus-level WER (sum of word errors / sum of reference words), 95% interval = bootstrap over utterances (2000 resamples)",
}
