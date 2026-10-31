# Narrowed OHS-AC keyword export: brief for a FRESH sealed agent (owner option 2 (b)) — NOT RUN

Status: a design. Nothing in this brief has been run, the output folder does not exist, and no agent has been started. It is sent only after
(1) the owner decides option 2 in words and (2) the orchestrator writes a ruling in PREREG_FINAL.md that carries the marker `OHSAC_KW_NARROW`
(`ruling_gate.py`). It is written in the form of `zed_orch/AC_SEALED_BRIEF.md` (same isolation rules); where they differ, this file only adds.

## 0. Who you are, and what you must not be

You are a **fresh sealed agent**: new context, no C2 conversation, no C2 hit data, no notion of which C2 text hit which keyword. The orchestrator
must NOT put any C2 count, family name, block name, example or hit list in your prompt beyond this file. If you have seen any, stop and say so.
You build ONE hash-only folder. Nobody on the C2 side ever sees a name you handle.

## 1. The rule is fixed and is not yours to change

The rule is `c2_build/zed_orch/owner_options/keyword_rule.py` (read it; import it; do not copy it; do not edit it; its sha256 goes into your
MANIFEST and the C2 loader refuses any other). In words (the file is the authority):

| step | test on one NAME (plain text, as your freeze builder has it) | result |
|---|---|---|
| R0 | normalise: lower-case, collapse spaces, strip `.,;:!?"'()[]{}<>` at both ends; under 4 characters | drop `too_short` |
| R1 | two or more space-separated tokens | KEEP `multi_token` |
| R2 | one token that contains a digit or any of `/ . _ @ : #` (dataset ids, hosts, file-like names) | KEEP `identifier` |
| R3 | one token, 5 or more characters, `wordfreq.zipf_frequency(token, "en", wordlist="large") < 3.0` | KEEP `rare_word` |
| R4 | anything else | drop `short_single` (under 5 characters) or `common_word` (Zipf >= 3.0) |

No allow-list, no deny-list, no per-name override, no second pass, no "borderline" handling. If the rule keeps a name you think is common, or
drops one you think is specific, you keep the rule's answer and may mention the COUNT of such disagreements, never the names.

Frequency source: `wordfreq` exactly `3.1.1` (`keyword_rule.WORDFREQ_VERSION`), installed into a virtualenv under `ohs_ac_sealed/tmp/` (network
is allowed for that one `pip install` only; record the wheel sha256 in your report). `keyword_rule.wordfreq_zipf()` fails closed if it is
missing or another version.

## 2. Isolation (as AC_SEALED_BRIEF section 1, plus)

- Read: the freeze keyword builder and its plain-text name list inside `ohs_ac_sealed/` (the code that wrote `sealed_hashes_ac/keyword_hashes.jsonl`
  and its inputs: every held-out registry / tool / carrier name of length >= 4 and every real-text source identifier), `c2_build/sealed_hashes_ac/`
  (hash files: for the subset check only), `c2_build/zed_orch/owner_options/keyword_rule.py`.
- Write: `ohs_ac_sealed/tmp/` and `c2_build/sealed_hashes_ac_kw2/` (new folder; create it; **never** write into `sealed_hashes_ac/` or
  `sealed_hashes_ac_union/`; if `sealed_hashes_ac_kw2/` already exists, stop and report).
- Do not read C2 data, C2 logs (`c2_build/logs/**`, `logs/decontam_counts/**`), C2 families' training files, pools or candidates.
  Do not run any C2 tool on C2 data. Do not run the compare of your output against any C2 text. The orchestrator does that, counts only.
- Seeds stay sealed (as AC_SEALED_BRIEF). Your reply and every file outside `ohs_ac_sealed/` hold counts, sha256 hashes and file names only: no
  name, token, id, value, URL host or example, not even a "typical" one, and no per-family or per-source breakdown that would identify a name.

## 3. What to build

1. Run your freeze keyword builder's name collection UNCHANGED to get the list of NAMES (plain text, in memory only; do not write it anywhere).
   Count them (`names_total`).
2. For each name call `keyword_rule.decide(name, zipf)`. Tally `kept_names_by_reason` and `dropped_names_by_reason`.
3. For each kept name produce the keyword hashes **with the freeze builder's own hash function** (the one that made `keyword_hashes.jsonl`: the
   FORMAT.md keyword rule, the run and its punctuation-stripped variant, URL hosts with and without `www.`). Collect them in a set.
4. Write `c2_build/sealed_hashes_ac_kw2/keyword_hashes.jsonl`: one line `{"kind": "keyword", "hash": "<64 hex>"}` per hash, sorted, no duplicates.
5. Write `c2_build/sealed_hashes_ac_kw2/MANIFEST.json` with exactly:
   ```
   {"kind": "ac_keyword_narrow", "version": 1,
    "parent_manifest_sha256": <sha256 of c2_build/sealed_hashes_ac/MANIFEST.json as it is now>,
    "files": {"keyword_hashes.jsonl": {"sha256": ..., "records": <lines>}},
    "rule": {"version": 1, "file": "keyword_rule.py", "rule_sha256": <sha256 of keyword_rule.py now>, "min_len_single": 5, "zipf_max": 3.0,
             "wordfreq_version": "3.1.1", "export_min_len": 4},
    "counts": {"full_keyword_hashes": <lines of sealed_hashes_ac/keyword_hashes.jsonl>, "narrowed_hashes": <records>,
               "kept_names_by_reason": {...}, "dropped_names_by_reason": {...}},
    "built_utc": ..., "builder_sha256": <sha256 of your build script>}
   ```
6. Self-checks before you report (all must hold; report each as pass/fail only):
   a. every narrowed hash is in `sealed_hashes_ac/keyword_hashes.jsonl` (set subset by hash; no token is ever looked up);
   b. `0 < narrowed < full`; the three kept reasons and the three dropped reasons are the only ones used;
   c. recomputing steps 1-4 from scratch gives byte-identical `keyword_hashes.jsonl` (determinism);
   d. `python -B c2_build/zed_orch/owner_options/keyword_narrow.py verify` (the C2 loader) prints `"ok": true` and counts equal yours;
   e. you changed no other file (list the `git status` paths, counts only).

## 4. Report (your final reply: counts and shas only)

`names_total`; `kept_names_by_reason`; `dropped_names_by_reason`; `full_keyword_hashes`; `narrowed_hashes`; sha256 of `keyword_hashes.jsonl`,
`MANIFEST.json`, your build script, `keyword_rule.py`; the wordfreq wheel sha256; self-checks a to e; wall time. If any check fails, write nothing
under `sealed_hashes_ac_kw2/` that is final (delete your partial folder) and report the failing check by its letter.

## 5. After you

The orchestrator (not you) reruns the OHS-AC early check with the narrowed export under the ruling and reports the new drop counts to the owner.
No family is re-opened, no training starts, and no bar changes because of this export; it is one of the owner's options and stays unused until
the ruling exists.
