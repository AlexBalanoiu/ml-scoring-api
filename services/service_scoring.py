import joblib
import numpy as np

from utils.logger import get_logger

LOW_THRESHOLD =0.3
HIGH_THRESHOLD =0.7
logger = get_logger(__name__)

_model = joblib.load('model_risk.pkl')
_scaler = joblib.load('scaler_risk.pkl')

def compute_risk_score(age: int, income: float, loan_amount: float, credit_score: int) -> float:
    features = np.array([[age, income, loan_amount, credit_score]])
    features_scaled = _scaler.transform(features)
    score = float(_model.predict(features_scaled)[0])
    score = round(max(0.0, min(1.0, score)), 4)
    logger.debug(
        f"Model scoring | age={age} income={income} loan={loan_amount} "
        f"credit={credit_score} | final={score}"
    )
    return score

def categorize_risk(score: float) -> str:
    if score < LOW_THRESHOLD:
        return "LOW"
    elif score < HIGH_THRESHOLD:
        return "MEDIUM"
    else:
        return "HIGH"