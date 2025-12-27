from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import warnings

# Suppress noisy warnings (safe for prod/dev)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Import routers
from app.routers import dashboard, analysis, chat

# Initialize FastAPI app
app = FastAPI(
    title="CyberSpy API",
    description="Modular AI-powered Cyber Security Threat Detection Backend",
    version="2.0.0"
)

# CORS Middleware (restrict later for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to frontend URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Router Registration (SINGLE SOURCE OF TRUTH)
# -------------------------------------------------

# Dashboard & Streaming APIs
app.include_router(
    dashboard.router,
    prefix="/api/dashboard",
    tags=["Dashboard"]
)

# File, URL, QR, PCAP analysis APIs
app.include_router(
    analysis.router,
    prefix="/api/analyze",
    tags=["Analysis"]
)

# AI Chat APIs
app.include_router(
    chat.router,
    prefix="/api/chat",
    tags=["Chat"]
)

# -------------------------------------------------
# Health Check
# -------------------------------------------------
@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "CyberSpy Core Active",
        "version": "2.0.0"
    }
