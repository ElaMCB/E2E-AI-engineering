"""
Integration tests for runtime traces and CI guardrails.
"""

import json
import importlib.util
from pathlib import Path

import pytest


def _load_analyzer_module():
    repo_root = Path(__file__).resolve().parents[1]
    analyzer_path = repo_root / "ai-monitor" / "analyzer.py"
    spec = importlib.util.spec_from_file_location("ai_monitor_analyzer", analyzer_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_runtime_trace_generation_and_thresholds(tmp_path):
    """Analyzer should emit runtime trace that passes baseline thresholds."""
    from metrics.runtime_observability import evaluate_runtime_trace, check_runtime_thresholds

    analyzer_module = _load_analyzer_module()
    results_dir = tmp_path / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    weekly_summary = [
        {
            "date": "2026-04-13",
            "updates": [],
        },
        {
            "date": "2026-04-20",
            "updates": [
                {
                    "title": "DeepSeek releases vNext",
                    "summary": "New model release with open source weights",
                    "source": "GitHub Releases",
                    "date": "2026-04-20",
                    "keywords": ["deepseek"],
                    "hash": "a1",
                },
                {
                    "title": "Kimi announces new capability",
                    "summary": "Moonshot AI expands features",
                    "source": "Company Blog",
                    "date": "2026-04-20",
                    "keywords": ["kimi"],
                    "hash": "a2",
                },
            ],
        }
    ]

    with open(results_dir / "weekly_summary.json", "w", encoding="utf-8") as f:
        json.dump(weekly_summary, f, indent=2)

    analyzer = analyzer_module.IntelligentAnalyzer(results_dir=str(results_dir))
    analysis = analyzer.analyze_weekly_data()
    assert "error" not in analysis

    trace_path = results_dir / "latest_runtime_trace.json"
    assert trace_path.exists()

    with open(trace_path, "r", encoding="utf-8") as f:
        trace_data = json.load(f)

    metrics = evaluate_runtime_trace(trace_data)
    gate = check_runtime_thresholds(
        metrics,
        min_success_rate=0.95,
        max_avg_step_duration_ms=5000.0,
        max_steps_per_run=12.0,
    )
    assert gate["ok"], f"Runtime threshold violations: {gate['violations']}"
    assert any(
        change["category"] == "market_shift"
        and change["week_over_week_change"]["prev"] == 0
        for change in analysis["significant_changes"]
    )


def test_agent_failure_preserves_last_valid_analysis(tmp_path, monkeypatch):
    """A failed agent must not replace the last complete analysis."""
    analyzer_module = _load_analyzer_module()
    results_dir = tmp_path / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    weekly_summary = [{"date": "2026-04-20", "updates": []}]
    previous_analysis = {"date": "2026-04-13", "top_insights": ["valid"]}
    with open(results_dir / "weekly_summary.json", "w", encoding="utf-8") as f:
        json.dump(weekly_summary, f)
    with open(results_dir / "latest_analysis.json", "w", encoding="utf-8") as f:
        json.dump(previous_analysis, f)

    analyzer = analyzer_module.IntelligentAnalyzer(results_dir=str(results_dir))

    def fail_agent(_context):
        raise RuntimeError("injected agent failure")

    monkeypatch.setattr(analyzer.priority_agent, "run", fail_agent)
    result = analyzer.analyze_weekly_data()

    assert result["failed_agents"] == ["priority_scoring"]
    with open(results_dir / "latest_analysis.json", "r", encoding="utf-8") as f:
        assert json.load(f) == previous_analysis
    with open(results_dir / "latest_runtime_trace.json", "r", encoding="utf-8") as f:
        trace = json.load(f)
    assert trace["summary"]["failed_steps"] == 1
    assert trace["runs"][0]["error"] == "injected agent failure"


def test_analyzer_cli_exits_nonzero_on_analysis_error(monkeypatch):
    """The scheduled workflow must be able to detect analyzer failures."""
    analyzer_module = _load_analyzer_module()

    class FailingAnalyzer:
        def analyze_weekly_data(self):
            return {"error": "agent failed"}

    monkeypatch.setattr(analyzer_module, "IntelligentAnalyzer", FailingAnalyzer)

    with pytest.raises(SystemExit) as exc_info:
        analyzer_module.main()

    assert exc_info.value.code == 1
