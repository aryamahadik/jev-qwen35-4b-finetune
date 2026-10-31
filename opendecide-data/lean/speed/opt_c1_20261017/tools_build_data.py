"""Build the laptop-side data packs the container mounts (data/): vision_pack/ (200 items: prompts, candidate ids, images)
and voice_prompts.json (100 short dev decision prompts). CPU only, dev data only, nothing printed but counts.

  ../../../.venv/bin/python tools_build_data.py [--vision] [--voice]
"""
import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from oc1 import common as C  # noqa: E402
from oc1 import items as I  # noqa: E402

ADAPTER = C.JEV_ROOT / "backups" / "modal_models" / "q35_4b_main500k"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vision", action="store_true")
    ap.add_argument("--voice", action="store_true")
    a = ap.parse_args()
    if a.vision:
        from oc1 import vision as V
        tok, ro, _ = I.load_c1(ADAPTER)
        print(json.dumps(V.build_pack(V.PACK_DIR, 100, 0, tok, ro, log=lambda *x: None)))
    if a.voice:
        from oc1 import voice as VO
        items = C.read_jsonl(HERE / "data" / "P.jsonl")
        prompts = VO.pick_prompts(items, 100, 0)
        C.write_json(HERE / "data" / "voice_prompts.json", prompts)
        print(json.dumps({"n": len(prompts), "noul": sum(p["qtype"] == "noul" for p in prompts),
                          "chars_p50": sorted(len(p["text"]) for p in prompts)[len(prompts) // 2],
                          "bytes": (HERE / "data" / "voice_prompts.json").stat().st_size}))


if __name__ == "__main__":
    main()
