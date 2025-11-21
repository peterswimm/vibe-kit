"""Centralized configuration with Pydantic for Event Guide Agent.

Validates environment variables on startup and provides feature flags.
Fails fast with clear error messages when required config is missing.
"""

from __future__ import annotations
from typing import Optional
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
import sys


class Settings(BaseSettings):
    """Event Guide Agent configuration from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Microsoft Graph / Azure AD
    graph_tenant_id: Optional[str] = Field(default=None, alias="GRAPH_TENANT_ID")
    graph_client_id: Optional[str] = Field(default=None, alias="GRAPH_CLIENT_ID")
    graph_client_secret: Optional[str] = Field(
        default=None, alias="GRAPH_CLIENT_SECRET"
    )

    # Storage
    azure_storage_connection_string: Optional[str] = Field(
        default=None, alias="AZURE_STORAGE_CONNECTION_STRING"
    )
    event_guide_storage_file: Optional[str] = Field(
        default=None, alias="EVENT_GUIDE_STORAGE_FILE"
    )

    # Feature Flags
    enable_graph_fetch: bool = Field(default=False, alias="ENABLE_GRAPH_FETCH")
    enable_sharepoint_publish: bool = Field(
        default=False, alias="ENABLE_SHAREPOINT_PUBLISH"
    )
    enable_session_cache: bool = Field(default=True, alias="ENABLE_SESSION_CACHE")
    session_cache_ttl_minutes: int = Field(
        default=15, alias="SESSION_CACHE_TTL_MINUTES"
    )

    # Graph Data Sources (optional, for flexible backend selection)
    graph_calendar_id: Optional[str] = Field(default=None, alias="GRAPH_CALENDAR_ID")
    sharepoint_site_id: Optional[str] = Field(default=None, alias="SHAREPOINT_SITE_ID")
    sharepoint_list_id: Optional[str] = Field(default=None, alias="SHAREPOINT_LIST_ID")

    # Telemetry
    telemetry_file: str = Field(
        default="integration_telemetry.jsonl", alias="TELEMETRY_FILE"
    )

    # SDK Hosting
    agent_port: int = Field(default=3978, alias="AGENT_PORT")

    def graph_enabled(self) -> bool:
        """Check if all required Graph credentials are present."""
        return bool(
            self.graph_tenant_id and self.graph_client_id and self.graph_client_secret
        )

    def validate_for_graph_fetch(self) -> None:
        """Raise if graph fetch enabled but credentials missing."""
        if self.enable_graph_fetch and not self.graph_enabled():
            raise ValueError(
                "ENABLE_GRAPH_FETCH=true requires GRAPH_TENANT_ID, GRAPH_CLIENT_ID, "
                "and GRAPH_CLIENT_SECRET to be set."
            )

    def validate_for_sharepoint_publish(self) -> None:
        """Raise if SharePoint publish enabled but site ID missing."""
        if self.enable_sharepoint_publish:
            if not self.graph_enabled():
                raise ValueError(
                    "ENABLE_SHAREPOINT_PUBLISH=true requires GRAPH_TENANT_ID, GRAPH_CLIENT_ID, "
                    "and GRAPH_CLIENT_SECRET."
                )
            if not self.sharepoint_site_id:
                raise ValueError(
                    "ENABLE_SHAREPOINT_PUBLISH=true requires SHAREPOINT_SITE_ID."
                )


def load_settings() -> Settings:
    """Load and validate settings; exit with helpful message on failure."""
    try:
        settings = Settings()
        settings.validate_for_graph_fetch()
        settings.validate_for_sharepoint_publish()
        return settings
    except ValidationError as e:
        print("❌ Configuration validation failed:", file=sys.stderr)
        for error in e.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            print(f"  - {field}: {error['msg']}", file=sys.stderr)
        print("\nSet required environment variables and try again.", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Configuration error: {e}", file=sys.stderr)
        sys.exit(1)


# Global singleton for easy import
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Lazy-load global settings instance."""
    global _settings
    if _settings is None:
        _settings = load_settings()
    return _settings
