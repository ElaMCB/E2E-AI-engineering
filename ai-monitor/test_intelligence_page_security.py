import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent))

from generate_intelligence_page import generate_html_from_analysis


def test_agent_chat_uses_text_content_for_dynamic_messages():
    html = generate_html_from_analysis(
        {
            "date": "2026-06-29",
            "executive_summary": {"summary": "Summary"},
            "top_insights": [
                {
                    "title": '<img src=x onerror="alert(1)">',
                    "description": '<script>alert("stored")</script>',
                    "impact_score": 9,
                    "type": "security",
                    "evidence": ["rss"],
                }
            ],
            "significant_changes": [],
            "recommendations": [],
        }
    )

    assert "paragraph.textContent = text;" in html
    assert "${question}" not in html
    assert "${response}" not in html
    assert '<img src=x onerror="alert(1)">' not in html
    assert '<script>alert("stored")</script>' not in html
    assert "&lt;img src=x" in html
    assert "&lt;script&gt;alert" in html
