"""
Security regressions for the generated intelligence page.
"""

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent))

from generate_intelligence_page import generate_html_from_analysis


def test_agent_chat_uses_text_content_for_dynamic_messages():
    """Chat UI must not inject user input or feed-derived responses as HTML."""
    html = generate_html_from_analysis(
        {
            "date": "2026-04-20",
            "executive_summary": {"summary": "safe"},
            "top_insights": [],
            "significant_changes": [],
            "recommendations": [],
        }
    )

    assert "paragraph.textContent = message;" in html
    assert "${question}" not in html
    assert "${response}" not in html


def test_committed_intelligence_page_has_no_chat_template_injection():
    """The checked-in static page is served directly and must stay patched."""
    docs_page = Path(__file__).resolve().parents[1] / "docs" / "intelligence.html"
    html = docs_page.read_text(encoding="utf-8")

    assert "paragraph.textContent = message;" in html
    assert "${question}" not in html
    assert "${response}" not in html
