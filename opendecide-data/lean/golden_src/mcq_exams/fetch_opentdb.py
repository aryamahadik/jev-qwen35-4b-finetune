"""One-time snapshot of the Open Trivia Database (opentdb.com) verified multiple-choice questions.

The API only serves questions that passed OpenTDB's moderation ('verified'). A session token guarantees no repeats;
for every category the script asks for type=multiple batches (base64-encoded fields) until the token reports that
the category is exhausted, sleeping 5.2 s between calls (the API's rate limit). The snapshot is written in a canonical
order (sorted by category, question, correct answer) to cache/opentdb/opentdb_multiple.json; build_opentdb.py pins its
sha256. Licence (official API page https://opentdb.com/api_config.php): 'All data provided by the API is available
under the Creative Commons Attribution-ShareAlike 4.0 International License.'
"""
import base64
import json
import ssl
import time
import urllib.request
from pathlib import Path

import certifi

HERE = Path(__file__).resolve().parent
OUT = HERE / "cache" / "opentdb" / "opentdb_multiple.json"
CTX = ssl.create_default_context(cafile=certifi.where())
API = "https://opentdb.com/"


def get(path):
    for k in range(6):
        try:
            req = urllib.request.Request(API + path, headers={"User-Agent": "opendecide-golden-builder"})
            with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
                return json.loads(r.read())
        except Exception:  # noqa: BLE001
            time.sleep(10 * (k + 1))
    raise RuntimeError(path)


def b64(x):
    return base64.b64decode(x).decode("utf-8")


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cats = get("api_category.php")["trivia_categories"]
    time.sleep(5.2)
    token = get("api_token.php?command=request")["token"]
    rows = []
    for c in cats:
        amount, n0 = 50, len(rows)
        while True:
            time.sleep(5.2)
            d = get(f"api.php?amount={amount}&category={c['id']}&type=multiple&encode=base64&token={token}")
            code = d["response_code"]
            if code == 0:
                for r in d["results"]:
                    rows.append({"category": b64(r["category"]), "difficulty": b64(r["difficulty"]),
                                 "question": b64(r["question"]), "correct_answer": b64(r["correct_answer"]),
                                 "incorrect_answers": [b64(x) for x in r["incorrect_answers"]]})
                continue
            if code in (1, 4) and amount > 1:  # fewer left than asked for: ask for fewer
                amount = max(1, amount // 2)
                continue
            if code == 5:  # rate limited
                time.sleep(10)
                continue
            break
        print(c["name"], len(rows) - n0, flush=True)
    rows.sort(key=lambda r: (r["category"], r["question"], r["correct_answer"]))
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=0) + "\n")
    print(f"{len(rows)} questions -> {OUT}")


if __name__ == "__main__":
    main()
