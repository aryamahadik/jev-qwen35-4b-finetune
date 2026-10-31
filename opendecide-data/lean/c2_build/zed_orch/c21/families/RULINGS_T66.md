# Opus spec rulings: T66

Opus 5.5, Sun 18 Oct 2026 (ET). Read-only review; this file is the only write for T66.

**Basis.** Ruled from written text only: T66/G0_LITE.md (including the Opus batch-1b block) and c21_fam/T66/README.md. Code was read only to locate the cause and to name what must change. No bar is changed. No path containing ohs, sealed, quarantine, longbench, jevbench or preread was opened.

**Built rows.** No T66 pool row exists (rows start Sun 25 at the earliest), so nothing has to be regenerated. The MSG dry run and the solver-B agreement harness must be run again after the fix.

---

## Q8. T66 K7: the message-only length probe

### Spec lines
- T66/G0_LITE.md:4: "Every number below is a design value fixed BEFORE any pilot".
- T66/G0_LITE.md:41, the NO-row construction:
  - "NO row: the same diff with a message taken from ANOTHER change spec of the same base-module group, chosen by a DERANGEMENT within the diff-size quintile of the group, with token Jaccard < 0.5 against the true message, >= 4 tokens, and its (verb class, object) different from the substantive hunk AND from every trivial hunk's description."
  - "A message that describes only a trivial hunk of the same diff is also a NO kind (CH-trivial, >= 25% of NO rows)."
  - "Every diff appears once with its true message (YES) and once with a swapped message (NO): message marginals are identical across labels by construction."
- T66/G0_LITE.md:42 (MSG-REAL): "both messages >= 4 tokens".
- T66/G0_LITE.md:77 (M-MULTI HIGH): "2 trivial hunks and the NO message describes one of them".
- T66/G0_LITE.md:78 (M-OVL HIGH): "true message shares none (describes the intent); the swapped message shares identifiers".
- T66/G0_LITE.md:87: "Same-skeleton regeneration only for NON-G13 answer-check drops".
- T66/G0_LITE.md:89: "SET-LEVEL checks run ONCE per family on the pilot and once on the built family, never at the mix: ... section 7 probes".
- T66/G0_LITE.md:104 (K7): "MSG probes: message-only; diff-only; joint length ...; lexical-overlap probe on the hard stratum (>= 30% of MSG rows ...) | each AUC <= 0.55, ub <= 0.60".
- T66/G0_LITE.md:163: "Allowed fix levers: generator parameters, quotas, kind mix, group sizes, wording pools, ...; NOT the bars. Defects found before the pilot by unit tests, the build skeptic or A/B disagreement on CPU fixtures are build fixes."
- T66/G0_LITE.md:211 (T66-B3): "describes" = the single substantive hunk; a trivial-hunk message is NO.
- T66/G0_LITE.md:213 (T66-B5): pilot = 50% of the 800 generated rows = 400, proportional by head.
- T66/G0_LITE.md:216-218 (T66-B7): "... so message-only and diff-only probes are at chance by construction, as in the generated MSG block."
- c21_fam/T66/README.md section 2: "a swapped message keeps the neighbour's wording but names THIS diff's identifiers".
- c21_fam/T66/README.md section 5: "Cause: the swapped messages are always style I (longer characters per token) and the trivial messages are shorter".
- c21_fam/T66/gates.py `k7_msg`: message_only = [token count, character length].

### Cause, read against the text
1. **The NO-message source departs from the text.** The text takes the partner spec's message as is. The generator instead redraws it: the partner's kind, a forced style (`SWAP_STYLE_RULE = "inverted_only"`, so always style I) and THIS diff's identifiers. Swapped messages therefore have a different length and character distribution from YES messages. This breaks the property the text states at :41 and :216-218 ("identical by construction").
2. **CH-trivial NO messages form a population that never appears as YES.** If they are shorter, length predicts NO. The text keeps this kind at >= 25% of NO rows (:41). Its length must be neutralised by construction; the kind cannot be removed.

Neither lever tried in the dry run restores identity by construction:
- `LENGTH_MATCH` matched against re-styled swaps;
- `SWAP_STYLE_RULE="opposite"` moves the style signal around and breaks the overlap stratum.

### Ruling: the exact design rule
- **R1. Source: verbatim swap.** Every non-trivial NO message is the partner spec's TRUE message, verbatim as rendered in the partner's own YES row: same wording id, style and slot fillers, including the partner's identifiers. No redraw, no style rule and no re-binding of slots to this diff. Remove `SWAP_STYLE_RULE` and the slot re-binding for swapped messages.
- **R2. Derangement over the swap set.** In each base-module group:
  - let D = the diffs whose NO row is a swap, and T = the diffs whose NO row is CH-trivial;
  - sigma is a derangement of D onto D: each D diff's true message is used exactly once as a NO message on another D diff;
  - it stays within the diff-size quintile and keeps Jaccard < 0.5, >= 4 tokens and the verb-class / object constraints (:41);
  - so the NO messages of D equal the YES messages of D exactly, as a multiset.
- **R3. CH-trivial matched to its own diff's true message.** For each i in T, the true message m_i is not reused (by R2). The CH-trivial NO message t_i, which describes one of i's own trivial hunks, must have:
  - the SAME rendered token count as m_i;
  - the SAME style (I or N) as m_i;
  - a character length within +-3 characters of m_i.
  If the pool has no such wording, regenerate the group on the same skeleton (non-G13, :87); an unmatched draw is never allowed.
  - Wording-pool lever (:163, a build fix before the pilot): write the trivial-kind templates (fmt, comment, doc) to cover the substantive kinds' token-count and character ranges in both styles.
  - With R1-R3 the message-length multiset is identical across labels inside every group, so the message-only probe is at chance by construction (T66-B7).
- **R4. The M-OVL hard stratum is built inside R1** (K7 asks >= 30% of MSG rows). Take a true message in style N, and choose its derangement partner inside the same base module so that the partner's verbatim style-I message names identifiers that occur in THIS diff. Plan group specs so that partner hunks touch functions visible in each other's diffs. Do not re-bind slots.
- **R5. >= 4 tokens on every generated message, YES included.** Every true message must be usable as a swap for the marginals to be identical (:41; MSG-REAL :42). The pool lint's 4-16 token rule already covers this; assert it per row.

### What the text allows changing
- **CH-trivial share:** NO. ">= 25% of NO rows" (:41) is a design value (:4) and a policy kind (T66-B3, M-MULTI). Keep it; under R3 it carries no length signal.
- **NO-message source:** the text fixes it (:41). The current redraw is the deviation, and returning to the verbatim swap is REQUIRED.
- **K7 bar:** unchanged.

### Which read binds
- K7 is a section 7 probe, so it is SET-LEVEL. It is read on the pilot (first look, about 100 of the 400 pilot rows are MSG; T66-B5) and on the built family, which is binding (:89).
- The 4-seed dry run is a build-stage diagnostic. Its failure is a defect to fix before the pilot (:163), but it is not the gate read.
- Re-run the solver-B agreement harness after R1-R5, because B's dev rounds used the redrawn messages.
