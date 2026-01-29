"""Settings management endpoints."""

import os
from fastapi import APIRouter

# Reinitialize KERAG API
from ...core.kerag_client import client
from kerag.api import KERAGAPI

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/")
async def get_settings():
    """Get current settings."""
    return {
        "success": True,
        "data": {
            "kerag_home": os.getenv("KERAG_HOME", ""),
            "kerag_local": os.getenv("KERAG_LOCAL", ""),
            "kerag_lang": os.getenv("KERAG_LANG", "")
        },
        "metadata": {}
    }


@router.post("/apply")
async def apply_settings(settings: dict):
    """Apply settings and reinitialize."""
    try:
        # Update environment variables
        os.environ["KERAG_HOME"] = settings.get("kerag_home", "")
        os.environ["KERAG_LOCAL"] = settings.get("kerag_local", "")
        os.environ["KERAG_LANG"] = settings.get("kerag_lang", "")

        # Create new API instance
        new_api = KERAGAPI(
            local_root=settings.get("kerag_local"),
            global_root=settings.get("kerag_home"),
            lang=settings.get("kerag_lang")
        )

        # Replace the singleton instance
        client._api = new_api

        return {
            "success": True,
            "data": settings,
            "metadata": {
                "message": "Settings applied successfully"
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "metadata": {}
        }