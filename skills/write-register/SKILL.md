---
name: write-register
description: Write a Register for the agent in this project. A Register is a record kept by code, outside the model, shown to the agent at every decision. Use when the user wants their agent to keep track of what it did and what the world answered, beyond what stays in its context.
---

# Write a Register for this agent

A Register is a Python class with `observe(step)` and `brief()`. It reads what the agent was shown after each action, keeps a record in the task's terms, and puts a short summary of that record on top of every model call. It makes no model call itself.

Steps:

1. Get the author code. If this project has no copy yet, clone https://github.com/SamBagetAI/agent-register into a folder next to this project. Read its `README.md` and `author/README.md`.
2. Find the agent in this project: its goal, its instructions (system prompt), its tools, and what it keeps in view from one step to the next. Ask the user for anything you cannot find.
3. Write a `spec.json` for it, following `author/examples/ahabench/spec.json` and the field table in `author/README.md`. Add one example step exactly as the agent receives it. Add a past run if the user has one.
4. Check that `ANTHROPIC_API_KEY` is set. The author step calls Claude Opus 5.5 through the Anthropic API (https://www.anthropic.com); the Register it writes does not.
5. Run `python author/author.py <path to spec.json> --name <register name>` (add `--past-runs` when the spec has a past run).
6. Show the user the Register that was written, and the block it prints for the example step, before you change their agent.
7. Only after the user agrees: add it to the agent loop with `author/adapter.py`, as shown in the README's "Use it" section. The Register's text goes into the agent's context before each decision.

Keep these rules from the README:

- The Register only reads what the agent was shown. Never the environment's internal state.
- Counts are counts, not rules. The Register says what happened; it does not tell the agent what to do.
- It helps when the agent needs a total over many steps. When one prompt already holds everything, expect no gain.
