## Long irrelevant state (eval_long)

Accuracy on the same questions: clean state vs the message buried in ~1,500 / ~4,500 words.

| Model | Choice clean | Choice 1.5k | Choice 4.5k | Yes/no clean | Yes/no 1.5k | Yes/no 4.5k |
|---|---|---|---|---|---|---|
| jev | 93.0 [87.0–98.0] | 90.0 [84.0–95.0] | 90.0 [84.0–95.0] | 87.0 [80.0–93.0] | 86.0 [80.0–92.0] | 85.0 [78.0–92.0] |
| q4b_v05_A3 | 94.0 [89.0–98.0] | 96.0 [92.0–99.0] | 95.0 [90.0–99.0] | 93.0 [88.0–97.0] | 94.0 [89.0–98.0] | 96.0 [92.0–99.0] |
| g12_v06_A3_cal | 95.0 [91.0–99.0] | 95.0 [90.0–99.0] | 91.0 [85.0–96.0] | 90.0 [83.0–96.0] | 83.0 [75.0–90.0] | 83.0 [75.0–90.0] |

## Several records in one state (eval_multi)

3-6 support tickets in the state; the question names one ticket. Accuracy, 95% bootstrap CI over states.

| Model | Choice | Yes/no (all) | Yes/no about a distractor ticket's label |
|---|---|---|---|
| jev | 90.6 [86.1–94.4] | 88.9 [84.4–92.8] | 95.5 [91.0–99.1] |
| q4b_v05_A3 | 92.8 [88.3–96.1] | 95.6 [92.2–98.3] | 97.3 [93.7–100.0] |
| g12_v06_A3_cal | 90.6 [86.1–94.4] | 91.1 [86.7–95.0] | 97.3 [93.7–100.0] |

