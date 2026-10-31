"""rk_vote: which option a group chooses under a stated counting rule (plurality with a stated tie-break, Borda
count, instant runoff, top-two runoff, approval), from ranked or approval ballots listed as groups
("7 members: B > A > C").  Profiles are preferred where the counting rule matters (another common rule would pick a
different winner).  Outcome: an option label, or TIE when the stated rules leave a tie (to be settled by lot).
"""
import copy
import itertools
import random

LET = "ABCDEFG"
CONTEXTS = [  # (group, voters, decision, option word, option names)
    ("the Hollybrook Allotment Society", "members", "which layout to adopt for the new community plot", "Proposal",
     ["the raised-bed layout", "the orchard corner", "the shared greenhouse", "the wildflower strip",
      "the pond area", "the tool-shed extension"]),
    ("the staff wellbeing committee", "staff members", "which activity to fund this year", "Proposal",
     ["weekly yoga sessions", "a bike-repair workshop", "a lunchtime walking club", "a cooking class series",
      "a quiet room refit", "a book exchange"]),
    ("the Maple Street residents' association", "households", "which design to use for the new playground", "Design",
     ["the treehouse design", "the water-play design", "the rope-course design", "the sensory garden",
      "the climbing-wall design", "the natural-play design"]),
    ("the Kestrel Robotics team", "engineers", "which logo to put on the new product", "Design",
     ["the hexagon logo", "the wordmark logo", "the circuit logo", "the bird logo", "the monogram logo",
      "the gradient logo"]),
    ("the student union", "voting students", "who should chair the events committee", "Candidate",
     ["Amara Okafor", "Luis Ortega", "Mei Tanaka", "Tomasz Nowak", "Grace Mensah", "Hamza Qureshi"]),
    ("the Riverside Tenants' Forum", "tenants", "who should represent them on the landlord's panel", "Candidate",
     ["Isabel Duarte", "Kwame Asante", "Nora Lindqvist", "Ravi Menon", "Chloe Martin", "Yusuf Demir"]),
    ("the Riverside Book Club", "members", "which book to read next", "Book",
     ["The Salt Cartographer", "Nine Winters in Ostrava", "The Clockmaker's Ledger", "Orchard of Glass",
      "A Lantern for Mira", "The Tidewater Letters"]),
    ("the Northfield Cycling Club", "members", "which route to use for the annual charity ride", "Route",
     ["the coastal route", "the hill route", "the lakes route", "the river route", "the forest route",
      "the city route"]),
    ("the Harbour Arts Collective", "artists", "which theme to use for the winter exhibition", "Theme",
     ["Light and Shadow", "Tides", "Found Objects", "The City at Night", "Small Worlds", "Migration"]),
    ("Year 11 at Pinewood School", "students", "which charity the summer fair should support", "Charity",
     ["the Riverbank Food Share", "Second Chance Bikes", "the Oakfield Carers' Circle", "Open Doors Literacy",
      "the Seaside Dementia Cafe", "Greenstreet Tree Planters"]),
    ("the Eastgate Housing Cooperative", "households", "which refurbishment scheme to back", "Scheme",
     ["the heat-pump scheme", "the insulation-first scheme", "the solar-roof scheme", "the window-replacement scheme",
      "the courtyard scheme", "the lift-upgrade scheme"]),
]
METHODS = ["plurality", "borda", "irv", "runoff", "approval"]


def tie_opt():
    return "tie not settled by the rules"


def firsts(ballots, alive):
    c = {x: 0 for x in alive}
    for n, rank in ballots:
        for x in rank:
            if x in alive:
                c[x] += n
                break
    return c


def borda(ballots, opts):
    m = len(opts)
    pts = {x: 0 for x in opts}
    for n, rank in ballots:
        for pos, x in enumerate(rank):
            pts[x] += n * (m - 1 - pos)
    return pts


def seconds(ballots, opts):
    c = {x: 0 for x in opts}
    for n, rank in ballots:
        if len(rank) > 1:
            c[rank[1]] += n
    return c


def pick_top(score, cands, tb=None):
    best = max(score[x] for x in cands)
    top = [x for x in cands if score[x] == best]
    if len(top) > 1 and tb is not None:
        b2 = max(tb[x] for x in top)
        top = [x for x in top if tb[x] == b2]
    return top[0] if len(top) == 1 else None


def count(item, method=None):
    """Primary evaluator; returns option key (e.g. 'A') or 'TIE'."""
    m = method or item["method"]
    opts = item["opts"]
    B = item["ballots"]
    if m == "plurality":
        w = pick_top(firsts(B, opts), opts, seconds(B, opts))
        return w or "TIE"
    if m == "borda":
        w = pick_top(borda(B, opts), opts, firsts(B, opts))
        return w or "TIE"
    if m == "approval":
        c = {x: sum(n for n, s in item["approvals"] if x in s) for x in opts}
        w = pick_top(c, opts)
        return w or "TIE"
    total = sum(n for n, _ in B)
    orig = firsts(B, opts)
    if m == "irv":
        alive = list(opts)
        while True:
            f = firsts(B, alive)
            for x in alive:
                if 2 * f[x] > total:
                    return x
            if len(alive) == 2:
                return pick_top(f, alive) or "TIE"
            low = min(f[x] for x in alive)
            losers = [x for x in alive if f[x] == low]
            if len(losers) > 1:
                lo2 = min(orig[x] for x in losers)
                losers = [x for x in losers if orig[x] == lo2]
            if len(losers) > 1:
                losers = [max(losers)]  # the later letter is eliminated
            alive.remove(losers[0])
    if m == "runoff":
        f = orig
        for x in opts:
            if 2 * f[x] > total:
                return x
        s = seconds(B, opts)
        order = sorted(opts, key=lambda x: (-f[x], -s[x]))
        if len(order) > 2 and (f[order[1]], s[order[1]]) == (f[order[2]], s[order[2]]):
            return "TIE"
        a, b = order[0], order[1]
        pa = sum(n for n, r in B if r.index(a) < r.index(b))
        pb = total - pa
        return a if pa > pb else (b if pb > pa else "TIE")
    raise ValueError(m)


def sample(rng):
    k = rng.choice([3, 3, 4, 4, 5])
    opts = list(LET[:k])
    method = rng.choices(METHODS, weights=[18, 24, 24, 18, 16])[0]
    ctx = rng.choice(CONTEXTS)
    word, scheme = ctx[3], rng.choice(["L", "N"])
    names = rng.sample(ctx[4], k)
    groups = rng.randint(3, 7)
    ballots, approvals = [], []
    perms = list(itertools.permutations(opts))
    for _ in range(groups):
        n = rng.randint(1, 12)
        ballots.append([n, list(rng.choice(perms))])
    # merge identical rankings
    merged = {}
    for n, r in ballots:
        merged[tuple(r)] = merged.get(tuple(r), 0) + n
    ballots = [[n, list(r)] for r, n in merged.items()]
    for n, r in ballots:
        cut = rng.randint(1, max(1, k - 1))
        approvals.append([n, sorted(r[:cut])])
    item = {"opts": opts, "method": method, "ballots": ballots, "approvals": approvals, "word": word,
            "scheme": scheme, "names": names, "ctx": list(ctx[:3]),
            "r": {"q": rng.randrange(1000), "rule": rng.randrange(2), "lay": rng.randrange(3)}}
    return item


def label(item, x):
    i = item["opts"].index(x)
    return f"{item['word']} {x if item['scheme'] == 'L' else i + 1}"


def gold_option(item, out):
    return tie_opt() if out == "TIE" else label(item, out)


def rule_text(item):
    m = item["method"]
    k = len(item["opts"])
    v = item["r"]["rule"]
    if m == "plurality":
        return ["Counting rule: the option with the most first preferences wins. If options tie on first preferences, "
                "the one with more second preferences wins; if still tied, lots are drawn.",
                "Only first choices count. Most first choices wins; a tie is broken by counting second choices, and if "
                "that is also tied the result goes to a draw."][v]
    if m == "borda":
        pts = ", ".join(f"{k - 1 - i} for {['1st', '2nd', '3rd', '4th', '5th'][i]}" for i in range(k))
        return [f"Counting rule (Borda count): each ballot gives {pts} place. The highest total wins; a tie is broken "
                f"by the number of first preferences, and if still tied, lots are drawn.",
                f"Borda scoring: {pts}. Add up the points; most points wins. Ties go to the option with more first "
                f"preferences, then to a draw."][v]
    if m == "irv":
        return ["Counting rule (instant runoff): count first preferences. An option with more than half of all "
                "ballots wins. Otherwise eliminate the option with the fewest first preferences and move each of its "
                "ballots to the next preference still in the count; repeat. If two options tie for fewest, eliminate "
                "the one with fewer first preferences in the original count, and if still tied, the one listed later. "
                "If the last two tie, lots are drawn.",
                "Instant runoff: an option needs a majority (more than half) of the ballots. While no option has one, "
                "drop the option with the fewest current first preferences (ties: fewer original first preferences, "
                "then the one listed later) and transfer its ballots to their next remaining choice. A final tie "
                "goes to a draw."][v]
    if m == "runoff":
        return ["Counting rule (top-two runoff): if an option has more than half of the first preferences, it wins. "
                "Otherwise the two options with the most first preferences go to a runoff (a tie for second place is "
                "settled by second preferences, then by lot), and each ballot counts for whichever of the two it ranks "
                "higher. A tied runoff is settled by lot.",
                "Two-round rule: a first-preference majority (more than half) wins outright. If there is none, keep the "
                "top two on first preferences (a tie for second is broken by second preferences, then by lot) and give "
                "each ballot to whichever of the two it prefers; a tie in that runoff goes to a draw."][v]
    return ["Counting rule (approval): each member approves any number of options; the option with the most approvals "
            "wins. A tie is settled by lot.",
            "Approval vote: count how many members approve each option. Most approvals wins; ties go to a draw."][v]


def render(item):
    org, who, what = item["ctx"]
    r = item["r"]
    total = sum(n for n, _ in item["ballots"])
    lab = {x: label(item, x) for x in item["opts"]}
    lines = [f"{org[0].upper() + org[1:]} ({total} {who}) is deciding {what}. The options are:"]
    for x, nm in zip(item["opts"], item["names"]):
        lines.append(f"- {lab[x]}: {nm}")
    lines.append("")
    lines.append(rule_text(item))
    lines.append("")
    if item["method"] == "approval":
        lines.append("Ballots (options approved):")
        for n, s in item["approvals"]:
            who1 = who if n != 1 else who.rstrip("s")
            lines.append(f"{n} {who1}: " + ", ".join(lab[x] for x in s))
    else:
        lines.append(["Ballots (most preferred first):", "Ranked ballots, grouped:", "Preference ballots:"][r["lay"]])
        for n, rank in item["ballots"]:
            who1 = who if n != 1 else who[:-1] if who.endswith("s") else who
            lines.append(f"{n} {who1}: " + " > ".join(lab[x] for x in rank))
    state = "\n".join(lines)
    q = ["Under the stated counting rule, which option wins?", "Which option is chosen when the ballots are counted "
         "exactly as the rule says?", "Applying the counting rule and its tie-break, which option does the group adopt?",
         "Which option wins the vote under these rules?"]
    ins = q[r["q"] % len(q)]
    opts = [lab[x] for x in item["opts"]] + [tie_opt()]
    return state, ins, opts


def edges(item):
    e = ["numeric", "quantifier"]
    if item["method"] in ("irv", "runoff"):
        e.append("multi_hop")
    return e


def twin(item, rng, base_out):
    cands = []
    key = "approvals" if item["method"] == "approval" else "ballots"
    for gi, (n, r) in enumerate(item[key]):
        for d in (1, -1, 2, -2, 3, -3):
            if n + d < 1:
                continue
            it2 = copy.deepcopy(item)
            it2[key][gi][0] = n + d
            if key == "ballots":
                it2["approvals"][gi][0] = n + d
            o2 = count(it2)
            if o2 != base_out:
                cands.append((it2, {"type": "count", "group": gi, "old": n, "new": n + d}, o2, 1.0 / abs(d)))
        if key == "ballots":
            for j in range(len(r) - 1):
                it2 = copy.deepcopy(item)
                rr = it2["ballots"][gi][1]
                rr[j], rr[j + 1] = rr[j + 1], rr[j]
                if any(tuple(x[1]) == tuple(rr) for k2, x in enumerate(it2["ballots"]) if k2 != gi):
                    continue
                o2 = count(it2)
                if o2 != base_out:
                    cands.append((it2, {"type": "swap", "group": gi, "pos": j}, o2, 0.8))
    if not cands:
        return None
    normal = [c for c in cands if c[2] != "TIE"]
    pool = normal if normal and rng.random() < 0.85 else cands
    it2, desc, o2, _ = rng.choices(pool, weights=[c[3] for c in pool])[0]
    return it2, desc, o2


def build(rng):
    it = sample(rng)
    out = count(it)
    others = {count(it, m) for m in ("plurality", "borda", "irv") if m != it["method"]} if it["method"] != "approval" \
        else {count(it, "plurality")}
    if others == {out} and rng.random() < 0.7:
        return None  # prefer profiles where the counting rule matters
    if out == "TIE" and rng.random() < 0.5:
        return None
    return it, out
