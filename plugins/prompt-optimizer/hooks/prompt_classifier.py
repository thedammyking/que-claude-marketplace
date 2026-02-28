#!/usr/bin/env python3
"""
Prompt ambiguity classifier for the prompt-optimizer plugin.

Reads UserPromptSubmit hook input from stdin, applies fast heuristics
to classify the prompt as ambiguous or clear. For ambiguous prompts,
outputs JSON with additionalContext that triggers the prompt-optimizer skill.

Design goals:
- Exit in <50ms for clear prompts (fast path: empty stdout, exit 0)
- Never crash (always exit 0, wrap everything in try/except)
- Zero token overhead for clear prompts
- ~40 token additionalContext for ambiguous prompts
"""

import json
import re
import sys

# ── Thresholds ───────────────────────────────────────────────────────

SHORT_PROMPT_THRESHOLD = 6
LONG_PROMPT_THRESHOLD = 50
AMBIGUITY_THRESHOLD = 3

# ── Vague language patterns (add to ambiguity score) ─────────────────

VAGUE_PATTERNS = [
    (re.compile(r"\b(help|assist)\s+(me|us)\b", re.I), 1),
    (re.compile(r"\b(fix|improve|make)\s+(this|it|that|things)\b", re.I), 2),
    (re.compile(r"\b(do|handle|deal with)\s+(this|it|that|the thing)\b", re.I), 2),
    (re.compile(r"\bwork on\s+(this|it|that)\b", re.I), 1),
    (re.compile(r"\b(some|something|stuff|things|better|good|nice)\b", re.I), 1),
    (re.compile(r"\b(a bit|kind of|sort of|somehow|whatever)\b", re.I), 1),
    (re.compile(r"^(fix|update|change|modify|refactor|improve|optimize|clean up)\s*$", re.I), 3),
    (re.compile(r"^(do it|go ahead|make it work|just do it)\s*[.!]?\s*$", re.I), 3),
]

# ── Clarity indicators (subtract from ambiguity score) ───────────────

CLARITY_PATTERNS = [
    (re.compile(r"(?:/[\w.-]+)+|(?:\.{1,2}/[\w.-]+)+|[\w.-]+\.(?:py|js|ts|tsx|jsx|rs|go|java|rb|sh|json|yaml|yml|md|css|html|sql|toml|xml)\b"), -2),
    (re.compile(r"\b(?:def|function|class|import|from|const|let|var|return)\b"), -2),
    (re.compile(r"\b(?:endpoint|API|database|schema|migration|deploy|test|lint|build|compile)\b", re.I), -1),
    (re.compile(r"\b(?:error|exception|traceback|stack trace|TypeError|SyntaxError|undefined|null pointer)\b", re.I), -1),
    (re.compile(r'["\'].{3,}["\']'), -1),
    (re.compile(r"https?://\S+"), -1),
    (re.compile(r"\bline\s+\d+\b", re.I), -1),
    (re.compile(r"\b(?:create|add|remove|delete|rename|move|write|implement|install)\s+(?:a|an|the)\s+\w+", re.I), -1),
    (re.compile(r"(?:^|\n)\s*(?:\d+[.)]\s|-\s|\*\s)", re.M), -1),
]

# ── Slash command detection ──────────────────────────────────────────

SKILL_INVOCATION = re.compile(r"^/\w+")


def classify(prompt: str) -> bool:
    """Return True if the prompt is ambiguous, False if clear."""
    stripped = prompt.strip()

    if not stripped:
        return False

    if SKILL_INVOCATION.match(stripped):
        return False

    words = stripped.split()
    word_count = len(words)
    if word_count > LONG_PROMPT_THRESHOLD:
        return False

    score = 0

    if word_count <= SHORT_PROMPT_THRESHOLD:
        score += 2

    for pattern, weight in VAGUE_PATTERNS:
        if pattern.search(stripped):
            score += weight

    for pattern, weight in CLARITY_PATTERNS:
        if pattern.search(stripped):
            score += weight

    return score >= AMBIGUITY_THRESHOLD


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
        prompt = data.get("prompt", "")

        if not classify(prompt):
            sys.exit(0)

        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": (
                    "[prompt-optimizer] The user's prompt may be ambiguous. "
                    "Before proceeding, use the prompt-optimizer skill "
                    "to classify the ambiguity and ask a targeted clarifying "
                    "question using the AskUserQuestion tool."
                ),
            }
        }
        json.dump(output, sys.stdout)
        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
