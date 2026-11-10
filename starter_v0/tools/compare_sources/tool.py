from __future__ import annotations

from typing import Any
from urllib.parse import urlsplit

from tools._shared import err


def compare_sources(urls: list[str] | None = None) -> dict[str, Any]:
    """Group collected research URLs by hostname without fetching them."""
    tool = "compare_sources"
    if not isinstance(urls, list) or not urls:
        return err(tool, ValueError("urls must be a non-empty list of URL strings"))

    groups: dict[str, list[str]] = {}
    seen: set[str] = set()
    for index, value in enumerate(urls):
        if not isinstance(value, str) or not value.strip():
            return err(tool, ValueError(f"urls[{index}] must be a non-empty string"))

        url = value.strip()
        try:
            parts = urlsplit(url)
            _ = parts.port  # urlsplit validates the port only when it is accessed.
        except ValueError:
            return err(tool, ValueError(f"urls[{index}] has a malformed host or port"))

        hostname = (parts.hostname or "").removeprefix("www.")
        if not hostname or parts.scheme not in {"http", "https"} or any(char.isspace() for char in url):
            return err(tool, ValueError(f"urls[{index}] must be an absolute HTTP or HTTPS URL"))

        if url in seen:
            continue
        seen.add(url)
        groups.setdefault(hostname, []).append(url)

    return {
        "tool": tool,
        "domain_count": len(groups),
        "url_count": len(seen),
        "groups": [{"domain": hostname, "urls": links} for hostname, links in groups.items()],
    }
