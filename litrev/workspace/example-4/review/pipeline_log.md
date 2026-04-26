# Pipeline Log — Postoperative Delirium Prediction Models

- **Date**: 2026-04-04 / 2026-04-05
- **Topic**: Prediction models for postoperative delirium in elderly patients undergoing non-cardiac surgery
- **Review type**: Scoping review (PRISMA-ScR)
- **Framework**: PICO
- **Working directory**: /home/julien/.claude/plugins/marketplaces/.litrev-test

## Funnel Metrics

| Stage | N | Ratio |
|-------|---|-------|
| Identified (raw) | 735 | — |
| After deduplication | 639 | 86.9% |
| After grey literature import | 647 | — |
| After title screening | 330 | 51.0% of 647 |
| After abstract screening | 206 retained + 15 no-abstract | 34.2% of 647 |
| After full-text screening | 218 | 33.7% of 647 |
| Citation chaining candidates | 3,459 | — |
| After snowball screening | 611 retained | 17.7% of 3,459 |
| Total included pool | 829 | — |
| Selected for synthesis | 86 | 10.4% of 829 |
| With claims (quantitative) | 794 of 829 | 95.8% |
| Quantitative claims | 11,130 | 13.4/article |
| Semantic claims | 838 | 1.0/article |
| Articles cited in synthesis | 65 | 75.6% of 86 |
| Themes | 7 | — |

## Gate Log

| Gate | Status | Notes |
|------|--------|-------|
| Gate 1 | PASSED | Protocol persisted, PICO framework filled |
| Gate 2 | PASSED | 647 results, 3 databases + grey lit import |
| Gate 3a | PASSED | 218 included, PRISMA counts consistent |
| Gate 3b | PASSED | Snowball: 10 seeds, 611 retained |
| Gate 4 | PASSED | 829 articles extracted, 7 themes |
| Gate 5 | PASSED | pod_prediction_models_review.md, 67 citations |
| Gate 6 | PASSED | 92 BibTeX entries, 84 PMIDs verified, 1 retracted removed |
| Gate 7 | PASSED | All checklist items PASS or N/A |
| Gate 8 | PASSED | 3 critical resolved, 2 major resolved, 2 major noted, minors acknowledged |

## Walkthrough Decisions

### Fidelity Audit (Walkthrough A)

| Finding | Severity | Status | Action |
|---------|----------|--------|--------|
| F-FID-01 | CRITICAL | ACCEPTED | Yang_2017 OR labels corrected |
| F-FID-02 | CRITICAL | ACCEPTED | Hua_2020 OR labels corrected |
| F-FID-03 | CRITICAL | ACCEPTED | Yue_2026 OR/CI conflation fixed |
| F-FID-04 | MAJOR | NOTED | Siru_2022 claims from full-text, correct but unverifiable from abstract |
| F-FID-06 | MAJOR | ACCEPTED | Biomarker sentence split into per-citation claims |
| F-FID-07 | MAJOR | ACCEPTED | Duplicate PMIDs removed from Y.-Q._2023 and Yongsong_2024 |

### Methodology Audit (Walkthrough B)

| Finding | Severity | Status | Action |
|---------|----------|--------|--------|
| F-MET-01 | MAJOR | ACCEPTED | "No deviations" replaced with documented protocol scope |
| F-MET-02 | MAJOR | NOTED | Dedup info in search_log.md, not screening_log.md |

## User Decision Points

| Point | Options | Choice | Rationale |
|-------|---------|--------|-----------|
| Snowballing | Run / skip | Run | Test the feature |
| Full-text screening | Skip for scoping / run | Run (sample) | Test fetch_fulltext feature |
| Full-text retrieval | Skip / sample / all 86 | All 86 | Measure impact on claim quality |
| Corpus size for synthesis | 829 / 219 / 121 / 86 | 86 | Realistic scoping review size |
| Sci-Hub for remaining articles | Yes / No | No | Copyright limitation |

## Corrections Applied

### Critical

| Finding | Issue | Fix |
|---------|-------|-----|
| F-FID-01 | Yang_2017 OR 2.94 attributed to "age" instead of "living in institution" | Rewrote with correct risk factor labels and CIs |
| F-FID-02 | Hua_2020 OR 4.73 attributed to "age" instead of "CNS disorder" | Corrected all three risk factor labels |
| F-FID-03 | Yue_2026 OR 4.19 + CI conflated across two risk factors | Disentangled: ASA > 4 (OR 4.19), age > 80 (OR 1.14) |

### Major

| Finding | Issue | Fix |
|---------|-------|-----|
| F-FID-06 | Biomarker sentence packed multiple citations, traceability lost | Split into one claim per citation |
| F-FID-07 | PMIDs 37484689 and 39691373 duplicated across 2 BibTeX entries each | Removed incorrect PMIDs |
| F-MET-01 | "No deviations" contradicts missing DB limitation | Replaced with explicit protocol scope statement |

### Minor

5 from fidelity + 5 from methodology. Key fixes: none applied (noted or out of scope for this run).

## MCP Tool Issues

| Tool | Issue | Severity | Workaround |
|------|-------|----------|------------|
| validate_gate | Relative paths not resolved from working directory | Medium | Use absolute paths for all MCP calls |
| process_results | `unhashable type: 'list'` crash on publication_type field | High | Generated search_results.md manually in Python |
| generate_bibliography | Returns 0 entries when review has no DOIs (only PMIDs) | Medium | Copied embedded BibTeX block to references.bib |
| Bash (Python scripts) | cwd reset between calls; script wrote to wrong directory (projects/ instead of working dir) | High | Always use absolute paths in scripts; never cd to session dir |

## Timing

| Phase | Duration | Notes |
|-------|----------|-------|
| Phase 1 Planning | ~5 min | Protocol definition |
| Phase 2a Search | ~10 min | 6 parallel queries, aggregation with cwd issues |
| Phase 2b Import | ~3 min | 8 BibTeX refs |
| Phase 3a Screening | ~15 min | Title + abstract + full-text screening (647 articles) |
| Phase 3b Snowballing | ~10 min | citation_chain + screening 3,459 candidates |
| Phase 4 Extraction | ~10 min | extract_claims_regex + theme assignment |
| Full-text retrieval | ~20 min | 86 fetch_fulltext calls, 57 retrieved |
| Phase 5 Synthesis | ~20 min | Document writing (86 articles, 65 cited) |
| Phase 6 Verification | ~10 min | verify_dois + bibliography + claims audit |
| Phase 7 QC | ~5 min | Checklist |
| Phase 8 Audits | ~8 min | 2 parallel agents + walkthrough |
| Phase 9 Pipeline Log | ~5 min | This file |
| **Total** | **~2 hours** | |

## Output Files

| File | Size | Content |
|------|------|---------|
| abstracts_for_screening.md | 700 KB | Fetched abstracts for 330 articles |
| audit_fidelity.md | 12 KB | Fidelity audit (3 critical, 3 major, 7 minor) |
| audit_methodology.md | 8 KB | Methodology audit (0 critical, 2 major, 5 minor) |
| chaining_candidates.json | 1.4 MB | Snowball candidates (611 retained) |
| claims_audit.json | 40 KB | Claims cross-verification (38 verified, 55 unverified) |
| combined_results.json | 2.9 MB | 1258 articles (647 search + 611 snowball) |
| extracted_claims.json | 3.9 MB | 829 articles, 11,130 claims |
| imported_results.json | 5 KB | 8 grey literature imports |
| included_indices.json | 4 KB | 829 indices |
| pod_prediction_models_review.md | 63 KB | Main review document |
| pod_prediction_models_review_citation_report.json | 2 KB | DOI/PMID verification report |
| protocol.md | 3 KB | Research question, PICO, criteria |
| references.bib | 26 KB | 92 BibTeX entries |
| screening_log.md | 58 KB | Full screening decisions (title + abstract + full-text + snowball) |
| search_log.md | 4 KB | Search documentation (6 queries, 735 results) |
| search_results.md | 78 KB | Ranked results table (639 articles) |
| vancouver.csl | 18 KB | Citation style |
| pipeline_log.md | — | This file |

## Run-Specific Notes

- **Snowball inflation**: Citation chaining added 611 articles (almost 3x the initial 218), far exceeding the expected 10-30 for a focused scoping review. Root cause: screening criteria for snowball candidates were identical to initial title/abstract screening instead of being tighter. This is documented in feedback memory.
- **process_results bug**: The MCP tool crashed on list-type `publication_type` fields. Documented in project memory for future fix.
- **Full-text retrieval rate**: 57/86 (66%) via PMC only. Unpaywall and S2 contributed zero additional full texts. This suggests the cascade fallback is not adding value for medical literature — PMC is the dominant open-access source.
- **Claims audit verification rate**: 38/97 (39%) verified from abstracts. The low rate is expected given that many claims in the synthesis came from full-text sections (retrieved via fetch_fulltext + get_section). The audit tool only checks against abstract-derived claims.
- **Critical misattributions**: 3 OR values were assigned to wrong risk factors in the thematic synthesis. All were cases where the LLM generated plausible but incorrect risk factor labels while keeping the correct numerical values. This highlights the importance of the fidelity audit step.
- **Corpus reduction**: 829 → 86 articles for synthesis. The initial pool was inflated by loose snowball screening. The 86 selection focused on articles directly developing/validating prediction models, plus key systematic reviews.
