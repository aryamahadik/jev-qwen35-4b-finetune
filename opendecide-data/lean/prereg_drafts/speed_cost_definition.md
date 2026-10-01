# Speed and cost for OHS-3: proposed definitions (draft for the owner, 1 Oct 2026)

**Status.** `PREREG_OHS3.md` defines no speed and no cost endpoint. The final goal still says to beat Jev on speed and
on cost. If these definitions are adopted (as written or edited), commit them as a PREREG_OHS3 amendment **before the
first OHS-3 run**. Choose them without any OHS-3 data. Nothing here has been run.

**One constraint shapes everything.** PREREG rule 4 says OpenDecide runs **exactly once per model** on OHS-3, in its
serving configuration. So the timing must come from that one scored run. A second OHS-3 pass only for timing would
break rule 4. Anything measured outside the scored run (for example a throughput test) uses dev inputs, not OHS-3.

OHS-3 has 2,456 calls, one row per call, so one call = one decision.

## Speed

**S1, primary: end-to-end latency per call, p50.**
- **Clock.** The client's `time.perf_counter`. It starts just before the HTTP request is sent and stops when the full
  response has been received and parsed. Network, TLS, provider queueing and retries are all included.
- **Retries.** A retried call is timed from the first attempt's start to the successful attempt's end. A call that
  fails after all retries is recorded at the timeout (proposed: 30 s), so failures count in the percentiles. Failed
  calls are also reported separately.
- **Client.** Both systems are timed from the same client machine and network, in the same time window, with the same
  request format: one state plus its question(s), the format `serve_od.py` and the Jev SDK both use.
- **Concurrency 1.** Calls are sent one at a time. OpenDecide and Jev run 1 (`jev_guard`) are **interleaved** call by
  call, in a seeded order, so both see the same network conditions. Jev run 2 is timed the same way; its latency is
  reported only as Jev's run-to-run noise.
- **Warm-up.** Before timing, send 20 warm-up calls to each system using **dev** inputs. Cold start (the time to
  first answer after scale-from-zero) is reported separately and is not in S1.
- **Test.** Jev minus OpenDecide p50, so a positive difference means OpenDecide is faster. Use a paired bootstrap over
  calls, stratified by task: 10,000 resamples, `default_rng(0)`, 95% percentile interval.
- **"Faster than Jev"** means the CI of the p50 difference is entirely above 0, **and** the p95 point estimate is
  also lower.

**S2, secondary: p95, same procedure.** Reported descriptively: p99, server compute time (`server_ms`), TCP connect
and TLS time to each host (the network floor), and the client location and server regions of both systems.

**What the claim names.** The timed OpenDecide configuration must be the one that produced the scored predictions:
- checkpoint sha256, precision and layout;
- GPU type and region;
- CUDA graphs on or off;
- endpoint type: a direct tunnel (`modal.forward`) or the Modal web endpoint.

The claim must also say whether that endpoint is something a customer could actually use. If the headline system is
the 2B to 4B cascade, time the cascade end to end, routing included.

**Why this matters (measured before; see `projection/evidence.md` section 9):**

| System and path | Client p50 | Client p95 |
|---|---|---|
| Jev via OpenRouter, from the laptop | 187-205 ms | 266-539 ms |
| v10 on an H100 with CUDA graphs, direct tunnel | 114.6 ms | 124.1 ms |
| The same model through the Modal web endpoint | 410 ms | 517 ms |

So the endpoint type decides the speed result. Layout E end to end has **never** been measured.

**Tooling gap (not built in this job).** `run_jev.py` times only the successful attempt, and it runs 8 calls at a
time. A new harness is needed: interleaved, concurrency 1, recording first-attempt start, retries, `server_ms`, usage
tokens and model id. Do not edit `run_jev.py` itself; it produced the OHS-1 and OHS-2 records. Once S1 and S2 are
approved, they can be added to `score_ohs3.py`.

## Cost

**C1, primary: dollars per 1,000 decisions under sustained load.**
- **OpenDecide.** The all-in hourly price of the serving machine, from billing (GPU + CPU + RAM; the measured H100
  rate was $4.09/h all-in). Divide by the sustained decisions per hour at the serving batch policy. Measure that rate
  with a load test on dev inputs whose token-length distribution matches the OHS-3 run's logged input lengths.
- **Utilisation.** Report the figure at 100% and at 40% utilisation (40% multiplies the cost by 2.5).
- **Jev.** List price times the input tokens measured in the OHS-3 run, from the API usage field ($0.042 per million
  input tokens; output is free). Also report the billed amount for that run when the billing can isolate it. The only
  billed figure so far is $0.032 per 1,000 calls (OHS-1, 3,694 calls, $0.12).
- **"Cheaper than Jev"** means OpenDecide's C1 at **40%** utilisation is below Jev's C1. This is the conservative
  choice. The owner may choose 100% instead, but must decide before the run. No CI: both figures are rates, not
  samples.

**C2, secondary: as-run cost of the one OHS-3 run.**
- OpenDecide: the billed cost from the first to the last scored call, divided by 2,456, times 1,000. Idle time between
  calls counts. Image build and model download do not.
- Jev: the billed or list-price cost of `jev_guard`, computed the same way.

**C3, secondary: the JevBench v1.5.4 formula.** Pooled tokens times list price. Ours is priced at the frozen
Qwen3.5-4B reference (DeepInfra: $0.03 per million input tokens, $0.15 per million output). Reference values: 4B-E
$0.0245 per 1,000, Jev $0.0384 per 1,000 (`scores_v154_all.json`).

**Caveats to state with any cost claim:**
- C1 ignores the operating cost of self-hosting.
- Layout E prompts are longer than text_first prompts (about 627 vs 265 characters on 2,000 dev rows), which raises
  token-based cost.
- A cascade's cost is the 2B's cost plus the routed fraction times the 4B's cost. The 2B/4B inference cost ratio has
  never been measured; the one measurement says the 2B is 1.16 times **slower**.

## Decisions needed from the owner

1. **S1 rule.** Accept "p50 CI above 0 and p95 lower", or choose another.
2. **Endpoint type** for the scored run: direct tunnel or web endpoint. It must also be named in the model amendment.
3. **Interleaving.** Run OpenDecide's single OHS-3 run interleaved with Jev run 1 at concurrency 1. This changes how
   the Jev run is executed compared with OHS-2, which used concurrency 8.
4. **C1 utilisation** for the "cheaper" claim: 40% (proposed) or 100%.
5. **Who builds and tests the timing harness**, on CPU and dev inputs, before the run.
