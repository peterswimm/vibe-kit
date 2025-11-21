from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Any, Dict


class TelemetryLogger:
    def __init__(self, path: str = "telemetry.jsonl"):
        self.path = Path(path)

    def log(self, event_type: str, payload: Dict[str, Any]) -> None:
        record = {
            "ts": time.time(),
            "type": event_type,
            "payload": payload,
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
