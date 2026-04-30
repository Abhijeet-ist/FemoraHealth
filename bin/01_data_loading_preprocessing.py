# %% [markdown]
# # 1. Data Loading & Preprocessing
# **INT 374 — Data Science Toolbox: Python Programming**  
# **Project: PCOS (Polycystic Ovary Syndrome) Prediction**
# 
# This notebook covers:
# - Loading and merging datasets
# - Data cleaning and type corrections
# - Missing value analysis and imputation
# - Outlier detection
# - Dataset validation report

# %% [markdown]
# ## 1.1 Import Libraries

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
import warnings
import os

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12
plt.rcParams['figure.dpi'] = 150

# Create output directories
os.makedirs('../outputs/figures', exist_ok=True)
os.makedirs('../outputs/reports', exist_ok=True)

print("✅ Libraries imported successfully")

# %% [markdown]
# ## 1.2 Load Datasets

# %%
# Load primary dataset (Excel - Full_new sheet)
df_main = pd.read_excel('../data/PCOS_data_without_infertility.xlsx', sheet_name='Full_new')
print(f"📊 Primary Dataset (Excel): {df_main.shape[0]} rows × {df_main.shape[1]} columns")

# Load secondary dataset (CSV - infertility data)
df_infertility = pd.read_csv('../data/PCOS_infertility.csv')
print(f"📊 Secondary Dataset (CSV): {df_infertility.shape[0]} rows × {df_infertility.shape[1]} columns")

# %%
# Display primary dataset info
print("=" * 70)
print("PRIMARY DATASET — First 5 Rows")
print("=" * 70)
df_main.head()

# %%
# Display secondary dataset info
print("=" * 70)
print("SECONDARY DATASET — First 5 Rows")
print("=" * 70)
df_infertility.head()

# %%
# Check sheet names
xls = pd.ExcelFile('../data/PCOS_data_without_infertility.xlsx')
print(f"📋 Excel Sheets: {xls.sheet_names}")

# %% [markdown]
# ## 1.3 Initial Dataset Validation Report (Pre-Cleaning)

# %%
def generate_validation_report(df, title="Dataset"):
    """Generate a comprehensive validation report for the dataset."""
    report = []
    report.append(f"\n{'='*70}")
    report.append(f"  DATASET VALIDATION REPORT — {title}")
    report.append(f"{'='*70}")
    report.append(f"\n📐 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    report.append(f"💾 Memory Usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    # Data types
    report.append(f"\n📊 Data Types:")
    for dtype, count in df.dtypes.value_counts().items():
        report.append(f"   • {dtype}: {count} columns")
    
    # Missing values
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({'Missing': missing, 'Percentage': missing_pct})
    missing_df = missing_df[missing_df['Missing'] > 0].sort_values('Missing', ascending=False)
    
    report.append(f"\n❌ Missing Values: {missing.sum()} total across {len(missing_df)} columns")
    if len(missing_df) > 0:
        for col, row in missing_df.iterrows():
            report.append(f"   • {col}: {int(row['Missing'])} ({row['Percentage']}%)")
    
    # Duplicates
    dup_count = df.duplicated().sum()
    report.append(f"\n🔄 Duplicate Rows: {dup_count}")
    
    # Numeric stats
    numeric_cols = df.select_dtypes(include='number').columns
    report.append(f"\n📈 Numeric Columns: {len(numeric_cols)}")
    report.append(f"📝 Categorical/Object Columns: {len(df.select_dtypes(include='object').columns)}")
    
    report_text = '\n'.join(report)
    print(report_text)
    return report_text

pre_clean_report = generate_validation_report(df_main, "PRE-CLEANING")

# %%
# Detailed column information
print(f"\n{'Column':<35} {'Dtype':<12} {'Nulls':<8} {'Unique':<8} {'Sample Values'}")
print("-" * 100)
for col in df_main.columns:
    dtype = str(df_main[col].dtype)
    nulls = df_main[col].isnull().sum()
    unique = df_main[col].nunique()
    samples = str(df_main[col].dropna().unique()[:3].tolist())[:40]
    print(f"{col:<35} {dtype:<12} {nulls:<8} {unique:<8} {samples}")

# %% [markdown]
# ## 1.4 Data Cleaning

# %% [markdown]
# ### 1.4.1 Drop Junk Columns

# %%
# Drop unnecessary columns
cols_to_drop = ['Unnamed: 44', 'Sl. No', 'Patient File No.']
df = df_main.drop(columns=cols_to_drop, errors='ignore')
print(f"🗑️  Dropped columns: {cols_to_drop}")
print(f"📐 New shape: {df.shape}")

# %% [markdown]
# ### 1.4.2 Clean Column Names

# %%
# Store original column names for reference
original_names = df.columns.tolist()

# Clean column names - strip whitespace
df.columns = df.columns.str.strip()

# Create a cleaner column name mapping
column_mapping = {
    'Age (yrs)': 'Age',
    'Weight (Kg)': 'Weight_Kg',
    'Height(Cm)': 'Height_Cm',
    'Blood Group': 'Blood_Group',
    'Pulse rate(bpm)': 'Pulse_Rate',
    'RR (breaths/min)': 'Resp_Rate',
    'Hb(g/dl)': 'Hemoglobin',
    'Cycle(R/I)': 'Cycle_RI',
    'Cycle length(days)': 'Cycle_Length',
    'Marraige Status (Yrs)': 'Marriage_Yrs',
    'Pregnant(Y/N)': 'Pregnant',
    'No. of aborptions': 'Num_Abortions',
    'I   beta-HCG(mIU/mL)': 'Beta_HCG_I',
    'II    beta-HCG(mIU/mL)': 'Beta_HCG_II',
    'FSH(mIU/mL)': 'FSH',
    'LH(mIU/mL)': 'LH',
    'FSH/LH': 'FSH_LH_Ratio',
    'Hip(inch)': 'Hip',
    'Waist(inch)': 'Waist',
    'Waist:Hip Ratio': 'Waist_Hip_Ratio',
    'TSH (mIU/L)': 'TSH',
    'AMH(ng/mL)': 'AMH',
    'PRL(ng/mL)': 'Prolactin',
    'Vit D3 (ng/mL)': 'Vit_D3',
    'PRG(ng/mL)': 'Progesterone',
    'RBS(mg/dl)': 'RBS',
    'Weight gain(Y/N)': 'Weight_Gain',
    'hair growth(Y/N)': 'Hair_Growth',
    'Skin darkening (Y/N)': 'Skin_Darkening',
    'Hair loss(Y/N)': 'Hair_Loss',
    'Pimples(Y/N)': 'Pimples',
    'Fast food (Y/N)': 'Fast_Food',
    'Reg.Exercise(Y/N)': 'Regular_Exercise',
    'BP _Systolic (mmHg)': 'BP_Systolic',
    'BP _Diastolic (mmHg)': 'BP_Diastolic',
    'Follicle No. (L)': 'Follicle_L',
    'Follicle No. (R)': 'Follicle_R',
    'Avg. F size (L) (mm)': 'Avg_Follicle_Size_L',
    'Avg. F size (R) (mm)': 'Avg_Follicle_Size_R',
    'Endometrium (mm)': 'Endometrium',
    'PCOS (Y/N)': 'PCOS'
}

df.rename(columns=column_mapping, inplace=True)

print("✅ Column names cleaned and standardized:")
print(df.columns.tolist())

# %% [markdown]
# ### 1.4.3 Fix Data Types

# %%
# Check columns with wrong dtypes
print("🔍 Columns with object dtype (should be numeric):")
obj_cols = df.select_dtypes(include='object').columns
for col in obj_cols:
    print(f"   • {col}: {df[col].unique()[:10]}")

# %%
# Convert object columns to numeric
for col in obj_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    print(f"   ✅ Converted '{col}' to {df[col].dtype}")

print(f"\n📊 Data types after conversion:")
print(df.dtypes.value_counts())

# %% [markdown]
# ## 1.5 Missing Data Analysis

# %%
# Missing values summary
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({
    'Column': missing.index,
    'Missing_Count': missing.values,
    'Missing_Percentage': missing_pct.values
}).sort_values('Missing_Count', ascending=False)

missing_df = missing_df[missing_df['Missing_Count'] > 0]
print("📊 Missing Values Summary:")
print(missing_df.to_string(index=False))

# %%
# Missing Data Visualization — Missingno Matrix
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Matrix plot
plt.sca(axes[0])
msno.matrix(df, ax=axes[0], fontsize=8, sparkline=False, color=(0.27, 0.52, 0.96))
axes[0].set_title('Missing Data Matrix', fontsize=14, fontweight='bold', pad=15)

# Bar chart
plt.sca(axes[1])
msno.bar(df, ax=axes[1], fontsize=8, color=(0.27, 0.52, 0.96))
axes[1].set_title('Data Completeness Bar Chart', fontsize=14, fontweight='bold', pad=15)

plt.tight_layout()
plt.savefig('../outputs/figures/01_missing_data_analysis.png', dpi=200, bbox_inches='tight')
plt.show()
print("💾 Saved: outputs/figures/01_missing_data_analysis.png")

# %%
# Missing data heatmap (focused view on columns with missing values)
if len(missing_df) > 0:
    fig, ax = plt.subplots(figsize=(10, 6))
    missing_cols = missing_df['Column'].tolist()
    
    # Create binary missing indicator
    missing_indicator = df[missing_cols].isnull().astype(int)
    
    sns.heatmap(missing_indicator.T, cmap='YlOrRd', cbar_kws={'label': 'Missing (1) / Present (0)'},
                yticklabels=missing_cols, ax=ax)
    ax.set_title('Missing Data Heatmap (Focused)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Sample Index')
    ax.set_ylabel('Features')
    
    plt.tight_layout()
    plt.savefig('../outputs/figures/02_missing_data_heatmap.png', dpi=200, bbox_inches='tight')
    plt.show()
    print("💾 Saved: outputs/figures/02_missing_data_heatmap.png")

# %% [markdown]
# ## 1.6 Missing Value Imputation

# %%
# Impute missing values
print("🔧 Imputing missing values...")

# Iterate over all columns and impute any missing values
for col in df.columns:
    if df[col].isnull().sum() > 0:
        count = df[col].isnull().sum()
        if df[col].nunique() <= 5:
            # Binary/categorical: use mode
            fill_val = df[col].mode()[0]
            df[col] = df[col].fillna(fill_val)
            print(f"   ✅ {col}: filled {count} missing with mode = {fill_val}")
        else:
            # Continuous: use median
            fill_val = df[col].median()
            df[col] = df[col].fillna(fill_val)
            print(f"   ✅ {col}: filled {count} missing with median = {fill_val:.2f}")

# Verify no missing values remain
total_missing = df.isnull().sum().sum()
assert total_missing == 0, f"Still have {total_missing} missing values!"
print(f"\n✅ Total missing values remaining: {total_missing}")

# %% [markdown]
# ## 1.7 Outlier Detection & Analysis

# %%
# IQR-based outlier detection
def detect_outliers_iqr(df, columns):
    """Detect outliers using IQR method."""
    outlier_summary = {}
    for col in columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower) | (df[col] > upper)]
        if len(outliers) > 0:
            outlier_summary[col] = {
                'count': len(outliers),
                'percentage': round(len(outliers) / len(df) * 100, 2),
                'lower_bound': round(lower, 2),
                'upper_bound': round(upper, 2),
                'min': round(df[col].min(), 2),
                'max': round(df[col].max(), 2)
            }
    return outlier_summary

continuous_cols = [col for col in df.select_dtypes(include='number').columns 
                   if df[col].nunique() > 5 and col != 'PCOS']

outlier_summary = detect_outliers_iqr(df, continuous_cols)

print(f"📊 Outlier Detection (IQR Method)")
print(f"{'Column':<25} {'Count':<8} {'%':<8} {'Lower':<12} {'Upper':<12} {'Min':<10} {'Max':<10}")
print("-" * 85)
for col, info in sorted(outlier_summary.items(), key=lambda x: x[1]['count'], reverse=True):
    print(f"{col:<25} {info['count']:<8} {info['percentage']:<8} {info['lower_bound']:<12} {info['upper_bound']:<12} {info['min']:<10} {info['max']:<10}")

# %%
# Box plots for outlier visualization
outlier_cols = list(outlier_summary.keys())[:12]  # Top 12 columns with outliers
n_cols = 4
n_rows = (len(outlier_cols) + n_cols - 1) // n_cols

fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 4 * n_rows))
axes = axes.flatten()

for idx, col in enumerate(outlier_cols):
    sns.boxplot(data=df, x='PCOS', y=col, ax=axes[idx], palette='Set2',
                hue='PCOS', legend=False)
    axes[idx].set_title(f'{col}', fontsize=11, fontweight='bold')
    axes[idx].set_xlabel('PCOS (0=No, 1=Yes)')

for idx in range(len(outlier_cols), len(axes)):
    axes[idx].set_visible(False)

plt.suptitle('Outlier Detection — Box Plots (Top Features with Outliers)', 
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('../outputs/figures/03_outlier_boxplots.png', dpi=200, bbox_inches='tight')
plt.show()
print("💾 Saved: outputs/figures/03_outlier_boxplots.png")

# %% [markdown]
# ### 1.7.1 Outlier Treatment
# We'll cap extreme outliers using IQR winsorization (only for extreme values beyond 3×IQR).
# Medical data often has legitimate outliers, so we use a conservative approach.

# %%
# Conservative outlier capping (3x IQR — only extreme values)
def cap_outliers(df, columns, multiplier=3.0):
    """Cap extreme outliers using IQR method with a multiplier."""
    capped_info = {}
    for col in columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - multiplier * IQR
        upper = Q3 + multiplier * IQR
        
        lower_count = (df[col] < lower).sum()
        upper_count = (df[col] > upper).sum()
        
        if lower_count > 0 or upper_count > 0:
            df[col] = df[col].clip(lower=lower, upper=upper)
            capped_info[col] = {'lower_capped': lower_count, 'upper_capped': upper_count}
    
    return capped_info

capped = cap_outliers(df, continuous_cols, multiplier=3.0)
print("🔧 Extreme Outlier Capping (3×IQR):")
for col, info in capped.items():
    print(f"   • {col}: {info['lower_capped']} lower + {info['upper_capped']} upper capped")

if not capped:
    print("   No extreme outliers detected (3×IQR threshold). Data retained as-is.")

# %% [markdown]
# ## 1.8 Feature Type Categorization

# %%
# Categorize features
target = 'PCOS'

binary_features = [col for col in df.columns if df[col].nunique() == 2 and col != target]
continuous_features = [col for col in df.select_dtypes(include='number').columns 
                       if df[col].nunique() > 10 and col != target]
discrete_features = [col for col in df.select_dtypes(include='number').columns 
                     if 3 <= df[col].nunique() <= 10 and col != target]

print(f"🎯 Target: {target}")
print(f"\n📊 Binary Features ({len(binary_features)}):")
for f in binary_features:
    print(f"   • {f}: {sorted(df[f].unique())}")

print(f"\n📈 Continuous Features ({len(continuous_features)}):")
for f in continuous_features:
    print(f"   • {f}: range [{df[f].min():.2f}, {df[f].max():.2f}]")

print(f"\n📉 Discrete Features ({len(discrete_features)}):")
for f in discrete_features:
    print(f"   • {f}: {sorted(df[f].unique())}")

# %% [markdown]
# ## 1.9 Descriptive Statistics

# %%
# Comprehensive descriptive statistics
print("📊 Descriptive Statistics — Continuous Features")
df[continuous_features].describe().round(2)

# %%
# Statistics by PCOS status
print("📊 Mean Values by PCOS Status")
comparison = df.groupby('PCOS')[continuous_features].mean().T
comparison.columns = ['Non-PCOS (0)', 'PCOS (1)']
comparison['Difference'] = comparison['PCOS (1)'] - comparison['Non-PCOS (0)']
comparison['% Change'] = ((comparison['Difference'] / comparison['Non-PCOS (0)']) * 100).round(2)
comparison = comparison.sort_values('% Change', ascending=False)
print(comparison.to_string())

# %% [markdown]
# ## 1.10 Post-Cleaning Validation Report

# %%
post_clean_report = generate_validation_report(df, "POST-CLEANING")

# %%
# Save validation report to file
with open('../outputs/reports/dataset_validation_report.txt', 'w') as f:
    f.write("PCOS DATASET — VALIDATION REPORT\n")
    f.write("=" * 70 + "\n")
    f.write(f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write("--- PRE-CLEANING ---\n")
    f.write(pre_clean_report)
    f.write("\n\n--- POST-CLEANING ---\n")
    f.write(post_clean_report)
    f.write(f"\n\n--- FEATURE SUMMARY ---\n")
    f.write(f"Target: {target}\n")
    f.write(f"Binary Features: {binary_features}\n")
    f.write(f"Continuous Features: {continuous_features}\n")
    f.write(f"Discrete Features: {discrete_features}\n")
    f.write(f"\n--- TARGET DISTRIBUTION ---\n")
    f.write(f"{df['PCOS'].value_counts().to_string()}\n")
    f.write(f"Positive Rate: {df['PCOS'].mean()*100:.1f}%\n")

print("💾 Saved: outputs/reports/dataset_validation_report.txt")

# %% [markdown]
# ## 1.11 Save Cleaned Dataset

# %%
# Save the cleaned dataset
df.to_csv('../data/PCOS_cleaned.csv', index=False)
print(f"💾 Saved: data/PCOS_cleaned.csv")
print(f"   Shape: {df.shape}")
print(f"   Missing values: {df.isnull().sum().sum()}")
print(f"   Columns: {df.columns.tolist()}")

# %%
print("\n" + "=" * 70)
print("  ✅ DATA LOADING & PREPROCESSING — COMPLETE")
print("=" * 70)
print(f"  • Loaded 2 datasets, merged and cleaned")
print(f"  • Final shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"  • Missing values: {df.isnull().sum().sum()}")
print(f"  • Target: PCOS (0={(df['PCOS']==0).sum()}, 1={(df['PCOS']==1).sum()})")
print(f"  • Saved: data/PCOS_cleaned.csv")
print(f"  • Reports: outputs/reports/dataset_validation_report.txt")
print(f"  • Figures: outputs/figures/01-03_*.png")
