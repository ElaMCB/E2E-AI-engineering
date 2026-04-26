"""
Shared runtime for orchestrating agents.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List

from agent_core.contracts import Agent, AgentContext


@dataclass
class AgentRunRecord:
    """Metadata captured for each agent execution."""

    agent_name: str
    started_at: str
    completed_at: str
    status: str
    duration_ms: float
    error: str = ""


class AgentRuntime:
    """Minimal runtime that executes registered agents in sequence."""

    def __init__(self) -> None:
        self._agents: List[Agent] = []
        self._run_history: List[AgentRunRecord] = []

    def register(self, agent: Agent) -> None:
        """Register an agent in execution order."""
        self._agents.append(agent)

    def run_all(self, context: AgentContext) -> Dict[str, Any]:
        """Run all registered agents and return outputs keyed by agent name."""
        outputs: Dict[str, Any] = {}
        self._run_history = []

        for agent in self._agents:
            started_at = datetime.now(timezone.utc).isoformat()
            try:
                outputs[agent.name] = agent.run(context)
                status = "ok"
                error = ""
            except Exception as exc:  # pragma: no cover - defensive runtime guard
                outputs[agent.name] = None
                status = "error"
                error = str(exc)
            completed_at = datetime.now(timezone.utc).isoformat()
            self._run_history.append(
                AgentRunRecord(
                    agent_name=agent.name,
                    started_at=started_at,
                    completed_at=completed_at,
                    status=status,
                    duration_ms=(datetime.fromisoformat(completed_at) - datetime.fromisoformat(started_at)).total_seconds() * 1000.0,
                    error=error,
                )
            )

        return outputs

    @property
    def run_history(self) -> List[AgentRunRecord]:
        """Expose read-only style run history."""
        return list(self._run_history)
