import importlib.util
import subprocess
import sys
from pathlib import Path


def _load_generate_metrics_module():
    repo_root = Path(__file__).resolve().parents[1]
    script_path = repo_root / ".github" / "scripts" / "generate_metrics.py"
    spec = importlib.util.spec_from_file_location("generate_metrics", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_eval_parse_failure_does_not_report_green_score(monkeypatch):
    module = _load_generate_metrics_module()
    repo_root = Path(__file__).resolve().parents[1]
    monkeypatch.chdir(repo_root)

    def fake_run(*_args, **_kwargs):
        return subprocess.CompletedProcess(
            [sys.executable, "evals/run_ab_test_models_prompts.py", "--quick"],
            0,
            stdout="evaluation completed without the expected score line",
            stderr="",
        )

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    result = module.run_evaluation_tests()

    assert result["message"] == "N/A"
    assert result["color"] == "grey"
