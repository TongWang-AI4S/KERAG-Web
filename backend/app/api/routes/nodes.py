"""Node navigation and content endpoints."""

import traceback
import sys
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from pydantic import BaseModel
from urllib.parse import unquote
import logging
from ...core.kerag_client import client


router = APIRouter(prefix="/nodes", tags=["nodes"])


def handle_exception(e: Exception, endpoint_name: str) -> HTTPException:
    """统一错误处理函数，打印详细错误并返回HTTPException"""
    error_detail = f"{str(e)}\n\nFull traceback:\n{traceback.format_exc()}"
    print(f"\n{'='*80}\n[ERROR] {endpoint_name} - Exception:\n{error_detail}\n{'='*80}\n", file=sys.stderr)
    return HTTPException(status_code=500, detail=error_detail)

# 配置日志
logger = logging.getLogger(__name__)

class NavigateRequest(BaseModel):
    target: str
    current_id: Optional[str] = None


def decode_node_id(encoded_id: str) -> str:
    """Decode URL-encoded node ID, preserving original characters like :: and /"""
    return unquote(encoded_id)


@router.get("/current")
async def get_current_node():
    """Get current node."""
    try:
        result = client.api.get_current_node()
        if not result.get("success"):
            raise HTTPException(status_code=404, detail=result.get("error", "No current node"))

        return result
    except HTTPException:
        raise
    except Exception as e:
        error_detail = f"{str(e)}\n\nFull traceback:\n{traceback.format_exc()}"
        logger.error(f"Error in get_current_node: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)


@router.post("/navigate")
async def navigate_to(target: str = Query(..., description="Target node ID"), current_id: Optional[str] = None):
    """Navigate to a node."""
    try:
        if current_id:
            # 如果有 current_id，先切换到该节点（此处可能需要处理返回结果，但保持逻辑简单）
            client.api.navigate_to(current_id)

        result = client.api.navigate_to(target)

        if not result.get("success"):
            error_msg = result.get("error", "Navigation failed")
            raise HTTPException(status_code=400, detail=error_msg)

        return result
    except HTTPException:
        raise
    except Exception as e:
        error_detail = f"{str(e)}\n\nFull traceback:\n{traceback.format_exc()}"
        logger.error(f"Error in navigate_to: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)


@router.post("/back")
async def go_back(steps: int = Query(1, ge=1)):
    """Go back in history."""
    try:
        result = client.api.navigate_back(steps)

        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))

        return result
    except HTTPException:
        raise
    except Exception as e:
        error_detail = f"{str(e)}\n\nFull traceback:\n{traceback.format_exc()}"
        logger.error(f"Error in go_back: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)


@router.post("/forward")
async def go_forward(steps: int = Query(1, ge=1)):
    """Go forward in history."""
    try:
        result = client.api.navigate_forward(steps)

        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))

        return result
    except HTTPException:
        raise
    except Exception as e:
        error_detail = f"{str(e)}\n\nFull traceback:\n{traceback.format_exc()}"
        logger.error(f"Error in go_forward: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)


@router.post("/up")
async def go_up(levels: int = Query(1, ge=1)):
    """Move up in hierarchy."""
    try:
        result = client.api.up(levels)

        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))

        return result
    except HTTPException:
        raise
    except Exception as e:
        error_detail = f"{str(e)}\n\nFull traceback:\n{traceback.format_exc()}"
        logger.error(f"Error in go_up: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)


@router.get("/resolve")
async def resolve_node_id(target: str = Query(..., description="Shorthand or index to resolve")):
    """Resolve shorthand ID to full node ID."""
    try:
        result = client.api.resolve_target_id(target)
        if not result.get("success"):
             raise HTTPException(status_code=400, detail=result.get("error", "Resolution failed"))
        return result
    except HTTPException:
        raise
    except Exception as e:
        error_detail = f"{str(e)}\n\nFull traceback:\n{traceback.format_exc()}"
        logger.error(f"Error in resolve_node_id: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)


@router.get("/detail")
async def get_node(
    node_id: str = Query(..., description="Node ID"),
    depth: int = Query(1, ge=0, le=5),
    include_content: bool = Query(True),
    include_see_also: bool = Query(True),
    format: str = Query("text", pattern="^(text|markdown|tree|json)$"),
    show_metadata: bool = Query(False),
    display_mode: str = Query("none", pattern="^(none|label|full_id)$")
):
    """Get node details."""
    full_node_id = decode_node_id(node_id)
    try:
        result = client.api.get_node_view(
            node_id=full_node_id,
            depth=depth,
            include_content=include_content,
            include_see_also=include_see_also,
            format=format,
            show_metadata=show_metadata,
            display_mode=display_mode
        )

        if not result.get("success"):
            raise HTTPException(status_code=404, detail=result.get("error"))

        return result
    except HTTPException:
        raise
    except Exception as e:
        error_detail = f"{str(e)}\n\nFull traceback:\n{traceback.format_exc()}"
        logger.error(f"Error in get_node: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)


@router.get("/children")
async def get_children(
    node_id: str = Query(..., description="Node ID")
):
    """Get children of a node."""
    full_node_id = decode_node_id(node_id)
    try:
        result = client.api.get_children(full_node_id)
        return result
    except Exception as e:
        error_detail = f"{str(e)}\n\nFull traceback:\n{traceback.format_exc()}"
        logger.error(f"Error in get_children: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)


@router.get("/preview_children")
async def preview_children(
    node_id: str = Query(..., description="Node ID"),
    node_type: str = Query("all", pattern="^(all|section|content)$"),
    sort_by: str = Query("order", pattern="^(order|title|label)$")
):
    """Get children of a node with preview information."""
    full_node_id = decode_node_id(node_id)
    try:
        result = client.api.preview_children(full_node_id, node_type, sort_by)
        return result
    except Exception as e:
        error_detail = f"{str(e)}\n\nFull traceback:\n{traceback.format_exc()}"
        logger.error(f"Error in preview_children: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)


@router.get("/breadcrumb")
async def get_breadcrumb(
    node_id: Optional[str] = Query(None, description="Node ID (optional)")
):
    """Get breadcrumb path."""
    try:
        # 如果提供了 node_id，API 目前不支持获取非当前位置的 breadcrumb，
        # 除非先导航过去。由于 API 有状态，我们保持现状。
        result = client.api.get_breadcrumb()
        return result
    except Exception as e:
        error_detail = f"{str(e)}\n\nFull traceback:\n{traceback.format_exc()}"
        logger.error(f"Error in get_breadcrumb: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)


@router.get("/history")
async def get_history():
    """Get navigation history."""
    try:
        result = client.api.get_history()
        return result
    except Exception as e:
        error_detail = f"{str(e)}\n\nFull traceback:\n{traceback.format_exc()}"
        logger.error(f"Error in get_history: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)
