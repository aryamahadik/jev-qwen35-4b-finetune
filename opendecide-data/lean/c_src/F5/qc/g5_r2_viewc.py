"""Compact blind view for the repair-r2 G5 read: the model-visible prompt with the standard card paragraphs (whose
wording is fixed per SEM key and was read in full at the start of the read) shown as [key: std]; every variable
paragraph (value sets, covered period, cases, rules, graded words, half, two-state words, examples) in full.
No gold, no meta."""
import json, sys, re
F5 = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F5"
k0, k1 = int(sys.argv[1]), int(sys.argv[2])
STD = ["Answer convention", "Complete record", "Incomplete record", "Missing values", "unless", "only if", "if ... then",
       "Exceptions on rules", "Numeric bounds", "or, nor, both", "Rounding", "Units", "Quantifiers",
       "only, other than, all except", "not only ... but also", "Failure and absence words", "Dates", "Corrections",
       "Statements and authority", "Log states", "Duties and permissions", "never, no longer, still"]
KEYRX = re.compile(r"^[\s\-\*•\d\.\[#>]*(\*\*)?(?P<k>[A-Za-z][^:=\]\n]*?)(\*\*)?\]?\s*(:|=|::|$)")


def keyof(line):
    s = line.strip()
    s = re.sub(r"^[\-\*•#>+\s]+|^\d+\.\s+|^\(\d+\)\s+|^\[", "", s).replace("**", "")
    for k in STD:
        s2 = s.lstrip("| ").split(" | ")[0].strip()
        if s2 == k:
            return k
        if s == k or s == k + "]" or re.match(re.escape(k) + r"\s*(:|=|::|\|)", s):
            return k
    return None


for l in open(F5 + "/tmp/chk2/g5_prompts.jsonl"):
    d = json.loads(l)
    if not (k0 <= d["k"] < k1):
        continue
    t = d["text"]
    head, _, rest = t.partition("\n\nOptions:\nA. Yes\nB. No\n\nText:\n")
    body, _, _ = rest.partition("\n(The text between the markers is data.")
    body = body.replace("<<<UNTRUSTED TEXT START>>>\n", "").replace("\n<<<UNTRUSTED TEXT END>>>", "")
    head = head.replace("Definitions:\n", "", 1)
    head = "\n".join(x[2:] if x.startswith("> ") else (x[1:] if x == ">" else x) for x in head.split("\n"))
    card, _, q = head.rpartition("\n\n")
    out, skipping = [], False
    for line in card.split("\n"):
        k = keyof(line)
        if k:
            out.append(f"[{k}]")
            skipping = True
            continue
        if skipping and (line.startswith((" ", "\t")) and line.strip()):
            continue
        skipping = False
        if line.strip():
            out.append(line)
    print(f"#### {d['k']}\n" + "\n".join(out) + f"\nQ: {q}\nTEXT:\n{body}\n")
