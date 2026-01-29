"""Search endpoints."""

import traceback
import sys
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ...core.kerag_client import client


router = APIRouter(prefix="/search", tags=["search"])


def handle_exception(e: Exception, endpoint_name: str) -> HTTPException:
    """统一错误处理函数，打印详细错误并返回HTTPException"""
    error_detail = f"{str(e)}\n\nFull traceback:\n{traceback.format_exc()}"
    print(f"\n{'='*80}\n[ERROR] {endpoint_name} - Exception:\n{error_detail}\n{'='*80}\n", file=sys.stderr)
    return HTTPException(status_code=500, detail=error_detail)


@router.get("/")
async def search(
    q: str = Query(..., min_length=1, description="Search keyword"),
    scope: str = Query("all", regex="^(all|content|title|label)$"),
    max_results: int = Query(50, ge=1, le=1000),
    whole_word: bool = Query(False),
    case_sensitive: bool = Query(False),
    use_regex: bool = Query(False)
):
    """Search nodes."""
    try:
        result = client.api.search(
            keyword=q,
            scope=scope,
            max_results=max_results,
            whole_word=whole_word,
            case_sensitive=case_sensitive,
            use_regex=use_regex
        )

        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))

        return result
    except HTTPException:
        raise
    except Exception as e:
        error_detail = f"{str(e)}\n\nFull traceback:\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)
