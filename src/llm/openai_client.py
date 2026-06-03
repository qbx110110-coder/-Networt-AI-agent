"""OpenAI LLM client implementation"""

import os
from typing import Any, Dict, List, Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from .base import BaseLLM


class OpenAIClient(BaseLLM):
    """OpenAI GPT client implementation"""

    def __init__(self, config: Dict[str, Any]):
        """Initialize OpenAI client

        Args:
            config: OpenAI configuration dictionary
        """
        super().__init__(config)

        if OpenAI is None:
            raise ImportError("openai package is required. Install with: pip install openai")

        # Get API key from config or environment
        api_key = config.get("api_key") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not provided")

        self.client = OpenAI(api_key=api_key)
        self.model = config.get("model", "gpt-4")
        self.temperature = config.get("temperature", 0.3)
        self.max_tokens = config.get("max_tokens", 2000)

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from prompt using OpenAI

        Args:
            prompt: Input prompt
            **kwargs: Additional parameters (temperature, max_tokens, etc.)

        Returns:
            Generated text response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", self.temperature),
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat interface with message history

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            **kwargs: Additional parameters

        Returns:
            Generated text response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get("temperature", self.temperature),
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")
