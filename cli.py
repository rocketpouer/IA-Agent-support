"""Command-line interface for the prototype."""
import argparse
from .agent import respond
from .llm import rewrite_with_llm


def main():
    parser = argparse.ArgumentParser(description="Fictional pharma support assistant")
    parser.add_argument("--llm", action="store_true", help="Use configured LLM for approved answers")
    args = parser.parse_args()
    print("Pharma Support Assistant (fictional demo). Type 'exit' to quit.")
    while True:
        try:
            question = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
        if question.lower() in {"exit", "quit"}:
            break
        result = respond(question)
        answer = result["answer"]
        if args.llm and result["status"] == "answered":
            try:
                answer = rewrite_with_llm(question, answer)
            except Exception as exc:
                print(f"[LLM unavailable; using approved answer: {type(exc).__name__}]")
        print(f"Assistant [{result['status']}]: {answer}")
        if result["source"]:
            print(f"Source: {result['source']}")


if __name__ == "__main__":
    main()
