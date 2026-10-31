"""oc1: C1 serving-optimisation tests (17 Oct 2026). See modal_app.py for the entry points and run_plan.json for the plan.

  common     constants, payer guard (jaypatil-duke only), path guard, USD 5.00 budget governor
  configs    the SGLang server configs (S1 + one change each), the online-quantization ignore lists
  items      workload rows -> rendered, tokenized decisions with fastcore.readout (= decoder_io byte for byte)
  backend    two readouts of the same pre-tokenized ids: S1's /generate and SGLang's /v1/score
  measure    parity pass, batch-1 / batch-8 latency, saturation throughput, prefix-cache hit rate, GPU sampler
  parity     the 99.5% bar, near-tie analysis of the flips, stratified subsamples
  session    in-container orchestrator: boot -> measure -> extras -> stop, gated by the running spend
  runner     the measurement process (prep / measure / front / voice_c1 / vision)
  front      end-to-end HTTP front with a capped batching wait, admission control, per-stage timing
  loadgen    laptop-side Poisson load client with httpx stage traces + the same-client Jev sample
  vision     image-token caps on 200 vision-bench items          voice   Kokoro TTS -> Nemotron ASR -> C1
  smooth     SmoothQuant as a BF16 -> BF16 transform             pypatch  opt-in online FP8 / INT8 with an ignore list
  costmodel  USD per 1K decisions from measured throughput        plan     the run plan and its estimate
  report     post-processing of a session folder (laptop)
"""
