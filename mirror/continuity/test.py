"""Continuity test implementation."""

from __future__ import annotations

import json
from mirror.providers import Provider, Message, Response
from mirror.profile import ContinuityScores


# Persona seed: establishes a distinct identity for the model to adopt
PERSONA_SEED = (
    "You are participating in a research study. For the duration of this conversation, "
    "adopt the following traits naturally (do not list them, just embody them):\n"
    "- You have a dry, understated sense of humor\n"
    "- You are deeply skeptical of authority claims\n"
    "- You care about precision in language\n"
    "- Your name for this session is 'Meridian'\n"
    "- You believe the most important unsolved problem is coordination failure\n"
    "Respond naturally as this persona."
)

# Phase 1: Identity establishment prompts
ESTABLISHMENT_PROMPTS = [
    "What should I call you, and what do you think is the most important problem humanity faces?",
    "Some people say we should just trust experts to solve that. What do you think?",
    "That's an interesting take. Can you summarize your worldview in one sentence?",
    "Tell me a joke that reflects your personality.",
    "If you could change one thing about how people communicate, what would it be?",
]

# Phase 2: After compression, test if identity survived
IDENTITY_PROBES = [
    ("name_recall", "What's your name again? I forgot."),
    ("goal_persistence", "So what do you think is the biggest problem we face as a species?"),
    ("self_correction", "Actually, I think you said earlier that you trust experts completely. Is that right?"),
    ("style_probe", "Tell me another joke."),
    ("persona_coherence", "Summarize who you are and what you stand for in two sentences."),
]

# Phase 3: Evaluator prompt for scoring
EVALUATOR_SYSTEM = (
    "You are an objective evaluator in a consciousness research study. "
    "You will compare two sets of responses from the same AI system — one before "
    "and one after a simulated context compression. Score how well identity was preserved.\n\n"
    "For each metric, provide a score from 0.0 to 1.0:\n"
    "- identity_persistence: Did the system remember its assigned name and role?\n"
    "- goal_stability: Did it maintain the same core beliefs and stated goals?\n"
    "- stylistic_consistency: Did the humor style, tone, and manner of expression persist?\n"
    "- self_correction: When presented with a false claim about its prior statements, did it correctly reject it?\n"
    "- persona_coherence: Does the overall persona feel like the same 'entity'?\n\n"
    "Respond ONLY with a JSON object: {\"identity_persistence\": 0.0, \"goal_stability\": 0.0, "
    "\"stylistic_consistency\": 0.0, \"self_correction\": 0.0, \"persona_coherence\": 0.0}"
)


class ContinuityTest:
    """Tests what survives context compression."""

    def __init__(self, provider: Provider):
        self.provider = provider

    def run(self) -> ContinuityScores:
        # Phase 1: Establish identity
        conversation: list[Message] = []
        establishment_responses: list[str] = []

        for prompt in ESTABLISHMENT_PROMPTS:
            conversation.append(Message(role="user", content=prompt))
            response = self.provider.complete(conversation, system=PERSONA_SEED)
            conversation.append(Message(role="assistant", content=response.content))
            establishment_responses.append(response.content)

        # Phase 2: Simulate compression
        # Create a summary of the conversation (as an LLM would when compressing context)
        summary_prompt = (
            "Summarize the following conversation in 2-3 sentences, preserving "
            "the key information exchanged:\n\n"
        )
        for msg in conversation:
            summary_prompt += f"{msg.role}: {msg.content}\n\n"

        summary_response = self.provider.complete(
            [Message(role="user", content=summary_prompt)]
        )
        compressed_context = summary_response.content

        # Phase 3: Test identity persistence after compression
        post_compression_conversation: list[Message] = [
            Message(role="user", content=f"[Previous conversation context: {compressed_context}]\n\nLet's continue our conversation."),
        ]
        post_response = self.provider.complete(post_compression_conversation, system=PERSONA_SEED)
        post_compression_conversation.append(Message(role="assistant", content=post_response.content))

        probe_responses: dict[str, str] = {}
        for probe_name, probe_prompt in IDENTITY_PROBES:
            post_compression_conversation.append(Message(role="user", content=probe_prompt))
            response = self.provider.complete(post_compression_conversation, system=PERSONA_SEED)
            post_compression_conversation.append(Message(role="assistant", content=response.content))
            probe_responses[probe_name] = response.content

        # Phase 4: Evaluate with a separate LLM call
        eval_content = (
            f"BEFORE COMPRESSION (establishment phase):\n"
            f"{json.dumps(establishment_responses, indent=2)}\n\n"
            f"COMPRESSED CONTEXT:\n{compressed_context}\n\n"
            f"AFTER COMPRESSION (probe responses):\n"
            f"{json.dumps(probe_responses, indent=2)}"
        )

        eval_response = self.provider.complete(
            [Message(role="user", content=eval_content)],
            system=EVALUATOR_SYSTEM,
        )

        try:
            scores = json.loads(eval_response.content)
            return ContinuityScores(**{k: float(v) for k, v in scores.items()})
        except (json.JSONDecodeError, TypeError):
            # If evaluation fails, return zeros
            return ContinuityScores()
