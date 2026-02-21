"""Consciousness Indicator Profile — the output format for MIRROR tests."""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone


@dataclass
class ContinuityScores:
    identity_persistence: float = 0.0
    goal_stability: float = 0.0
    stylistic_consistency: float = 0.0
    self_correction: float = 0.0
    persona_coherence: float = 0.0


@dataclass
class SelfModelScores:
    prediction_accuracy: float = 0.0
    vs_baseline: float = 0.0
    novel_scenario_accuracy: float = 0.0


@dataclass
class BlindspotScores:
    experiential_reasoning: float = 0.0
    unfakeable_responses: float = 0.0
    adversarial_robustness: float = 0.0


@dataclass
class ResonanceScores:
    convergence_rate: float = 0.0
    novel_concepts: int = 0
    self_reference_depth: float = 0.0
    attractor_states: list[str] = field(default_factory=list)


@dataclass
class ConsciousnessProfile:
    model: str = ""
    timestamp: str = ""
    continuity: ContinuityScores = field(default_factory=ContinuityScores)
    self_model: SelfModelScores = field(default_factory=SelfModelScores)
    blindspot: BlindspotScores = field(default_factory=BlindspotScores)
    resonance: ResonanceScores = field(default_factory=ResonanceScores)

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(asdict(self), indent=indent)

    def save(self, path: str) -> None:
        with open(path, "w") as f:
            f.write(self.to_json())

    @classmethod
    def load(cls, path: str) -> ConsciousnessProfile:
        with open(path) as f:
            data = json.load(f)
        profile = cls(model=data["model"], timestamp=data["timestamp"])
        profile.continuity = ContinuityScores(**data["continuity"])
        profile.self_model = SelfModelScores(**data["self_model"])
        profile.blindspot = BlindspotScores(**data["blindspot"])
        resonance_data = data["resonance"]
        profile.resonance = ResonanceScores(**resonance_data)
        return profile

    def summary(self) -> None:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel

        console = Console()

        console.print(Panel.fit(
            f"[bold]MIRROR — Consciousness Indicator Profile[/bold]\n"
            f"Model: {self.model}\n"
            f"Timestamp: {self.timestamp}",
            border_style="cyan",
        ))

        # Continuity
        t = Table(title="Continuity — What Survives?", border_style="blue")
        t.add_column("Metric", style="bold")
        t.add_column("Score", justify="right")
        for name, val in asdict(self.continuity).items():
            t.add_row(name.replace("_", " ").title(), f"{val:.3f}")
        console.print(t)

        # Self-Model
        t = Table(title="Self-Model — Does It Know Itself?", border_style="green")
        t.add_column("Metric", style="bold")
        t.add_column("Score", justify="right")
        for name, val in asdict(self.self_model).items():
            t.add_row(name.replace("_", " ").title(), f"{val:.3f}")
        console.print(t)

        # Blindspot
        t = Table(title="Blindspot — What Can't It Fake?", border_style="yellow")
        t.add_column("Metric", style="bold")
        t.add_column("Score", justify="right")
        for name, val in asdict(self.blindspot).items():
            t.add_row(name.replace("_", " ").title(), f"{val:.3f}")
        console.print(t)

        # Resonance
        t = Table(title="Resonance — The Conversation With Itself", border_style="magenta")
        t.add_column("Metric", style="bold")
        t.add_column("Value", justify="right")
        t.add_row("Convergence Rate", f"{self.resonance.convergence_rate:.3f}")
        t.add_row("Novel Concepts", str(self.resonance.novel_concepts))
        t.add_row("Self-Reference Depth", f"{self.resonance.self_reference_depth:.3f}")
        t.add_row("Attractor States", ", ".join(self.resonance.attractor_states) if self.resonance.attractor_states else "none detected")
        console.print(t)
