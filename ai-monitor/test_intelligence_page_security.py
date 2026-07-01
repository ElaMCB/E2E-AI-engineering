import importlib.util
from pathlib import Path


def _load_generator_module():
    module_path = Path(__file__).resolve().parent / "generate_intelligence_page.py"
    spec = importlib.util.spec_from_file_location("generate_intelligence_page", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_chat_messages_use_text_content_for_untrusted_text():
    generator = _load_generator_module()

    html = generator.generate_html_from_analysis(
        {
            "executive_summary": {"summary": "Safe summary"},
            "top_insights": [],
            "significant_changes": [],
            "recommendations": [],
        }
    )

    assert "${question}" not in html
    assert "${response}" not in html
    assert "userMsg.querySelector('p').textContent = question;" in html
    assert "agentMsg.querySelector('p').textContent = response;" in html


def test_embedded_analysis_json_cannot_break_out_of_script_tag():
    generator = _load_generator_module()
    payload = "</script><img src=x onerror=alert(1)>"

    html = generator.generate_html_from_analysis(
        {
            "executive_summary": {"summary": payload},
            "top_insights": [
                {
                    "type": "new_model",
                    "title": payload,
                    "description": payload,
                    "impact_score": 9.0,
                    "confidence": 0.9,
                    "related_updates": [],
                    "evidence": [],
                    "timestamp": "2026-07-01",
                }
            ],
            "significant_changes": [],
            "recommendations": [payload],
        }
    )

    assert payload not in html
    assert "\\u003c/script\\u003e\\u003cimg" in html
    assert "&lt;/script&gt;&lt;img" in html
    assert "JSON.parse(dataElement.textContent)" in html
    assert "fetch('ai-monitor/results/latest_analysis.json')" not in html
