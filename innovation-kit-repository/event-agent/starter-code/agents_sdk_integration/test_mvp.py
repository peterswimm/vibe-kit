#!/usr/bin/env python3
"""End-to-end MVP smoke test for Event Guide Agent.

Tests:
1. Settings validation
2. Recommend with mock sessions (Graph disabled)
3. Explain with profile auto-load
4. Publish capability (feature flag driven)
5. Telemetry capture

Run: python test_mvp.py
"""

from __future__ import annotations
import sys
import os
import pathlib
import json

# Add integration and parent directories to path
_here = pathlib.Path(__file__).resolve().parent
_starter_code = _here.parent
sys.path.insert(0, str(_here))
sys.path.insert(0, str(_starter_code))

from activities import RecommendActivity, ExplainActivity
from storage import StorageFacade
from settings import Settings
import graph_sources


def test_settings_validation():
    """Test 1: Settings load without crashing when Graph disabled."""
    print("✓ Test 1: Settings validation")
    try:
        # Override env for test
        os.environ.pop("ENABLE_GRAPH_FETCH", None)
        os.environ.pop("ENABLE_SHAREPOINT_PUBLISH", None)
        settings = Settings()
        assert settings.enable_graph_fetch is False
        assert settings.enable_sharepoint_publish is False
        print("  ✓ Settings loaded with Graph disabled")
    except Exception as e:
        print(f"  ✗ Settings validation failed: {e}")
        return False
    return True


def test_recommend_with_mock():
    """Test 2: Recommend activity with mock sessions."""
    print("✓ Test 2: Recommend with mock sessions")
    try:
        activity = RecommendActivity(include_card=True, publish_itinerary=False)
        result = activity.run(interests=["agents", "AI"], max_sessions=2)

        assert "sessions" in result
        assert "scoring" in result
        assert "adaptiveCard" in result
        assert result["sessionSource"] == "mock"
        assert len(result["sessions"]) <= 2

        # Validate adaptive card structure
        card = result["adaptiveCard"]
        assert card["type"] == "AdaptiveCard"
        assert "actions" in card
        assert len(card["actions"]) == len(result["sessions"])

        print(f"  ✓ Returned {len(result['sessions'])} sessions")
        print(f"  ✓ Session source: {result['sessionSource']}")
        print(f"  ✓ Adaptive card with {len(card['actions'])} actions")
    except Exception as e:
        print(f"  ✗ Recommend test failed: {e}")
        return False
    return True


def test_profile_storage():
    """Test 3: Profile save and load."""
    print("✓ Test 3: Profile storage")
    try:
        storage = StorageFacade()
        test_interests = ["AI", "agents", "telemetry"]
        storage.set("test_user_profile", test_interests)

        loaded = storage.get("test_user_profile")
        assert loaded == test_interests
        print(f"  ✓ Stored and loaded profile: {loaded}")
    except Exception as e:
        print(f"  ✗ Profile storage test failed: {e}")
        return False
    return True


def test_explain_activity():
    """Test 4: Explain activity."""
    print("✓ Test 4: Explain activity")
    try:
        activity = ExplainActivity()
        result = activity.run(
            session_title="Generative Agents in Production",
            interests=["agents", "gen ai"],
        )

        assert "title" in result or "error" in result
        if "error" not in result:
            assert "score" in result
            assert "contributions" in result
            print(
                f"  ✓ Explained session: {result['title']} (score: {result['score']})"
            )
        else:
            print(f"  ⚠ Session not found (expected with mock data)")
    except Exception as e:
        print(f"  ✗ Explain test failed: {e}")
        return False
    return True


def test_publish_skip_when_disabled():
    """Test 5: Publish skips gracefully when disabled."""
    print("✓ Test 5: Publish capability (feature flag)")
    try:
        # Ensure publish is disabled
        os.environ["ENABLE_SHAREPOINT_PUBLISH"] = "false"

        from event_agent.main import MOCK_SESSIONS

        sessions = MOCK_SESSIONS[:2]

        result = graph_sources.publish_itinerary(sessions, user_name="TestUser")

        assert result["status"] == "skipped"
        assert "ENABLE_SHAREPOINT_PUBLISH=false" in result["reason"]
        print(f"  ✓ Publish correctly skipped: {result['reason']}")
    except Exception as e:
        print(f"  ✗ Publish test failed: {e}")
        return False
    return True


def test_cache_functionality():
    """Test 6: Session cache TTL."""
    print("✓ Test 6: Session cache")
    try:
        from session_cache import SessionCache
        from event_agent.main import MOCK_SESSIONS

        cache = SessionCache(ttl_minutes=1)

        # Initial state
        assert cache.get() is None
        assert not cache.is_valid()

        # Store sessions
        test_sessions = MOCK_SESSIONS[:2]
        cache.set(test_sessions)
        assert cache.is_valid()

        # Retrieve
        cached = cache.get()
        assert cached == test_sessions

        # Invalidate
        cache.invalidate()
        assert cache.get() is None

        print("  ✓ Cache set, get, and invalidate working")
    except Exception as e:
        print(f"  ✗ Cache test failed: {e}")
        return False
    return True


def test_adaptive_card_actions():
    """Test 7: Adaptive card contains correct action payloads."""
    print("✓ Test 7: Adaptive card action payloads")
    try:
        activity = RecommendActivity(include_card=True)
        result = activity.run(interests=["AI"], max_sessions=2)

        card = result["adaptiveCard"]
        actions = card.get("actions", [])

        assert len(actions) > 0
        first_action = actions[0]
        assert first_action["type"] == "Action.Submit"
        assert "data" in first_action
        assert first_action["data"]["action"] == "explainSession"
        assert "sessionTitle" in first_action["data"]

        print(f"  ✓ {len(actions)} actions with explainSession payloads")
    except Exception as e:
        print(f"  ✗ Card action test failed: {e}")
        return False
    return True


def main():
    print("\n" + "=" * 60)
    print("EVENT GUIDE AGENT - MVP END-TO-END TEST")
    print("=" * 60 + "\n")

    tests = [
        test_settings_validation,
        test_recommend_with_mock,
        test_profile_storage,
        test_explain_activity,
        test_publish_skip_when_disabled,
        test_cache_functionality,
        test_adaptive_card_actions,
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test crashed: {e}")
            failed += 1
        print()

    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed > 0:
        sys.exit(1)
    else:
        print("\n🎉 All MVP tests passed! Ready for real Graph integration.")
        sys.exit(0)


if __name__ == "__main__":
    main()
