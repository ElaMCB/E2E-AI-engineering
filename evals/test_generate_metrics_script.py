"""
Tests for CI metrics generation.
"""

import importlib.util
import subprocess
from pathlib import Path


def _load_generate_metrics_module():
    repo_root = Path(__file__).resolve().parents[1]
    module_path = repo_root / ".github" / "scripts" / "generate_metrics.py"
    spec = importlib.util.spec_from_file_location("generate_metrics", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_eval_metric_parse_failure_is_not_reported_as_passing(tmp_path, monkeypatch):
    """Unparseable eval output must not publish a green score."""
    metrics_module = _load_generate_metrics_module()
    (tmp_path / "evals").mkdir()
    monkeypatch.chdir(tmp_path)

    def fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args,
            returncode=0,
            stdout="All evals completed, but the output format changed.",
            stderr="",
        )

    monkeypatch.setattr(metrics_module.subprocess, "run", fake_run)

    metric = metrics_module.run_evaluation_tests()

    assert metric["message"] == "N/A"
    assert metric["color"] == "grey"


def test_eval_metric_parses_reported_score(tmp_path, monkeypatch):
    """Valid eval output should still publish the measured score."""
    metrics_module = _load_generate_metrics_module()
    (tmp_path / "evals").mkdir()
    monkeypatch.chdir(tmp_path)

    def fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args,
            returncode=0,
            stdout="\nEval Score: 72.5%\n",
            stderr="",
        )

    monkeypatch.setattr(metrics_module.subprocess, "run", fake_run)

    metric = metrics_module.run_evaluation_tests()

    assert metric["message"] == "72.5%"
    assert metric["color"] == "yellow"
