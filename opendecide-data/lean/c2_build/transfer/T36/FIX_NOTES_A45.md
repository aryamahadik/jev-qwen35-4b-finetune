# T36 A45 c fix notes (partial, not closed)
Cause (verified on a 6,000-row build, 2,873 choice rows): gold position and option count are uniform (k=3: 487/488/483; k=4: 354/360/350/351), abstain/longest/shortest rates equal 1/k. The leak is in the VALUES of the options (token features, not dense: tok-only LR 0.329 vs dense-only 0.273). The gold (a version the range admits) has a larger last number than a wrong option on 43% of rows vs 25% lower (sum of numbers 54% vs 40%); lex rank is uniform.
Tried (both reverted, no gain): finer final_bucket (10 buckets + zero-major/minor flags): tok LR 0.334 overall; exact last number <=9: worse (0.362, dense 0.321).
Kept: yes/no negative wording stratified (strat per gold, each of 3 wordings once per 3 bases) - plugin.py line 932; backups in _backup_a45/. Untested after edit (pytest started, result not read).
Needed next: pool redesign so distractors are drawn from the same candidate distribution around the bounds as the gold (not only error-model outputs of the gold); then pilot_i2.
No pilot_i2 produced.
