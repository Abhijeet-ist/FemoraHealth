# %% [markdown]
# # 4. Model Building & Evaluation
# **INT 374 — Data Science Toolbox: Python Programming**  
# **Project: PCOS Prediction**

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, GridSearchCV, learning_curve
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                             roc_curve, auc, precision_recall_curve, f1_score,
                             precision_score, recall_score, roc_auc_score)
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
import joblib
import warnings, os

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'figure.dpi': 150, 'font.size': 12})
os.makedirs('../outputs/figures', exist_ok=True)
os.makedirs('../outputs/reports', exist_ok=True)
os.makedirs('../outputs/models', exist_ok=True)

PALETTE = ['#3498DB', '#E74C3C']

# %% [markdown]
# ## 4.1 Load & Prepare Data

# %%
df = pd.read_csv('../data/PCOS_final.csv')
target = 'PCOS'

X = df.drop(columns=[target])
y = df[target]

print(f"✅ Loaded: {df.shape}")
print(f"   Features: {X.shape[1]}, Samples: {X.shape[0]}")
print(f"   Target distribution:\n{y.value_counts()}")

# %%
# Train-Test Split (80/20, stratified)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"\n📊 Train: {X_train.shape[0]} samples | Test: {X_test.shape[0]} samples")
print(f"   Train target: {dict(y_train.value_counts())}")
print(f"   Test target:  {dict(y_test.value_counts())}")

# %%
# Feature Scaling
scaler = StandardScaler()
X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X.columns, index=X_train.index)
X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X.columns, index=X_test.index)
print("✅ Features scaled with StandardScaler")

# Save scaler for Streamlit
joblib.dump(scaler, '../outputs/models/scaler.pkl')
print("💾 Saved: outputs/models/scaler.pkl")

# %%
# Handle Class Imbalance with SMOTE
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train_scaled, y_train)
print(f"\n🔄 SMOTE Resampling:")
print(f"   Before: {dict(y_train.value_counts())}")
print(f"   After:  {dict(pd.Series(y_train_res).value_counts())}")

# %% [markdown]
# ## 4.2 Define & Train Models

# %%
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'SVM': SVC(kernel='rbf', probability=True, random_state=42),
    'KNN': KNeighborsClassifier(n_neighbors=5),
    'XGBoost': XGBClassifier(n_estimators=100, use_label_encoder=False, eval_metric='logloss',
                              random_state=42, verbosity=0)
}

results = {}
trained_models = {}

for name, model in models.items():
    print(f"\n{'='*50}")
    print(f"Training: {name}")
    print(f"{'='*50}")
    
    # Train
    model.fit(X_train_res, y_train_res)
    trained_models[name] = model
    
    # Predict
    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]
    
    # Metrics
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc_score = roc_auc_score(y_test, y_prob)
    
    results[name] = {
        'Accuracy': acc, 'Precision': prec, 'Recall': rec,
        'F1-Score': f1, 'AUC': auc_score,
        'y_pred': y_pred, 'y_prob': y_prob
    }
    
    print(f"   Accuracy:  {acc:.4f}")
    print(f"   Precision: {prec:.4f}")
    print(f"   Recall:    {rec:.4f}")
    print(f"   F1-Score:  {f1:.4f}")
    print(f"   AUC:       {auc_score:.4f}")

# %% [markdown]
# ## 4.3 Confusion Matrices

# %%
fig, axes = plt.subplots(2, 3, figsize=(20, 12))
axes = axes.flatten()

for idx, (name, res) in enumerate(results.items()):
    cm = confusion_matrix(y_test, res['y_pred'])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                xticklabels=['Non-PCOS', 'PCOS'], yticklabels=['Non-PCOS', 'PCOS'],
                linewidths=2, linecolor='white', annot_kws={'size': 16, 'fontweight': 'bold'})
    axes[idx].set_title(f'{name}\nAcc={res["Accuracy"]:.3f} | F1={res["F1-Score"]:.3f}',
                        fontsize=12, fontweight='bold')
    axes[idx].set_ylabel('Actual')
    axes[idx].set_xlabel('Predicted')

plt.suptitle('Figure 21: Confusion Matrices — All Models', fontsize=18, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('../outputs/figures/28_confusion_matrices.png', dpi=200, bbox_inches='tight')
plt.show()
print("💾 Saved: 28_confusion_matrices.png")

# %% [markdown]
# ## 4.4 ROC Curves

# %%
fig, ax = plt.subplots(figsize=(12, 8))
colors = sns.color_palette('husl', len(results))

for (name, res), color in zip(results.items(), colors):
    fpr, tpr, _ = roc_curve(y_test, res['y_prob'])
    ax.plot(fpr, tpr, color=color, linewidth=2.5, label=f"{name} (AUC={res['AUC']:.3f})")

ax.plot([0, 1], [0, 1], 'k--', linewidth=1, alpha=0.5, label='Random Baseline')
ax.fill_between([0, 1], [0, 1], alpha=0.05, color='gray')
ax.set_xlabel('False Positive Rate', fontsize=13)
ax.set_ylabel('True Positive Rate', fontsize=13)
ax.set_title('Figure 22: ROC Curves — Model Comparison', fontsize=16, fontweight='bold')
ax.legend(fontsize=11, loc='lower right')
ax.set_xlim([0, 1])
ax.set_ylim([0, 1.02])
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.savefig('../outputs/figures/29_roc_curves.png', dpi=200, bbox_inches='tight')
plt.show()
print("💾 Saved: 29_roc_curves.png")

# %% [markdown]
# ## 4.5 Precision-Recall Curves

# %%
fig, ax = plt.subplots(figsize=(12, 8))

for (name, res), color in zip(results.items(), colors):
    prec_vals, rec_vals, _ = precision_recall_curve(y_test, res['y_prob'])
    ax.plot(rec_vals, prec_vals, color=color, linewidth=2.5, label=f"{name}")

ax.set_xlabel('Recall', fontsize=13)
ax.set_ylabel('Precision', fontsize=13)
ax.set_title('Figure 23: Precision-Recall Curves', fontsize=16, fontweight='bold')
ax.legend(fontsize=11)
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.savefig('../outputs/figures/30_precision_recall_curves.png', dpi=200, bbox_inches='tight')
plt.show()
print("💾 Saved: 30_precision_recall_curves.png")

# %% [markdown]
# ## 4.6 Model Comparison Bar Chart

# %%
metrics_df = pd.DataFrame({
    name: {k: v for k, v in res.items() if k not in ['y_pred', 'y_prob']}
    for name, res in results.items()
}).T

fig, ax = plt.subplots(figsize=(16, 7))
x = np.arange(len(metrics_df))
width = 0.15
metric_colors = ['#3498DB', '#2ECC71', '#E74C3C', '#F39C12', '#9B59B6']

for i, (metric, color) in enumerate(zip(metrics_df.columns, metric_colors)):
    bars = ax.bar(x + i * width, metrics_df[metric], width, label=metric, color=color, edgecolor='white')
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                f'{height:.2f}', ha='center', va='bottom', fontsize=7, fontweight='bold')

ax.set_xticks(x + width * 2)
ax.set_xticklabels(metrics_df.index, rotation=15, ha='right')
ax.set_ylabel('Score')
ax.set_ylim(0, 1.12)
ax.set_title('Figure 24: Model Comparison — All Metrics', fontsize=16, fontweight='bold')
ax.legend(fontsize=10, loc='upper right')
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.savefig('../outputs/figures/31_model_comparison.png', dpi=200, bbox_inches='tight')
plt.show()
print("💾 Saved: 31_model_comparison.png")

# %% [markdown]
# ## 4.7 Cross-Validation (5-Fold Stratified)

# %%
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_results = {}

print("📊 5-Fold Stratified Cross-Validation Results:")
print(f"{'Model':<25} {'Mean Acc':<12} {'Std':<10} {'Mean F1':<12} {'Std':<10}")
print("-" * 70)

for name, model in models.items():
    acc_scores = cross_val_score(model, X_train_res, y_train_res, cv=cv, scoring='accuracy')
    f1_scores = cross_val_score(model, X_train_res, y_train_res, cv=cv, scoring='f1')
    cv_results[name] = {'accuracy': acc_scores, 'f1': f1_scores}
    print(f"{name:<25} {acc_scores.mean():<12.4f} {acc_scores.std():<10.4f} {f1_scores.mean():<12.4f} {f1_scores.std():<10.4f}")

# %%
# Box plot of CV scores
fig, axes = plt.subplots(1, 2, figsize=(18, 7))

# Accuracy
cv_acc_data = [cv_results[m]['accuracy'] for m in models]
bp1 = axes[0].boxplot(cv_acc_data, labels=list(models.keys()), patch_artist=True)
for patch, color in zip(bp1['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
axes[0].set_title('Cross-Validation: Accuracy', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Accuracy')
axes[0].tick_params(axis='x', rotation=20)

# F1 Score
cv_f1_data = [cv_results[m]['f1'] for m in models]
bp2 = axes[1].boxplot(cv_f1_data, labels=list(models.keys()), patch_artist=True)
for patch, color in zip(bp2['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
axes[1].set_title('Cross-Validation: F1-Score', fontsize=14, fontweight='bold')
axes[1].set_ylabel('F1-Score')
axes[1].tick_params(axis='x', rotation=20)

plt.suptitle('Figure 25: Cross-Validation Score Distributions', fontsize=17, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('../outputs/figures/32_cv_boxplots.png', dpi=200, bbox_inches='tight')
plt.show()
print("💾 Saved: 32_cv_boxplots.png")

# %% [markdown]
# ## 4.8 Hyperparameter Tuning (Top 2 Models)

# %%
# Find top 2 models by F1 score
top2 = sorted(results.items(), key=lambda x: x[1]['F1-Score'], reverse=True)[:2]
print(f"🏆 Top 2 models for hyperparameter tuning:")
for name, res in top2:
    print(f"   {name}: F1={res['F1-Score']:.4f}")

# %%
# Hyperparameter grids
param_grids = {
    'Random Forest': {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    },
    'XGBoost': {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 5, 7, 10],
        'learning_rate': [0.01, 0.05, 0.1, 0.2],
        'subsample': [0.8, 1.0]
    },
    'Logistic Regression': {
        'C': [0.001, 0.01, 0.1, 1, 10, 100],
        'penalty': ['l1', 'l2'],
        'solver': ['liblinear', 'saga']
    },
    'SVM': {
        'C': [0.1, 1, 10],
        'gamma': ['scale', 'auto', 0.01, 0.1],
        'kernel': ['rbf', 'linear']
    },
    'KNN': {
        'n_neighbors': [3, 5, 7, 9, 11],
        'weights': ['uniform', 'distance'],
        'metric': ['euclidean', 'manhattan']
    },
    'Decision Tree': {
        'max_depth': [None, 5, 10, 20],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
}

tuned_models = {}
for name, res in top2:
    print(f"\n{'='*50}")
    print(f"Tuning: {name}")
    print(f"{'='*50}")
    
    if name in param_grids:
        grid = GridSearchCV(models[name], param_grids[name], cv=3, scoring='f1', n_jobs=-1, verbose=0)
        grid.fit(X_train_res, y_train_res)
        
        print(f"   Best params: {grid.best_params_}")
        print(f"   Best CV F1:  {grid.best_score_:.4f}")
        
        # Evaluate on test
        y_pred = grid.best_estimator_.predict(X_test_scaled)
        y_prob = grid.best_estimator_.predict_proba(X_test_scaled)[:, 1]
        
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc_val = roc_auc_score(y_test, y_prob)
        
        print(f"   Test Accuracy:  {acc:.4f}")
        print(f"   Test F1-Score:  {f1:.4f}")
        print(f"   Test AUC:       {auc_val:.4f}")
        
        tuned_models[name] = {
            'model': grid.best_estimator_,
            'params': grid.best_params_,
            'accuracy': acc,
            'f1': f1,
            'auc': auc_val,
            'y_pred': y_pred,
            'y_prob': y_prob
        }

# %% [markdown]
# ## 4.9 Learning Curves (Best Model)

# %%
# Select best model
best_name = max(tuned_models, key=lambda k: tuned_models[k]['f1']) if tuned_models else top2[0][0]
best_model = tuned_models[best_name]['model'] if tuned_models else trained_models[best_name]

print(f"🏆 Best Model: {best_name}")

# Learning curve
train_sizes, train_scores, val_scores = learning_curve(
    best_model, X_train_res, y_train_res, cv=5, n_jobs=-1,
    train_sizes=np.linspace(0.1, 1.0, 10), scoring='f1'
)

fig, ax = plt.subplots(figsize=(12, 7))
ax.fill_between(train_sizes, train_scores.mean(axis=1) - train_scores.std(axis=1),
                train_scores.mean(axis=1) + train_scores.std(axis=1), alpha=0.1, color='#3498DB')
ax.fill_between(train_sizes, val_scores.mean(axis=1) - val_scores.std(axis=1),
                val_scores.mean(axis=1) + val_scores.std(axis=1), alpha=0.1, color='#E74C3C')
ax.plot(train_sizes, train_scores.mean(axis=1), 'o-', color='#3498DB', linewidth=2, label='Training F1')
ax.plot(train_sizes, val_scores.mean(axis=1), 'o-', color='#E74C3C', linewidth=2, label='Validation F1')

ax.set_xlabel('Training Set Size', fontsize=13)
ax.set_ylabel('F1-Score', fontsize=13)
ax.set_title(f'Figure 26: Learning Curve — {best_name}', fontsize=16, fontweight='bold')
ax.legend(fontsize=12)
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.savefig('../outputs/figures/33_learning_curve.png', dpi=200, bbox_inches='tight')
plt.show()
print("💾 Saved: 33_learning_curve.png")

# %% [markdown]
# ## 4.10 Classification Reports

# %%
print("📊 Detailed Classification Reports")
for name, res in results.items():
    print(f"\n{'='*50}")
    print(f"  {name}")
    print(f"{'='*50}")
    print(classification_report(y_test, res['y_pred'], target_names=['Non-PCOS', 'PCOS']))

# Tuned models
if tuned_models:
    print("\n" + "=" * 60)
    print("  TUNED MODELS")
    print("=" * 60)
    for name, info in tuned_models.items():
        print(f"\n{'='*50}")
        print(f"  {name} (Tuned)")
        print(f"{'='*50}")
        print(f"  Best params: {info['params']}")
        print(classification_report(y_test, info['y_pred'], target_names=['Non-PCOS', 'PCOS']))

# %% [markdown]
# ## 4.11 Save Best Model & Reports

# %%
# Save best model
joblib.dump(best_model, '../outputs/models/best_model.pkl')
print(f"💾 Saved: outputs/models/best_model.pkl ({best_name})")

# Save feature names for Streamlit
joblib.dump(X.columns.tolist(), '../outputs/models/feature_names.pkl')
print("💾 Saved: outputs/models/feature_names.pkl")

# %%
# Save comprehensive model comparison report
report_lines = []
report_lines.append("PCOS — MODEL COMPARISON REPORT")
report_lines.append("=" * 60)
report_lines.append(f"\nBest Model: {best_name}")
report_lines.append(f"Features used: {X.shape[1]}")
report_lines.append(f"Train samples: {X_train.shape[0]} (after SMOTE: {X_train_res.shape[0]})")
report_lines.append(f"Test samples: {X_test.shape[0]}")
report_lines.append(f"\n{'Model':<25} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1':<12} {'AUC':<12}")
report_lines.append("-" * 85)

for name, res in results.items():
    line = f"{name:<25} {res['Accuracy']:<12.4f} {res['Precision']:<12.4f} {res['Recall']:<12.4f} {res['F1-Score']:<12.4f} {res['AUC']:<12.4f}"
    report_lines.append(line)

if tuned_models:
    report_lines.append(f"\n\nTUNED MODELS:")
    report_lines.append("-" * 85)
    for name, info in tuned_models.items():
        report_lines.append(f"{name} (Tuned): Acc={info['accuracy']:.4f} F1={info['f1']:.4f} AUC={info['auc']:.4f}")
        report_lines.append(f"  Params: {info['params']}")

report_text = '\n'.join(report_lines)

with open('../outputs/reports/model_comparison_report.txt', 'w') as f:
    f.write(report_text)

print("\n💾 Saved: outputs/reports/model_comparison_report.txt")

print("\n" + "=" * 70)
print("  ✅ MODEL BUILDING & EVALUATION — COMPLETE")
print("=" * 70)
print(f"  🏆 Best Model: {best_name}")
if best_name in tuned_models:
    print(f"  📈 Test F1: {tuned_models[best_name]['f1']:.4f} | AUC: {tuned_models[best_name]['auc']:.4f}")
else:
    print(f"  📈 Test F1: {results[best_name]['F1-Score']:.4f} | AUC: {results[best_name]['AUC']:.4f}")
