"""System status endpoints."""

from fastapi import APIRouter
from ...core.kerag_client import client

router = APIRouter(prefix="/status", tags=["status"])


@router.get("/")
async def get_status():
    """Get system status."""
    try:
        result = client.api.get_status()
        return result
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
            "metadata": {}
        }
