from pydantic import BaseModel, Field, field_validator


class LoanApplication(BaseModel):
    age: int = Field(..., ge=18, le=100, description="Applicant age (18–100)")
    income: float = Field(..., gt=0, description="Annual income in USD (must be > 0)")
    loan_amount: float = Field(..., gt=0, description="Requested loan amount in USD (must be > 0)")
    credit_score: int = Field(..., ge=300, le=850, description="Credit score (300–850)")

    @field_validator("loan_amount")
    @classmethod
    def loan_must_not_exceed_income_cap(cls, v, info):
        # Loan amount must not exceed 10x income
        if "income" in info.data and v > info.data["income"] * 10:
            raise ValueError("loan_amount cannot exceed 10x the applicant's income")
        return v


class ScoreResponse(BaseModel):
    risk_score: float = Field(..., description="Normalized risk score between 0.0 and 1.0")
    risk_category: str = Field(..., description="Risk category: LOW, MEDIUM, or HIGH")