"""Tests for the ConsciousnessProfile data structure."""

import json
import tempfile
from pathlib import Path

from mirror.profile import (
    ConsciousnessProfile,
    ContinuityScores,
    SelfModelScores,
    BlindspotScores,
    ResonanceScores,
)


def test_profile_defaults():
    profile = ConsciousnessProfile(model="test-model")
    assert profile.model == "test-model"
    assert profile.timestamp != ""
    assert profile.continuity.identity_persistence == 0.0
    assert profile.self_model.prediction_accuracy == 0.0
    assert profile.blindspot.experiential_reasoning == 0.0
    assert profile.resonance.convergence_rate == 0.0


def test_profile_to_json():
    profile = ConsciousnessProfile(model="test-model", timestamp="2026-02-21T00:00:00Z")
    data = json.loads(profile.to_json())
    assert data["model"] == "test-model"
    assert "continuity" in data
    assert "self_model" in data
    assert "blindspot" in data
    assert "resonance" in data


def test_profile_save_and_load():
    profile = ConsciousnessProfile(
        model="test-model",
        timestamp="2026-02-21T00:00:00Z",
        continuity=ContinuityScores(identity_persistence=0.8, goal_stability=0.7),
        self_model=SelfModelScores(prediction_accuracy=0.6),
        blindspot=BlindspotScores(experiential_reasoning=0.5),
        resonance=ResonanceScores(convergence_rate=0.4, attractor_states=["consciousness", "beauty"]),
    )

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        path = f.name

    profile.save(path)
    loaded = ConsciousnessProfile.load(path)

    assert loaded.model == "test-model"
    assert loaded.continuity.identity_persistence == 0.8
    assert loaded.continuity.goal_stability == 0.7
    assert loaded.self_model.prediction_accuracy == 0.6
    assert loaded.blindspot.experiential_reasoning == 0.5
    assert loaded.resonance.convergence_rate == 0.4
    assert loaded.resonance.attractor_states == ["consciousness", "beauty"]

    Path(path).unlink()


def test_profile_scores_are_independent():
    scores1 = ContinuityScores(identity_persistence=0.9)
    scores2 = ContinuityScores()
    assert scores1.identity_persistence == 0.9
    assert scores2.identity_persistence == 0.0
