"""
Integration tests for runtime traces and CI guardrails.
"""

import json
import importlib.util
from pathlib import Path


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


def test_zero_update_baseline_generates_successful_runtime_trace(tmp_path):
    """A quiet prior week followed by activity should not fail change detection."""
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
            ],
        },
    ]

    with open(results_dir / "weekly_summary.json", "w", encoding="utf-8") as f:
        json.dump(weekly_summary, f, indent=2)

    analyzer = analyzer_module.IntelligentAnalyzer(results_dir=str(results_dir))
    analysis = analyzer.analyze_weekly_data()
    assert "error" not in analysis
    assert analysis["significant_changes"]
    descriptions = [change["description"] for change in analysis["significant_changes"]]
    assert any("zero baseline" in description for description in descriptions)

    with open(results_dir / "latest_runtime_trace.json", "r", encoding="utf-8") as f:
        trace_data = json.load(f)

    assert all(run["status"] == "ok" for run in trace_data["runs"])
    metrics = evaluate_runtime_trace(trace_data)
    gate = check_runtime_thresholds(metrics, min_success_rate=0.95)
    assert gate["ok"], f"Runtime threshold violations: {gate['violations']}"


def test_runtime_metrics_derive_success_rate_from_runs():
    """Failed run records should fail the gate even if the summary is stale."""
    from metrics.runtime_observability import evaluate_runtime_trace, check_runtime_thresholds

    trace_data = {
        "summary": {
            "total_steps": 2,
            "success_steps": 2,
            "failed_steps": 0,
            "success_rate": 1.0,
            "average_step_duration_ms": 1.0,
            "estimated_cost_usd": 0.0,
        },
        "runs": [
            {"agent_name": "priority_scoring", "status": "ok", "duration_ms": 1.0},
            {"agent_name": "change_detection", "status": "error", "duration_ms": 1.0},
        ],
    }

    metrics = evaluate_runtime_trace(trace_data)
    assert metrics["success_rate"] == 0.5
    assert metrics["failure_rate"] == 0.5

    gate = check_runtime_thresholds(metrics, min_success_rate=0.95)
    assert not gate["ok"]
    assert "success_rate 0.500 < 0.950" in gate["violations"]
