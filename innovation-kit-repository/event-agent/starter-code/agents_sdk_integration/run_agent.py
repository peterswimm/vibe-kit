#!/usr/bin/env python3
"""Run the Event Guide Agent using Microsoft Agents SDK if available, else fallback CLI.
Usage (SDK):
  python run_agent.py --mode sdk
Usage (fallback):
  python run_agent.py recommend --interests "AI safety, agents" --max-sessions 3
"""

from __future__ import annotations
import argparse
import json
import sys
import pathlib
import hashlib
from typing import List

# Ensure parent directories are on sys.path for absolute imports during direct execution
_here = pathlib.Path(__file__).resolve().parent
_starter_code = _here.parent  # directory containing event_agent package
sys.path.insert(0, str(_here))
sys.path.insert(0, str(_starter_code))

try:
    from microsoft_agents.hosting.aiohttp import start_agent_process  # type: ignore
    from microsoft_agents.hosting.core import TurnContext  # type: ignore

    HAVE_SDK = True
except ImportError:
    HAVE_SDK = False

try:
    from .activities import RecommendActivity, ExplainActivity  # type: ignore
except ImportError:
    # Fallback when executed as a plain script without package context
    from activities import RecommendActivity, ExplainActivity  # type: ignore


def parse_args():
    p = argparse.ArgumentParser(description="Event Guide Agent Runner")
    sub = p.add_subparsers(dest="command")

    sdk = sub.add_parser("sdk", help="Run SDK hosting (aiohttp)")
    sdk.add_argument("--port", type=int, default=3978)

    rec = sub.add_parser("recommend", help="Recommend sessions")
    rec.add_argument(
        "--interests",
        required=False,
        help="Comma separated interests; optional if --profile-load provided",
    )
    rec.add_argument("--max-sessions", type=int, default=3)
    rec.add_argument(
        "--profile-load", help="Profile key to load interests from storage"
    )
    rec.add_argument(
        "--profile-save", help="Save provided interests under this profile key"
    )
    rec.add_argument(
        "--test-token",
        action="store_true",
        help="Attempt MSAL token acquisition and print summary",
    )
    rec.add_argument(
        "--publish",
        action="store_true",
        help="Publish itinerary to SharePoint (requires ENABLE_SHAREPOINT_PUBLISH)",
    )

    exp = sub.add_parser("explain", help="Explain session score")
    exp.add_argument("--session", required=True)
    exp.add_argument(
        "--interests",
        required=False,
        help="Comma separated interests; optional if --profile-load provided",
    )
    exp.add_argument(
        "--profile-load", help="Profile key to load interests from storage"
    )
    exp.add_argument(
        "--test-token",
        action="store_true",
        help="Attempt MSAL token acquisition and print summary",
    )
    return p.parse_args()


def run_sdk(port: int):  # pragma: no cover - requires SDK
    if not HAVE_SDK:
        print("SDK packages not available; install microsoft-agents-* to enable.")
        return
    try:
        from aiohttp import web  # type: ignore
    except Exception as e:  # noqa: BLE001
        print(f"Unable to import aiohttp: {e}")
        return
    # Lightweight local hosting wrapper (does not yet use CloudAdapter due to additional
    # connection/token requirements). It simulates a TurnContext sufficient for our
    # EventGuideActivityHandler to process 'recommend:' and 'explain:' messages.
    try:
        from event_handler import EventGuideActivityHandler  # type: ignore
    except ImportError:
        try:
            from .event_handler import EventGuideActivityHandler  # type: ignore
        except ImportError as e:  # noqa: BLE001
            print(f"Could not import EventGuideActivityHandler: {e}")
            return
    handler = EventGuideActivityHandler()

    class FakeTurnContext:  # pragma: no cover - simple adapter shim
        def __init__(self, activity):
            self.activity = activity
            self._response = None

        async def send_activity(self, message):  # handler expects awaited call
            if isinstance(message, str):
                try:
                    self._response = json.loads(message)
                except Exception:  # noqa: BLE001
                    self._response = {"text": message}
            else:
                self._response = message

    async def messages(request):  # type: ignore
        data = await request.json()

        # Build minimal activity object with 'text' and optional 'value'
        class ActivityObj:  # noqa: D401 - simple container
            pass

        activity = ActivityObj()
        for k, v in data.items():
            setattr(activity, k, v)
        tc = FakeTurnContext(activity)
        await handler.on_message_activity(tc)
        return web.json_response(tc._response or {"status": "no response"})

    app = web.Application()
    app.router.add_post("/api/messages", messages)
    print(
        f"Starting lightweight Event Guide server on port {port} (POST /api/messages)"
    )
    print("Example recommend:")
    print(
        f"curl -X POST http://localhost:{port}/api/messages -H 'Content-Type: application/json' -d '{{\"text\":\"recommend:AI safety, agents\"}}'"
    )
    web.run_app(app, port=port)


def _try_token():
    try:
        from auth import MsalClientCredentials  # type: ignore

        client = MsalClientCredentials()
        token = client.acquire_token()
        return {
            "tokenPreview": token[:32] + "...",
            "length": len(token),
        }
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}


def main():
    args = parse_args()
    if args.command == "sdk":
        run_sdk(args.port)
        return

    if args.command == "recommend":
        from storage import StorageFacade  # type: ignore

        interests: List[str] = []
        storage = StorageFacade()
        if args.profile_load:
            loaded = storage.get(args.profile_load)
            if isinstance(loaded, list):
                interests = [str(x) for x in loaded]
        if not interests and args.interests:
            norm = args.interests.replace(";", ",")
            interests = [t.strip() for t in norm.split(",") if t.strip()]
        if not interests:
            print(
                "No interests provided or loaded; supply --interests or --profile-load"
            )
            return
        activity = RecommendActivity(publish_itinerary=args.publish)
        result = activity.run(interests, args.max_sessions)
        if args.profile_save:
            storage.set(args.profile_save, interests)
            result["profileSaved"] = args.profile_save
        if args.test_token:
            token_info = _try_token()
            result["auth"] = token_info
        print(json.dumps(result, indent=2))
        return

    if args.command == "explain":
        from storage import StorageFacade  # type: ignore

        storage = StorageFacade()
        interests: List[str] = []
        if args.profile_load:
            loaded = storage.get(args.profile_load)
            if isinstance(loaded, list):
                interests = [str(x) for x in loaded]
        if not interests and args.interests:
            norm = args.interests.replace(";", ",")
            interests = [t.strip() for t in norm.split(",") if t.strip()]
        if not interests:
            print(
                "No interests provided or loaded; supply --interests or --profile-load"
            )
            return
        result = ExplainActivity().run(args.session, interests)
        if args.test_token:
            result["auth"] = _try_token()
        print(json.dumps(result, indent=2))
        return

    print("No command provided. Use one of: sdk, recommend, explain")


if __name__ == "__main__":
    main()
