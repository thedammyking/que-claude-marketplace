# prompt-optimizer

A Claude Code plugin that detects ambiguous prompts and guides Claude through structured clarification to improve response quality.

## What It Does

When you submit a prompt, a lightweight Python hook classifies it as clear or ambiguous using fast heuristics. Clear prompts pass through with zero overhead. Ambiguous prompts trigger the prompt-optimizer skill, which guides Claude to:

1. Classify the ambiguity type (linguistic, intent, contextual, epistemic, interactional)
2. Generate 2-3 possible interpretations
3. Ask a targeted clarifying question using the native question prompt
4. Respond with the clarified understanding

## Research-Backed Design

Based on prompt optimization research showing:

- **72%** preference win rate with targeted clarification (Stanford STaR-GATE)
- **90%** user response rate to well-targeted questions (Haptik production data)
- **27%** error reduction from a single clarifying question

## Installation

Add the marketplace:

```
/plugin marketplace add thedammyking/que-claude-marketplace
```

Install the plugin:

```
/plugin install prompt-optimizer@que-claude-marketplace
```

## How It Works

### Hook: Prompt Classifier

- Fires on every `UserPromptSubmit` event
- Applies fast heuristics (word count, vague patterns, clarity indicators)
- Exits silently for clear prompts (<50ms, zero token cost)
- Injects context for ambiguous prompts (~40 tokens)

### Skill: Prompt Optimizer

- Triggered by the hook's context injection or natural ambiguity detection
- Classifies five ambiguity types
- Uses the hybrid approach: respond with assumptions when interpretations are close
- Asks structured questions with native question prompt (2-4 options, never open-ended)
- Limits to one question per turn, max 1-3 total

## Token Budget

| Scenario | Cost |
|----------|------|
| Clear prompt | ~100 words (skill metadata only) |
| Ambiguous prompt | ~2,100 words (metadata + skill body + hook context) |
| Deep optimization | +reference files loaded as needed |

## Requirements

- Python 3.6+ (uses only standard library)
