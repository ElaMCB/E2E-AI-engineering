"""
Regression tests for intelligence page generation.
"""

from generate_intelligence_page import generate_html_from_analysis


def test_generated_intelligence_page_escapes_untrusted_analysis_and_chat_text():
    payload = '<img src=x onerror="alert(1)">'
    analysis = {
        "date": "2026-04-20",
        "executive_summary": {"summary": payload},
        "top_insights": [
            {
                "title": payload,
                "description": payload,
                "impact_score": 9.0,
                "type": "new_model",
                "evidence": [payload],
            }
        ],
        "significant_changes": [
            {
                "category": "market_shift",
                "description": payload,
                "magnitude": 6.0,
                "implications": [payload],
            }
        ],
        "recommendations": [payload],
    }

    html = generate_html_from_analysis(analysis)

    assert payload not in html
    assert "&lt;img src=x onerror=&quot;alert(1)&quot;&gt;" in html
    assert "paragraph.textContent = text;" in html
    assert "${question}" not in html
    assert "${response}" not in html
