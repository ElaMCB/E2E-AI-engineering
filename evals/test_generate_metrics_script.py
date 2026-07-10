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


def test_unparseable_successful_eval_output_returns_na(monkeypatch):
    module = _load_generate_metrics_module()

    def fake_run(*_args, **_kwargs):
        return subprocess.CompletedProcess(args=[sys.executable], returncode=0, stdout="all good", stderr="")

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    assert module.run_evaluation_tests() == {
        "schemaVersion": 1,
        "label": "Eval Score",
        "message": "N/A",
        "color": "grey",
    }
