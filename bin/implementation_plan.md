# INT 374 — PCOS Data Science Project: Implementation Plan

## Project Overview

**Subject**: INT 374 — Data Science Toolbox: Python Programming  
**Dataset**: PCOS (Polycystic Ovary Syndrome) clinical data  
**Objective**: Binary classification — predict PCOS diagnosis (Y/N) from clinical, hormonal, and lifestyle features. Demonstrate end-to-end data science skills: preprocessing, EDA, visualization, modeling, SHAP interpretation, and Streamlit deployment.

---

## Dataset Profile

| Property | Value |
|---|---|
| **Primary file** | [data/PCOS_data_without_infertility.xlsx](file:///Users/abhijeet.ist/Downloads/FemoraHealth/data/PCOS_data_without_infertility.xlsx) (sheet: `Full_new`) |
| **Secondary file** | [data/PCOS_infertility.csv](file:///Users/abhijeet.ist/Downloads/FemoraHealth/data/PCOS_infertility.csv) (redundant subset — 6 cols) |
| **Samples** | 541 |
| **Features** | 45 raw → ~41 usable (after cleanup) |
| **Target** | `PCOS (Y/N)` → Binary (0/1) |
| **Class ratio** | 364 non-PCOS (67.3%) / 177 PCOS (32.7%) — moderate imbalance |
| **Missing values** | Minimal — `Marraige Status (Yrs)`: 1, `Fast food (Y/N)`: 1, `Unnamed: 44`: 539 |
| **Junk columns** | `Unnamed: 44` (539/541 nulls), `Sl. No`, `Patient File No.` (IDs) |
| **Dtype issues** | `II beta-HCG(mIU/mL)` and `AMH(ng/mL)` stored as `object` → need numeric conversion |
| **Binary features** | 10 (Weight gain, Hair growth, Skin darkening, Hair loss, Pimples, Fast food, Exercise, Pregnant, PCOS, Cycle) |

---

## User Review Required

> [!IMPORTANT]
> **Model selection**: The plan includes 6 models (Logistic Regression, Decision Tree, Random Forest, SVM, KNN, XGBoost). Confirm this is sufficient, or if you want additional models (e.g., LightGBM, Neural Network).

> [!IMPORTANT]
> **Notebook vs Scripts**: I will implement this as **Jupyter notebooks** (`.ipynb`) for a university project presentation. If you prefer `.py` scripts instead, let me know.

> [!NOTE]
> The CSV file ([PCOS_infertility.csv](file:///Users/abhijeet.ist/Downloads/FemoraHealth/data/PCOS_infertility.csv)) is a redundant subset of the Excel data (same 6 columns). I will merge them by using the Excel as the primary source and supplementing any missing values from the CSV.

---

## Proposed Changes

### Project Structure

```
FemoraHealth/
├── venv/                              # Virtual environment
├── data/
│   ├── PCOS_data_without_infertility.xlsx
│   └── PCOS_infertility.csv
├── notebooks/
│   ├── 01_data_loading_preprocessing.ipynb
│   ├── 02_eda_visualization.ipynb
│   ├── 03_feature_engineering_selection.ipynb
│   ├── 04_model_building_evaluation.ipynb
│   └── 05_shap_analysis.ipynb
├── outputs/
│   ├── figures/                       # All saved plots
│   ├── reports/                       # Validation reports
│   └── models/                       # Saved model pickle files
├── requirements.txt
└── README.md
```

---

### Phase 1: Environment & Dependencies

#### [NEW] [requirements.txt](file:///Users/abhijeet.ist/Downloads/FemoraHealth/requirements.txt)

Core libraries: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `xgboost`, `shap`, `openpyxl`, `jupyter`, `missingno`, `imbalanced-learn`, `joblib`

---

### Phase 2: Data Loading & Preprocessing

#### [NEW] [01_data_loading_preprocessing.ipynb](file:///Users/abhijeet.ist/Downloads/FemoraHealth/notebooks/01_data_loading_preprocessing.ipynb)

**Steps:**
1. Load Excel (`Full_new` sheet) + CSV
2. Merge datasets (supplement missing beta-HCG and AMH from CSV)
3. Drop junk columns (`Unnamed: 44`, `Sl. No`, `Patient File No.`)
4. Clean column names (strip whitespace, standardize)
5. Fix dtypes: convert `II beta-HCG` and `AMH` from object → float
6. Handle missing values:
   - `Marraige Status (Yrs)`: median imputation (1 missing)
   - `Fast food (Y/N)`: mode imputation (1 missing)
7. Outlier detection (IQR method + Z-score) with visualizations
8. Save cleaned dataset as `data/PCOS_cleaned.csv`

**Outputs:**
- Dataset Validation Report (pre and post cleaning)
- Missing Data Analysis heatmap (using `missingno`)
- Missing data bar chart
- Data quality summary table

---

### Phase 3: EDA & Visualizations

#### [NEW] [02_eda_visualization.ipynb](file:///Users/abhijeet.ist/Downloads/FemoraHealth/notebooks/02_eda_visualization.ipynb)

**Visualizations to generate (20+ plots):**

| # | Plot Type | Details |
|---|---|---|
| 1 | **Target Distribution** | Bar + Pie chart of PCOS vs Non-PCOS |
| 2 | **Missing Data Heatmap** | `missingno` matrix visualization |
| 3 | **Missing Data Bar Chart** | Per-column missing percentages |
| 4 | **Distributions** | Histograms + KDE for all continuous features |
| 5 | **Box Plots** | All numeric features grouped by PCOS status |
| 6 | **Violin Plots** | Key hormonal features by PCOS status |
| 7 | **Correlation Heatmap** | Full-feature annotated heatmap |
| 8 | **Top Correlations Bar** | Top 15 features correlated with target |
| 9 | **Pair Plot** | Top 5 features colored by PCOS status |
| 10 | **Count Plots** | All binary features split by PCOS |
| 11 | **Age vs BMI Scatter** | Colored by PCOS status |
| 12 | **Hormonal Profile** | FSH, LH, TSH, AMH — grouped bar charts |
| 13 | **BMI Distribution** | By PCOS status (overlapping KDE) |
| 14 | **Follicle Analysis** | Left vs Right follicle count by PCOS |
| 15 | **Waist-Hip Ratio** | Distribution by PCOS status |
| 16 | **Blood Pressure Analysis** | Systolic vs Diastolic scatter by PCOS |
| 17 | **Lifestyle Factors Heatmap** | Binary lifestyle features vs PCOS |
| 18 | **Feature Spread Radar Chart** | Mean feature values PCOS vs Non-PCOS |
| 19 | **Outlier Summary** | IQR-based outlier count per feature |
| 20 | **QQ Plots** | Normality check for key features |

All plots saved to `outputs/figures/`.

---

### Phase 4: Feature Engineering & Selection

#### [NEW] [03_feature_engineering_selection.ipynb](file:///Users/abhijeet.ist/Downloads/FemoraHealth/notebooks/03_feature_engineering_selection.ipynb)

**Steps:**
1. Create new features (e.g., LH/FSH ratio already exists, BMI categories, follicle total)
2. Correlation-based feature elimination (drop features with >0.9 inter-correlation)
3. Chi-square test for binary features vs target
4. ANOVA F-test for continuous features vs target
5. Mutual Information scores
6. Feature ranking visualization
7. Save final feature-selected dataset

---

### Phase 5: Model Building & Evaluation

#### [NEW] [04_model_building_evaluation.ipynb](file:///Users/abhijeet.ist/Downloads/FemoraHealth/notebooks/04_model_building_evaluation.ipynb)

**Pipeline:**
1. Train/test split (80/20, stratified)
2. Feature scaling (StandardScaler)
3. Handle class imbalance (SMOTE)
4. Train 6 models:
   - Logistic Regression
   - Decision Tree
   - Random Forest
   - Support Vector Machine (SVM)
   - K-Nearest Neighbors (KNN)
   - XGBoost
5. Cross-validation (5-fold stratified)
6. Hyperparameter tuning (GridSearchCV on top 2 models)

**Evaluation Outputs:**

| Output | Description |
|---|---|
| **Confusion Matrix** | Heatmap for each model |
| **ROC Curve** | All models on single plot + AUC scores |
| **Precision-Recall Curve** | All models overlaid |
| **Classification Report** | Table — Precision, Recall, F1, Accuracy |
| **Model Comparison Bar Chart** | Accuracy, F1, AUC side-by-side |
| **Cross-Validation Box Plot** | Score distributions per model |
| **Learning Curves** | Train vs validation score for best model |

Save best model as `outputs/models/best_model.pkl`.

---

### Phase 6: SHAP Analysis

#### [NEW] [05_shap_analysis.ipynb](file:///Users/abhijeet.ist/Downloads/FemoraHealth/notebooks/05_shap_analysis.ipynb)

**Outputs:**
1. **SHAP Summary Plot** (beeswarm) — global feature importance
2. **SHAP Bar Plot** — mean absolute SHAP values
3. **SHAP Waterfall Plot** — single prediction explanation
4. **SHAP Dependence Plots** — top 3 features vs SHAP value
5. **SHAP Force Plot** — individual prediction visualization

---

### Phase 7: Reports

#### Outputs generated across notebooks:

| Report | Location |
|---|---|
| Dataset Validation Report | `outputs/reports/dataset_validation_report.txt` |
| Feature Selection Summary | `outputs/reports/feature_selection_summary.txt` |
| Model Comparison Report | `outputs/reports/model_comparison_report.txt` |
| Final Validation Report | `outputs/reports/final_validation_report.txt` |

---

## Verification Plan

### Automated Checks

Each notebook will be verified by running it end-to-end with:

```bash
cd /Users/abhijeet.ist/Downloads/FemoraHealth
source venv/bin/activate
jupyter nbconvert --to notebook --execute notebooks/01_data_loading_preprocessing.ipynb
jupyter nbconvert --to notebook --execute notebooks/02_eda_visualization.ipynb
jupyter nbconvert --to notebook --execute notebooks/03_feature_engineering_selection.ipynb
jupyter nbconvert --to notebook --execute notebooks/04_model_building_evaluation.ipynb
jupyter nbconvert --to notebook --execute notebooks/05_shap_analysis.ipynb
```

**Success criteria:**
- All notebooks execute without errors
- `data/PCOS_cleaned.csv` is generated with 541 rows and no nulls
- `outputs/figures/` contains 20+ visualization files
- `outputs/models/best_model.pkl` exists and is loadable
- `outputs/reports/` contains all 4 report files

### Manual Verification

1. **Open each notebook** in Jupyter and visually inspect all plots render correctly
2. **Check the cleaned dataset** — no missing values, correct dtypes, expected shape
3. **Review model metrics** — accuracy, F1, AUC are reasonable (expect >80% for best model given domain)
4. **SHAP plots render** — waterfall, beeswarm display correctly
