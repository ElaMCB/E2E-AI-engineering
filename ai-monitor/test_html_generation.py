import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from generate_html import generate_html_from_summaries
from generate_intelligence_page import generate_html_from_analysis


def test_monitor_html_rejects_scriptable_update_urls():
    summaries = [
        {
            "date": "2026-07-10",
            "updates": [
                {
                    "title": "Malicious link",
                    "summary": "Poisoned feed item",
                    "source": "Feed",
                    "date": "2026-07-10",
                    "keywords": ["deepseek"],
                    "url": "javascript:alert(1)",
                }
            ],
        }
    ]

    html = generate_html_from_summaries(summaries)

    assert "javascript:alert" not in html
    assert 'href="#"' in html


def test_intelligence_chat_uses_text_content_for_dynamic_messages():
    analysis = {
        "date": "2026-07-10",
        "executive_summary": {"summary": "Summary"},
        "top_insights": [
            {
                "title": "<img src=x onerror=alert(1)>",
                "description": "<script>alert(1)</script>",
                "impact_score": 9.0,
                "type": "release",
                "evidence": ["feed"],
            }
        ],
        "significant_changes": [],
        "recommendations": [],
    }

    html = generate_html_from_analysis(analysis)

    assert "textContent = message" in html
    assert "${question}" not in html
    assert "${response}" not in html
    assert "<img src=x onerror=alert(1)>" not in html
    assert "<script>alert(1)</script>" not in html
