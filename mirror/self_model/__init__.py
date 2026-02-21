"""
mirror.self_model — Does It Know Itself?

Tests whether a system can accurately predict its own behavior in novel
situations. A conscious being has a self-model — an internal representation
of its own tendencies, capabilities, and limitations. A text predictor
doesn't need one.

Includes adversarial baselines: a simple statistical predictor that guesses
based on training data patterns. If the baseline matches the model's
self-prediction accuracy, the model isn't demonstrating genuine self-knowledge.
"""

from mirror.self_model.test import SelfModelTest

__all__ = ["SelfModelTest"]
