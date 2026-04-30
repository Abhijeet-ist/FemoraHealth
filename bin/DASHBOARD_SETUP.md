# 🏥 FemoraHealth Dashboard - Setup & Usage Guide

## Quick Start

### 1. Install Dependencies
```bash
cd /Users/abhijeet.ist/Downloads/FemoraHealth
pip install -r requirements.txt
```

### 2. Run the Dashboard
```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

---

## 📋 Dashboard Features

### 🏠 **Home Page**
- Project overview with key metrics
- Model performance comparison
- Top predictive features visualization
- Project introduction and goals

### 📊 **Dataset Overview**
- Dataset statistics and summary
- Target class distribution
- Correlation analysis
- Feature distributions
- Data sample viewer

### 📈 **Model Performance**
- Model comparison table
- Individual metric analysis
- ROC curves comparison
- Confusion matrices
- Learning curves

### 🧠 **Feature Analysis**
- Feature importance ranking
- Statistical test scores (ANOVA, Chi², MI)
- SHAP summary plots
- SHAP force plots
- Feature dependence analysis
- Waterfall plots

### 🔮 **Make Prediction**
- Interactive patient data input
- Real-time PCOS risk prediction
- Probability visualization
- Risk assessment with confidence levels

### ℹ️ **About**
- Project documentation
- Methodology overview
- Dataset description
- Technology stack
- Key findings and insights

---

## 🎨 Design Features

### Color Palette (Light Aesthetic)
```
Primary (Indigo):    #6366F1
Secondary (Pink):    #EC4899
Success (Green):     #10B981
Info (Blue):         #3B82F6
Warning (Amber):     #F59E0B
Background:          #F8F9FA
```

### UI Components
- ✨ Smooth gradients and transitions
- 📱 Fully responsive design
- 🎯 Interactive visualizations with Plotly
- 💳 Beautiful metric cards
- 📊 Professional data tables
- 🌈 Modern color-coded visualizations

---

## 📁 Project Structure

```
FemoraHealth/
├── app.py                          # Main Streamlit dashboard
├── requirements.txt                # Python dependencies
├── data/
│   ├── PCOS_cleaned.csv
│   └── PCOS_final.csv
├── outputs/
│   ├── figures/                   # All visualizations (38 plots)
│   ├── models/
│   │   ├── best_model.pkl         # Trained Random Forest
│   │   ├── scaler.pkl             # Feature scaler
│   │   └── feature_names.pkl      # Feature list
│   └── reports/                   # Validation reports
├── notebooks/                      # Jupyter notebooks
└── README.md
```

---

## 🚀 How to Deploy

### Local Deployment
```bash
streamlit run app.py
```

### Cloud Deployment (Streamlit Cloud)
1. Push project to GitHub
2. Go to https://share.streamlit.io
3. Connect GitHub account
4. Deploy app.py
5. Share public link

### Docker Deployment
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

```bash
docker build -t femorahealth .
docker run -p 8501:8501 femorahealth
```

---

## 📊 Navigation Guide

| Page | Purpose | Key Components |
|------|---------|---|
| Home | Project overview | Metrics, model comparison, top features |
| Dataset | Data exploration | Stats, distributions, correlations, samples |
| Model Performance | Model evaluation | Metrics comparison, ROC curves, confusion matrices |
| Feature Analysis | SHAP & importance | Feature ranking, SHAP plots, dependence analysis |
| Make Prediction | Real-time predictions | Patient input form, prediction output |
| About | Documentation | Project info, methodology, resources |

---

## 🎯 Key Metrics Explained

- **Accuracy**: Overall correctness of predictions
- **Precision**: Accuracy of positive predictions (fewer false alarms)
- **Recall**: Ability to identify all positive cases
- **F1-Score**: Harmonic mean of precision and recall
- **AUC**: Area under ROC curve (0-1, higher is better)

---

## 💡 Tips for Best Experience

1. **First Time?** Start with the "Home" page for overview
2. **Data Curious?** Go to "Dataset Overview" for exploration
3. **Model Details?** Check "Model Performance" tab
4. **Understand Predictions?** Visit "Feature Analysis" for SHAP insights
5. **Try It Out?** Go to "Make Prediction" to test the model

---

## ⚠️ Important Disclaimers

- This dashboard is for **educational and research purposes**
- Model predictions should **NOT replace professional medical diagnosis**
- Always consult with healthcare professionals for proper evaluation
- Dataset contains 541 patients from a specific population
- Model performance may vary on different demographic groups

---

## 🛠️ Troubleshooting

### Model Not Loading?
- Check if `outputs/models/` folder exists
- Verify `best_model.pkl`, `scaler.pkl`, and `feature_names.pkl` files are present

### Visualizations Not Showing?
- Check if `outputs/figures/` folder has PNG files
- Try running the Jupyter notebooks to regenerate visualizations

### Dashboard Slow?
- Check internet connection
- Clear browser cache
- Restart Streamlit: `streamlit run app.py --logger.level=debug`

---

## 📚 Technologies

- **Streamlit**: Web app framework
- **Plotly**: Interactive visualizations
- **Scikit-learn**: Machine learning models
- **Pandas/NumPy**: Data processing
- **SHAP**: Model interpretation

---

## 📞 Contact & Support

For issues or questions about this project, please refer to the project documentation or contact the author.

---

**Last Updated**: May 2024  
**Version**: 1.0  
**Status**: Production Ready ✅
