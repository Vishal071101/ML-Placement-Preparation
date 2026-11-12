from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path
import subprocess, os, re, zipfile, textwrap

OUT=Path('/mnt/data/churn_docs')
PROJ='Customer Churn Prediction'
SOURCE='https://github.com/YuvarajGarla/Customer-churn-prediction'

# document data: title, content as structured blocks
sections=[]

def sec(title, blocks): sections.append((title,blocks))

sec('01 - Business Problem and Objective', [
('h2','1. Project context'),('p','Customer churn is the situation in which an existing customer stops using a company\'s products or services. For a telecom provider, churn may mean disconnecting a mobile connection, broadband subscription, or another paid service.'),
('p','The business problem is to identify customers who are at elevated risk of leaving, early enough for the company to consider an appropriate retention action. Acquiring a replacement customer can require marketing, onboarding, and sales expenditure; retaining a suitable existing customer may therefore be economically attractive.'),
('h2','2. Machine-learning objective'),('p','This is a supervised binary-classification problem. The target is Churn: Yes is encoded as 1 and No as 0. The model attempts to estimate P(Churn = 1 | customer information), using demographic, account, service, tenure, and billing attributes.'),
('formula','Y = 1 if the customer churns; Y = 0 otherwise'),('formula','Model objective: estimate P(Y = 1 | X), where X is the vector of customer features.'),
('h2','3. Business use'),('bullets',['Prioritize customers with high predicted churn risk for review or outreach.','Tailor retention offers rather than applying the same intervention to every customer.','Investigate service or contract characteristics associated with churn.','Measure whether retention interventions work through a properly designed experiment.']),
('note','A prediction is not a causal explanation. The model estimates risk from historical associations; it does not prove why a customer leaves or guarantee that an offer will prevent churn.'),
('h2','4. Interview-ready explanation'),('quote','The objective of this project was to predict customer churn for a telecom company. Customer churn refers to customers discontinuing their telecom services. Since retaining existing customers is an important business priority, we wanted to identify customers who were likely to leave using their demographic information, subscription details, service usage, tenure, and billing information. The predictions could help the business prioritize high-risk customers for proactive retention measures.'),
('h2','5. Questions to prepare'),('qa',[
('Why is this a classification problem?','The outcome is a discrete label with two classes: churn and non-churn. The model can estimate a probability and then assign a class using a decision threshold.'),
('What is the business value of churn prediction?','It helps prioritize limited retention resources toward customers who may be at risk. The value depends on whether interventions change behaviour enough to justify their cost.'),
('Does a high churn probability tell us why a customer leaves?','No. It is a predictive risk score, not a causal explanation. Explanation and intervention-effect estimation need additional analysis.')])
])

sec('02 - Dataset Understanding', [
('h2','1. Dataset source and dimensions'),('p',f'The repository uses the IBM Telco Customer Churn dataset distributed as WA_Fn-UseC_-Telco-Customer-Churn.csv. The EDA notebook reports 7,043 rows and 21 columns. After converting TotalCharges and dropping rows that become missing, the model-building data contains 7,032 observations.'),
('p',f'Source repository: {SOURCE}'),
('h2','2. Feature groups'),('table',[
['Group','Columns / examples','Meaning'],
['Customer demographics','gender, SeniorCitizen, Partner, Dependents','Basic customer profile'],
['Account / subscription','tenure, Contract, PaperlessBilling, PaymentMethod','Customer relationship and billing arrangements'],
['Services','PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies','Services subscribed to'],
['Billing','MonthlyCharges, TotalCharges','Current monthly charge and cumulative charges'],
['Identifier / target','customerID, Churn','Unique identifier and outcome label']]),
('h2','3. Target distribution'),('p','The EDA notebook reports an approximate 73:27 distribution: about 73% non-churn and 27% churn. Exact counts should be recalculated from the cleaned dataset rather than inferred from the rounded percentages.'),
('bullets',['Class 0: customer did not churn.','Class 1: customer churned.','The target imbalance makes accuracy alone an insufficient evaluation measure.']),
('h2','4. Important data-type observation'),('p','TotalCharges is initially read as an object/string column even though it represents a numeric amount. The notebook converts it to numeric, coercing unparseable blank entries to missing values. SeniorCitizen is numerically encoded as 0/1 but should be interpreted as a categorical indicator in descriptive analysis.'),
('h2','5. Interview-ready explanation'),('quote','We used the IBM Telco Customer Churn dataset, containing 7,043 customer observations and 21 columns. It included demographic information, services subscribed, contract details, tenure, and billing attributes. Churn was the binary target. The target distribution was imbalanced, with roughly 73% non-churn and 27% churn observations, which influenced our evaluation strategy.'),
('h2','6. Questions to prepare'),('qa',[
('Why remove customerID?','It is an identifier, not a meaningful customer behaviour attribute. Including it can let a model memorize arbitrary identifiers or exploit accidental patterns.'),
('Why is TotalCharges initially an object?','The CSV contains blank or non-numeric values. Pandas therefore reads the column as text; it must be parsed before numeric analysis or modelling.'),
('Why is class imbalance relevant?','A model can achieve seemingly good accuracy by predicting the majority class while missing many churners. Recall, precision, F1, and precision-recall analysis are important.')])
])

sec('03 - Exploratory Data Analysis', [
('h2','1. EDA goals'),('p','Exploratory data analysis is used to inspect data quality, understand feature distributions, identify unusual values, study relationships with the target, and develop hypotheses that can guide modelling. EDA findings should be treated as associations, not causal conclusions.'),
('h2','2. Initial inspection'),('code','telco_base_data.head()\ntelco_base_data.shape\ntelco_base_data.columns\ntelco_base_data.dtypes\ntelco_base_data.describe()\ntelco_base_data.info()'),
('table', [['Operation','Purpose'],['head()','Inspect sample records'],['shape / columns','Understand dimensions and available attributes'],['dtypes / info()','Inspect types and non-null counts'],['describe()','Review numerical distributions and summary statistics']]),
('h2','3. Target distribution'),('p','The notebook plots Churn counts and percentages. Its narrative identifies an approximately 73:27 majority-to-minority class ratio. This tells us to examine performance separately for churners rather than rely on accuracy alone.'),
('h2','4. Univariate and bivariate analysis'),('p','The EDA notebook uses count plots with hue=Churn to compare outcomes across categories such as Contract, PaymentMethod, and service subscriptions. It also uses density plots to compare MonthlyCharges and TotalCharges by churn outcome.'),
('h2','5. Main observations documented in the notebook'),('bullets',['Month-to-month contract customers show higher churn than longer-contract customers.','Customers without OnlineSecurity and TechSupport show higher churn.','Electronic-check users are identified as a high-churn group.','Higher MonthlyCharges are associated with higher churn in the notebook analysis.','Customers with shorter tenure / in the first year show higher churn.','Longer-tenure customers show lower churn.','Gender, PhoneService, and MultipleLines are described as having relatively weak association with churn.']),
('note','The observations above reflect the notebook’s descriptive analysis. To compare churn rates fairly across categories, calculate within-category churn rates, not just raw counts. Category sizes differ, and raw counts can be misleading.'),
('h2','6. TotalCharges and tenure relationship'),('p','The notebook notes that churn appears higher among customers with lower TotalCharges. This becomes easier to interpret alongside tenure: cumulative charges tend to increase with time subscribed and monthly price. A customer can therefore have high MonthlyCharges but low TotalCharges because their tenure is short.'),
('formula','TotalCharges is approximately related to MonthlyCharges × Tenure, but is not exactly equal because charges can vary over time and include other billing details.'),
('h2','7. Correlation analysis'),('code',"telco_data_dummies.corr()['Churn'].sort_values(ascending=False)\nsns.heatmap(telco_data_dummies.corr())"),
('p','The notebook computes correlations after dummy encoding. For binary encoded variables, correlation can indicate association, but it is not causation. Correlation among one-hot columns and the target also needs context, including the reference categories and prevalence of each category.'),
('h2','8. Better EDA practices to mention'),('bullets',['Report churn rate within each category: P(Churn=1 | category), not only total counts.','Use normalized stacked bars where category sizes differ.','Inspect numeric distributions and outliers separately for churn/non-churn groups.','Check association and redundancy among features.','Do not use target information from outside the training data for any learned preprocessing decisions.']),
('h2','9. Interview-ready explanation'),('quote','During EDA, I examined dataset structure, types, summary statistics, and the target distribution. I then compared churn and non-churn customers across contract, service, tenure, payment, and billing attributes. The notebook highlighted higher churn among month-to-month customers, customers without online security or technical support, electronic-check users, and customers with shorter tenure. These patterns helped frame the preprocessing and modelling work, while being treated as associations rather than causal effects.'),
('h2','10. Questions to prepare'),('qa',[
('What is the difference between univariate and bivariate analysis?','Univariate analysis studies one variable’s distribution. Bivariate analysis studies the relationship between two variables, for example MonthlyCharges and Churn.'),
('What does a KDE plot show?','It estimates a smoothed probability density function for a continuous variable, allowing comparison of distributions across groups.'),
('Why can raw category counts be misleading?','Categories have different population sizes. A larger category can produce more churners even if its churn rate is lower. Compare normalized rates.'),
('Does correlation imply causation?','No. A correlation can arise from confounding, selection, reverse relationships, or coincidence. Causal claims need an appropriate causal design.')])
])

sec('04 - Preprocessing and Feature Engineering', [
('h2','1. Convert TotalCharges to numeric'),('code',"telco_data.TotalCharges = pd.to_numeric(\n    telco_data.TotalCharges, errors='coerce'\n)"),
('p','The errors=coerce option converts values that cannot be parsed into numbers into NaN. The notebook then finds 11 missing TotalCharges entries, which are removed using dropna. This is about 0.16% of the original 7,043 rows.'),
('note','A careful analysis should inspect those 11 rows. In this dataset, blank TotalCharges entries are associated with zero tenure. Dropping them is a small row loss, but the decision and its business/data implications should be documented.'),
('h2','2. Create tenure groups'),('code','labels = [f"{i} - {i+11}" for i in range(1, 72, 12)]\ntelco_data["tenure_group"] = pd.cut(\n    telco_data.tenure, range(1, 80, 12),\n    right=False, labels=labels\n)'),
('table',[['Group','Months'],['1 - 12','1 to 12'],['13 - 24','13 to 24'],['25 - 36','25 to 36'],['37 - 48','37 to 48'],['49 - 60','49 to 60'],['61 - 72','61 to 72']]),
('p','Binning can capture lifecycle stages and simplify interpretation. The trade-off is information loss: two customers with different tenure values in the same bin become indistinguishable with respect to this feature.'),
('h2','3. Remove identifier and original tenure'),('code',"telco_data.drop(columns=['customerID', 'tenure'], inplace=True)"),
('p','customerID is an identifier, not a generalizable behavioural feature. tenure is removed because tenure_group was created from it. This is a modelling choice, not a universal rule: keeping both could be tested if the model and validation design justify it.'),
('h2','4. Encode target'),('code',"telco_data['Churn'] = np.where(\n    telco_data.Churn == 'Yes', 1, 0\n)"),
('h2','5. One-hot encode categorical features'),('code','telco_data_dummies = pd.get_dummies(telco_data)'),
('p','One-hot encoding creates a separate binary indicator for each category. This avoids imposing an artificial numerical ordering on nominal categories. The repository applies pandas get_dummies to the prepared dataframe.'),
('note','For a robust production/reusable training workflow, use a fitted preprocessing transformer such as OneHotEncoder(handle_unknown="ignore") inside a Pipeline. Fit encoders on training data only and apply the same learned mapping to validation/test/new data. The Flask app’s separate get_dummies logic may be sensitive to missing or unexpected categories and column order.'),
('h2','6. Feature scaling'),('p','The repository does not scale features before Decision Tree or Random Forest training. This is generally acceptable for tree-based methods because monotonic scaling of a feature preserves its ordering and possible threshold partitions. Scaling is important for many distance- or gradient-based algorithms and becomes relevant for PCA.'),
('h2','7. Interview-ready explanation'),('quote','During preprocessing, I converted TotalCharges from object to numeric. This exposed 11 missing observations, which the notebook removed. I created 12-month tenure groups to represent customer lifecycle stages, removed customerID and the original tenure column, encoded Churn as 0/1, and applied one-hot encoding to categorical variables. The tree-based models used in the project do not require feature scaling.'),
('h2','8. Questions to prepare'),('qa',[
('What does errors="coerce" do?','It converts unparseable values to NaN so they can be identified and handled explicitly.'),
('What is one-hot encoding?','It represents each category with a binary indicator column, avoiding an artificial ordinal relationship between nominal categories.'),
('Why might we not scale for Random Forest?','Tree splits depend on feature ordering and thresholds. A monotonic rescaling generally preserves the ordering and candidate partitions.'),
('What is the drawback of binning tenure?','It discards within-bin variation and can create arbitrary boundaries. It should be justified and compared against retaining continuous tenure.')])
])

sec('05 - Train-Test Split and Validation Strategy', [
('h2','1. Separate features and target'),('code',"X = df.drop('Churn', axis=1)\ny = df['Churn']"),
('p','X contains predictor columns and y contains the binary outcome. The EDA notebook exports the dummy-encoded dataset to tel_churn.csv; the model notebook reads it and removes the exported dataframe index column named Unnamed: 0.'),
('h2','2. Original train-test split'),('code','x_train, x_test, y_train, y_test = train_test_split(\n    x, y, test_size=0.2\n)'),
('p','The repository uses an 80:20 split. On the cleaned 7,032-row dataset, the notebook reports 1,407 test observations, with the remainder used for training.'),
('h2','3. Recommended split'),('code','X_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.2, random_state=42, stratify=y\n)'),
('p','random_state makes the split reproducible. stratify=y preserves approximately the same class proportions in both partitions, which is useful for an imbalanced classification task.'),
('h2','4. Critical issue in the repository: resampling before splitting'),('p','The model notebook applies SMOTEENN to the entire feature matrix and target first, then splits the resampled data into train and test partitions. This is methodologically incorrect for an unbiased evaluation.'),
('formula','Repository sequence: full dataset → SMOTEENN → train/test split'),
('p','SMOTE creates synthetic observations using minority-class neighbours; ENN removes observations based on neighbour relationships. If these operations are performed before the split, the eventual test observations can influence synthetic sample generation or cleaning. Related information can therefore cross the training/test boundary, compromising test independence.'),
('h2','5. Correct approach'),('formula','Correct sequence: original data → train/test split → resample training data only → fit model → evaluate on untouched test data'),
('code','from imblearn.pipeline import Pipeline\nfrom imblearn.combine import SMOTEENN\nfrom sklearn.ensemble import RandomForestClassifier\n\npipe = Pipeline([\n    ("resample", SMOTEENN(random_state=42)),\n    ("model", RandomForestClassifier(\n        n_estimators=100, max_depth=6,\n        min_samples_leaf=8, random_state=100\n    ))\n])\npipe.fit(X_train, y_train)\ny_pred = pipe.predict(X_test)'),
('p','An imbalanced-learn Pipeline applies resampling during fit. During cross-validation, each fold’s resampling is confined to its training partition. The held-out test dataset remains in its original class distribution and is never resampled.'),
('h2','6. Cross-validation'),('p','The repository does not demonstrate cross-validation. A better development process uses StratifiedKFold to evaluate candidate models and tune hyperparameters on training data. The final test set should be held out until model selection and threshold decisions are complete.'),
('h2','7. Interview-ready explanation'),('quote','The notebook uses an 80:20 train-test split. However, it does not set a random state or stratify the target, and more importantly, it applies SMOTEENN before splitting. That is a data-leakage risk because the resampling process sees observations that later enter the test partition. I would correct this by splitting the original data first and placing SMOTEENN and the classifier in an imbalanced-learn pipeline, so resampling happens only inside each training fold.'),
('h2','8. Questions to prepare'),('qa',[
('Why do we need a test set?','To estimate generalization on observations not used to fit or select the model.'),
('Why stratify?','To preserve approximate class proportions in each partition.'),
('What is data leakage?','It is the unintended use of information unavailable at prediction time or information from evaluation data during training/model selection, causing unreliable evaluation.'),
('Should the test set be resampled?','No. It should preserve the real-world distribution to estimate performance on the intended population.'),
('Why cross-validate only within training data?','It lets us compare and tune models without repeatedly using the final test set, keeping the test estimate independent.')])
])

sec('06 - Model Selection', [
('h2','1. Algorithms used'),('p','The repository experiments with DecisionTreeClassifier and RandomForestClassifier. It also tests a Random Forest after PCA. The notebook does not show a Logistic Regression baseline or a formal model-search procedure.'),
('h2','2. Decision Tree'),('p','A Decision Tree recursively partitions the feature space using feature-threshold or category-based rules. Each internal node tests a feature condition; a terminal leaf provides a class prediction or class-probability estimate.'),
('h3','Gini impurity'),('formula','Gini = 1 - Σ(p_k²)'),('p','For binary classification, Gini = 1 - p_0² - p_1². A pure node has impurity 0. A 50:50 binary node has impurity 0.5. At each split, the algorithm seeks child nodes with low weighted impurity.'),
('formula','Weighted split impurity = (N_L/N) Gini_L + (N_R/N) Gini_R'),
('h3','Repository hyperparameters'),('code','DecisionTreeClassifier(\n    criterion="gini", random_state=100,\n    max_depth=6, min_samples_leaf=8\n)'),
('table',[['Parameter','Value','Meaning'],['criterion','gini','Impurity measure used to choose splits'],['random_state','100','Controls randomized behaviour'],['max_depth','6','Limits maximum tree depth'],['min_samples_leaf','8','Minimum samples required in a leaf']]),
('h3','Strengths and limitations'),('bullets',['Interpretable rule structure and visualizable decisions.','Captures nonlinear relationships and feature interactions.','Does not generally require scaling.','A single tree can have high variance and overfit; small data changes can produce a different tree.']),
('h2','3. Random Forest'),('p','Random Forest is an ensemble of decision trees. Each tree is trained using a bootstrap sample of the training observations, and at each split a random subset of features is considered. For classification, the trees’ outputs are aggregated, commonly by majority vote.'),
('h3','Why the ensemble helps'),('p','Individual trees can be unstable. Combining sufficiently diverse trees can reduce variance and improve stability. The benefit depends on tree diversity and model settings; Random Forest is not guaranteed to outperform every alternative.'),
('h3','Repository hyperparameters'),('code','RandomForestClassifier(\n    n_estimators=100, criterion="gini",\n    random_state=100, max_depth=6,\n    min_samples_leaf=8\n)'),
('table',[['Parameter','Value','Meaning'],['n_estimators','100','Number of trees'],['criterion','gini','Split impurity measure'],['random_state','100','Reproducibility'],['max_depth','6','Maximum depth per tree'],['min_samples_leaf','8','Minimum observations in a leaf']]),
('h3','Strengths and limitations'),('bullets',['Often more stable than a single unconstrained tree.','Captures nonlinear patterns and interactions.','Can estimate feature importance.','Less transparent than one tree; may require more memory and compute.']),
('h2','4. Decision Tree versus Random Forest'),('table',[['Aspect','Decision Tree','Random Forest'],['Structure','One tree','Ensemble of trees'],['Prediction','Single tree output','Aggregated tree outputs'],['Variance','Often higher','Often reduced through averaging'],['Interpretability','Relatively easy','More difficult'],['Compute','Lower','Higher']]),
('h2','5. Why Random Forest was selected'),('p','In the repository’s experiments, Random Forest with SMOTEENN had the highest reported aggregate metrics among the listed configurations. However, those resampled test results are compromised by resampling before splitting. Therefore, this is the author’s reported selection, not a verified conclusion that Random Forest is superior on an untouched test set.'),
('h2','6. Interview-ready explanation'),('quote','We experimented with Decision Tree and Random Forest classifiers. Decision Tree is an interpretable rule-based model that selects splits to reduce impurity, using Gini in this implementation. Random Forest combines multiple randomized trees through ensemble voting and can reduce variance relative to a single tree. The repository selected the Random Forest configuration based on its reported results, although the resampling leakage means a clean validation experiment is needed before claiming a reliable performance advantage.'),
('h2','7. Questions to prepare'),('qa',[
('What is Gini impurity?','It measures node impurity based on class proportions: 1 minus the sum of squared class probabilities.'),
('What is bootstrap sampling?','Sampling observations with replacement to create a training sample for an individual tree.'),
('Why random feature subsets?','They decorrelate trees so their errors are less similar, improving the benefit of aggregation.'),
('Why can Random Forest overfit less than a single tree?','Averaging many diverse trees often reduces variance, although unconstrained forests can still overfit or fail to generalize.'),
('Does Random Forest need scaling?','Usually not; tree split ordering is invariant to monotonic feature scaling.')])
])

sec('07 - Model Training and Hyperparameter Tuning', [
('h2','1. Training a Decision Tree'),('code','model_dt.fit(x_train, y_train)\ny_pred = model_dt.predict(x_test)'),('p','fit() learns the tree structure from labelled training data. predict() applies the learned rules to new feature rows.'),
('h2','2. SMOTE: synthetic minority oversampling'),('p','SMOTE (Synthetic Minority Over-sampling Technique) generates synthetic minority-class observations using interpolation between an observation and one of its minority-class nearest neighbours.'),
('formula','x_new = x_i + λ(x_zi - x_i), where λ is sampled between 0 and 1'),
('p','This creates points along the segment joining two minority-class observations. It differs from random oversampling, which duplicates existing minority examples. SMOTE can still create overlapping or unrealistic examples, especially when features are categorical or the minority class has complex structure.'),
('h2','3. ENN and SMOTEENN'),('p','Edited Nearest Neighbours (ENN) is a cleaning/undersampling method that removes observations whose class labels are inconsistent with their nearest neighbours. SMOTEENN first applies SMOTE and then ENN cleaning. The intention is to increase minority representation and remove ambiguous/noisy examples.'),
('note','The repository uses SMOTEENN on the complete dataset before the train-test split. This is a methodological error. Use the resampler only inside the training portion of an imbalanced-learn Pipeline. Also consider categorical-aware resampling such as SMOTENC where appropriate; plain SMOTE on one-hot encoded categorical variables can create fractional dummy values.'),
('h2','4. Random Forest training'),('code','model_rf_smote = RandomForestClassifier(\n    n_estimators=100, criterion="gini",\n    random_state=100, max_depth=6,\n    min_samples_leaf=8\n)\nmodel_rf_smote.fit(xr_train1, yr_train1)'),
('p','The model is fit using the resampled training partition as generated by the notebook’s workflow. Its reported evaluation must be interpreted with the leakage caveat described in the validation section.'),
('h2','5. Was hyperparameter tuning performed?'),('p','The repository specifies hyperparameters manually. It does not demonstrate GridSearchCV, RandomizedSearchCV, Bayesian optimization, or a systematic cross-validated tuning procedure. Do not claim that formal hyperparameter tuning was performed.'),
('h3','Suggested tuning approach'),('code','from imblearn.pipeline import Pipeline\nfrom imblearn.combine import SMOTEENN\nfrom sklearn.model_selection import RandomizedSearchCV, StratifiedKFold\nfrom sklearn.ensemble import RandomForestClassifier\n\npipe = Pipeline([\n    ("resample", SMOTEENN(random_state=42)),\n    ("model", RandomForestClassifier(random_state=100))\n])\nparam_dist = {\n    "model__n_estimators": [100, 200, 300],\n    "model__max_depth": [4, 6, 8, 10, None],\n    "model__min_samples_leaf": [2, 4, 8, 10],\n    "model__max_features": ["sqrt", "log2"]\n}\ncv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)\nsearch = RandomizedSearchCV(\n    pipe, param_distributions=param_dist,\n    n_iter=25, scoring="average_precision",\n    cv=cv, random_state=42, n_jobs=-1\n)\nsearch.fit(X_train, y_train)'),
('p','The exact scoring metric should reflect the business objective. Average precision / PR-AUC can be informative for the positive minority class; recall at a specified precision or a cost-based objective may be more appropriate in some settings.'),
('h2','6. Interview-ready explanation'),('quote','The notebooks train Decision Tree and Random Forest classifiers and use SMOTEENN to address class imbalance. SMOTE creates synthetic minority observations, while ENN removes observations based on nearest-neighbour disagreement. The hyperparameters were manually specified; there is no documented GridSearchCV or RandomizedSearchCV. A stronger approach is to place resampling and the classifier in a pipeline and tune it using stratified cross-validation.'),
('h2','7. Questions to prepare'),('qa',[
('How does SMOTE generate a sample?','It interpolates between a minority observation and one of its minority-class nearest neighbours.'),
('What does ENN do?','It removes observations considered inconsistent with their nearest-neighbour labels.'),
('Why is resampling inside cross-validation?','To ensure each fold’s validation data does not influence synthetic sample generation or cleaning.'),
('Grid search versus random search?','Grid search evaluates every specified combination. Random search samples a fixed number of combinations and can explore broad spaces more efficiently when only a few hyperparameters matter strongly.'),
('What is overfitting?','A model fits training-specific patterns or noise and performs substantially worse on unseen data.')])
])

sec('08 - Model Evaluation', [
('h2','1. Confusion matrix'),('p','For this project, churn is the positive class. TP is a churner correctly predicted as churn; FN is a churner predicted as non-churn; FP is a non-churner predicted as churn; TN is a non-churner correctly predicted as non-churn.'),
('table',[['','Predicted churn','Predicted non-churn'],['Actual churn','TP','FN'],['Actual non-churn','FP','TN']]),
('h2','2. Evaluation metrics'),('formula','Accuracy = (TP + TN) / (TP + TN + FP + FN)'),('formula','Precision = TP / (TP + FP)'),('formula','Recall = TP / (TP + FN)'),('formula','F1 = 2 × Precision × Recall / (Precision + Recall)'),
('p','Accuracy is the fraction of all predictions that are correct. Precision answers: among customers flagged as churners, what fraction actually churned? Recall answers: among all actual churners, what fraction did we identify? F1 is the harmonic mean of precision and recall.'),
('h2','3. Why recall and precision matter'),('p','A false negative is a churner missed by the model. If the business does not contact that customer, it loses a potential retention opportunity. A false positive is a customer flagged as at risk who would not have churned; outreach may waste campaign budget or annoy the customer. A sensible decision threshold balances these costs.'),
('h2','4. Reported baseline results'),('table',[['Model (original class distribution)','Churn precision','Churn recall','Churn F1','Accuracy'],['Decision Tree','0.63','0.49','0.55','about 0.78'],['Random Forest','0.69','0.45','0.55','about 0.80']]),
('p','The model notebook reports 1,407 test observations: 1,023 non-churn and 384 churn. Random Forest has higher churn precision but lower churn recall than Decision Tree in this baseline comparison. This illustrates why accuracy alone is inadequate.'),
('h2','5. Reported results after SMOTEENN'),('table',[['Configuration','Churn precision','Churn recall','Churn F1','Reported accuracy'],['Decision Tree + SMOTEENN','0.91','0.98','0.94','0.9344'],['Random Forest + SMOTEENN','0.94','0.96','0.95','0.9427'],['Random Forest + SMOTEENN + PCA','0.72','0.81','0.77','0.7239']]),
('note','The post-SMOTEENN test results are not valid estimates of generalization because the repository resamples the full dataset before splitting it. Present them only as reported notebook outputs and explicitly qualify them.'),
('h2','6. Confusion matrices reported'),('p','Decision Tree + SMOTEENN: [[477, 63], [14, 620]]. Random Forest + SMOTEENN: [[478, 40], [27, 625]]. In scikit-learn ordering, rows are actual classes and columns are predicted classes.'),
('h2','7. PCA experiment'),('p','The repository applies PCA(n_components=0.9) to the resampled training data, fits PCA on training data and transforms the corresponding test data. The PCA Random Forest result is reported as approximately 72.39% accuracy, with churn precision 0.72, recall 0.81 and F1 0.77. The author therefore retains the Random Forest without PCA.'),
('p','PCA projects features into orthogonal linear combinations called principal components, ordered by explained variance. Retaining 90% variance does not guarantee retaining the information most useful for classification. PCA can also make tree-based splits less directly useful because the components mix original variables.'),
('h2','8. Additional metrics worth knowing'),('bullets',['ROC-AUC evaluates ranking across true-positive and false-positive rates.','PR-AUC / average precision summarizes precision-recall behaviour and is often informative when the positive class is uncommon.','Calibration checks whether predicted probabilities correspond to observed event frequencies.','A confusion matrix should be evaluated at the chosen operating threshold.']),
('h2','9. Interview-ready explanation'),('quote','Initially, the Decision Tree and Random Forest showed weak recall for churners, around 49% and 45% respectively. The notebook then explored SMOTEENN and reported much higher scores, with Random Forest reaching approximately 94% accuracy and 96% churn recall. However, because SMOTEENN was applied before the train-test split, those resampled test figures are subject to leakage and should not be treated as reliable unseen-data performance. I would rerun evaluation with stratified splitting and resampling confined to training folds.'),
('h2','10. Questions to prepare'),('qa',[
('Why can accuracy be misleading?','A majority-class model can score around the majority prevalence while missing the minority class entirely.'),
('What is the precision-recall trade-off?','Changing the threshold typically changes both: flagging more observations tends to increase recall but can reduce precision.'),
('Why PR-AUC for an imbalanced task?','It focuses on precision and recall of the positive class and is often more informative than ROC-AUC when the positive class is rare.'),
('What does PCA(n_components=0.9) mean?','Retain enough components to explain at least 90% of the variance in the data used to fit PCA.'),
('Why can PCA reduce tree performance?','Linear combinations can obscure simple axis-aligned threshold patterns, and variance preservation does not equal predictive-information preservation.')])
])

sec('09 - Business Interpretation, Results and Limitations', [
('h2','1. Repository’s selected model'),('p','The author selects Random Forest with SMOTEENN because it has the strongest reported overall metrics among the tried configurations. The model is serialized to model.sav using pickle. The repository includes app.py, which loads the saved estimator and obtains predictions for entered customer attributes.'),
('code','import pickle\npickle.dump(model_rf_smote, open("model.sav", "wb"))\nloaded_model = pickle.load(open("model.sav", "rb"))'),
('note','The application code recreates dummy columns by concatenating the input row with first_telc.csv and applying get_dummies. This can be fragile if category levels or column ordering differ from training. A fitted preprocessing-and-model pipeline is safer. Deployment is outside the requested interview scope, but this detail helps explain the artifact.'),
('h2','2. Business observations'),('table',[['Observed characteristic','Notebook association','Possible business question'],['Month-to-month contract','Higher churn','Can suitable longer-term plans improve retention?'],['No online security / tech support','Higher churn','Are customers aware of included support/security options?'],['Electronic check','Higher churn','Is payment friction or customer profile a confounder?'],['Short tenure','Higher churn','Would onboarding support improve early retention?'],['Higher monthly charges','Higher churn noted','Is perceived value or price sensitivity involved?']]),
('p','These patterns generate hypotheses for business teams; they do not prove that changing a feature will change churn. For example, an offer or service intervention should be evaluated through a randomized or otherwise credible causal design.'),
('h2','3. Limitations'),('numbered',['Resampling leakage: SMOTEENN is run before train-test split, compromising the post-resampling test metrics.','No stratification or fixed random seed in the original split.','No demonstrated cross-validation.','No systematic hyperparameter tuning; values are manually specified.','No documented threshold optimization or probability calibration.','No comprehensive baseline comparison, such as Logistic Regression.','No systematic final-model feature-importance or SHAP analysis.','Potential fragility in separately recreating one-hot columns in the application.','EDA observations are associative and not causal.']),
('h2','4. Stronger experimental plan'),('numbered',['Clean and validate the original dataset; inspect the 11 missing TotalCharges records.','Create a stratified train/test split before any learned transformations or resampling.','Build a baseline with Logistic Regression and a tree model.','Use a preprocessing + resampling + classifier pipeline. Consider categorical-aware resampling where suitable.','Compare Decision Tree, Random Forest, and a boosting model through stratified cross-validation.','Tune hyperparameters using a metric aligned with business costs.','Choose a threshold using validation predictions and an explicit cost/benefit framework.','Evaluate once on the untouched test set; report precision, recall, F1, PR-AUC, ROC-AUC, confusion matrix, and calibration as appropriate.']),
('h2','5. Interview-ready explanation'),('quote','The repository selects Random Forest with SMOTEENN based on its reported metrics. The EDA suggests that contract type, tenure, payment method, and service subscriptions are associated with churn. The key limitation is that resampling was performed before splitting, so the high resampled test metrics are not trustworthy. I would correct that with a stratified holdout, a leakage-safe pipeline, cross-validation, systematic tuning, and threshold selection based on the cost of missed churners versus unnecessary retention outreach.'),
('h2','6. Questions to prepare'),('qa',[
('Can an important feature be a cause of churn?','Not from predictive importance or correlation alone. Importance measures model reliance or association, not causal effect.'),
('What is permutation importance?','It measures the drop in a model metric after randomly permuting a feature, breaking its relationship with the target while leaving other columns unchanged.'),
('What is SHAP?','A framework that attributes a prediction to feature contributions using Shapley-value concepts. It explains model output, not causal effects.'),
('Why choose a threshold other than 0.5?','The best threshold depends on class prevalence, probability calibration, and relative costs of false positives and false negatives.'),
('What would you say if an interviewer challenges the reported 94% accuracy?','I would clarify it is the repository’s reported score, but because SMOTEENN was applied before the split, it is contaminated by leakage. I would not claim it as unbiased test performance and would rerun the experiment correctly.')])
])

sec('10 - Two-Minute Interview Narration', [
('note','Practice this as a natural explanation, not as a script to recite word-for-word. It deliberately distinguishes repository-reported results from trustworthy validation.'),
('h2','Two-minute narration'),('quote','The objective of this project was to predict customer churn for a telecom company. Customer churn refers to customers discontinuing their telecom services. Since retaining existing customers is an important business priority, we wanted to identify customers who were likely to leave so that the business could prioritize retention actions.\n\nWe used the IBM Telco Customer Churn dataset, which contained around 7,043 customer records and 21 columns. It included demographic information, services subscribed, contract details, tenure, and billing information. The target variable was Churn, and the class distribution was imbalanced, with approximately 73% non-churn and 27% churn customers.\n\nDuring EDA, we observed higher churn among month-to-month contract customers, customers without online security or technical support, electronic-check users, and customers with shorter tenure.\n\nFor preprocessing, we converted TotalCharges to numeric, handled 11 missing observations, created tenure groups, removed the customer identifier and original tenure column, encoded the target, and one-hot encoded categorical variables.\n\nWe experimented with Decision Tree and Random Forest classifiers. Since the baseline models had limited recall for churners, the repository explored SMOTEENN, which combines synthetic minority oversampling with nearest-neighbour cleaning. Random Forest with SMOTEENN produced the strongest reported result, at approximately 94% accuracy and 96% churn recall. The notebook also tested PCA, but that configuration performed worse.\n\nOne important limitation I identified is that SMOTEENN was applied before the train-test split, introducing data leakage. Therefore, I would not present the resampled test score as a reliable estimate of unseen-data performance. I would improve the experiment by splitting first, applying resampling only within training folds, using stratified cross-validation, tuning the model systematically, and selecting a decision threshold based on business costs.'),
('h2','Shorter 60-second version'),('quote','I worked on a telecom customer churn prediction problem using the IBM Telco Customer Churn dataset. The goal was to identify customers likely to discontinue service, so the business could prioritize retention efforts. The data contained around 7,043 observations and 21 columns, with an imbalanced target of roughly 73% non-churn and 27% churn. EDA highlighted higher churn among month-to-month contract customers, customers without online security or technical support, electronic-check users, and customers with shorter tenure. After cleaning, tenure grouping, and one-hot encoding, the repository compared Decision Tree and Random Forest. It explored SMOTEENN to address imbalance and selected Random Forest based on its reported metrics. A critical improvement is to apply SMOTEENN only after splitting, inside the training pipeline, because the original workflow resampled before splitting and therefore leaked information into the test process.'),
('h2','Follow-up questions the narration invites'),('qa',[
('What was your individual contribution?','Answer honestly based on your actual work. Since this is a repository being studied for interview preparation, do not imply you authored or personally implemented steps you did not perform.'),
('Why did you choose Random Forest?','The repository’s reported comparison favoured it after resampling, but a correct leakage-free validation is required to confirm that selection.'),
('What was the biggest issue you found?','SMOTEENN was applied before the train-test split, contaminating the evaluation. The correct approach is to split first and resample training folds only.'),
('What metric matters most?','It depends on the cost of missed churners and false alarms. Recall is important when missing a churner is costly, but precision and campaign cost must also be considered.')]),
('h2','Presentation discipline'),('bullets',['Say “the repository reports” when quoting its metrics.','Do not claim formal hyperparameter tuning or cross-validation; they are not demonstrated.','Do not claim SMOTEENN results are valid test estimates.','Be clear about what the original project did versus what you recommend improving.','Never claim personal implementation ownership unless it is true.'])
])

# Styling helpers
NAVY='17365D'; BLUE='1F4E79'; LIGHT='D9EAF7'; PALE='F3F6FA'; GREY='5B6573'; ORANGE='FCE4D6'

def shade(cell, fill):
    tcPr=cell._tc.get_or_add_tcPr(); shd=OxmlElement('w:shd'); shd.set(qn('w:fill'),fill); tcPr.append(shd)

def set_cell_text(cell, txt, bold=False, color=None, size=9):
    cell.text=''; p=cell.paragraphs[0]; p.paragraph_format.space_after=Pt(2)
    r=p.add_run(str(txt)); r.bold=bold; r.font.size=Pt(size)
    if color: r.font.color.rgb=RGBColor.from_string(color)
    cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER

def add_field(paragraph, field):
    run=paragraph.add_run()
    fldChar1=OxmlElement('w:fldChar'); fldChar1.set(qn('w:fldCharType'),'begin')
    instr=OxmlElement('w:instrText'); instr.set(qn('xml:space'),'preserve'); instr.text=field
    fldChar2=OxmlElement('w:fldChar'); fldChar2.set(qn('w:fldCharType'),'end')
    run._r.append(fldChar1); run._r.append(instr); run._r.append(fldChar2)

def build_doc(title, blocks, outpath):
    d=Document(); sec0=d.sections[0]
    sec0.top_margin=Inches(.68); sec0.bottom_margin=Inches(.68); sec0.left_margin=Inches(.78); sec0.right_margin=Inches(.78)
    styles=d.styles
    styles['Normal'].font.name='Aptos'; styles['Normal'].font.size=Pt(9.5); styles['Normal'].font.color.rgb=RGBColor(38,48,60)
    styles['Normal'].paragraph_format.space_after=Pt(5)
    for st,sz,col in [('Title',24,NAVY),('Heading 1',17,NAVY),('Heading 2',13,BLUE),('Heading 3',10,BLUE)]:
        s=styles[st]; s.font.name='Aptos Display'; s.font.size=Pt(sz); s.font.bold=True; s.font.color.rgb=RGBColor.from_string(col)
        s.paragraph_format.space_before=Pt(9); s.paragraph_format.space_after=Pt(4)
    header=sec0.header.paragraphs[0]; header.text='ML PLACEMENT PREPARATION  |  PROJECT 01'; header.style='Caption'
    header.runs[0].font.color.rgb=RGBColor.from_string(GREY); header.runs[0].font.size=Pt(8)
    footer=sec0.footer.paragraphs[0]; footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
    rr=footer.add_run('Customer Churn Prediction  •  Page '); rr.font.size=Pt(8); rr.font.color.rgb=RGBColor.from_string(GREY); add_field(footer,'PAGE')
    p=d.add_paragraph(); p.style='Title'; p.add_run(title)
    p=d.add_paragraph(); p.paragraph_format.space_after=Pt(12)
    r=p.add_run('Customer Churn Prediction  |  Repository-based interview study guide'); r.italic=True; r.font.color.rgb=RGBColor.from_string(GREY); r.font.size=Pt(9)
    p=d.add_paragraph(); p.paragraph_format.space_after=Pt(12)
    r=p.add_run('Source: '); r.bold=True; r.font.size=Pt(8)
    r=p.add_run(SOURCE); r.font.size=Pt(8); r.font.color.rgb=RGBColor.from_string(BLUE)
    for typ,val in blocks:
        if typ=='h2': d.add_heading(val, level=2)
        elif typ=='h3': d.add_heading(val, level=3)
        elif typ=='p': d.add_paragraph(val)
        elif typ=='note':
            t=d.add_table(rows=1, cols=1); t.alignment=WD_TABLE_ALIGNMENT.CENTER; c=t.cell(0,0); shade(c,ORANGE)
            p=c.paragraphs[0]; p.paragraph_format.space_after=Pt(4); r=p.add_run('Important: '); r.bold=True; r.font.color.rgb=RGBColor(156,65,25); p.add_run(val)
            d.add_paragraph().paragraph_format.space_after=Pt(1)
        elif typ=='formula':
            t=d.add_table(rows=1,cols=1); c=t.cell(0,0); shade(c,LIGHT); p=c.paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.CENTER
            r=p.add_run(val); r.bold=True; r.font.name='Cambria Math'; r.font.size=Pt(10); r.font.color.rgb=RGBColor.from_string(NAVY)
        elif typ=='code':
            t=d.add_table(rows=1,cols=1); c=t.cell(0,0); shade(c,'F1F3F5'); p=c.paragraphs[0]; p.paragraph_format.space_after=Pt(2)
            for i,line in enumerate(val.splitlines()):
                if i: p.add_run().add_break()
                r=p.add_run(line); r.font.name='Consolas'; r.font.size=Pt(8); r.font.color.rgb=RGBColor.from_string('263238')
        elif typ in ('bullets','numbered'):
            style='List Bullet' if typ=='bullets' else 'List Number'
            for x in val:
                p=d.add_paragraph(style=style); p.paragraph_format.space_after=Pt(2); p.add_run(x)
        elif typ=='quote':
            t=d.add_table(rows=1,cols=1); c=t.cell(0,0); shade(c,PALE); p=c.paragraphs[0]; p.paragraph_format.left_indent=Inches(.08); p.paragraph_format.right_indent=Inches(.08)
            for i,line in enumerate(val.split('\n')):
                if i: p.add_run().add_break()
                r=p.add_run(line); r.italic=True
        elif typ=='table':
            table=d.add_table(rows=0, cols=len(val[0])); table.alignment=WD_TABLE_ALIGNMENT.CENTER; table.style='Table Grid'
            for ri,row in enumerate(val):
                cells=table.add_row().cells
                for ci,txt in enumerate(row):
                    set_cell_text(cells[ci],txt,bold=(ri==0),color='FFFFFF' if ri==0 else None,size=8.2)
                    if ri==0: shade(cells[ci],BLUE)
                    elif ri%2==0: shade(cells[ci],'F5F8FB')
            d.add_paragraph().paragraph_format.space_after=Pt(1)
        elif typ=='qa':
            for q,a in val:
                p=d.add_paragraph(); p.paragraph_format.space_before=Pt(4); p.paragraph_format.space_after=Pt(1)
                r=p.add_run('Q. '+q); r.bold=True; r.font.color.rgb=RGBColor.from_string(BLUE)
                p=d.add_paragraph(a); p.paragraph_format.left_indent=Inches(.18); p.paragraph_format.space_after=Pt(5)
    d.core_properties.title=title; d.core_properties.subject='Machine learning placement preparation'; d.core_properties.author=''
    d.save(outpath)

# Make docx and pdfs
for idx,(title,blocks) in enumerate(sections,1):
    base=f'{idx:02d}_{re.sub(r"[^A-Za-z0-9]+","_",title.split(" - ",1)[-1]).strip("_")}'
    docx=OUT/(base+'.docx'); build_doc(title,blocks,docx)
    subprocess.run(['python','/home/oai/skills/docx/render_docx.py',str(docx),'--output_dir',str(OUT/'render'/base),'--emit_pdf'],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    produced=OUT/'render'/base/(docx.stem+'.pdf')
    pdf=OUT/(base+'.pdf'); produced.replace(pdf)
    docx.unlink()
# README and ZIP
readme='''# Customer Churn Prediction - Interview Study Pack\n\nRepository analyzed: '''+SOURCE+'''\n\nThis pack contains separate PDFs for the nine agreed project sections, plus a dedicated two-minute interview narration. The notes distinguish the repository implementation from recommended corrections.\n\n## Important methodological finding\nThe notebook applies SMOTEENN before train-test splitting. This is data leakage and makes its post-resampling test metrics unreliable as estimates of unseen-data performance. The notes explicitly flag this and provide a corrected pipeline approach.\n\n## Files\n'''
for p in sorted(OUT.glob('*.pdf')): readme+=f'- {p.name}\n'
(OUT/'README.md').write_text(readme)
zip_path=Path('/mnt/data/Customer_Churn_Prediction_Study_Pack.zip')
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.iterdir()):
        if p.is_file(): z.write(p,arcname='01_Customer_Churn_Prediction/'+p.name)
print('ZIP',zip_path,zip_path.stat().st_size)
print('PDFS',len(list(OUT.glob('*.pdf'))))
