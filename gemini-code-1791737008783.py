from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class FinancialDataInput(BaseModel):
    credit_score: int = Field(..., ge=300, le=900, description="CIBIL score between 300 and 900")
    monthly_income: float = Field(..., gt=0)
    monthly_expenses: float = Field(..., ge=0)
    total_debt: float = Field(..., ge=0)
    credit_limit: float = Field(..., gt=0)

class FinancialDataResponse(BaseModel):
    id: int
    user_id: int
    credit_score: int
    monthly_income: float
    monthly_expenses: float
    total_debt: float
    credit_limit: float
    credit_utilization: float
    dti_ratio: float
    updated_at: datetime

    class Config:
        from_attributes = True

class ScoreHistoryResponse(BaseModel):
    id: int
    user_id: int
    credit_score: int
    recorded_at: datetime
    improvement_delta: int

    class Config:
        from_attributes = True

class UtilizationResponse(BaseModel):
    used_credit: float
    available_credit: float
    total_limit: float
    utilization_percentage: float

class AIAdviceResponse(BaseModel):
    id: int
    user_id: int
    analysis: str
    action_plan: List[str]
    created_at: datetime

    class Config:
        from_attributes = True