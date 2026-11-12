# Loan Approval Prediction — Interview Study Pack

Source archive supplied in this conversation: `Loan-Approval-main.zip`
Notebook: `credit_wise.ipynb`
Dataset: `loan_approval_data.csv`

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

## Repository facts and important caveats
- Dataset has 1,000 rows and 20 columns; every column has 50 missing values.
- The notebook imputes all columns before splitting, including the target `Loan_Approved` using most-frequent imputation. This creates 50 artificial labels and is a major issue.
- Applicant_ID is dropped; Education_Level and Loan_Approved are label-encoded; six categorical columns are one-hot encoded.
- An 80/20 random split with `random_state=42` is used without stratification.
- StandardScaler is fit on the training set and applied to the test set.
- Baseline models: Logistic Regression, KNN (k=5), GaussianNB.
- A second experiment adds squared DTI and Credit Score features, then drops the original columns.
- Reported single-split metrics are documented in the PDFs. No cross-validation or systematic hyperparameter tuning is performed.
- No deployment material is included.

The study notes distinguish repository behaviour from recommended improvements. Reported scores should not be treated as reliable production performance until target missingness and preprocessing leakage are fixed.
