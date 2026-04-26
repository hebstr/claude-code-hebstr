# Deferred

Findings reportés lors des code reviews. À revisiter périodiquement.

| Date | Finding | Fichier | Raison du report |
|------|---------|---------|-----------------|
| ~~2026-03-27~~ | ~~FN-3/GAP-3 : Import path pour corpus pré-existant (PMIDs, BibTeX, PDFs → combined_results.json)~~ | ~~skills/litrev/SKILL.md, skills/litrev-search/SKILL.md~~ | DONE (2026-04-04): Feature F — `import_corpus` tool, 15 tools, 338 tests |
| 2026-04-01 | Support umbrella review (review of reviews) — workflow différent : recherche de SR/MA, critères adaptés, qualité via AMSTAR 2 | skills/litrev/SKILL.md Phase 1 | Actuellement flaggé non supporté dans l'orchestrateur |
| ~~2026-04-02~~ | ~~Tests unitaires manquants pour 5/10 modules MCP tools (abstracts, openalex_search, pubmed_search, s2_search, snowball)~~ | ~~mcp/tests/~~ | DONE (2026-04-04): 91 tests ajoutés, 288 total |
| 2026-03-31 | F24 — Screen evals: ajouter test edge-case pool vide | skills/litrev-screen/evals/evals.json | Amélioration eval, pas un bug |
| 2026-03-31 | F25 — Extract evals: ajouter test edge-case 0 articles inclus | skills/litrev-extract/evals/evals.json | Amélioration eval, pas un bug |
| 2026-03-31 | F26 — Orchestrator: créer une suite d'evals | skills/litrev/evals/ | Evals absentes, nécessite conception dédiée |
| 2026-03-31 | F27 — Synthesize: créer une suite d'evals | skills/litrev-synthesize/evals/ | Evals absentes, nécessite conception dédiée |
| 2026-04-04 | E2 — `search_scopus` : Elsevier API, dedup-compatible output | mcp/src/litrev_mcp/tools/ | Nécessite clé API institutionnelle (insttoken) ; couverture déjà assurée par OpenAlex |
| 2026-04-04 | E3 — `search_wos` : Clarivate Starter API | mcp/src/litrev_mcp/tools/ | Nécessite abonnement institutionnel + licence API ; couverture déjà assurée par PubMed + OpenAlex + S2 |
| 2026-04-01 | No eval coverage for rapid review + no-abstract path | skills/litrev-screen/evals/ | Requires creating new test data with missing abstracts for a rapid review scenario |
| 2026-04-01 | file_exists assertion checks review/ but eval sandbox writes to outputs/ | skills/litrev-extract/evals/evals.json | Fix depends on eval harness sandbox directory mapping behavior |
| 2026-04-05 | F28 — PRISMA flow diagram: MCP tool generating PRISMA 2020 diagram (SVG/Mermaid) from screening_log.md counters | mcp/src/litrev_mcp/tools/ | Quick win, utile indépendamment du Quarto Book |
| 2026-04-05 | F29 — Quarto Book export: phase 10 dans l'orchestrateur ou outil MCP. Génère `_quarto.yml` + `.qmd` wrappers depuis review/. Chapitres : protocol, search, screening, extraction, review, references. Appendices : audit fidelity, audit methodology, AI process (pipeline_log + metadata LLM), PRISMA flow. Transcript Claude Code en supplementary material (pas un chapitre). | skills/litrev/SKILL.md, mcp/ | Post-stabilisation. Dépend de F28 (PRISMA flow) |
| 2026-04-05 | F30 — Full-text screening (Phase 3c): pass de screening sur full-text des articles inclus, exploitant fetch_fulltext + get_section | skills/litrev-screen/SKILL.md | Gap méthodologique pour revues systématiques complètes |
| 2026-04-05 | F31 — Study design filter in screening: option to exclude narrative reviews/editorials/commentaries for systematic reviews. Configurable per review type (SR=strict, scoping=permissive). 46% narrative reviews in example-5 pool dilute evidence quality. | skills/litrev-screen/SKILL.md | Passe 3 — screening improvement, not extraction fix |
