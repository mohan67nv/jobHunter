"""
SmartJobHunter Pro - Main FastAPI Application
A beautiful, AI-powered job hunting dashboard for the German market
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time

from config import settings
from database import init_db, SessionLocal
from routers import jobs, applications, analysis, scrapers, user, analytics, dev
from routers import seed_real_jobs
from utils.logger import setup_logger
from utils.scheduler import setup_scheduler

logger = setup_logger(__name__)

# Scheduler instance (will be initialized in lifespan)
scheduler = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown events"""
    # Startup
    logger.info("🚀 Starting SmartJobHunter Pro...")
    
    # Initialize database
    try:
        init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
    
    # Start scheduler for automated scraping
    try:
        global scheduler
        scheduler = setup_scheduler(SessionLocal)
        logger.info("✅ Scheduler started")
    except Exception as e:
        logger.error(f"❌ Scheduler initialization failed: {e}")
    
    logger.info("🎉 SmartJobHunter Pro is ready!")
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down SmartJobHunter Pro...")
    
    if scheduler:
        scheduler.stop()
        logger.info("✅ Scheduler stopped")
    
    logger.info("✅ Shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="SmartJobHunter Pro API",
    description="AI-powered job hunting dashboard for the German job market",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": "SmartJobHunter Pro",
        "version": "1.0.0",
        "environment": settings.environment
    }


# Root endpoint
@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to SmartJobHunter Pro API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Include routers
app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(analysis.router)
app.include_router(scrapers.router)
app.include_router(user.router)
app.include_router(analytics.router)
app.include_router(dev.router)  # Developer utilities
app.include_router(seed_real_jobs.router)  # Seed realistic jobs


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all uncaught exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.debug else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        timeout_keep_alive=300  # 5 minutes for long AI analysis
    )
