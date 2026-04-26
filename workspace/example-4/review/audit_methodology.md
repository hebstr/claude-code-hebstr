# Methodology Audit — Synthesis Critique

## Summary

The synthesis is well-structured, covers all PICO outcomes, and maintains generally good citation discipline throughout the Results sections. However, the review contains an internally contradictory claim of "no protocol deviations" while acknowledging missing databases, the Discussion section lacks citations entirely, and PRISMA deduplication details are undocumented in the screening log. Several limitations that are detectable from the pipeline artifacts (abstract-only claim extraction, single LLM screener) are partially disclosed but could be more explicit.

## Findings

### [F-MET-01] "No deviations" claim contradicted by database substitution — major — ACCEPTED (RESOLVED)

**Detail**: Line 62 of the synthesis states `**Deviations**: None from the pre-specified protocol.` However, the protocol (protocol.md) lists three databases: PubMed/MEDLINE, Semantic Scholar, and OpenAlex. The Limitations section (line 313) acknowledges that "EMBASE, Scopus, and Web of Science were not searched." While the protocol itself did not list those databases, the more significant issue is the internal contradiction: the synthesis simultaneously claims zero deviations and then lists missing database coverage as a limitation. If the protocol was followed exactly, the missing databases are not a deviation — but the Limitations section frames them as a gap. The wording should be reconciled: either the protocol scope was intentionally narrow (and this should be stated as a design choice in Methodology, not a limitation), or the protocol was aspirational and the deviation should be documented.

**Recommendation**: Replace "Deviations: None" with an explicit statement acknowledging the narrow database scope as a deliberate protocol choice, or document the omission of EMBASE/Scopus/WoS as a deviation from best practice (even if not from the written protocol).

---

### [F-MET-02] PRISMA deduplication step undocumented in screening log — major — NOTED

**Detail**: The synthesis (line 123) reports `Records identified from databases: 735 → After deduplication + grey literature import: 647`, implying 735 + 8 grey lit imports - 96 duplicates = 647. However, the screening log (`screening_log.md`) begins directly at "Pool: 647" with no deduplication section. There is no record of how many duplicates were found, which databases overlapped, or what deduplication method was used. The PRISMA-ScR flow requires transparent reporting of the deduplication step. Zero or near-zero duplicates between PubMed, Semantic Scholar, and OpenAlex would be suspicious given substantial overlap between these databases, but this cannot be assessed because the data is missing.

**Recommendation**: Add a "Deduplication" section to `screening_log.md` documenting: raw counts per database (PubMed: 335, Semantic Scholar: 200, OpenAlex: 200 — per line 152 of synthesis), number of duplicates removed, and deduplication method (DOI matching, title fuzzy matching, etc.).

---

### [F-MET-03] Discussion section contains no citations — minor

**Detail**: The entire Discussion section (lines 281-335) contains zero `[@...]` Pandoc citations, with the exception of three citations in lines 304 and 326 (which reference specific studies). The "Main Findings" subsection (lines 285-294), "Interpretation and Implications" paragraphs (lines 298-303), and the "Practice" and "Research" implication bullets (lines 302-303) make factual claims about the state of the field without any supporting citations. While discussion sections conventionally synthesize rather than cite exhaustively, statements like "The POD prediction field lags behind other domains (e.g., cardiovascular risk, sepsis prediction) in implementation science" (line 298) are verifiable claims that should be sourced.

**Recommendation**: Add citations to at least the comparative claims in Discussion (cardiovascular/sepsis comparison, claim about ML vs simple scores in practice).

---

### [F-MET-04] Claim extraction exclusively from titles and abstracts despite full-text retrieval — minor

**Detail**: The synthesis states (line 308) "Full-text retrieval for 66% of synthesized articles (57/86)" as a strength. However, `extracted_claims.json` contains 646 claims sourced from "title" and 192 from "abstract", with zero claims sourced from "fulltext". The Limitations section does not disclose that quantitative claim extraction was limited to title and abstract fields despite full-text availability. The synthesis narrative does incorporate full-text details (e.g., model architectures, feature counts), but the structured claim extraction pipeline did not leverage full-text content.

**Recommendation**: Add a limitation noting that structured claim extraction (regex-based) was performed on titles and abstracts only. The full-text retrieval enriched the narrative synthesis but did not feed into the quantitative claims dataset.

---

### [F-MET-05] Cumulative language pattern in Results — minor

**Detail**: The Results sections use cumulative language ("confirmed these findings", "confirmed that elevated serum CRP") at lines 204, 210, 242, and 261 without confronting contradictions between studies. For example, line 204: "Dong et al. confirmed these findings in geriatric spinal surgery patients." The synthesis presents all studies as mutually reinforcing without discussing cases where models disagreed, risk factor rankings diverged, or effect sizes were substantially different across populations. The Controversy paragraph in Discussion (line 294) raises ML vs. clinical scores as unresolved, but contradictions at the individual study level (e.g., varying AUC ranges, conflicting risk factor rankings) are not surfaced.

**Recommendation**: Add a paragraph in Results or Discussion explicitly identifying where individual study findings conflict (e.g., studies reporting different top predictors, divergent AUC ranges for similar model types) and discussing possible explanations (population differences, outcome definitions, model specifications).

---

### [F-MET-06] Impact on early detection and length of stay — thin coverage relative to PICO outcome — minor

**Detail**: PICO Outcome (3) is "Impact on early detection and length of stay." The corresponding synthesis section (lines 257-263) cites only 4 studies (Benjamin, Shengjie, Lauren, Cheng-Chou) and explicitly acknowledges the gap: "prospective studies demonstrating that routine use of prediction models reduces delirium incidence or hospital length of stay are conspicuously absent." This is honest reporting, but the section is disproportionately thin (7 lines) compared to the clinical scores section (37 lines for 26 studies) and the ML section (29 lines for 16 studies). The Knowledge Gaps section (line 271) repeats the same point.

**Recommendation**: No content change needed — the gap is real and honestly reported. Consider consolidating the "Impact" section content into Knowledge Gaps to avoid the near-repetition.

---

### [F-MET-07] Single-reviewer LLM screening not disclosed in synthesis Limitations — minor

**Detail**: The screening log (line 523) states: "Screening performed by a single AI reviewer (LLM). PRISMA recommends dual independent screening." This limitation is not carried over to the synthesis Limitations section (lines 310-316). The synthesis mentions "AI-assisted tools" and "human verification at each phase gate" (line 312) but does not explicitly state that screening was performed by a single LLM reviewer without a second independent human screener.

**Recommendation**: Add a bullet to the Limitations section: "Screening was performed by a single AI reviewer; PRISMA recommends dual independent screening. A human second reviewer did not independently validate a sample of exclusion decisions."

---

## Summary table

| Severity | Count | Findings |
|----------|-------|----------|
| Critical | 0 | — |
| Major | 2 | F-MET-01, F-MET-02 |
| Minor | 5 | F-MET-03, F-MET-04, F-MET-05, F-MET-06, F-MET-07 |
