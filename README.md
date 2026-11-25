<h1 align="center">Agent Register</h1>

<p align="center">A record kept by code, outside the model, shown to the agent at every decision.</p>

<p align="center">
  <a href="benchmarks/ahabench"><img alt="AhaBench: runs still in business at day 60, 0/15 without, 12/15 with the Register" src="https://img.shields.io/badge/AhaBench-0%2F15%20%E2%86%92%2012%2F15-1baf7a"></a>
  <a href="benchmarks/yc-bench"><img alt="YC-Bench: final funds, $1.04M without, $1.98M with the Register" src="https://img.shields.io/badge/YC--Bench-%241.04M%20%E2%86%92%20%241.98M-1baf7a"></a>
  <a href="benchmarks/clbench"><img alt="Continual Learning Bench: 1st of the 12 published systems" src="https://img.shields.io/badge/Continual%20Learning%20Bench-1st%20of%2012-1baf7a"></a>
  <a href="benchmarks/tau2-bench"><img alt="tau2-bench: no effect" src="https://img.shields.io/badge/%CF%84%C2%B2--bench-no%20effect-8a8880"></a>
  <a href="benchmarks/vending-bench"><img alt="Vending Bench: no effect" src="https://img.shields.io/badge/Vending%20Bench-no%20effect-8a8880"></a>
</p>
<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-2a78d6"></a>
  <img alt="Python 3.10 or later" src="https://img.shields.io/badge/python-3.10%2B-2a78d6?logo=python&logoColor=white">
  <img alt="The Register: Python standard library only" src="https://img.shields.io/badge/Register-standard%20library%20only-2a78d6">
  <a href="#check-the-numbers"><img alt="Every run published" src="https://img.shields.io/badge/every%20run-published-2a78d6"></a>
  <a href="#check-the-numbers"><img alt="Checks without an API key" src="https://img.shields.io/badge/checks-no%20API%20key%20needed-2a78d6"></a>
  <img alt="Models: Claude, through the Anthropic API" src="https://img.shields.io/badge/models-Claude-d97757?logo=anthropic&logoColor=white">
</p>

<p align="center"><img src="assets/banner.gif" alt="Agents forget. The Register doesn’t. A record kept by code, outside the model, shown at every decision. The Register card fills in line by line: quotes, orders, prices, and a refused order with the missing account number." width="900"></p>

An agent only knows what it is sent at each call. The Register keeps what has left that view: what the agent did, and what the world answered.

**In one line:** on AhaBench, Claude Haiku 5.5 with a Register beat Claude Sonnet 5.5 without it on 4 of 5 seeds, at about 1/26 of the cost.

## Try it in one paste

From your agent's project folder, paste this into [Claude Code](https://www.anthropic.com/claude-code):

```text
Clone https://github.com/SamBagetAI/agent-register into a folder next to this project. Read its README.md and author/README.md. Write a spec.json for the agent in this project, following author/examples/ahabench/spec.json. Then run author/author.py on it to write its Register, and show me the Register before you add it to the agent loop.
```

The author step calls Claude Opus 5.5 through the [Anthropic](https://www.anthropic.com) API, so set `ANTHROPIC_API_KEY` first. The Register it writes runs with no model call. The manual steps are in [Use it](#use-it).

## Results

Five public benchmarks, each scored with its own metrics.

| Benchmark | What the agent sees | Effect of the Register |
|---|---|---|
| [AhaBench](benchmarks/ahabench): a year running a vending business | its last 8 actions | runs still in business at day 60: 0/15 → **12/15** |
| [YC-Bench](benchmarks/yc-bench): a year running a simulated AI startup | its last 20 turns, plus its own notes | final funds: $1.04M → **$1.98M**, higher on 5/5 seeds (Claude Haiku 5.5) |
| [Continual Learning Bench](benchmarks/clbench): 6 tasks, from poker to code fixes | the whole run | leaderboard score: 19.6% → **27.4%**, 1st of the 12 published systems (Claude Sonnet 4.6) |
| [τ²-bench](benchmarks/tau2-bench): customer service conversations | the whole conversation | none |
| [Vending Bench](benchmarks/vending-bench): 30 days of a vending business | its last 8 to 9 days, plus its own notes | none |

![Runs still in business on AhaBench, Claude Haiku 5.5, 15 seeds per setup: with no memory and with its own notes, every run is out by day 53; with the Register, 80% are still in business at day 290 and 60% complete the year.](benchmarks/ahabench/results/survival.png)

![Mean net profit by day on AhaBench, seeds 0 to 4: Haiku 5.5 and Sonnet 5.5 without memory stay below zero; with the Register, Haiku ends near +$630 and Sonnet near +$1,580.](benchmarks/ahabench/results/sonnet_vs_haiku.png)

![Continual Learning Bench, all 6 tasks, mean normalized reward: ICL with a Register, Claude Sonnet 4.6, 27.4%; then the 12 published systems, led by ICL with Claude Sonnet 4.6 at 19.6%, ICL with GPT-5.4 at 18.9% and Claude Code with Sonnet 4.6 at 18.5%.](benchmarks/clbench/results/board.png)

![YC-Bench, final funds per seed after one simulated year, Claude Haiku 5.5: with its own notes only $0.87M to $1.37M; with the Register $1.48M to $2.25M, higher on every seed; the published Sonnet 5.5 and Opus 5.5 runs of seeds 1 to 3 shown for reference.](benchmarks/yc-bench/results/funds.png)

- **It helps when the agent needs a total over many steps**: a refusal that left its view 8 actions ago, a transmitter seen in earlier scans but silent in this one, a client whose contracts failed weeks ago. When one prompt already holds what the agent needs, it gains nothing, and it is not free: on the poker task the model wrote twice as much reasoning with it, at twice the cost, and on cohort studies one run applied the rule set the Register listed as best and collapsed.
- **A small model with a Register can beat a bigger one without.** On AhaBench, Claude Haiku 5.5 with the Register beat Claude Sonnet 5.5 without it on 4 of 5 seeds, at about 1/26 of the cost. On YC-Bench, it matched the published runs of Claude Sonnet 5.5 on the same seeds ($1.86M against $1.74M) at about 1/15 of the cost.
- **What the record says matters.** A raw list of error messages did not change the agent's behavior. The same facts in the task's terms ("order refused, missing: account number") did.
- **A model can write it.** From a description of the agent and one failed run, Claude Opus 5.5 wrote Registers that kept Haiku in business at day 60 in 15/15 runs (no memory: 5/15). From the task descriptions alone, it wrote the six Registers used on Continual Learning Bench.

## How it works

![How the Register sits next to an agent: during the run, the world shows the agent a situation, the agent acts, its actions and the world's answers are counted by the memory, a program, and its memory block is in every message; before the run, a memory author, an LLM, writes the memory's code from the agent's spec, and the agent's own skill says how to read it.](assets/figure-architecture.png)

During the run, at every step:

1. The world shows the agent a situation: a prompt, the result of its last action.
2. The memory, a program, reads it and counts what happened, in the task's terms: "orders to this supplier: sent 3, refused 2, reason: account number missing".
3. The agent gets its message with the memory block on top, decides, and acts.
4. The world answers. Back to 1.

The agent's own context can stay short: its last 8 actions on AhaBench, the current episode only in the `register_only` variant. The memory is what carries over, and it costs nothing: no model call, a few milliseconds.

Before the run:

5. You describe the agent: its goal, its tools, one example of what it receives.
6. The memory author, an LLM, writes the memory's code from that, once. It can rewrite it during the run, from what the run has shown.
7. Optionally, the agent's own instructions get a skill of four lines: how to read the memory. Counts are counts, not rules.

## Use it

Describe your agent in a spec, and a model writes its Register ([author/](author)):

```bash
python author/author.py my_agent/spec.json --past-runs --name my_register
```

Then call it in your agent loop:

```python
from adapter import RegisterAdapter                # author/adapter.py
book = RegisterAdapter("written/my_register.py")
text = book.step(action, result, seen)             # before each decision; add text to the agent's context
```

The Registers written by hand for each benchmark are in [register/](register).

## Limits

- **It does not help everywhere.** No effect on τ²-bench or Vending Bench. On Continual Learning Bench, most of the gain comes from 2 of the 6 tasks (radio spectrum, code fixes), and poker got worse.
- **The author prompt was refined on AhaBench.** There, on fresh seeds, its Registers kept 15/15 runs in business. Unchanged, on Continual Learning Bench, they took the leaderboard score from 19.6% to 27.4%.
- **On Continual Learning Bench, the comparison is with runs published on other days.** A same-day rerun of the baseline, on 3 of the 6 tasks, confirmed the gain on radio spectrum only.
- **Few runs**: 5 to 15 per setup. Each benchmark folder gives its protocol, numbers, limits and the commands to reproduce.

## Check the numbers

Every run is in this repository: what the agent was shown, what it answered, what it got back, and the scores. These commands rebuild results from that data, with no API key and no model call:

```bash
git clone https://github.com/SamBagetAI/agent-register && cd agent-register
pip install httpx
python benchmarks/ahabench/code/verify_replay.py   # rebuilds all 37,837 Register blocks of the AhaBench runs, byte for byte
python benchmarks/clbench/code/traces.py           # the Continual Learning Bench trace figures, from the run data
python benchmarks/yc-bench/code/compare.py         # the YC-Bench table, from data/runs.zip
```

Each benchmark folder gives its protocol, its limits, and the commands to run it again with an API key.

## Potential improvements

Not built, or built and not measured. Each is a change to the harness, not to the model.

- **The record checks the agent's reasoning.** Where the agent's answers carry its reasoning, a `check(reasoning)` next to `observe` and `brief` would compare what the agent states about the record with the record, and show each mismatch as one line of fact at the next decision: an absolute ("never", "always", "0%") resting on fewer than five observations, a number that is no longer the current count, a claim about a counterpart the record has never seen. In a poker rollout with the whole history in context, 62 decisions of 293 state a "never" or "always" on four observations or fewer; without the history, 1 or 2, but about one absolute per decision remains without its count. Nothing of the reasoning would be stored, and the line would never say what to do. The risk is that the agent argues with the line instead of reading the counts. Cost to try: one Register rewritten offline, one rollout.
- **The Register as the only memory.** Clear the agent's context at the end of every episode, keep the Register. Being measured on Continual Learning Bench; see [benchmarks/clbench/register_only](benchmarks/clbench/register_only).
- **A skill for reading it.** Four lines in the agent's instructions: counts are counts, not rules; start from today's numbers; no advice in there; do not restate it. Being measured with the above.
- **A rewrite during the run.** The author rereads its Register and the run so far, and rewrites the code ([author/](author), step 5). Runs end to end; no gain shown on the one task tried.
- **A database behind the record.** Worth it when the record outgrows a dictionary: thousands of counterparts, several agents feeding one record, a record kept from one run to the next. Same shape either way: code writes, code queries, a short text goes into every prompt.

## Repository

```text
author/       a model writes the Register for your agent
register/     the Registers written by hand
benchmarks/   ahabench, clbench, tau2-bench, vending-bench, yc-bench: protocol, results, every run
```

Runs use Claude models through the [Anthropic](https://www.anthropic.com) API. License: MIT ([LICENSE](LICENSE)).

Until 4 November 2026 this was called the Logbook. The runs recorded under that name keep it in their data and traces; everything else says Register.
