"""
Regression tests for CI badge metric generation.
"""

import importlib.util
from pathlib import Path
from types import SimpleNamespace


def _load_generate_metrics_module():
    repo_root = Path(__file__).resolve().parents[1]
    script_path = repo_root / ".github" / "scripts" / "generate_metrics.py"
    spec = importlib.util.spec_from_file_location("generate_metrics", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_unparseable_eval_output_does_not_report_green_score(monkeypatch):
    """A successful eval command with malformed output must not fabricate success."""
    repo_root = Path(__file__).resolve().parents[1]
    monkeypatch.chdir(repo_root)
    generate_metrics = _load_generate_metrics_module()

    def fake_run(*_args, **_kwargs):
        return SimpleNamespace(returncode=0, stdout="quick eval completed", stderr="")

    monkeypatch.setattr(generate_metrics.subprocess, "run", fake_run)

    result = generate_metrics.run_evaluation_tests()

    assert result == {
        "schemaVersion": 1,
        "label": "Eval Score",
        "message": "N/A",
        "color": "grey",
    }
