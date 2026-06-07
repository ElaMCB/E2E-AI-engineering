"""
Runtime observability metrics for agent orchestrations.
"""

from __future__ import annotations

from typing import Any, Dict, List


def evaluate_runtime_trace(trace: Dict[str, Any]) -> Dict[str, float]:
    """
    Compute reliability-style metrics from a runtime trace payload.

    Expected schema:
      {
        "summary": {
          "total_steps": int,
          "success_rate": float,
          "average_step_duration_ms": float,
          "estimated_cost_usd": float
        },
        "runs": [{"status": "ok|error", "duration_ms": float, ...}]
      }
    """
    summary = trace.get("summary", {})
    runs: List[Dict[str, Any]] = trace.get("runs", [])

    avg_step_duration_ms = float(summary.get("average_step_duration_ms", 0.0))
    estimated_cost_usd = float(summary.get("estimated_cost_usd", 0.0))

    if runs:
        total_steps = len(runs)
        failed_steps = sum(1 for run in runs if run.get("status") != "ok")
        success_rate = ((total_steps - failed_steps) / total_steps) if total_steps else 1.0
    else:
        total_steps = int(summary.get("total_steps", 0))
        success_rate = float(summary.get("success_rate", 1.0 if total_steps == 0 else 0.0))
        failed_steps = int(summary.get("failed_steps", 0))

    if runs and avg_step_duration_ms <= 0.0:
        avg_step_duration_ms = sum(float(r.get("duration_ms", 0.0)) for r in runs) / len(runs)

    failure_rate = (failed_steps / total_steps) if total_steps else 0.0

    return {
        "total_steps": float(total_steps),
        "success_rate": success_rate,
        "failure_rate": failure_rate,
        "average_step_duration_ms": avg_step_duration_ms,
        "estimated_cost_usd": estimated_cost_usd,
    }


def check_runtime_thresholds(
    metrics: Dict[str, float],
    min_success_rate: float = 0.95,
    max_avg_step_duration_ms: float = 3000.0,
    max_steps_per_run: float = 12.0,
) -> Dict[str, Any]:
    """Evaluate whether runtime metrics satisfy CI guardrails."""
    violations = []

    if metrics.get("success_rate", 0.0) < min_success_rate:
        violations.append(
            f"success_rate {metrics.get('success_rate', 0.0):.3f} < {min_success_rate:.3f}"
        )

    if metrics.get("average_step_duration_ms", 0.0) > max_avg_step_duration_ms:
        violations.append(
            f"average_step_duration_ms {metrics.get('average_step_duration_ms', 0.0):.1f} > {max_avg_step_duration_ms:.1f}"
        )

    if metrics.get("total_steps", 0.0) > max_steps_per_run:
        violations.append(
            f"total_steps {metrics.get('total_steps', 0.0):.0f} > {max_steps_per_run:.0f}"
        )

    return {
        "ok": len(violations) == 0,
        "violations": violations,
    }
