# Loan Risk Scoring API

A production-style REST API built with FastAPI that evaluates loan applications and returns a risk score and category.

## Features

- `POST /predict` – scores a loan application
- `GET /health` – health check endpoint
- Pydantic v2 input validation with descriptive error messages
- Weighted scoring formula based on credit score, debt-to-income ratio, and age
- Logging to both console and file
- Fully configurable via environment variables
- Dockerized for easy deployment

## Risk Scoring Formula

The risk score is a pretraied ml simple regression model

**Categories:**
- `LOW` → score < 0.3
- `MEDIUM` → 0.3 ≤ score < 0.7
- `HIGH` → score ≥ 0.7

## Quick Start (local)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs available at: http://localhost:8000/docs

## Quick Start (Docker)

```bash
docker build -t loan-scoring-api .
docker run -p 8000:8000 loan-scoring-api
```

## Example Request

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 35, "income": 50000, "loan_amount": 10000, "credit_score": 680}'
```

**Response:**
```json
{
  "risk_score": 0.3521,
  "risk_category": "MEDIUM"
}
```

## Configuration

Copy `.env.example` to `.env` and adjust as needed:

| Variable | Default | Description |
|---|---|---|
| `APP_PORT` | `8000` | Server port |
| `LOG_LEVEL` | `INFO` | Logging level |
| `LOG_FILE` | `logs/app.log` | Log file path |
| `LOW_THRESHOLD` | `0.3` | Score below this → LOW |
| `HIGH_THRESHOLD` | `0.7` | Score above this → HIGH |
| `WEIGHT_CREDIT_SCORE` | `0.4` | Weight for credit score component |
| `WEIGHT_DEBT_RATIO` | `0.35` | Weight for debt-to-income component |
| `WEIGHT_AGE` | `0.25` | Weight for age component |

## Project Structure

```
app/
├── main.py               # FastAPI app and routes
├── models.py             # Pydantic input/output models
├── config.py             # Environment variable config
├── services/
│   └── scoring_service.py  # Risk scoring logic
└── utils/
    └── logger.py         # Logging setup
Dockerfile
requirements.txt
.env.example
```

## Input Validation Rules

- `age`: integer, 18–100
- `income`: float, must be > 0
- `loan_amount`: float, must be > 0 and ≤ 10× income
- `credit_score`: integer, 300–850
