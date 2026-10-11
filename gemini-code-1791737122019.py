from datetime import datetime, timedelta
from app.database import SessionLocal, Base, engine
from app.models import User, FinancialData, ScoreHistory, AIAdvice
from app.auth import get_password_hash

def seed_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    demo_user = User(
        name="Aarav Sharma",
        email="aarav@example.com",
        hashed_password=get_password_hash("password123")
    )
    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)

    # Initial financial entry (Fair credit status)
    fin_data = FinancialData(
        user_id=demo_user.id,
        credit_score=680,
        monthly_income=75000.0,
        monthly_expenses=32000.0,
        total_debt=180000.0,
        credit_limit=300000.0,
        credit_utilization=(180000.0 / 300000.0) * 100, # 60.0%
        dti_ratio=(32000.0 / 75000.0) * 100 # 42.6%
    )
    db.add(fin_data)

    # 4 months history
    base_date = datetime.utcnow() - timedelta(days=120)
    scores = [620, 645, 660, 680]
    
    for i, s in enumerate(scores):
        delta = 0 if i == 0 else s - scores[i-1]
        rec_date = base_date + timedelta(days=30 * i)
        history_item = ScoreHistory(
            user_id=demo_user.id,
            credit_score=s,
            recorded_at=rec_date,
            improvement_delta=delta
        )
        db.add(history_item)

    # Initial AI advice seed
    advice = AIAdvice(
        user_id=demo_user.id,
        analysis="Fair",
        action_plan=[
            "Your Credit Utilization is high at 60.0%. Pay down balances to under ₹90,000 to keep it below 30%.",
            "Your DTI ratio is 42.7%, exceeding the recommended 40%. Lower monthly EMI expenses or boost income.",
            "Set up NACH auto-debit for your credit card dues to maintain a 100% on-time payment track record.",
            "Avoid applying for multiple new credit cards or personal loans within a 6-month window to minimize hard inquiries.",
            "Monitor your CIBIL report quarterly to verify all accounts are properly reported."
        ]
    )
    db.add(advice)

    db.commit()
    db.close()
    print("Seed complete: Demo user created (Email: aarav@example.com, Pass: password123)")

if __name__ == "__main__":
    seed_database()