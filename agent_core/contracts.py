"""
Shared contracts for agent-style systems.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AgentContext:
    """Standard execution context passed to agents."""

    updates: List[Dict[str, Any]]
    historical_data: List[Dict[str, Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)


class Agent(ABC):
    """Base contract for any executable agent."""

    def __init__(self, name: Optional[str] = None):
        self.name = name or self.__class__.__name__

    @abstractmethod
    def run(self, context: AgentContext) -> Any:
        """Execute the agent with a standard context."""
        raise NotImplementedError


class Tool(ABC):
    """Optional tool contract for future agent tool use."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self, **kwargs: Any) -> Any:
        """Execute a tool call."""
        raise NotImplementedError
