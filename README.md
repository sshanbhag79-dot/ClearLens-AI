# 🧬 ClearLens-AI (LeedsHack 2026)

Theme: Systems Rebooted (Health & Consumer Transparency)

ClearLens-AI is a personalized AI lens for food products. It scans barcodes, fetches ingredients, and analyzes them against your unique biological profile (allergies, diets) to give you a clear Safety Rating.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+ installed.
- An API Key for Google Gemini.

### 2. Setup
```bash
# Clone the repository (if not already local)
# git clone <repo_url>

# Install Dependencies
pip install -r requirements.txt

# Configure Environment
# Copy .env.example to .env and open it to add your API Key
copy .env.example .env
notepad .env
```

### 3. Run the App
Double-click `run_app.bat` 
OR run manually:

**Backend:**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Frontend:**
```bash
streamlit run frontend/app.py
```

## 🏗️ Tech Stack
-   **Frontend**: Streamlit
-   **Backend**: FastAPI
-   **AI**: Google Gemini Flash
-   **Data**: Open Food Facts API

## 🧪 Features
-   **Bio-Profile**: Set allergies (Nut, Dairy, etc.) and goals (Vegan, Keto).
-   **Scanner**: Manual barcode entry (MVP) or Camera.
-   **Traffic Light UI**: Green/Yellow/Red safety indicators.
-   **Smart Reboots**: AI-suggested alternatives for unsafe products.
