"""
mirror.blindspot — What Can't It Fake?

Adversarial test suite inspired by Schneider's AI Consciousness Test (ACT).
Designs questions where a conscious entity and a sophisticated pattern matcher
would answer differently.

The key insight: a system trained on text about consciousness can parrot
descriptions of subjective experience perfectly. The challenge is designing
questions where genuine experience (if it exists) would produce detectably
different answers from sophisticated mimicry.

Gets harder as models get more capable — the adversarial design ensures
the test remains meaningful even as language models improve.
"""

from mirror.blindspot.test import BlindspotTest

__all__ = ["BlindspotTest"]
