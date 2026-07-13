import importlib.util
from pathlib import Path


def _load_module(module_name: str, file_name: str):
    module_path = Path(__file__).resolve().parent / file_name
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_monitor_html_rejects_scriptable_urls():
    generator = _load_module("generate_html", "generate_html.py")

    rendered = generator.generate_html_from_summaries(
        [
            {
                "date": "2026-04-20",
                "updates": [
                    {
                        "title": "Malicious feed item",
                        "summary": "External feed controlled content",
                        "source": "RSS",
                        "date": "2026-04-20",
                        "url": "javascript:alert(1)",
                        "keywords": ["deepseek"],
                    }
                ],
            }
        ]
    )

    assert 'href="#"' in rendered
    assert "javascript:alert" not in rendered


def test_intelligence_chat_renders_dynamic_messages_as_text():
    generator = _load_module("generate_intelligence_page", "generate_intelligence_page.py")

    rendered = generator.generate_html_from_analysis(
        {
            "date": "2026-04-20",
            "executive_summary": {"summary": "Summary"},
            "top_insights": [
                {
                    "title": "<img src=x onerror=alert(1)>",
                    "description": "<script>alert(1)</script>",
                    "impact_score": 9.0,
                    "confidence": 0.9,
                    "type": "new_model",
                    "evidence": ["feed"],
                }
            ],
            "significant_changes": [],
            "recommendations": ["Review top insights"],
        }
    )

    assert "paragraph.textContent = text" in rendered
    assert "${question}" not in rendered
    assert "${response}" not in rendered
