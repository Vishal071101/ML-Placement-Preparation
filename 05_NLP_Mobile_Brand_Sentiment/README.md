# NLP Mobile Brand Sentiment & Headline Generator — Interview Study Pack

Source archive: `NLP-Sentiment-Classification-of-Mobile-brands-main.zip`
Notebook: `main.ipynb`
Supporting materials: `Report.pdf`, `presentation.pdf`, `bridgei2i-PS.pdf`, `TO-DO.md`

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

## Repository facts and caveats
- Challenge pipeline: mobile-tech theme classification → brand extraction → language detection/translation → brand-specific sentiment → English article headline generation.
- Report specifies 3,000/600/400 stratified train/validation/test partitions separately for articles and tweets.
- Theme identification uses TF-IDF + XGBoost; brand identification uses regex over about 150 brands; sentiment combines contextual BERT, lightweight TF-IDF, dependency/lexicon approaches; headline generation uses fine-tuned T5-base.
- Notebook evaluation snapshot: 222 articles and 210 tweets initially displayed; 71 articles and 62 tweets predicted mobile-tech; 557 brand-level output rows.
- Recorded total runtime is about 361.98 seconds; translation takes about 290.37 seconds.
- The notebook does not show final numeric theme/sentiment/brand/headline evaluation metrics; do not invent them.
- The supplied archive lacks `evaluation_data.xlsx`, original training data, source Python modules and model checkpoints. It downloads model artifacts externally and imports modules from an AHSG-InterIIT directory.
- No deployment guide is included.

The PDFs distinguish project report claims, notebook-observed outputs and recommended improvements. They intentionally do not claim a final composite score.
