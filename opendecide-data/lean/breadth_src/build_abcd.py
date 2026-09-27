"""Build raw rows for abcd (ABCD, Action-Based Conversations Dataset; Chen et al., NAACL 2021).

Source : GitHub asappresearch/abcd, data/abcd_v1.1.json.gz, key 'train' ONLY (dev/test never read into rows).
         Pinned to commit 6b8700ce67c6b37b062dd7a60abc76d7ef832a97; raw files snapshotted under cache/abcd/ with sha256.
Licence: MIT (repo LICENSE file, "Copyright (c) 2021 ASAPP Research").
Texts  : human-human chats (crowd "Expert Live Chat": one worker plays customer from an assigned scenario, one the agent).
Labels : the scenario's flow (10) and subflow the customer was assigned (human-set scenario, not model-labelled).
         FAQ subflows (boots_how_1, pricing_3, ...) are merged to their article/category as in the official ontology,
         giving the 55 official subflow intents. Data-only spellings are mapped to ontology names:
         subscription_inquiry/status_questions -> status_active, order_issue/status_delivery_date -> status_delivery_time.
State  : the first 1-3 customer turns (verbatim, action logs and agent turns dropped), one per line as "Customer: ...".
Tasks  : each source record is used once, either for the 55-way intent question (MAX_SUB rows, round-robin) or the
         10-way issue-category question (the rest, round-robin). Soft labels: none (single scenario label) -> null.
Deterministic (seed 20261101).
"""
import collections
import gzip
import hashlib
import json
import random
import re
import sys
import urllib.request
from pathlib import Path

SEED = 20261101
MAX_ROWS = 650
MAX_SUB = 390  # rows for the 55-way intent question; the rest go to the 10-way flow question
KEY = "abcd"
HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
CACHE = HERE / "cache" / KEY
OUT = LEAN / "data" / "v13_parts" / "raw" / f"{KEY}.jsonl"

COMMIT = "6b8700ce67c6b37b062dd7a60abc76d7ef832a97"
BASE = f"https://raw.githubusercontent.com/asappresearch/abcd/{COMMIT}/"
FILES = {
    "data/abcd_v1.1.json.gz": "2bdf53ac359543dcdc38d55bc6513e78df120363f8f44870716e909f4606de15",
    "data/ontology.json": "2e1c1d763518ba084ada7f7bc8b54f0b489c81da3b170875cf9340891e06524c",
    "LICENSE": "3ab7e179a7f13027b7bc64293541f0e9beacca3701cade67fb8fce78c2d9317b",
}
LICENCE = ("MIT (https://github.com/asappresearch/abcd/blob/" + COMMIT + "/LICENSE, "
           "'Copyright (c) 2021 ASAPP Research')")

FLOW_Q = "Which broad category of customer-service issue is the customer contacting support about?"
SUB_Q = "Which specific customer-service request does the customer have?"

FLOW_NAMES = {
    "account_access": "account access",
    "manage_account": "manage account",
    "order_issue": "order issue",
    "product_defect": "product defect",
    "purchase_dispute": "purchase dispute",
    "shipping_issue": "shipping issue",
    "single_item_query": "single-item question",
    "storewide_query": "storewide question",
    "subscription_inquiry": "subscription inquiry",
    "troubleshoot_site": "site troubleshooting",
}
SUB_NAMES = {
    ("account_access", "recover_username"): "recover username",
    ("account_access", "recover_password"): "recover password",
    ("account_access", "reset_2fa"): "reset two-factor authentication",
    ("manage_account", "status_service_added"): "unknown service added",
    ("manage_account", "status_service_removed"): "service wrongly removed",
    ("manage_account", "status_shipping_question"): "account international shipping question",
    ("manage_account", "status_credit_missing"): "account credit missing",
    ("manage_account", "manage_change_address"): "change account address",
    ("manage_account", "manage_change_name"): "change account name",
    ("manage_account", "manage_change_phone"): "change account phone number",
    ("manage_account", "manage_payment_method"): "change account payment method",
    ("order_issue", "status_mystery_fee"): "unexpected fee on order",
    ("order_issue", "status_delivery_time"): "change delivery time",
    ("order_issue", "status_payment_method"): "wrong order payment method",
    ("order_issue", "status_quantity"): "wrong order quantity",
    ("order_issue", "manage_upgrade"): "upgrade to overnight shipping",
    ("order_issue", "manage_downgrade"): "downgrade shipping speed",
    ("order_issue", "manage_create"): "add item to existing order",
    ("order_issue", "manage_cancel"): "remove duplicate item from order",
    ("product_defect", "refund_initiate"): "start a refund",
    ("product_defect", "refund_update"): "add item to existing refund",
    ("product_defect", "refund_status"): "refund status",
    ("product_defect", "return_stain"): "return due to stain",
    ("product_defect", "return_color"): "return due to color",
    ("product_defect", "return_size"): "return due to size",
    ("purchase_dispute", "bad_price_competitor"): "competitor price lower",
    ("purchase_dispute", "bad_price_yesterday"): "price was lower yesterday",
    ("purchase_dispute", "out_of_stock_general"): "items generally out of stock",
    ("purchase_dispute", "out_of_stock_one_item"): "one item out of stock",
    ("purchase_dispute", "promo_code_invalid"): "promo code invalid",
    ("purchase_dispute", "promo_code_out_of_date"): "promo code expired",
    ("purchase_dispute", "mistimed_billing_already_returned"): "billed for returned item",
    ("purchase_dispute", "mistimed_billing_never_bought"): "billed for item never bought",
    ("shipping_issue", "status"): "shipment status question",
    ("shipping_issue", "manage"): "change shipment details",
    ("shipping_issue", "missing"): "item never arrived",
    ("shipping_issue", "cost"): "shipping cost too high",
    ("single_item_query", "boots"): "boots product question",
    ("single_item_query", "shirt"): "shirt product question",
    ("single_item_query", "jeans"): "jeans product question",
    ("single_item_query", "jacket"): "jacket product question",
    ("storewide_query", "pricing"): "store pricing question",
    ("storewide_query", "membership"): "membership question",
    ("storewide_query", "timing"): "store timing question",
    ("storewide_query", "policy"): "store policy question",
    ("subscription_inquiry", "status_active"): "is subscription active",
    ("subscription_inquiry", "status_due_amount"): "subscription amount due",
    ("subscription_inquiry", "status_due_date"): "subscription due date",
    ("subscription_inquiry", "manage_pay_bill"): "pay subscription bill",
    ("subscription_inquiry", "manage_extension"): "subscription payment extension",
    ("subscription_inquiry", "manage_dispute_bill"): "dispute subscription bill",
    ("troubleshoot_site", "credit_card"): "credit card rejected",
    ("troubleshoot_site", "shopping_cart"): "cart not updating",
    ("troubleshoot_site", "search_results"): "search not working",
    ("troubleshoot_site", "slow_speed"): "website too slow",
}
DATA_ALIASES = {("subscription_inquiry", "status_questions"): "status_active",
                ("order_issue", "status_delivery_date"): "status_delivery_time"}


def fetch(rel, sha):
    path = CACHE / Path(rel).name
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(BASE + rel, path)
    got = hashlib.sha256(path.read_bytes()).hexdigest()
    if got != sha:
        sys.exit(f"sha256 mismatch for {path}: {got}")
    return path


def norm(t):
    return re.sub(r"\s+", " ", t).strip().lower()


def official_subflow(flow, sub):
    if flow in ("single_item_query", "storewide_query"):
        return sub.split("_")[0]  # boots_how_1 -> boots, pricing_3 -> pricing
    return DATA_ALIASES.get((flow, sub), sub)


def round_robin(pools, n):
    labels = sorted(pools)
    out, i = [], 0
    while len(out) < n and any(pools[k] for k in labels):
        k = labels[i % len(labels)]
        if pools[k]:
            out.append(pools[k].pop())
        i += 1
    return out


def main():
    paths = {rel: fetch(rel, sha) for rel, sha in FILES.items()}
    ont = json.loads(paths["data/ontology.json"].read_text())["intents"]
    assert set(ont["flows"]) == set(FLOW_NAMES)
    ont_subs = {(f, s) for f, ss in ont["subflows"].items() for s in ss}
    assert ont_subs == set(SUB_NAMES) and len(ont_subs) == 55
    assert len(set(SUB_NAMES.values()) | set(FLOW_NAMES.values())) == 65  # all option names distinct

    train = json.load(gzip.open(paths["data/abcd_v1.1.json.gz"]))["train"]  # TRAIN ONLY
    flow_opts = sorted(FLOW_NAMES.values())
    sub_opts = sorted(SUB_NAMES.values())

    stats = collections.Counter()
    seen = set()
    recs = []
    for c in train:
        flow, sub = c["scenario"]["flow"], c["scenario"]["subflow"]
        osub = official_subflow(flow, sub)
        assert (flow, osub) in SUB_NAMES, (flow, sub)
        turns = [t for sp, t in c["original"] if sp == "customer" and t.strip()][:3]
        state = "\n".join("Customer: " + t.strip() for t in turns)
        if not (15 <= len(state) <= 4000):
            stats["len_drop"] += 1
            continue
        n = norm(state)
        if n in seen:
            stats["dup_drop"] += 1
            continue
        seen.add(n)
        recs.append({"rid": str(c["convo_id"]), "state": state, "flow": flow, "sub": sub, "osub": osub})

    rng = random.Random(SEED)
    recs.sort(key=lambda r: int(r["rid"]))
    rng.shuffle(recs)

    # 1) 55-way intent rows
    pools = collections.defaultdict(list)
    for r in recs:
        pools[SUB_NAMES[(r["flow"], r["osub"])]].append(r)
    sub_rows = round_robin(pools, MAX_SUB)
    used = {r["rid"] for r in sub_rows}
    # 2) 10-way flow rows from the remaining records
    pools = collections.defaultdict(list)
    for r in recs:
        if r["rid"] not in used:
            pools[FLOW_NAMES[r["flow"]]].append(r)
    flow_rows = round_robin(pools, MAX_ROWS - len(sub_rows))

    def row(r, level):
        sub_level = level == "subflow"
        return {
            "key": KEY,
            "rid": r["rid"],
            "state": r["state"],
            "instructions": SUB_Q if sub_level else FLOW_Q,
            "options": sub_opts if sub_level else flow_opts,
            "gold": SUB_NAMES[(r["flow"], r["osub"])] if sub_level else FLOW_NAMES[r["flow"]],
            "soft": None,
            "meta": {
                "dataset": "ABCD (Action-Based Conversations Dataset), asappresearch/abcd",
                "config": f"data/abcd_v1.1.json.gz; label level={level} ({'55 official subflows' if sub_level else '10 flows'})",
                "revision": f"git:{COMMIT}; sha256:{FILES['data/abcd_v1.1.json.gz']}",
                "licence": LICENCE,
                "split": "train",
                "orig_label": {"flow": r["flow"], "subflow": r["sub"], "official_subflow": r["osub"]},
            },
        }

    out = [row(r, "subflow") for r in sub_rows] + [row(r, "flow") for r in flow_rows]
    assert len({r["rid"] for r in out}) == len(out)
    rng.shuffle(out)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    import statistics
    lens = [len(r["state"]) for r in out]
    print(f"train convos={len(train)} usable={len(recs)} drops={dict(stats)}")
    print(f"wrote {len(out)} rows -> {OUT}  (subflow rows={len(sub_rows)}, flow rows={len(flow_rows)})")
    for lvl in ("subflow", "flow"):
        rows = [r for r in out if r["meta"]["config"].split("level=")[1].startswith(lvl + " ")]
        cnt = collections.Counter(r["gold"] for r in rows)
        top = max(cnt.values()) / len(rows)
        print(f"[{lvl}] labels={len(cnt)} max share={top:.1%}")
        print("  ", dict(sorted(cnt.items())))
    print(f"soft coverage: {sum(r['soft'] is not None for r in out)}/{len(out)}")
    print(f"length chars: min={min(lens)} median={int(statistics.median(lens))} mean={statistics.mean(lens):.0f} max={max(lens)}")


if __name__ == "__main__":
    main()
