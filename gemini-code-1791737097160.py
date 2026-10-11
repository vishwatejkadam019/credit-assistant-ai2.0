from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.models import User, FinancialData, ScoreHistory
from app.schemas import FinancialDataInput, FinancialDataResponse, ScoreHistoryResponse, UtilizationResponse
from app.auth import get_current_user

router = APIRouter(prefix="/financial", tags=["Financial Data"])

@router.post("/", response_model=FinancialDataResponse)
@router.put("/", response_model=FinancialDataResponse)
def create_or_update_financial_data(
    data: FinancialDataInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Formulas:
    # DTI = (monthly debt payments / monthly income) * 100
    # Utilization = (total debt / credit limit) * 100
    dti_ratio = (data.monthly_expenses / data.monthly_income) * 100
    credit_utilization = (data.total_debt / data.credit_limit) * 100

    existing_data = db.query(FinancialData).filter(FinancialData.user_id == current_user.id).first()

    # Calculate score delta relative to previous score history
    last_history = db.query(ScoreHistory).filter(ScoreHistory.user_id == current_user.id).order_by(ScoreHistory.recorded_at.desc()).first()
    
    delta = 0
    if last_history:
        delta = data.credit_score - last_history.credit_score
    
    if existing_data:
        existing_data.credit_score = data.credit_score
        existing_data.monthly_income = data.monthly_income
        existing_data.monthly_expenses = data.monthly_expenses
        existing_data.total_debt = data.total_debt
        existing_data.credit_limit = data.credit_limit
        existing_data.credit_utilization = credit_utilization
        existing_data.dti_ratio = dti_ratio
        fin_obj = existing_data
    else:
        fin_obj = FinancialData(
            user_id=current_user.id,
            credit_score=data.credit_score,
            monthly_income=data.monthly_income,
            monthly_expenses=data.monthly_expenses,
            total_debt=data.total_debt,
            credit_limit=data.credit_limit,
            credit_utilization=credit_utilization,
            dti_ratio=dti_ratio
        )
        db.add(fin_obj)

    # Append to score history on every update
    new_history = ScoreHistory(
        user_id=current_user.id,
        credit_score=data.credit_score,
        improvement_delta=delta,
        recorded_at=datetime.utcnow()
    )
    db.add(new_history)

    db.commit()
    db.refresh(fin_obj)
    return fin_obj

@router.get("/current", response_model=FinancialDataResponse)
def get_current_financial_data(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = db.query(FinancialData).filter(FinancialData.user_id == current_user.id).first()
    if not data:
        raise HTTPException(status_code=404, detail="No financial data found")
    return data

@router.get("/history", response_model=List[ScoreHistoryResponse])
def get_score_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    history = db.query(ScoreHistory).filter(ScoreHistory.user_id == current_user.id).order_by(ScoreHistory.recorded_at.asc()).all()
    return history

@router.get("/utilization", response_model=UtilizationResponse)
def get_utilization(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = db.query(FinancialData).filter(FinancialData.user_id == current_user.id).first()
    if not data:
        raise HTTPException(status_code=404, detail="No financial data found")

    available = max(0.0, data.credit_limit - data.total_debt)
    return UtilizationResponse(
        used_credit=data.total_debt,
        available_credit=available,
        total_limit=data.credit_limit,
        utilization_percentage=round(data.credit_utilization, 2)
    )