# 🏥 Insurance Premium Category Predictor

A machine learning web application that predicts insurance premium categories based on user demographics and lifestyle factors. Built with **FastAPI** (backend) and **Streamlit** (frontend), trained using a **scikit-learn Pipeline** with a Random Forest classifier.

---

## 📁 Project Structure

```
insurance-premium-predictor/
├── ml_model.ipynb       # Data preprocessing, feature engineering & model training
├── main.py              # FastAPI backend server
├── frontend.py          # Streamlit UI
├── pipeline.pkl         # Serialized sklearn Pipeline (preprocessor + classifier)
├── insurance.csv        # Raw training dataset
├── pyproject.toml       # Project dependencies managed by uv
├── .venv/               # Virtual environment (managed by uv, not committed)
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Package Manager | [uv](https://github.com/astral-sh/uv) |
| ML | scikit-learn (RandomForestClassifier) |
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Data | Pandas, NumPy |
| Serialization | Pickle |

---

## 🧠 How It Works

### Feature Engineering (Notebook → Pipeline)
Raw user inputs are transformed into engineered features before being fed to the model:

| Raw Input | Engineered Feature | Logic |
|---|---|---|
| `weight`, `height` | `bmi` | `weight / height²` |
| `age` | `age_group` | young / adult / middle_aged / senior |
| `smoker` + `bmi` | `lifestyle_risk` | low / medium / high |
| `city` | `city_tier` | 1 (metro) / 2 (tier-2) / 3 (rest) |

The trained object exported as `pipeline.pkl` is a full **sklearn Pipeline** — it contains both the `ColumnTransformer` (with OneHotEncoder) and the `RandomForestClassifier`. This means encoding and prediction happen in a single `pipeline.predict()` call.

### Request Flow
```
User fills Streamlit form
    → POST /predict (JSON with 7 raw fields)
    → FastAPI validates input via Pydantic (computes engineered features automatically)
    → pipeline.predict() runs OHE + RandomForest internally
    → Returns predicted category (low / medium / high)
    → Streamlit displays result
```

---

## 🚀 Getting Started

### Prerequisites
Make sure you have [uv](https://github.com/astral-sh/uv) installed:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 1. Clone the repository
```bash
git clone https://github.com/ArunAryal/insurance-premium-category-predictor.git
cd insurance-premium-category-predictor
```

### 2. Set up the environment
```bash
uv sync
```
This will create a `.venv` and install all dependencies from `pyproject.toml`.

### 3. Train the model (optional — as `pipeline.pkl` is already present)
Open and run all cells in `ml_model.ipynb`. This will generate `pipeline.pkl`.

### 4. Run the backend
```bash
uv run uvicorn main:app --reload
```
FastAPI will be available at `http://localhost:8000`. You can explore the auto-generated API docs at `http://localhost:8000/docs`.

### 5. Run the frontend (in a separate terminal)
```bash
uv run streamlit run frontend.py
```
The app will open in your browser at `http://localhost:8501`.

> ⚠️ **Both servers must be running simultaneously.** The Streamlit frontend makes HTTP requests to the FastAPI backend — if the backend is down, predictions will fail.

---

## 📬 API Reference

### `POST /predict`

**Request Body:**
```json
{
  "age": 30,
  "weight": 70.0,
  "height": 1.75,
  "income_lpa": 12.0,
  "smoker": false,
  "city": "Mumbai",
  "occupation": "private_job"
}
```

**Response:**
```json
{
  "response": {
    "predicted_category": "low"
  }
}
```

**Supported occupations:** `retired`, `freelancer`, `student`, `government_job`, `business_owner`, `unemployed`, `private_job`

---

## 📄 License

MIT License. Feel free to use and modify.
