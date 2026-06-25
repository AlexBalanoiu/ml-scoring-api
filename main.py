from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from models import LoanApplication, ScoreResponse
from services.service_scoring import compute_risk_score, categorize_risk
from utils.logger import get_logger
APP_HOST = "0.0.0.0"   
APP_PORT = 8000         

logger = get_logger(__name__)

app = FastAPI(
    title="Loan Risk Scoring API",
    description="Evaluates loan applications and returns a risk score and category.",
    version="1.0.0",
)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.warning(f"Validation error on {request.url}: {exc}")
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error on {request.url}: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict", response_model=ScoreResponse)
def predict(application: LoanApplication):
    logger.info(
        f"Received application | age={application.age} income={application.income} "
        f"loan={application.loan_amount} credit={application.credit_score}"
    )

    score = compute_risk_score(
        age=application.age,
        income=application.income,
        loan_amount=application.loan_amount,
        credit_score=application.credit_score,
    )
    category = categorize_risk(score)

    logger.info(f"Result | risk_score={score} risk_category={category}")

    return ScoreResponse(risk_score=score, risk_category=category)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=APP_HOST, port=APP_PORT, reload=False)