"""Main FastAPI application."""

import os
import sys
import logging
import traceback
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

# Add KERAG root to path to import kerag
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from .api.routes import modules, nodes, search, status, settings
from .core.kerag_client import client

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
app = FastAPI(
    title="KERAG Web API",
    description="Web API for KERAG Knowledge Base",
    version="1.0.0"
)
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add global exception handler to catch all unhandled exceptions
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        logger.info(f"API Request: {request.method} {request.url.path}")
        response = await call_next(request)

        # Catch all 4xx and 5xx errors
        if response.status_code >= 400:
            # Clone response body to read error details
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            # Recreate response body
            response = JSONResponse(
                status_code=response.status_code,
                content=response_body.decode() if response_body else {"error": "Unknown error"}
            )

            # Print error information
            error_msg = f"\n{'='*80}\n[ERROR] API Response Error {response.status_code}: {request.method} {request.url.path}\n{'='*80}"
            error_msg += f"\nResponse Content: {response_body.decode()}\n{'='*80}\n"

            logger.error(error_msg)
            print(error_msg, file=sys.stderr)

        return response
    except Exception as exc:
        # Print full error info to console and logs
        error_msg = f"\n{'='*80}\n[ERROR] Uncaught Exception: {exc.__class__.__name__}: {str(exc)}\n{'='*80}"
        error_msg += f"\nRequest Info:\n  - Method: {request.method}\n  - URL: {request.url}\n  - Client IP: {request.client.host if request.client else 'unknown'}"
        error_msg += f"\n\nFull Traceback:\n{traceback.format_exc()}\n{'='*80}\n"

        logger.error(error_msg)
        print(error_msg, file=sys.stderr)

        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "detail": str(exc),
                "traceback": traceback.format_exc()
            }
        )

# Include routers with /api prefix (with trailing slash support)
app.include_router(modules.router, prefix="/api", tags=["modules"])
app.include_router(nodes.router, prefix="/api", tags=["nodes"])
app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(status.router, prefix="/api", tags=["status"])
app.include_router(settings.router, prefix="/api", tags=["settings"])

# Initialize KERAG API on startup
@app.on_event("startup")
async def startup_event():
    """Initialize KERAG on startup."""
    project_root = Path(__file__).parent.parent.parent.parent
    lang = os.getenv("KERAG_LANG", "")
    local_root = os.getenv("KERAG_LOCAL", "")
    global_root = os.getenv("KERAG_HOME", "")

    logger.info(f"Initializing KERAG with local root: {local_root}, global root: {global_root} and language: {lang}")
    client.init_api(local_root=local_root, global_root=global_root, lang=lang)
    logger.info(f"KERAG initialized with local root: {local_root}, global root: {global_root} and language: {lang}")

# Health check
@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

# Mount static files
# In production, frontend/dist contains the built assets
app_dir = Path(__file__).parent
# Case 1: Package installation (dist is inside kerag_web package)
static_path = app_dir.parent / "dist"

# Case 2: Source development (dist is in ../../../frontend/dist)
if not static_path.exists():
    static_path = app_dir.parent.parent.parent / "frontend" / "dist"

if static_path.exists():
    logger.info(f"Serving static files from: {static_path}")
    app.mount("/assets", StaticFiles(directory=str(static_path / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(request: Request, full_path: str):
        # Prevent accessing /api routes here (though include_router usually handles it)
        if full_path.startswith("api"):
            return JSONResponse(status_code=404, content={"error": "API endpoint not found"})

        # If the file exists in dist, serve it
        file_path = static_path / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))

        # Otherwise, serve index.html for SPA routing
        return FileResponse(str(static_path / "index.html"))
else:
    logger.warning(f"Static directory not found at {static_path}. Running in API-only mode.")

    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": "KERAG Web API (Development Mode)",
            "frontend_info": "Frontend dist not found. Please run frontend in dev mode or build it.",
            "docs": "/docs",
            "redoc": "/redoc"
        }
