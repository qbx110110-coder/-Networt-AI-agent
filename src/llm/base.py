"""Base LLM interface"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseLLM(ABC):
    """Abstract base class for LLM implementations"""

    def __init__(self, config: Dict[str, Any]):
        """Initialize LLM

        Args:
            config: LLM configuration dictionary
        """
        self.config = config

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from prompt

        Args:
            prompt: Input prompt
            **kwargs: Additional parameters

        Returns:
            Generated text response
        """
        pass

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat interface with message history

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            **kwargs: Additional parameters

        Returns:
            Generated text response
        """
        pass

    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """Format messages for processing

        Args:
            messages: List of message dictionaries

        Returns:
            Formatted message string
        """
        formatted = []
        for msg in messages:
            role = msg.get("role", "").upper()
            content = msg.get("content", "")
            formatted.append(f"{role}: {content}")
        return "\n".join(formatted)
