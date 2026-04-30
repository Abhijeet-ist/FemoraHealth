#!/bin/bash

# FemoraHealth Dashboard Launch Script
# This script sets up the environment and launches the Streamlit dashboard

echo "🏥 FemoraHealth - PCOS Prediction Dashboard"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Navigate to project directory
cd "$(dirname "$0")" || exit

echo "📁 Project directory: $(pwd)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""
echo "🔄 Activating virtual environment..."
source venv/bin/activate

echo ""
echo "📚 Installing/Updating dependencies..."
pip install -r requirements.txt -q

echo ""
echo "✅ All set!"
echo ""
echo "=========================================="
echo "🚀 Launching FemoraHealth Dashboard..."
echo "=========================================="
echo ""
echo "📱 Dashboard will open at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Launch Streamlit
streamlit run app.py --logger.level=info

