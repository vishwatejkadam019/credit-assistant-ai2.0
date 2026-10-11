from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth_router, financial_router, ai_router

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Credit Assistant: AI-Powered Financial Health Advisor",
    version="1.0.0",
    description="Backend API for managing credit health, tracking CIBIL history, and receiving personalized AI advice."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(financial_router.router)
app.include_router(ai_router.router)

@app.get("/")
def read_root():
    return {"message": "Credit Assistant API is up and running!"}