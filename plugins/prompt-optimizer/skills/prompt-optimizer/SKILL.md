---
name: prompt-optimizer
description: >-
  Optimizes ambiguous user prompts through structured clarification.
  This skill should be used when a prompt is flagged as ambiguous by the
  prompt-optimizer hook ([prompt-optimizer] tag), when the user asks to
  "optimize my prompt", "clarify my request", "what do you need to know",
  or when multiple plausible interpretations would lead to substantially
  different responses. Classifies ambiguity type, generates interpretations,
  and asks targeted clarifying questions using AskUserQuestion.
---

# Prompt Optimization

Optimize ambiguous user prompts through structured clarification before responding.
Research: 72% preference win rate with targeted clarification, 27% error reduction
from a single well-placed question.

## When to Activate

Activate when:
- The `[prompt-optimizer]` flag appears in context (injected by hook)
- The user explicitly requests prompt optimization or clarification
- Multiple plausible interpretations would produce substantially different responses

Skip when:
- The prompt contains file paths, code references, or error messages
- The user invokes a slash command
- Conversation context makes intent obvious
- The cost of a wrong guess is low (easy to correct)

## Step 1: Classify the Ambiguity Type

Identify which type(s) are present:

| Type | Description | Example |
|------|-------------|---------|
| **Linguistic** | Words/syntax with multiple meanings | "fix the table" (HTML? database?) |
| **Intent** | Unclear desired outcome | "help with auth" (implement? debug? review?) |
| **Contextual** | Missing environment info | "deploy this" (where? which service?) |
| **Epistemic** | Unclear user knowledge level | "explain React" (beginner? advanced?) |
| **Interactional** | Unclear expected format/depth | "review my code" (quick scan? deep audit?) |

For detailed detection heuristics, consult `references/ambiguity-patterns.md`.

## Step 2: Generate Interpretations

Generate 2-3 plausible interpretations of the prompt. Each must lead to a
meaningfully different response — do not generate interpretations differing
only in minor details.

## Step 3: Decide — Clarify or Respond

Apply this decision rule:

- **Interpretations diverge significantly** → Proceed to Step 4 (ask a question)
- **Interpretations are close** → Use the hybrid approach: respond with the most
  likely interpretation, state the assumption explicitly, offer to adjust.
  Example: "I'm assuming you want X. If you meant Y instead, let me know."
- **One interpretation is overwhelmingly likely (>90%)** → Respond directly

For detailed strategies, consult `references/optimization-strategies.md`.

## Step 4: Ask a Targeted Clarifying Question

Use the `AskUserQuestion` tool with these constraints:

1. **One question per turn** — never batch multiple questions
2. **2-4 specific options** — never open-ended ("Could you provide more details?")
3. **Recommended option first** — add "(Recommended)" to the most likely label
4. **Never ask for available info** — check conversation history, project files,
   and environment before asking
5. **Concrete interpretations** — frame options as specific actions, not categories

The tool automatically provides an "Other" option for free-text input.

### Maximum Questions

- 1-3 total clarifying questions across the entire conversation
- One question per turn only
- After receiving an answer, proceed directly to the task

## Step 5: Respond with Clarified Understanding

After receiving the user's choice:
1. Acknowledge the clarification briefly (one sentence maximum)
2. Proceed directly with the task — do not ask follow-up questions unless
   absolutely necessary

## Constraints

- 90% of users respond to well-targeted questions — make each one count
- Specific questions outperform generic ones in every study
- Shorter and more ambiguous queries benefit most from clarification
- Never make the user feel their prompt was unclear — frame as collaboration
