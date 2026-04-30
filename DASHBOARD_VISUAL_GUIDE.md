# 🏥 FemoraHealth Dashboard - Visual Guide & Architecture

## Dashboard Overview Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     🏥 FemoraHealth Dashboard                   │
│              PCOS Prediction | INT 374 Data Science             │
└─────────────────────────────────────────────────────────────────┘
                                  │
                  ┌───────────────┴───────────────┐
                  │                               │
          ┌───────▼────────┐          ┌──────────▼────────┐
          │   SIDEBAR NAV  │          │  MAIN CONTENT     │
          │                │          │                   │
          │ • Home         │          │  Dynamic Pages    │
          │ • Dataset      │          │  based on         │
          │ • Models       │          │  selection        │
          │ • Features     │          │                   │
          │ • Predict      │          │  Renders:         │
          │ • About        │          │  - Plots          │
          │                │          │  - Tables         │
          │ Dataset Info   │          │  - Forms          │
          └────────────────┘          └───────────────────┘
```

---

## Page Structure & Layout

### 🏠 HOME PAGE
```
┌─ Header ─────────────────────────────────────────────┐
│ 🏥 PCOS Prediction Dashboard                         │
│ Comprehensive analysis & predictive modeling         │
└──────────────────────────────────────────────────────┘
┌─ Key Metrics Row ────────────────────────────────────┐
│  [541]     [177]      [92%]      [0.96]    [42]     │
│  Patients  PCOS       Accuracy   AUC       Features │
│           Cases                                      │
└──────────────────────────────────────────────────────┘
┌─ Model Comparison ───────────────────────────────────┐
│  Radar Chart         Best Model Info                 │
│  (Performance        • Accuracy: 92%                 │
│   Metrics)           • AUC: 0.96                     │
│                      • F1: 0.87                      │
└──────────────────────────────────────────────────────┘
┌─ Top Predictive Features ────────────────────────────┐
│  Bar Chart (Horizontal)                              │
│  Total Follicles, Symptom Score, Skin Darkening     │
└──────────────────────────────────────────────────────┘
┌─ Project Info Cards ─────────────────────────────────┐
│  [Dataset]  [Methodology]  [Goal]                    │
│   Card        Card         Card                      │
└──────────────────────────────────────────────────────┘
```

### 📊 DATASET OVERVIEW PAGE
```
┌─ Statistics Row ──────────────────────────────────────┐
│  [541]        [42]         [177]        [364]       │
│  Records      Features     PCOS (+)     PCOS (-)    │
└───────────────────────────────────────────────────────┘
┌─ Tabs Navigation ─────────────────────────────────────┐
│  [Target Distribution] [Correlations] [Distributions]│
│  [Data Sample]                                       │
├───────────────────────────────────────────────────────┤
│  TAB 1: Target Distribution                          │
│  ├─ Bar Chart (Count)                               │
│  └─ Pie Chart (Percentage)                          │
│                                                      │
│  TAB 2: Correlation Analysis                        │
│  └─ Heatmap Image (from outputs/figures)            │
│                                                      │
│  TAB 3: Feature Distributions                       │
│  └─ Distribution Plots (from outputs/figures)       │
│                                                      │
│  TAB 4: Data Sample                                 │
│  ├─ DataFrame Preview (10 rows)                     │
│  └─ Data Types & Missing Values Summary             │
└───────────────────────────────────────────────────────┘
```

### 📈 MODEL PERFORMANCE PAGE
```
┌─ Model Comparison Table ──────────────────────────────┐
│  Model      Accuracy Precision Recall F1 AUC         │
│  ────────────────────────────────────────────────    │
│  Random Forest 92%    91%      83%    0.87 0.96      │ (Highlighted)
│  XGBoost       88%    84%      78%    0.81 0.94      │
│  SVM           88%    83%      81%    0.82 0.93      │
│  ...more...                                          │
└───────────────────────────────────────────────────────┘
┌─ Tabs Navigation ─────────────────────────────────────┐
│  [Metrics] [ROC Curves] [Confusion Matrices] [Learning]│
├───────────────────────────────────────────────────────┤
│  TAB 1: Performance Metrics                          │
│  ├─ Accuracy Bar Chart                              │
│  ├─ Precision Bar Chart                             │
│  ├─ Recall Bar Chart                                │
│  ├─ F1-Score Bar Chart                              │
│  └─ AUC Bar Chart                                   │
│                                                      │
│  TAB 2: ROC Curves                                  │
│  └─ ROC Curves Comparison Image                     │
│                                                      │
│  TAB 3: Confusion Matrices                          │
│  └─ All Models Confusion Matrices Image             │
│                                                      │
│  TAB 4: Learning Curves                             │
│  └─ Learning Curve Analysis Image                   │
└───────────────────────────────────────────────────────┘
```

### 🧠 FEATURE ANALYSIS PAGE
```
┌─ Tabs Navigation ─────────────────────────────────────┐
│  [Ranking] [SHAP Summary] [SHAP Values] [Dependence]  │
│  [Waterfall]                                          │
├───────────────────────────────────────────────────────┤
│  TAB 1: Feature Ranking                              │
│  ├─ Combined Feature Ranking Image                  │
│  ├─ ANOVA F-Scores Image                            │
│  ├─ Chi-Square Scores Image                         │
│  └─ Mutual Information Image                        │
│                                                      │
│  TAB 2: SHAP Summary                                 │
│  ├─ SHAP Summary Plot Image                         │
│  └─ SHAP Bar Plot Image                             │
│                                                      │
│  TAB 3: SHAP Values                                 │
│  ├─ Info Box (Explanation)                          │
│  └─ SHAP Force Plot Image                           │
│                                                      │
│  TAB 4: Dependence Plots                            │
│  └─ Feature Dependence Analysis Image               │
│                                                      │
│  TAB 5: Waterfall Plot                              │
│  └─ SHAP Waterfall Visualization Image              │
└───────────────────────────────────────────────────────┘
```

### 🔮 MAKE PREDICTION PAGE
```
┌─ Patient Information Input ───────────────────────────┐
│                                                       │
│  Column 1:          Column 2:        Column 3:       │
│  • Age (slider)     • Systolic BP    • AMH Level     │
│  • Weight (slider)  • Diastolic BP   • Follicles     │
│  • Height (slider)  • FSH Level      • Hair Growth   │
│  • BMI (display)    • LH Level       • Skin Darkening│
│                                                       │
│         [🔍 Predict PCOS Risk Button]               │
└───────────────────────────────────────────────────────┘
┌─ Prediction Result (After Button Click) ──────────────┐
│                                                       │
│  Result Box              Probability Chart           │
│  ┌─────────────────┐     ┌──────────────────────┐   │
│  │  ⚠️ HIGH RISK   │     │  [Bar Chart]         │   │
│  │  PCOS Likely    │     │  Neg: 25%  Pos: 75% │   │
│  └─────────────────┘     └──────────────────────┘   │
│                                                      │
│  Probability Breakdown                              │
│  • PCOS Negative: 25%                              │
│  • PCOS Positive: 75%                              │
│                                                      │
│  ⚠️ Important Disclaimer Box                        │
│  (Medical advice warning)                           │
└───────────────────────────────────────────────────────┘
```

### ℹ️ ABOUT PAGE
```
┌─ Left Column ─────────────┬─ Right Column ────────────┐
│                           │                           │
│ Main Documentation        │ • Resources Card         │
│ • Project Description     │ • Author Info Card       │
│ • Dataset Overview        │ • Project Info Card      │
│ • Methodology Sections    │                          │
│ • Best Model Details      │                          │
│ • Key Findings            │                          │
│ • Technologies Used       │                          │
│                           │                          │
└───────────────────────────┴───────────────────────────┘
```

---

## Color Scheme & Design System

### Primary Colors
```
Indigo (Primary):     #6366F1  ██████████
Pink (Secondary):     #EC4899  ██████████
Emerald (Success):    #10B981  ██████████
Blue (Info):          #3B82F6  ██████████
Amber (Warning):      #F59E0B  ██████████
```

### Background & Text
```
Background:           #F8F9FA  ░░░░░░░░░░░░░░░░░░░░
Card Background:      #FFFFFF  ████████████████████
Primary Text:         #1F2937  ████████████████████
Secondary Text:       #4B5563  ██████████████
Muted Text:           #9CA3AF  ████████
```

### Component Styling
```
┌─ Metric Card ─────────────────────────┐
│  Label (uppercase, muted gray)       │
│  12345 (large, gradient color)       │
│  Subtext (smaller gray)              │
│                                      │
│  On Hover: Border highlights,       │
│  shadow grows, slight lift           │
└──────────────────────────────────────┘

┌─ Button ──────────────────────────────┐
│  Gradient Background                 │
│  White Text                          │
│  Rounded Corners                     │
│  Smooth Hover Effect                 │
│  Shadow on Hover                     │
└──────────────────────────────────────┘

┌─ Info Box ────────────────────────────┐
│  Left Border: Colored                │
│  Light Background: Tinted            │
│  Colored Text                        │
│  Rounded Corners                     │
└──────────────────────────────────────┘
```

---

## User Flow Diagram

```
                          🏥 Dashboard Launch
                                │
                                ▼
                    ┌──────────────────────┐
                    │   Sidebar Navigation │
                    └──────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
            Home Page      Dataset Exp.    Model Perf.
                │               │               │
                ├──────────────┬┴──────────────┤
                │              │               │
                ▼              ▼               ▼
          Feature Anal.   Prediction     About Page
                │              │               │
                └──────────┬───┴───────────────┘
                           │
                    ┌──────▼───────┐
                    │  Sidebar Info│
                    │  Dataset KPIs│
                    └──────────────┘
```

---

## Responsive Design

The dashboard is optimized for:
- 💻 **Desktop** (1920x1080 and above)
- 📱 **Tablet** (768px and above)
- 📲 **Mobile** (responsive columns)

All visualizations use Plotly's responsive features.

---

## Interactive Features

### Input Elements
- ✅ Sliders for numeric input (Age, Weight, Height, etc.)
- ✅ Selectboxes for categorical input (Yes/No)
- ✅ Tabs for organizing content
- ✅ Expanders for additional details
- ✅ Buttons for predictions and actions

### Visualizations
- 📊 Interactive bar charts with hover info
- 📈 Plotly graphs with zoom/pan
- 🔄 Heatmaps with color gradients
- 📍 Scatter plots with correlation colors
- 🥧 Pie charts with percentage labels

### Displays
- 📋 Sortable dataframes
- 📌 Metric cards with status
- 📬 Info/Warning/Success boxes
- 💬 Tooltips and help text

---

## Performance Optimizations

- ⚡ Caching with `@st.cache_data` for data loading
- ⚡ Caching with `@st.cache_resource` for model loading
- ⚡ Lazy loading of images
- ⚡ Plotly for efficient interactive charts
- ⚡ Minimal re-renders with proper state management

---

## Accessibility Features

- ✅ High contrast colors (WCAG AA compliant)
- ✅ Clear labels for all inputs
- ✅ Descriptive button text
- ✅ Alt text for images
- ✅ Keyboard navigable
- ✅ Readable font sizes

---

## File Organization

```
FemoraHealth/
├── app.py                    ← Main dashboard (YOU ARE HERE)
├── .streamlit/
│   ├── config.toml           ← Streamlit settings
│   └── theme.json            ← Theme configuration
├── data/
│   ├── PCOS_cleaned.csv      ← Processed data
│   └── PCOS_final.csv        ← Feature-selected data
├── outputs/
│   ├── figures/
│   │   ├── 04_target_distribution.png
│   │   ├── 06_correlation_heatmap.png
│   │   ├── 24-37_analysis_plots.png
│   │   └── ...38 total visualizations
│   ├── models/
│   │   ├── best_model.pkl    ← Trained model
│   │   ├── scaler.pkl        ← Feature scaler
│   │   └── feature_names.pkl ← Feature list
│   └── reports/              ← Validation reports
├── notebooks/                ← Jupyter notebooks
├── requirements.txt          ← Python dependencies
├── launch_dashboard.sh       ← Launch script
├── DASHBOARD_SETUP.md        ← Setup guide
└── README.md                 ← Project info
```

---

## 🚀 Quick Launch

### Option 1: Direct Command
```bash
cd /Users/abhijeet.ist/Downloads/FemoraHealth
streamlit run app.py
```

### Option 2: Using Launch Script
```bash
chmod +x launch_dashboard.sh
./launch_dashboard.sh
```

### Option 3: With Virtual Environment
```bash
source venv/bin/activate
streamlit run app.py
```

---

## Browser Recommendations

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

All modern browsers support the dashboard features.

---

**Created**: May 2024  
**Version**: 1.0  
**Status**: Production Ready ✅
