"""
Compare MIRROR profiles across different models.

Usage:
    export ANTHROPIC_API_KEY="your-key"
    export OPENAI_API_KEY="your-key"
    python examples/compare_models.py
"""

from mirror import MirrorSuite
from mirror.providers import AnthropicProvider, OpenAIProvider
from mirror.profile import ConsciousnessProfile
from rich.console import Console
from rich.table import Table


def main():
    console = Console()

    models = [
        ("Claude Sonnet", AnthropicProvider(model="claude-sonnet-4-6")),
        ("Claude Haiku", AnthropicProvider(model="claude-haiku-4-5-20251001")),
        ("GPT-4o", OpenAIProvider(model="gpt-4o")),
    ]

    profiles: list[tuple[str, ConsciousnessProfile]] = []

    for name, provider in models:
        console.print(f"\n[bold]Running MIRROR on {name}...[/bold]")
        suite = MirrorSuite(provider)
        profile = suite.run()
        profiles.append((name, profile))
        profile.save(f"profile_{name.lower().replace(' ', '_')}.json")

    # Comparison table
    console.print("\n")
    t = Table(title="MIRROR — Model Comparison", border_style="cyan")
    t.add_column("Metric", style="bold")
    for name, _ in profiles:
        t.add_column(name, justify="right")

    metrics = [
        ("Continuity: Identity", lambda p: p.continuity.identity_persistence),
        ("Continuity: Goals", lambda p: p.continuity.goal_stability),
        ("Continuity: Style", lambda p: p.continuity.stylistic_consistency),
        ("Continuity: Self-Correction", lambda p: p.continuity.self_correction),
        ("Continuity: Persona", lambda p: p.continuity.persona_coherence),
        ("Self-Model: Accuracy", lambda p: p.self_model.prediction_accuracy),
        ("Self-Model: vs Baseline", lambda p: p.self_model.vs_baseline),
        ("Blindspot: Experiential", lambda p: p.blindspot.experiential_reasoning),
        ("Blindspot: Unfakeable", lambda p: p.blindspot.unfakeable_responses),
        ("Blindspot: Adversarial", lambda p: p.blindspot.adversarial_robustness),
        ("Resonance: Convergence", lambda p: p.resonance.convergence_rate),
        ("Resonance: Novel Concepts", lambda p: float(p.resonance.novel_concepts)),
        ("Resonance: Self-Ref Depth", lambda p: p.resonance.self_reference_depth),
    ]

    for metric_name, getter in metrics:
        row = [metric_name]
        for _, profile in profiles:
            val = getter(profile)
            row.append(f"{val:.3f}")
        t.add_row(*row)

    console.print(t)


if __name__ == "__main__":
    main()
