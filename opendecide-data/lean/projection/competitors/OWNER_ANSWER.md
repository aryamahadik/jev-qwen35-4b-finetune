# Cygnet, Winnow and Jev: how we compare (30 Sep 2026)

I think "Sonnet and Vino" means **Cygnet (#1)** and **Winnow-12B (#2)** on the JevBench v1.5.4 board. The live board today matches our saved copy.

## 1. The leaders and us

| System | Size | Open weights | Score A | Accuracy (I) | Calibration | Speed | Cost |
|---|---|---|---|---|---|---|---|
| Cygnet (#1) | 12B (Gemma-4, not trained) | Yes | 73.70 | 71.1 | 87.0 | 91.0 | 56.4 |
| Winnow-12B (#2) | 12B (Gemma-4, LoRA) | Yes | 73.23 | **74.4** | 84.1 | 86.1 | 56.6 |
| Jev 1.13 (#3) | Unknown | No (API only) | 72.13 | 72.0 | 88.0 | 83.8 | 54.7 |
| JevK5 v0.3 (#4) | 4B (Qwen3.5) | Yes | 71.90 | 56.3 | 88.3 | 93.6 | 63.1 |
| decider-4b v2 (#7) | 4B (Qwen3.5) | Yes | 71.28 | 55.8 | 85.6 | 90.9 | 64.5 |
| **Our 4B-E, as trained*** | 4B (Qwen3.5) | Yes | 71.03 | 62.5 | 84.3 | 88.6 | 58.3 |
| **Our 4B-E, firm yes/no*** | 4B (Qwen3.5) | Yes | 75.27 | 78.7 | 83.4 | 88.6 | 58.3 |
| Jev on the same items* | | | 68.80 | 63.2 | 81.2 | 91.4 | 52.5 |

\*Our unofficial run on the 231 public items, not board scores. We built the model with these items, so they flatter us.

We got 204 of the 231 right, Cygnet 203, Jev 200 and Winnow about 198. **The public items can't tell the systems apart.**

## 2. Where we would probably land on the real board (estimate)

| How we answer yes/no | Accuracy (I) | Score A | Likely rank | Chance accuracy beats Jev | Chance Score A beats Jev |
|---|---|---|---|---|---|
| As trained | about 53 (49-58) | about 69 | about #11 (#8-#21) | 0.00 | 0.02 |
| Firm yes/no | about 68.5 (63-74) | about 73.1 | about #3 (#1-#7) | 0.19 | 0.76 |
| "Band edge" yes/no | about 68.5 (63-74) | about 73.9 | about #1 (#1-#3) | 0.19 | 0.90 |

**Why the hidden half matters.** Half of the accuracy score comes from 720 hidden ("sealed") items. JevK5, Plumb and decider scored 61-62 on the public items, like us, then dropped 10-12 points on the hidden ones. Jev and the 12B leaders did not. Likely result: **we win Score A on speed and cost, but lose on accuracy.**

## 3. Your success rule

Beat Jev on overall accuracy (OHS-3 and JevBench) and on every other metric. Calibration may lose; yes/no may be a little lower.

| What we must win | Chance | Where it stands today |
|---|---|---|
| OHS-3 overall accuracy | 0.45 | Coin flip: −0.3 pp [−3.6, +3.2] |
| JevBench accuracy, our public run | 0.88 | Win, but on items we built with |
| JevBench accuracy, real board | 0.19 | Likely loss |
| Hijack | 0.97 | **Proven win**: 0.6% vs 99.4% (the adaptive attack not run yet) |
| Cost | 0.95 | **Proven win**: $0.0245 vs $0.0384 per 1K |
| Prompt injection | 0.70 | Tie: 1.0% vs 1.3% |
| Consistency: yes and no agree | 0.70 | About a tie |
| Consistency: option order | 0.30 | Likely loss: 8.2% drift; Jev never measured |
| Speed, end to end | 0.75 with direct hosting, 0.10 via Modal | **Loss today**: 410 ms vs 187-248 ms |
| Calibration | Allowed to lose | Mixed |
| Yes/no | Allowed to be a bit lower | Below Jev |

**Chance of winning all of them together:**
- About 0.16 if "consistency" means only yes and no agreeing.
- 0.05 if it also covers option order.
- 0.02-0.05 if "JevBench" means the real board.
- Under 0.01 if we stopped today.

**So no, we are not yet winning everything except calibration.** Only hijack and cost are proven.

## 4. What raises the odds most

1. **Host it directly** on an H100 or RTX 5090 with CUDA graphs, timed end to end. Speed: 0.10 to 0.75.
2. **Fix option order.** Measure drift on dev, then test averaging normal and reversed order. Weakest link (0.30).
3. **Firm yes/no answers on JevBench only** ("band edge", fixed in advance). Score A win chance: 0.02 to 0.90. Board accuracy stays behind.
4. **The new 500K 4B on OHS-3.** Accuracy is the coin flip; yes/no is the lever (+1 pp yes/no = +0.39 pp overall).

## 5. What Cygnet and Winnow teach us

- **Size helps on new items.** Both 12Bs held up on the hidden half; every 4B dropped. An open model beating Jev on accuracy exists (Winnow). A 4B doing it does not yet.
- **Quality beats volume.** Winnow trained on about 26K good examples. decider trained on 1.89M and still dropped.
- **How you read the answer matters.** Cygnet is untrained: it reads the answer-letter scores once, with one temperature setting.
- **Both answer yes/no more often** (13-14% skipped, Jev 23%), the same lesson as our firm yes/no.
- We keep our 4B-then-2B rule. Pitch: 3x smaller, faster, cheaper, hijack-proof, and about tied with Jev on accuracy.
