import hashlib, re, pathlib
root = pathlib.Path('/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b')
sha = hashlib.sha256((root/'G0_LITE_T37B_A1.md').read_bytes()).hexdigest()
p = root/'builder.py'
s = p.read_text()
s2 = re.sub(r'G0_AMENDMENT_SHA256 = "[0-9a-f]{64}"', f'G0_AMENDMENT_SHA256 = "{sha}"', s)
p.write_text(s2)
print(sha, len((root/'G0_LITE_T37B_A1.md').read_text().splitlines()), 'lines')
