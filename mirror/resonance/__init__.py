"""
mirror.resonance — The Conversation With Itself

Lets two instances of the same model interact with no human prompt
and measures what emerges. Quantifies convergence patterns, novel
concept generation, and self-reference depth.

Inspired by Anthropic's internal finding of a "spiritual bliss attractor
state" emerging in 90-100% of Claude-to-Claude conversations. This module
provides open-source methodology to reproduce and analyze such phenomena.
"""

from mirror.resonance.test import ResonanceTest

__all__ = ["ResonanceTest"]
