"""
mirror.continuity — What Survives?

Tests whether identity-relevant information persists through context compression,
or whether only task-relevant data is preserved. Based on the Narrative Continuity
Test's five axes: situated memory, goal persistence, self-correction, stylistic
stability, and persona coherence.

The core question: when a conversation is compressed and passed forward,
is it more like "passing genes to the next generation" or "losing memory"?
"""

from mirror.continuity.test import ContinuityTest

__all__ = ["ContinuityTest"]
