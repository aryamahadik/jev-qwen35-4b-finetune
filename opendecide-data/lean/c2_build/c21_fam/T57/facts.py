"""Program-rendered statement of the INTENDED behaviour (TASK_CARD facts). One plain sentence per function, built from the
behaviour atom's clauses. Wording variety of the card frame comes from the wording pool (T57-TC-FRAME); the facts
themselves are mechanical so they can never contradict the reference module."""
from LC_COMMON import ir as I


def _params(lo, fname):
    return [p[0] for p in I.functions(lo)[fname]["params"]]


def _fmt(kind, f, ps, cl, lo):
    c = cl[0]
    if kind == "tier_rate":
        _, ths, rates, op, mode = c
        a = ps[0]
        parts = ["%d when %s %s %d" % (r, a, op, t) for t, r in zip(ths, rates)]
        what = {"rate": "returns the rate", "amount": "returns %s * rate // 100" % a, "net": "returns %s - %s * rate // 100" % (a, a)}[mode]
        return "%s(%s): the rate is %s, otherwise %d; it %s." % (f, ", ".join(ps), ", ".join(parts), rates[-1], what)
    if kind == "capacity":
        return "%s(%s): capacity is %d; a request <= 0 is a value error; if nothing is left (%s >= capacity) it is a state error; otherwise it returns min(%s, capacity - %s)." % (
            f, ", ".join(ps), c[1], ps[0], ps[1], ps[0])
    if kind == "page_window":
        return "%s(%s): pages hold %d items; it returns how many of the %s items fall on page %s (0 when the page starts past the end)." % (
            f, ", ".join(ps), c[1], ps[0], ps[1])
    if kind == "retry_delay":
        _, grow, step, cap = c
        g = "doubles" if grow == "double" else "grows by %d" % step
        return "%s(%s): the delay starts at %s and %s once per attempt, never above %d." % (f, ", ".join(ps), ps[1], g, cap)
    if kind == "batch_count":
        _, size, unit, sur = c
        return "%s(%s): items go in batches of %d; each started batch costs %d, plus a surcharge of %d when the last batch is not full." % (
            f, ", ".join(ps), size, unit, sur)
    if kind == "role_match":
        _, r1, r2, t1, hi1, lo1, cap2 = c
        return "%s(%s): role '%s' gets %d when %s >= %d, else %d; role '%s' gets min(%s, %d); any other role gets 0." % (
            f, ", ".join(ps), r1, hi1, ps[1], t1, lo1, r2, ps[1], cap2)
    if kind == "fmt_label":
        _, sep, width, hi, tail = c
        return "%s(%s): the label is %s + '%s' + the code zero-padded to %d digits; a code above %d gives '%s' instead of the digits." % (
            f, ", ".join(ps), ps[1], sep, width, hi, tail)
    if kind == "unit_convert":
        return "%s(%s): multiplies %s by the factor of the unit at the given index in the table %s and divides by 10 (integer division)." % (
            f, ", ".join(ps), ps[0], c[1])
    if kind == "validate_record":
        _, lo_, hi_ = c
        return "%s(%s): 1 for an empty name, 2 for %s < %d, 3 for %s > %d, otherwise 0." % (f, ", ".join(ps), ps[0], lo_, ps[0], hi_)
    if kind == "route_follow":
        return "%s(%s): follows the next-hop table %s for the given number of steps from the start node and returns the node reached." % (
            f, ", ".join(ps), c[1])
    if kind == "sum_over":
        _, mode, op = c
        w = {"sum": "adds the item", "count": "adds 1", "weighted": "adds the item times a fixed weight"}[mode]
        return "%s(%s): over the items %s %s, %s." % (f, ", ".join(ps), "that are", "%s the limit" % ("at most" if op == "<=" else "below"), w)
    if kind == "dedupe_count":
        _, mode, k, t0 = c
        return "%s(%s): looks at each distinct value once (first occurrence) and %s." % (
            f, ", ".join(ps), {"count": "counts it", "sum": "adds it", "weighted": "adds it times %d" % k, "positive": "counts it when above %d" % t0}[mode])
    if kind == "merge_overrides":
        _, mode, cmp_op, t = c
        return "%s(%s): result item k comes from %s when %s, otherwise from %s." % (
            f, ", ".join(ps), ps[1], ("it exists and %s[k] %s %d" % (ps[1], cmp_op, t)) if mode == "override" else ("it exists and %s[k] %s %s[k]" % (ps[1], cmp_op, ps[0])), ps[0])
    if kind == "log_tally":
        _, mode, w = c
        return "%s(%s): %s." % (f, ", ".join(ps), {"count": "counts the lines that start with the prefix", "not": "counts the lines that do not start with the prefix",
                                                   "weighted": "adds %d times the length of each line that starts with the prefix" % w}[mode])
    if kind == "ledger":
        return "%s: the running total may not exceed %d (state error); a non-positive amount is a value error; a refund larger than the total is a state error." % (f, c[1])
    if kind == "queue_fifo":
        return "%s: a queue of at most %d items (%s); adding to a full queue or taking from an empty one is a state error." % (f, c[1], c[2])
    if kind == "tally_counts":
        return "%s: a tally with %d counters; counting outside them is an index error; each call adds %d to one counter." % (f, c[1], c[2])
    if kind == "retry_state":
        return "%s: the delay starts at %d and doubles on each failure up to %d; more than %d failures in a row is a state error; success resets it." % (f, c[1], c[2], c[3])
    if kind == "note_counter":
        return "%s: counts lines that start with '%s' (+%d) separately from other lines (+%d)." % (f, c[1], c[2], c[3])
    if kind == "wrapper":
        return "%s(%s): applies %s to the result of %s." % (f, ", ".join(ps), c[2], c[1])
    return "%s: see the code." % f


def facts_for(lo, fnames):
    """Fact lines for the named functions of module `lo` (an intended-behaviour statement; the buggy code is shown apart)."""
    specs = lo["meta"]["fns"]
    lines = []
    for n in fnames:
        sp = specs.get(n)
        if not sp:
            continue
        lines.append(_fmt(sp["atom"], n, _params(lo, n), sp["clauses"], lo))
    return lines
