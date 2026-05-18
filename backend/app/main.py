from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.test_routes import router as test_router

app = FastAPI(
    title="Auto Test Data Generator",
    description="LLM + Genetic Algorithm + Hill Climbing for automatic test data generation",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test_router, prefix="/api/test", tags=["Test Generator"])


@app.get("/")
def home():
    return {
        "message": "Auto Test Data Generator Backend is running",
        "docs": "/docs",
    }