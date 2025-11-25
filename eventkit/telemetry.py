import json, time, pathlib
from typing import Any, Dict


class Telemetry:
    def __init__(self, file: str):
        self.path = pathlib.Path(file)

    def log(
        self,
        action: str,
        payload: Dict[str, Any],
        start_ts: float,
        success: bool,
        error: str | None = None,
    ):
        entry = {
            "ts": time.time(),
            "action": action,
            "success": success,
            "error": error,
            "latency_ms": (time.time() - start_ts) * 1000,
            "payload": {
                k: v for k, v in payload.items() if k in {"sessions", "title", "score"}
            },
        }
        try:
            with self.path.open("a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass


def get_telemetry(manifest):  # pragma: no cover
    feat = manifest.get("features", {}).get("telemetry", {})
    if not feat.get("enabled"):
        return None
    return Telemetry(feat.get("file", "telemetry.jsonl"))
