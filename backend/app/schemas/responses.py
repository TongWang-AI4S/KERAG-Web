"""Response schemas for the KERAG Web API."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    """Base response model for all API responses."""
    success: bool
    message: Optional[str] = None
    error: Optional[Dict[str, str]] = None


class ModuleInfo(BaseModel):
    """Module information."""
    name: str
    loaded: bool
    file_count: int = 0


class NodeInfo(BaseModel):
    """Basic node information."""
    id: str
    label: str
    type: str
    title: Optional[str] = None
    has_children: bool = False


class NodeDetail(NodeInfo):
    """Detailed node information."""
    content: Optional[str] = None
    module: Optional[str] = None
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    parent_id: Optional[str] = None
    children_ids: List[str] = Field(default_factory=list)
    see_also: List[Dict[str, str]] = Field(default_factory=list)


class BreadcrumbItem(BaseModel):
    """Breadcrumb navigation item."""
    id: str
    label: str


class FormattedContent(BaseModel):
    """Content in different formats."""
    markdown: Optional[str] = None
    text: Optional[str] = None
    tree: Optional[str] = None
    json_data: Optional[Dict[str, Any]] = None


class NodeView(BaseModel):
    """Complete node view with content."""
    node: NodeDetail
    formatted_content: FormattedContent


class SearchResult(BaseModel):
    """Search result item."""
    id: str
    label: str
    title: Optional[str] = None
    type: str
    module: Optional[str] = None
    score: float = 0.0
    highlights: List[Dict[str, str]] = Field(default_factory=list)


# API Response Models

class ModuleListResponse(BaseResponse):
    """Response for module list API."""
    data: Dict[str, List]


class ModuleOperationResponse(BaseResponse):
    """Response for module load/unload operations."""
    data: Dict[str, Any]


class NodeResponse(BaseResponse):
    """Response for node operations."""
    data: Dict[str, Optional[NodeDetail]]


class NodeViewResponse(BaseResponse):
    """Response for node view operations."""
    data: Dict[str, Optional[NodeView]]


class ChildrenResponse(BaseResponse):
    """Response for children list operations."""
    data: Dict[str, List[NodeInfo]]


class BreadcrumbResponse(BaseResponse):
    """Response for breadcrumb operations."""
    data: Dict[str, List[BreadcrumbItem]]


class SearchResponse(BaseResponse):
    """Response for search operations."""
    data: Dict[str, Any]


class SystemStatusResponse(BaseResponse):
    """Response for system status."""
    data: Dict[str, Any]
