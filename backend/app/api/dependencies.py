"""API dependencies."""

from typing import Optional
from fastapi import Header, HTTPException
from ...core.kerag_client import client


async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Verify API key (placeholder for future auth)."""
    # TODO: Implement actual API key verification
    # if x_api_key != "expected_api_key":
    #     raise HTTPException(status_code=401, detail="Invalid API key")
    pass


def get_kerag_client():
    """Get KERAG client instance."""
    return client
