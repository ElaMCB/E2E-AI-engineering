import importlib.util
import subprocess
from pathlib import Path


def load_generate_metrics_module():
    script_path = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "generate_metrics.py"
    spec = importlib.util.spec_from_file_location("generate_metrics", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_unparseable_eval_output_fails_closed(monkeypatch):
    generate_metrics = load_generate_metrics_module()

    def fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(args[0], 0, stdout="All checks passed\n", stderr="")

    monkeypatch.setattr(generate_metrics.subprocess, "run", fake_run)
    badge = generate_metrics.run_evaluation_tests()

    assert badge == {
        "schemaVersion": 1,
        "label": "Eval Score",
        "message": "N/A",
        "color": "grey",
    }
