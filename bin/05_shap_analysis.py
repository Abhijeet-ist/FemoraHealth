# %% [markdown]
# # 5. SHAP Analysis & Final Validation
# **INT 374 — Data Science Toolbox: Python Programming**  
# **Project: PCOS Prediction**

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import shap
import joblib
import warnings, os

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'figure.dpi': 150, 'font.size': 12})
os.makedirs('../outputs/figures', exist_ok=True)
os.makedirs('../outputs/reports', exist_ok=True)

# %% [markdown]
# ## 5.1 Load Model & Data

# %%
df = pd.read_csv('../data/PCOS_final.csv')
target = 'PCOS'
X = df.drop(columns=[target])
y = df[target]

# Load saved artifacts
model = joblib.load('../outputs/models/best_model.pkl')
scaler = joblib.load('../outputs/models/scaler.pkl')
feature_names = joblib.load('../outputs/models/feature_names.pkl')

X_scaled = pd.DataFrame(scaler.transform(X), columns=feature_names)
print(f"✅ Loaded model: {type(model).__name__}")
print(f"   Features: {len(feature_names)}")

# %% [markdown]
# ## 5.2 SHAP Explainer Setup

# %%
# Use TreeExplainer if tree-based, otherwise KernelExplainer
model_type = type(model).__name__
print(f"🔍 Model type: {model_type}")

if model_type in ['RandomForestClassifier', 'XGBClassifier', 'DecisionTreeClassifier']:
    explainer = shap.TreeExplainer(model)
    shap_values_raw = explainer.shap_values(X_scaled)
    
    # Handle different SHAP output formats
    if isinstance(shap_values_raw, list):
        # Old-style: list of [class0_array, class1_array]
        shap_values_plot = shap_values_raw[1]  # PCOS positive class
    elif isinstance(shap_values_raw, np.ndarray) and shap_values_raw.ndim == 3:
        # New-style: 3D array (samples, features, classes)
        shap_values_plot = shap_values_raw[:, :, 1]  # PCOS positive class
    else:
        shap_values_plot = shap_values_raw
        
    # Get base value for positive class
    base_value = explainer.expected_value
    if isinstance(base_value, (list, np.ndarray)):
        base_value = base_value[1] if len(base_value) > 1 else base_value[0]
else:
    # Use a sample for KernelExplainer (computationally expensive)
    background = shap.sample(X_scaled, 100)
    explainer = shap.KernelExplainer(model.predict_proba, background)
    shap_values_raw = explainer.shap_values(X_scaled.iloc[:100])
    if isinstance(shap_values_raw, list):
        shap_values_plot = shap_values_raw[1]
    elif isinstance(shap_values_raw, np.ndarray) and shap_values_raw.ndim == 3:
        shap_values_plot = shap_values_raw[:, :, 1]
    else:
        shap_values_plot = shap_values_raw
    X_scaled = X_scaled.iloc[:100]
    
    base_value = explainer.expected_value
    if isinstance(base_value, (list, np.ndarray)):
        base_value = base_value[1] if len(base_value) > 1 else base_value[0]

print(f"✅ SHAP values computed: {np.array(shap_values_plot).shape}")
print(f"   Base value: {base_value:.4f}")

# %% [markdown]
# ## 5.3 SHAP Summary Plot (Beeswarm)

# %%
fig, ax = plt.subplots(figsize=(14, 10))
shap.summary_plot(shap_values_plot, X_scaled, feature_names=feature_names, 
                  show=False, max_display=20)
plt.title('Figure 27: SHAP Summary Plot — Feature Importance (Beeswarm)', 
          fontsize=15, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('../outputs/figures/34_shap_summary.png', dpi=200, bbox_inches='tight')
plt.show()
print("💾 Saved: 34_shap_summary.png")

# %% [markdown]
# ## 5.4 SHAP Bar Plot — Mean |SHAP|

# %%
fig, ax = plt.subplots(figsize=(14, 10))
shap.summary_plot(shap_values_plot, X_scaled, feature_names=feature_names,
                  plot_type='bar', show=False, max_display=20)
plt.title('Figure 28: SHAP Feature Importance (Bar Plot)', 
          fontsize=15, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('../outputs/figures/35_shap_bar.png', dpi=200, bbox_inches='tight')
plt.show()
print("💾 Saved: 35_shap_bar.png")

# %% [markdown]
# ## 5.5 SHAP Waterfall Plot — Single Prediction

# %%
# Explain a single PCOS-positive prediction
pcos_indices = y[y == 1].index.tolist()
sample_idx = pcos_indices[0]  # First PCOS patient
pos = sample_idx if sample_idx < len(shap_values_plot) else 0

explanation = shap.Explanation(
    values=shap_values_plot[pos],
    base_values=base_value,
    data=X_scaled.iloc[pos].values,
    feature_names=feature_names
)

fig, ax = plt.subplots(figsize=(14, 10))
shap.plots.waterfall(explanation, show=False, max_display=15)
plt.title(f'Figure 29: SHAP Waterfall — Sample #{sample_idx} (PCOS Positive)',
          fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('../outputs/figures/36_shap_waterfall.png', dpi=200, bbox_inches='tight')
plt.show()
print("💾 Saved: 36_shap_waterfall.png")

# %% [markdown]
# ## 5.6 SHAP Dependence Plots — Top 3 Features

# %%
# Get top 3 features by mean |SHAP|
mean_abs_shap = np.abs(shap_values_plot).mean(axis=0)
top3_indices = np.argsort(mean_abs_shap)[-3:][::-1]
top3_features = [feature_names[i] for i in top3_indices]

fig, axes = plt.subplots(1, 3, figsize=(22, 6))
for idx, feat in enumerate(top3_features):
    shap.dependence_plot(feat, shap_values_plot, X_scaled, feature_names=feature_names,
                         ax=axes[idx], show=False)
    axes[idx].set_title(f'SHAP Dependence: {feat}', fontsize=12, fontweight='bold')

plt.suptitle('Figure 30: SHAP Dependence Plots — Top 3 Features', 
             fontsize=17, fontweight='bold', y=1.03)
plt.tight_layout()
plt.savefig('../outputs/figures/37_shap_dependence.png', dpi=200, bbox_inches='tight')
plt.show()
print("💾 Saved: 37_shap_dependence.png")

# %% [markdown]
# ## 5.7 SHAP Force Plot — Individual Prediction

# %%
# Force plot for a single sample (save as HTML-free version)
fig, ax = plt.subplots(figsize=(20, 4))
shap.force_plot(base_value, shap_values_plot[pos], X_scaled.iloc[pos],
                feature_names=feature_names, matplotlib=True, show=False)
plt.title(f'Figure 31: SHAP Force Plot — Sample #{sample_idx}', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('../outputs/figures/38_shap_force.png', dpi=200, bbox_inches='tight')
plt.show()
print("💾 Saved: 38_shap_force.png")

# %% [markdown]
# ---
# ## 5.8 Final Validation Report

# %%
# Load model comparison
model_report = open('../outputs/reports/model_comparison_report.txt').read()

# Generate final report
final_report = []
final_report.append("=" * 70)
final_report.append("  PCOS PREDICTION — FINAL VALIDATION REPORT")
final_report.append("=" * 70)
final_report.append(f"\nGenerated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

final_report.append(f"\n\n{'='*50}")
final_report.append("  DATASET SUMMARY")
final_report.append(f"{'='*50}")
final_report.append(f"Total samples: {len(df)}")
final_report.append(f"Features used: {len(feature_names)}")
final_report.append(f"Target: PCOS (0={sum(y==0)}, 1={sum(y==1)})")
final_report.append(f"Positive rate: {y.mean()*100:.1f}%")

final_report.append(f"\n\n{'='*50}")
final_report.append("  MODEL PERFORMANCE")
final_report.append(f"{'='*50}")
final_report.append(model_report)

final_report.append(f"\n\n{'='*50}")
final_report.append("  SHAP ANALYSIS — TOP FEATURES")
final_report.append(f"{'='*50}")
shap_importance = pd.DataFrame({
    'Feature': feature_names,
    'Mean_SHAP': mean_abs_shap
}).sort_values('Mean_SHAP', ascending=False)

for i, row in shap_importance.head(15).iterrows():
    final_report.append(f"  {row['Feature']:<30} SHAP: {row['Mean_SHAP']:.4f}")

final_report.append(f"\n\n{'='*50}")
final_report.append("  ARTIFACTS GENERATED")
final_report.append(f"{'='*50}")
fig_count = len([f for f in os.listdir('../outputs/figures') if f.endswith('.png')])
final_report.append(f"Figures: {fig_count} (outputs/figures/)")
final_report.append(f"Models: best_model.pkl, scaler.pkl, feature_names.pkl")
final_report.append(f"Reports: dataset_validation_report.txt, feature_selection_summary.txt,")
final_report.append(f"         model_comparison_report.txt, statistical_tests.csv")
final_report.append(f"         final_validation_report.txt")

final_report.append(f"\n\n{'='*50}")
final_report.append("  CONCLUSION")
final_report.append(f"{'='*50}")
final_report.append(f"Best model: {type(model).__name__}")
final_report.append(f"Key predictors (by SHAP): {top3_features}")
final_report.append(f"Ready for Streamlit deployment ✅")

report_text = '\n'.join(final_report)
with open('../outputs/reports/final_validation_report.txt', 'w') as f:
    f.write(report_text)

print(report_text)
print("\n💾 Saved: outputs/reports/final_validation_report.txt")

# %%
print("\n" + "=" * 70)
print("  ✅ SHAP ANALYSIS & FINAL VALIDATION — COMPLETE")
print("=" * 70)
print(f"  • Generated SHAP plots: summary, bar, waterfall, dependence, force")
print(f"  • Best model: {type(model).__name__}")
print(f"  • Top predictors: {top3_features}")
print(f"  • All artifacts saved to outputs/")
