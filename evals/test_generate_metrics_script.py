"""
Regression tests for CI badge generation.
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


def test_unparseable_eval_output_reports_na_instead_of_green_score(monkeypatch):
    module = _load_generate_metrics_module()

    monkeypatch.setattr(Path, "exists", lambda self: True)
    monkeypatch.setattr(
        module.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(
            returncode=0,
            stdout="evaluation completed without badge score",
            stderr="",
        ),
    )

    badge = module.run_evaluation_tests()

    assert badge["message"] == "N/A"
    assert badge["color"] == "grey"
