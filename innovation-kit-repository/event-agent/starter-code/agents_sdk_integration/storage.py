"""Storage provider scaffold for Event Guide.
Implements in-memory storage and optional Azure Blob backend.
"""

from __future__ import annotations
from typing import Optional, Dict, Any
import json
import os

try:
    from azure.storage.blob import BlobServiceClient  # type: ignore

    HAVE_BLOB = True
except ImportError:  # pragma: no cover
    HAVE_BLOB = False


class InMemoryStorage:
    def __init__(self):
        self._store: Dict[str, Any] = {}

    def get(self, key: str) -> Any:
        return self._store.get(key)

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value


class BlobStorageProvider:
    def __init__(
        self, container: str = "event-guide", connection_string: Optional[str] = None
    ):
        if not HAVE_BLOB:
            raise RuntimeError("azure-storage-blob not installed")
        conn = connection_string or os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        if not conn:
            raise RuntimeError("Missing AZURE_STORAGE_CONNECTION_STRING")
        self.client = BlobServiceClient.from_connection_string(conn)
        self.container_client = self.client.get_container_client(container)
        try:
            self.container_client.create_container()
        except Exception:
            pass  # already exists

    def get(self, key: str) -> Any:
        blob = self.container_client.get_blob_client(f"{key}.json")
        if not blob.exists():
            return None
        data = blob.download_blob().readall().decode("utf-8")
        return json.loads(data)

    def set(self, key: str, value: Any) -> None:
        blob = self.container_client.get_blob_client(f"{key}.json")
        blob.upload_blob(json.dumps(value), overwrite=True)


class FileStorageProvider:
    def __init__(self, file_path: Optional[str] = None):
        # Default path inside user home for persistence across repo resets
        default_name = ".event_guide_storage.json"
        self.file_path = (
            file_path
            or os.getenv("EVENT_GUIDE_STORAGE_FILE")
            or os.path.join(os.path.expanduser("~"), default_name)
        )
        self._store: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self._store = json.load(f)
            except Exception:
                # Corrupted file; start fresh
                self._store = {}

    def _flush(self) -> None:
        tmp_path = self.file_path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(self._store, f)
        os.replace(tmp_path, self.file_path)

    def get(self, key: str) -> Any:
        return self._store.get(key)

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value
        self._flush()


class StorageFacade:
    def __init__(self):
        if HAVE_BLOB and os.getenv("AZURE_STORAGE_CONNECTION_STRING"):
            # Use Azure Blob when configured
            self.backend = BlobStorageProvider()
        else:
            # File persistence fallback (survives process restarts)
            self.backend = FileStorageProvider()

    def get(self, key: str) -> Any:
        return self.backend.get(key)

    def set(self, key: str, value: Any) -> None:
        self.backend.set(key, value)
