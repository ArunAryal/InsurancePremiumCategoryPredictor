# 🏥 Insurance Premium Category Predictor

A machine learning web application that predicts insurance premium categories based on user demographics and lifestyle factors. Built with **FastAPI** (backend) and **Streamlit** (frontend), trained using a **scikit-learn Pipeline** with a Random Forest classifier.

---

## 📁 Project Structure

```
InsurancePremiumPredictor/
├── config/
│   └── city_tier.py            # Tier 1 and Tier 2 city lists
├── frontend/
│   └── frontend.py             # Streamlit UI
├── model/
│   ├── insurance.csv           # Raw training dataset
│   ├── ml_model.ipynb          # Feature engineering & model training
│   ├── pipeline.pkl            # Serialized sklearn Pipeline (not committed)
│   └── predict.py              # Prediction logic & pipeline loader
├── schema/
│   ├── user_input.py           # Pydantic input validation model
│   └── prediction_response.py  # Pydantic response model
├── main.py                     # FastAPI app & route definitions
├── pyproject.toml              # Project dependencies managed by uv
├── .env                        # Environment variables (not committed)
├── .python-version             # Python version pin
├── uv.lock                     # Locked dependency versions
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
| Configuration | python-dotenv |

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

City names are automatically normalized (stripped and title-cased) via a Pydantic `@field_validator`, so inputs like `"mumbai"` or `" Mumbai "` are handled gracefully.

The trained object exported as `pipeline.pkl` is a full **sklearn Pipeline** — it contains both the `ColumnTransformer` (with OneHotEncoder) and the `RandomForestClassifier`. This means encoding and prediction happen in a single `pipeline.predict()` call.

### Request Flow
```
User fills Streamlit form
    → POST /predict (JSON with 7 raw fields)
    → FastAPI validates input via Pydantic (computes engineered features automatically)
    → pipeline.predict() runs OHE + RandomForest internally
    → Returns predicted category + confidence score + class probabilities
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
git clone https://github.com/ArunAryal/InsurancePremiumCategoryPredictor
cd InsurancePremiumCategoryPredictor
```

### 2. Set up the environment
```bash
uv sync
```
This will create a `.venv` and install all dependencies from `pyproject.toml`.

### 3. Configure environment variables
Create a `.env` file in the project root:
```
API_URL=http://localhost:8000/predict
```

### 4. Train the model
Open and run all cells in `model/ml_model.ipynb`. This will generate `model/pipeline.pkl`.

### 5. Run the backend
```bash
uv run uvicorn main:app --reload
```
FastAPI will be available at `http://localhost:8000`. You can explore the auto-generated API docs at `http://localhost:8000/docs`.

### 6. Run the frontend (in a separate terminal)
```bash
uv run streamlit run frontend/frontend.py
```
The app will open in your browser at `http://localhost:8501`.

> ⚠️ **Both servers must be running simultaneously.** The Streamlit frontend makes HTTP requests to the FastAPI backend — if the backend is down, predictions will fail.

---

## 📬 API Reference

### `GET /`
Returns a human-readable message confirming the API is running.

**Response:**
```json
{
  "message": "Insurance Premium Prediction API"
}
```

---

### `GET /health`
Machine-readable health check. Useful for monitoring and deployment pipelines.

**Response:**
```json
{
  "status": "OK",
  "version": "1.0.0",
  "model_loaded": true
}
```

---

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
  "predicted_category": "low",
  "confidence": 0.87,
  "class_probablities": {
    "high": 0.05,
    "low": 0.87,
    "medium": 0.08
  }
}
```

**Supported occupations:** `retired`, `freelancer`, `student`, `government_job`, `business_owner`, `unemployed`, `private_job`

---

## 📄 License

MIT License. Feel free to use and modify.
