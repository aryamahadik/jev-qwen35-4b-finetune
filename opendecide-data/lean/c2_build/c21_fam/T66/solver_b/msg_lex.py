"""Message side of the MSG head: which kind of change does a commit message describe?

The kinds are the registered change kinds of the G0-lite (section 2.3): CH-1 add guard, CH-2 fix off-by-one, CH-3 rename symbol, CH-4 extract helper,
CH-5 change default, CH-6 add parameter, CH-7 remove dead branch, CH-8 change message text, CH-9 add logging call, CH-10 change constant, and the three TRIVIAL kinds
(formatting, comment, docstring). A message is scored against a closed cue table (regular expressions over lower-cased words; weights 1-5); the table is a Python
constant written from the kind names and ordinary developer vocabulary. It reads nothing at run time and has no access to any wording pool."""
import re

TRIV = ("TRIV-fmt", "TRIV-comment", "TRIV-doc")
KINDS = ("CH-1", "CH-2", "CH-3", "CH-4", "CH-5", "CH-6", "CH-7", "CH-8", "CH-9", "CH-10") + TRIV

_RAW = [
    # CH-1 add guard: a new check that rejects invalid input (raise / fail early)
    ("CH-1", 5, r"\bguard"), ("CH-1", 5, r"\bvalidat"), ("CH-1", 5, r"\bassert(s|ed|ion)?\b|\benforce"), ("CH-1", 4, r"\breject"),
    ("CH-1", 4, r"\braises? (a |an |the )?(\w+error|exception|error|valueerror)|\braising (a |an )?(\w+error|exception)|\braising if|\braise otherwise|\braises? (if|when|on)\b"),
    ("CH-1", 4, r"\bthrows? "), ("CH-1", 4, r"\brefus"), ("CH-1", 4, r"\bturn(s|ing|ed)? .{0,8}away|\bhead(s|ed|ing)? off|\bbail"),
    ("CH-1", 4, r"\bprecondition|\bsanity|\bdefensive|\bearly[- ](exit|return|check)|\bfail(s|ing|ed)? (fast|early|before|loudly|hard)|\bor fails\b|\bfails? fast|\bfailing fast"),
    ("CH-1", 4, r"\bvalid\b|\bnon-?empty|\bnon-?null|\bnot none|\bis none\b|\bmust (be|not)\b|\bnone is passed|\bwhen \w+ is (none|missing|empty)|\bout[- ]of[- ]range"),
    ("CH-1", 3, r"\bprevent|\bdisallow|\bforbid|\bblock(s|ing|ed)?\b|\bprotect|\bcatch(es)? .{0,14}\b(bad|invalid|malformed)|\bearly\b|\bkeeps? .{0,30}\bfrom\b|\bstops? .{0,40}\b(from|reaching|slipping)|\bslipping (past|through)|\bbefore any work|\bno longer (accepts|lets|allows)"),
    ("CH-1", 3, r"\binput check|\bchecks? (for|that|the input|if)|\bensure|\bmake sure .{0,40}(valid|non|not|never)|\bsafety"),
    ("CH-1", 2, r"\bsilent(ly)?|\binvalid|\bmalformed|\bbad (input|value|argument|data)|\bbad\b|\bjunk|\bnegative|\bnonsense|\bunusable|\boff-spec|\billegal|\bgarbage"),
    ("CH-1", 6, r"\bnow an? (clear |proper |real |explicit )?(error|exception)|\binstead of (a )?(wrong|silent|bad)|\bnot a wrong answer"), ("CH-1", 3, r"\bcrash(es|ing)?\b|\bblow(s)? up"), ("CH-1", 1, r"\bcheck(s|ed|ing)?\b|\bnull\b|\bnone\b|\bempty\b|\bmissing\b|\braises?\b|\bthrows?\b|\berror\b"),
    # CH-2 fix off-by-one
    ("CH-2", 7, r"off[- ]?by[- ]?one|\bfence[- ]?post|\bone[- ]off|\bone (\w+ )?short\b|\bshort by one|\bstopped short|\bone step (past|short)|\bruns? .{0,12}past the end"),
    ("CH-2", 5, r"\binclusive|\bexclusive|\bboundar|\bend(point| index)|\bupper bound|\bindex bounds?|\brange end|\bcount matches|\bless[- ]than|\bgreater[- ]than|\bless[- ]or[- ]equal|\bgreater[- ]or[- ]equal|<=|>=|\bstrict(ly)? (less|greater|smaller|larger)|\bcomparison"),
    ("CH-2", 4, r"\bthe (last|final|newest)\b|\b(last|final) (item|element|entry|row|record|one)\b|\btrailing\b|\bedge (case|item|element|row)s?\b|\bone (more|fewer|less|too)|\bextra (item|iteration|element)|\bskips? the (last|final)|\bdropp?(ed|ing)? (the )?(last|final|trailing|item|element|row|entry)|\bmiss(es|ed|ing)? the (last|final)|\bleft out|\bleaving out|\bwere missing from|\bpast the end|\bcount the\b|\blost\b|\bat the end\b|\bthe end\b"),
    ("CH-2", 5, r"\bupper (limit|bound)|\blower (limit|bound)|\bloop (limit|bound|end|range)|\bstop (value|index)"), ("CH-2", 7, r"\bfrom [01] instead of [01]|\bzero-based|\bone-based|\binstead of (0|zero)\b|\bstarts? (at|from) (0|1|zero|one)"), ("CH-2", 3, r"\bbounds?\b|\bloop"),
    ("CH-2", 2, r"\biterat|\brange\b|\bindex|\bcount(s|ed)? (is|was|one)|\bevery \w+ (gets|is|are)|\bcovers?\b|\bincludes?\b|\bvisited"),
    # CH-3 rename symbol
    ("CH-3", 7, r"\brenam"), ("CH-3", 5, r"\b(new|clearer|better|sensible|descriptive|proper|accurate|clean|nicer|shorter|fresh|telling|meaningful|readable|friendlier|consistent|helpful) (name|identifier|naming)|\bnaming|\bre-?label|\bre-?title|\bwas called|\bnow called|\bnow named|\bformerly|\bswapped for a (clearer|better)"),
    ("CH-3", 3, r"\bname\b|\bnames\b|\bnamed\b|\bcalled\b|\balias|\bidentifier|\bsymbol|\bvocabulary"),
    # CH-4 extract helper (registered, never realised by the generator; kept for completeness)
    ("CH-4", 7, r"\bextract|\bfactor out|\bsplit out|\bpull(s|ed)? (out|into)|\bmove(s|d)? .{0,25}into (a )?(new |separate )?(function|helper)"), ("CH-4", 2, r"\bhelpers?\b"),
    # CH-5 change default
    ("CH-5", 6, r"\bdefault"), ("CH-5", 4, r"\bby default\b|\bnew default\b|\bdefaults? to\b|\bdefaulting\b"), ("CH-5", 4, r"\bwhen omitted|\bif (omitted|unspecified|not (given|passed|provided|supplied))|\bwhen (it is |they are |callers? )?(not|n't) (passed|given|provided|supplied)|\bskip(s|ped)? (the |a |an )?(\{?\w+\}?)? ?(argument|arg|param|parameter|value)|\bnever pass|\bwhen they (skip|omit|leave out)|\bunspecified|\bfall(s|ing)? back|\bnone is passed|\bwhen none|\bunless (told|specified|asked)|\bout of the box|\bbaseline|\bomit"),
    ("CH-5", 5, r"\b(isn't|is not|aren't|wasn't|never|not) (given|passed|provided|supplied|set)( explicitly)?\b|\bunset\b|\bleft (unset|blank|out)\b"), ("CH-5", 7, r"\bno longer needs?\b.{0,30}\b(passed|given|supplied|provided|pass)"), ("CH-5", 3, r"\bassumes?\b|\bstarting (value|size|point|level|state)|\bstarts? (more|out)|\bflip|\bswitch(es|ed)? (to|from)|\bopt-?(in|out)"),
    # CH-6 add parameter / parameter list
    ("CH-6", 4, r"\bparam|\bsignature|\bkeyword"), ("CH-6", 4, r"\bhidden global|\bimplicit|\bglobal state|\bambient"), ("CH-6", 2, r"\bargs?\b|\barguments?\b"), ("CH-6", 3, r"\brequir"),
    ("CH-6", 5, r"\bmandatory|\bexplicit|\bspelled out|\bmust (pass|supply|provide|be passed)|\bno longer optional|\bextra (arg|param|input)|\bnew (arg|param|input)|\bcallers? (must|need|have to|now|supply|pass|provide)|\bthreaded through|\bpassed in\b|\bas (an )?input|\bfrom the caller|\bin the call"),
    ("CH-6", 5, r"\b(demands?|insists?|asks? for|wants|needs|expects|accepts|takes|gains) (now )?(a|an|the|one|another|its|it|that)? ?(\w+ )?(value|argument|arg|param|parameter|input|flag|option|setting)|\bnow (demands|insists on|wants|asks for|needs|expects|accepts|takes) (a|an|the|one|another|its|it|that|each|every)\b|\binsists? on|\basks? for (it|that|this|them)\b"),
    ("CH-6", 2, r"\bgains?\b|\baccepts?\b|\bwants?\b|\basks? for|\btakes?\b|\bneeds?\b|\bexpects?\b|\bpass(es|ed|ing)?\b|\bsupply|\bprovide|\breceiv"),
    # CH-7 remove dead branch (registered, never realised)
    ("CH-7", 7, r"\bdead (code|branch)|\bunreachable|\bunused branch|\bremove (the )?(dead|unused|obsolete|redundant) |\bdrop(s|ped)? (the )?(dead|unused|obsolete)"),
    # CH-8 change message text
    ("CH-8", 7, r"\b(error|exception|failure|warning)[- ](message|string|text|wording|msg)|\bmessage text|\bmsg\b|\bwording|\breword|\brephras|\bphrasing|\bmessage (says|reads|now|about|shown|for|on)|\b(error|message|text)\b.{0,40}\b(reads?|says?|natural|plain|sentence|readable|friendlier|clearer|helpful|spells?|words?)"),
    ("CH-8", 6, r"\berrors?\b.{0,40}\b(readable|clear|clearer|friendly|helpful|understandable|useful)|\b(readable|clearer|friendlier) errors?|\bexplain(s|ed)? .{0,25}error|\berror (now |also )?(quotes|includes|shows|names|mentions|says|tells)|\binstead of a stack ?trace|\bpoints? (people|users) at|\btells? (people|users)"), ("CH-8", 5, r"\b(clearer|better|friendlier|helpful|more helpful|clear|descriptive|nicer|readable|plain|full) (error|hint|message|wording|text|sentence|english)|\bexplains itself|\bhint\b|\bwhat went wrong|\bconfused (reports|users)|\bmore (helpful|useful) (error|message)|\bcryptic (error|message|text|wording)|\bplain english|\bfull sentence|\bknow the fix|\bwhat was expected|\bsupport (queues|tickets)|\bnon-technical|\bhuman[- ](readable|friendly)|\bwords it\b"),
    ("CH-8", 2, r"\bmessage\b|\btext\b|\bstring\b|\bcopy\b|\btypo|\bsays\b|\breports? .{0,30}\bwith\b|\bmentions?\b|\bnames the\b|\bexplains?\b|\bwords?\b|\bproblem\b|\bcryptic\b"),
    # CH-9 add logging call
    ("CH-9", 7, r"\blogs?\b|\blogg(ed|ing|er)\b|\bprint"), ("CH-9", 5, r"\btrac(e|es|ing)\b|\btraced\b(?! (to|back))|\btelemetry|\baudit|\bdiagnostic|\bdebug(ging)? (output|line|log|info|print|message|statement)s?|\binstrument|\bobservab|\bmetrics?\b|\btracking\b|\bmonitor"),
    ("CH-9", 5, r"\bleaves? a trail|\baudit trail|\bpaper trail"), ("CH-9", 2, r"\bdebug|\bnoise|\bverbos|\bquiet"), ("CH-9", 7, r"\bemits? an? (warning|message|log|line|notice)|\bwarn(s|ing)? (when|if|about)\b"), ("CH-9", 4, r"\bat run ?time\b|\bknowing\b|\bhelps? (when|diagnos|debug|us)|\bruns? slow|\bslow\b"), ("CH-9", 3, r"\bemits?\b|\brecords?\b|\bbreadcrumb|\btrail|\bvisibility|\bstdout|\bdump|\boutput|\bsee what (happened|is|was)|\bto see\b|\bvisible|\bnote(s|d)? (down|when|what)|\bwhat happened|\boperators? need|\bcounts? how many|\bwrites? (a |the )?(line|note|entry)"),
    # CH-10 change constant
    ("CH-10", 7, r"\bconstant|\bmultiplier|\bfactor\b|\bcoefficient|\bscal(e|es|ed|ing)\b|\bmagic number|\bmultiplies|\bmultiplied"),
    ("CH-10", 5, r"\bthreshold|\bceiling|\bmaximum|\bminimum|\bquota|\ballows? (fewer|more)|\btighten|\bloosen|\bfrom [\d.]+ to [\d.]+|\bfrom \w+ to \w+ (seconds|ms|items|retries)|\b(raises?|lowers?|raised|lowered|increases?|decreases?|reduces?|bumps?) .{0,30}\b(limit|cap|threshold|ceiling|value|number|figure|factor)"),
    ("CH-10", 2, r"\btun(e|es|ed|ing)\b"), ("CH-10", 5, r"\bup to \d+|\binstead of \d+|\bat \d+ (instead|rather)|\bcaps?\b|\bcapped\b|\bwaits? (less|more|longer|shorter)|\bgiving up\b|\bconcurrency\b|\b(from|to) \d+\b"), ("CH-10", 3, r"\blimits?\b|\bcap\b"), ("CH-10", 4, r"\btweak|\bbump|\bretun|\bhogging|\btighter|\blooser|\bfewer (retries|attempts)|\bretries|\btimeout|\bbudget|\bbatch size"),
    ("CH-10", 3, r"\b(bigger|smaller|larger|longer|shorter|higher|lower|lighter|heavier|stricter|relaxed|generous|more patient|more confidence|fewer|more)\b|\bincreas|\bdecreas|\badjust|\bshrink|\bnumber\b|\bfigure\b|\bsize\b"),
    ("CH-10", 1, r"\b\d+(\.\d+)?\b|\bvalue\b"),
    # trivial kinds
    ("TRIV-fmt", 7, r"\breformat|\bformatting|\bwhitespace|\bwhite space|\bspacing|\bindent|\bcosmetic|\bpep ?-?8|\blint|\blayout|\bprettif|\bline (length|wrap|break)s?|\bwrap(s|ped|ping)?\b|\balign (the |all )?(columns|args|arguments|imports|equals|values|text|code|lines)|\bcolumns? lines? up|\balign(s|ed|ing)? .{0,30}(across|over) (several |multiple )?lines|\bacross lines|\brealign|\breflow|\bblank lines?|\bbeautif|\bcode style|\bstyle (only|fix|cleanup|tweak)|\bformat(s|ted)?\b|\bone per line|\bper line|\bread top to bottom|\bsort(s|ed)? (the )?imports|\bimport order|\bcolumns?\b"),
    ("TRIV-fmt", 3, r"\balign|\blines? up\b"), ("TRIV-fmt", 4, r"\bspaces?\b|\bsplit .{0,25}(across|over) (several |multiple )?lines|\bnewline|\bline break|\btabs?\b"),
    ("TRIV-fmt", 3, r"\btidy|\btidies|\bclean(s|ed)? ?up\b|\bneaten|\bnicer to read|\breadab|\bstyle\b"),
    ("TRIV-comment", 7, r"\bcomments?\b|\bcommented\b|\bcommenting|\btodo\b|\bfixme"), ("TRIV-comment", 5, r"\binline note|\bannotat|\bremark|\bleave a note|\bjustif"),
    ("TRIV-comment", 5, r"\bspell(s|ed)? out the (reason|why)|\bexplain(s|ing)? (why|the reason)"), ("TRIV-comment", 3, r"\bnotes?\b"), ("TRIV-doc", 7, r"\bdocstrings?\b"), ("TRIV-doc", 5, r"\bdocument(ation|ed|s|ing)?\b|\bdocs\b|\breadme|\bapi docs"),
]
CUES = list(_RAW)



def _clean(text, identifiers):
    low = re.sub(r"stack ?trace", " ", text.lower())
    if identifiers:
        ids = sorted({i.lower() for i in identifiers if len(i) >= 3}, key=len, reverse=True)
        if ids:
            low = re.sub(r"(?<![a-z0-9_])(" + "|".join(re.escape(i) for i in ids) + r")(?![a-z0-9_])", " ", low)
    return low


def scores(text, identifiers=()):
    """-> {kind: score}. Every cue that matches adds its weight once (a cue is a regular expression with alternatives; each cue row counts once)."""
    low = _clean(text, identifiers)
    out = dict((k, 0) for k in KINDS)
    for kind, w, rx in CUES:
        if re.search(rx, low):
            out[kind] += w
    # combos that change reading: "default" together with removal / requirement words means the parameter list changed, not the default value
    if re.search(r"\bdefault", low) and re.search(r"\b(remov|drop|delet|without|no longer|requir|mandatory|explicit|spelled out)", low):
        out["CH-6"] += 6
        out["CH-5"] = max(0, out["CH-5"] - 6)
    if re.search(r"\bdefault", low) and out["CH-5"] > 0:
        out["CH-10"] = min(out["CH-10"], 2)                      # numbers and "tuned/limit" words inside a default-value message do not make it a constant change
    if re.search(r"\bno default\b|\bnot? (a )?default\b|\bdefault.{0,20}(removed|dropped|gone)", low):
        out["CH-6"] += 6
        out["CH-5"] = max(0, out["CH-5"] - 6)
    # wording of a comment / TODO / docstring is a trivial edit, not an error-message change
    if re.search(r"\b(reword\w*|rephras\w*|wording|text|phrasing)\b.{0,25}\b(comment|todo|note|docstring)|\b(comment|todo|docstring)\b.{0,25}\b(wording|text|phrasing)", low):
        out["CH-8"] = max(0, out["CH-8"] - 12)
        out["TRIV-doc" if "docstring" in low else "TRIV-comment"] += 6
    # a docstring or comment is named: the edit is trivial whatever else the sentence mentions
    if re.search(r"\bdocstrings?\b", low):
        out["TRIV-doc"] += 4
    if re.search(r"\bcomments?\b|\btodo\b", low):
        out["TRIV-comment"] += 4
    # "raises/lowers its limit" is a constant, not a guard
    if re.search(r"\b(raises?|lowers?|raised|lowered)\b.{0,30}\b(limit|cap|threshold|ceiling)", low):
        out["CH-1"] = max(0, out["CH-1"] - 4)
    # a "docstring" or "comment" word dominates a bare "describe/explain" reading
    return out


# Decision thresholds: the top kind must score at least MIN_TOP and lead the runner-up by at least MIN_MARGIN, else the message is "not decisive" and B abstains.
# Strict on purpose (abstain rather than guess); fixed after the three stand-in pools had been looked at, so the numbers on them are not clean estimates.
MIN_TOP = 5
MIN_MARGIN = 4


def classify(text, identifiers=(), min_top=None, min_margin=None):
    """-> (kind or None, scores). None = the message is not decisively one kind (the caller abstains)."""
    min_top = MIN_TOP if min_top is None else min_top
    min_margin = MIN_MARGIN if min_margin is None else min_margin
    sc = scores(text, identifiers)
    order = sorted(sc.items(), key=lambda kv: (-kv[1], kv[0]))
    (k1, s1), (k2, s2) = order[0], order[1]
    if s1 < min_top or s1 - s2 < min_margin:
        return None, sc
    return k1, sc
