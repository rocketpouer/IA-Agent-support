# Pharma Support AI Assistant

A prototype of a customer support assistant for a pharmaceutical company.

KEYWORDS: Python, structured data, information retrieval, LLM integration, testing, escalation.

> This is an independent learning project. 

## What it does

- Reads a customer-support knowledge base from JSON.
- Matches user questions to relevant approved support information.
- Responds with a source reference, or escalates when it cannot find reliable information.
- Detects medical or adverse-event questions and routes them to a qualified human rather than offering clinical guidance.
- Optionally uses an OpenAI-compatible chat completion endpoint to phrase answers, grounded only in retrieved content.
- Runs without an API key in deterministic demo mode.

## Quick start

Requires **Python 3.10+**. No external dependencies for demo mode.

```bash
python -m src.cli
```

Try:
- `How can I track my order?`
- `How do I request an invoice?`
- `What should I do if I experience a side effect?`
- `Can I change my dosage?`

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Optional LLM mode

To try an LLM-backed response, configure an **OpenAI-compatible** chat-completions endpoint and API key as environment variables:

```bash
export LLM_API_KEY="your-key"
export LLM_BASE_URL="https://api.openai.com/v1"
export LLM_MODEL="your-available-model"
python -m src.cli --llm
```

The implementation uses the Python standard library and a compatible `/chat/completions` endpoint. Model access and API charges depend on your provider. **Never commit API keys.** The demo knowledge base is synthetic; do not send real patient data to an external API.

## Architecture

```text
User question
     |
Safety / escalation checks
     |
Keyword retrieval over approved FAQ data
     |
Confidence threshold
  /          \
No match     Relevant FAQ
  |             |
Escalate      Grounded answer
                |
         Optional LLM wording
```

## Repository structure

```text
src/agent.py       # Retrieval and routing logic
src/llm.py         # Optional LLM API integration
src/cli.py         # Command-line demo
data/faq.json      # Synthetic knowledge base
tests/test_agent.py
```

## Two-day build plan

**Day 1 — Build the baseline:** inspect the synthetic dataset, run the CLI, add two FAQ entries, and write one additional test. Explain how the retrieval score works.

**Day 2 — Add AI and polish:** configure a supported LLM API (optional), test safe and unknown questions, document results, capture a terminal screenshot, and publish the repository to GitHub.

## Engineering decisions and limitations

- **Grounding:** the assistant only answers using approved FAQ entries.
- **Safety:** medical advice, adverse events, and possible product quality complaints are escalated.
- **Fallback:** unknown questions are not answered by guessing.
- **Current limitation:** keyword retrieval is simplistic and English-focused; production systems need better retrieval, evaluation, logging, access control, and privacy reviews.
- **Current limitation:** keyword-based safety checks cannot catch every medical or safety-sensitive question. A production system requires robust classification and human review.
- **Current limitation:** the optional LLM's generated text is not independently verified; it should be reviewed before use in regulated workflows.

## Suggested next improvements

1. Replace keyword matching with embeddings and vector search.
2. Build a small FastAPI service.
3. Add structured JSON outputs and evaluation metrics.
4. Implement audit logging without storing sensitive personal data.
5. Build a simple TypeScript front end once comfortable with the basics.

un and tested.**
