# Must-haves for the 2B hard-data build (owner + Codex review, 30 Sep 2026)

1. **Test generalisation, not memorisation.** The 2B A/B test must score on:
   - generator families and templates that were NOT used to make the added training rows (hold out whole
     templates or families, not only seeds);
   - real human-labelled dev sets (dev, devzs, and the dev splits of weak-area sources).

   If the gain appears only on the same generators, the data is rejected: it teaches shortcuts.
2. **No regression.** Multiple choice must not drop, using the pre-registered pass rule on dev. Security
   (jagged/OPI) must not get worse.
3. **Labels by program only**, with no model labels. The added rows are trained on gold only (kd_skip).
4. **The 4B is not patched automatically.** "4B_main + hard" (a short extra fine-tune) is a separate variant. It is
   used only if it passes the same dev ship gate against 4B_main. The clean 500K result stays the headline.
5. **OHS-3 is never used** to choose data, settings or variants.
