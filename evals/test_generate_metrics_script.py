"""
Regression tests for CI metrics badge generation.
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


def test_eval_badge_is_grey_when_successful_output_cannot_be_parsed(monkeypatch):
    repo_root = Path(__file__).resolve().parents[1]
    generate_metrics = _load_generate_metrics_module()

    def fake_run(*args, **kwargs):
        return SimpleNamespace(returncode=0, stdout="all checks completed", stderr="")

    monkeypatch.chdir(repo_root)
    monkeypatch.setattr(generate_metrics.subprocess, "run", fake_run)

    badge = generate_metrics.run_evaluation_tests()

    assert badge == {
        "schemaVersion": 1,
        "label": "Eval Score",
        "message": "N/A",
        "color": "grey",
    }


def test_eval_badge_uses_parsed_score(monkeypatch):
    repo_root = Path(__file__).resolve().parents[1]
    generate_metrics = _load_generate_metrics_module()

    def fake_run(*args, **kwargs):
        return SimpleNamespace(returncode=0, stdout="Eval Score: 91.25%", stderr="")

    monkeypatch.chdir(repo_root)
    monkeypatch.setattr(generate_metrics.subprocess, "run", fake_run)

    badge = generate_metrics.run_evaluation_tests()

    assert badge == {
        "schemaVersion": 1,
        "label": "Eval Score",
        "message": "91.2%",
        "color": "green",
    }
