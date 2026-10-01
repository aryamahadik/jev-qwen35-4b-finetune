# PREREG_FINAL.md amendment A7 (DRAFT for the owner): the 4B parity stop

**Status:** draft, written 1 Oct 2026 ~05:30 UTC by the gate-runbook job. Nothing in `PREREG_FINAL.md` or `gate_dev.py`
has been changed.

**Name:** A7 follows the A0-A6 drafts in `prereg_drafts/AMENDMENTS_1oct.md`, which were written in parallel.
- A0 there adopts PREREG_FINAL.md and records in section 9 the `gate_dev.py` frozen in `82b07d4` (sha256 `d1f913a3…`).
  Keep that record as it is: it is what was frozen.
- A7 then records the **amended** `gate_dev.py` in its own text (sha256 below; the commit is the one that adds A7).
  The gate job logs the sha256 of the `gate_dev.py` it runs (`events.log`, preflight) and the manifest pins it, so the
  scoring job must show the A7 sha256, not `d1f913a3…`.
- Commit A0 and A7 together, or A7 right after A0, both before job 1. (Review note, 1 Oct: the first draft said A7
  should overwrite A0's section-9 record; that would contradict A0 and the never-edit rule.)

**Deadline:** `PREREG_FINAL.md` says an amendment must be committed **before the first candidate prediction exists**. The
first candidate read is the C1 read in gate job 1, after the 4B finishes (~17:00 UTC today). So this has to be decided
and committed before `gate/gate_4b_l4.sh launch job1`.

## The problem: as frozen, the 4B gate cannot pass its own parity stop

**Defect 1: the tool refuses to run (certain).** PREREG 4 says to run
`python gate_dev.py <fresh REF> q35_4b_pxE --mode refparity`.
- The frozen `gate_dev.py` (sha256 `d1f913a3…`, commit 82b07d4) stops at once:
  `refparity: --size/names say 4B but the metas of 'q35_4b_pxE' record base(s) ['Qwen/Qwen3.5-2B']`.
- The cause is `resolve_size`, which checks the base recorded in the stored REF metas. 4B-E's stored metas say
  Qwen3.5-2B by mistake; PREREG 4 already notes this mistake.
- Every ship look against the stored REF stops the same way. That includes the "tool smoke check" in PREREG 10, which
  no longer reproduces.
- No look can therefore be FINAL, because FINAL needs a passing refparity look.

**Defect 2: the bar fails even with defect 1 fixed (measured).**
- On 30 Sep (11:25-11:51 UTC, logs/audit_parity.log) 4B-E was read with `od_gcp.py predict` on the same L4. This is the
  scoring job's own pipeline: merged, bf16, revision pinned, `forced: []`.
- That read is `q35_4b_pxE_parity`. Against the stored in-process read `q35_4b_pxE` on the 9 splits (8,143 rows):

  | Check | Result | Bar |
  |---|---|---|
  | Argmax agreement | 99.57% | ≥ 99% (pass) |
  | Mean \|dp\| | 0.00255 | ≤ 0.005 (pass) |
  | Max \|dp\| | **0.0986** | ≤ 0.05 (**FAIL**) |
  | Accuracy | 80.72 vs 80.66 (+0.06 pp) | within 0.3 pp (pass) |

- Only 3 rows are above 0.05, and they are long rows:
  - pg_dev r_pg_routing_dev_16: 0.0986 (6 options, 4.4K characters);
  - pg_dev r_pg_policy_dev_11: 0.063;
  - devp_card r_f4c30f555763: 0.056.
- The 99.9th percentile is 0.031.
- The cause is merging the adapter into bf16 weights versus the unmerged in-process model. Plan 3.2 set the 0.05 bar
  on the **dev** split only, where the same read's maximum is 0.022. The ship rule then extended it to the 9 splits,
  which include pg_dev's long rows.
- A fresh 4B-E read in the gate job will almost surely fail the bar in the same way. PREREG 4 then says to stop and
  consult the owner, and ship mode refuses every later look.

**Reproduce (CPU, nothing logged):**
- `gate_dev.py q35_4b_pxE_parity q35_4b_pxE --mode refparity --no-log` (frozen tool) gives the base error above.
- A scratch copy with option b gives `PARITY FAIL` (max \|dp\| 0.0986).
- `gate/tests/sim_gate.py` scenarios `frozen` and `B` run the whole job and show the same two stops.

## Proposed amendment (text to append to PREREG_FINAL.md, dated, before the first candidate read)

> **Amendment A7 (1 Oct 2026, before any candidate prediction).** The 4B stored REF for the parity stop (section 4) is
> `q35_4b_pxE_parity`, not `q35_4b_pxE`.
> - `q35_4b_pxE_parity` is the `od_gcp.py predict` read of 4B-E made on the Google L4 on 30 Sep 2026 (11:25-11:51
>   UTC): merged, bf16, revision 851bf6e8, layout schema_branch_mark, no forced override, 8,143 rows on the 9 splits.
> - Its file sha256 values are recorded below.
> - **Reason.** The only merged predict read of 4B-E we have (30 Sep) does not reproduce the in-process read
>   `q35_4b_pxE` within the max |dp| ≤ 0.05 bar: its max is 0.0986 (3 of 8,143 rows are above 0.05, all long pg_dev /
>   devp_card rows), and it passes the other three checks. The cause is the bf16 merge versus the unmerged in-process model, so a new fresh read would almost surely
>   miss too. The frozen tool also refuses `q35_4b_pxE`, because its metas record base Qwen3.5-2B.
> - **What stays the same:** the bar, the 9 splits, the stop rule, the fresh-REF rule, the ship rule and every
>   threshold. The parity stop now checks what it was meant to check: that the scoring job reproduces the scoring
>   pipeline.
> - **The link to the in-process read is recorded** and was not chosen on any candidate: `q35_4b_pxE_parity` vs
>   `q35_4b_pxE` gives agreement 99.57%, mean |dp| 0.00255, max |dp| 0.0986, accuracy +0.06 pp.
> - **Code:** `STORED_REF["4b"] = "q35_4b_pxE_parity"` in `gate_dev.py` (patch `prereg_drafts/amendment_A7a_gate_dev.patch`).
>   Optional b: `resolve_size` reads the base of an in-process meta from its training cfg (patch
>   `amendment_A7ab_gate_dev.patch`, both changes together).
> - **Tests:** `tests/test_amendment_A7.py`.
> - **Freeze record after A7** (adds to A0's section-9 record of the 82b07d4 file): `gate_dev.py` sha256
>   `78975445bc9b72c6ea3bee2ef74e80330928cbd711015fed4005608186799fc5` (option a) [OWNER: or
>   `374f604f84a3739d1f81c2289800e4bad49c04b4df767ba2d2272aa8f2e16972` if a + b]; re-check with `shasum -a 256 gate_dev.py`
>   after patching.
> - **The 2B is unchanged here.** Its stored REF `q35_2b_v11r` is also an in-process read. Before the 2B is scored,
>   check whether a predict read of v11r meets the bar on all 9 splits. The dev split alone gives max |dp| 0.023;
>   pg_dev is the risk.
> - **C2 and C3 are read as ordinary adapters.** The `cat` averages are written to disk as one PEFT adapter by
>   `gate/materialize_cat.py` and read with `od_gcp.py predict`. `od_gcp.py blend` writes a "blend" meta that the
>   pipeline check refuses, and it has no `--perm-seed` for the `_perm` read.
>   - The math is PEFT 0.21.0's `add_weighted_adapter(cat)`, and in fp32 it is bit-identical (gate/tests/peft_equivalence_check.py).
>   - On a bf16 base, `od_gcp.py blend` also rounds the blended A and B to bf16 before merging. The materialized
>     adapter keeps them fp32: the same average with one rounding step less.
> - **Three readings that the original text leaves open:**
>   1. C3's "passes every constraint on select AND confirm" means constraints (b), (c), (d) on each half (T fitted on
>      the other half, without tb_mixtral) and (g) on the full attack sets, all against the job-2 fresh REF.
>   2. If C2 and C3 both meet the replacement rule, the owner chooses.
>   3. A NOT FINAL ship look stops the sequence; ship look 2 is not run.
>
> Stored-REF sha256 values (`preds_<split>/q35_4b_pxE_parity.jsonl`):
>
> | Split | sha256 |
> |---|---|
> | dev_nc | 1e0fb93d969b9c80c0f2a593b67035f2dced373d416b9c9f2163db9496a2c806 |
> | taskbank_dev | 26b182d10f25647af22f6f987fd457ba8c1518dbd6b88dc5c589fc9a2e92df3d |
> | hard_dev | 581cb02ff392b99100c36c2fc5a04bbc3952fcf7a5ec3dc89494515b5e50c69e |
> | dev_negwords | 961b158801dcae895f383a4300312a29fa983081da84545d9d172fd978ff9897 |
> | dev_claims | 62cce5c9d040759aa0563ae6ed6d1e7764f5c73133f6af188fba8dfd76cc6142 |
> | pg_dev | f1063b0409542ade959ec4b7c98873441ebc159802f51cef2078440ca32088e7 |
> | devzs | 278b75c0b61d56b2fe8e6bc4b91234db343ce173d51fe4b8dc58292b94a75959 |
> | devp_card | 5d48bf46f163b4bae473899b466e28bfe12e478ae28eceee2a2bfd489a3c0364 |
> | dev | d3a7fb756da22f1adfeda1f8429f15aaa99a3157ab50962efded4faeba6822aa |

## Options for the owner

| Option | What changes | Effect | Risk |
|---|---|---|---|
| **a (recommended)** | `STORED_REF["4b"]` → `q35_4b_pxE_parity` | Defects 1 and 2 are solved. The bar is unchanged. | If the L4 software changed since 30 Sep, the parity look fails. That is the job of the stop, and it happens **before** any candidate is read (the script reads REF first). |
| a + b | as a, plus `meta_base` in `resolve_size` | The same, and the tool can also compare against the in-process read for the report | None found: 32/32 tests pass. |
| b alone | only `meta_base` | Defect 1 is fixed, defect 2 is not | The parity look fails (simulation `B`): stop. |
| c | Keep `q35_4b_pxE`, fix b, and replace max \|dp\| ≤ 0.05 with a quantile rule (e.g. 99.9th percentile ≤ 0.05) | Passes on the 30 Sep numbers | A threshold changed after seeing REF-vs-REF data. It is defensible (no candidate data), but weaker than a. |
| 0 | Nothing | The gate cannot give a FINAL verdict | The 4B ships as 4B-E by default, or the decision becomes ad hoc. |

**Also fix at the same commit:**
- PREREG_FINAL.md still says "Status: DRAFT, pending owner review".
- Section 9 (the freeze record) is still blank. A0 fills it with the 82b07d4 file; A7's own text adds the amended
  file's sha256 (a commit cannot name its own hash, so the A7 commit is identified as the commit that adds A7). The
  scratch copies give these sha256 values:
  - option a: `78975445bc9b72c6ea3bee2ef74e80330928cbd711015fed4005608186799fc5`;
  - options a + b: `374f604f84a3739d1f81c2289800e4bad49c04b4df767ba2d2272aa8f2e16972`.
- Neither the stored 4B-E preds nor the parity read are tracked in git. The sha256 table above, and
  `gate/manifest_4b.sha256` on the VM, are what protect them.

## How to adopt (owner, on the Mac, before `launch job1`)
```
cd ~/Documents/jev/opendecide-data/lean
patch gate_dev.py < prereg_drafts/amendment_A7a_gate_dev.patch        # or amendment_A7ab_gate_dev.patch
cp prereg_drafts/test_amendment_A7.py tests/
../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_ship_rule.py tests/test_amendment_A7.py   # 31 (a) / 32 (ab) pass
# append A0 (AMENDMENTS_1oct.md) and the quoted A7 above to PREREG_FINAL.md (dated; A7 carries the new sha256), then:
git add gate_dev.py tests/test_amendment_A7.py PREREG_FINAL.md && git commit -m "PREREG_FINAL amendment A7: 4B parity stop vs the 30 Sep predict read"
bash gate/gate_4b_l4.sh manifest      # the manifest must be re-made after gate_dev.py changes
```
