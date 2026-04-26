# Fidelity Audit -- Claims vs Sources

## Summary

- **97 claims** extracted from **64 citation keys** across 86 synthesized articles
- Automated audit: 38 VERIFIED, 55 UNVERIFIED, 4 NO_ABSTRACT, 0 NO_EXTRACTION
- BibTeX entries: 92 total, 28 orphans (not cited in review text)
- Duplicate PMIDs: 2 pairs sharing the same PMID across distinct BibTeX entries
- Critical misattributions identified: 2 (OR values attributed to wrong risk factors)

---

## Findings

### [F-FID-01] Yang_2017 -- OR values attributed to wrong risk factors -- critical -- ACCEPTED (RESOLVED)

**Detail**: The review states (line 204):

> "Yang et al. pooled risk factors for POD after hip fracture and found age (OR 2.94), dementia (OR 2.46), and depression (OR 2.21) as the top three predictors"

However, the automated audit matched these values against the abstract verbatim, which reads:

- OR 2.94 = "living in an institution" (95% CI 1.65--5.23)
- OR 2.46 = "heart failure" (95% CI 1.72--3.53)
- OR 2.21 = "total hip arthroplasty" (95% CI 1.16--4.22)

The review attributes three OR values to completely different risk factors than those in the source abstract. This is a context vs result confusion: the correct risk factors were replaced by plausible-sounding but incorrect ones.

**Recommendation**: Rewrite this sentence using the actual risk factors from the Yang_2017 abstract, or if the intent was to cite different risk factors from this meta-analysis, verify against the full text and use the correct OR values.

---

### [F-FID-02] Hua_2020 -- OR values attributed to wrong risk factors -- critical -- ACCEPTED (RESOLVED)

**Detail**: The review states (line 234):

> "Hua et al. reported a pooled POD incidence after spinal surgery with consistently identified risk factors including age (OR 4.73), dementia (OR 1.16), and depression (OR 1.10)"

The audit matched these values against the abstract, which reads:

- OR 4.73 = "central nervous system disorder" (95% CI 4.30--5.19)
- OR 1.16 = "age" (95% CI 1.05--2.47)
- OR 1.10 = "blood loss" (95% CI 1.01--1.20)

Only the OR 1.16 = age mapping is correct. OR 4.73 is attributed to "age" in the review but actually corresponds to "central nervous system disorder." OR 1.10 is attributed to "depression" but corresponds to "blood loss."

**Recommendation**: Correct the risk factor labels to match the abstract. The strongest predictor (OR 4.73) was CNS disorder, not age.

---

### [F-FID-03] Yue_2026 -- OR = 4.19 attributed to age instead of ASA classification -- critical -- ACCEPTED (RESOLVED)

**Detail**: The review states (line 242):

> "Yue et al. synthesized evidence on POD after hip fracture in the elderly, confirming advanced age (OR = 4.19, 95% CI 1.08--1.21) and cognitive impairment as dominant risk factors"

The audit verbatim from the abstract reads:

> "age > 80 (OR = 1.14, 95% CI [1.08--1.21]), ASA classification > 4 (OR = 4.19, 95% CI [1.85--9.52]); dementia (OR = 3.42, ...)"

Two errors: (1) OR 4.19 belongs to ASA classification > 4, not to advanced age. (2) The 95% CI 1.08--1.21 belongs to age > 80 (OR 1.14), not to OR 4.19. The numbers from two different risk factors have been conflated into a single claim.

**Recommendation**: Rewrite as: "Yue et al. confirmed ASA > 4 (OR 4.19, 95% CI 1.85--9.52), dementia (OR 3.42), and age > 80 (OR 1.14, 95% CI 1.08--1.21) as dominant risk factors."

---

### [F-FID-04] Siru_2022 -- multiple numerical claims unverified -- major -- NOTED

**Detail**: The review (line 176) reports detailed performance metrics for Siru_2022:

> "achieving an AUC of 0.921 (95% CI: 0.918--0.923) with LightGBM at a 12-hour prediction window [...] logistic regression (AUC 0.87), random forest (F1 0.334), and neural network (AUC 0.772)"

All specific numerical values (0.921, 0.87, 0.334, 0.772) and the sample sizes (34,035 patients, 331,489 CAM assessments, 896 features) are marked UNVERIFIED. The article was not found in `combined_results.json` by its citation key. Without abstract confirmation, these precise figures cannot be traced to source text.

**Recommendation**: Verify these numbers against the original article (PMID 36343112). If the values come from the full text rather than the abstract, annotate this in the review or provide a page/table reference.

---

### [F-FID-05] Ahn_2025 -- partial verification, several secondary metrics unverified -- minor

**Detail**: For Ahn_2025, the primary AUROC (0.870) and its CI (0.789--0.935) are VERIFIED. However, the comparison model AUCs (XGBoost 0.801, LightGBM 0.798, Random Forest 0.799) and the ICI value (0.107) are UNVERIFIED, likely because they appear only in the full text or supplementary materials rather than the abstract.

**Recommendation**: These values are plausible given the verified primary result. Consider adding a note that comparison values come from full-text data, or verify against the published article.

---

### [F-FID-06] Biomarker claims with wrong citation key attribution -- major -- ACCEPTED (RESOLVED)

**Detail**: In line 214, the review lists novel biomarkers in a comma-separated sentence:

> "serum ferritin [@Xianghan_2024], plasminogen activator inhibitor-1 (PAI-1, p < 0.0001 for POD prediction) [@Kazuhito_2022], glycated hemoglobin (HbA1c) as a predictor in diabetic patients (95% CI 1.34--6.52, p = 0.007) [@M._2025a], uric acid (lower levels associated with higher POD risk, p = 0.015) [@Lin_2022a]"

The automated audit flagged many of these statistics as UNVERIFIED for Xianghan_2024, Kazuhito_2022, and Ida_2020. The claim extractor appears to have propagated statistics from the entire sentence to multiple citation keys incorrectly (the p-values and CIs from one study were attributed to others). For example, "p < 0.0001" is attributed to both Kazuhito_2022 and Xianghan_2024 in the audit, and "95% CI 1.34--6.52, p = 0.007" (which belongs to M._2025a per the review text) was also attributed to Kazuhito_2022, Xianghan_2024, Lin_2022a, and Ida_2020.

This is primarily an automated extraction artifact, but the underlying claim sentence packs too many studies into one sentence, making claim-source traceability difficult.

**Recommendation**: Break this sentence into individual claim-per-citation statements to improve traceability. Verify the p < 0.0001 for Kazuhito_2022 and p = 0.015 for Lin_2022a against their respective abstracts.

---

### [F-FID-07] Duplicate PMIDs in references.bib -- major -- ACCEPTED (RESOLVED)

**Detail**: Two pairs of BibTeX entries share the same PMID, suggesting either erroneous bibliography generation or actual duplicates:

1. **PMID 37484689**: `Neto_2023` ("Developing and validating a machine learning ensemble model...") and `Y.-Q._2023` ("Risk prediction models for postoperative delirium... systematic review and meta-analysis"). These are different titles in the same journal (Frontiers in Aging Neuroscience, 2023) but share a PMID. At least one PMID is incorrect.

2. **PMID 39691373**: `Yoshimura_2024` ("Development and validation of a machine learning model... gastrointestinal surgery") and `Yongsong_2024` ("Causal relationship between dementia and delirium... Mendelian randomization"). These are clearly different articles with different titles but share the same PMID. At least one is wrong.

**Recommendation**: Look up the correct PMIDs for these four articles and fix the bibliography. Verify that the abstracts used for claim extraction correspond to the correct articles.

---

### [F-FID-08] 28 orphan BibTeX entries -- minor

**Detail**: The following 28 keys appear in `references.bib` but are never cited in the review text:

Ai-lin_2023, Annie_2020a, Annina_2019, Changgui_2015, Chantal_2019, Dong_2025b, E._2023b, Huawei_2021, Jiahan_2022, Jia-Yi_2020, John_2018, Juan_2020, Kim_2022, Rong_2023, S._2019b, Samuel_2020, Ties_2019a, Wang_2025a, X._2025, Xiaoling_2025, Xinchun_2019, Y._2022a, Yang-hui_2022, Yanwei_2025, Yongsong_2024, Zhang_2025, Zhihua_2026a, Zhihua_2026b

These represent articles that were included in the bibliography but not cited in the narrative synthesis. Some may have been part of the screening pool or citation chaining and were never incorporated into the text.

**Recommendation**: Either cite these articles where relevant in the review, or remove them from `references.bib` to avoid inflating the reference count. Notably, several of these (Zhang_2025, Zhihua_2026a, Zhihua_2026b, Annie_2020a, John_2018) are prediction model studies that could strengthen the synthesis.

---

### [F-FID-09] Aldecoa_2017 and Evered_2018 -- NO_ABSTRACT, incidence range untraceable -- minor

**Detail**: Four claims (the "10% to over 50%" incidence range) are attributed to Aldecoa_2017 and Evered_2018, but both articles had no abstract available in `combined_results.json`. These are well-known reference works (ESA guideline and Nomenclature Consensus respectively), and the 10--50% range is a widely cited figure in the field.

**Recommendation**: While the claim is likely accurate from domain knowledge, it cannot be verified from the available data. Consider adding the abstracts to the search results, or citing a source where the abstract is available.

---

### [F-FID-10] Daiyu_2021 -- OR values unverified -- minor

**Detail**: The review reports specific ORs for Daiyu_2021 (OR 4.364 for age, OR 4.640 for diabetes, OR 2.528 for low albumin). All three are marked UNVERIFIED -- the article was found in `combined_results.json` but without an abstract containing these numbers. These may come from full-text extraction.

**Recommendation**: Verify these ORs against the published full text (PMID 34258278). If confirmed, note the source as full text rather than abstract.

---

### [F-FID-11] Wei_2024 and Yu_2024 -- OR values unverified -- minor

**Detail**: OR 8.816 for frailty (Wei_2024) and OR 4.681 (Yu_2024) are both UNVERIFIED. These are strong effect sizes that significantly shape the narrative around frailty as a predictor.

**Recommendation**: Verify against original abstracts or full texts. The OR 8.816 is unusually high and warrants particular attention.

---

### [F-FID-12] Semantic duplicates across meta-analyses -- minor

**Detail**: Multiple meta-analyses cite overlapping risk factors with similar ORs without being flagged as convergent evidence:

- Yang_2017 and Yue_2026 both report pooled ORs for age and cognitive impairment in hip fracture populations
- Dong_2025 confirms findings in spinal surgery patients
- Niu_2025 reports similar patterns in orthopedic populations

The review correctly presents these as separate findings but does not explicitly note the degree of overlap in primary studies included in these meta-analyses, which could inflate the apparent convergence.

**Recommendation**: Add a sentence noting potential overlap in primary studies across meta-analyses covering similar populations and timeframes.

---

### [F-FID-13] Tu_2025 -- "median AUC of 0.82" matched against wrong verbatim -- minor

**Detail**: The review states Tu_2025 found "a median AUC of 0.82 across 15 studies." The audit marked value 0.82 as VERIFIED, but the matched verbatim reads: "sensitivity of 0.73 [...] and a specificity of 0.79 [95% CI, 0.74-0.82]." The 0.82 matched to the upper bound of a specificity CI, not to a median AUC. The "15" matched against a date ("February 15, 2025"), not the number of studies. These are false-positive verifications.

**Recommendation**: Re-verify the median AUC and number of included studies for Tu_2025 against the actual abstract or full text.

---

## Summary table

| Severity | Count | Findings |
|----------|-------|----------|
| Critical | 3 | F-FID-01, F-FID-02, F-FID-03 |
| Major | 3 | F-FID-04, F-FID-06, F-FID-07 |
| Minor | 7 | F-FID-05, F-FID-08, F-FID-09, F-FID-10, F-FID-11, F-FID-12, F-FID-13 |
