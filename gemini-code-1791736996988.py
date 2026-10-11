from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    financial_data = relationship("FinancialData", back_populates="owner", uselist=False)
    score_history = relationship("ScoreHistory", back_populates="owner")
    ai_advices = relationship("AIAdvice", back_populates="owner")


class FinancialData(Base):
    __tablename__ = "financial_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    credit_score = Column(Integer, nullable=False)
    monthly_income = Column(Float, nullable=False)
    monthly_expenses = Column(Float, nullable=False)
    total_debt = Column(Float, nullable=False)
    credit_limit = Column(Float, nullable=False)
    credit_utilization = Column(Float, nullable=False)
    dti_ratio = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="financial_data")


class ScoreHistory(Base):
    __tablename__ = "score_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    credit_score = Column(Integer, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    improvement_delta = Column(Integer, default=0)

    owner = relationship("User", back_populates="score_history")


class AIAdvice(Base):
    __tablename__ = "ai_advice"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    analysis = Column(String, nullable=False)
    action_plan = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="ai_advices")