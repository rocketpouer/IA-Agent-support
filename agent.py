"""Simple retrieval-grounded support agent using synthetic data."""
import json
import re
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "faq.json"

# Conservative demonstration rules. Not sufficient for production triage.
SAFETY_PATTERNS = [
    r"\b(side effect|adverse event|reaction|symptom|overdose|dosage|dose|pregnan|medical advice|prescription|treatment|allerg|hurt|sick)\b",
    r"\b(damaged|contaminated|defective|broken seal|wrong medication|wrong product|quality complaint)\b",
]
STOPWORDS = {"a", "an", "the", "i", "my", "to", "do", "can", "how", "is", "what", "where",
             "please", "for", "of", "on", "in", "you", "me", "and", "it"}


def tokenize(text):
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOPWORDS


def load_faq(path=DATA_FILE):
    with Path(path).open(encoding="utf-8") as f:
        return json.load(f)


def requires_human_review(question):
    q = question.lower()
    return any(re.search(pattern, q) for pattern in SAFETY_PATTERNS)


def retrieve(question, faq=None):
    faq = load_faq() if faq is None else faq
    words = tokenize(question)
    ranked = []
    for item in faq:
        terms = set(item["keywords"]) | tokenize(item["topic"])
        score = len(words & terms)
        if score:
            ranked.append((score, item))
    if not ranked:
        return None
    ranked.sort(key=lambda x: (-x[0], x[1]["id"]))
    return ranked[0][1]


def respond(question, faq=None):
    if not question.strip():
        return {"status": "clarify", "answer": "Please enter a question.", "source": None}
    if requires_human_review(question):
        return {
            "status": "escalate",
            "answer": "This request may involve medical or product safety information. "
                      "Please contact a qualified healthcare professional or the appropriate "
                      "customer safety/support team. This demo cannot provide medical guidance.",
            "source": None,
        }
    item = retrieve(question, faq)
    if item is None:
        return {
            "status": "escalate",
            "answer": "I could not find an approved answer. Please contact the support team.",
            "source": None,
        }
    return {"status": "answered", "answer": item["answer"], "source": item["id"]}
