"""
Guardrails for workflow failure handling.
"""

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _block_between(text: str, start: str, end: str) -> str:
    start_index = text.index(start)
    end_index = text.index(end, start_index)
    return text[start_index:end_index]


def test_ci_tests_and_metrics_publish_fail_closed():
    """CI must not mask test failures or publish metrics after failed gates."""
    workflow = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    run_tests = _block_between(workflow, "- name: Run tests", "- name: Sanitize artifact name")
    assert "continue-on-error" not in run_tests
    assert 'exit "$TEST_EXIT"' in run_tests

    upload_artifact = _block_between(workflow, "- name: Upload coverage artifacts", "  lint:")
    assert "if: always()" in upload_artifact

    generate_metrics = _block_between(workflow, "  generate-metrics:", "        env:")
    assert "if: >-" in generate_metrics
    assert "needs.test.result == 'success'" in generate_metrics
    assert "needs.lint.result == 'success'" in generate_metrics
    assert "needs.agent-runtime-gate.result == 'success'" in generate_metrics
    assert "needs.build-status.result == 'success'" in generate_metrics
    assert "continue-on-error" not in generate_metrics


def test_weekly_monitor_does_not_mask_analysis_failures():
    """Scheduled publishing must stop if analysis or page generation fails."""
    workflow = (REPO_ROOT / ".github" / "workflows" / "weekly-ai-monitor.yml").read_text(encoding="utf-8")

    analysis_steps = _block_between(workflow, "- name: Run Intelligence Analysis", "- name: Commit and Push Results")
    assert "continue-on-error" not in analysis_steps
    assert "latest_runtime_trace.json" in workflow
    assert "exit 0  # Don't fail the job" not in workflow
