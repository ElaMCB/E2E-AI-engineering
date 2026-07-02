"""
Regression tests for generated HTML security behavior.
"""

import importlib.util
from pathlib import Path


def _load_module(module_name: str, filename: str):
    module_path = Path(__file__).resolve().parent / filename
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_monitor_page_rejects_script_link_schemes():
    generate_html = _load_module("generate_html_under_test", "generate_html.py")

    page = generate_html.generate_html_from_summaries([
        {
            "date": "2026-07-02",
            "updates": [
                {
                    "title": "Malicious feed item",
                    "summary": "External feed supplied an unsafe URL",
                    "source": "RSS",
                    "date": "2026-07-02",
                    "url": "javascript:alert(1)",
                    "keywords": ["deepseek"],
                }
            ],
        }
    ])

    assert 'href="javascript:alert(1)"' not in page
    assert 'href="#"' in page


def test_intelligence_chat_embeds_data_safely_and_renders_text():
    generate_intelligence_page = _load_module(
        "generate_intelligence_page_under_test",
        "generate_intelligence_page.py",
    )
    analysis = {
        "date": "2026-07-02",
        "executive_summary": {"summary": "Weekly summary"},
        "top_insights": [
            {
                "title": "</script><img src=x onerror=alert(1)>",
                "description": "<svg onload=alert(1)>DeepSeek update</svg>",
                "impact_score": 9.0,
                "type": "trend",
                "evidence": ["RSS"],
            }
        ],
        "significant_changes": [],
        "recommendations": ["Review safely"],
    }

    page = generate_intelligence_page.generate_html_from_analysis(analysis)

    assert "fetch('ai-monitor/results/latest_analysis.json')" not in page
    assert 'id="analysis-data"' in page
    assert "<\\/script>" in page
    assert "</script><img" not in page
    assert "paragraph.textContent = text;" in page
    assert "${question}" not in page
    assert "${response}" not in page
