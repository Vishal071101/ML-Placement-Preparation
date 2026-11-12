# Customer Segmentation — Corrected Interview Study Pack

This is a regenerated replacement for the earlier Customer Segmentation ZIP. The PDFs were rebuilt with clean ReportLab paragraph handling, readable tables, consistent typography, page footers, and text extraction checks.

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

## Source verified
- Repository: `Sai-Likhith-2005/Customer-Segmentation`
- Notebook: `smartcart.ipynb`
- Dataset: `smartcart_customers.csv`

## Grounded facts
- Original dataset: 2,240 rows × 22 columns; 24 missing Income values.
- Four records removed by notebook filters; 2,236 retained.
- Median imputation; engineered Age, Customer_Tenure_Days, Total_Spending and Total_Children.
- Education grouped into Undergraduate / Graduate / Postgraduate; marital status simplified into Living_With.
- Drops ID, Year_Birth, Marital_Status, Kidhome, Teenhome, Dt_Customer and six product-category spend columns after summing spending.
- One-hot encoded Education and Living_With; final matrix 2,236 × 18.
- StandardScaler then PCA(3); explained variance ratios 23.16%, 11.39%, 10.41% (44.95% total).
- K-Means inertia sweep K=1..10; KneeLocator reports K=4. Silhouette scores plotted for K=2..10 but numeric values are not printed.
- K-Means used for exploration/visualisation; final profile labels are from AgglomerativeClustering(n_clusters=4, linkage='ward').
- Response is retained as a feature, which is a potential leakage issue for future-campaign segmentation.
- No train/test split, no stability analysis, no deployment workflow.

## Important corrections and cautions
- Cluster profiles are descriptive and cluster IDs are arbitrary.
- Cluster 3's high Response average is not independent validation because Response was included in the clustering inputs.
- Age is hard-coded as 2026 minus Year_Birth.
- Preprocessing/PCA are fitted on the full dataset; future use requires a reusable fitted pipeline and validation.
- Three-component PCA retains 44.95% of variance.
- Standard supervised accuracy is not applicable without true segment labels.
