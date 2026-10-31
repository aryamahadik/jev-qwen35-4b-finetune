# H100 speed test, 4B-E (30 Sep 2026, Modal arya-mahadik-ai, September credit)

**Setup:** extra/modal_speed_v154.py on the 231 public JevBench items, using the official harness with CUDA graphs.
Raw files are in extra/speed_v154/.

| Readout | p50 raw (speed items) | p95 raw | JevBench speed axis | Cost axis | Tokens per decision |
|---|---|---|---|---|---|
| 1 read (harness, graphs) | **16.6 ms** | 16.9 ms | **94.7** | 58.3 | 818 |
| 1 read (inline loop) | 16.0 ms | 16.3 ms | 94.8 | 58.3 | 818 |
| 2-view, one after the other | 31.6 ms | 32.1 ms | 93.4 | **49.3** (< 50: gate penalty) | 1,636 |
| 2-view, as one batch of 2 | 56.5 ms | 59.3 ms | 91.5 | 49.3 | 1,636 |

**For reference:**
- Jev scores 83.8 on the speed axis (616 ms on the board).
- The best 4B on the board, JevK5, scores 93.6 (16 ms, H100).
- Our L4 run with no graphs scored 88.6 (110 ms).

**Findings:**
- On an H100 with graphs, our 4B is in the fastest tier on the board: 94.7 vs Jev's 83.8.
- The graphs self-check matched exactly (max prob diff 0.0), and the model peaked at 9.5 GB of GPU memory.
- 2-view read twice doubles the tokens counted, so JevBench's cost axis drops below the 50 gate. Use 1 read on
  JevBench. Keep 2-view as an option for OHS-3 consistency.
- On public items the 2-view read gave I_open 60.8 vs 62.1 for 1 read (raw readout). This is noise-level.
- The batch-of-2 graph capture ran out of memory: 68 GB of graph pools on top of the 1-view graphs. Two views run one
  after the other are faster anyway.
