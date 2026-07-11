import importlib.util
import json
from pathlib import Path


def _load_module(module_name: str, file_name: str):
    module_path = Path(__file__).with_name(file_name)
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_intelligence_page_embeds_analysis_and_renders_chat_text_safely():
    generator = _load_module("generate_intelligence_page", "generate_intelligence_page.py")
    malicious_title = "<img src=x onerror=alert(1)>"
    malicious_description = "</script><script>alert(1)</script>"
    analysis = {
        "date": "2026-07-11",
        "executive_summary": {"summary": "Weekly summary"},
        "top_insights": [
            {
                "title": malicious_title,
                "description": malicious_description,
                "impact_score": 9.0,
                "type": "breakthrough",
                "evidence": ["Feed"],
            }
        ],
        "significant_changes": [],
        "recommendations": [],
    }

    html_output = generator.generate_html_from_analysis(analysis)

    assert "fetch('ai-monitor/results/latest_analysis.json')" not in html_output
    assert '<script id="analysis-data" type="application/json">' in html_output
    assert "</script><script>alert(1)</script>" not in html_output
    assert "<img src=x onerror=alert(1)>" not in html_output
    assert "${question}" not in html_output
    assert "${response}" not in html_output
    assert "textContent = text" in html_output

    embedded_json = html_output.split(
        '<script id="analysis-data" type="application/json">', 1
    )[1].split("</script>", 1)[0]
    embedded_analysis = json.loads(embedded_json)
    assert embedded_analysis["top_insights"][0]["title"] == malicious_title
    assert embedded_analysis["top_insights"][0]["description"] == malicious_description


def test_monitor_page_drops_non_http_urls_from_generated_links():
    generator = _load_module("generate_html", "generate_html.py")
    summaries = [
        {
            "date": "2026-07-11",
            "updates": [
                {
                    "title": "Unsafe link",
                    "url": "javascript:alert(1)",
                    "source": "Poisoned Feed",
                    "date": "2026-07-11",
                    "summary": "Should render without a clickable href",
                    "keywords": ["security"],
                },
                {
                    "title": "Safe link",
                    "url": "https://example.com/update?x=1&y=2",
                    "source": "Trusted Feed",
                    "date": "2026-07-11",
                    "summary": "Should keep the link",
                    "keywords": ["security"],
                },
            ],
        }
    ]

    html_output = generator.generate_html_from_summaries(summaries)

    assert 'href="javascript:alert(1)"' not in html_output
    assert "javascript:alert(1)" not in html_output
    assert "<span>Unsafe link</span>" in html_output
    assert 'href="https://example.com/update?x=1&amp;y=2"' in html_output
