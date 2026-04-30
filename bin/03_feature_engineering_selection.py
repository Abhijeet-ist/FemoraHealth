# %% [markdown]
# # 3. Feature Engineering & Selection
# **INT 374 — Data Science Toolbox: Python Programming**  
# **Project: PCOS Prediction**

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.feature_selection import mutual_info_classif, chi2, SelectKBest, f_classif
from sklearn.preprocessing import StandardScaler
import warnings, os

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'figure.dpi': 150, 'font.size': 12})
os.makedirs('../outputs/figures', exist_ok=True)
os.makedirs('../outputs/reports', exist_ok=True)

df = pd.read_csv('../data/PCOS_cleaned.csv')
target = 'PCOS'
print(f"✅ Loaded: {df.shape}")

# %% [markdown]
# ## 3.1 Feature Engineering — Create New Features

# %%
# Create meaningful derived features
df['Total_Follicles'] = df['Follicle_L'] + df['Follicle_R']
df['Avg_Follicle_Size'] = (df['Avg_Follicle_Size_L'] + df['Avg_Follicle_Size_R']) / 2
df['LH_FSH_Ratio'] = df['LH'] / (df['FSH'] + 0.001)  # avoid division by zero
df['Beta_HCG_Avg'] = (df['Beta_HCG_I'] + df['Beta_HCG_II']) / 2
df['BP_Mean'] = (df['BP_Systolic'] + df['BP_Diastolic']) / 2
df['Symptom_Score'] = df[['Weight_Gain', 'Hair_Growth', 'Skin_Darkening', 'Hair_Loss', 'Pimples']].sum(axis=1)

new_features = ['Total_Follicles', 'Avg_Follicle_Size', 'LH_FSH_Ratio', 'Beta_HCG_Avg', 'BP_Mean', 'Symptom_Score']
print(f"✅ Created {len(new_features)} new features: {new_features}")
print(f"   New shape: {df.shape}")

# %% [markdown]
# ## 3.2 Correlation-Based Feature Elimination

# %%
# Remove highly correlated feature pairs (>0.9)
corr_matrix = df.drop(columns=[target]).corr().abs()
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

high_corr_pairs = []
to_drop = set()
for col in upper.columns:
    for idx in upper.index:
        if upper.loc[idx, col] > 0.9:
            high_corr_pairs.append((idx, col, upper.loc[idx, col]))
            # Drop the one with lower correlation to target
            corr_target_idx = abs(df[idx].corr(df[target]))
            corr_target_col = abs(df[col].corr(df[target]))
            drop_col = idx if corr_target_idx < corr_target_col else col
            to_drop.add(drop_col)

print("📊 Highly Correlated Feature Pairs (>0.9):")
for f1, f2, c in high_corr_pairs:
    print(f"   {f1} ↔ {f2}: {c:.3f}")
print(f"\n🗑️  Features to drop: {to_drop}")

df_selected = df.drop(columns=list(to_drop))
print(f"📐 Shape after elimination: {df_selected.shape}")

# %% [markdown]
# ## 3.3 Statistical Tests — ANOVA F-test (Continuous Features)

# %%
X = df_selected.drop(columns=[target])
y = df_selected[target]

continuous = [c for c in X.columns if X[c].nunique() > 5]

# ANOVA F-test
X_cont = X[continuous].fillna(0)
f_scores, f_pvalues = f_classif(X_cont, y)

anova_df = pd.DataFrame({
    'Feature': continuous,
    'F-Score': f_scores,
    'p-value': f_pvalues
}).sort_values('F-Score', ascending=False)
anova_df['Significant'] = anova_df['p-value'] < 0.05

fig, ax = plt.subplots(figsize=(14, 8))
colors = ['#2ECC71' if s else '#E74C3C' for s in anova_df['Significant']]
ax.barh(anova_df['Feature'], anova_df['F-Score'], color=colors, edgecolor='white')
ax.set_title('Feature Selection: ANOVA F-Scores (Green=Significant)', fontsize=15, fontweight='bold')
ax.set_xlabel('F-Score')
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig('../outputs/figures/24_anova_fscores.png', dpi=200, bbox_inches='tight')
plt.show()
print("💾 Saved: 24_anova_fscores.png")

# %% [markdown]
# ## 3.4 Chi-Square Test (Binary Features)

# %%
binary = [c for c in X.columns if X[c].nunique() <= 5]
X_bin = X[binary].fillna(0)

chi_scores, chi_pvalues = chi2(X_bin, y)

chi_df = pd.DataFrame({
    'Feature': binary,
    'Chi2-Score': chi_scores,
    'p-value': chi_pvalues
}).sort_values('Chi2-Score', ascending=False)
chi_df['Significant'] = chi_df['p-value'] < 0.05

fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#2ECC71' if s else '#E74C3C' for s in chi_df['Significant']]
ax.barh(chi_df['Feature'], chi_df['Chi2-Score'], color=colors, edgecolor='white')
ax.set_title('Feature Selection: Chi-Square Scores (Binary Features)', fontsize=15, fontweight='bold')
ax.set_xlabel('Chi² Score')
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig('../outputs/figures/25_chi2_scores.png', dpi=200, bbox_inches='tight')
plt.show()
print("💾 Saved: 25_chi2_scores.png")

# %% [markdown]
# ## 3.5 Mutual Information Scores

# %%
X_all = X.fillna(0)
mi_scores = mutual_info_classif(X_all, y, random_state=42)
mi_df = pd.DataFrame({
    'Feature': X.columns,
    'MI_Score': mi_scores
}).sort_values('MI_Score', ascending=False)

fig, ax = plt.subplots(figsize=(14, 10))
colors = sns.color_palette('viridis', len(mi_df))
ax.barh(mi_df['Feature'], mi_df['MI_Score'], color=colors, edgecolor='white')
ax.set_title('Feature Selection: Mutual Information Scores', fontsize=15, fontweight='bold')
ax.set_xlabel('Mutual Information Score')
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig('../outputs/figures/26_mutual_info.png', dpi=200, bbox_inches='tight')
plt.show()
print("💾 Saved: 26_mutual_info.png")

# %% [markdown]
# ## 3.6 Combined Feature Ranking

# %%
# Normalize each score to 0-1 and combine
from sklearn.preprocessing import MinMaxScaler

all_features = X.columns.tolist()
scores_combined = pd.DataFrame({'Feature': all_features})

# Correlation with target
corr_scores = X.corrwith(y).abs()
scores_combined['Correlation'] = MinMaxScaler().fit_transform(corr_scores.values.reshape(-1, 1))

# Mutual Information
mi_dict = dict(zip(mi_df['Feature'], mi_df['MI_Score']))
scores_combined['MI'] = MinMaxScaler().fit_transform(
    np.array([mi_dict.get(f, 0) for f in all_features]).reshape(-1, 1))

# ANOVA (for continuous features)
anova_dict = dict(zip(anova_df['Feature'], anova_df['F-Score']))
f_vals = np.array([anova_dict.get(f, 0) for f in all_features]).reshape(-1, 1)
scores_combined['ANOVA'] = MinMaxScaler().fit_transform(f_vals)

# Average rank
scores_combined['Avg_Score'] = scores_combined[['Correlation', 'MI', 'ANOVA']].mean(axis=1)
scores_combined = scores_combined.sort_values('Avg_Score', ascending=False)

print("📊 Combined Feature Ranking (Top 20):")
print(scores_combined.head(20).to_string(index=False))

# Select top features (above average score)
threshold = scores_combined['Avg_Score'].quantile(0.25)
selected_features = scores_combined[scores_combined['Avg_Score'] >= threshold]['Feature'].tolist()
print(f"\n✅ Selected {len(selected_features)} features (above 25th percentile)")

# %%
# Visualize combined ranking
fig, ax = plt.subplots(figsize=(14, 12))
top20 = scores_combined.head(20)

x = np.arange(len(top20))
width = 0.25

ax.barh(x - width, top20['Correlation'], width, label='Correlation', color='#3498DB')
ax.barh(x, top20['MI'], width, label='Mutual Information', color='#E74C3C')
ax.barh(x + width, top20['ANOVA'], width, label='ANOVA F-test', color='#2ECC71')

ax.set_yticks(x)
ax.set_yticklabels(top20['Feature'])
ax.set_title('Feature Ranking: Combined Scores (Top 20)', fontsize=15, fontweight='bold')
ax.set_xlabel('Normalized Score (0-1)')
ax.legend(fontsize=11)
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.savefig('../outputs/figures/27_combined_feature_ranking.png', dpi=200, bbox_inches='tight')
plt.show()
print("💾 Saved: 27_combined_feature_ranking.png")

# %% [markdown]
# ## 3.7 Save Final Feature Set

# %%
# Save processed data with selected features
df_final = df_selected[selected_features + [target]]
df_final.to_csv('../data/PCOS_final.csv', index=False)

# Save feature selection report
with open('../outputs/reports/feature_selection_summary.txt', 'w') as f:
    f.write("PCOS — FEATURE SELECTION SUMMARY\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Original features: {len(df.columns) - 1}\n")
    f.write(f"After correlation elimination: {len(df_selected.columns) - 1}\n")
    f.write(f"Final selected features: {len(selected_features)}\n\n")
    f.write("Selected features:\n")
    for i, feat in enumerate(selected_features, 1):
        score = scores_combined[scores_combined['Feature'] == feat]['Avg_Score'].values[0]
        f.write(f"  {i}. {feat} (score: {score:.3f})\n")
    f.write(f"\nDropped (high correlation): {list(to_drop)}\n")
    f.write(f"\nCombined ranking:\n{scores_combined.to_string(index=False)}\n")

print(f"💾 Saved: data/PCOS_final.csv ({df_final.shape})")
print(f"💾 Saved: outputs/reports/feature_selection_summary.txt")

print("\n" + "=" * 70)
print("  ✅ FEATURE ENGINEERING & SELECTION — COMPLETE")
print("=" * 70)
