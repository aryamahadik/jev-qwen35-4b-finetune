# Group C mappers (15 Oct 2026)

Sources: md_gene_ontology (CC BY 4.0, release 2026-07-26), md_cma (Cleveland Museum of Art, CC0; md_met is NOT used),
md_cordis_h2020 (11th source). Run each with `nice -n 10 .venv/bin/python -B meta_src/mappers/<file>.py` from c2_build
(shared engine: mdkit_c.py; raw downloads in meta_src/raw/{go,cma,cordis}).

11th-source decision (licence verified upstream, 15 Oct 2026, name check PASS for all five candidates):
- CORDIS H2020 chosen. data.europa.eu record https://data.europa.eu/api/hub/search/datasets/cordish2020projects lists, for
  cordis-h2020projects-csv.zip, the licence COM_REUSE "European Commission reuse notice" =
  http://data.europa.eu/eli/dec/2011/833/oj; https://commission.europa.eu/legal-notice_en: EU-owned content is CC BY 4.0.
  Domain "research funding (EU)" is new to the block. Caveat: closed programme (data refreshed Oct 2025 files).
- Not chosen: md_nasa_exoplanets (archive acknowledgement page has no licence text; only NASA media guidelines "generally
  not subject to copyright"), md_cms_hospitals (DCAT record has no licence field; policy pages script-rendered),
  md_nsf_awards and md_clinicaltrials (terms pages not readable).

Noise gate: each source has data/c2_md_parts/<source>/noise_gate/{chunks,key,manifest,prompts}. After the Haiku reads put the
answer files in noise_gate/answers/, then run meta_src/merge_md.py (see its docstring).
