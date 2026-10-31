import html
import re
import sys

src = sys.argv[1]
raw = open(src, encoding="utf-8", errors="replace").read()
raw = re.sub(r"(?is)<(script|style|noscript|svg)\b.*?</\1>", " ", raw)
raw = re.sub(r"(?i)<br\s*/?>|</(p|div|li|tr|h[1-6]|section|article|table)>", "\n", raw)
text = re.sub(r"<[^>]+>", " ", raw)
text = html.unescape(text)
lines = [re.sub(r"[ \t]+", " ", l).strip() for l in text.splitlines()]
out = "\n".join(l for l in lines if l)
print(out)
