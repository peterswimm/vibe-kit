"""EventGuideActivityHandler bridging SDK message activities to domain logic.
Falls back gracefully when microsoft_agents SDK not installed.
"""

from __future__ import annotations
import time
from typing import Any, Dict

try:
    from microsoft_agents.hosting.core import TurnContext  # type: ignore

    HAVE_SDK = True
except ImportError:  # pragma: no cover - SDK absent
    HAVE_SDK = False
    TurnContext = object  # type: ignore

from .activities import RecommendActivity, ExplainActivity
from .integration_telemetry import StructuredTelemetry
from .storage import StorageFacade


class EventGuideActivityHandler:  # pragma: no cover - runtime depends on SDK
    def __init__(self):
        self.recommend_activity = RecommendActivity()
        self.explain_activity = ExplainActivity()
        self.telemetry = StructuredTelemetry()
        self.storage = StorageFacade()

    async def on_message_activity(self, turn_context: TurnContext):  # type: ignore[override]
        activity = getattr(turn_context, "activity", {}) if HAVE_SDK else {}
        value: Dict[str, Any] = getattr(activity, "value", {}) if HAVE_SDK else {}
        text = getattr(activity, "text", "") if HAVE_SDK else ""
        # Card action handling first (Adaptive Card Action.Submit payload)
        if (
            value
            and isinstance(value, dict)
            and value.get("action") == "explainSession"
        ):
            session_title = value.get("sessionTitle") or value.get("title") or ""
            user_id = getattr(getattr(activity, "from", {}), "id", None)

            # Auto-load interests from user profile
            interests = []
            profile_key = f"profile_{user_id}" if user_id else "default_profile"
            stored_interests = self.storage.get(profile_key)
            if isinstance(stored_interests, list):
                interests = [str(t) for t in stored_interests]

            start_ts = time.time()
            result = self.explain_activity.run(session_title, interests)
            result["profileUsed"] = profile_key if interests else None
            self.telemetry.log(
                "explainCardAction",
                {"session": session_title, "profileLoaded": bool(interests)},
                user_id=user_id,
                channel="teams" if HAVE_SDK else "local",
                start_ts=start_ts,
                success="error" not in result,
                error=result.get("error"),
            )
            await turn_context.send_activity(str(result))
            return
        if not text:
            await turn_context.send_activity(
                "Provide a command: recommend:<interests> or explain:<session>:<interests>"
            )
            return
        start_ts = time.time() if HAVE_SDK else None
        if text.startswith("recommend:"):
            interests_part = text.split(":", 1)[1]
            interests = [t.strip() for t in interests_part.split(",") if t.strip()]
            user_id = getattr(getattr(activity, "from", {}), "id", None)

            # Auto-save profile for user
            if interests and user_id:
                profile_key = f"profile_{user_id}"
                self.storage.set(profile_key, interests)

            result = self.recommend_activity.run(interests)
            self.telemetry.log(
                "recommend",
                {"sessions": len(result.get("sessions", []))},
                user_id=user_id,
                channel="teams" if HAVE_SDK else "local",
                start_ts=start_ts,
                success=True,
            )
            await turn_context.send_activity(str(result))
            return
        if text.startswith("explain:"):
            parts = text.split(":", 2)
            if len(parts) < 3:
                await turn_context.send_activity("Format explain:<session>:<interests>")
                return
            session_title = parts[1].strip()
            interests_part = parts[2].strip()
            interests = [t.strip() for t in interests_part.split(",") if t.strip()]
            result = self.explain_activity.run(session_title, interests)
            self.telemetry.log(
                "explain",
                {"session": session_title},
                user_id=getattr(getattr(activity, "from", {}), "id", None),
                channel="teams" if HAVE_SDK else "local",
                start_ts=start_ts,
                success="error" not in result,
                error=result.get("error"),
            )
            await turn_context.send_activity(str(result))
            return
        await turn_context.send_activity(
            "Commands: recommend:<interests> | explain:<session>:<interests>"
        )
