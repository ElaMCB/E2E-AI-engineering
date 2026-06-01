"""Regression tests for generated monitor pages."""

from generate_html import generate_html_from_summaries
from generate_intelligence_page import generate_html_from_analysis


def test_monitor_page_blocks_scriptable_update_urls():
    html_output = generate_html_from_summaries(
        [
            {
                "date": "2026-04-20",
                "updates": [
                    {
                        "title": "Unsafe link",
                        "summary": "External feed supplied a script URL",
                        "source": "Feed",
                        "date": "2026-04-20",
                        "keywords": ["deepseek"],
                        "url": "javascript:alert(document.cookie)",
                    },
                    {
                        "title": "Safe link",
                        "summary": "Normal HTTP URL",
                        "source": "Feed",
                        "date": "2026-04-20",
                        "keywords": ["deepseek"],
                        "url": "https://example.com/update",
                    },
                ],
            }
        ]
    )

    assert 'href="javascript:alert(document.cookie)"' not in html_output
    assert 'href="https://example.com/update"' in html_output


def test_intelligence_chat_renders_messages_as_text():
    html_output = generate_html_from_analysis(
        {
            "date": "2026-04-20",
            "executive_summary": {"summary": "Weekly summary"},
            "top_insights": [
                {
                    "title": "<img src=x onerror=alert(1)>",
                    "description": "<script>alert(1)</script>",
                    "impact_score": 9,
                    "type": "breakthrough",
                    "evidence": ["Feed"],
                    "recommendations": [],
                }
            ],
            "significant_changes": [],
            "recommendations": [],
        }
    )

    assert "userBubble.textContent = question;" in html_output
    assert "agentBubble.textContent = response;" in html_output
    assert "${question}" not in html_output
    assert "${response}" not in html_output
    assert "<img src=x onerror=alert(1)>" not in html_output
    assert "<script>alert(1)</script>" not in html_output
