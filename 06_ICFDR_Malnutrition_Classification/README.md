# ICFDR Malnutrition Classification — Interview Study Pack

Source archive: `ICFDR---ML-Project-main.zip`
Main notebook: `MalnutritionDetect.ipynb`
Additional notebooks: `SMOTE.ipynb`, `Oversampling on the whole dataset.ipynb`

## Contents
1. Business Problem & Objective
2. Dataset Understanding
3. Exploratory Data Analysis
4. Preprocessing & Feature Engineering
5. Train-Test Split & Validation Strategy
6. Model Selection
7. Model Training & Hyperparameter Tuning
8. Model Evaluation
9. Business Interpretation, Results & Limitations
10. Two-Minute Interview Narration

## Grounded repository facts
- `Malnutrition data.csv`: 837 rows × 8 columns; no missing values.
- Target distribution: Stunting 696, Overweight 94, Underweight 43, Wasting 4.
- Features include Sex, Age, Height, Weight and three income group indicators.
- Main notebook explores Random Forest, SVM and a dense neural network.
- A separate SMOTE notebook splits first and resamples only the training set: 585 -> 1,940 rows.
- Another notebook explicitly applies SMOTE to the whole dataset before splitting. This is data leakage; its evaluation should not be trusted.
- Main notebook results include RF test accuracy 72.22% and linear SVM test accuracy 84.13%, but the test partition has no Wasting examples and minority-class performance is poor.
- A neural network branch uses a single sigmoid/binary cross-entropy for a four-class target, which is a formulation error.
- No deployment tutorial is included. The API file is discussed only as a repository artifact.

## Important qualification
This is an educational ML project, not a validated clinical screening tool. The PDFs distinguish the implementation from recommended corrections and do not overstate model performance.
