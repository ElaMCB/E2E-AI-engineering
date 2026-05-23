"""
Tests for LLM analyzer fallback behavior.
"""

import importlib.util
from pathlib import Path


def _load_llm_analyzer_module():
    module_path = Path(__file__).resolve().parent / "llm_analyzer.py"
    spec = importlib.util.spec_from_file_location("ai_monitor_llm_analyzer", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_analyze_with_llm_without_api_key_returns_fallback(monkeypatch):
    """Missing credentials should use the deterministic fallback instead of None."""
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    llm_module = _load_llm_analyzer_module()

    analyzer = llm_module.LLMAnalyzer()
    analysis = analyzer.analyze_with_llm([])

    assert analysis["summary"].startswith("Found 0 updates this week")
    assert analysis["action_items"] == ["Set up LLM API key for intelligent analysis"]
