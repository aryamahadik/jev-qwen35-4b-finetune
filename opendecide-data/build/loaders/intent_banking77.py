"""Banking77 loader: the reference example for build/loaders/ (see README.md).

Source: legacy-datasets/banking77 @ f54121560de48f2852f90be299010d1d6dc612ec (parquet; identical to the PolyAI GitHub
CSVs at 57ec275d). Splits: train 10,003 / test 3,080; fields `text` and `label` (ClassLabel, 77 names).
Licence CC-BY-4.0 (open_by). Wrapper at render: "Customer message:\\n{text}" (DESIGN 3.5), so no wrapper meta needed.

What the loader does (DESIGN 13 step 2 hygiene):
  * PII masking (e-mails, phone numbers) via ctx.clean(); the count goes to meta.pii_masked
  * drops rows whose label is missing or outside the ClassLabel range ("invalid_label")
  * drops rows whose text is empty after cleaning ("empty_text")
It does NOT drop duplicates, sample, split off the dev hold-out, or apply the wrapper: those are later steps
(s03 index, s04/s06 sampling, s07 render).

source_id = the row index within the pinned HF split (stable at a pinned revision); label = the ClassLabel name,
e.g. "card_arrival" (the raw id; Choice keys come from assets/labels/keys/banking77.keys.json, never from this).

authored_by: llm:claude:foundation-engineer-1
"""
from __future__ import annotations

import common
from loaders import LoaderContext, register


@register("banking77", splits=("train", "test"), lock_key="banking77", wrapper="banking77", task_family="intent")
def load_banking77(split: str, ctx: LoaderContext):
    ds = ctx.load_hf(split=split)
    names = ds.features["label"].names
    ctx.note("n_classes", len(names))
    for i, row in enumerate(ds):
        lab = row.get("label")
        if not isinstance(lab, int) or isinstance(lab, bool) or not 0 <= lab < len(names):
            ctx.drop("invalid_label")
            continue
        raw = row.get("text")
        if not isinstance(raw, str):
            ctx.drop("empty_text")
            continue
        text, n_pii = ctx.clean(raw)
        if not text:
            ctx.drop("empty_text")
            continue
        meta = {"label_index": lab}
        if n_pii:
            meta["pii_masked"] = n_pii
        yield common.make_record("banking77", split, i, text, label=names[lab], soft=None, meta=meta)
