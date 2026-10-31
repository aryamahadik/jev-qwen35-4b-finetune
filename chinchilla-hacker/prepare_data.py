"""Step 1: get the data.

Downloads a 200 MB slice of TinyStories (GPT-4 version; Eldan & Li, 2023) and turns it into
character-level token ids. Characters keep the vocabulary tiny (~80 symbols). With a
50k-word vocabulary, the embedding table would be most of a 100k-parameter model.

Output: data/train.bin, data/val.bin (uint8 token ids), data/vocab.json
"""
import json
import os
import subprocess

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
URL = "https://huggingface.co/datasets/roneneldan/TinyStories/resolve/main/"
TRAIN, VAL = "TinyStoriesV2-GPT4-train.txt", "TinyStoriesV2-GPT4-valid.txt"
EOT = "\x04"  # one character marks the end of each story
FIX = {"“": '"', "”": '"', "‘": "'", "’": "'",
       "–": "-", "—": "-", "…": "..."}
MIN_COUNT = 20  # characters rarer than this (e.g. "\t", "[") are dropped


def download(name, nbytes=None):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        byte_range = ["-r", f"0-{nbytes - 1}"] if nbytes else []
        subprocess.run(["curl", "-sSL", "--fail", *byte_range, "-o", path, URL + name], check=True)
    return open(path, encoding="utf-8", errors="ignore").read()


def to_bytes(text):
    for a, b in FIX.items():
        text = text.replace(a, b)
    text = text.replace("<|endoftext|>", EOT)
    text = text[: text.rfind(EOT) + 1]  # drop the story cut in half by the 200 MB limit
    return np.frombuffer(text.encode("ascii", "ignore"), dtype=np.uint8)


def main():
    os.makedirs(DATA, exist_ok=True)
    train = to_bytes(download(TRAIN, nbytes=200_000_000))
    val = to_bytes(download(VAL))

    counts = np.bincount(train, minlength=128)
    keep = [c for c in range(128) if counts[c] >= MIN_COUNT]
    lut = np.full(256, 255, dtype=np.uint8)  # byte -> token id (255 = drop)
    lut[keep] = np.arange(len(keep), dtype=np.uint8)

    for name, arr in [("train", train), ("val", val)]:
        ids = lut[arr]
        ids = ids[ids != 255]
        ids.tofile(os.path.join(DATA, f"{name}.bin"))
        print(f"{name}: {len(ids):,} characters")
    json.dump([chr(c) for c in keep], open(os.path.join(DATA, "vocab.json"), "w"))
    print(f"vocab: {len(keep)} characters")


if __name__ == "__main__":
    main()
