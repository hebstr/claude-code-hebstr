# Litrev — Plan

## Current objective

Passe 2 — modular skill testing. 6c-fix-b done (re-enrichment). Next: Step 6c-fix-c (verify counts), then 6d (synthesize).

## Steps

| # | Step | Status |
|---|------|--------|
| 1 | Prepare workspace/example-4: new topic, PROMPT.md, CONTEXT files | done |
| 2 | Prepare a BibTeX or PMID list file to test Phase 2b (import_corpus) | done |
| P1 | Plugin conversion: move repo to `~/.claude/plugins/marketplaces/litrev/` | done |
| P2 | Plugin conversion: `.mcp.json` at plugin root with env vars, global entry cleared | done |
| P3 | Plugin conversion: register `"litrev@litrev": true` in `settings.json` | done |
| P4 | Plugin conversion: verify skill discovery + MCP connection (requires restart) | done |
| P5 | Plugin conversion: migrate memory to new project context path, remove symlink | deferred |
| P6 | Publish litrev-mcp to PyPI, switch .mcp.json to uvx | blocked |
| 3 | Run full pipeline end-to-end in workspace/example-4 | done |
| 4 | Triage issues found during run (4 parallel agents) | done |
| 5a | **Passe 1 — Fix C1: `process_results` crash on list `publication_type`** | done |
| 5b | **Passe 1 — Fix C2: `search_pubmed` no pagination beyond 200** | done |
| 5c | **Passe 1 — Fix C3: snowball candidates bypass screening in `litrev-screen`** | done |
| 5d | **Passe 1 — Fix C4/C5: `audit_claims` verifies number existence, not label match** | done |
| 5e | **Passe 1 — Fix M7: `quality` field never populated in extraction** | not-a-bug |
| 5f | **Passe 1 — Fix M9: multi-citation sentence duplication in `audit_claims`** | done |
| 6a | **Passe 2A — Search: relevance gate (required_terms + max_offtopic_pct)** | done |
| 6b | **Passe 2B — Screen: test screening on example-5 results** | done |
| 6b+ | **Passe 2B+ — `relevance_mode=filter` in `process_results`** | done |
| 6c | **Passe 2C — Extract: test claim extraction on screened articles** | done |
| 6c-fix-a | **Passe 2C fix — SKILL.md: cross-reference regex/semantic, direction guard, `provides_primary_data` field** | done |
| 6c-fix-b | **Passe 2C fix — Re-enrich ~30 empirical articles missing effect_size + ~10 with wrong direction** | done |
| 6c-fix-c | **Passe 2C fix — Verify: count effect_sizes, null/mixed directions, primary_data flags** | done |
| 6d | **Passe 2D — Synthesize: test synthesis on extracted claims** | todo |
| 7 | **Passe 3 — New end-to-end run (smaller topic) to validate integration** | todo |
| 8 | F26: design + implement orchestrator evals | todo |
| 9 | F27: design + implement synthesize evals | todo |

## Dependencies

- Steps 1-4: done
- 5a–5f: independent, can be parallelized
- Step 6a-6b done; 6b+ is independent (code change); 6c-6d sequential (each produces fixtures for the next)
- 6c-fix-a → 6c-fix-b → 6c-fix-c (sequential: SKILL.md first, then re-enrich, then verify)
- Step 6d depends on 6c-fix-c
- Step 7 depends on 6d
- Steps 8-9 depend on 7
- P5 deferred to a future session
- P6 blocked: package name permanent on PyPI — user wants to finalize naming first

## Example-4 triage summary (2026-04-05)

5 CRITICAL, 11 MAJOR, 10 MINOR issues found via 4 parallel audit agents.

**Code bugs to fix (Passe 1):**
- C1: `process_results` crash — `unhashable type: 'list'` on `publication_type` field
- C2: `search_pubmed` — PubMed Query 1 truncated 200/550, no pagination
- C3: `litrev-screen` — 611 snowball candidates included without abstract screening (100% acceptance)
- C4/C5: `audit_claims` — verifies number exists in abstract but not label/predictor correspondence
- M7: `quality` field null on all 829 articles — never populated
- M9: `extract_claims_regex` — multi-citation sentence propagates same stats to 5 keys

**Quality issues (not code bugs, addressed by Passe 2/3):**
- OpenAlex off-topic results (weak queries)
- 4/8 imports outside inclusion window
- 28 orphan BibTeX entries, 0 DOIs, duplicate PMIDs
- 57% claims unverified (abstract-only) not disclosed
- Causal drift in observational data presentation

## Resume context

Feature F complete (2026-04-04). E1 done. Plugin conversion P1-P4 done (2026-04-04).
Example-4 end-to-end run completed (2026-04-05, run by user). Triage done via 4 parallel agents.
Passe 1 complete (2026-04-05): 5 bugs fixed, 1 not-a-bug (M7 = correct behavior for scoping reviews). 347 tests, all green.
Passe 2A complete (2026-04-05): relevance gate implemented in `process_results`. 356 tests, all green.
- New: `_check_relevance()`, `required_terms` + `max_offtopic_pct` params
- Files modified: `mcp/src/litrev_mcp/tools/search.py`, `mcp/src/litrev_mcp/server.py`, `mcp/tests/test_process_results.py`, `skills/litrev-search/SKILL.md`
- Test workspace: `workspace/example-5/` (melatonin + sleep + autism, 403 articles, search complete)
- Finding: PubMed 93% on-topic, S2 36%, OpenAlex 11% — gate correctly blocks S2+OpenAlex
Passe 2B complete (2026-04-05): screening on example-5 PubMed-only results (243 articles).
- Relevance gate validated: S2 63.9% off-topic, OpenAlex 88.9% — correctly blocked.
- Title screening: 243 → 178 retained (65 excluded)
- Abstract screening: 178 → 142 retained + 5 no-abstract (31 excluded)
- Full-text screening: 147 → 147 retained (0 excluded, 1 duplicate cohort flagged)
- Files: `review/screening_log.md`, `review/included_indices.json`, `review/abstracts_for_screening.md`
- Documented S2/OpenAlex API precision limitations in `database_strategies.md` and memory
Passe 2B+ complete (2026-04-05): `relevance_mode="filter"` added to `process_results`.
- New param: `relevance_mode` (`"block"` default, `"filter"` keeps on-topic articles from noisy sources)
- `_check_relevance()` now returns `source_stats_detail` with `off_topic_indices` for filter mode
- Files modified: `mcp/src/litrev_mcp/tools/search.py`, `mcp/src/litrev_mcp/server.py`, `mcp/tests/test_process_results.py`, `skills/litrev-search/SKILL.md`
- 4 new tests, 360 total, all green
Passe 2C complete (2026-04-05): claim extraction on example-5 (147 articles).
- MCP `extract_claims_regex`: 635 quantitative claims, 96 articles with regex matches
- LLM enrichment: 313 semantic claims, quality assessment, 13 themes assigned
- Quality: 19 low risk, 110 moderate, 9 high, 9 unclear
- Key RCTs: Gringras 2017 (PedPRM, N=125), Hayashi 2022 (1/4mg, N=196), Cortesi 2012 (CR-melatonin+CBT, N=160), Wright 2011 (crossover, N=22)
- Key SR/MAs: Nogueira 2023, Xiong 2023, Rossignol 2011, Parker 2019, McDonagh 2019, Yang 2025, Sirao 2026
- Note: MCP resolves paths from its own cwd, not caller's workspace — absolute paths required
- File: `workspace/example-5/review/extracted_claims.json`
Quality audit of 2C found 3 issues requiring fix before synthesize:
1. **Effect sizes missing**: only 4/313 semantic claims have `effect_size`, despite 96 articles having regex claims with stats. SKILL.md doesn't instruct cross-referencing regex claims with semantic claims.
2. **Direction bias**: 84% positive (262/313). LLM defaults to "positive" even for reviews stating "evidence is limited/unclear". No calibration guard in SKILL.md.
3. **No primary data flag**: 67/147 are narrative reviews (no original data). Synthesize skill needs to distinguish primary vs secondary sources. Add `provides_primary_data` boolean.
Fix plan: 6c-fix-a (SKILL.md changes) → 6c-fix-b (re-enrich ~40 articles) → 6c-fix-c (verify counts) → 6d (synthesize).
Screening-level fix (filter by design) deferred to Passe 3.
6c-fix-b complete (2026-04-05): automated re-enrichment of extracted_claims.json.
- `provides_primary_data`: 45 true (RCT/cohort/cross-sectional/case-control/case series/qualitative/quasi-exp/open-label) / 102 false (narrative review/SR-MA/guideline/editorial)
- `effect_size` cross-referenced: 4 → 42 (automated regex→semantic matching + cleanup of 76 false positives: plain numbers like study counts and years)
- Direction recalibrated: 84% → 82.4% positive (4 hedge-word suspects fixed to mixed). >75% threshold flagged but reflects genuine literature consensus on melatonin efficacy for ASD sleep.
- 25/21 articles with 'statistic'-type regex claims have effect_size in semantic claims (full coverage).

## Post-stabilisation roadmap

Features planifiées après Passes 2-3 + evals. Détails dans DEFERRED.md.

| Priority | Feature | ID | Depends on |
|----------|---------|-----|------------|
| 1 | PRISMA flow diagram (SVG/Mermaid from screening_log.md) | F28 | — |
| 2 | Quarto Book export (review/ → navigable book with appendices) | F29 | F28 |
| 3 | Full-text screening (Phase 3c) | F30 | — |
| — | Umbrella reviews (AMSTAR 2) | DEFERRED | — |
| — | PyPI publish (litrev-mcp) | P6 | naming finalized |

Knowledge graph : écarté (rapport valeur/effort défavorable à cette échelle).

## Reference files

- `DEFERRED.md` — backlog items not on the current plan
- `mcp/` — MCP server source and tests
- `skills/` — 5 skills (orchestrator + 4 sub-skills)
- `workspace/example-4/` — end-to-end run outputs (reference only, not active work)
- `workspace/example-5/` — Passe 2 test workspace (melatonin/sleep/autism, active)
