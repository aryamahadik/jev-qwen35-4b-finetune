import json, glob, os
from PIL import Image
R = "/Users/aryamahadik/Documents/jev/vision_bench/data"
out = {}
for f in glob.glob(f"{R}/*/images/*"):
    with Image.open(f) as im:
        out[f] = im.size
json.dump(out, open("/Users/aryamahadik/Documents/jev/vision_bench/review/tmp/sizes.json", "w"))
print(len(out))
