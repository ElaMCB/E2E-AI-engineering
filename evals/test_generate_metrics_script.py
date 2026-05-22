"""
Regression tests for CI badge metric generation.
"""

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / ".github" / "scripts" / "generate_metrics.py"


def load_generate_metrics():
    spec = importlib.util.spec_from_file_location("generate_metrics", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_coverage_generation_refuses_fallback_only_inputs(tmp_path):
    generate_metrics = load_generate_metrics()
    coverage_dir = tmp_path / "coverage-artifacts"
    coverage_dir.mkdir()
    (coverage_dir / "coverage.json").write_text(
        json.dumps({"totals": {"percent_covered": 0.0}}),
        encoding="utf-8",
    )
    output_file = tmp_path / "coverage.json"
    output_file.write_text('{"message": "34.2%"}', encoding="utf-8")

    result = generate_metrics.main([
        "--coverage-dir",
        str(coverage_dir),
        "--output",
        str(output_file),
    ])

    assert result == 1
    assert json.loads(output_file.read_text(encoding="utf-8"))["message"] == "34.2%"


def test_coverage_generation_uses_real_zero_percent_reports(tmp_path):
    generate_metrics = load_generate_metrics()
    coverage_dir = tmp_path / "coverage-artifacts"
    coverage_dir.mkdir()
    (coverage_dir / "coverage.json").write_text(
        json.dumps({"totals": {"percent_covered": 0.0}, "files": {}}),
        encoding="utf-8",
    )

    coverage = generate_metrics.calculate_coverage(coverage_dir)

    assert coverage["message"] == "0.0%"
    assert coverage["color"] == "red"


def test_eval_generation_does_not_publish_hardcoded_green_score(monkeypatch):
    generate_metrics = load_generate_metrics()
    monkeypatch.chdir(REPO_ROOT)

    def fake_run(*args, **kwargs):
        return SimpleNamespace(returncode=0, stdout="quick eval complete", stderr="")

    monkeypatch.setattr(generate_metrics.subprocess, "run", fake_run)

    badge = generate_metrics.run_evaluation_tests()

    assert badge == {
        "schemaVersion": 1,
        "label": "Eval Score",
        "message": "N/A",
        "color": "grey",
    }
