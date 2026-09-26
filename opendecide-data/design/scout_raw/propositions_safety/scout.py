"""Scout HF datasets: metadata, licence, split sizes, a streamed sample, label stats.
Usage: python3 scout.py <out.json> id[:config] [id[:config] ...]
"""
import json, sys, time, traceback, urllib.request, urllib.parse
from huggingface_hub import HfApi
import datasets
from datasets import load_dataset, get_dataset_config_names

api = HfApi()
DS = "https://datasets-server.huggingface.co"


def get(url, timeout=30):
    try:
        import requests
        r = requests.get(url, timeout=timeout)
        return r.json()
    except Exception as e:
        return {"_error": str(e)[:300]}


def short(v, n=300):
    s = v if isinstance(v, str) else json.dumps(v, default=str)
    return s if len(s) <= n else s[:n] + "..."


def scout(spec):
    ds_id, _, cfg = spec.partition(":")
    cfg = cfg or None
    out = {"id": ds_id, "config_requested": cfg}
    # 1. hub metadata
    try:
        info = api.dataset_info(ds_id)
        cd = info.card_data.to_dict() if info.card_data else {}
        out["sha"] = info.sha
        out["gated"] = info.gated
        out["last_modified"] = str(info.last_modified)
        out["card_license"] = cd.get("license")
        out["card_license_name"] = cd.get("license_name")
        out["card_license_link"] = cd.get("license_link")
        out["tags_license"] = [t for t in (info.tags or []) if t.startswith("license:")]
        out["files"] = [s.rfilename for s in (info.siblings or [])][:40]
        out["has_script"] = any(f.endswith(".py") for f in out["files"])
    except Exception as e:
        out["hub_error"] = str(e)[:300]
    # 2. datasets-server sizes
    q = urllib.parse.quote(ds_id, safe="")
    sz = get(f"{DS}/size?dataset={q}")
    if "size" in sz:
        out["splits_rows"] = [(s["config"], s["split"], s["num_rows"]) for s in sz["size"]["splits"]]
    else:
        out["size_error"] = short(sz, 200)
    # 3. config names
    try:
        out["configs"] = get_dataset_config_names(ds_id)[:30]
    except Exception as e:
        out["configs_error"] = str(e)[:200]
    # 4. streamed sample
    attempts = [dict()]
    attempts.append(dict(revision="refs/convert/parquet"))
    for kw in attempts:
        try:
            args = [ds_id]
            kwargs = dict(streaming=True, **kw)
            if cfg:
                if "revision" in kw:
                    kwargs["data_dir"] = cfg
                else:
                    args.append(cfg)
            dd = load_dataset(*args, **kwargs)
            split = list(dd.keys())[0]
            it = iter(dd[split])
            rows = [next(it) for _ in range(2)]
            out["load_ok"] = {"kwargs": {k: v for k, v in kwargs.items() if k != "streaming"}, "splits_seen": list(dd.keys())}
            feats = dd[split].features
            out["features"] = short({k: str(v) for k, v in (feats or {}).items()}, 1200)
            out["sample"] = {k: short(v, 400) for k, v in rows[0].items()}
            out["sample2"] = {k: short(v, 200) for k, v in rows[1].items()}
            break
        except Exception as e:
            out.setdefault("load_errors", []).append({"kwargs": {k: v for k, v in kw.items()}, "err": (type(e).__name__ + ": " + str(e))[:400]})
    # 5. label statistics for the first config/split from datasets-server
    if out.get("splits_rows"):
        c0 = cfg or out["splits_rows"][0][0]
        stats = {}
        for (c, s, n) in out["splits_rows"]:
            if c != c0:
                continue
            st = get(f"{DS}/statistics?dataset={q}&config={urllib.parse.quote(c)}&split={urllib.parse.quote(s)}")
            if "statistics" in st:
                for col in st["statistics"]:
                    if col["column_type"] in ("class_label", "bool", "string_label") or col["column_name"] in ("label", "labels", "toxicity", "toxic", "answer", "Label", "label_text", "Email Type"):
                        stats[f"{s}.{col['column_name']}"] = short(col["column_statistics"].get("frequencies") or {k: col["column_statistics"].get(k) for k in ("mean", "min", "max", "histogram") if k in col["column_statistics"]}, 500)
            else:
                stats[s] = short(st, 150)
        out["label_stats"] = stats
    return out


if __name__ == "__main__":
    outp = sys.argv[1]
    try:
        res = json.load(open(outp))
    except Exception:
        res = {}
    for spec in sys.argv[2:]:
        t = time.time()
        try:
            res[spec] = scout(spec)
        except Exception as e:
            res[spec] = {"fatal": traceback.format_exc()[-800:]}
        res[spec]["secs"] = round(time.time() - t, 1)
        print("done", spec, res[spec].get("load_ok"), res[spec]["secs"], flush=True)
        json.dump(res, open(outp, "w"), indent=1, default=str)
