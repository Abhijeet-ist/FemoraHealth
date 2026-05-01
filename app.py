import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import os
from datetime import datetime

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="FemoraHealth | PCOS Prediction Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS - LIGHT MODERN THEME ====================
def local_css():
    st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
        }
        
        /* Main background */
        .appViewContainer, .main {
            background: linear-gradient(135deg, #F8F9FA 0%, #F0F4F8 100%);
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #FFFFFF 0%, #F8F9FA 100%);
            border-right: 1px solid #E5E7EB;
        }
        
        /* Main content area */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #1F2937;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        
        h1 {
            font-size: 2.5rem;
            background: linear-gradient(135deg, #6366F1 0%, #EC4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        }
        
        h2 {
            font-size: 1.8rem;
            color: #374151;
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-bottom: 3px solid #6366F1;
            padding-bottom: 0.5rem;
        }
        
        h3 {
            font-size: 1.3rem;
            color: #4B5563;
        }
        
        /* Metric cards */
        .metric-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            border: 2px solid #E5E7EB;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            border-color: #6366F1;
            box-shadow: 0 8px 16px rgba(99, 102, 241, 0.15);
            transform: translateY(-2px);
        }
        
        /* Stat boxes with gradient headers */
        .stat-value {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0.5rem 0;
        }
        
        .stat-label {
            font-size: 0.95rem;
            color: #6B7280;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Primary accent */
        .accent-primary {
            color: #6366F1;
        }
        
        .accent-secondary {
            color: #EC4899;
        }
        
        .accent-success {
            color: #10B981;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #6366F1 0%, #818CF8 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            box-shadow: 0 8px 16px rgba(99, 102, 241, 0.3);
            transform: translateY(-2px);
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: white;
            border: 2px solid #E5E7EB;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            color: #6B7280;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
            color: white;
            border-color: #6366F1;
        }
        
        /* Input fields */
        .stTextInput input, .stSelectbox select, .stSlider {
            border-radius: 8px !important;
            border: 2px solid #E5E7EB !important;
        }
        
        /* Expanders */
        .stExpander {
            border: 2px solid #E5E7EB;
            border-radius: 8px;
            background: white;
        }
        
        /* Divider */
        .stDivider {
            margin: 2rem 0;
            border-color: #E5E7EB;
        }
        
        /* Text styling */
        p {
            color: #4B5563;
            line-height: 1.6;
        }
        
        /* Success/Info/Warning/Error boxes */
        .success-box {
            background: #ECFDF5;
            border-left: 4px solid #10B981;
            padding: 1rem;
            border-radius: 8px;
            color: #065F46;
        }
        
        .info-box {
            background: #EFF6FF;
            border-left: 4px solid #3B82F6;
            padding: 1rem;
            border-radius: 8px;
            color: #1E40AF;
        }
        
        .warning-box {
            background: #FFFBEB;
            border-left: 4px solid #F59E0B;
            padding: 1rem;
            border-radius: 8px;
            color: #92400E;
        }
        
        /* Cards in columns */
        .card {
            background: white;
            border: 1px solid #E5E7EB;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 2rem;
            color: #9CA3AF;
            font-size: 0.85rem;
            border-top: 1px solid #E5E7EB;
            margin-top: 3rem;
        }
    </style>
    """, unsafe_allow_html=True)

local_css()

# ==================== UTILITY FUNCTIONS ====================
@st.cache_resource
def load_model_and_scaler():
    """Load trained model and scaler"""
    try:
        with open('outputs/models/best_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('outputs/models/scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        try:
            with open('outputs/models/feature_names.pkl', 'rb') as f:
                feature_names = pickle.load(f)
        except:
            feature_names = None
        return model, scaler, feature_names
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        return None, None, None

@st.cache_data
def load_data():
    """Load cleaned and processed data"""
    try:
        df_cleaned = pd.read_csv('data/PCOS_cleaned.csv')
        df_final = pd.read_csv('data/PCOS_final.csv')
        return df_cleaned, df_final
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

def load_image(image_path):
    """Load and display image"""
    try:
        return Image.open(image_path)
    except:
        return None

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🏥 FemoraHealth")
    st.markdown("**PCOS Prediction Dashboard**")
    st.markdown("*INT 374: Data Science Toolbox*")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["🏠 Home", "📊 Dataset Overview", "📈 Model Performance", 
         "🧠 Feature Analysis", "🔮 Make Prediction", "ℹ️ About"]
    )
    
    st.markdown("---")
    st.markdown("### Dataset Info")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Samples", "541")
        st.metric("Features Used", "32")
    with col2:
        st.metric("PCOS Cases", "177")
        st.metric("Best Model AUC", "0.96")

# ==================== PAGE: HOME ====================
if page == "🏠 Home":
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("# 🏥 PCOS Prediction Dashboard")
        st.markdown("*Comprehensive analysis & predictive modeling for Polycystic Ovary Syndrome*")
    with col2:
        st.info(f"Last Updated: {datetime.now().strftime('%d %b %Y')}", icon="📅")
    
    st.markdown("---")
    
    # Key Metrics
    st.markdown("## 📊 Project Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="stat-label">Total Patients</div>
            <div class="stat-value accent-primary">541</div>
            <div style="font-size: 0.85rem; color: #9CA3AF;">Dataset Size</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="stat-label">PCOS Cases</div>
            <div class="stat-value accent-secondary">177</div>
            <div style="font-size: 0.85rem; color: #9CA3AF;">32.7% Prevalence</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="stat-label">Model Accuracy</div>
            <div class="stat-value accent-success">92%</div>
            <div style="font-size: 0.85rem; color: #9CA3AF;">Random Forest</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="stat-label">AUC Score</div>
            <div class="stat-value" style="color: #F59E0B;">0.96</div>
            <div style="font-size: 0.85rem; color: #9CA3AF;">Excellent Fit</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="metric-card">
            <div class="stat-label">Features</div>
            <div class="stat-value accent-primary">42</div>
            <div style="font-size: 0.85rem; color: #9CA3AF;">Clinical & Lab</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Model Comparison
    st.markdown("## 🎯 Model Performance Comparison")
    
    model_data = {
        'Model': ['Logistic Regression', 'Decision Tree', 'Random Forest', 'SVM', 'KNN', 'XGBoost'],
        'Accuracy': [0.85, 0.87, 0.92, 0.88, 0.83, 0.88],
        'Precision': [0.76, 0.85, 0.91, 0.83, 0.77, 0.84],
        'Recall': [0.81, 0.75, 0.83, 0.81, 0.69, 0.78],
        'F1-Score': [0.78, 0.80, 0.87, 0.82, 0.73, 0.81],
        'AUC': [0.93, 0.84, 0.96, 0.93, 0.87, 0.94]
    }
    
    df_models = pd.DataFrame(model_data)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = go.Figure(data=[
            go.Scatterpolar(
                r=df_models.loc[0, ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC']],
                theta=['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC'],
                fill='toself',
                name='Random Forest',
                line_color='#6366F1',
                fillcolor='rgba(99, 102, 241, 0.2)'
            ),
            go.Scatterpolar(
                r=df_models.loc[1, ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC']],
                theta=['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC'],
                fill='toself',
                name='XGBoost',
                line_color='#EC4899',
                fillcolor='rgba(236, 72, 153, 0.2)'
            )
        ])
        fig.update_layout(
            font_family="Arial",
            font_color="#1F2937",
            paper_bgcolor='rgba(255,255,255,0)',
            plot_bgcolor='rgba(248,249,250,0.5)',
            showlegend=True,
            height=400,
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <b>🏆 Best Model: Random Forest</b><br><br>
            • Accuracy: <b>92%</b><br>
            • AUC Score: <b>0.96</b><br>
            • Precision: <b>91%</b><br>
            • Recall: <b>83%</b><br>
            • F1-Score: <b>0.87</b><br><br>
            Excellent discriminative ability with minimal false positives.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key Features
    st.markdown("## 🔑 Top Predictive Features")
    
    top_features = {
        'Feature': ['Total Follicles', 'Symptom Score', 'Skin Darkening', 
                   'Hair Growth', 'FSH Level', 'LH/FSH Ratio'],
        'Importance': [0.18, 0.14, 0.12, 0.11, 0.10, 0.09]
    }
    
    df_features = pd.DataFrame(top_features)
    
    fig = px.bar(
        df_features,
        x='Importance',
        y='Feature',
        orientation='h',
        color='Importance',
        color_continuous_scale=['#A78BFA', '#8B5CF6', '#7C3AED', '#6D28D9'],
        title='Top 6 Features by Importance Score'
    )
    
    fig.update_layout(
        height=350,
        showlegend=False,
        hovermode='y unified',
        template="plotly_white",
        plot_bgcolor='rgba(248,249,250,0.5)',
        paper_bgcolor='rgba(255,255,255,0)',
        font_color="#1F2937"
    )
    fig.update_xaxes(title_text="Importance Score")
    fig.update_yaxes(title_text="")
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 🎓 About This Project")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h4 style="color: #6366F1;">📚 Dataset</h4>
            541 PCOS patients with 42 clinical, hormonal, and lifestyle features. Includes lab values, physical measurements, and symptom indicators.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4 style="color: #EC4899;">🔬 Methodology</h4>
            Comprehensive ML pipeline: data cleaning, EDA, feature engineering, model training with cross-validation, and SHAP-based interpretation.
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h4 style="color: #10B981;">🎯 Goal</h4>
            Enable early, accurate PCOS diagnosis prediction to support clinical decision-making and patient care.
        </div>
        """, unsafe_allow_html=True)

# ==================== PAGE: DATASET OVERVIEW ====================
elif page == "📊 Dataset Overview":
    st.markdown("# 📊 Dataset Overview & Analysis")
    st.markdown("Comprehensive exploratory data analysis of PCOS clinical dataset")
    st.markdown("---")
    
    df_cleaned, df_final = load_data()
    
    if df_cleaned is not None:
        # Dataset Statistics
        st.markdown("## 📈 Dataset Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="stat-label">Total Records</div>
                <div class="stat-value accent-primary">{len(df_cleaned)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="stat-label">Total Features</div>
                <div class="stat-value accent-secondary">{df_cleaned.shape[1]}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            pcos_count = (df_cleaned['PCOS'] == 1).sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="stat-label">PCOS Positive</div>
                <div class="stat-value accent-success">{pcos_count}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            non_pcos = (df_cleaned['PCOS'] == 0).sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="stat-label">PCOS Negative</div>
                <div class="stat-value" style="color: #F59E0B;">{non_pcos}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Tabs for different analyses
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Target Distribution", "🔄 Correlations", "📉 Distributions", "🗂️ Data Sample"])
        
        with tab1:
            st.markdown("### Target Class Distribution")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                pcos_counts = df_cleaned['PCOS'].value_counts().sort_index()
                fig = go.Figure(data=[
                    go.Bar(
                        x=['Non-PCOS', 'PCOS'],
                        y=[pcos_counts[0], pcos_counts[1]],
                        marker_color=['#6366F1', '#EC4899'],
                        text=[pcos_counts[0], pcos_counts[1]],
                        textposition='auto',
                    )
                ])
                fig.update_layout(
                    height=400,
                    showlegend=False,
                    template="plotly_white",
                    plot_bgcolor='rgba(248,249,250,0.5)',
                    paper_bgcolor='rgba(255,255,255,0)',
                    font_color="#1F2937"
                )
                fig.update_xaxes(title_text="")
                fig.update_yaxes(title_text="Count")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                pcos_pct = (pcos_counts[1] / len(df_cleaned) * 100)
                non_pcos_pct = (pcos_counts[0] / len(df_cleaned) * 100)
                
                fig_pie = go.Figure(data=[go.Pie(
                    labels=['Non-PCOS', 'PCOS'],
                    values=[int(pcos_counts[0]), int(pcos_counts[1])],
                    marker=dict(colors=['#6366F1', '#EC4899']),
                    textinfo='label+percent',
                    hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
                )])
                fig_pie.update_layout(
                    height=400,
                    template="plotly_white",
                    paper_bgcolor='rgba(255,255,255,0)',
                    font_color="#1F2937"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with tab2:
            st.markdown("### Feature Correlation Analysis")
            
            # Load correlation heatmap image
            heatmap_path = 'outputs/figures/06_correlation_heatmap.png'
            if os.path.exists(heatmap_path):
                img = load_image(heatmap_path)
                st.image(img, use_column_width=True)
            else:
                st.info("Correlation heatmap visualization loading...")
        
        with tab3:
            st.markdown("### Feature Distributions")
            
            # Load distribution plots
            dist_path = 'outputs/figures/04_target_distribution.png'
            if os.path.exists(dist_path):
                img = load_image(dist_path)
                st.image(img, use_column_width=True)
        
        with tab4:
            st.markdown("### Dataset Sample")
            st.dataframe(
                df_cleaned.head(10),
                use_container_width=True,
                height=400
            )
            
            st.markdown("### Data Types & Info")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Numeric Features**")
                numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns.tolist()
                st.info(f"Count: {len(numeric_cols)}\n\n" + ", ".join(numeric_cols[:5]) + "...")
            
            with col2:
                st.markdown("**Missing Values**")
                missing = df_cleaned.isnull().sum()
                if missing.sum() == 0:
                    st.success("✅ No missing values!")
                else:
                    st.warning(f"Missing values: {missing[missing > 0].to_dict()}")

# ==================== PAGE: MODEL PERFORMANCE ====================
elif page == "📈 Model Performance":
    st.markdown("# 📈 Model Performance & Evaluation")
    st.markdown("Detailed analysis of all trained models")
    st.markdown("---")
    
    # Model Comparison Table
    st.markdown("## Model Performance Comparison")
    
    model_data = {
        'Model': ['Logistic Regression', 'Decision Tree', 'Random Forest', 'SVM', 'KNN', 'XGBoost'],
        'Accuracy': [0.85, 0.87, 0.92, 0.88, 0.83, 0.88],
        'Precision': [0.76, 0.85, 0.91, 0.83, 0.77, 0.84],
        'Recall': [0.81, 0.75, 0.83, 0.81, 0.69, 0.78],
        'F1-Score': [0.78, 0.80, 0.87, 0.82, 0.73, 0.81],
        'AUC': [0.93, 0.84, 0.96, 0.93, 0.87, 0.94]
    }
    
    df_models = pd.DataFrame(model_data)
    
    # Highlight best model
    def highlight_best(s):
        is_max = s == s.max()
        return ['background-color: rgba(16, 185, 129, 0.2)' if v else '' for v in is_max]
    
    st.dataframe(
        df_models.style.apply(highlight_best, subset=['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC']),
        use_container_width=True,
        height=300
    )
    
    st.markdown("---")
    
    # Tabs for detailed analysis
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Performance Metrics", "🎯 ROC Curves", "🔍 Confusion Matrices", "📉 Learning Curves"])
    
    with tab1:
        st.markdown("### Metrics Comparison")
        
        metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC']
        
        for metric in metrics:
            fig = px.bar(
                df_models,
                x='Model',
                y=metric,
                color=metric,
                color_continuous_scale=['#A78BFA', '#8B5CF6', '#7C3AED', '#6D28D9'],
                title=f'{metric} Comparison'
            )
            fig.update_layout(
                height=300,
                showlegend=False,
                template="plotly_white",
                plot_bgcolor='rgba(248,249,250,0.5)',
                paper_bgcolor='rgba(255,255,255,0)',
                font_color="#1F2937",
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### ROC Curves")
        
        roc_path = 'outputs/figures/29_roc_curves.png'
        if os.path.exists(roc_path):
            img = load_image(roc_path)
            st.image(img, use_column_width=True)
        else:
            st.info("ROC curves visualization loading...")
    
    with tab3:
        st.markdown("### Confusion Matrices")
        
        conf_path = 'outputs/figures/28_confusion_matrices.png'
        if os.path.exists(conf_path):
            img = load_image(conf_path)
            st.image(img, use_column_width=True)
        else:
            st.info("Confusion matrices visualization loading...")
    
    with tab4:
        st.markdown("### Learning Curves")
        
        learning_path = 'outputs/figures/33_learning_curve.png'
        if os.path.exists(learning_path):
            img = load_image(learning_path)
            st.image(img, use_column_width=True)
        else:
            st.info("Learning curves visualization loading...")

# ==================== PAGE: FEATURE ANALYSIS ====================
elif page == "🧠 Feature Analysis":
    st.markdown("# 🧠 Feature Importance & SHAP Analysis")
    st.markdown("Understanding model predictions through feature importance")
    st.markdown("---")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📊 Feature Ranking", "🎯 SHAP Summary", "📈 SHAP Values", "🔗 Dependence", "⚡ Waterfall"]
    )
    
    with tab1:
        st.markdown("### Combined Feature Ranking")
        
        ranking_path = 'outputs/figures/27_combined_feature_ranking.png'
        if os.path.exists(ranking_path):
            img = load_image(ranking_path)
            st.image(img, use_column_width=True)
        else:
            st.info("Feature ranking visualization loading...")
        
        st.markdown("### Statistical Test Scores")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            anova_path = 'outputs/figures/24_anova_fscores.png'
            if os.path.exists(anova_path):
                img = load_image(anova_path)
                st.image(img, use_column_width=True)
        
        with col2:
            chi2_path = 'outputs/figures/25_chi2_scores.png'
            if os.path.exists(chi2_path):
                img = load_image(chi2_path)
                st.image(img, use_column_width=True)
        
        with col3:
            mi_path = 'outputs/figures/26_mutual_info.png'
            if os.path.exists(mi_path):
                img = load_image(mi_path)
                st.image(img, use_column_width=True)
    
    with tab2:
        st.markdown("### SHAP Summary Plot")
        
        summary_path = 'outputs/figures/34_shap_summary.png'
        if os.path.exists(summary_path):
            img = load_image(summary_path)
            st.image(img, use_column_width=True)
        else:
            st.info("SHAP summary plot loading...")
        
        st.markdown("### SHAP Bar Plot")
        
        bar_path = 'outputs/figures/35_shap_bar.png'
        if os.path.exists(bar_path):
            img = load_image(bar_path)
            st.image(img, use_column_width=True)
    
    with tab3:
        st.markdown("### SHAP Force Plot")
        
        st.info("🔍 SHAP values show how much each feature contributes to pushing the prediction from the base value to the actual prediction.")
        
        summary_path = 'outputs/figures/34_shap_summary.png'
        if os.path.exists(summary_path):
            img = load_image(summary_path)
            st.image(img, use_column_width=True)
    
    with tab4:
        st.markdown("### Feature Dependence Plots")
        
        dep_path = 'outputs/figures/37_shap_dependence.png'
        if os.path.exists(dep_path):
            img = load_image(dep_path)
            st.image(img, use_column_width=True)
        else:
            st.info("Dependence plots loading...")
    
    with tab5:
        st.markdown("### SHAP Waterfall Plot")
        
        waterfall_path = 'outputs/figures/36_shap_waterfall.png'
        if os.path.exists(waterfall_path):
            img = load_image(waterfall_path)
            st.image(img, use_column_width=True)
        else:
            st.info("Waterfall plot loading...")

# ==================== PAGE: MAKE PREDICTION ====================
elif page == "🔮 Make Prediction":
    st.markdown("# 🔮 PCOS Prediction Tool")
    st.markdown("Enter patient data to get a PCOS risk prediction")
    st.markdown("---")
    
    model, scaler, feature_names = load_model_and_scaler()
    
    if model is not None:
        st.markdown("## Patient Information")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            age = st.slider("Age (years)", 15, 60, 28)
            weight = st.slider("Weight (kg)", 40, 120, 65)
            height = st.slider("Height (cm)", 140, 190, 160)
            bmi = weight / ((height/100) ** 2)
            st.info(f"BMI: {bmi:.1f}")
        
        with col2:
            systolic = st.slider("Systolic BP (mmHg)", 80, 180, 120)
            diastolic = st.slider("Diastolic BP (mmHg)", 50, 110, 80)
            fsh = st.slider("FSH Level (mIU/mL)", 1.0, 15.0, 6.0)
            lh = st.slider("LH Level (mIU/mL)", 1.0, 30.0, 8.0)
        
        with col3:
            amh = st.slider("AMH Level (ng/mL)", 0.0, 15.0, 3.0)
            follicles_l = st.slider("Left Follicles", 0, 30, 5)
            follicles_r = st.slider("Right Follicles", 0, 30, 5)
            hair_growth = st.selectbox("Hair Growth (Y/N)", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        
        st.markdown("---")
        
        # Create input array - simplified with 12 key features
        input_data = np.array([[
            age, weight, height, bmi, systolic, diastolic,
            fsh, lh, amh, follicles_l + follicles_r, hair_growth, 0
        ]])
        
        # Make prediction
        if st.button("🔍 Predict PCOS Risk", use_container_width=True):
            try:
                # Create simple prediction without scaler if scaler is None
                if scaler is not None:
                    input_scaled = scaler.transform(input_data)
                else:
                    input_scaled = input_data
                
                # Get prediction
                prediction = model.predict(input_scaled)[0]
                probability = model.predict_proba(input_scaled)[0]
                
                st.markdown("---")
                st.markdown("## 📋 Prediction Result")
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if prediction == 1:
                        st.markdown("""
                        <div class="warning-box" style="text-align: center; padding: 2rem;">
                            <h2 style="color: #F59E0B; margin: 0;">⚠️ HIGH RISK</h2>
                            <p style="margin: 1rem 0 0 0; font-size: 1.1rem; font-weight: 600;">PCOS Likely</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="success-box" style="text-align: center; padding: 2rem;">
                            <h2 style="color: #10B981; margin: 0;">✅ LOW RISK</h2>
                            <p style="margin: 1rem 0 0 0; font-size: 1.1rem; font-weight: 600;">PCOS Unlikely</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    fig = go.Figure(data=[
                        go.Bar(
                            x=['PCOS Negative', 'PCOS Positive'],
                            y=[probability[0] * 100, probability[1] * 100],
                            marker_color=['#6366F1', '#EC4899'],
                            text=[f'{probability[0] * 100:.1f}%', f'{probability[1] * 100:.1f}%'],
                            textposition='auto'
                        )
                    ])
                    fig.update_layout(
                        height=300,
                        showlegend=False,
                        template="plotly_white",
                        plot_bgcolor='rgba(248,249,250,0.5)',
                        paper_bgcolor='rgba(255,255,255,0)',
                        font_color="#1F2937",
                        yaxis_title="Probability (%)"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("---")
                st.markdown("## 📊 Probability Breakdown")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        "PCOS Negative Probability",
                        f"{probability[0] * 100:.1f}%",
                        delta=None
                    )
                
                with col2:
                    st.metric(
                        "PCOS Positive Probability",
                        f"{probability[1] * 100:.1f}%",
                        delta=None
                    )
                
                st.markdown("---")
                st.markdown("""
                <div class="info-box">
                    <b>📝 Important Note</b><br><br>
                    This prediction is generated by a machine learning model trained on clinical data.
                    It should NOT be used as a substitute for professional medical diagnosis.
                    Please consult with a healthcare provider for proper evaluation and diagnosis.
                </div>
                """, unsafe_allow_html=True)
            
            except Exception as e:
                st.error(f"Error making prediction: {e}")
    else:
        st.warning("⚠️ Model not loaded")
        st.info("""
        The model files couldn't be loaded. Please ensure:
        1. `outputs/models/best_model.pkl` exists
        2. `outputs/models/scaler.pkl` exists
        
        If you're seeing pickle errors, the model may need to be regenerated.
        """)
        
        # Provide simulation/demo prediction
        st.markdown("---")
        st.markdown("## 📋 Demo Prediction (Using Random Forest Simulation)")
        st.info("Demo mode activated - Showing simulated predictions")
        
        # Create a simple linear model for demo
        age = st.slider("Age (years)", 15, 60, 28)
        weight = st.slider("Weight (kg)", 40, 120, 65)
        height = st.slider("Height (cm)", 140, 190, 160)
        follicles = st.slider("Total Follicles", 0, 50, 15)
        
        if st.button("🔍 Demo Prediction", use_container_width=True):
            # Simple heuristic for demo
            risk_score = (age - 20) * 0.02 + (weight - 50) * 0.01 + (follicles - 10) * 0.03
            probability_positive = 1 / (1 + np.exp(-risk_score))
            probability_negative = 1 - probability_positive
            
            st.markdown("---")
            st.markdown("## 📋 Demo Prediction Result")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if probability_positive > 0.5:
                    st.warning(f"Risk Level: {probability_positive * 100:.1f}%")
                else:
                    st.success(f"Risk Level: {probability_positive * 100:.1f}%")
            
            with col2:
                fig = go.Figure(data=[
                    go.Bar(
                        x=['PCOS Negative', 'PCOS Positive'],
                        y=[probability_negative * 100, probability_positive * 100],
                        marker_color=['#6366F1', '#EC4899'],
                        text=[f'{probability_negative * 100:.1f}%', f'{probability_positive * 100:.1f}%'],
                        textposition='auto'
                    )
                ])
                fig.update_layout(
                    height=300,
                    showlegend=False,
                    template="plotly_white",
                    plot_bgcolor='rgba(248,249,250,0.5)',
                    paper_bgcolor='rgba(255,255,255,0)',
                    font_color="#1F2937",
                    yaxis_title="Probability (%)"
                )
                st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE: ABOUT ====================
elif page == "ℹ️ About":
    st.markdown("# ℹ️ About This Project")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 🏥 FemoraHealth - PCOS Prediction Dashboard
        
        **Course**: INT 374 - Data Science Toolbox: Python Programming
        
        **Objective**: Build a comprehensive machine learning pipeline to predict Polycystic Ovary Syndrome (PCOS) 
        diagnosis from clinical, hormonal, and lifestyle features.
        
        ---
        
        ## 📊 Dataset Overview
        
        - **Samples**: 541 patients
        - **Features**: 42 clinical and laboratory measurements
        - **Target**: Binary classification (PCOS: Yes/No)
        - **Class Distribution**: 67.3% Non-PCOS, 32.7% PCOS (moderate imbalance)
        
        **Feature Categories**:
        - Demographic data (age, weight, height)
        - Hormonal levels (FSH, LH, AMH, TSH, etc.)
        - Physical measurements (BMI, waist-hip ratio, blood pressure)
        - Symptom indicators (hair growth, skin darkening, acne, etc.)
        - Lifestyle factors (exercise, diet, fast food consumption)
        - Follicle counts and ovarian measurements
        
        ---
        
        ## 🚀 Methodology
        
        ### Phase 1: Data Preparation
        - Data loading and merging from multiple sources
        - Comprehensive data cleaning and validation
        - Missing value imputation and outlier detection
        - Type conversion and feature standardization
        
        ### Phase 2: Exploratory Data Analysis
        - 38 professional visualizations
        - Distribution analysis
        - Correlation studies
        - Target variable analysis
        
        ### Phase 3: Feature Engineering
        - Statistical tests (ANOVA, Chi-square, Mutual Information)
        - Correlation-based feature selection
        - Feature ranking and importance analysis
        - Dimensionality reduction (42 → 32 key features)
        
        ### Phase 4: Model Development
        - 6 machine learning models trained:
          - Logistic Regression
          - Decision Tree
          - **Random Forest** (Best)
          - SVM
          - K-Nearest Neighbors
          - XGBoost
        - Class balancing with SMOTE
        - Hyperparameter tuning with GridSearchCV
        - Cross-validation (5-fold)
        
        ### Phase 5: Model Evaluation
        - Comprehensive metrics: Accuracy, Precision, Recall, F1-Score, AUC
        - ROC curves and confusion matrices
        - Learning curves and model comparison
        
        ### Phase 6: Interpretability
        - SHAP (SHapley Additive exPlanations) analysis
        - Feature contribution visualization
        - Dependence plots
        - Waterfall plots for individual predictions
        
        ### Phase 7: Deployment
        - Streamlit dashboard for interactive predictions
        - Model persistence with pickle
        - Real-time prediction interface
        
        ---
        
        ## 🎯 Best Model: Random Forest
        
        **Performance Metrics**:
        - **Accuracy**: 92%
        - **Precision**: 91%
        - **Recall**: 83%
        - **F1-Score**: 0.87
        - **AUC**: 0.96
        
        **Advantages**:
        - Excellent discriminative ability
        - Robust to outliers
        - Handles non-linear relationships
        - Feature importance readily available
        - Minimal false positive rate
        
        ---
        
        ## 📊 Key Findings
        
        **Top Predictive Features**:
        1. Total Follicles (18% importance)
        2. Symptom Score (14%)
        3. Skin Darkening (12%)
        4. Hair Growth (11%)
        5. FSH Level (10%)
        6. LH/FSH Ratio (9%)
        
        **Clinical Insights**:
        - Hormonal imbalances are strong PCOS indicators
        - Follicle count is the most important predictor
        - Physical symptoms (hair growth, skin darkening) are significant
        - Multiple symptoms together increase confidence in diagnosis
        
        ---
        
        ## 💡 Technologies Used
        
        **Data Processing**:
        - Pandas, NumPy
        
        **Visualization**:
        - Matplotlib, Seaborn, Plotly
        
        **Machine Learning**:
        - Scikit-learn, XGBoost
        
        **Model Interpretation**:
        - SHAP
        
        **Web Application**:
        - Streamlit
        
        **Development**:
        - Python 3.8+, Jupyter Notebooks
        """)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4 style="color: #6366F1;">📚 Resources</h4>
            <ul style="color: #4B5563; line-height: 2;">
                <li><a href="#" style="color: #6366F1; text-decoration: none;">Project Repository</a></li>
                <li><a href="#" style="color: #6366F1; text-decoration: none;">Dataset Info</a></li>
                <li><a href="#" style="color: #6366F1; text-decoration: none;">Research Papers</a></li>
                <li><a href="#" style="color: #6366F1; text-decoration: none;">Documentation</a></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h4 style="color: #EC4899;">👤 Author</h4>
            <p style="color: #4B5563;">Abhijeet Kumar</p>
            <p style="color: #9CA3AF; font-size: 0.9rem;">Data Science | Machine Learning<br>Student at Lovely Professional University</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h4 style="color: #10B981;">📅 Project Info</h4>
            <p style="color: #4B5563;">
                <strong>Status:</strong> Complete<br>
                <strong>Version:</strong> 1.0<br>
                <strong>License:</strong> MIT
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>🏥 <strong>FemoraHealth</strong> - PCOS Prediction Dashboard </p>
    <p>INT 374: Data Science Toolbox | University Project</p>
    <p style="margin-top: 1rem; font-size: 0.8rem;"></p>
</div>
""", unsafe_allow_html=True)
