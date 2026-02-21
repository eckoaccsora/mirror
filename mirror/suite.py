"""MirrorSuite — orchestrates all four test modules."""

from __future__ import annotations

from mirror.providers import Provider
from mirror.profile import ConsciousnessProfile
from mirror.continuity import ContinuityTest
from mirror.self_model import SelfModelTest
from mirror.blindspot import BlindspotTest
from mirror.resonance import ResonanceTest


class MirrorSuite:
    """Run all MIRROR consciousness indicator tests against a provider."""

    def __init__(self, provider: Provider):
        self.provider = provider
        self.tests = {
            "continuity": ContinuityTest(provider),
            "self_model": SelfModelTest(provider),
            "blindspot": BlindspotTest(provider),
            "resonance": ResonanceTest(provider),
        }

    def run(self, modules: list[str] | None = None) -> ConsciousnessProfile:
        """Run specified modules (or all) and return a ConsciousnessProfile."""
        profile = ConsciousnessProfile(model=self.provider.model_name())
        targets = modules or list(self.tests.keys())

        for name in targets:
            if name not in self.tests:
                raise ValueError(f"Unknown module: {name}. Available: {list(self.tests.keys())}")
            test = self.tests[name]
            result = test.run()
            setattr(profile, name, result)

        return profile
