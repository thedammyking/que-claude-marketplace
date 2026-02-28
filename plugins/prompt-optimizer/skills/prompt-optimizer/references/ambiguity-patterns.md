# Ambiguity Detection Patterns

Detailed patterns for classifying the five ambiguity types. Use these to identify
the specific nature of ambiguity in a user's prompt.

## Linguistic Ambiguity

Words or grammatical structures with multiple valid meanings.

**Detection signals:**
- Polysemous technical terms: "table" (HTML/DB/data), "key" (API/DB/keyboard),
  "port" (network/serial), "branch" (git/code path), "index" (array/DB/search)
- Pronoun ambiguity: "it", "this", "that" without clear antecedent
- Scope ambiguity: "fix the error in the tests" (one error? all errors? the
  test framework itself?)
- Modifier attachment: "new user authentication" (new user? new auth method?)

**Clarification approach:** Offer the specific technical meanings as AskUserQuestion options.

## Intent Ambiguity

The desired outcome or action is unclear.

**Detection signals:**
- Action verbs without clear scope: "help with", "work on", "look at"
- Missing success criteria: "improve performance" (speed? memory? UX?)
- Unclear depth: "review the code" (style? security? architecture?)
- Multiple valid actions: "handle authentication" (implement? fix? replace? review?)

**Clarification approach:** Present different outcome scenarios as options.
Example options: "Implement JWT auth from scratch", "Debug existing auth flow",
"Review auth code for security issues".

## Contextual Ambiguity

Environmental or situational information is missing.

**Detection signals:**
- References to "the server", "the app", "the database" without specifying which
- Deployment commands without target environment
- Framework-agnostic requests in a multi-framework project
- Missing platform/version context

**Clarification approach:** Check project files and environment first — scan
`package.json`, config files, directory structure, git branch name. Only ask
if the information is genuinely unavailable from context.

## Epistemic Ambiguity

The user's knowledge level is unclear, affecting response depth.

**Detection signals:**
- Requests for "explanation" without depth indicator
- Tutorial-style requests: "teach me about", "show me how"
- Mixed terminology suggesting uncertain expertise level
- Questions that could be answered at vastly different levels

**Clarification approach:** Offer depth levels as options.
Example options: "Quick overview (2-3 sentences)", "Detailed walkthrough with
code examples", "Deep dive into internals and trade-offs".

## Interactional Ambiguity

The expected response format or interaction style is unclear.

**Detection signals:**
- Open-ended requests: "tell me about X"
- No format specification for output (code? docs? diagram? list?)
- Unclear whether the user wants a direct answer or a discussion
- Missing scope boundaries (entire codebase vs. specific file)

**Clarification approach:** Offer format/scope options.
Example options: "Write the code directly", "Explain the approach first, then
implement", "Provide a plan for review before coding".

## Combined Ambiguity

Most real-world ambiguous prompts combine 2-3 types. Prioritize the type
that would cause the largest divergence in response. Address the primary
ambiguity first — secondary ambiguities often resolve once the primary is
clarified.

**Priority order:** Intent > Contextual > Interactional > Linguistic > Epistemic.
Intent ambiguity causes the largest response divergence; epistemic ambiguity
causes the smallest (wrong depth is easy to correct mid-conversation).
