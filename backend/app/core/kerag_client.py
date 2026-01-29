"""KERAG API client for the web backend."""

import sys
from pathlib import Path

# Add KERAG root to path to import kerag
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from kerag.api import KERAGAPI


class KERAGClient:
    """Singleton wrapper for KERAG API instance."""

    _instance = None
    _api = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def init_api(self, local_root: str = None, global_root: str = None, lang: str = None):
        """Initialize KERAG API with root path."""
        if self._api is None:
            self._api = KERAGAPI(local_root, global_root, lang)
        return self._api

    @property
    def api(self) -> KERAGAPI:
        """Get the API instance."""
        if self._api is None:
            raise RuntimeError("KERAG API not initialized. Call init_api() first.")
        return self._api


# Global client instance
client = KERAGClient()
