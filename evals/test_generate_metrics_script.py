"""Regression tests for CI badge metric generation."""

import importlib.util
from pathlib import Path


def _load_generate_metrics_module():
    repo_root = Path(__file__).resolve().parents[1]
    script_path = repo_root / ".github" / "scripts" / "generate_metrics.py"
    spec = importlib.util.spec_from_file_location("generate_metrics", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_unparseable_eval_output_is_not_reported_as_green(monkeypatch):
    module = _load_generate_metrics_module()
    repo_root = Path(__file__).resolve().parents[1]
    monkeypatch.chdir(repo_root)

    class Result:
        returncode = 0
        stdout = "quick eval completed without a score line"
        stderr = ""

    monkeypatch.setattr(module.subprocess, "run", lambda *args, **kwargs: Result())

    badge = module.run_evaluation_tests()

    assert badge["message"] == "N/A"
    assert badge["color"] == "grey"
