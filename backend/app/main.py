from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
import os
from dotenv import load_dotenv

from app.api import auth, analytics, reports, social_data, users
from app.core.config import settings

# Load environment variables
load_dotenv()

# Security
security = HTTPBearer()

app = FastAPI(
    title="AI Social Intelligence API",
    description="AI-powered social media intelligence and company operations platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["User Management"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(social_data.router, prefix="/api/social-data", tags=["Social Data"])
# app.include_router(datasets.router, prefix="/api/datasets", tags=["Datasets"])  # Temporarily disabled
# app.include_router(realtime.router, prefix="/api/realtime", tags=["Real-time"])  # Temporarily disabled

@app.get("/")
async def root():
    return {
        "message": "AI Social Intelligence API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )