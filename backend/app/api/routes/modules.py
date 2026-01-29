"""Module management endpoints."""

import traceback
import sys
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from ...core.kerag_client import client


router = APIRouter(prefix="/modules", tags=["modules"])


def handle_exception(e: Exception, endpoint_name: str, status_code: int = 500) -> HTTPException:
    """统一错误处理函数，打印详细错误并返回HTTPException"""
    error_detail = f"{str(e)}\n\nFull traceback:\n{traceback.format_exc()}"
    print(f"\n{'='*80}\n[ERROR] {endpoint_name} ({status_code}):\n{error_detail}\n{'='*80}\n", file=sys.stderr)
    return HTTPException(status_code=status_code, detail=error_detail)


@router.get("/")
async def get_all_modules():
    """Get all modules."""
    try:
        result = client.api.get_all_modules()
        if not result.get("success"):
            raise handle_exception(Exception(result.get("error", "Failed to get modules")), "/modules", 500)

        return result
    except Exception as e:
        raise handle_exception(e, "/modules")


@router.get("/roots")
async def get_loaded_roots():
    """Get all loaded module root nodes."""
    try:
        result = client.api.get_loaded_roots()
        if not result.get("success"):
             raise handle_exception(Exception(result.get("error", "Failed to get roots")), "/modules/roots", 500)

        return result
    except Exception as e:
        raise handle_exception(e, "/modules/roots")


@router.post("/load")
async def load_module(module_name: str = Query(..., description="Name of the module to load")):
    """Load a module."""
    try:
        result = client.api.load_module(module_name)
        if not result.get("success"):
            error_msg = result.get("error", "Unknown error")
            raise handle_exception(Exception(error_msg), "/modules/load", 400)

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise handle_exception(e, "/modules/load")


@router.delete("/unload")
async def unload_module(module_name: str = Query(..., description="Name of the module to unload")):
    """Unload a module."""
    try:
        result = client.api.unload_module(module_name)
        if not result.get("success"):
            error_msg = result.get("error", "Unknown error")
            raise handle_exception(Exception(error_msg), "/modules/unload", 400)

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise handle_exception(e, "/modules/unload")


@router.post("/purge")
async def purge_modules():
    """Unload all modules."""
    try:
        result = client.api.purge()
        if not result.get("success"):
            error_msg = result.get("error", "Unknown error")
            raise handle_exception(Exception(error_msg), "/modules/purge", 400)

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise handle_exception(e, "/modules/purge")
