# Loan Risk Scoring API

A production-style REST API built with FastAPI that evaluates loan applications and returns a risk score and category.

## Features

- `POST /predict` – scores a loan application
- `GET /health` – health check endpoint
- Pydantic v2 input validation with descriptive error messages
- Logging to both console and file
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


## Input Validation Rules

- `age`: integer, 18–100
- `income`: float, must be > 0
- `loan_amount`: float, must be > 0 and ≤ 10× income
- `credit_score`: integer, 300–850
