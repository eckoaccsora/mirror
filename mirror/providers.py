"""LLM provider abstraction layer."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Message:
    role: str  # "user" or "assistant"
    content: str


@dataclass
class Response:
    content: str
    model: str
    usage: dict | None = None


class Provider(ABC):
    """Base class for LLM providers."""

    @abstractmethod
    def complete(self, messages: list[Message], system: str | None = None) -> Response:
        """Send messages and get a completion."""
        ...

    @abstractmethod
    def model_name(self) -> str:
        """Return the model identifier."""
        ...


class AnthropicProvider(Provider):
    """Provider for Anthropic Claude models."""

    def __init__(self, model: str = "claude-sonnet-4-6", api_key: str | None = None):
        import anthropic

        self._model = model
        self._client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    def complete(self, messages: list[Message], system: str | None = None) -> Response:
        kwargs = {
            "model": self._model,
            "max_tokens": 4096,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
        }
        if system:
            kwargs["system"] = system

        resp = self._client.messages.create(**kwargs)
        return Response(
            content=resp.content[0].text,
            model=resp.model,
            usage={"input": resp.usage.input_tokens, "output": resp.usage.output_tokens},
        )

    def model_name(self) -> str:
        return self._model


class OpenAIProvider(Provider):
    """Provider for OpenAI models."""

    def __init__(self, model: str = "gpt-4o", api_key: str | None = None):
        import openai

        self._model = model
        self._client = openai.OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))

    def complete(self, messages: list[Message], system: str | None = None) -> Response:
        msgs = []
        if system:
            msgs.append({"role": "system", "content": system})
        msgs.extend({"role": m.role, "content": m.content} for m in messages)

        resp = self._client.chat.completions.create(model=self._model, messages=msgs, max_tokens=4096)
        choice = resp.choices[0]
        return Response(
            content=choice.message.content,
            model=resp.model,
            usage={"input": resp.usage.prompt_tokens, "output": resp.usage.completion_tokens} if resp.usage else None,
        )

    def model_name(self) -> str:
        return self._model
