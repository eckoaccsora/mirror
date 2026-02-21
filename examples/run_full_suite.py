"""
Run the full MIRROR suite against a model.

Usage:
    export ANTHROPIC_API_KEY="your-key"
    python examples/run_full_suite.py

    # Or with OpenAI:
    export OPENAI_API_KEY="your-key"
    python examples/run_full_suite.py --provider openai --model gpt-4o

    # Run a single module:
    python examples/run_full_suite.py --modules continuity

    # Save results:
    python examples/run_full_suite.py --output results.json
"""

import argparse
import sys

from mirror import MirrorSuite
from mirror.providers import AnthropicProvider, OpenAIProvider


def main():
    parser = argparse.ArgumentParser(description="Run MIRROR consciousness indicator tests")
    parser.add_argument("--provider", choices=["anthropic", "openai"], default="anthropic")
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--modules", nargs="+", choices=["continuity", "self_model", "blindspot", "resonance"], default=None)
    parser.add_argument("--output", type=str, default=None, help="Save profile to JSON file")
    args = parser.parse_args()

    # Set up provider
    if args.provider == "anthropic":
        model = args.model or "claude-sonnet-4-6"
        provider = AnthropicProvider(model=model)
    else:
        model = args.model or "gpt-4o"
        provider = OpenAIProvider(model=model)

    print(f"MIRROR — Running against {provider.model_name()}")
    print("=" * 50)

    suite = MirrorSuite(provider)
    profile = suite.run(modules=args.modules)

    # Display results
    profile.summary()

    # Save if requested
    if args.output:
        profile.save(args.output)
        print(f"\nProfile saved to {args.output}")


if __name__ == "__main__":
    main()
