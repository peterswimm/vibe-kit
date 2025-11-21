"""Structured telemetry logger for SDK integration.
Adds channel, user_hash, latency, action fields.
"""

from __future__ import annotations
import json
import time
import hashlib
from pathlib import Path
from typing import Any, Dict


class StructuredTelemetry:
    def __init__(self, path: str = "integration_telemetry.jsonl"):
        self.path = Path(path)

    def _hash_user(self, user_id: str | None) -> str:
        if not user_id:
            return "anon"
        return hashlib.sha256(user_id.encode("utf-8")).hexdigest()[:16]

    def log(
        self,
        action: str,
        payload: Dict[str, Any],
        user_id: str | None = None,
        channel: str | None = None,
        start_ts: float | None = None,
        success: bool | None = None,
        error: str | None = None,
    ) -> None:
        record = {
            "ts": time.time(),
            "action": action,
            "channel": channel or "local",
            "user": self._hash_user(user_id),
            "latency_ms": int((time.time() - start_ts) * 1000) if start_ts else None,
            "payload": payload,
            "success": success,
            "error": error,
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
