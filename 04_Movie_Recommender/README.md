# Movie Recommender System — Interview Study Pack

Source archive supplied in this conversation: `Movie-recommender-system-main.zip`
Notebook: `notebook.ipynb`
App: `app.py`

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
- Notebook expects `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv`; these source CSVs are not included in the supplied ZIP.
- Movies has 4,803 rows before joining; after processing the vector matrix is reported as (4,806, 5,000), so merge-on-title duplicates/mismatches should be investigated.
- Fields are parsed and combined into `tags`: overview, genres, keywords, top-three cast and director.
- CountVectorizer uses `max_features=5000` and English stop-word removal.
- Pairwise cosine similarity is calculated; the example for Gandhi returns five titles.
- There is no train/test split, user feedback, ranking metric, or systematic tuning in the repository.
- Notebook saves `movie_list.pkl` and `similarity.pkl`; app expects them under `model/`, but the supplied ZIP does not contain those artifacts.
- The app has a hard-coded TMDB API key. It should be treated as exposed and moved to a secrets store; rotate/revoke the key.
- No deployment guide is included in this study pack.

The PDFs distinguish actual repository implementation from recommended improvements.
