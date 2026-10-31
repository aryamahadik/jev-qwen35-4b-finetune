"""GEN row builder (IN MEMORY ONLY). Turns items from the sub-block modules into candidate rows.

This module never writes a file. `Builder.units(...)` is a generator of candidate rows used by unit tests and by the
20-example dry run. A real row job is a later step: it must pass c21_infra/row_start_guard.py first, use non-provisional
names (namespace.py kinds added by L-0) and a non-test wording pool; `Builder(mode="rows")` refuses otherwise.

Row fields: see SCHEMA.md.
"""
import collections
import math
import re

import adversary as ADV
import blocks as B
import heuristics as H
from gen_common import (BINARY_FORMS, BIN_NAMES, BIN_SHARE_TARGET, DEV_DOMAINS, DEV_WORDING_GROUP, FORMS, LETTERS, N_WORDING_GROUPS,
                        TABLE_CARRIERS, TEXT_CARRIERS, TRAIN_DOMAINS, Balancer, GenAllow, ProvisionalNamesError, RowNamer, WordingPool,
                        approx_tokens, canon_json, check_pool, decision_spans_of, k_of, make_rng, refuse_provisional_for_rows, seed_int,
                        sha256_text, slot_check, sub_block_of, verify_provenance, word_count)

SCHEMA_VERSION = "gen-row-1"
TRAP_CAP = 0.345         # builder keeps every trap type below this share of a form's wrong slots (gate bar is 35 percent)
TRAP_MIN_SAMPLE = 45
WORDING_BAR = 0.02
HARD_TOKEN_CAP = 1536
FEASIBLE_BINS = {"TB-B3": ("mid", "hard"), "AR-F3": BIN_NAMES}
HEUR_CAP = 0.265        # running accuracy of every panel heuristic (per sub-block, 4-option rows) stays below this after n >= 40
HEUR_MIN_N = 40
LEN_BUCKET = 25         # stem length bucket width in estimated tokens; class counts inside a bucket differ by at most 1 (binary and 3-way forms)
HEUR_Z = 1.7            # reject a 4-option item when the number of panel heuristics picking the correct option exceeds expected + HEUR_Z sigma
LEN_QUOTA_FORMS = tuple(f for f in FORMS if k_of(f) in (2, 3))
ADV_SKIP_FORMS = ("CA-C3", "TM-T3")        # the four options are the same four fixed words in every row: nothing for a detector to learn
VOICE_ELIGIBLE_FORMS = ("AR-F1", "AR-F2", "TM-T1", "TM-T2")
VOICE_MAX_WORDS = 60

_NUMLIKE = re.compile(r"-?\d+(?:\.\d+)?")


def operator_ids(spec):
    """The operators / mechanisms a row uses, as a sorted list of ids (metadata for the template-level gold-bug audit, A1). Pure function of the spec."""
    f = spec["form"]
    out = {f}
    if f.startswith("AR"):
        out |= {"op." + s["op"] for s in spec["steps"]}
        if "f2" in spec:
            out.add("cmp." + spec["f2"]["cmp"])
    elif f.startswith("LG"):
        if f == "LG-L3":
            out |= {"c." + c["t"] for c in spec["constraints"]}
        else:
            out |= {"rule." + r["kind"] for r in spec["rules"]}
            out |= {"head.neg" for r in spec["rules"] if not r["head"][1]}
            out.add("pred." + spec.get("pred_source", "ns"))
    elif f.startswith("CA"):
        if "fn" in spec:
            out |= {"fn." + v["kind"] for v in spec["fn"].values()}
        else:
            out.add("graph")
    elif f.startswith("TM"):
        if f == "TM-T1":
            out |= {"unit." + o["unit"] for o in spec["ops"]}
            if spec.get("month_rule"):
                out.add("month." + spec["month_rule"])
        elif f == "TM-T2":
            out.add("fmt." + spec["fmt"])
        elif f == "TM-T4":
            out.add("variant." + spec["variant"])
    else:
        q = spec["query"]
        out.add("agg." + q["agg"]["fn"])
        out |= {"op." + c["op"] for c in q["where"]}
        if q.get("join"):
            out.add("join")
        if q.get("group"):
            out.add("group")
        if len(q["where"]) > 1:
            out.add("conj." + q.get("conj", "and"))
    return sorted(out)


def norm_option(text):
    t = " ".join(text.lower().split())
    return _NUMLIKE.sub(lambda m: str(float(m.group(0))).rstrip("0").rstrip("."), t)


class Builder:
    def __init__(self, seed, pool, allow=None, provisional=True, mode="dry", deny_check=None, form_targets=None, vocab=None, adversary=None):
        if mode == "rows":
            refuse_provisional_for_rows(provisional)
            if pool.testonly:
                raise ProvisionalNamesError("a TEST-ONLY wording pool cannot be used for rows")
            probs = check_pool(pool)
            if probs:
                raise ValueError("wording pool incomplete: %s" % probs[:3])
        self.seed = str(seed)
        self.pool = pool
        self.allow = allow or GenAllow()
        self.provisional = provisional
        self.mode = mode
        self.deny_check = deny_check
        self.bal = Balancer(self.seed + "/main")
        self.trap_bal = Balancer(self.seed + "/trap")
        self.tally = collections.defaultdict(collections.Counter)    # form -> trap type -> wrong slots
        self.wrong_slots = collections.Counter()                      # form -> wrong slots
        self.word_use = collections.Counter()                         # (qkey, idx) -> rows
        self.stats = collections.Counter()
        self.counter = 0
        self.heur = collections.defaultdict(lambda: [0, 0])          # (sub_block, heuristic) -> [applicable, hits]
        self.len_counts = collections.defaultdict(collections.Counter)  # (form, bucket) -> class counts
        self.adversary = (mode == "rows") if adversary is None else bool(adversary)                  # screen 4-option candidates with the online shortcut detectors (adversary.py)
        self.adv = {}                                     # form -> ADV.Adversary
        self._warmed = set()
        self.vocab = vocab or {}                          # {domain id: [predicate phrases]} (pool_loader.predicate_vocab()); {} = nonsense stems only
        self.form_targets = dict(form_targets or {})     # form -> planned rows (train); gives the per-wording cap floor(2% * rows)

    # ---------------------------------------------------------------- choosers
    def _domain(self, split, sub):
        doms = DEV_DOMAINS if split == "dev" else TRAIN_DOMAINS
        return self.bal.pick("dom.%s.%s" % (split, sub), doms)

    def _carrier(self, sub, form):
        if sub == "TABLE":
            cs = TABLE_CARRIERS
        else:
            cs = TEXT_CARRIERS[sub]
        c = self.bal.pick("car.%s" % form, cs)
        return self.allow.check_carrier(c)

    def _bin(self, sub, form=None):
        # least-used bin relative to the target share, among the bins the form can produce
        bins = list(FEASIBLE_BINS.get(form, BIN_NAMES))
        return self.bal.pick("bin.%s" % sub, bins, weights=BIN_SHARE_TARGET)

    def _word(self, qkey, split, form=None, unit_size=1):
        ids = self.pool.dev_ids(qkey) if split == "dev" else self.pool.train_ids(qkey)
        if not ids:
            raise ValueError("no %s wordings for %s" % (split, qkey))
        tgt = self.form_targets.get(form)
        if tgt and split != "dev":
            cap = int(WORDING_BAR * tgt)
            under = [i for i in ids if self.word_use[(qkey, i)] + unit_size <= cap]
            if under:
                ids = under
            else:
                self.stats["wording_cap_unmet"] += 1
        best = min(self.word_use[(qkey, i)] for i in ids)
        cand = [i for i in ids if self.word_use[(qkey, i)] == best]
        return self.bal.rng.choice(cand)

    def _heur_ok(self, sub, texts, correct_idx, stem):
        for name, idx in H.predictions(texts, stem).items():
            n, h = self.heur[(sub, name)]
            if idx == correct_idx and n >= HEUR_MIN_N and (h + 1) / (n + 1) > HEUR_CAP:
                return False
        return True

    def _heur_commit(self, sub, texts, correct_idx, stem):
        for name, idx in H.predictions(texts, stem).items():
            c = self.heur[(sub, name)]
            c[0] += 1
            c[1] += int(idx == correct_idx)

    # ---------------------------------------------------------------- adversarial filter
    def _adv(self, form):
        a = self.adv.get(form)
        if a is None:
            a = self.adv[form] = ADV.Adversary(k_of(form))
            self._warm(form, a)
        return a

    def _warm(self, form, a):
        """Burn-in: raw candidate items (never emitted) teach the detectors what the generator gives away before the first row exists. Leaves the
        balancers exactly as they were."""
        sub = sub_block_of(form)
        blk = B.BLOCK[sub]
        snap = self.trap_bal.snapshot()
        done = 0
        for j in range(ADV.WARM_CANDIDATES * 3):
            if done >= ADV.WARM_CANDIDATES:
                break
            rng = make_rng(self.seed, "warm", form, j)
            namer = RowNamer("%s/warm/%s/%d" % (self.seed, form, j), provisional=self.provisional, deny_check=self.deny_check)
            want = rng.choice(B.WANT[form]) if form in B.WANT else None
            carrier = rng.choice(TABLE_CARRIERS if sub == "TABLE" else TEXT_CARRIERS[sub])
            tbin = rng.choice(list(FEASIBLE_BINS.get(form, BIN_NAMES)))
            item = blk.make(form, rng, namer, tbin, want, self.trap_bal, "trap." + form, carrier, vocab=None)
            if item is None or not self._validate_item(item):
                continue
            stem, _sp = blk.render(item, self.pool, 0, make_rng(self.seed, "warm", form, j, "r"), TRAIN_DOMAINS[0], carrier)
            texts = [o["text"] for o in item["options"]]
            a.add(texts, stem, [i for i, o in enumerate(item["options"]) if o["correct"]][0])
            done += 1
        self.trap_bal.restore(snap)
        a.maybe_fit(force=True)

    # ---------------------------------------------------------------- budget
    def _budget_ok(self, form, item):
        wrong = [o for o in item["options"] if not o["correct"]]
        n_after = self.wrong_slots[form] + len(wrong)
        if n_after < TRAP_MIN_SAMPLE:
            return True
        add = collections.Counter(o["trap"] for o in wrong)
        n_now = self.wrong_slots[form]
        for t in add:
            new = (self.tally[form][t] + add[t]) / n_after
            old = self.tally[form][t] / n_now if n_now else 0.0
            # reject only a candidate that pushes a type over the cap AND raises its share. (Skeptic fix 18 Oct: the old test also rejected a
            # candidate that did not touch an over-cap type, or that lowered it, so a form could freeze for good after one lucky run of a type:
            # CA-C3 on the dev split produced 14 rows out of 1,000 planned.)
            if new > TRAP_CAP and new > old + 1e-12:
                return False
        return True

    def _commit(self, form, item):
        for o in item["options"]:
            if not o["correct"]:
                self.tally[form][o["trap"]] += 1
                self.wrong_slots[form] += 1

    # ---------------------------------------------------------------- items
    def _item(self, form, split, want, target_bin, carrier, row_seed, scope_pref, prefer_bin=True, domain=None):
        sub = sub_block_of(form)
        blk = B.BLOCK[sub]
        best = None
        adv_target = self.bal.pick("advrank." + form, [0, 1, 2, 3]) if (self.adversary and k_of(form) == 4 and form not in ADV_SKIP_FORMS) else None
        for attempt in range(120):
            snap_t, snap_m = self.trap_bal.snapshot(), self.bal.snapshot()
            rng = make_rng(self.seed, row_seed, attempt)
            namer = RowNamer("%s/%s/%d" % (self.seed, row_seed, attempt), provisional=self.provisional, deny_check=self.deny_check)
            item = blk.make(form, rng, namer, target_bin, want, self.trap_bal, "trap." + form, carrier, vocab=self.vocab.get(domain))
            ok, why = item is not None, "make_none"
            if ok:
                ok, why = self._budget_ok(form, item), "budget"
            if ok and prefer_bin and attempt < 100 and blk.bin(item) != target_bin:
                ok, why = False, "bin"
            if ok and not self._validate_item(item):
                ok, why = False, "validate"
            if ok:
                stem, _sp = blk.render(item, self.pool, 0, make_rng(self.seed, row_seed, attempt, "tokprobe"), TRAIN_DOMAINS[0], carrier)
                if approx_tokens(stem) + sum(approx_tokens(o["text"]) for o in item["options"]) > HARD_TOKEN_CAP - 40:
                    ok, why = False, "tokens"
                elif k_of(form) == 4:
                    texts = [o["text"] for o in item["options"]]
                    hits, napply = H.hits_on(texts, [i for i, o in enumerate(item["options"]) if o["correct"]][0], stem)
                    if hits > math.ceil(napply / 4 + HEUR_Z * math.sqrt(napply * 3 / 16)):
                        ok, why = False, "heuristic_hits"
                    elif not self._heur_ok(sub, texts, [i for i, o in enumerate(item["options"]) if o["correct"]][0], stem):
                        ok, why = False, "heuristic_running"
                    elif self.adversary and form not in ADV_SKIP_FORMS and attempt < 110 and not self._adv(form).ok(texts, stem, [i for i, o in enumerate(item["options"]) if o["correct"]][0], adv_target):
                        ok, why = False, "adversary"
                elif form in LEN_QUOTA_FORMS and attempt < 100:
                    toks = approx_tokens(stem)
                    cls = norm_option(item["answer"] if isinstance(item["answer"], str) else str(item["answer"]))
                    cnt = self.len_counts[(form, toks // LEN_BUCKET)]
                    others = [norm_option(o["text"]) for o in item["options"]]
                    classes = set(others) if form == "LG-L1" else {norm_option(o["text"]) for o in item["options"]}
                    if cnt[cls] - min([cnt[c] for c in classes] or [0]) >= 2:
                        ok, why = False, "len_bucket"
            if not ok:
                self.trap_bal.restore(snap_t)
                self.stats["retry_" + why] += 1
                self.stats["retry_%s_%s" % (form, why)] += 1
                continue
            item["_namer"] = namer
            item["_rng_seed"] = (self.seed, row_seed, attempt)
            return item
        self.stats["item_fail"] += 1
        return None

    def _validate_item(self, item):
        texts = [norm_option(o["text"]) for o in item["options"]]
        if len(set(texts)) != len(texts):
            return False
        if sum(1 for o in item["options"] if o["correct"]) != 1:
            return False
        at = B.solve_row_spec(item["spec"])
        if at is None:
            return False
        return [norm_option(o["text"]) for o in item["options"] if o["correct"]] == [norm_option(at)]

    # ---------------------------------------------------------------- rows
    def _make_row(self, item, form, split, domain, carrier, widx, pair_id, pair_role, rid):
        sub = sub_block_of(form)
        blk = B.BLOCK[sub]
        k = k_of(form)
        rng = make_rng(self.seed, rid, "render")
        qkey = blk.qkey(item)
        stem, spans = blk.render(item, self.pool, widx, rng, domain, carrier)
        assert slot_check(stem, spans), "render map self-check failed"
        # option placement: correct option at the least-used position, others shuffled
        pos = self.bal.pick("pos." + form, list(range(k)))
        correct = [o for o in item["options"] if o["correct"]][0]
        wrong = [o for o in item["options"] if not o["correct"]]
        rng.shuffle(wrong)
        order = wrong[:pos] + [correct] + wrong[pos:]
        options = [o["text"] for o in order]
        label = pos
        namer = item["_namer"]
        voice = (form in VOICE_ELIGIBLE_FORMS and word_count(stem) <= VOICE_MAX_WORDS and carrier == "TXT-PROSE")
        row = {
            "schema": SCHEMA_VERSION, "row_id": rid, "family": "GEN", "sub_block": sub, "form": form, "k": k, "split": split,
            "domain_id": domain, "carrier": carrier,
            "stem": stem, "options": options, "label": label, "label_letter": LETTERS[label], "answer_text": correct["text"],
            "option_meta": [{"text": o["text"], "trap_type": o["trap"], "correct": o["correct"]} for o in order],
            "spec": item["spec"],
            "render_map": spans, "decision_spans": decision_spans_of(stem, spans),
            "voice_eligible": bool(voice),
            "wording": {"key": qkey, "idx": widx, "group": widx % N_WORDING_GROUPS},
            # metadata for the template-level audit (A1); `level` and `length_tier` need the difficulty ladder and the A21 padding, which are NOT BUILT
            "template_id": "%s|%s|%s" % (form, carrier, qkey), "wording_id": "%s#%d" % (qkey, widx), "operator_ids": operator_ids(item["spec"]),
            "error_model_ids": sorted({o["trap"] for o in order if o["trap"]}), "level": None, "length_tier": None,
            "pair_id": pair_id, "pair_role": pair_role,
            "difficulty": {"bin": blk.bin(item), "score": item["score"]},
            "tokens_est": approx_tokens(stem) + sum(approx_tokens(o) for o in options),
            "names": self.allow.job_names([carrier]),
            "name_provenance": [list(p) for p in namer.provenance],
            "namespace_fingerprint": namer.fingerprint(), "name_seed": namer.row_seed,
            "provisional_names": bool(namer.used_provisional),
            "weight": 1.0,                       # NO hard-bin upweight on GEN rows (plan section 2)
            "pool_sha": self.pool.sha(), "pool_testonly": self.pool.testonly,
            "seed": self.seed,
        }
        row["spec_sha"] = sha256_text(canon_json(item["spec"]))
        self.word_use[(qkey, widx)] += 1
        if k == 4:
            self._heur_commit(sub, options, label, stem)
            if self.adversary and form not in ADV_SKIP_FORMS:
                a = self._adv(form)
                a.add(options, stem, label)
                a.maybe_fit()
        elif form in LEN_QUOTA_FORMS:
            self.len_counts[(form, approx_tokens(stem) // LEN_BUCKET)][norm_option(correct["text"])] += 1
        return row

    def unit(self, form, split, index, pair_prob=0.45):
        """One unit = one row or a minimal pair. Returns a list of 1-2 rows, or [] on failure."""
        sub = sub_block_of(form)
        k = k_of(form)
        self.allow.check_form(form)
        rid = "%s-%s-%05d" % (form, split, index)
        want = None
        if form in B.WANT:
            want = self.bal.pick("want." + form, B.WANT[form])
        carrier = self._carrier(sub, form)
        target_bin = self._bin(sub, form)
        domain = self.allow.check_domain(self._domain(split, sub))
        item = self._item(form, split, want, target_bin, carrier, rid, "trap." + form, domain=domain)
        if item is None:
            return []
        blk = B.BLOCK[sub]
        qkey = blk.qkey(item)
        paired = self.bal.rng.random() < pair_prob
        widx = self._word(qkey, split, form, 2 if paired else 1)
        self._commit(form, item)
        rows = []
        pair_id = ("P-" + rid) if paired else None
        # actual bin counted for share control
        self.bal.note("binreal.%s" % sub, blk.bin(item))
        r1 = self._make_row(item, form, split, domain, carrier, widx, pair_id, "a" if paired else None, rid, )
        rows.append(r1)
        if paired:
            snap = self.trap_bal.snapshot()
            rng = make_rng(self.seed, rid, "pair")
            adv_t = self.bal.pick("advrank." + form, [0, 1, 2, 3]) if (self.adversary and k == 4 and form not in ADV_SKIP_FORMS) else None
            for _try in range(14 if adv_t is not None else 3):
                p = blk.perturb(item, rng, self.trap_bal, "trap." + form)
                if p is not None and adv_t is not None:
                    pt = [o["text"] for o in p["options"]]
                    pstem, _sp = blk.render(p, self.pool, 0, make_rng(self.seed, rid, "padv", _try), domain, carrier)
                    if not self._adv(form).ok(pt, pstem, [i for i, o in enumerate(p["options"]) if o["correct"]][0], adv_t):
                        self.trap_bal.restore(snap)
                        continue
                if p is not None and self._validate_item(p) and self._budget_ok(form, p):
                    p["_namer"] = item["_namer"]
                    self._commit(form, p)
                    r2 = self._make_row(p, form, split, domain, carrier, widx, pair_id, "b", rid + "b")
                    if r2["answer_text"] != r1["answer_text"]:
                        rows.append(r2)
                        if form in B.WANT:
                            self.bal.note("want." + form, p["answer"] if isinstance(p["answer"], str) else str(p["answer"]).lower())
                        break
                self.trap_bal.restore(snap)
            if len(rows) == 1:
                rows[0]["pair_id"] = None
                rows[0]["pair_role"] = None
                self.stats["pair_fail"] += 1
        self.counter += 1
        return rows

    def build_form(self, form, n_units, split="train", start=0):
        out = []
        for i in range(start, start + n_units):
            out.extend(self.unit(form, split, i))
        return out


def spec_names(spec):
    """Every identifier-like name stored in a spec (for the namespace-only check)."""
    out = []
    form = spec["form"]
    if form.startswith("AR"):
        out += list(spec["names"].values())
        if spec.get("count_noun"):
            out.append(spec["count_noun"])
    elif form.startswith("LG"):
        if form == "LG-L3":
            out += spec["item_names"]
        else:
            out += spec["ent_names"] + ([] if spec.get("pred_source") == "vocab" else spec["pred_names"]) + ([spec["rel_name"]] if spec.get("rel_name") else [])
    elif form.startswith("CA"):
        out += spec["var_names"]
    elif form in ("TM-T2", "TM-T3"):
        out += spec["names"]
    elif form == "TM-T4":
        out += [t["name"] for t in spec["tasks"]] if spec["variant"] == "plan" else spec["names"]
    elif form.startswith("TB"):
        for t in spec["tables"]:
            out.append(t["label"])
            out += [c["name"] for c in t["columns"]]
            for i, c in enumerate(t["columns"]):
                if c["type"] in ("name", "cat"):
                    out += sorted({r[i] for r in t["rows"]})
    return out


def validate_row(row, allow=None):
    """Row-level checks every candidate must pass (used by tests and by the gates). Returns a list of problems."""
    probs = []
    allow = allow or GenAllow()
    form = row["form"]
    try:
        allow.check_form(form)
        allow.check_domain(row["domain_id"])
        allow.check_carrier(row["carrier"])
    except Exception as e:
        probs.append("allow-list: %s" % e)
    if row["names"]["carrier"] != [row["carrier"]] or any(row["names"][c] for c in ("policy", "tool", "language", "runner")):
        probs.append("names block")
    try:                                         # G-D2: every unit of an ARITH row is on the closed UNIT-SET
        sp = row["spec"]
        for u in [b["unit"] for b in sp.get("base", [])] + [s["param"] for s in sp.get("steps", []) if s.get("op") == "conv"]:
            allow.check_unit(u)
    except Exception as e:
        probs.append("allow-list: %s" % e)
    if len(row["options"]) != row["k"]:
        probs.append("option count")
    texts = [norm_option(o) for o in row["options"]]
    if len(set(texts)) != len(texts):
        probs.append("options not pairwise distinct")
    at = B.solve_row_spec(row["spec"])
    if at is None or norm_option(at) != norm_option(row["options"][row["label"]]):
        probs.append("solver A disagrees with the label")
    if sum(1 for t in texts if t == norm_option(at or "")) != 1:
        probs.append("not exactly one correct option")
    if not slot_check(row["stem"], row["render_map"]):
        probs.append("render map")
    if row["label_letter"] != LETTERS[row["label"]]:
        probs.append("letter")
    if not verify_provenance(row["name_seed"], row["name_provenance"], provisional=row["provisional_names"]):
        probs.append("names are not reproducible from the TRAINING-salt namespace")
    pset = {p[3].lower() for p in row["name_provenance"]}
    missing = [n for n in spec_names(row["spec"]) if n.lower() not in pset]
    if missing:
        probs.append("names not from the namespace: %s" % missing[:3])
    if row["weight"] != 1.0:
        probs.append("weight != 1.0 (no hard-bin upweight on GEN)")
    if row["tokens_est"] > HARD_TOKEN_CAP:
        probs.append("token hard cap")
    return probs
