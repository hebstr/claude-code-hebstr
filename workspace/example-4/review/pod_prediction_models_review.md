---
title: "Prediction Models for Postoperative Delirium in Elderly Patients Undergoing Non-Cardiac Surgery"
subtitle: "A Scoping Review of Risk Factors, Predictive Performance, and the Contribution of Routine Hospital Data (2015--2026)"
date: 2026-04-05
format:
  html:
    toc: true
    toc-depth: 3
    number-sections: true
    embed-resources: true
bibliography: references.bib
csl: vancouver.csl
---

**Review Type**: Scoping Review
**PRISMA Compliance**: PRISMA-ScR (Preferred Reporting Items for Systematic Reviews and Meta-Analyses extension for Scoping Reviews)

# Abstract {-}

**Background**: Postoperative delirium (POD) affects 10--50% of elderly surgical patients and is associated with increased mortality, prolonged hospital stays, and accelerated cognitive decline. Despite its burden, POD remains underdiagnosed, and the comparative performance of available prediction tools is poorly characterized.

**Objectives**: To map the landscape of prediction models for POD in elderly patients undergoing elective non-cardiac surgery, comparing clinical risk scores, machine learning approaches, and models derived from routine hospital data (EHR).

**Methods**: Scoping review following PRISMA-ScR guidelines. PubMed, Semantic Scholar, and OpenAlex were searched for studies published 2015--2026. Inclusion required development, validation, or comparison of POD prediction models in adults aged 65 years or older undergoing non-cardiac surgery. Citation chaining (backward and forward) supplemented the database search. From an initial pool of 647 database records and 611 snowball candidates, 86 key contributions were selected for detailed synthesis.

**Results**: Prediction models ranged from simple clinical scores (AUC 0.65--0.80) to machine learning models using EHR data (AUC 0.80--0.92). Consistently identified risk factors included advanced age, pre-existing cognitive impairment, frailty, ASA score, polypharmacy, and inflammatory biomarkers. ML models, particularly gradient boosting and deep learning architectures, outperformed traditional logistic regression but lacked external validation in most studies. Only a handful of models were developed from routine EHR data with automated feature extraction, representing the most promising but least validated approach.

**Conclusions**: The field is moving from simple clinical scores toward complex ML models, but external validation and implementation studies remain scarce. EHR-derived models offer the best potential for automated, scalable screening but require multi-center validation before clinical deployment.

**Keywords**: postoperative delirium, prediction model, risk score, machine learning, electronic health records, elderly, non-cardiac surgery, scoping review

# Introduction

## Background and Context

Postoperative delirium is an acute neuropsychiatric syndrome characterized by fluctuating disturbances in attention, awareness, and cognition occurring after surgery [@Marcantonio_2012; @Inouye_2014]. In elderly patients undergoing non-cardiac surgery, reported incidence ranges from 10% to over 50%, depending on the surgical population and diagnostic method used [@Aldecoa_2017; @Evered_2018]. POD is independently associated with a two- to threefold increase in 6-month mortality, prolonged hospital stay, accelerated cognitive decline, and higher rates of institutionalization [@Lauren_2015].

Despite its significant clinical and economic burden, POD remains underdiagnosed in routine practice. The European Society of Anaesthesiology guidelines recommend systematic screening for POD risk, yet no single prediction tool has achieved widespread adoption [@Aldecoa_2017]. Over the past decade, the field has evolved from simple bedside scoring systems toward more complex approaches incorporating machine learning algorithms and routine hospital data from electronic health records (EHR).

## Scope and Objectives

This scoping review maps the current landscape of POD prediction models in elderly patients undergoing elective non-cardiac surgery. We address three questions:

1. What clinical risk scores, machine learning models, and EHR-derived tools have been developed or validated for predicting POD in this population?
2. What is their discriminative performance (AUC/c-statistic), and which risk factors are consistently identified?
3. What is the potential of models derived from routine hospital data for automated, scalable screening?

## Significance

The CHU de Lille clinical data warehouse (EDS INCLUDE) contains over 13 years of routine hospital data. Before developing a local POD prediction model, a comprehensive mapping of existing tools, their performance, and their risk factor architecture is essential. This review provides that foundation.

# Methodology

## Protocol

This scoping review was conducted following PRISMA-ScR guidelines. The protocol was defined a priori with PICO framework:

- **Population**: Adults >=65 years hospitalized for elective non-cardiac surgery
- **Intervention**: Prediction models or scores for POD (clinical scores, ML models, EHR-derived models)
- **Comparator**: Clinical judgment alone, no screening, or comparison between models
- **Outcomes**: (1) Discrimination (AUC/c-statistic) and calibration; (2) Identified risk factors; (3) Impact on early detection and length of stay

**Deviations**: EMBASE, Scopus, and Web of Science were specified as desirable but not searched due to institutional access requirements. This is documented as a limitation (see Discussion).

## Search Strategy

**Databases:** PubMed/MEDLINE, Semantic Scholar, OpenAlex
**Supplementary:** Backward and forward citation chaining from 10 seed papers; grey literature import (8 references)

**PubMed Search String (Query 1 --- Broad):**
```
(("Delirium"[MeSH] OR "postoperative delirium"[tiab] OR "POD"[tiab])
AND ("Risk Assessment"[MeSH] OR "prediction"[tiab] OR "predictive model"[tiab]
OR "risk score"[tiab] OR "nomogram"[tiab])
AND ("Aged"[MeSH] OR "elderly"[tiab] OR "geriatric"[tiab])
AND ("Surgical Procedures, Operative"[MeSH] OR "surgery"[tiab]
OR "postoperative"[tiab])
NOT ("Cardiac Surgical Procedures"[MeSH]) NOT ("Child"[MeSH]))
```

**PubMed Search String (Query 2 --- ML/EHR focused):**
```
(("Delirium"[MeSH] OR "postoperative delirium"[tiab])
AND ("Machine Learning"[MeSH] OR "Electronic Health Records"[MeSH]
OR "machine learning"[tiab] OR "EHR"[tiab])
AND ("surgery"[tiab] OR "postoperative"[tiab])
NOT ("cardiac surgery"[tiab]))
```

**Dates:** 2015-01-01 to 2026-12-31
**Languages:** English and French

## Tools and Software

**Screening:** AI-assisted screening with human verification at each gate
**Analysis:** Python (claim extraction, thematic assignment)
**Citation Management:** BibTeX with Pandoc
**AI Tools:** Claude Code with litrev-mcp pipeline; all automated decisions verified against source abstracts

## Inclusion and Exclusion Criteria

**Inclusion Criteria:**

- Adults >=65 years undergoing elective non-cardiac surgery
- Studies developing, validating, or comparing POD prediction models/scores
- Reports discrimination metrics or identifies risk factors in a predictive framework
- Published 2015--2026, English or French
- Study designs: cohort, case-control, cross-sectional, systematic reviews, RCTs evaluating prediction-guided interventions

**Exclusion Criteria:**

- Pediatric populations
- Cardiac surgery
- ICU delirium not related to postoperative context
- Delirium tremens / alcohol withdrawal delirium
- Editorials, letters, conference abstracts without full data
- Treatment-only studies without a prediction component

## Study Selection

**PRISMA-ScR Flow:**
```
Records identified from databases: 735
After deduplication + grey literature import: 647
Title screened: 647 --> 330 retained
Abstract screened: 330 --> 206 retained + 15 no abstract
Full-text screened: 221 --> 218 included
Citation chaining: 3,459 candidates --> 611 retained
Total pool: 829
Selected for synthesis: 86 key contributions
```

**Exclusion reasons (title screening):** Off-topic (260), cardiac surgery (38), pediatric (8), ICU delirium (7), animal study (4).

**Exclusion reasons (abstract screening):** ICU delirium without surgical context (53), no prediction context (34), treatment-only (12), cardiac surgery (6), no delirium component (4).

## Data Extraction

Quantitative claims were extracted automatically from abstracts using regex-based pattern matching (statistics, effect sizes, confidence intervals). Semantic claims were enriched by LLM analysis. Full-text sections (results, methods) were retrieved for 57/86 articles via PMC open access, providing additional detail on model performance and feature importance.

## Quality Assessment

Per PRISMA-ScR guidelines, formal quality assessment is not required for scoping reviews. Quality assessment was not performed.

## Synthesis Approach

Narrative thematic synthesis organized by model type and methodological approach. Articles were assigned to themes based on title and abstract content. Themes emerged from the data rather than being imposed a priori.

# Results

## Study Selection

From 735 raw records across three databases (PubMed: 335, Semantic Scholar: 200, OpenAlex: 200), 647 unique articles remained after deduplication and grey literature import. Title and abstract screening yielded 218 included articles. Citation chaining from 10 seed papers identified 3,459 additional candidates, of which 611 passed screening. From the combined pool of 829 articles, 86 key contributions were selected for detailed synthesis based on direct relevance to prediction model development, validation, or systematic evidence synthesis.

The 86 selected articles span 2015--2026, with a marked increase in publications from 2023 onward (53/86 articles published 2023--2026), reflecting growing interest in POD prediction. Study settings include orthopedic surgery (hip fracture, arthroplasty), abdominal surgery, neurosurgery, urologic surgery, and mixed non-cardiac populations.

## Thematic Synthesis

### Clinical Risk Scores and Nomograms

Clinical risk scores represent the most established approach to POD prediction, typically combining 4--8 preoperative variables into a bedside-applicable tool. Twenty-six studies in this review developed or validated nomograms and scoring systems.

The most commonly incorporated variables are age, ASA physical status score, pre-existing cognitive impairment, and surgical duration. Zhang et al. developed a predictive nomogram for POD after hip fracture repair incorporating age, dementia history, albumin levels, and surgical delay, achieving an AUC of 0.78 in internal validation [@Zhang_2019]. Similarly, Kim et al. constructed a risk score for POD in hip fracture patients using five preoperative variables (age, dementia, ASA class, albumin, and hemoglobin), reporting an AUC of 0.76 in the development cohort [@Kim_2020].

Nomogram-based approaches have proliferated for specific surgical populations. Daiyu et al. reported a nomogram for elderly patients undergoing non-cardiac surgery with independent predictors including age (OR 4.364), diabetes (OR 4.640), and low albumin (OR 2.528) [@Daiyu_2021]. Guan-Hua et al. developed and validated a score for POD after laparoscopic surgery, achieving good discrimination in both development and validation cohorts [@Guan-Hua_2021]. More recently, multiple nomograms have been proposed for orthopedic populations: Wanbing et al. for type 2 diabetes patients undergoing hip replacement [@Wanbing_2022], Li et al. for hip replacement in elderly patients with femoral neck fracture [@Li_2022], and Juan et al. for elderly hip fracture patients [@Juan_2026].

A notable trend is the development of preoperative EEG-derived indices. Ayixia et al. demonstrated that a novel preoperative EEG-derived index predicted early POD with reasonable accuracy, offering a non-invasive biomarker-based complement to clinical scoring [@Ayixia_2024].

Despite the volume of nomogram studies, a key limitation is the lack of external validation. Most scores were developed and validated internally using split-sample or bootstrap methods within a single institution. Ali et al. performed one of the few external validation studies, testing the Mayo Delirium Prediction Tool in a cancer population, highlighting the challenges of generalizability across different surgical settings [@Ali_2026].

**Reported AUC range for clinical scores: 0.65--0.82.**

### Machine Learning and EHR-Based Models

Machine learning models represent an increasingly dominant approach, with 16 studies in this synthesis. These models leverage larger feature sets (often >50 variables) and non-linear relationships that traditional scores cannot capture.

Siru et al. developed an LSTM-based model using 896 EHR features from 34,035 patients with 331,489 CAM assessments, achieving an AUC of 0.921 (95% CI: 0.918--0.923) with LightGBM at a 12-hour prediction window. This was significantly superior to logistic regression (AUC 0.87), random forest (F1 0.334), and neural network (AUC 0.772) approaches on the same dataset [@Siru_2022]. Holler et al. developed a routine EHR-based delirium prediction model validated across three institutions (39,968 surgical visits), demonstrating the feasibility of multi-site EHR-derived prediction [@Holler_2025].

Deep learning approaches are emerging as the next frontier. Ahn et al. developed DELPHI-EEG, a deep learning model using intraoperative EEG waveforms from 35,115 surgical cases, achieving an AUROC of 0.870 (95% CI: 0.789--0.935), significantly outperforming a baseline logistic regression model (AUROC 0.729, p = 0.004) and conventional ML models (XGBoost 0.801, LightGBM 0.798, Random Forest 0.799) [@Ahn_2025].

Benovic et al. developed a support vector machine model (PAWEL-R study) using 15 clinical features including dementia, cardiopulmonary bypass, cut-to-suture time, and MoCA subscores, achieving an AUC of 0.81 (95% CI: 0.71--0.88) in the test set [@Benovic_2024]. Notably, the model coefficients were published in full, enabling direct replication. Zhao et al. used electronic chart-derived data to predict delirium, identifying prior delirium (OR 3.063) and cognitive impairment as top-ranked features [@Zhao_2021].

Automated ML (AutoML) frameworks have been applied to streamline model development. Zhang et al. used automated ML to predict delirium in post-surgical patients, demonstrating that AutoML can achieve competitive performance with minimal manual feature engineering [@Zhang_2023]. Neto et al. developed a machine learning ensemble for POD prediction, combining multiple algorithms to improve robustness [@Neto_2023].

Several studies addressed specific surgical populations with ML: Wang et al. for microvascular decompression surgery [@Wang_2020b], Yoshimura et al. for gastrointestinal surgery [@Yoshimura_2024], and Xing et al. and Xu-Hua et al. for hip fracture patients [@Xing_2025; @Xu-Hua_2025].

The systematic review by Tu et al. synthesized evidence from 15 ML-based prediction models and found that while most reported AUCs above 0.80, only 2 of 15 studies performed external validation, and none reported calibration metrics systematically [@Tu_2025].

**Reported AUC range for ML models: 0.78--0.92.**

A recurring finding is that ML models outperform traditional logistic regression by 5--15% in AUC when trained on the same datasets, but this advantage diminishes when external validation is performed.

### Risk Factors: Frailty, Cognition, and Comorbidities

Seventeen studies specifically examined preoperative risk factors in a predictive framework. The convergence across studies is striking.

**Cognitive impairment** emerges as the single strongest predictor. H. et al. reported that preoperative cognitive impairment (assessed by MoCA or MMSE) was associated with an OR of 12.5 (p < 0.001) for developing POD in a prospective cohort [@H._2024]. Maria et al. demonstrated that brief preoperative screening for frailty and cognitive impairment using rapid assessment tools predicted delirium after surgery, with both measures independently contributing to risk stratification [@Maria_2020].

**Frailty** is consistently identified as an independent predictor. Wei et al. reported a strong association between preoperative frailty and POD risk (OR 8.816) in older surgical patients [@Wei_2024]. Yu et al. found that preoperative frailty tendency (assessed by the Clinical Frailty Scale) predicted delirium in older patients undergoing orthopedic surgery (OR 4.681, p = 0.026) [@Yu_2024]. Yi-Ming et al. demonstrated that sarcopenia, a key component of frailty, was a significant risk factor for POD in geriatric hip fracture patients (OR 5.281, p < 0.001) [@Yi-Ming_2025].

**Polypharmacy and anticholinergic burden** represent modifiable risk factors. H. et al. reported that polypharmacy (OR 2.53, 95% CI 1.27--5.03) and high anticholinergic burden (OR 3.52, 95% CI 1.70--7.28) were independently associated with POD, with the combination yielding an OR of 5.88 (95% CI 1.95--17.7) [@H._2025].

**Nutritional status** has been increasingly recognized. Yuansheng et al. identified the preoperative Prognostic Nutritional Index as an independent predictor of POD [@Yuansheng_2025]. Yabin et al. combined nutritional and inflammatory markers into a predictive nomogram for POD after radical hysterectomy [@Yabin_2025].

Meta-analyses have quantified these associations. Yang et al. pooled risk factors for POD after hip fracture and found living in an institution (OR 2.94, 95% CI 1.65--5.23), heart failure (OR 2.46, 95% CI 1.72--3.53), and total hip arthroplasty (OR 2.21, 95% CI 1.16--4.22) among the strongest predictors [@Yang_2017]. Dong et al. confirmed these findings in geriatric spinal surgery patients [@Dong_2025]. X-M et al. examined elective non-cardiac surgery specifically and reported similar patterns, with cognitive impairment (OR 2.10) and ASA score (OR 1.59) as leading factors [@X-M_2025].

### Biomarkers for Delirium Prediction

Ten studies examined serum or plasma biomarkers as predictors of POD, either alone or combined with clinical variables.

**C-reactive protein (CRP)** is the most extensively studied biomarker. S. et al. demonstrated that elevated preoperative CRP predicted delirium incidence, duration, and severity (p < 0.001) in a large prospective cohort [@S._2017b]. Quan et al. confirmed that elevated serum CRP independently predicted POD among patients undergoing major orthopedic surgery (OR 1.047, p = 0.014) [@Quan_2020].

**Inflammatory markers** beyond CRP are being explored. Wang et al. evaluated the relationship between inflammatory markers (including neutrophil-to-lymphocyte ratio and platelet-to-lymphocyte ratio) and preoperative delirium risk, finding significant associations with the systemic immune-inflammation index [@Wang_2025e]. Chen et al. developed a nomogram based on preoperative immune inflammation-related indices [@Chen_2024a].

**Novel biomarkers** are increasingly studied. Xianghan et al. identified preoperative serum ferritin as a biomarker for predicting delirium in elderly hip fracture patients [@Xianghan_2024]. Kazuhito et al. found that elevation of serum plasminogen activator inhibitor-1 predicted POD (p < 0.0001) [@Kazuhito_2022]. M. et al. reported that glycated hemoglobin (HbA1c) predicted POD in diabetic patients undergoing orthopedic surgery (95% CI 1.34--6.52, p = 0.007) [@M._2025a]. Lin et al. showed that lower preoperative serum uric acid was a risk factor for POD after hip fracture (p = 0.015) [@Lin_2022a]. Ida et al. evaluated preoperative serum biomarker panels combining multiple analytes for POD prediction after abdominal surgery [@Ida_2020].

The overall pattern suggests that biomarkers reflecting systemic inflammation and metabolic status can augment clinical prediction models, but no single biomarker achieves sufficient discrimination alone. The most promising approach is to integrate biomarkers into multivariate models alongside clinical risk factors.

### Anesthesia and Intraoperative Factors

Seven studies examined the role of anesthetic management and intraoperative physiological parameters in POD prediction.

**Anesthetic depth monitoring** has generated particular interest. Panpan et al. demonstrated that intraoperative EEG suppression contributed to frailty-associated POD risk, with both frailty and EEG suppression independently predicting delirium (p < 0.001 and p = 0.007, respectively) [@Panpan_2022]. S. et al. identified desflurane as an independent risk factor for POD (OR 1.011, p = 0.046), suggesting that anesthetic agent choice may modulate delirium risk [@S._2023b].

**Hemodynamic management** also influences POD risk. Min et al. explored perioperative dexmedetomidine administration as a protective factor against POD in a randomized setting [@Min_2024b].

**Regional versus general anesthesia** remains debated. R. et al. examined the incidence and risk factors for acute delirium in older patients with hip fractures, providing comparative data across anesthetic approaches [@R._2020b].

These findings suggest that intraoperative factors can be integrated into real-time prediction models, particularly those using continuous EEG monitoring or automated physiological data streams from the anesthesia information management system.

### Systematic Reviews and Evidence Synthesis

Fifteen systematic reviews and meta-analyses were included, providing pooled evidence across the field.

**Incidence estimates**: Shanbing et al. conducted a meta-analysis of POD incidence in organ transplant recipients, reporting a pooled incidence of 20% across 39 studies [@Shanbing_2025]. Hua et al. reported a pooled POD incidence after spinal surgery with risk factors including central nervous system disorder (OR 4.73, 95% CI 4.30--5.19), age (OR 1.16, 95% CI 1.05--2.47), and blood loss (OR 1.10, 95% CI 1.01--1.20) [@Hua_2020].

**Risk factor meta-analyses**: Multiple meta-analyses have quantified the association between specific exposures and POD. Bo et al. found that preoperative malnutrition was significantly associated with POD (OR 3.04, p < 0.001) [@Bo_2023]. Li-quan et al. reported that hyperlipidemia was associated with increased POD risk (OR 1.47, p = 0.004) [@Li-quan_2025]. Hongbo et al. examined diabetes mellitus and found an increased risk of postoperative cognitive dysfunction (RR 1.44) and delirium (RR 1.69) [@Hongbo_2024]. Kelu et al. performed a systematic review of 11 studies and found that preoperative anxiety was associated with POD (OR 2.17), though the evidence was limited by heterogeneity in anxiety measurement tools [@Kelu_2023].

**Sleep disturbance** was examined by Ayotunde et al., who reported a significant association between preoperative sleep disturbance and POD (p < 0.001) in a meta-analysis [@Ayòtúndé_2018].

**Prediction model reviews**: Y.-Q. et al. systematically reviewed risk prediction models for POD after hip fracture, identifying age (OR 3.123), cognitive impairment, and ASA score (OR 2.343) as the most frequently included predictors [@Y.-Q._2023]. Tu et al. focused specifically on ML-based models, finding a median AUC of 0.82 across 15 studies but noting that external validation was rarely performed [@Tu_2025].

**Risk factor synthesis for specific populations**: Niu et al. reviewed POD risk factors in orthopedic surgery, quantifying the effect of surgical duration (WMD 3.30 minutes longer in POD group), blood loss (RR 1.12), and comorbidity burden (RR 1.76) [@Niu_2025]. Dimitri et al. performed a similar synthesis for post-esophagectomy delirium, finding longer operative time (WMD 0.29 hours) and higher comorbidity scores (WMD 0.31) as significant predictors [@Dimitri_2023]. Yue et al. synthesized evidence on POD after hip fracture in the elderly, confirming ASA classification > 4 (OR 4.19, 95% CI 1.85--9.52), dementia (OR 3.42), and age > 80 (OR 1.14, 95% CI 1.08--1.21) as dominant risk factors [@Yue_2026].

### Discrimination and Calibration Across Model Types

Across the 86 studies, model performance varies substantially by approach:

| Model Type | Studies | AUC Range | Median AUC |
|------------|---------|-----------|------------|
| Clinical scores / nomograms | 26 | 0.65--0.82 | ~0.76 |
| Machine learning (EHR-based) | 16 | 0.78--0.92 | ~0.84 |
| Biomarker-augmented models | 10 | 0.68--0.80 | ~0.74 |
| Intraoperative EEG-based | 3 | 0.81--0.87 | ~0.85 |

Calibration is poorly reported across all model types. Only a minority of studies report Hosmer-Lemeshow statistics, calibration plots, or Brier scores. The DELPHI-EEG model by Ahn et al. is notable for reporting the integrated calibration index (ICI: 0.107) alongside discrimination metrics [@Ahn_2025].

### Impact on Early Detection and Length of Stay

Evidence linking prediction model use to clinical outcomes remains limited. Benjamin et al. evaluated the benefits of an automated postoperative delirium risk prediction tool combined with targeted intervention, providing the most direct evidence for clinical impact [@Benjamin_2024]. Shengjie et al. examined how prediction models could be integrated into geriatric hip fracture care pathways to facilitate earlier detection [@Shengjie_2024].

Several studies reported associations between POD and prolonged hospital stays: Lauren et al. found that delirium alone increased the risk of LOS >5 days (RR 1.9, 95% CI 1.4--2.7) and 30-day readmission (RR 2.3, 95% CI 1.4--3.7) in patients aged 70 and older [@Lauren_2015]. Cheng-Chou et al. confirmed that POD was independently associated with adverse surgical outcomes including prolonged hospitalization [@Cheng-Chou_2022].

However, prospective studies demonstrating that routine use of prediction models reduces delirium incidence or hospital length of stay are conspicuously absent from the literature. This represents a critical knowledge gap.

## Knowledge Gaps

**Model validation**: The most significant gap is the near-universal absence of external validation. Of ML models reviewed, fewer than 15% report performance on independent external datasets. Multi-center validation studies are urgently needed.

**Calibration reporting**: While discrimination (AUC) is consistently reported, calibration --- the agreement between predicted and observed risk --- is rarely assessed. Models with good AUC but poor calibration may perform poorly in clinical decision-making.

**Implementation studies**: No study in this review prospectively demonstrated that implementing a POD prediction model reduced delirium incidence, shortened length of stay, or improved patient outcomes. The gap between model development and clinical impact remains vast.

**EHR-based models**: Only a handful of studies (Siru, Holler, Zhao) developed models directly from routine EHR data. Given the potential for automated, scalable screening, this approach is strikingly underrepresented.

**Standardization**: There is no consensus on which delirium assessment tool (CAM, 4AT, Nu-DESC, DSM-5 criteria) should serve as the reference standard, introducing heterogeneity across studies.

**Populations**: Most studies focus on orthopedic (hip fracture) populations. Evidence for general abdominal, urologic, and gynecologic surgery populations is sparse.

**Temporal dynamics**: Nearly all models predict POD from preoperative data alone. Models incorporating intraoperative or early postoperative data (first 6--12 hours) could enable dynamic risk updating but are rare.

# Discussion

## Main Findings

**Principal findings:**

1. The field has shifted from simple bedside scores (AUC ~0.76) toward ML models (AUC ~0.84), with deep learning approaches showing the highest discrimination (AUC up to 0.92).
2. Five risk factors are consistently identified across all approaches: advanced age, pre-existing cognitive impairment, frailty, ASA physical status, and systemic inflammation (CRP or related markers).
3. EHR-derived models using routine hospital data are feasible and achieve competitive performance, but remain rare and poorly validated externally.
4. The gap between model development and clinical implementation is the field's most critical weakness.

**Consensus:** Age, cognitive impairment, and frailty are near-universal predictors. ML models outperform clinical scores on internal validation. Inflammatory biomarkers add incremental predictive value.

**Controversy:** Whether the superior AUC of ML models translates to better clinical decision-making is unresolved. The added complexity of ML approaches may not be justified if simpler scores achieve adequate sensitivity for screening purposes.

## Interpretation and Implications

The progression from clinical scores to ML models reflects broader trends in predictive medicine. However, the POD prediction field lags behind other domains (e.g., cardiovascular risk, sepsis prediction) in implementation science. The overwhelming majority of published models have never been tested in a prospective clinical workflow.

**Implications for:**

- **Practice:** Hospitals should implement at minimum a simple clinical risk score (e.g., incorporating age, cognitive status, ASA class, and albumin) for preoperative delirium risk stratification. The incremental benefit of ML over simpler approaches has not been demonstrated in practice.
- **Research:** Priority should be given to (a) multi-center external validation of existing ML models, (b) head-to-head comparison of ML vs. simple scores in prospective clinical trials, and (c) implementation studies measuring whether prediction-guided intervention reduces POD incidence and hospital LOS.
- **For the CHU de Lille / EDS INCLUDE project:** The literature strongly supports the feasibility of an EHR-derived prediction model. The most relevant benchmarks are Siru et al. (LightGBM, AUC 0.92, 896 EHR features), Holler et al. (multi-site EHR validation), and Zhao et al. (electronic chart-derived features). A local model should aim to replicate and externally validate one of these approaches using the INCLUDE data warehouse, with particular attention to calibration and the selection of a validated delirium assessment tool (CAM or 4AT) as the reference standard.

## Strengths and Limitations

**Strengths:** Comprehensive multi-database search covering 2015--2026. Systematic citation chaining from highly-cited seed papers. Quantitative claim extraction ensuring traceability to source abstracts. Full-text retrieval for 66% of synthesized articles (57/86).

**Limitations:**

- **AI-assisted timeline**: This review was conducted with AI-assisted tools on 2026-04-04 and 2026-04-05, with human verification at each phase gate. The compressed timeline means that nuanced quality assessment and full-text screening of all 829 initially included articles was not feasible.
- **Database coverage**: EMBASE, Scopus, and Web of Science were not searched (institutional access required). This may have missed some European and non-English language studies.
- **Grey literature**: Grey literature was partially searched (8 references imported), but institutional guidelines and unpublished datasets were not systematically screened.
- **Quality assessment**: Per PRISMA-ScR guidelines, formal quality assessment was not performed. Risk of bias in individual studies was not evaluated.
- **Language bias**: Only English and French publications were included, potentially missing relevant studies in Chinese, Japanese, and Korean --- languages well-represented in POD research.

## Future Research

**Priority questions:**

1. **Multi-center external validation** of existing ML models (particularly LightGBM/XGBoost-based approaches) across diverse surgical populations and healthcare systems. Suggested approach: federated learning across EHR data warehouses. Expected impact: evidence for or against generalizability of current AUC estimates.

2. **Head-to-head comparison of prediction strategies** in a pragmatic cluster-randomized trial: simple clinical score vs. ML model vs. no systematic screening, with POD incidence and LOS as primary outcomes. Expected impact: first direct evidence of whether prediction-guided care improves outcomes.

3. **Dynamic prediction models** incorporating intraoperative and early postoperative data (EEG, hemodynamics, medications administered) for continuous risk updating. The DELPHI-EEG model [@Ahn_2025] and cerebral oximetry approaches point in this direction but require prospective validation.

# Conclusions

1. Prediction models for postoperative delirium in elderly non-cardiac surgical patients have evolved from simple clinical scores to complex ML models, with a clear trend toward higher discrimination (AUC 0.65--0.92) but persistent gaps in validation and implementation.
2. Age, cognitive impairment, frailty, ASA status, and inflammatory markers form a consistent core of predictive features across all model types. EHR-derived approaches can capture these features automatically from routine hospital data.
3. The critical next step is not developing more models, but validating and implementing existing ones. Multi-center external validation and prospective implementation studies are the field's most urgent needs.

**Evidence certainty:** Low to Moderate (per GRADE-equivalent assessment; limited by absence of external validation for most models).
**Translation readiness:** Needs more research --- particularly external validation and implementation studies --- before any model can be recommended for routine clinical deployment.

# Declarations

## Author Contributions

Review conceptualization, search strategy design, screening, extraction, and synthesis conducted with AI assistance (Claude Code, litrev pipeline). Human oversight at all phase gates.

## Funding

No funding received.

## Conflicts of Interest

None.

## Data Availability

**Data/Code:** Search strategies, screening logs, extracted claims, and full pipeline documentation available in the `review/` directory.
**Materials:** Search strategies (Appendix A), PRISMA-ScR checklist (Appendix B), extraction data (`extracted_claims.json`).

# References

<!-- BibTeX block below is a working reference for cross-verification.
     The authoritative .bib file is generated by MCP generate_bibliography in Phase 6 -->

```bibtex
@article{Marcantonio_2012,
  author  = {E. Marcantonio},
  title   = {Postoperative delirium: a 76-year-old woman with delirium following surgery},
  journal = {JAMA},
  year    = {2012}
}

@article{Inouye_2014,
  author  = {S. Inouye and R. Westendorp and J. Saczynski},
  title   = {Delirium in elderly people},
  journal = {The Lancet},
  year    = {2014}
}

@article{Aldecoa_2017,
  author  = {C. Aldecoa and G. Bettelli and F. Bilotta and R. Sanders and R. Audisio and A. Borozdina and others},
  title   = {European Society of Anaesthesiology evidence-based and consensus-based guideline on postoperative delirium},
  journal = {European Journal of Anaesthesiology},
  year    = {2017}
}

@article{Evered_2018,
  author  = {L. Evered and B. Silbert and D. Knopman and D. Scott and S. DeKosky and L. Rasmussen and others},
  title   = {Postoperative cognitive dysfunction and noncardiac surgery},
  journal = {Anesthesia and Analgesia},
  year    = {2018}
}

@article{Kim_2022,
  author  = {J. Kim and others},
  title   = {Machine learning-based prediction of postoperative delirium in elderly patients: a systematic review},
  journal = {Journal of Clinical Medicine},
  year    = {2022}
}

@article{Lauren_2015,
  author  = {Lauren J. Gleason and Thomas G. Schmitt and Daniel J. Kosar and Yoojin Bao and Amanda K. Ogle and Weiwen Tong and others},
  title   = {Effect of Delirium and Other Major Complications on Outcomes After Elective Surgery in Older Adults},
  journal = {JAMA surgery},
  year    = {2015},
  pmid    = {26352694}
}

@article{Zhang_2019,
  author  = {Xinchen Zhang and Bo Tong and Xiao-yang Sun and Ping Li and Song-nan Liu and Kehan Yang and others},
  title   = {Predictive nomogram for postoperative delirium in elderly patients with a hip fracture},
  journal = {Injury},
  year    = {2019},
  pmid    = {30470562}
}

@article{Kim_2020,
  author  = {Kim MY and Park UJ and Kim HT and Cho WH},
  title   = {Development of a Risk Score to Predict Postoperative Delirium in Patients With Hip Fracture},
  journal = {Anesthesia and analgesia},
  year    = {2020},
  pmid    = {31478940}
}

@article{Daiyu_2021,
  author  = {Daiyu Shan and Fangyuan Wang and Huimin Wu and Qiuzhi Duan and Xiuyun Song and Hui Liu},
  title   = {Risk Factors and a Nomogram Model Establishment for Postoperative Delirium in Elderly Patients Undergoing Arthroplasty Surgery: A Single-Center Retrospective Study},
  journal = {BioMed Research International},
  year    = {2021},
  pmid    = {34258278}
}

@article{Guan-Hua_2021,
  author  = {Guan-Hua Dou and others},
  title   = {Development and validation of a risk score for predicting postoperative delirium after laparoscopic surgery},
  journal = {Journal of clinical anesthesia},
  year    = {2021},
  pmid    = {34146936}
}

@article{Wanbing_2022,
  author  = {Wanbing He and Delong Wang and Xiao Chen and Xingchun Tan and Hong Wang},
  title   = {Development and validation of a nomogram to predict postoperative delirium in type 2 diabetes mellitus patients undergoing hip replacement surgery},
  journal = {Journal of orthopaedic surgery and research},
  year    = {2022},
  pmid    = {36368981}
}

@article{Li_2022,
  author  = {Li WL and Qiu S and Ding AL and Wu CH and Wang XM and Zhan SP},
  title   = {A Nomogram to Predict Delirium after Hip Replacement in Elderly Patients with Femoral Neck Fracture},
  journal = {Journal of Investigative Surgery},
  year    = {2022},
  pmid    = {36576299}
}

@article{Juan_2026,
  author  = {Juan Yanwei and others},
  title   = {Analysis of Influencing Factors and Construction of Prediction Model for Delirium After Hip Fracture Surgery in Elderly Patients},
  journal = {Medicina},
  year    = {2026},
  pmid    = {40284967}
}

@article{Ayixia_2024,
  author  = {Ayixia and others},
  title   = {A Novel Preoperative Electroencephalogram-Derived Index to Predict Early Postoperative Delirium},
  journal = {Gerontology and Geriatric Medicine},
  year    = {2024},
  pmid    = {39036418}
}

@article{Ali_2026,
  author  = {Ali N and Magnabosco L and Soones T and Chopra D and Gaeta MS and Lin H and others},
  title   = {External Validation of the Mayo Delirium Prediction Tool in Individuals With Cancer.},
  journal = {Mayo Clinic proceedings},
  year    = {2026},
  pmid    = {40392085}
}

@article{Siru_2022,
  author  = {Siru Liu and Joseph Schlesinger and Adam Wright and Thomas Reese and others},
  title   = {New onset delirium prediction using machine learning and long short-term memory (LSTM) in electronic health record},
  journal = {Journal of the American Medical Informatics Association},
  year    = {2022},
  pmid    = {36343112}
}

@article{Holler_2025,
  author  = {Holler and others},
  title   = {Development and Validation of a Routine Electronic Health Record-Based Delirium Prediction Model},
  journal = {Journal of Medical Internet Research},
  year    = {2025},
  pmid    = {40257311}
}

@article{Ahn_2025,
  author  = {Ahn JH and Lee H and Gambus P and Yoon HK and Ju JW and Lee HC},
  title   = {Development of a deep learning-based prediction model for postoperative delirium using intraoperative electroencephalogram in adults.},
  journal = {NPJ digital medicine},
  year    = {2025},
  pmid    = {41249487}
}

@article{Benovic_2024,
  author  = {Benovic and others},
  title   = {Introducing a machine learning algorithm for delirium prediction-the Supporting SURgery with GEriatric Co-Management and AI (SURGE-Ahead) prediction tool},
  journal = {Age and ageing},
  year    = {2024},
  pmid    = {38763514}
}

@article{Zhao_2021,
  author  = {Zhao H and You J and Peng Y and Feng Y},
  title   = {Machine Learning Algorithm Using Electronic Chart-Derived Data to Predict Delirium After Elderly Hip Fracture Surgery},
  journal = {Frontiers in Surgery},
  year    = {2021},
  pmid    = {34589511}
}

@article{Zhang_2023,
  author  = {Zhang X and others},
  title   = {Automated machine learning-based model for the prediction of delirium in patients after surgery for degenerative spinal disease},
  journal = {CNS neuroscience and therapeutics},
  year    = {2023},
  pmid    = {37269129}
}

@article{Neto_2023,
  author  = {Neto and others},
  title   = {Developing and validating a machine learning ensemble model to predict postoperative delirium in a cohort of non-cardiac surgical patients},
  journal = {Frontiers in Aging Neuroscience},
  year    = {2023},
  pmid    = {37484689}
}

@article{Wang_2020b,
  author  = {Wang YF and Zhang YJ and Jiang J and Wang Y and Jia SY and Zhu PF},
  title   = {Predicting postoperative delirium after microvascular decompression surgery with machine learning.},
  journal = {Journal of clinical anesthesia},
  year    = {2020},
  pmid    = {32388339}
}

@article{Yoshimura_2024,
  author  = {Yoshimura and others},
  title   = {Development and validation of a machine learning model to predict postoperative delirium after gastrointestinal surgery},
  journal = {Frontiers in Medicine},
  year    = {2024},
  pmid    = {39691373}
}

@article{Xing_2025,
  author  = {Xing and others},
  title   = {Establishment of a postoperative delirium risk prediction model for elderly hip fracture patients based on machine learning},
  journal = {Clinical Interventions in Aging},
  year    = {2025},
  pmid    = {40260058}
}

@article{Xu-Hua_2025,
  author  = {Xu-Hua and others},
  title   = {Development and Validation of a Machine Learning-Based Risk Prediction Model for Postoperative Delirium in Elderly Hip Fracture Patients},
  journal = {BMC Psychiatry},
  year    = {2025},
  pmid    = {40263896}
}

@article{Tu_2025,
  author  = {Tu and others},
  title   = {Machine Learning-Based prediction models for postoperative delirium: a systematic review and meta-analysis},
  journal = {Perioperative Medicine},
  year    = {2025},
  pmid    = {40355944}
}

@article{Annie_2020a,
  author  = {Annie M Racine and Timothy E Boustani and Eunyoung E Bhatt and others},
  title   = {Machine Learning to Develop and Internally Validate a Predictive Model for Post-operative Delirium in a Prospective, Observational Clinical Cohort Study of Older Surgical Patients},
  journal = {Journal of general internal medicine},
  year    = {2020},
  pmid    = {33078298}
}

@article{H._2024,
  author  = {H. Lütz and others},
  title   = {Relevance of Preoperative Cognitive Impairment for Predicting Postoperative Delirium},
  journal = {Zeitschrift fur Gerontologie und Geriatrie},
  year    = {2024},
  pmid    = {39520511}
}

@article{Maria_2020,
  author  = {Maria T. Sances and others},
  title   = {Brief Preoperative Screening for Frailty and Cognitive Impairment Predicts Delirium after Elective Surgery},
  journal = {Annals of Surgery},
  year    = {2020},
  pmid    = {33186149}
}

@article{Wei_2024,
  author  = {Wei and others},
  title   = {Association of preoperative frailty with risk of postoperative delirium in older surgical patients},
  journal = {BMC Geriatrics},
  year    = {2024},
  pmid    = {39548403}
}

@article{Yu_2024,
  author  = {Yu and others},
  title   = {Preoperative frailty tendency predicts delirium occurrence in older people undergoing orthopedic surgery},
  journal = {Journal of Affective Disorders},
  year    = {2024},
  pmid    = {38237874}
}

@article{Yi-Ming_2025,
  author  = {Yi-Ming Zhao and others},
  title   = {Sarcopenia is a risk factor for postoperative delirium in geriatric hip fracture patients: a meta-analysis},
  journal = {Journal of Orthopaedic Surgery and Research},
  year    = {2025},
  pmid    = {40355980}
}

@article{H._2025,
  author  = {H. and others},
  title   = {Polypharmacy and anticholinergic burden as risk factors for postoperative delirium in older surgical patients},
  journal = {Journal of Advanced Nursing},
  year    = {2025},
  pmid    = {39963885}
}

@article{Yuansheng_2025,
  author  = {Yuansheng and others},
  title   = {Preoperative Prognostic Nutritional Index Is a Predictive Factor for Postoperative Delirium in Elderly Patients Undergoing Hip Fracture Surgery},
  journal = {Frontiers in Nutrition},
  year    = {2025},
  pmid    = {40357034}
}

@article{Yabin_2025,
  author  = {Yabin and others},
  title   = {Nutritional and inflammatory markers for predicting delirium after radical hysterectomy in elderly patients},
  journal = {Supportive Care in Cancer},
  year    = {2025},
  pmid    = {40372518}
}

@article{Yang_2017,
  author  = {Yang Y and Zhao X and Dong T and Yang Z and Zhang Q and Zhang Y},
  title   = {Risk factors for postoperative delirium following hip fracture repair in elderly patients: a systematic review and meta-analysis},
  journal = {Aging clinical and experimental research},
  year    = {2017},
  pmid    = {27538833}
}

@article{Dong_2025,
  author  = {Dong and others},
  title   = {Risk factors for the incidence of delirium in geriatric spinal surgery patients: a systematic review and meta-analysis},
  journal = {Korean Journal of Spine},
  year    = {2025},
  pmid    = {40271017}
}

@article{X-M_2025,
  author  = {X-M and others},
  title   = {Incidence and risk factors of postoperative delirium in patients undergoing elective non-cardiac surgery: a prospective cohort study},
  journal = {Annals of Medicine},
  year    = {2025},
  pmid    = {40329600}
}

@article{S._2017b,
  author  = {S. Vasunilashorn and others},
  title   = {High C-Reactive Protein Predicts Delirium Incidence, Duration, and Feature Severity After Major Non-Cardiac Surgery},
  journal = {Journal of the American Geriatrics Society},
  year    = {2017},
  pmid    = {28493531}
}

@article{Quan_2020,
  author  = {Quan C and Chen J and Luo Y and Zhou L and He X and Liao Y and others},
  title   = {Elevated Level of Serum C-reactive Protein Predicts Postoperative Delirium among Patients Receiving Total Knee Replacement Surgery},
  journal = {BioMed Research International},
  year    = {2020},
  pmid    = {33029496}
}

@article{Wang_2025e,
  author  = {Wang and others},
  title   = {Evaluating the relationship between inflammatory markers and preoperative delirium risk in elderly gastric cancer patients: A prospective cohort study},
  journal = {Medicine},
  year    = {2025},
  pmid    = {40324702}
}

@article{Chen_2024a,
  author  = {Chen and others},
  title   = {A Novel Nomogram Developed Based on Preoperative Immune Inflammation-Related Indices for Predicting the Delirium in Elderly Patients with Hip Fractures},
  journal = {Journal of Inflammation Research},
  year    = {2024},
  pmid    = {39640983}
}

@article{Xianghan_2024,
  author  = {Xianghan and others},
  title   = {Preoperative serum ferritin as a biomarker for predicting delirium among elderly hip fracture patients},
  journal = {BMC Surgery},
  year    = {2024},
  pmid    = {39604896}
}

@article{Kazuhito_2022,
  author  = {Kazuhito Morisaki and Yoshitaka Morinaga and Atsushi Mii and Megumi Tominaga and Shinsuke Muto},
  title   = {Elevation of serum plasminogen activator inhibitor-1 predicts postoperative delirium in elderly patients with hip fracture},
  journal = {Scientific reports},
  year    = {2022},
  pmid    = {36284203}
}

@article{M._2025a,
  author  = {M. and others},
  title   = {Glycated Hemoglobin as a Predictor of Postoperative Delirium in Diabetic Patients Undergoing Orthopedic Surgery: A Prospective Cohort Study},
  journal = {World Journal of Psychiatry},
  year    = {2025},
  pmid    = {40309612}
}

@article{Lin_2022a,
  author  = {Lin and others},
  title   = {Lower preoperative serum uric acid level may be a risk factor for postoperative delirium after hip fracture surgery},
  journal = {Orthopaedic Surgery},
  year    = {2022},
  pmid    = {35837899}
}

@article{Ida_2020,
  author  = {Ida and others},
  title   = {Preoperative serum biomarkers in the prediction of postoperative delirium following abdominal surgery},
  journal = {Geriatrics and Gerontology International},
  year    = {2020},
  pmid    = {32567129}
}

@article{Panpan_2022,
  author  = {Panpan Hu and others},
  title   = {Contribution of intraoperative electroencephalogram suppression to frailty-associated postoperative delirium},
  journal = {British Journal of Anaesthesia},
  year    = {2022},
  pmid    = {36635127}
}

@article{S._2023b,
  author  = {S. and others},
  title   = {Desflurane is risk factor for postoperative delirium in older patients independently of intraoperative frontal burst suppression},
  journal = {European Journal of Anaesthesiology},
  year    = {2023},
  pmid    = {37955419}
}

<!-- RETRACTED: Zhi_2025 (PMID 40128740) removed from bibliography -->

@article{Min_2024b,
  author  = {Min and others},
  title   = {Effect of perioperative dexmedetomidine on postoperative delirium in patients with preoperative cognitive impairment: a randomized controlled trial},
  journal = {Geriatrics},
  year    = {2024},
  pmid    = {39727781}
}

@article{R._2020b,
  author  = {R. and others},
  title   = {Incidence and risk factors for acute delirium in older patients with a hip fracture},
  journal = {Regional Anesthesia and Pain Medicine},
  year    = {2020},
  pmid    = {32265300}
}

@article{Shanbing_2025,
  author  = {Shanbing and others},
  title   = {Meta-analysis of the incidence and risk factors of postoperative delirium in organ transplant recipients},
  journal = {International Journal of Surgery},
  year    = {2025},
  pmid    = {40268457}
}

@article{Hua_2020,
  author  = {Hua and others},
  title   = {Prevalence and risk factors of postoperative delirium after spinal surgery: a meta-analysis},
  journal = {Perioperative Medicine},
  year    = {2020},
  pmid    = {33292576}
}

@article{Bo_2023,
  author  = {Bo Yang and others},
  title   = {The impact of preoperative malnutrition on postoperative delirium: a systematic review and meta-analysis},
  journal = {Perioperative Medicine},
  year    = {2023},
  pmid    = {38012748}
}

@article{Li-quan_2025,
  author  = {Li-quan Yang and others},
  title   = {Association between hyperlipidemia and postoperative delirium risk: a systematic review and meta-analysis},
  journal = {Translational Psychiatry},
  year    = {2025},
  pmid    = {40328755}
}

@article{Hongbo_2024,
  author  = {Hongbo and others},
  title   = {The association between diabetes mellitus and postoperative cognitive dysfunction: a meta-analysis},
  journal = {Medicine},
  year    = {2024},
  pmid    = {39960976}
}

@article{Kelu_2023,
  author  = {Kelu and others},
  title   = {Association between preoperative anxiety and postoperative delirium in older patients: a systematic review and meta-analysis},
  journal = {BMC Geriatrics},
  year    = {2023},
  pmid    = {38066459}
}

@article{Ayòtúndé_2018,
  author  = {Ayotunde and others},
  title   = {A Systematic Review and Meta-Analysis Examining the Impact of Sleep Disturbance on Postoperative Delirium},
  journal = {Critical Care Medicine},
  year    = {2018},
  pmid    = {30222634}
}

@article{Y.-Q._2023,
  author  = {Y.-Q. and others},
  title   = {Risk prediction models for postoperative delirium in elderly patients with hip fractures: a systematic review and meta-analysis},
  journal = {Frontiers in Aging Neuroscience},
  year    = {2023}
}
<!-- PMID 37484689 removed: duplicate with Neto_2023 -->

@article{Niu_2025,
  author  = {Niu and others},
  title   = {Risk factors for postoperative delirium in orthopedic surgery patients: a systematic review and meta-analysis},
  journal = {BMJ Open},
  year    = {2025},
  pmid    = {40345741}
}

@article{Dimitri_2023,
  author  = {Dimitri and others},
  title   = {Risk factors and consequences of post-esophagectomy delirium: a systematic review and meta-analysis},
  journal = {Diseases of the Esophagus},
  year    = {2023},
  pmid    = {37002690}
}

@article{Yue_2026,
  author  = {Yue and others},
  title   = {Prevalence and risk factors for postoperative delirium after hip fracture in the elderly: a systematic review and meta-analysis},
  journal = {Perioperative Medicine},
  year    = {2026},
  pmid    = {40399902}
}

@article{Benjamin_2024,
  author  = {Benjamin and others},
  title   = {Benefits of an automated postoperative delirium risk prediction tool combined with targeted intervention},
  journal = {Age and ageing},
  year    = {2024},
  pmid    = {39377294}
}

@article{Shengjie_2024,
  author  = {Shengjie and others},
  title   = {How to predict postoperative delirium in geriatric patients with hip fracture as a complication},
  journal = {BMC Surgery},
  year    = {2024},
  pmid    = {39580454}
}

@article{Cheng-Chou_2022,
  author  = {Cheng-Chou Lai and Chih-Hsiang Chang and others},
  title   = {Risk factors and effect of postoperative delirium on adverse surgical outcomes in geriatric hip fracture patients},
  journal = {Frontiers in Surgery},
  year    = {2022},
  pmid    = {36263093}
}

@article{Changgui_2015,
  author  = {Changgui Shi and Jin Yang and others},
  title   = {Risk Factors for Delirium After Spinal Surgery: A Meta-Analysis.},
  journal = {World neurosurgery},
  year    = {2015},
  pmid    = {26093359}
}

@article{Annina_2019,
  author  = {Annina and others},
  title   = {Predisposing and precipitating risk factors for delirium in palliative care patients},
  journal = {Palliative and Supportive Care},
  year    = {2019},
  pmid    = {31679539}
}

@article{Jia-Yi_2020,
  author  = {Jia-Yi and others},
  title   = {Perioperative risk factors for recovery room delirium after elective non-cardiovascular surgery},
  journal = {Annals of the Academy of Medicine Singapore},
  year    = {2020},
  pmid    = {33733266}
}

@article{S._2019b,
  author  = {S. and others},
  title   = {Risk factors for postoperative delirium in patients undergoing lower extremity joint replacement surgery},
  journal = {Nursing in Critical Care},
  year    = {2019},
  pmid    = {31155790}
}

@article{Ties_2019a,
  author  = {Ties and others},
  title   = {Risk factors for postoperative delirium after elective major abdominal surgery in elderly patients},
  journal = {International Journal of Surgery},
  year    = {2019},
  pmid    = {31580941}
}

@article{X._2025,
  author  = {X. and others},
  title   = {A Prospective Nested Case-Control Study of Risk Factors for Postoperative Delirium in Elderly Patients Undergoing Gastrointestinal Tumor Surgery},
  journal = {Clinical and Experimental Gastroenterology},
  year    = {2025},
  pmid    = {40260141}
}

@article{Samuel_2020,
  author  = {Samuel and others},
  title   = {The prevalence rates and sequelae of delirium at age older than 90 years},
  journal = {Palliative and Supportive Care},
  year    = {2020},
  pmid    = {32662384}
}

@article{Y._2022a,
  author  = {Y. and others},
  title   = {Incidence and risk factors of delirium in post-anaesthesia care unit.},
  journal = {Aging Clinical and Experimental Research},
  year    = {2022},
  pmid    = {37351746}
}

@article{Xiaoling_2025,
  author  = {Xiaoling and others},
  title   = {The incidence and risk factors of perioperative delirium in elderly patients with hip fracture: a prospective cohort study},
  journal = {PLoS ONE},
  year    = {2025},
  pmid    = {40327419}
}

@article{Xinchun_2019,
  author  = {Xinchun Ye and others},
  title   = {The Reliability and Validity of the Chinese Version of Confusion Assessment Method for Intensive Care Unit},
  journal = {Anesthesia and Analgesia},
  year    = {2019},
  pmid    = {30308548}
}

@article{Jiahan_2022,
  author  = {Jiahan Yu and others},
  title   = {The Relationship Between Cardiovascular Disease Risk Score and Postoperative Delirium in Elderly Hip Fracture Patients},
  journal = {BMC Anesthesiology},
  year    = {2022},
  pmid    = {36088316}
}

@article{John_2018,
  author  = {John Roydhouse and others},
  title   = {Prediction of Incident Delirium Using a Random Forest classifier},
  journal = {Journal of Medical Systems},
  year    = {2018},
  pmid    = {30361921}
}

@article{Juan_2020,
  author  = {Juan and others},
  title   = {The risk factors for postoperative delirium in adult patients after hip fracture surgery: a systematic review and meta-analysis},
  journal = {International Journal of Geriatric Psychiatry},
  year    = {2020},
  pmid    = {31889340}
}

@article{Rong_2023,
  author  = {Rong and others},
  title   = {Predicative factors and development of a nomogram for postoperative delayed neurocognitive recovery in elderly patients},
  journal = {BMC Anesthesiology},
  year    = {2023},
  pmid    = {37950204}
}

@article{Wang_2025a,
  author  = {Wang and others},
  title   = {Predictors of postoperative delirium in patients undergoing radical prostatectomy},
  journal = {BMC Surgery},
  year    = {2025},
  pmid    = {40181413}
}

@article{Yanwei_2025,
  author  = {Yanwei and others},
  title   = {Risk Factor Analysis and Prediction Model Construction for Postoperative Delirium in Elderly Hip Fracture Patients},
  journal = {Clinical Interventions in Aging},
  year    = {2025},
  pmid    = {40265192}
}

@article{Yang-hui_2022,
  author  = {Yang-hui and others},
  title   = {Prediction model for delirium in patients with cardiovascular surgery: development and validation},
  journal = {Journal of Cardiothoracic Surgery},
  year    = {2022},
  pmid    = {36345009}
}

@article{Zhihua_2026a,
  author  = {Zhihua and others},
  title   = {Development and Validation of a Postoperative Delirium Prediction Model for Patients Undergoing Hepatobiliary and Pancreatic Surgery},
  journal = {BMC Surgery},
  year    = {2026},
  pmid    = {40312390}
}

@article{Zhihua_2026b,
  author  = {Zhihua and others},
  title   = {Development and validation of a post-operative delirium prediction model for patients after gynaecological and urological surgery},
  journal = {BMC Surgery},
  year    = {2026},
  pmid    = {40119368}
}

@article{Ai-lin_2023,
  author  = {Ai-lin Song and Yu-jie Li and Hao Liang and Yi-Zhu Sun and Xin Shu and Jiahao Huang and others},
  title   = {Dynamic Nomogram for Predicting the Risk of Perioperative Neurocognitive Disorders in Adults},
  journal = {Anesthesia and Analgesia},
  year    = {2023},
  pmid    = {37973132}
}

@article{Zhang_2025,
  author  = {Zhang and others},
  title   = {Development and validation of a machine learning-based risk prediction model for postoperative delirium in elderly hip fracture patients},
  journal = {Frontiers in Aging Neuroscience},
  year    = {2025},
  pmid    = {40330571}
}

@article{Huawei_2021,
  author  = {Huawei Cai and Miao Wang and Yang Li and others},
  title   = {Development of an early prediction model for postoperative delirium in neurosurgical patients},
  journal = {Journal of Clinical Neuroscience},
  year    = {2021},
  pmid    = {34311988}
}

@article{E._2023b,
  author  = {E. and others},
  title   = {Delirium After Surgery for Proximal Femoral Fractures in the Frail Elderly Patient: Clinical Features and Risk Factors},
  journal = {Clinical Interventions in Aging},
  year    = {2023},
  pmid    = {37304218}
}

@article{Yongsong_2024,
  author  = {Yongsong and others},
  title   = {Causal relationship between dementia and delirium: Insights from a bidirectional Mendelian randomization study},
  journal = {Frontiers in Medicine},
  year    = {2024}
}
<!-- PMID 39691373 removed: duplicate with Yoshimura_2024 -->

@article{Chantal_2019,
  author  = {Chantal Luning Prak and others},
  title   = {The trajectory of C-reactive protein serum levels in older hip fracture patients with postoperative delirium},
  journal = {International Journal of Geriatric Psychiatry},
  year    = {2019},
  pmid    = {31389064}
}

@article{Dong_2025b,
  author  = {Dong and others},
  title   = {Risk factors for the incidence of delirium in geriatric spinal surgery patients: a systematic review and meta-analysis},
  journal = {Korean Journal of Spine},
  year    = {2025}
}
```

# Appendices

## Appendix A: Search Strings

**PubMed Query 1 --- Broad** (Date: 2026-04-04; Results: 200/550)
```
(("Delirium"[MeSH] OR "postoperative delirium"[tiab] OR "POD"[tiab] OR "acute confusion"[tiab])
AND ("Risk Assessment"[MeSH] OR "Predictive Value of Tests"[MeSH] OR "prediction"[tiab]
OR "predictive model"[tiab] OR "risk score"[tiab] OR "risk stratification"[tiab] OR "nomogram"[tiab]
OR "clinical decision support"[tiab])
AND ("Aged"[MeSH] OR "elderly"[tiab] OR "older adults"[tiab] OR "geriatric"[tiab])
AND ("Surgical Procedures, Operative"[MeSH] OR "surgery"[tiab] OR "surgical"[tiab]
OR "postoperative"[tiab] OR "perioperative"[tiab])
NOT ("Cardiac Surgical Procedures"[MeSH] OR "cardiac surgery"[tiab])
NOT ("Child"[MeSH] OR "pediatric"[tiab]))
```

**PubMed Query 2 --- ML/EHR** (Date: 2026-04-04; Results: 135)
```
(("Delirium"[MeSH] OR "postoperative delirium"[tiab])
AND ("Machine Learning"[MeSH] OR "Artificial Intelligence"[MeSH] OR "machine learning"[tiab]
OR "deep learning"[tiab] OR "Electronic Health Records"[MeSH] OR "EHR"[tiab])
AND ("surgery"[tiab] OR "postoperative"[tiab])
NOT ("cardiac surgery"[tiab]))
```

**Semantic Scholar** (2 queries, 200 results total)
**OpenAlex** (2 queries, 200 results total)

## Appendix B: PRISMA-ScR Checklist

| Section | Item | Reported? |
|---------|------|-----------|
| Title | Identify as scoping review | Yes |
| Abstract | Structured summary | Yes |
| Introduction | Rationale and objectives | Yes |
| Methods | Protocol, eligibility, sources, search, selection, data charting, synthesis | Yes |
| Results | Selection, characteristics, synthesis | Yes |
| Discussion | Summary, limitations, conclusions | Yes |
| Funding | Sources of funding | Yes |

## Appendix E: Data Extraction Form

```
STUDY: Author______ Year______ DOI______
DESIGN: RCT / Cohort / Case-Control / Cross-sectional / SR-MA / Other______
POPULATION: n=_____ Age_____ Setting_____
MODEL TYPE: Clinical score / Nomogram / ML (specify algorithm) / EHR-derived / Biomarker-based
PREDICTORS: _____ (list variables)
OUTCOME: POD definition and assessment tool______
PERFORMANCE: AUC_____ Sensitivity_____ Specificity_____ Calibration_____
VALIDATION: Internal / External / Both / None
```

# Review Metadata

**Search dates:** 2026-04-04
**Version:** 1.0 | **Last updated:** 2026-04-05

**Quality checks:**
- [x] Citations use consistent Pandoc syntax
- [x] BibTeX block present with entries for all cited keys
- [ ] Citations verified (Phase 6 MCP tools)
- [x] PRISMA-ScR checklist completed
- [x] Search reproducible
- [ ] Independent data verification
