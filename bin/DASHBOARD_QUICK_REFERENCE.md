# 🎯 FemoraHealth Dashboard - Quick Reference Card

## 🚀 Launch Commands

```bash
# Standard Launch
streamlit run app.py

# With Debug Logging
streamlit run app.py --logger.level=debug

# Custom Port
streamlit run app.py --server.port 8502

# Read-Only Mode
streamlit run app.py --client.toolbarMode minimal
```

---

## 🗺️ Navigation Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl/Cmd + S` | Save (if in input field) |
| `Escape` | Close popups/modals |
| `Tab` | Navigate between elements |
| `Enter` | Activate buttons |
| `Space` | Toggle checkboxes |

---

## 📊 Dashboard Pages Overview

### 1️⃣ Home (🏠)
**Best for**: First-time visitors  
**Contains**: Key metrics, model comparison, project intro  
**Time to explore**: 2-3 minutes

### 2️⃣ Dataset Overview (📊)
**Best for**: Understanding the data  
**Contains**: Statistics, distributions, correlations, sample data  
**Time to explore**: 3-5 minutes

### 3️⃣ Model Performance (📈)
**Best for**: Model evaluation details  
**Contains**: Performance comparison, ROC curves, confusion matrices  
**Time to explore**: 3-4 minutes

### 4️⃣ Feature Analysis (🧠)
**Best for**: Understanding predictions  
**Contains**: SHAP analysis, feature importance, dependence plots  
**Time to explore**: 4-5 minutes

### 5️⃣ Make Prediction (🔮)
**Best for**: Testing the model  
**Contains**: Interactive input form, risk prediction output  
**Time to use**: 2-3 minutes

### 6️⃣ About (ℹ️)
**Best for**: Project details  
**Contains**: Methodology, technologies, documentation  
**Time to read**: 5-10 minutes

---

## 🎨 Color Legend

```
🟣 Indigo (#6366F1)    = Primary/Main metrics
🩷 Pink (#EC4899)      = Secondary/Important alerts
🟢 Green (#10B981)     = Success/Positive indicators
🔵 Blue (#3B82F6)      = Information/Details
🟡 Amber (#F59E0B)     = Warnings/Caution
⚪ White (#FFFFFF)     = Cards/Containers
⬜ Gray (#F8F9FA)      = Background
```

---

## 📊 What Each Visualization Means

### Model Performance Radar Chart
- **Larger polygon** = Better overall performance
- **Points closer to outer edge** = Higher metrics (max 1.0)
- Use to compare model capabilities at a glance

### Bar Charts
- **Height** = Magnitude of the metric
- **Color gradient** = Value intensity (darker = higher)
- Hover for exact numbers

### Confusion Matrices
- **True Negatives** (top-left) = Correctly predicted negative
- **False Positives** (top-right) = Wrongly predicted positive
- **False Negatives** (bottom-left) = Missed positive cases
- **True Positives** (bottom-right) = Correctly predicted positive

### ROC Curves
- **Line closer to top-left** = Better model
- **Diagonal line** = Random guessing (50% performance)
- **AUC above 0.9** = Excellent discrimination

### SHAP Plots
- **Red dots** = High feature value pushing prediction up
- **Blue dots** = Low feature value pushing prediction down
- **Longer bars** = More important features

---

## 🧮 Understanding the Prediction Result

### Risk Categories
```
PCOS Positive Probability    Risk Level
─────────────────────────────────────────
75% - 100%                   🔴 HIGH RISK
50% - 74%                    🟡 MODERATE RISK
25% - 49%                    🟢 LOW-MODERATE RISK
0% - 24%                     🟢 LOW RISK
```

### What to Do
1. **If HIGH RISK**: Consult healthcare provider
2. **If MODERATE**: Monitor symptoms, schedule checkup
3. **If LOW**: Routine screening recommended
4. **Always**: Seek professional medical advice

---

## ⚙️ Customization Options

### Change Colors
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#new_color_code"
secondaryBackgroundColor = "#new_color_code"
```

### Change Layout
Edit `app.py`:
- Modify `st.set_page_config()` for page settings
- Adjust column widths: `col1, col2 = st.columns([2, 1])`
- Change font in CSS section

### Add More Pages
In `app.py`, add to sidebar options:
```python
page = st.radio("Navigation", ["...", "🆕 New Page"])
```
Then add `elif page == "🆕 New Page":` section

---

## 🐛 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Dashboard won't load | Check all dependencies in requirements.txt |
| Model not found | Verify `outputs/models/` folder exists |
| Images not showing | Run notebooks to regenerate plots |
| Slow performance | Clear browser cache, restart Streamlit |
| Layout broken | Ensure browser window is wide enough (1000px+) |
| Sidebar missing | Try: Press `>` button if it collapsed |

---

## 📈 Performance Metrics Explained

| Metric | Meaning | Formula | Ideal |
|--------|---------|---------|-------|
| **Accuracy** | Overall correctness | (TP+TN)/(TP+TN+FP+FN) | 100% |
| **Precision** | Positive pred. accuracy | TP/(TP+FP) | High (false alarms) |
| **Recall** | Catches all positives | TP/(TP+FN) | High (missed cases) |
| **F1-Score** | Balance of P & R | 2*(P*R)/(P+R) | High |
| **AUC** | Discrimination ability | Area under ROC curve | 0.9+ is excellent |

---

## 💡 Pro Tips

1. **Hover over charts** for detailed information
2. **Click legend items** in plots to toggle visibility
3. **Use tabs** to organize information logically
4. **Check sidebar metrics** for quick overview
5. **Read disclaimers** carefully before predictions
6. **Export data** using browser's download feature
7. **Share dashboard** via Streamlit Cloud for easy access
8. **Bookmark pages** you visit frequently

---

## 🔒 Data Privacy & Security

- ✅ All computations happen locally
- ✅ No data stored on external servers
- ✅ Model predictions are not logged
- ✅ Patient inputs are not saved
- ⚠️ This is not HIPAA compliant for production use

---

## 📚 Learning Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Plotly Docs**: https://plotly.com/python/
- **SHAP Documentation**: https://shap.readthedocs.io
- **Scikit-learn Guide**: https://scikit-learn.org/stable/
- **PCOS Information**: Medical journals and resources

---

## 🎓 What This Dashboard Demonstrates

✅ End-to-end ML pipeline  
✅ Data cleaning & preprocessing  
✅ Exploratory data analysis  
✅ Feature engineering & selection  
✅ Multiple model training & comparison  
✅ Cross-validation & tuning  
✅ Model evaluation metrics  
✅ SHAP explainability  
✅ Production-ready web deployment  
✅ Professional UI/UX design  

---

## 📞 Support & Troubleshooting

### For Technical Issues
1. Check Python version: `python --version` (3.8+ required)
2. Reinstall packages: `pip install -r requirements.txt --force-reinstall`
3. Clear cache: `streamlit cache clear`
4. Check logs: Run with `--logger.level=debug`

### For Data Issues
1. Verify data files exist: `data/PCOS_cleaned.csv`, `data/PCOS_final.csv`
2. Check model files: `outputs/models/*.pkl`
3. Regenerate plots: Run Jupyter notebooks

### For Deployment Issues
- Local: Check firewall settings
- Cloud: Verify GitHub integration
- Docker: Check image build logs

---

## 🎉 You're All Set!

The dashboard is ready to use. Start by:
1. Running the launch script or command
2. Opening http://localhost:8501
3. Exploring the Home page first
4. Then check Dataset Overview
5. Test predictions in Make Prediction page

**Happy analyzing! 🚀**

---

**Dashboard Version**: 1.0  
**Last Updated**: May 2024  
**Python**: 3.8+  
**Streamlit**: 1.28.0+  
