from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, FinancialData, AIAdvice
from app.schemas import AIAdviceResponse
from app.auth import get_current_user
from app.gemini_service import generate_credit_advice

router = APIRouter(prefix="/ai-advice", tags=["AI Advice"])

@router.post("/", response_model=AIAdviceResponse)
def get_and_store_ai_advice(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    fin_data = db.query(FinancialData).filter(FinancialData.user_id == current_user.id).first()
    if not fin_data:
        raise HTTPException(status_code=400, detail="Please submit your financial data before asking for advice.")

    data_dict = {
        "credit_score": fin_data.credit_score,
        "monthly_income": fin_data.monthly_income,
        "monthly_expenses": fin_data.monthly_expenses,
        "total_debt": fin_data.total_debt,
        "credit_limit": fin_data.credit_limit,
        "credit_utilization": fin_data.credit_utilization,
        "dti_ratio": fin_data.dti_ratio
    }

    result = generate_credit_advice(data_dict)

    advice_record = AIAdvice(
        user_id=current_user.id,
        analysis=result["analysis"],
        action_plan=result["action_plan"]
    )
    db.add(advice_record)
    db.commit()
    db.refresh(advice_record)

    return advice_record

@router.get("/latest", response_model=AIAdviceResponse)
def get_latest_advice(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    advice = db.query(AIAdvice).filter(AIAdvice.user_id == current_user.id).order_by(AIAdvice.created_at.desc()).first()
    if not advice:
        raise HTTPException(status_code=404, detail="No AI advice records found.")
    return advice