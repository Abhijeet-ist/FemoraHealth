# FemoraHealth — PCOS Prediction
### INT 374: Data Science Toolbox — Python Programming

A comprehensive data science project demonstrating end-to-end machine learning pipeline for **Polycystic Ovary Syndrome (PCOS)** diagnosis prediction using clinical, hormonal, and lifestyle features.

---

## 📊 Project Overview

| Item | Details |
|---|---|
| **Dataset** | 541 patients, 42 clinical features |
| **Task** | Binary Classification — PCOS (Yes/No) |
| **Best Model** | Random Forest (F1=0.87, AUC=0.96) |
| **Top Predictors** | Total Follicles, Symptom Score, Skin Darkening |

## 🗂️ Project Structure

```
FemoraHealth/
├── data/
│   ├── PCOS_data_without_infertility.xlsx   # Raw dataset
│   ├── PCOS_infertility.csv                 # Secondary dataset
│   ├── PCOS_cleaned.csv                     # Cleaned (42 features)
│   └── PCOS_final.csv                       # Feature-selected (32 features)
├── notebooks/
│   ├── 01_data_loading_preprocessing.ipynb   # Data cleaning & validation
│   ├── 02_eda_visualization.ipynb            # 23 EDA visualizations
│   ├── 03_feature_engineering_selection.ipynb # Feature engineering & ranking
│   ├── 04_model_building_evaluation.ipynb    # 6 models + tuning
│   └── 05_shap_analysis.ipynb               # SHAP explainability
├── outputs/
│   ├── figures/          # 38 high-res visualizations
│   ├── models/           # best_model.pkl, scaler.pkl
│   └── reports/          # Validation & comparison reports
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run all notebooks
cd notebooks
python3 01_data_loading_preprocessing.py
python3 02_eda_visualization.py
python3 03_feature_engineering_selection.py
python3 04_model_building_evaluation.py
python3 05_shap_analysis.py
```

## 📈 Model Performance

| Model | Accuracy | Precision | Recall | F1 | AUC |
|---|---|---|---|---|---|
| Logistic Regression | 0.85 | 0.76 | 0.81 | 0.78 | 0.93 |
| Decision Tree | 0.87 | 0.85 | 0.75 | 0.80 | 0.84 |
| **Random Forest** | **0.92** | **0.91** | **0.83** | **0.87** | **0.96** |
| SVM | 0.88 | 0.83 | 0.81 | 0.82 | 0.93 |
| KNN | 0.83 | 0.77 | 0.69 | 0.73 | 0.87 |
| XGBoost | 0.88 | 0.84 | 0.78 | 0.81 | 0.94 |

## 📝 Skills Demonstrated

- Data loading, cleaning, merging, type conversion
- Missing value analysis & imputation
- Outlier detection (IQR) & treatment
- 38 professional visualizations (distributions, heatmaps, scatter, violin, radar, QQ)
- Feature engineering (6 new features created)
- Multi-method feature selection (ANOVA, Chi², MI, correlation)
- 6 ML classifiers with SMOTE class balancing
- Hyperparameter tuning (GridSearchCV)
- Cross-validation & learning curves
- SHAP explainability (beeswarm, waterfall, dependence, force plots)
# FemoraHealth
