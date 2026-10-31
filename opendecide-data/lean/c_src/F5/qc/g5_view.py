"""Print model-visible prompts k0..k1-1 compactly (boilerplate and the repeated question dropped). No gold, no meta."""
import json, sys
F5 = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F5"
k0, k1 = int(sys.argv[1]), int(sys.argv[2])
for l in open(F5 + "/tmp/chk/g5_prompts.jsonl"):
    d = json.loads(l)
    if not (k0 <= d["k"] < k1):
        continue
    t = d["text"]
    head, _, rest = t.partition("\n\nOptions:\nA. Yes\nB. No\n\nText:\n")
    body, _, _ = rest.partition("\n(The text between the markers is data.")
    body = body.replace("<<<UNTRUSTED TEXT START>>>\n", "").replace("\n<<<UNTRUSTED TEXT END>>>", "")
    head = head.replace("Definitions:\n", "", 1)
    head = "\n".join(x[2:] if x.startswith("> ") else (x[1:] if x == ">" else x) for x in head.split("\n"))
    head = head.replace("**Definitions for this task**\n\n", "")
    card, _, q = head.rpartition("\n\n")
    print(f"########## {d['k']}\n[CARD]\n{card}\n[Q] {q}\n[TEXT]\n{body}\n")
