"""LR-11 CommitPackFT (bigcode/commitpackft; Muennighoff et al., OctoPack 2023), LICENCE WHITELIST ONLY. Tier C check C13: the card
says 'Each sample comes from a code repository with a permissive license. The license is provided by the `license` field', yet that
field takes 13 values including agpl-3.0, lgpl-2.1, mpl-2.0, epl-1.0, artistic-2.0, isc, unlicense and unknown. Per-sample filter: keep
ONLY license in {mit, apache-2.0, bsd-2-clause, bsd-3-clause, cc0-1.0} (Opus LR-M3 one code whitelist; isc and unlicense are dropped).
Every language file (277) is streamed once (sha256 of the upstream bytes logged); only whitelisted rows are written, to
train/data/<lang>.jsonl.gz; per-licence and per-language counts (all rows, kept rows) go to the log. There is no test split in the
release (one 'train' file per language), so rule 2 of plan 16.3 applies: BEFORE mapping, a seeded 10% hold-out BY REPOSITORY
(dc.holdout_unit on 'commitpackft|<repo>'; a row with several comma-separated repos is held out when ANY of them is) is routed by
program into the quarantine store (quarantine/holdout10/<lang>.jsonl.gz, an internal G13 target, never trained and never opened).
No field is dropped (commit, old_file, new_file, old_contents, new_contents, subject,
message, lang, license, repos).
"""
import gzip
import hashlib
import json
import os
import sys
import time

import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402
import lr_tierc_common as tc  # noqa: E402

DATASET = "commitpackft"
HF = "bigcode/commitpackft"


def is_holdout_repo(repos):
    return any(dc.holdout_unit("commitpackft|" + r.strip()) for r in str(repos or "").split(",") if r.strip())


def stream_language(url, out_path, whitelist, hold_path, retries=4):
    """Stream one language file; write whitelisted rows to out_path (gzip jsonl). Returns stats dict."""
    last = None
    for attempt in range(retries):
        try:
            h = hashlib.sha256()
            nbytes = 0
            total = kept = held = 0
            by_lic = {}
            kept_by_lic = {}
            tmp = out_path + ".part"
            buf = b""
            htmp = hold_path + ".part"
            hold = [None]

            def emit(o, out):
                nonlocal kept, held
                if is_holdout_repo(o.get("repos")):
                    if hold[0] is None:
                        os.makedirs(os.path.dirname(hold_path), exist_ok=True)
                        hold[0] = gzip.open(htmp, "wt", encoding="utf-8", compresslevel=6)
                    hold[0].write(json.dumps(o, ensure_ascii=False) + "\n")
                    held += 1
                else:
                    out.write(json.dumps(o, ensure_ascii=False) + "\n")
                    kept += 1

            with requests.get(url, stream=True, timeout=120, headers={"User-Agent": dc.UA}) as r, gzip.open(tmp, "wt", encoding="utf-8", compresslevel=6) as out:
                r.raise_for_status()
                for chunk in r.iter_content(1 << 20):
                    if not chunk:
                        continue
                    h.update(chunk)
                    nbytes += len(chunk)
                    buf += chunk
                    *lines, buf = buf.split(b"\n")
                    for ln in lines:
                        if not ln.strip():
                            continue
                        o = json.loads(ln)
                        total += 1
                        lic = o.get("license")
                        by_lic[lic] = by_lic.get(lic, 0) + 1
                        if lic in whitelist:
                            kept_by_lic[lic] = kept_by_lic.get(lic, 0) + 1
                            emit(o, out)
                if buf.strip():
                    o = json.loads(buf)
                    total += 1
                    lic = o.get("license")
                    by_lic[lic] = by_lic.get(lic, 0) + 1
                    if lic in whitelist:
                        kept_by_lic[lic] = kept_by_lic.get(lic, 0) + 1
                        emit(o, out)
            if hold[0] is not None:
                hold[0].close()
                os.replace(htmp, hold_path)
            os.replace(tmp, out_path)
            return {"upstream_sha256": h.hexdigest(), "upstream_bytes": nbytes, "rows": total, "kept": kept, "held_out": held,
                    "by_license": by_lic, "kept_by_license": kept_by_lic}
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 + 3 * attempt)
    raise RuntimeError("stream failed %s: %s" % (url, last))


def run(only=None):
    st = dc.Store(DATASET)
    rev = dc.hf_revision(HF)
    st.log["upstream_revision"] = rev
    from huggingface_hub import HfApi
    files = sorted(s.rfilename for s in HfApi().dataset_info(HF, files_metadata=False).siblings if s.rfilename.startswith("data/") and s.rfilename.endswith("/data.jsonl"))
    if only:
        files = [f for f in files if f.split("/")[1] in only]
    wl = set(tc.CODE_WHITELIST_CPFT)
    per_lang, tot_lic, tot_kept_lic = {}, {}, {}
    n_total = n_kept = n_held = up_bytes = 0
    for f in files:
        lang = f.split("/")[1]
        url = dc.hf_url(HF, rev, f)
        rel = "data/%s.jsonl.gz" % lang.replace("/", "_")
        out_path = st.train_path(rel)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        hold_rel = "holdout10/%s.jsonl.gz" % lang.replace("/", "_")
        hold_path = st.quar_path(hold_rel)
        s = stream_language(url, out_path, wl, hold_path)
        per_lang[lang] = {k: s[k] for k in ("upstream_sha256", "upstream_bytes", "rows", "kept", "held_out")}
        for k, v in s["by_license"].items():
            tot_lic[k] = tot_lic.get(k, 0) + v
        for k, v in s["kept_by_license"].items():
            tot_kept_lic[k] = tot_kept_lic.get(k, 0) + v
        n_total += s["rows"]
        n_kept += s["kept"]
        n_held += s["held_out"]
        up_bytes += s["upstream_bytes"]
        if s["kept"]:
            st.add_train_file(rel, source_urls=[url], rows=s["kept"])
        else:
            os.remove(out_path)
        if s["held_out"]:
            st.add_quar_file(hold_rel, role="holdout10", source_urls=[url], rows=s["held_out"])
        print(lang, s["rows"], s["kept"], flush=True)
    st.log["per_language"] = per_lang
    counts = {"files": len(files), "rows_upstream": n_total, "rows_whitelisted_total": n_kept + n_held, "rows_kept_train": n_kept, "rows_held_out_quarantine": n_held, "upstream_bytes_streamed": up_bytes,
              "all_rows_by_license": dict(sorted(tot_lic.items(), key=lambda kv: -kv[1])),
              "kept_rows_by_license": dict(sorted(tot_kept_lic.items(), key=lambda kv: -kv[1]))}
    lic = tc.licence_with_checks(
        DATASET, "LR-11", quote="Each sample comes from a code repository with a permissive license. The license is provided by the `license` field for each sample.",
        quote_url="https://huggingface.co/datasets/bigcode/commitpackft", verify_url=dc.hf_card_url(HF, rev),
        licence_class="per-sample whitelist: mit, apache-2.0, bsd-2-clause, bsd-3-clause, cc0-1.0 (the card also lists agpl-3.0, lgpl-2.1, mpl-2.0, epl-1.0, artistic-2.0, isc, unlicense, unknown: all dropped)",
        provenance="human",
        notes="Check C13 (licence whitelist only). Human commit messages and human code; rule filters selected the rows (OctoPack paper); no "
              "model text in any field. Card YAML says 'license: mit' for the dataset as a whole, which is not the per-repo licence.",
    )
    st.write_licence(lic)
    return st.finish({"counts": counts})


if __name__ == "__main__":
    print(dc.summarize(run(set(sys.argv[1:]) or None)))
