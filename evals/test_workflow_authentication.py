"""Regression tests for workflow publishing authentication."""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]


def _workflow_step(workflow_name, job_name, step_name):
    workflow_path = REPO_ROOT / ".github" / "workflows" / workflow_name
    workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    return next(
        step
        for step in workflow["jobs"][job_name]["steps"]
        if step.get("name") == step_name
    )


def test_weekly_publish_uses_pat_without_checkout_header_override():
    checkout = _workflow_step("weekly-ai-monitor.yml", "monitor", "Checkout repository")
    publish = _workflow_step(
        "weekly-ai-monitor.yml", "monitor", "Commit and Push Results"
    )

    assert checkout["with"]["persist-credentials"] is False
    assert (
        'git remote set-url origin "https://x-access-token:${GIT_TOKEN}'
        in publish["run"]
    )
    assert publish["run"].index("git remote set-url") < publish["run"].index(
        "git pull origin main"
    )
    assert "exit 1" in publish["run"]


def test_metrics_publish_uses_pat_without_masking_push_failure():
    checkout = _workflow_step("ci.yml", "generate-metrics", "Checkout repository")
    publish = _workflow_step("ci.yml", "generate-metrics", "Commit and push metrics")

    assert checkout["with"]["persist-credentials"] is False
    assert (
        'git remote set-url origin "https://x-access-token:${GIT_TOKEN}'
        in publish["run"]
    )
    assert publish["run"].index("git remote set-url") < publish["run"].index(
        "git push origin main"
    )
    assert "exit 1" in publish["run"]
    assert not publish.get("continue-on-error", False)
