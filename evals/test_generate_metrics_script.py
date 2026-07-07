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


def test_eval_parse_miss_returns_unknown_badge(monkeypatch):
    module = _load_generate_metrics_module()
    repo_root = Path(__file__).resolve().parents[1]

    class CompletedProcess:
        returncode = 0
        stdout = "Evaluation completed successfully without badge summary"
        stderr = ""

    def fake_run(*args, **kwargs):
        return CompletedProcess()

    monkeypatch.chdir(repo_root)
    monkeypatch.setattr(module.subprocess, "run", fake_run)

    assert module.run_evaluation_tests() == {
        "schemaVersion": 1,
        "label": "Eval Score",
        "message": "N/A",
        "color": "grey",
    }
