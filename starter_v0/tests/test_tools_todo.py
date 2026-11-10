"""TODO CP3 (student): Tool Unit Test Challenge.

The starter challenge marks unfinished tests with `pytest.skip(...)`.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- The bonus challenge is complete when `pytest tests/ -v` shows 0 skipped and 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401
from tools.compare_sources.tool import compare_sources

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    # Call clarify with response_type="choice" and 2 options.
    # Assert: options are returned unchanged, awaiting_user is True.
    pytest.skip(TODO)


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    # Items with section "A", "B", "A" -> markdown has exactly one "## A" and one "## B".
    pytest.skip(TODO)


def test_format_thread_numbers_items() -> None:
    # template="thread" -> lines start with "1/", "2/", ...
    pytest.skip(TODO)


def test_format_empty_items_does_not_crash() -> None:
    # items=None and items=[] -> item_count == 0, no exception.
    pytest.skip(TODO)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    # Set TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, mock HTTP.
    # Assert: exactly one POST, URL contains the token, json has chat_id + text, status == "sent".
    pytest.skip(TODO)


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    pytest.skip(TODO)


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    # timeframe=None -> request body has no "time_range" key.
    pytest.skip(TODO)


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    # Mock {"data": {"markdown": "...", "metadata": {"title": "T", "sourceURL": "https://..."}}}
    # Assert title/url/source/summary in result["items"][0].
    pytest.skip(TODO)


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    pytest.skip(TODO)


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    # Mock {"timeline": [...]} with 1 item missing tweet_id and 6 valid items, limit=3.
    # Assert 3 items, and each url looks like https://x.com/<handle>/status/<id>.
    pytest.skip(TODO)


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    # Assert the request params carry the query and search_type ("Top" / "Latest").
    pytest.skip(TODO)


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    pytest.skip(TODO)


def test_policy_area_filter_only_returns_that_area() -> None:
    # policy_area="data_privacy" -> every result has policy_area == "data_privacy".
    pytest.skip(TODO)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    pytest.skip(TODO)


# ---------------- YOUR NEW TOOL(S) ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

def test_compare_sources_groups_urls_by_normalized_domain() -> None:
    result = compare_sources([
        " https://WWW.example.com/a ",
        "https://example.org/b",
        "https://example.com:443/c",
        "https://WWW.example.com/a",
    ])

    assert result == {
        "tool": "compare_sources",
        "domain_count": 2,
        "url_count": 3,
        "groups": [
            {"domain": "example.com", "urls": ["https://WWW.example.com/a", "https://example.com:443/c"]},
            {"domain": "example.org", "urls": ["https://example.org/b"]},
        ],
    }


@pytest.mark.parametrize("urls", [None, [], "https://example.com"])
def test_compare_sources_rejects_missing_or_non_list_input(urls) -> None:
    assert compare_sources(urls) == {
        "tool": "compare_sources",
        "error": "ValueError",
        "message": "urls must be a non-empty list of URL strings",
    }


@pytest.mark.parametrize("value", [42, " "])
def test_compare_sources_rejects_invalid_list_item(value) -> None:
    assert compare_sources([value]) == {
        "tool": "compare_sources",
        "error": "ValueError",
        "message": "urls[0] must be a non-empty string",
    }


@pytest.mark.parametrize("url", ["example.com/path", "ftp://example.com/a", "https://exa mple.com"])
def test_compare_sources_rejects_unsupported_url(url) -> None:
    assert compare_sources(["https://example.com", url]) == {
        "tool": "compare_sources",
        "error": "ValueError",
        "message": "urls[1] must be an absolute HTTP or HTTPS URL",
    }


@pytest.mark.parametrize("url", [
    "https://[bad-host",
    "https://example.com:abc/a",
    "https://example.com:65536/a",
])
def test_compare_sources_returns_error_for_malformed_host_or_port(url) -> None:
    assert compare_sources([url]) == {
        "tool": "compare_sources",
        "error": "ValueError",
        "message": "urls[0] has a malformed host or port",
    }
