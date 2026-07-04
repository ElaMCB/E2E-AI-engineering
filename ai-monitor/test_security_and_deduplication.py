"""
Regression tests for monitor publishing security and deduplication state.
"""

import json
from pathlib import Path

from generate_html import generate_html_from_summaries, sanitize_href
from generate_intelligence_page import generate_html_from_analysis
from monitor import AIMonitor


def test_sanitize_href_allows_only_http_urls():
    assert sanitize_href("https://example.com/a?b=1&c=2") == "https://example.com/a?b=1&amp;c=2"
    assert sanitize_href("http://example.com/path") == "http://example.com/path"
    assert sanitize_href("javascript:alert(1)") == "#"
    assert sanitize_href("data:text/html,<script>alert(1)</script>") == "#"
    assert sanitize_href("//example.com/path") == "#"


def test_generated_monitor_page_drops_scriptable_update_urls():
    html = generate_html_from_summaries(
        [
            {
                "date": "2026-04-20",
                "updates": [
                    {
                        "title": "Malicious update",
                        "summary": "Looks relevant",
                        "source": "RSS",
                        "date": "2026-04-20",
                        "keywords": ["deepseek"],
                        "url": "javascript:alert(document.cookie)",
                    }
                ],
            }
        ]
    )

    assert "javascript:alert" not in html
    assert 'href="#"' in html


def test_intelligence_chat_renders_dynamic_text_with_text_content():
    html = generate_html_from_analysis(
        {
            "date": "2026-04-20",
            "executive_summary": {"summary": "Summary"},
            "top_insights": [
                {
                    "title": "<img src=x onerror=alert(1)>",
                    "description": "<script>alert(1)</script>",
                    "impact_score": 9,
                    "type": "trend",
                    "confidence": 0.8,
                    "evidence": ["feed"],
                }
            ],
            "significant_changes": [],
            "recommendations": [],
        }
    )

    assert "textContent = question" in html
    assert "textContent = response" in html
    assert "${question}" not in html
    assert "${response}" not in html


def test_seen_hashes_backfill_from_weekly_summary(tmp_path, monkeypatch):
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    with open(results_dir / "weekly_summary.json", "w", encoding="utf-8") as f:
        json.dump(
            [
                {
                    "date": "2026-04-13",
                    "updates": [
                        {"hash": "hash-b"},
                        {"hash": ""},
                    ],
                },
                {
                    "date": "2026-04-20",
                    "updates": [
                        {"hash": "hash-a"},
                    ],
                },
            ],
            f,
        )

    monkeypatch.chdir(tmp_path)
    Path("config.json").write_text("{}", encoding="utf-8")
    monitor = AIMonitor()

    assert monitor.seen_hashes == {"hash-a", "hash-b"}

    monitor._save_seen_hashes()
    with open(results_dir / "seen_hashes.json", "r", encoding="utf-8") as f:
        assert json.load(f) == ["hash-a", "hash-b"]
