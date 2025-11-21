from __future__ import annotations
from typing import List
from .models import Session


class SharePointAuthor:
    def __init__(self, site_url: str | None = None):
        self.site_url = site_url or "https://contoso.sharepoint.com/sites/events"

    def create_page_stub(self, sessions: List[Session]) -> str:
        lines = ["SharePoint Page: My Event Picks"]
        for s in sessions:
            lines.append(f" - {s.title} ({s.start}-{s.end}) @ {s.location}")
        lines.append("(Integrate with SharePoint REST API to publish.)")
        return "\n".join(lines)
