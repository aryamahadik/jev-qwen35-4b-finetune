# Sources for the G-proxy (A42-D 12) and the metadata block (A42-D 8)

Built 15 Oct 2026 (network allowed for this task only). No mapper or task generator exists (A42-D 8.5: the name check comes first).

## Files
- `SOURCES_CANDIDATES.json`: 8 G-proxy and 19 metadata candidates (27 total; the two role lists are disjoint). Each entry has publisher, host, upstream id, dataset URL, licence name and URL, how the licence was verified, domain, record count, gold fields, 3-5 task templates with how gold is computed, freshness and disjointness notes.
- `source_name_check.py`: prints only `<id> PASS` or `<id> HIT`. Uses `g13_c2.keyword_hashes` (read-only import) on name, publisher, host (bare, with and without `www.`, and as URL), upstream id, licence URL and dataset URL. Compares with `sealed_hashes/keyword_hashes.jsonl` and, when present, `sealed_hashes_ac/keyword_hashes.jsonl` and `sealed_hashes_ac/source_keywords_prelim.jsonl`. `--exports ohs4` uses the OHS-4 export only.
- `c1_denylist_check.py`: clear-text check against the 330 C1 source names, the deny-list entries and aliases, and the G-block source words (prints what matched; nothing sealed is read).
- `name_check_ohs4_result.txt`: the run against the OHS-4 export plus the OHS-AC preliminary file (the AC folder held only `source_keywords_prelim.jsonl` when run).
- `samples/`: <= 50 records per source (names, addresses, phones and e-mails removed). Not for training.

## Name-check results (run now)
- OHS-4 export only: **26 PASS, 1 HIT (md_fdc)**. All 8 G-proxy candidates PASS.
- OHS-4 + OHS-AC preliminary: **25 PASS, 2 HIT (md_fdc, md_peps)**. md_peps hits only in the AC preliminary file.
- Per 8.5 a HIT removes the whole source. The checker prints no keyword, so the cause is unknown to the C2 side.
- The final mix needs a second run (8.5), and the full OHS-AC export is not here yet.

## Clear-text check (C1 names, deny-list, G-block)
- All 27 are CLEAR except the platform word "github" in the hosts of gp_ourairports (`davidmegginson.github.io`), md_met and md_cma (GitHub licence pages). A16 (a) says a bare platform word never matches on its own.
- C1 holds openFDA, CPSC, NHTSA, NOAA Storm Events, MSHA, O*NET, US Census NAICS and similar. None of these is used. USDA FDC, USGS, CMS and EPA fueleconomy are different datasets and agencies.

## Counts against the bars
- **G-proxy:** 8 candidates (need >= 5), 7 PASS-able with record counts; row supply is far above 2,000 for every source except gp_pa_personal_care (992) and gp_fueleconomy (not counted). Plan for 3 sources at about 700-800 rows each with a yes share of 40-50% set by seeded sampling per task (no source above 40%). All templates are yes/no heads on typed fields.
- **Metadata:** 19 candidates (need >= 15), 17 PASS on both exports. Row supply per source is large except md_peps (745, and a HIT in the AC file), md_nasa_exoplanets (6,451), md_cms_hospitals (5,419).
- Block arithmetic: 8,000-12,000 rows over 11 sources with a 15% cap means about 730-1,090 rows per source, 40-80 tasks each, so about 10-25 rows per task (<= 200 allowed). Card-free >= 30% is a mapper choice (direct metadata questions with no card); no source forces cards.

## Licence status (the weak point)
| Status | Sources |
|---|---|
| Verified in this session | gp_ourairports, the six Socrata sources (record licence from `/api/views/<id>.json`), md_openalex (CC0), md_musicbrainz (CC0 core data), md_usgs (public domain), md_geonames (CC BY), md_gbif (CC BY 4.0), md_met and md_cma (CC0), md_fsa (OGL v3), md_worldbank (CC BY 4.0; confirm that dataset 0037800 is the Projects dataset), md_ror (CC0), md_gene_ontology (CC BY 4.0), md_peps (PD/CC0), md_fdc (CC0, from the API OpenAPI spec) |
| Partial or not found; needs an Opus ruling | md_clinicaltrials (terms page not readable; submitters may claim copyright), md_cms_hospitals, md_nsf_awards, md_nasa_exoplanets, md_cordis_h2020 (EC notice says CC BY 4.0, dataset record not read), gp_fueleconomy |
| Do not use | md_openlibrary (no licence statement found) |

## Open issues for the orchestrator
1. **Socrata overlap with the G-block.** The six Socrata G-proxy datasets are all catalog entries (name and description) in the G-block `open_data` texts, because that block took every permissive-licence dataset on 114 portals. The rows differ from those texts. A42-D 12.1 asks for `fetch_socrata.py` sources, so a ruling is needed. Non-Socrata G-proxy options: gp_ourairports (verified) and gp_fueleconomy (licence open).
2. **Enough verified, PASS metadata sources?** After the HITs, the verified PASS pool is: openalex, musicbrainz, worldbank, usgs, geonames, gbif, fsa, ror, gene_ontology, plus one of met or cma (both would put 'art' at about 18% of the block, under the 20% cap). That is 10 distinct sources. The 11th must be a partial-licence source (clinicaltrials, cms_hospitals, nsf_awards, nasa_exoplanets or cordis) or a new one.
3. **Domains** in the 10-source pool: scholarly publishing (openalex, ror), music, development finance, geoscience, geography, biodiversity, ontology/bioinformatics, food safety, art. At least 8 domains, none above 20%.
4. **Rate limits.** OpenAlex without a key shares a $0.10 daily budget per IP; MusicBrainz allows 1 request per second (use a dump); the Met API is one request per object. The mapper agents need snapshots or keys.
5. **Privacy.** Socrata licence and registry sources carry personal names (CCB contractors, rental owners, liquor licensees); samples and templates use only categorical and date fields. FSA business names are not used.
6. **Freshness.** All sources were updated in 2025-2026 except md_cordis_h2020 (closed programme) and gp_howard_rental (Dec 2025).
