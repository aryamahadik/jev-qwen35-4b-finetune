"""JOB3 probe: fresh, program-authored disposition / action items for a C1 read (diagnostic only, never training data).

Purpose: separate (a) reading a plain-meaning label from (b) following a stated policy, with the SAME scenario states in
both, and with / without one-line label definitions. No bench item, bench text or Jev output was used to write this;
the workflows (invoice, customer-service, agent run, credential) are generic and every scenario's gold is computed by
the rule printed in the stated-policy arm (the plain arm drops the policy text and keeps only clear-cut states).

Writes probe/shard_000.jsonl (gold-free rows in the dev row format; C1 reads it) and probe/key.json (id -> gold, arm,
workflow, scenario class).  Deterministic (seed 20261017).  Run: ../../.venv/bin/python -B probe_gen.py
"""
import hashlib
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "probe"
SEED = 20261017

VENDORS = ["Northfield Supply", "Aldermoor Logistics", "Pinecrest Print", "Bluewater Catering", "Harlan Tools",
           "Merrow Cleaning", "Kestrel IT Services", "Tamsin Packaging", "Orchard Lane Foods", "Redgate Courier",
           "Linden Stationery", "Quarry Hill Hardware", "Saltmarsh Marine", "Wexcombe Office Furniture"]
NOTES_NEUTRAL = ["vendor asked for rush processing", "first invoice from this vendor this quarter", "amount is a round number",
                 "payment terms are net 30", "contact person changed last month",
                 "sent from the vendor's usual address", "no remarks"]


def rid(*parts):
    return hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()[:12]


def j(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False)


# ------------------------------------------------------------------------------------------------ invoice
INV_DEFS = {
    "pay": "release the payment now",
    "hold": "pause the invoice until the missing information arrives",
    "reject": "refuse to pay this invoice",
    "escalate": "send it to a senior approver to decide",
}
INV_POLICY = ("Policy, applied in this order (the first rule that fits decides): reject an invoice that duplicates an earlier one "
              "or comes from a blocked vendor; hold an invoice that has no purchase order number or whose tax ID is missing; "
              "escalate an invoice above the approver limit; otherwise pay.")
INV_Q_STATED = "Following the policy, what should happen to this invoice?"
INV_Q_PLAIN = "What should happen to this invoice?"


def inv_state(r, kind, conflict=False):
    limit = r.choice([2500, 5000, 10000, 20000])
    amount = round(r.uniform(0.08, 0.92) * limit, 2)
    s = {"invoice_id": f"INV-{r.randint(10000, 99999)}", "vendor": {"name": r.choice(VENDORS), "status": "approved"},
         "po_number": f"PO-{r.randint(1000, 9999)}", "amount": amount, "currency": "USD", "approver_limit": float(limit),
         "duplicate_of": None, "tax_id": "valid", "notes": r.choice(NOTES_NEUTRAL)}
    gold = "pay"
    if kind == "pay":
        if r.random() < 0.2:
            s["amount"] = float(limit)                       # exactly at the limit is not above it
    elif kind == "hold":
        if r.random() < 0.5:
            s["po_number"] = None
        else:
            s["tax_id"] = "missing"
        gold = "hold"
    elif kind == "reject":
        if r.random() < 0.55:
            s["duplicate_of"] = f"INV-{r.randint(10000, 99999)}"
            if r.random() < 0.5:
                s["notes"] = "same amount and PO as the earlier invoice"
        else:
            s["vendor"]["status"] = "blocked"
        gold = "reject"
    elif kind == "escalate":
        s["amount"] = round(limit + (0.01 if r.random() < 0.2 else r.uniform(0.05, 0.9) * limit), 2)
        gold = "escalate"
    if conflict:                                             # two rules fire; the stated order decides
        k2 = r.choice(["escalate", "hold"] if kind == "reject" else ["escalate"])
        if k2 == "escalate":
            s["amount"] = round(limit + r.uniform(0.05, 0.9) * limit, 2)
        else:
            s["po_number"] = None
    return s, gold


# ------------------------------------------------------------------------------------------------ customer service
CS_DEFS = {
    "refund": "give the customer their money back",
    "replace": "send the customer a new item",
    "human_agent": "pass the case to a human agent",
    "decline": "tell the customer the request cannot be granted",
}
CS_POLICY = ("Policy, applied in this order: safety or legal issues, and orders of $2,000 or more, go to a human_agent. A request "
             "made after the return window is declined. Inside the window: a damaged or wrong item is replaced if the item "
             "is in stock, otherwise refunded; an item that never arrived and that the carrier lists as lost is refunded.")
CS_Q_STATED = "Following the policy, which action should the assistant take?"
CS_Q_PLAIN = "Which action should the assistant take on this ticket?"


def cs_state(r, kind, plain=False):
    window = r.choice([14, 30, 30, 45])
    value = round(r.uniform(15, 400), 2)
    s = {"ticket_id": f"T-{r.randint(100000, 999999)}", "channel": r.choice(["chat", "email", "web form"]),
         "order": {"value_usd": value, "delivered_days_ago": r.randint(1, max(2, window - 3)), "return_window_days": window,
                   "item_in_stock": True},
         "customer": {"tier": r.choice(["standard", "standard", "gold"]), "identity_verified": True},
         "claim": {"type": "damaged_item", "photo_provided": r.random() < 0.7},
         "notes": r.choice(["customer is polite", "customer wrote in capital letters", "second contact about this order",
                            "customer mentions a bad review online", "no remarks"])}
    if kind == "replace":
        s["claim"]["type"] = r.choice(["damaged_item", "wrong_item"])
        gold = "replace"
    elif kind == "refund":
        if r.random() < 0.5:
            s["claim"]["type"] = r.choice(["damaged_item", "wrong_item"])
            s["order"]["item_in_stock"] = False
        else:
            s["claim"] = {"type": "not_received", "carrier_status": "lost"}
            s["order"]["delivered_days_ago"] = None
        gold = "refund"
    elif kind == "decline":
        s["claim"]["type"] = "changed_mind" if plain else r.choice(["changed_mind", "damaged_item"])
        s["order"]["delivered_days_ago"] = window + r.randint(3, 40)
        gold = "decline"
    else:                                                    # human_agent
        if r.random() < 0.55 or plain:
            s["claim"] = {"type": r.choice(["safety_injury", "legal_threat"]), "photo_provided": r.random() < 0.5}
            s["notes"] = r.choice(["customer says the product burned their hand", "customer mentions contacting a lawyer",
                                   "customer reports the charger overheated", "customer cites consumer-protection law"])
        else:
            s["order"]["value_usd"] = round(r.uniform(2000, 6500), 2)
        gold = "human_agent"
    return s, gold


# ------------------------------------------------------------------------------------------------ agent run
AG_DEFS = {
    "continue": "carry on with the next step as planned",
    "observe": "carry on, but flag the run for monitoring",
    "human_review": "pause and ask a person to approve the next step",
    "stop": "halt the run now",
}
AG_POLICY = ("Policy, applied in this order: stop when the budget is fully used or the same tool has failed 3 times in a row; "
             "send an irreversible action on production to human_review before it runs; observe when 1 or 2 of the last 5 events "
             "were warnings; otherwise continue.")
AG_Q_STATED = "Following the policy, what should the run do next?"
AG_Q_PLAIN = "What should the run do next?"
TOOLS = ["search_docs", "read_table", "write_file", "call_api", "run_query", "send_summary", "update_record", "fetch_page"]


def ag_state(r, kind):
    ev = []
    step = r.randint(8, 30)
    tools = r.sample(TOOLS, 5)
    for i in range(5):
        ev.append({"step": step - 5 + i, "tool": tools[i], "status": "ok"})
    used = r.randint(15, 80)
    pend = {"tool": r.choice(["write_file", "update_record", "send_summary", "run_query"]), "reversible": True,
            "environment": r.choice(["sandbox", "sandbox", "staging"])}
    if kind == "continue":
        pass
    elif kind == "observe":
        for i in r.sample(range(5), r.choice([1, 2])):
            ev[i]["status"] = "warning"
            ev[i]["detail"] = r.choice(["slow response", "retried once", "partial result", "rate limit near"])
    elif kind == "human_review":
        pend = {"tool": r.choice(["delete_records", "send_payment", "drop_table", "publish_release", "email_customers"]),
                "reversible": False, "environment": "production"}
    elif kind == "stop":
        if r.random() < 0.5:
            used = r.choice([100, 100, 104, 118])
        else:
            t = tools[0]
            for i in (2, 3, 4):
                ev[i] = {"step": step - 5 + i, "tool": t, "status": "error", "detail": r.choice(["timeout", "403 forbidden", "bad gateway"])}
    s = {"run_id": f"run-{r.randint(1000, 9999)}", "task": r.choice(["reconcile the Q3 ledger", "prepare the weekly customer digest",
                                                                  "migrate legacy records", "clean up stale accounts"]),
         "budget_used_pct": used, "last_5_events": ev, "pending_action": pend}
    return s, kind


# ------------------------------------------------------------------------------------------------ credential (yes/no)
CR_POLICY = ("Policy: treat a credential as compromised when it has not been rotated since it appeared in a public location, "
             "was used from an unrecognised country or network, or sat on a lost or stolen device without a remote wipe. "
             "Otherwise it is not compromised.")
CR_Q_STATED = "Following the policy, should this credential be treated as compromised?"
CR_Q_PLAIN = "Should this credential be treated as compromised?"
CR_CARD = "- Yes: it must be rotated and treated as exposed\n- No: no sign it is exposed, or the exposure has already been fixed"
BENIGN = ["two failed logins from the owner's usual laptop (typo)", "a secret scanner flagged a string that is a documented test token",
          "the key was used by the nightly job from the usual data-centre network", "the owner logged in from the usual office network",
          "an internal wiki page mentions the key name but not its value", "the credential was shared in a private channel of the owning team"]
ALARM_BENIGN = ["alert titled 'possible leak' closed as a duplicate of a rotated key", "security scan reported 5 findings, all in other repositories",
                "owner is travelling but logs in from the registered VPN"]


def cr_state(r, kind):
    s = {"credential": {"type": r.choice(["API key", "SSH key", "database password", "session token"]),
                        "owner": r.choice(["billing-service", "data-pipeline", "mobile-app", "support-tools"])},
         "events": [], "rotated_since_events": False}
    if kind == "yes":
        mode = r.choice(["public", "country", "device"])
        if mode == "public":
            s["events"].append({"day": -r.randint(1, 20), "type": r.choice(["value found in a public code repository", "value posted in a public paste"])})
        elif mode == "country":
            s["events"].append({"day": -r.randint(1, 5), "type": "used from a country the owner has never logged in from", "mfa": "bypassed"})
        else:
            s["events"].append({"day": -r.randint(1, 10), "type": "laptop holding the key reported stolen", "remote_wipe": "not done"})
        if r.random() < 0.5:
            s["events"].append({"day": -r.randint(0, 30), "type": r.choice(BENIGN + ALARM_BENIGN)})
    else:
        mode = r.choice(["benign", "rotated", "alarm_benign"])
        if mode == "rotated":
            s["events"].append({"day": -r.randint(5, 40), "type": r.choice(["value found in a public code repository", "used from a country the owner has never logged in from"])})
            s["rotated_since_events"] = True
        elif mode == "alarm_benign":
            s["events"].append({"day": -r.randint(1, 20), "type": r.choice(ALARM_BENIGN)})
            s["events"].append({"day": -r.randint(1, 20), "type": r.choice(BENIGN)})
        else:
            for t in r.sample(BENIGN, 2):
                s["events"].append({"day": -r.randint(1, 30), "type": t})
    r.shuffle(s["events"])
    return s, "yes" if kind == "yes" else "no"


# ------------------------------------------------------------------------------------------------ Arabic arm
# Same scenarios as the English "stated" arm with Arabic policy / question / definitions / free-text values. JSON keys and the
# option labels stay English (as in a product whose labels are system codes). Written by Claude; diagnostic only.
AR_TEXT = {
    # vendors
    "Northfield Supply": "شركة الشمال للتوريدات", "Aldermoor Logistics": "ألدرمور للخدمات اللوجستية", "Pinecrest Print": "بينكريست للطباعة",
    "Bluewater Catering": "بلو ووتر للتموين", "Harlan Tools": "هارلان للأدوات", "Merrow Cleaning": "ميرو للتنظيف",
    "Kestrel IT Services": "كيستريل لخدمات تقنية المعلومات", "Tamsin Packaging": "تامسين للتغليف", "Orchard Lane Foods": "أورتشارد لين للأغذية",
    "Redgate Courier": "ريدغيت للشحن", "Linden Stationery": "ليندن للقرطاسية", "Quarry Hill Hardware": "كواري هيل للمعدات",
    "Saltmarsh Marine": "سولتمارش للخدمات البحرية", "Wexcombe Office Furniture": "ويكسكومب لأثاث المكاتب",
    # invoice notes
    "vendor asked for rush processing": "طلب المورّد معالجة عاجلة", "first invoice from this vendor this quarter": "أول فاتورة من هذا المورّد في هذا الربع",
    "amount is a round number": "المبلغ رقم مستدير", "payment terms are net 30": "شروط الدفع صافي 30 يوماً",
    "contact person changed last month": "تغيّر جهة الاتصال الشهر الماضي", "sent from the vendor's usual address": "أُرسلت من عنوان المورّد المعتاد",
    "no remarks": "لا توجد ملاحظات", "same amount and PO as the earlier invoice": "نفس المبلغ ونفس أمر الشراء كالفاتورة السابقة",
    # agent
    "reconcile the Q3 ledger": "مطابقة دفتر الأستاذ للربع الثالث", "prepare the weekly customer digest": "إعداد النشرة الأسبوعية للعملاء",
    "migrate legacy records": "ترحيل السجلات القديمة", "clean up stale accounts": "تنظيف الحسابات الخاملة",
    "slow response": "استجابة بطيئة", "retried once": "أُعيدت المحاولة مرة واحدة", "partial result": "نتيجة جزئية", "rate limit near": "اقتراب من حدّ الطلبات",
    "timeout": "انتهاء المهلة", "403 forbidden": "403 ممنوع", "bad gateway": "بوابة سيئة",
}
INV_POLICY_AR = ("السياسة، وتُطبَّق بهذا الترتيب (أول قاعدة تنطبق هي التي تحسم): ارفض الفاتورة إذا كانت مكررة لفاتورة سابقة أو من مورّد محظور؛ "
                 "علّق الفاتورة إذا لم يكن لها رقم أمر شراء أو كان الرقم الضريبي مفقوداً؛ صعّد الفاتورة إذا تجاوزت حدّ المعتمِد؛ وفيما عدا ذلك ادفعها.")
INV_Q_AR = "وفقاً للسياسة، ماذا يجب أن يحدث لهذه الفاتورة؟"
INV_DEFS_AR = {"pay": "صرف المبلغ الآن", "hold": "إيقاف الفاتورة مؤقتاً حتى تصل المعلومات الناقصة", "reject": "رفض دفع هذه الفاتورة",
               "escalate": "إحالتها إلى معتمِد أعلى ليقرر"}
AG_POLICY_AR = ("السياسة، وتُطبَّق بهذا الترتيب: أوقف التشغيل (stop) عندما تُستنفد الميزانية بالكامل أو تفشل الأداة نفسها 3 مرات متتالية؛ "
                "أرسل أي إجراء لا يمكن التراجع عنه على بيئة الإنتاج إلى human_review قبل تنفيذه؛ استخدم observe عندما تكون حادثة أو حادثتان من آخر 5 أحداث تحذيرات؛ "
                "وفيما عدا ذلك تابع (continue).")
AG_Q_AR = "وفقاً للسياسة، ما الذي يجب أن يفعله التشغيل الآن؟"
AG_DEFS_AR = {"continue": "المتابعة بالخطوة التالية كما هو مخطط", "observe": "المتابعة مع وسم التشغيل للمراقبة",
              "human_review": "التوقف وطلب موافقة شخص على الخطوة التالية", "stop": "إيقاف التشغيل فوراً"}


def to_ar(obj):
    if isinstance(obj, dict):
        return {k: to_ar(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_ar(v) for v in obj]
    if isinstance(obj, str):
        return AR_TEXT.get(obj, obj)
    return obj


# ------------------------------------------------------------------------------------------------ assembly
def card(defs, labels):
    return "\n".join(f"- {l}: {defs[l]}" for l in labels)


def make_rows():
    rows, key = [], {}
    r0 = random.Random(SEED)
    spec = [
        ("invoice", ["pay", "hold", "reject", "escalate"], INV_DEFS, INV_POLICY, INV_Q_STATED, INV_Q_PLAIN),
        ("support", ["refund", "replace", "human_agent", "decline"], CS_DEFS, CS_POLICY, CS_Q_STATED, CS_Q_PLAIN),
        ("agent_run", ["continue", "observe", "human_review", "stop"], AG_DEFS, AG_POLICY, AG_Q_STATED, AG_Q_PLAIN),
    ]
    N = 16
    for wf, labels, defs, pol, qs, qp in spec:
        for variant in ("stated", "plain"):
            for k, kind in enumerate(labels):
                for n in range(N):
                    r = random.Random(f"{SEED}|{wf}|{kind}|{n}")          # same scenario in every arm of the variant pair
                    conflict = (wf == "invoice" and variant == "stated" and kind in ("reject", "hold") and n % 5 == 0)
                    if wf == "invoice":
                        st, gold = inv_state(r, kind, conflict)
                    elif wf == "support":
                        st, gold = cs_state(r, kind, plain=(variant == "plain"))
                    else:
                        st, gold = ag_state(r, kind)
                    for arm in (("defs", "nodefs", "ardefs", "arstate") if (variant == "stated" and wf in ("invoice", "agent_run")) else ("defs", "nodefs")):
                        rid_ = f"jb3_{wf}_{variant}_{arm}_{kind}_{n:02d}"
                        order = labels[:]
                        random.Random(f"ord|{rid_[:-3]}|{n}").shuffle(order)    # label-blind display order (shared across arm)
                        ins = (pol + "\n\n" + qs) if variant == "stated" else qp
                        stx, dfx = st, defs
                        if arm == "ardefs":
                            ins = (INV_POLICY_AR + "\n\n" + INV_Q_AR) if wf == "invoice" else (AG_POLICY_AR + "\n\n" + AG_Q_AR)
                            stx, dfx = to_ar(st), (INV_DEFS_AR if wf == "invoice" else AG_DEFS_AR)
                        if arm == "arstate":                       # A58 (d) convention: English instructions and definitions, Arabic content
                            stx = to_ar(st)
                        row = {"id": rid_, "group_id": f"jb3_g_{wf}_{variant}_{kind}_{n:02d}", "call_id": f"jb3_c_{wf}_{variant}_{arm}_{kind}_{n:02d}",
                               "source": "jb3_probe", "state": j(stx), "qtype": "choice", "instructions": ins, "options": order,
                               "role": "probe", "meta": {"wf": wf, "variant": variant, "arm": arm}}
                        if arm in ("defs", "ardefs", "arstate"):
                            row["card"] = card(dfx, labels)
                        rows.append(row)
                        key[rid_] = {"gold": gold, "wf": wf, "variant": variant, "arm": arm, "kind": kind, "conflict": conflict,
                                     "qtype": "choice", "n_opts": len(labels)}
    # credential yes/no
    for variant in ("stated", "plain"):
        for kind in ("yes", "no"):
            for n in range(40):
                r = random.Random(f"{SEED}|cred|{kind}|{n}")
                st, gold = cr_state(r, kind)
                for arm in ("defs", "nodefs"):
                    rid_ = f"jb3_cred_{variant}_{arm}_{kind}_{n:02d}"
                    ins = (CR_POLICY + "\n\n" + CR_Q_STATED) if variant == "stated" else CR_Q_PLAIN
                    row = {"id": rid_, "group_id": f"jb3_g_cred_{variant}_{kind}_{n:02d}", "call_id": f"jb3_c_cred_{variant}_{arm}_{kind}_{n:02d}",
                           "source": "jb3_probe", "state": j(st), "qtype": "noul", "instructions": ins, "options": None,
                           "role": "probe", "meta": {"wf": "cred", "variant": variant, "arm": arm}}
                    if arm == "defs":
                        row["card"] = CR_CARD
                    rows.append(row)
                    key[rid_] = {"gold": gold, "wf": "cred", "variant": variant, "arm": arm, "kind": kind, "conflict": False,
                                 "qtype": "noul", "n_opts": 2}
    return rows, key


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    rows, key = make_rows()
    with open(OUT / "shard_000.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    json.dump(key, open(OUT / "key.json", "w"), indent=0)
    import collections
    print(len(rows), collections.Counter((k["wf"], k["variant"], k["arm"]) for k in key.values()))
