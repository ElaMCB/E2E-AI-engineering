import importlib.util
from pathlib import Path


def _load_metrics_module():
    repo_root = Path(__file__).resolve().parents[1]
    script_path = repo_root / ".github" / "scripts" / "generate_metrics.py"
    spec = importlib.util.spec_from_file_location("generate_metrics", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class _CompletedProcess:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_eval_score_parse_failure_returns_grey_na(monkeypatch):
    metrics = _load_metrics_module()

    monkeypatch.setattr(
        metrics.subprocess,
        "run",
        lambda *args, **kwargs: _CompletedProcess(
            returncode=0,
            stdout="Evaluation finished, but score format changed",
        ),
    )

    badge = metrics.run_evaluation_tests()

    assert badge == {
        "schemaVersion": 1,
        "label": "Eval Score",
        "message": "N/A",
        "color": "grey",
    }


def test_eval_score_parse_success_uses_reported_score(monkeypatch):
    metrics = _load_metrics_module()

    monkeypatch.setattr(
        metrics.subprocess,
        "run",
        lambda *args, **kwargs: _CompletedProcess(
            returncode=0,
            stdout="Eval Score: 92.5%",
        ),
    )

    badge = metrics.run_evaluation_tests()

    assert badge["message"] == "92.5%"
    assert badge["color"] == "green"
