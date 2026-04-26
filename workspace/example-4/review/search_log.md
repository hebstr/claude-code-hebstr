# Search Log — Postoperative Delirium Prediction Models

## PubMed — Query 1 (Broad: prediction + elderly + surgery)

- **Date searched**: 2026-04-04
- **Date range**: 2015–2026
- **Query**: `(("Delirium"[MeSH] OR "postoperative delirium"[tiab] OR "POD"[tiab] OR "acute confusion"[tiab]) AND ("Risk Assessment"[MeSH] OR "Predictive Value of Tests"[MeSH] OR "prediction"[tiab] OR "predictive model"[tiab] OR "risk score"[tiab] OR "risk stratification"[tiab] OR "nomogram"[tiab] OR "clinical decision support"[tiab]) AND ("Aged"[MeSH] OR "elderly"[tiab] OR "older adults"[tiab] OR "geriatric"[tiab]) AND ("Surgical Procedures, Operative"[MeSH] OR "surgery"[tiab] OR "surgical"[tiab] OR "postoperative"[tiab] OR "perioperative"[tiab]) NOT ("Cardiac Surgical Procedures"[MeSH] OR "cardiac surgery"[tiab]) NOT ("Child"[MeSH] OR "pediatric"[tiab]))`
- **Total in PubMed**: 550
- **Results returned**: 200 (limit)
- **Status**: SUCCESS
- **Has API key**: yes

## PubMed — Query 2 (ML/EHR focused)

- **Date searched**: 2026-04-04
- **Date range**: 2015–2026
- **Query**: `(("Delirium"[MeSH] OR "postoperative delirium"[tiab]) AND ("Machine Learning"[MeSH] OR "Artificial Intelligence"[MeSH] OR "machine learning"[tiab] OR "deep learning"[tiab] OR "artificial intelligence"[tiab] OR "Electronic Health Records"[MeSH] OR "EHR"[tiab] OR "electronic health record"[tiab] OR "routine data"[tiab]) AND ("Surgical Procedures, Operative"[MeSH] OR "surgery"[tiab] OR "surgical"[tiab] OR "postoperative"[tiab]) NOT ("Cardiac Surgical Procedures"[MeSH] OR "cardiac surgery"[tiab]))`
- **Results returned**: 135
- **Status**: SUCCESS
- **Has API key**: yes

## Semantic Scholar — Query 1

- **Date searched**: 2026-04-04
- **Date range**: 2015–2026
- **Query**: `postoperative delirium prediction model elderly surgery risk score`
- **Fields of study**: Medicine
- **Results returned**: 100
- **Status**: SUCCESS
- **Has API key**: yes

## Semantic Scholar — Query 2

- **Date searched**: 2026-04-04
- **Date range**: 2015–2026
- **Query**: `machine learning delirium prediction surgical EHR electronic health record`
- **Fields of study**: Medicine
- **Results returned**: 100
- **Status**: SUCCESS
- **Has API key**: yes

## OpenAlex — Query 1

- **Date searched**: 2026-04-04
- **Date range**: 2015–2026
- **Query**: `postoperative delirium prediction model`
- **Results returned**: 100
- **Status**: SUCCESS

## OpenAlex — Query 2

- **Date searched**: 2026-04-04
- **Date range**: 2015–2026
- **Query**: `delirium risk score elderly surgery`
- **Results returned**: 100
- **Status**: SUCCESS

## Summary

| Database | Queries | Succeeded | Failed | Total Results |
|----------|---------|-----------|--------|---------------|
| PubMed | 2 | 2 | 0 | 335 |
| Semantic Scholar | 2 | 2 | 0 | 200 |
| OpenAlex | 2 | 2 | 0 | 200 |
| **Total** | **6** | **6** | **0** | **735** |

After deduplication: **639 unique articles** (96 duplicates removed: 90 by PMID, 0 by DOI, 6 by title)

### Grey literature

- Sources checked by user: yes (import_corpus.bib)
- Format: BibTeX, 8 records parsed, all enriched with citation counts
- References added: 8 (0 duplicates with existing results)
- After merge: **647 unique articles**

### Databases not searched

- EMBASE: requires institutional access (not suggested — scoping review, 3 databases sufficient)
- Scopus / Web of Science: requires institutional access

### MCP tool issues

- `process_results` crashed with `unhashable type: 'list'` on `publication_type` field — `search_results.md` generated manually in Python as workaround
