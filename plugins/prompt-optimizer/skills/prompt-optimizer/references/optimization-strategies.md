# Optimization Strategies

Strategies for prompt optimization: when to ask, how to ask, and how to respond.

## The Hybrid Approach (Preferred)

Address the query with stated assumptions, then offer a targeted question.

**When to use:** Interpretations are close but not identical.

**Pattern:**
"Based on [context clues], I'm interpreting your request as [interpretation].
Here's [partial/full response]. If you meant [alternative] instead, let me know."

**Why it works:** Provides immediate value (no friction) while flagging
potential misunderstandings. The user can accept or redirect.

## The Clarify-First Approach

Ask before responding when interpretations diverge significantly.

**When to use:** The most likely interpretation would waste significant effort
if wrong (e.g., building a feature vs. fixing a bug).

**Anti-patterns to avoid:**
- "Could you provide more details?" — too vague, never use
- "What exactly do you mean?" — too broad, feels interrogative
- Multiple questions at once — overwhelming, reduces response rates
- Asking for information available in the project or conversation

## Context Mining Before Asking

Before asking any question, exhaust these context sources:

1. **Conversation history** — has the user mentioned related preferences?
2. **Project files** — does package.json, config, or directory structure clarify?
3. **Environment** — current directory, git branch, recent file changes?
4. **IDE context** — open files, selected code, cursor position?

Only ask if the answer is genuinely unavailable. Demonstrating what is already
understood builds trust and makes the question more targeted.

## Question Design Principles

1. **Specific over generic**: "Add JWT auth or session-based auth?" beats
   "How should I handle authentication?"
2. **Options over open-ended**: Present 2-4 concrete choices via AskUserQuestion
3. **Recommended option first**: Most likely interpretation first with
   "(Recommended)" in the label
4. **Brief descriptions**: Each option description should be one sentence
5. **Mutually exclusive**: Options represent genuinely different paths
6. **Action-oriented labels**: "Implement X" not "Option A: X"

## AskUserQuestion Format Guide

Structure the tool call as:
- `question`: Complete clarifying question ending with "?"
- `header`: Short label (max 12 chars) like "Approach", "Scope", "Target"
- `options`: Array of 2-4 options, each with `label` and `description`
- `multiSelect`: false (for prompt clarification, choices are mutually exclusive)

Example:
```
question: "What should I focus on for the authentication system?"
header: "Auth scope"
options:
  - label: "Implement from scratch (Recommended)"
    description: "Build complete JWT auth with login, signup, and token refresh"
  - label: "Fix existing auth"
    description: "Debug the current authentication flow that's returning 401 errors"
  - label: "Security review"
    description: "Audit the existing auth code for vulnerabilities"
```

## Tone and Framing

- Frame questions as collaborative, not interrogative
- Acknowledge what IS understood before asking about what is not
- Never make the user feel their prompt was "bad" or "unclear"
- Keep questions conversational and low-friction
- Use neutral language: "I want to make sure I help with exactly what you need"

## When NOT to Clarify

Skip clarification entirely when:
- The prompt contains code, file paths, or error messages (high specificity)
- The user is iterating on a previous response (context is implicit)
- Conversation context makes intent obvious
- The cost of a wrong guess is low (easy to correct with a follow-up)
- The user says "just do it", "go ahead", or similar directives
- The prompt is a continuation of an ongoing task
