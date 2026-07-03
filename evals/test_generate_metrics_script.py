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


def test_unparseable_eval_output_reports_na(monkeypatch):
    """A successful command without a score should not publish a green badge."""
    module = _load_generate_metrics_module()
    repo_root = Path(__file__).resolve().parents[1]
    monkeypatch.chdir(repo_root)

    def fake_run(*args, **kwargs):
        return SimpleNamespace(returncode=0, stdout="completed without score", stderr="")

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    badge = module.run_evaluation_tests()

    assert badge["message"] == "N/A"
    assert badge["color"] == "grey"
