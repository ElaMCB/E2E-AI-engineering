"""
Tests for CI badge metric generation.
"""

import importlib.util
import subprocess
from pathlib import Path


def _load_generate_metrics_module():
    repo_root = Path(__file__).resolve().parents[1]
    script_path = repo_root / ".github" / "scripts" / "generate_metrics.py"
    spec = importlib.util.spec_from_file_location("generate_metrics_under_test", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_eval_parse_failure_returns_unavailable_badge(monkeypatch):
    generate_metrics = _load_generate_metrics_module()

    def run_without_score(*_args, **_kwargs):
        return subprocess.CompletedProcess(
            args=["python", "evals/run_ab_test_models_prompts.py", "--quick"],
            returncode=0,
            stdout="evaluation completed without a badge line",
            stderr="",
        )

    monkeypatch.setattr(generate_metrics.subprocess, "run", run_without_score)

    badge = generate_metrics.run_evaluation_tests()

    assert badge == {
        "schemaVersion": 1,
        "label": "Eval Score",
        "message": "N/A",
        "color": "grey",
    }
