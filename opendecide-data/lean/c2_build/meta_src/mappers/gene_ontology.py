"""Mapper: md_gene_ontology (Gene Ontology go-basic.obo, release 2026-07-26; CC BY 4.0).

Run (from lean/c2_build):  nice -n 10 .venv/bin/python -B meta_src/mappers/gene_ontology.py
Input: meta_src/raw/go/go-basic.obo (untrusted download; parsed as text). Output: data/c2_md_parts/md_gene_ontology/.
Gold = a program over the term's own fields (is_a / synonym / xref / subset counts and lines, namespace, is_obsolete).
Every count the question asks about is printed in the state (lists capped by pool filters, so they are complete).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdkit_c as K  # noqa: E402

SRC = "md_gene_ontology"
RAW = K.META_SRC / "raw" / "go" / "go-basic.obo"
LIC = {"name": "Creative Commons Attribution 4.0 (CC BY 4.0)", "url": "https://geneontology.org/docs/go-citation-policy/",
       "dataset_url": "https://purl.obolibrary.org/obo/go/go-basic.obo",
       "verified": "Gene Ontology Consortium citation policy: data licensed under CC BY 4.0"}
NS = ["biological_process", "molecular_function", "cellular_component"]
N = 14


def parse():
    terms = {}
    for st in RAW.read_text(encoding="utf-8").split("\n[Term]\n")[1:]:
        st = st.split("\n[Typedef]")[0]
        t = {"parents": [], "syn": [], "rel": [], "subset": [], "xref": [], "obs": False, "replaced": None}
        for ln in st.split("\n"):
            if ": " not in ln:
                continue
            k, v = ln.split(": ", 1)
            if k == "id":
                t["id"] = v
            elif k == "name":
                t["name"] = v
            elif k == "namespace":
                t["ns"] = v
            elif k == "def":
                m = re.match(r'"(.*)" \[(.*)\]', v)
                if m:
                    t["def"], t["defsrc"] = m.group(1), [x.strip() for x in m.group(2).split(",") if x.strip()]
            elif k == "synonym":
                m = re.match(r'"(.*)" (EXACT|RELATED|BROAD|NARROW)', v)
                if m:
                    t["syn"].append((m.group(1), m.group(2)))
            elif k == "is_a":
                t["parents"].append(v.split(" ! ")[-1].strip())
            elif k == "relationship":
                m = re.match(r"(\S+) (GO:\d+) ! (.*)", v)
                if m:
                    t["rel"].append((m.group(1), m.group(3)))
            elif k == "subset":
                t["subset"].append(v.strip())
            elif k == "xref":
                t["xref"].append(v.split(" ")[0])
            elif k == "is_obsolete":
                t["obs"] = v.strip() == "true"
            elif k == "replaced_by":
                t["replaced"] = v.strip()
        if all(x in t for x in ("id", "name", "ns", "def")):
            terms[t["id"]] = t
    return list(terms.values())


def state(fields):
    def f(t):
        L = [("GO term", t["id"]), ("Name", t["name"])]
        if "def" in fields:
            L.append(("Definition", K.clip(t["def"], 420)))
            L.append(("Definition sources", ", ".join(t["defsrc"]) or "none listed"))
        if "syn" in fields:
            L.append((f"Synonyms ({len(t['syn'])})", "; ".join(f'"{a}" {b}' for a, b in t["syn"]) or "none listed"))
        if "parents" in fields:
            L.append((f"Direct is_a parents ({len(t['parents'])})", "; ".join(t["parents"]) or "none listed"))
        if "rel" in fields:
            L.append(("Other relationships", "; ".join(f"{a} {b}" for a, b in t["rel"]) or "none listed"))
        if "subset" in fields:
            L.append(("Subsets", ", ".join(t["subset"]) or "none listed"))
        if "xref" in fields:
            L.append((f"Cross-references ({len(t['xref'])})", ", ".join(t["xref"]) or "none listed"))
        if "obs" in fields and t["replaced"]:
            L.append(("Replaced by", t["replaced"]))
        return K.kv(L)
    return f


ALL = {"def", "syn", "parents", "rel", "subset", "xref"}


def main():
    terms = parse()
    live = [t for t in terms if not t["obs"]]
    obs = [t for t in terms if t["obs"]]
    key = lambda t: t["id"]
    B = K.Builder(SRC, "bioinformatics ontology", LIC)
    P = lambda t: len(t["parents"])
    compact = [t for t in live if len(t["syn"]) <= 7 and len(t["parents"]) <= 6 and len(t["xref"]) <= 7
               and len(t["rel"]) <= 5 and len(t["subset"]) <= 5 and len(t["def"].split()) <= 70]
    byns = {n: [t for t in compact if t["ns"] == n] for n in NS}
    print({n: len(v) for n, v in byns.items()}, len(live), len(obs))
    short = {"biological_process": "biological process", "molecular_function": "molecular function",
             "cellular_component": "cellular component"}

    def num_task(tag, pool, fn, thr, noun, fields, card=None, n=N):
        qa_t = [f"Does this GO term have more than {thr} {noun}?", f"Is the number of {noun} of this GO term above {thr}?",
                f"Would you say this term has over {thr} {noun}?"]
        qb_t = [f"Does this GO term have at most {thr} {noun}?", f"Is the number of {noun} of this GO term {thr} or fewer?",
                f"Would you say this term has {thr} {noun} or fewer?"]
        qa, qb = K.pair_fns(list(zip(qa_t, qb_t)), tag, key)
        B.yn(tag, pool, key, state(fields), qa, qb, lambda t: fn(t) > thr, lambda t: fn(t) <= thr, card, n, tag.split(".")[0])

    pcard = ("Direct parents are the is_a entries listed on the term. Relationships such as part_of are not parents and "
             "are not counted. The list shown is complete.")
    # 1. parents x namespace (card on k=2 and k=3)
    for n in NS:
        for k in (1, 2, 3):
            num_task(f"parents.{n}.{k}", byns[n], P, k, "direct is_a parents", ALL,
                     card=(K.yn_card(f"the term lists more than {k} direct is_a parents. {pcard}", f"the term lists {k} or fewer direct is_a parents. {pcard}") if k >= 2 else None))
    # 2. synonyms x namespace
    for n in NS:
        for k in (0, 1, 2, 3):
            num_task(f"syn.{n}.{k}", byns[n], lambda t: len(t["syn"]), k, "listed synonyms", ALL)
    # 3. xref
    for k in (1, 2, 3):
        num_task(f"xref.all.{k}", compact, lambda t: len(t["xref"]), k, "cross-references", ALL,
                 card=K.yn_card(f"the number of cross-references shown is greater than {k}.", f"the number of cross-references shown is {k} or fewer."))
    # 4. part_of present x namespace
    for n in NS:
        qa, qb = K.pair_fns([("Does this term have a part_of relationship?", "Is the part_of relationship missing from this term?"),
                             ("Is a part_of relationship listed for this term?", "Does this term list other relationships without part_of?")][:1] +
                            [("Does this term list a part_of link?", "Is every listed link of this term something other than part_of?")][:0],
                            f"partof.{n}", key)
        B.yn(f"partof.{n}", byns[n], key, state(ALL), qa, qb, lambda t: any(a == "part_of" for a, _ in t["rel"]),
             lambda t: not any(a == "part_of" for a, _ in t["rel"]), None, N, "relationship")
    # 5. slim membership x namespace
    for n in NS:
        qa, qb = K.pair_fns([("Is this term a member of the generic GO slim subset?", "Is this term left out of the generic GO slim subset?")], f"slim.{n}", key)
        B.yn(f"slim.{n}", byns[n], key, state(ALL), qa, qb, lambda t: "goslim_generic" in t["subset"],
             lambda t: "goslim_generic" not in t["subset"],
             K.yn_card("the Subsets line includes goslim_generic.", "the Subsets line does not include goslim_generic (other slims do not count)."), N, "subset")
        qa2, qb2 = K.pair_fns([("Is this term in at least one GO slim subset?", "Is this term outside every GO slim subset?")], f"anyslim.{n}", key)
        B.yn(f"anyslim.{n}", byns[n], key, state(ALL), qa2, qb2, lambda t: any(s.startswith("goslim_") for s in t["subset"]),
             lambda t: not any(s.startswith("goslim_") for s in t["subset"]), None, N, "subset")
    # 6. name words
    for w in ("regulation", "transport", "binding", "process"):
        qa, qb = K.pair_fns([(f"Does the term name contain the word '{w}'?", f"Is the word '{w}' absent from the term name?")], f"nameword.{w}", key)
        B.yn(f"nameword.{w}", compact, key, state(ALL), qa, qb, lambda t, w=w: w in re.findall(r"[a-z]+", t["name"].lower()),
             lambda t, w=w: w not in re.findall(r"[a-z]+", t["name"].lower()), None, N, "name")
    for k in (3, 5, 7):
        qa, qb = K.pair_fns([(f"Does the term name have more than {k} words?", f"Does the term name have {k} words or fewer?")], f"namelen.{k}", key)
        B.yn(f"namelen.{k}", compact, key, state(ALL), qa, qb, lambda t, k=k: len(t["name"].split()) > k,
             lambda t, k=k: len(t["name"].split()) <= k, None, N, "name")
    for k in (20, 35, 50):
        full = [t for t in compact if len(t["def"].split()) <= 70 and len(t["def"]) <= 420]
        qa, qb = K.pair_fns([(f"Is the definition longer than {k} words?", f"Is the definition {k} words or shorter?")], f"deflen.{k}", key)
        B.yn(f"deflen.{k}", full, key, state(ALL), qa, qb, lambda t, k=k: len(t["def"].split()) > k,
             lambda t, k=k: len(t["def"].split()) <= k,
             K.yn_card(f"the definition text (without its source list) has more than {k} words.", f"the definition text (without its source list) has {k} words or fewer."), N, "def")
    # 7. namespace, hidden (knowledge tasks; the Haiku gate decides)
    nsdefs = {"biological_process": "a series of events a cell or organism carries out, such as a pathway, response, development or regulation",
              "molecular_function": "an activity of a gene product at the molecular level, such as catalysis, binding or transport activity",
              "cellular_component": "a place in a cell or a complex, such as an organelle, membrane, compartment or protein complex"}
    for tag, fields in (("name", set()), ("namedef", {"def"}), ("nameparents", {"parents"})):
        B.choice(f"nschoice.{tag}", compact, key, state(fields),
                 lambda t: ["Which GO namespace does this term belong to?", "In which of the three GO namespaces is this term placed?"][K.hx(K.SEED, "q", t["id"]) % 2],
                 NS, lambda t: t["ns"], K.choice_card(nsdefs), 18, "namespace")
    for n in NS:
        others = [m for m in NS if m != n]
        qa, qb = K.pair_fns([(f"Does this term belong to the {short[n]} namespace?", f"Does this term belong to the {short[others[0]]} or the {short[others[1]]} namespace?")], f"nsyn.{n}", key)
        B.yn(f"nsyn.{n}", compact, key, state({"def", "parents"}), qa, qb, lambda t, n=n: t["ns"] == n, lambda t, n=n: t["ns"] != n,
             K.yn_card(f"the term's namespace is {n}, meaning {nsdefs[n]}.", "the term's namespace is one of the two other GO namespaces."), N, "namespace")
    # 8. choices read off the state
    scope = [t for t in compact if t["syn"]]
    B.choice("firstsyn.scope", scope, key, state(ALL), "Which scope does the first listed synonym have?",
             ["EXACT", "RELATED", "BROAD", "NARROW"], lambda t: t["syn"][0][1],
             K.choice_card({"EXACT": "the synonym means the same as the term name", "RELATED": "the synonym is related in meaning but not the same",
                            "BROAD": "the synonym names a broader idea than the term", "NARROW": "the synonym names a narrower idea than the term"}), 20, "synonym")
    cats = ["GOC", "PMID", "ISBN", "Wikipedia", "other"]

    def dcat(t):
        p = t["defsrc"][0].split(":")[0] if t["defsrc"] else "other"
        return p if p in cats else "other"
    B.choice("defsrc.first", compact, key, state(ALL), "Which source prefix does the first definition source use?", cats, dcat,
             K.choice_card({"GOC": "the entry starts with GOC:", "PMID": "the entry starts with PMID:", "ISBN": "the entry starts with ISBN:",
                            "Wikipedia": "the entry starts with Wikipedia:", "other": "any other prefix"}), 20, "def_sources")
    B.choice("parents.band", compact, key, state(ALL), "Which band holds the number of direct is_a parents?", ["1", "2", "3 or more"],
             lambda t: "1" if P(t) == 1 else "2" if P(t) == 2 else "3 or more" if P(t) >= 3 else "0", None, 18, "is_a")
    sband = lambda t: "0" if not t["syn"] else "1 to 2" if len(t["syn"]) <= 2 else "3 or more"
    B.choice("syn.band", compact, key, state(ALL), "Which band holds the number of listed synonyms?", ["0", "1 to 2", "3 or more"], sband,
             K.choice_card({"0": "the term lists no synonyms", "1 to 2": "the term lists one or two synonyms", "3 or more": "the term lists three or more synonyms"}), 18, "synonym")
    xband = lambda t: "0" if not t["xref"] else "1 to 2" if len(t["xref"]) <= 2 else "3 or more"
    B.choice("xref.band", compact, key, state(ALL), "Which band holds the number of cross-references?", ["0", "1 to 2", "3 or more"], xband, None, 18, "xref")
    ncount = lambda t: sum(1 for s in {x for _, x in t["syn"]})
    B.choice("syn.scopes", [t for t in compact if t["syn"]], key, state(ALL), "How many different synonym scopes does the term use?", ["1", "2", "3 or more"],
             lambda t: "1" if ncount(t) == 1 else "2" if ncount(t) == 2 else "3 or more", None, 16, "synonym")
    # 9. obsolete (name keeps its 'obsolete' prefix on the term)
    ob = [t for t in obs if len(t["def"].split()) <= 70]
    mix = ob + [t for t in compact]
    qa, qb = K.pair_fns([("Is this GO term marked as obsolete?", "Is this GO term still active?")], "obsolete", key)
    B.yn("obsolete", mix, key, state({"def", "obs"}), qa, qb, lambda t: t["obs"], lambda t: not t["obs"],
         K.yn_card("the term is obsolete: its name starts with 'obsolete' and its definition starts with 'OBSOLETE'.", "the term is a current term: it has no 'obsolete' prefix in its name and no 'OBSOLETE' prefix in its definition."), N, "is_obsolete")
    rep = [t for t in ob if t["replaced"]]
    qa, qb = K.pair_fns([("Does this obsolete term name a replacement term?", "Is the Replaced by line missing for this obsolete term?")], "replaced", key)
    B.yn("replaced", ob, key, state({"def", "obs"}), qa, qb, lambda t: bool(t["replaced"]), lambda t: not t["replaced"], None, N, "replaced_by")
    man = B.write("Gene Ontology go-basic.obo release 2026-07-26 (CC BY 4.0); term fields are inputs and gold.")
    print(man["report"])


if __name__ == "__main__":
    main()
