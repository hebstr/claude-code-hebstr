# Protocol — Prediction Models for Postoperative Delirium in Elderly Patients

## Research Question

What prediction models, clinical scores, and machine learning tools have been developed or validated to predict postoperative delirium in elderly patients undergoing elective non-cardiac surgery, and what is their predictive performance?

## Framework: PICO

- **Population**: Adults ≥65 years hospitalized for elective non-cardiac surgery
- **Intervention**: Prediction models or scores for postoperative delirium (clinical scores, ML models, EHR-derived models)
- **Comparator**: Clinical judgment alone, no screening, or head-to-head comparison between models
- **Outcomes**: (1) Discrimination (AUC/c-statistic), calibration; (2) Identified risk factors (age, comorbidities, polypharmacy, frailty, biomarkers); (3) Impact on early detection and length of stay

## Review Type

Scoping review (PRISMA-ScR guidelines)

## Time Period

2015–2026

## Languages

English, French

## Inclusion Criteria

- Adults ≥65 years undergoing elective non-cardiac surgery
- Studies developing, validating, or comparing prediction models/scores for postoperative delirium
- Reports discrimination metrics (AUC, c-statistic, sensitivity, specificity) or identifies risk factors used in a predictive model
- Published 2015–2026
- English or French language
- Study designs: cohort (prospective/retrospective), case-control, cross-sectional, systematic reviews of prediction models, RCTs evaluating prediction-guided interventions

## Exclusion Criteria

- Pediatric populations (<18 years)
- Cardiac surgery
- ICU delirium not related to postoperative context
- Delirium tremens / alcohol withdrawal delirium
- Editorials, letters, conference abstracts without full data
- Studies focused solely on delirium treatment without a prediction component
- Animal studies

## Databases

1. PubMed/MEDLINE
2. Semantic Scholar
3. OpenAlex

## Search Strategy

### Key Concepts

| Concept | Terms |
|---------|-------|
| Delirium | delirium, postoperative delirium, POD, acute confusion, postoperative cognitive dysfunction, POCD |
| Prediction | prediction, predictive model, risk score, risk stratification, machine learning, deep learning, artificial intelligence, logistic regression, nomogram, clinical decision support, EHR, electronic health record, routine data |
| Elderly | elderly, older adults, aged, geriatric, ≥65, senior |
| Surgery | surgery, surgical, postoperative, perioperative, elective surgery, non-cardiac surgery |

### Boolean Query

```
(delirium OR "postoperative delirium" OR POD OR "acute confusion")
AND
(prediction OR "predictive model" OR "risk score" OR "risk stratification"
 OR "machine learning" OR "deep learning" OR "artificial intelligence"
 OR "logistic regression" OR nomogram OR "clinical decision support"
 OR EHR OR "electronic health record" OR "routine data")
AND
(elderly OR "older adults" OR aged OR geriatric OR senior)
AND
(surgery OR surgical OR postoperative OR perioperative)
```
