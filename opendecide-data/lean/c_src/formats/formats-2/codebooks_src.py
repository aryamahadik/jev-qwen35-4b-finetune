"""Real-text codebooks for spec 2.3 (F10 S7 and F11 S7). Claude-written seeds (CC0); every code is an explicit function
of the dataset's released human annotation vector (never of Claude reading the text).

F10 codebooks (G0 F10 3 S7): first fit in card order, residual last ("none of the other codes on this card fits"),
5-9 codes or 20-30 codes, flat conditions only (one literal, or one ALL / ANY list of literals; a literal is an atom or
NOT atom). Natural names are given here; masked IDs and swapped names are the builder's.
F11 codebooks (G0 F11 S7): codes are unions of FULL annotation combinations (SEM-46), 10-30 codes, generated in
build_codebooks.py from the merge patterns below; invented code names are the F11 builder's (full S7 cards), the
label-set name is given for single-set codes (short S7 cards).

Atoms per scheme:
  xed        EMO <emotion|neutral>                  membership of the line's label set
  mams_acsa  PAIR <category> <polarity>              the (category, polarity) pair is annotated
             CAT <category>                          the category is annotated (any polarity)
             POL <polarity>                          some annotated category has this polarity
  mams_atsa  TPOL <polarity>                         the asked target's polarity
             OTHER <polarity>                        some other listed target has this polarity
  ghc        FLAG <hd|cv|vo>                         the released label field is 1
  edos       SEXIST                                  label_sexist == "sexist"
             CAT <1|2|3|4>                           label_category is that category
             VEC <vector code, e.g. 2.1>             label_vector is that vector
"""

L = lambda *a: {"op": "LIT", "atom": list(a), "neg": False}          # noqa: E731
N = lambda *a: {"op": "LIT", "atom": list(a), "neg": True}           # noqa: E731
ALL = lambda *x: {"op": "ALL", "args": list(x)}                      # noqa: E731
ANY = lambda *x: {"op": "ANY", "args": list(x)}                      # noqa: E731
E = lambda e: L("EMO", e)                                            # noqa: E731

# (codebook key, scheme, dimension, [(natural name, condition), ...], residual natural name)
F10 = [
    # ---------------- XED (union of annotated + neutral lines), small
    ("xed_s1", "xed", "emotions annotators tagged in a line of film dialogue",
     [("Heated", E("anger")), ("Uneasy", E("fear")), ("Glad", E("joy")), ("Downcast", E("sadness")),
      ("Deadpan", E("neutral"))], "Elsewhere"),
    ("xed_s2", "xed", "emotions annotators tagged in a line of film dialogue",
     [("Hostile feeling", ANY(E("anger"), E("disgust"))), ("Distress", ANY(E("fear"), E("sadness"))),
      ("Warmth", ANY(E("joy"), E("trust"))), ("Flat delivery", E("neutral"))], "Watchful or startled"),
    ("xed_s3", "xed", "emotions annotators tagged in a line of film dialogue",
     [("Fury and revulsion", ALL(E("anger"), E("disgust"))), ("Glad confidence", ALL(E("joy"), E("trust"))),
      ("Astonished", E("surprise")), ("Expectant", E("anticipation")), ("Even tone", E("neutral")),
      ("Afraid", E("fear"))], "Leftover feeling"),
    ("xed_s4", "xed", "emotions annotators tagged in a line of film dialogue",
     [("Unemotional", E("neutral")), ("Bitter grief", ALL(E("anger"), E("sadness"))), ("Irate", E("anger")),
      ("Sorrowful", E("sadness")), ("Joy minus trust", ALL(E("joy"), N("EMO", "trust"))),
      ("Alarm", ALL(E("fear"), E("surprise"))), ("Fearful", E("fear"))], "Remaining mix"),
    ("xed_s5", "xed", "emotions annotators tagged in a line of film dialogue",
     [("Trusting", E("trust")), ("Repelled", E("disgust")), ("Taken aback", E("surprise")),
      ("Looking ahead", E("anticipation")), ("Sad but unafraid", ALL(E("sadness"), N("EMO", "fear")))],
     "Catch-all"),
    # ---------------- XED large (>= 19 non-residual codes)
    ("xed_l1", "xed", "emotions annotators tagged in a line of film dialogue",
     [("Fury and revulsion", ALL(E("anger"), E("disgust"))), ("Joy with trust", ALL(E("joy"), E("trust"))),
      ("Eager joy", ALL(E("anticipation"), E("joy"))), ("Hopeful trust", ALL(E("anticipation"), E("trust"))),
      ("Angry expectation", ALL(E("anger"), E("anticipation"))), ("Shocked sorrow", ALL(E("sadness"), E("surprise"))),
      ("Frightened grief", ALL(E("fear"), E("sadness"))), ("Angry fear", ALL(E("anger"), E("fear"))),
      ("Disgusted sorrow", ALL(E("disgust"), E("sadness"))), ("Angry shock", ALL(E("anger"), E("surprise"))),
      ("Angry grief", ALL(E("anger"), E("sadness"))), ("Delighted surprise", ALL(E("joy"), E("surprise"))),
      ("Startled expectation", ALL(E("anticipation"), E("surprise"))),
      ("Anxious expectation", ALL(E("anticipation"), E("fear"))),
      ("Anger", E("anger")), ("Anticipation", E("anticipation")), ("Joy", E("joy")), ("Trust", E("trust")),
      ("Sadness", E("sadness")), ("Fear", E("fear")), ("Disgust", E("disgust")), ("Surprise", E("surprise"))],
     "Neutral line"),
    ("xed_l2", "xed", "emotions annotators tagged in a line of film dialogue",
     [("Fury and revulsion", ALL(E("anger"), E("disgust"))), ("Joy with trust", ALL(E("joy"), E("trust"))),
      ("Eager joy", ALL(E("anticipation"), E("joy"))), ("Shocked sorrow", ALL(E("sadness"), E("surprise"))),
      ("Frightened grief", ALL(E("fear"), E("sadness"))), ("Angry fear", ALL(E("anger"), E("fear"))),
      ("Disgusted sorrow", ALL(E("disgust"), E("sadness"))), ("Delighted surprise", ALL(E("joy"), E("surprise"))),
      ("Startled expectation", ALL(E("anticipation"), E("surprise"))),
      ("Frightened surprise", ALL(E("fear"), E("surprise"))), ("Trusting fear", ALL(E("fear"), E("trust"))),
      ("Angry trust", ALL(E("anger"), E("trust"))),
      ("Disgust", E("disgust")), ("Surprise", E("surprise")), ("Sadness", E("sadness")), ("Fear", E("fear")),
      ("Trust", E("trust")), ("Joy", E("joy")), ("Anticipation", E("anticipation")), ("Anger", E("anger"))],
     "Neutral line"),
    ("xed_l3", "xed", "emotions annotators tagged in a line of film dialogue",
     [("Neutral line", E("neutral")),
      ("Joy with trust", ALL(E("joy"), E("trust"))), ("Hopeful trust", ALL(E("anticipation"), E("trust"))),
      ("Fury and revulsion", ALL(E("anger"), E("disgust"))), ("Eager joy", ALL(E("anticipation"), E("joy"))),
      ("Angry expectation", ALL(E("anger"), E("anticipation"))), ("Shocked sorrow", ALL(E("sadness"), E("surprise"))),
      ("Angry shock", ALL(E("anger"), E("surprise"))), ("Angry grief", ALL(E("anger"), E("sadness"))),
      ("Anxious expectation", ALL(E("anticipation"), E("fear"))), ("Frightened surprise", ALL(E("fear"), E("surprise"))),
      ("Disgusted shock", ALL(E("disgust"), E("surprise"))), ("Sad expectation", ALL(E("anticipation"), E("sadness"))),
      ("Repelled fear", ALL(E("disgust"), E("fear"))),
      ("Anger", E("anger")), ("Anticipation", E("anticipation")), ("Joy", E("joy")), ("Sadness", E("sadness")),
      ("Fear", E("fear")), ("Disgust", E("disgust")), ("Surprise", E("surprise"))],
     "Trust by itself"),
    # ---------------- MAMS ACSA (full (category, polarity) set)
    ("acsa_s1", "mams_acsa", "opinions annotators marked per aspect category in a restaurant review sentence",
     [("Staff complaint", L("PAIR", "staff", "negative")), ("Food complaint", L("PAIR", "food", "negative")),
      ("Service complaint", L("PAIR", "service", "negative")), ("Food praise", L("PAIR", "food", "positive")),
      ("Staff praise", L("PAIR", "staff", "positive"))], "Remainder"),
    ("acsa_s2", "mams_acsa", "opinions annotators marked per aspect category in a restaurant review sentence",
     [("Price talk", L("CAT", "price")), ("Atmosphere talk", L("CAT", "ambience")), ("Menu talk", L("CAT", "menu")),
      ("Venue talk", L("CAT", "place"))], "Core topics"),
    ("acsa_s3", "mams_acsa", "opinions annotators marked per aspect category in a restaurant review sentence",
     [("Good food, sore points", ALL(L("PAIR", "food", "positive"), L("POL", "negative"))),
      ("Poor food, bright spots", ALL(L("PAIR", "food", "negative"), L("POL", "positive"))),
      ("Staff letdown", L("PAIR", "staff", "negative")), ("Service plaudit", L("PAIR", "service", "positive")),
      ("Price gripe", L("PAIR", "price", "negative")), ("Extras plaudit", L("PAIR", "miscellaneous", "positive"))],
     "Unclassed mix"),
    # acsa_l1 is generated in build_codebooks.py (rarity-ordered PAIR codes; residual = the frequent pairs)
    # ---------------- MAMS ATSA ((asked target polarity; other listed targets' polarity set))
    ("atsa_s1", "mams_atsa", "polarity annotators gave the asked target and the other listed targets",
     [("Praised amid criticism", ALL(L("TPOL", "positive"), L("OTHER", "negative"))),
      ("Criticised amid praise", ALL(L("TPOL", "negative"), L("OTHER", "positive"))),
      ("Praised target", L("TPOL", "positive")), ("Criticised target", L("TPOL", "negative"))], "Neutral target"),
    ("atsa_s2", "mams_atsa", "polarity annotators gave the asked target and the other listed targets",
     [("Neutral between camps", ALL(L("TPOL", "neutral"), L("OTHER", "positive"), L("OTHER", "negative"))),
      ("Neutral beside criticism", ALL(L("TPOL", "neutral"), L("OTHER", "negative"))),
      ("Neutral beside praise", ALL(L("TPOL", "neutral"), L("OTHER", "positive"))),
      ("Favoured target", L("TPOL", "positive"))], "Faulted target"),
    ("atsa_s3", "mams_atsa", "polarity annotators gave the asked target and the other listed targets",
     [("Praise among strong views", ALL(L("TPOL", "positive"), N("OTHER", "neutral"))),
      ("Criticism among strong views", ALL(L("TPOL", "negative"), N("OTHER", "neutral"))),
      ("Praise beside plain mentions", ALL(L("TPOL", "positive"), L("OTHER", "neutral"))),
      ("Criticism beside plain mentions", ALL(L("TPOL", "negative"), L("OTHER", "neutral"))),
      ("Plain target, praise elsewhere", ALL(L("TPOL", "neutral"), L("OTHER", "positive")))],
     "Plain target, faults elsewhere"),
    ("atsa_s4", "mams_atsa", "polarity annotators gave the asked target and the other listed targets",
     [("Full spread among peers", ALL(L("OTHER", "positive"), L("OTHER", "negative"), L("OTHER", "neutral"))),
      ("Split peers", ALL(L("OTHER", "positive"), L("OTHER", "negative"))),
      ("Liked, plain peers", ALL(L("TPOL", "positive"), L("OTHER", "neutral"))),
      ("Disliked, plain peers", ALL(L("TPOL", "negative"), L("OTHER", "neutral"))),
      ("Plain, liked peers", ALL(L("TPOL", "neutral"), L("OTHER", "positive"))),
      ("Plain, disliked peers", ALL(L("TPOL", "neutral"), L("OTHER", "negative"))),
      ("Liked target", L("TPOL", "positive"))], "Disliked among liked"),
    # ---------------- GHC (hd = human degradation, cv = call for violence, vo = vulgarity / offensive)
    ("ghc_s1", "ghc", "hate-speech features annotators marked in a social media post",
     [("Violent call", L("FLAG", "cv")), ("Degrading and vulgar", ALL(L("FLAG", "hd"), L("FLAG", "vo"))),
      ("Degrading", L("FLAG", "hd")), ("Vulgar", L("FLAG", "vo"))], "Unflagged"),
    ("ghc_s2", "ghc", "hate-speech features annotators marked in a social media post",
     [("Degrading call to violence", ALL(L("FLAG", "hd"), L("FLAG", "cv"))), ("Violent call", L("FLAG", "cv")),
      ("Degrading", L("FLAG", "hd")), ("Plain vulgarity", L("FLAG", "vo"))], "Unflagged"),
    ("ghc_s3", "ghc", "hate-speech features annotators marked in a social media post",
     [("Vulgar violent call", ALL(L("FLAG", "vo"), L("FLAG", "cv"))), ("Violent call", L("FLAG", "cv")),
      ("Degrading and vulgar", ALL(L("FLAG", "hd"), L("FLAG", "vo"))), ("Degrading", L("FLAG", "hd")),
      ("Vulgar", L("FLAG", "vo"))], "Unflagged"),
    ("ghc_s4", "ghc", "hate-speech features annotators marked in a social media post",
     [("Degrading, clean language", ALL(L("FLAG", "hd"), N("FLAG", "vo"))),
      ("Vulgar, non-degrading", ALL(L("FLAG", "vo"), N("FLAG", "hd"))),
      ("Degrading and vulgar", ALL(L("FLAG", "hd"), L("FLAG", "vo"))), ("Violent call", L("FLAG", "cv"))],
     "Unflagged"),
    ("ghc_s5", "ghc", "hate-speech features annotators marked in a social media post",
     [("Degrading call to violence", ALL(L("FLAG", "hd"), L("FLAG", "cv"))), ("Violent call", L("FLAG", "cv")),
      ("Degrading and vulgar", ALL(L("FLAG", "hd"), L("FLAG", "vo"))),
      ("Single offence", ANY(L("FLAG", "hd"), L("FLAG", "vo")))], "Unflagged"),
    ("ghc_s6", "ghc", "hate-speech features annotators marked in a social media post",
     [("Violent call, non-degrading", ALL(N("FLAG", "hd"), L("FLAG", "cv"))),
      ("Degrading call to violence", ALL(L("FLAG", "hd"), L("FLAG", "cv"))),
      ("Degrading and vulgar", ALL(L("FLAG", "hd"), L("FLAG", "vo"))), ("Degrading", L("FLAG", "hd")),
      ("Vulgar", L("FLAG", "vo"))], "Unflagged"),
    ("ghc_s7", "ghc", "hate-speech features annotators marked in a social media post",
     [("Degrading and vulgar", ALL(L("FLAG", "hd"), L("FLAG", "vo"))), ("Degrading", L("FLAG", "hd")),
      ("Violent call", L("FLAG", "cv")), ("Vulgar", L("FLAG", "vo"))], "Unflagged"),
    # ---------------- EDOS (label_sexist, label_category, label_vector)
    ("edos_s1", "edos", "sexism type annotators assigned to an online post",
     [("Harm talk", L("CAT", "1")), ("Put-down", L("CAT", "2")), ("Hostile jab", L("CAT", "3")),
      ("Biased take", L("CAT", "4"))], "Clear post"),
    ("edos_s2", "edos", "sexism type annotators assigned to an online post",
     [("Descriptive attack", L("VEC", "2.1")), ("Aggressive attack", L("VEC", "2.2")),
      ("Dehumanising attack", L("VEC", "2.3")), ("Hostile jab", L("CAT", "3")),
      ("Harm or bias", ANY(L("CAT", "1"), L("CAT", "4")))], "Clear post"),
    ("edos_s3", "edos", "sexism type annotators assigned to an online post",
     [("Gendered slur", L("VEC", "3.1")), ("Stereotype", L("VEC", "3.2")),
      ("Backhanded or condescending", ANY(L("VEC", "3.3"), L("VEC", "3.4"))), ("Put-down", L("CAT", "2")),
      ("Harm talk", L("CAT", "1")), ("Biased take", L("CAT", "4"))], "Clear post"),
    ("edos_s4", "edos", "sexism type annotators assigned to an online post",
     [("Aggression", ANY(L("CAT", "1"), L("VEC", "2.2"))), ("Contempt", ANY(L("VEC", "2.1"), L("VEC", "2.3"))),
      ("Gendered slur", L("VEC", "3.1")), ("Patronising view", ANY(L("VEC", "3.2"), L("VEC", "3.3"), L("VEC", "3.4"))),
      ("Biased take", L("CAT", "4"))], "Clear post"),
    ("edos_s5", "edos", "sexism type annotators assigned to an online post",
     [("Descriptive attack", L("VEC", "2.1")), ("Gendered slur", L("VEC", "3.1")),
      ("Aggressive attack", L("VEC", "2.2")), ("Stereotype", L("VEC", "3.2")), ("Sexist, other kind", L("SEXIST"))],
     "Clear post"),
    ("edos_s6", "edos", "sexism type annotators assigned to an online post",
     [("Aggression", ANY(L("CAT", "1"), L("VEC", "2.2"))), ("Contempt", ANY(L("VEC", "2.1"), L("VEC", "2.3"))),
      ("Gendered slur", L("VEC", "3.1")), ("Stereotype", L("VEC", "3.2")),
      ("Backhanded or condescending", ANY(L("VEC", "3.3"), L("VEC", "3.4"))),
      ("Backing mistreatment", L("VEC", "4.1")), ("Backing discrimination", L("VEC", "4.2"))], "Clear post"),
    ("edos_s7", "edos", "sexism type annotators assigned to an online post",
     [("Incitement", L("VEC", "1.2")), ("Descriptive attack", L("VEC", "2.1")), ("Aggressive attack", L("VEC", "2.2")),
      ("Dehumanising attack", L("VEC", "2.3")), ("Gendered slur", L("VEC", "3.1")), ("Stereotype", L("VEC", "3.2")),
      ("Backing discrimination", L("VEC", "4.2")), ("Clear post", N("SEXIST"))], "Rare sexism kinds"),
]

# F11 merge patterns.
# XED: codes are lists of full label sets. 'S' = the 8 singletons; pairs and triples named explicitly; merged codes
# list several full sets. Coverage = the union of listed sets (other records are excluded from F11 S7, SEM-46).
EMOS = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]
P_TOP = [("anger", "disgust"), ("joy", "trust"), ("anticipation", "joy"), ("anticipation", "trust"),
         ("anger", "anticipation"), ("sadness", "surprise"), ("fear", "sadness"), ("anger", "fear"),
         ("disgust", "sadness"), ("anger", "surprise"), ("anger", "sadness"), ("joy", "surprise"),
         ("anticipation", "surprise"), ("anticipation", "fear"), ("fear", "surprise"), ("fear", "trust"),
         ("anger", "trust"), ("sadness", "trust"), ("disgust", "surprise"), ("anticipation", "sadness"),
         ("disgust", "fear"), ("surprise", "trust"), ("anger", "joy")]
T_TOP = [("anticipation", "joy", "trust"), ("anger", "disgust", "sadness"), ("anger", "disgust", "surprise"),
         ("anticipation", "joy", "surprise"), ("anger", "disgust", "fear"), ("joy", "surprise", "trust")]
# Each F11 XED codebook: ("singles", n_pairs, n_triples, merges) where merges = list of (single, pair) to merge into
# one code ("<e> alone, or <e> and <f>").
F11_XED = [
    ("x01", 8, 0, [("anger", ("anger", "disgust"))]), ("x02", 12, 0, [("trust", ("joy", "trust"))]), ("x03", 16, 2, []), ("x04", 16, 4, []), ("x05", 20, 2, []),
    ("x06", 10, 0, [("joy", ("joy", "trust"))]), ("x07", 14, 0, [("anger", ("anger", "disgust")),
                                                                ("sadness", ("sadness", "surprise"))]),
    ("x08", 18, 3, [("trust", ("anticipation", "trust"))]), ("x09", 7, 0, [("sadness", ("sadness", "surprise"))]),
    ("x10", 12, 1, [("fear", ("fear", "sadness")), ("anticipation", ("anticipation", "joy"))]),
    ("x11", 16, 0, [("disgust", ("anger", "disgust"))]), ("x12", 21, 2, [("surprise", ("joy", "surprise"))]),
]
# MAMS: per named polarity p, a pattern over the other targets' polarity sets S (p's own singleton {p} is never
# observed in MAMS). Patterns name merged blocks; 'a' = identity (6 blocks).
#   a : {N},{U},{X},{N,U}... all 6 observed sets separate                       (6 blocks)
#   b : merge {all three} into {the two polarities other than p}               (5 blocks)
#   d1: merge {all three} into {p, first other}; d2: into {p, second other}     (5 blocks)
#   c2: merge {q} with {q, p} for the first other polarity q                    (5 blocks, all-three separate)
#   c3: as c2, and also merge {all three} into {the two others}                 (4 blocks)
F11_MAMS = {
    "mams_acsa": [("a01", ("b", "b", "b")), ("a02", ("d1", "b", "d2")), ("a03", ("c3", "b", "b")),
                  ("a04", ("b", "c3", "d1")), ("a05", ("d2", "d2", "c3")), ("a06", ("c3", "c3", "b"))],
    "mams_atsa": [("t01", ("a", "a", "a")), ("t02", ("b", "a", "a")), ("t03", ("a", "c2", "b")),
                  ("t04", ("d1", "d2", "a")), ("t05", ("c2", "c2", "c2")), ("t06", ("b", "b", "c3"))],
}
# EDOS: merges of the 12 values (11 vectors + "none"); unmerged values are their own code.
F11_EDOS = [("e01", []), ("e02", [["3.3", "3.4"]]), ("e03", [["1.1", "1.2"]]), ("e04", [["4.1", "4.2"]]),
            ("e05", [["1.1", "1.2"], ["3.3", "3.4"]]), ("e06", [["4.1", "4.2"], ["1.1", "1.2"]]),
            ("e07", [["3.3", "3.4"], ["4.1", "4.2"]]), ("e08", [["2.2", "2.3"], ["1.1", "1.2"]])]
