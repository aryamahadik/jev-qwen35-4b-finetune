"""LR-03 Juliet Test Suite 1.3: C/C++ (SARD 112), Java (SARD 111) and C# (SARD 110); same terms (public domain in the US, CC0 1.0
for foreign rights). No split exists: own seeded 10% hold-out BY CWE DIRECTORY (family) is frozen first and the SAME CWE ids are
held out in every language (the hash key is the CWE id). train/ <- juliet_<lang>_train.zip (testcasesupport + the 90% CWE
directories); quarantine <- juliet_<lang>_holdout_cwe.zip. Source: https://samate.nist.gov/SARD/test-suites/{110,111,112}
"""
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import download_common as dc  # noqa: E402

DATASET = "juliet_1_3"
SUITES = {
    "c": {"url": "https://samate.nist.gov/SARD/downloads/test-suites/2017-10-01-juliet-test-suite-for-c-cplusplus-v1-3.zip",
          "page": "https://samate.nist.gov/SARD/test-suites/112", "ext": (".c", ".cpp", ".h")},
    "java": {"url": "https://samate.nist.gov/SARD/downloads/test-suites/2017-10-01-juliet-test-suite-for-java-v1-3.zip",
             "page": "https://samate.nist.gov/SARD/test-suites/111", "ext": (".java",)},
    "csharp": {"url": "https://samate.nist.gov/SARD/downloads/test-suites/2020-08-01-juliet-test-suite-for-csharp-v1-3.zip",
               "page": "https://samate.nist.gov/SARD/test-suites/110", "ext": (".cs",)},
}
_CWE = re.compile(r"(?:^|/)testcases/(CWE\d+)_")


def run():
    st = dc.Store(DATASET)
    counts = {}
    for lang, sp in SUITES.items():
        path, info = st.stage(sp["url"], "juliet-%s.zip" % lang)
        st.log.setdefault("staged_files", {})[lang] = {"sha256": info["sha256"], "bytes": info["bytes"], "url": sp["url"]}
        tr = st.train_path("juliet_%s_train.zip" % lang)
        hq = st.quar_path("juliet_%s_holdout_cwe.zip" % lang)
        os.makedirs(os.path.dirname(hq), exist_ok=True)
        n_train = n_hold = 0
        fam_train, fam_hold = set(), set()
        with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tr, "w", zipfile.ZIP_DEFLATED) as ztr, \
                zipfile.ZipFile(hq, "w", zipfile.ZIP_DEFLATED) as zho:
            for name in zin.namelist():
                if name.endswith("/") or not name.lower().endswith(sp["ext"]):
                    continue
                m = _CWE.search(name)
                if m:
                    fam = m.group(1)
                    if dc.holdout_unit("juliet|%s" % fam):
                        zho.writestr(name, zin.read(name))
                        n_hold += 1
                        fam_hold.add(fam)
                    else:
                        ztr.writestr(name, zin.read(name))
                        n_train += 1
                        fam_train.add(fam)
                elif "testcasesupport" in name:
                    ztr.writestr(name, zin.read(name))
        st.add_train_file("juliet_%s_train.zip" % lang, source_urls=[sp["url"]], rows=n_train,
                          note="rows = source files of the 90%% CWE directories; testcasesupport included")
        st.add_quar_file("juliet_%s_holdout_cwe.zip" % lang, role="own_frozen_holdout_by_cwe_directory", source_urls=[sp["url"]], rows=n_hold)
        counts[lang] = {"train_source_files": n_train, "holdout_source_files": n_hold, "train_cwe_dirs": len(fam_train),
                        "holdout_cwe_dirs": len(fam_hold), "holdout_cwe_ids": sorted(fam_hold)}
        st.clear_staging()
    q1 = "This software is not subject to copyright protection and is in the public domain."
    q2 = "the Test Suite is being made available to you under the CC0 1.0 Public Domain License"
    recs = [dc.licence_record(DATASET, "LR-03", quote=q1, quote_url=sp["page"], verify_url=sp["page"],
                              licence_class="US-government public domain + CC0 1.0 foreign rights (E2, LR-M2)", provenance="program",
                              tier="A", quote_alternatives=[q2]) for sp in SUITES.values()]
    main = dict(recs[0])
    main["per_suite"] = [{"language": lang, "page": sp["page"], "status": r["status"], "page_sha256": r["page_sha256"],
                          "fetched_utc": r["fetched_utc"]} for (lang, sp), r in zip(SUITES.items(), recs)]
    main["status"] = "OK" if all(r["status"] == "OK" for r in recs) else "QUOTE_NOT_VERIFIED"
    main["foreign_rights_quote"] = q2
    main["notes"] = ("Synthetic good/bad functions by CWE (NSA CAS). Foreign rights line: 'CC0 1.0 Public Domain License'. Guard F2: "
                     "no CVE ids. Languages C/C++, Java, C# (T65-B4).")
    st.write_licence(main)
    return st.finish({"counts": counts})


if __name__ == "__main__":
    print(dc.summarize(run()))
