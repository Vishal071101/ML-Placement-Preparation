# Customer Churn Prediction - Interview Study Pack

Repository analyzed: https://github.com/YuvarajGarla/Customer-churn-prediction

This pack contains separate PDFs for the nine agreed project sections, plus a dedicated two-minute interview narration. The notes distinguish the repository implementation from recommended corrections.

## Important methodological finding
The notebook applies SMOTEENN before train-test splitting. This is data leakage and makes its post-resampling test metrics unreliable as estimates of unseen-data performance. The notes explicitly flag this and provide a corrected pipeline approach.

## Files
- 01_Business_Problem_and_Objective.pdf
- 02_Dataset_Understanding.pdf
- 03_Exploratory_Data_Analysis.pdf
- 04_Preprocessing_and_Feature_Engineering.pdf
- 05_Train_Test_Split_and_Validation_Strategy.pdf
- 06_Model_Selection.pdf
- 07_Model_Training_and_Hyperparameter_Tuning.pdf
- 08_Model_Evaluation.pdf
- 09_Business_Interpretation_Results_and_Limitations.pdf
- 10_Two_Minute_Interview_Narration.pdf
