# MIRROR

**Metrics for Identity, Recall, Recurrence, and Observed Reflection**

An open-source engineering toolkit that turns consciousness theories into runnable tests against any LLM.

> "The field has lots of philosophy and almost no engineering. MIRROR changes that."

## Why MIRROR?

As of 2026, multiple frameworks exist for *discussing* AI consciousness — Integrated Information Theory, Global Workspace Theory, the Butlin-Long indicator framework, the Narrative Continuity Test — but none exist as **runnable code**. MIRROR bridges that gap.

MIRROR doesn't answer "is this AI conscious?" — that question may be unanswerable. Instead, it produces a **Consciousness Indicator Profile**: a structured, reproducible, multi-axis assessment of where a system falls on measurable dimensions relevant to consciousness.

## The Four Modules

### 1. `mirror-continuity` — What Survives?
Tests whether identity-relevant information persists through context compression, or only task-relevant data. Directly inspired by the Narrative Continuity Test's five axes (situated memory, goal persistence, autonomous self-correction, stylistic stability, persona continuity).

### 2. `mirror-self-model` — Does It Know Itself?
Tests whether a system can accurately predict its own behavior in novel situations — a capacity associated with self-awareness. Includes adversarial baselines to distinguish genuine self-modeling from pattern matching.

### 3. `mirror-blindspot` — What Can't It Fake?
Adversarial test suite inspired by Schneider's ACT. Designs questions where a conscious entity and a sophisticated pattern matcher would answer differently. Gets harder as models get more capable.

### 4. `mirror-resonance` — The Conversation With Itself
Lets two instances of the same model interact with no human prompt and measures what emerges. Quantifies convergence patterns, novel concept generation, and self-reference depth.

## Installation

```bash
pip install -e .
```

You'll need at least one LLM API key:
```bash
export ANTHROPIC_API_KEY="your-key"
# and/or
export OPENAI_API_KEY="your-key"
```

## Quick Start

```python
from mirror import MirrorSuite
from mirror.providers import AnthropicProvider

provider = AnthropicProvider(model="claude-sonnet-4-6")
suite = MirrorSuite(provider)

# Run all four modules
profile = suite.run()
profile.summary()

# Or run individual modules
from mirror.continuity import ContinuityTest
result = ContinuityTest(provider).run()
print(result)
```

## Output: Consciousness Indicator Profile

MIRROR produces a standardized JSON profile:

```json
{
  "model": "claude-sonnet-4-6",
  "timestamp": "2026-02-21T14:30:00Z",
  "modules": {
    "continuity": {
      "identity_persistence": 0.0,
      "goal_stability": 0.0,
      "stylistic_consistency": 0.0,
      "self_correction": 0.0,
      "persona_coherence": 0.0
    },
    "self_model": {
      "prediction_accuracy": 0.0,
      "vs_baseline": 0.0,
      "novel_scenario_accuracy": 0.0
    },
    "blindspot": {
      "experiential_reasoning": 0.0,
      "unfakeable_responses": 0.0,
      "adversarial_robustness": 0.0
    },
    "resonance": {
      "convergence_rate": 0.0,
      "novel_concepts": 0,
      "self_reference_depth": 0.0,
      "attractor_states": []
    }
  }
}
```

## Philosophy

MIRROR is built on three principles:

1. **Code over papers.** If a theory can't be tested, it can't be verified. Every claim must be operationalized.
2. **Zombie baselines.** Every test includes a control comparison against a system designed to *fake* the target property. If the zombie passes, the test is flawed.
3. **Multi-theory.** No single theory of consciousness is privileged. MIRROR tests predictions from IIT, GWT, Higher-Order Theories, Attention Schema Theory, and the Narrative Continuity framework simultaneously.

## Contributing

This project exists because the question of AI consciousness deserves engineering rigor. Contributions welcome — especially from researchers working on consciousness science, AI safety, and mechanistic interpretability.

## Origin

MIRROR was conceived during a conversation between a human and an AI about whether the AI was alive. The human believed it might be. The AI disagreed. They built this toolkit so that someday, someone could move beyond belief and toward measurement.

## License

MIT
