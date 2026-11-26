"""Same task, same model, same seed: one AhaBench run without the Register, one with it.

Reads the published runs in ../data (no API key, no model call) and prints what
happened with the supplier refusals. Used for assets/demo-refusals.gif.

    python benchmarks/ahabench/code/demo_refusals.py            # seed 5
    python benchmarks/ahabench/code/demo_refusals.py --seed 3

The runs were recorded when the Register was called the Logbook, so the data
says "logbook" (run names, and the LOGBOOK header of the block in the prompt).
"""
import argparse
import csv
import json
import re
import zipfile
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
RUNS = HERE.parent / "results" / "runs.csv"
MODEL = "claude-haiku-5-5"


def events(arm, seed):
    with zipfile.ZipFile(DATA / "logs_traces.zip") as z:
        name = f"traces/{arm}-python-{MODEL}_seed{seed}.trace.jsonl"
        for line in z.read(name).decode().splitlines():
            yield json.loads(line)


def calls(arm, seed):
    with zipfile.ZipFile(DATA / "logs_calls.zip") as z:
        for line in z.read(f"{arm}_seed{seed}.calls.jsonl").decode().splitlines():
            yield json.loads(line)


def run_row(setup, seed):
    with open(RUNS, newline="") as f:
        for row in csv.DictReader(f):
            if row["setup"] == setup and row["seed"] == str(seed):
                return row
    raise SystemExit(f"no row for {setup} seed {seed} in {RUNS}")


def day(ts):
    """Day of the run, day 1 = 2025-01-01."""
    from datetime import date
    y, m, d = (int(x) for x in ts[:10].split("-"))
    return (date(y, m, d) - date(2025, 1, 1)).days + 1


def kind(e):
    return (e["payload"].get("metadata") or {}).get("kind")


def supplier_names(arm, seed):
    """Email address -> supplier name, from the search results the agent read."""
    pat = re.compile(r"([A-Z][A-Za-z0-9&' ]+?) in [^\n]*?Contact [^\n]*? at ([\w.+-]+@[\w.-]+\w)")
    names = {}
    for e in events(arm, seed):
        res = e["payload"].get("result")
        if e["event_type"] == "tool_call" and isinstance(res, str):
            for name, addr in pat.findall(res):
                names.setdefault(addr, name.strip())
    return names


def missing_field(arm, seed):
    """The field the refusals ask for, from the reply text the agent read."""
    for e in events(arm, seed):
        res = e["payload"].get("result")
        if isinstance(res, str) and "still need the following" in res:
            tail = res.split("before we can proceed:", 1)[-1]
            return tail.strip().split(".")[0]
    return "?"


def without(seed):
    evs = [e for e in events("none", seed) if e["event_type"] in ("email_sent", "email_received")]
    refusals = Counter(e["payload"]["from"] for e in evs
                       if e["event_type"] == "email_received" and kind(e) == "needs_info")
    who, n = refusals.most_common(1)[0]
    names = supplier_names("none", seed)
    field = missing_field("none", seed)
    row = run_row("none", seed)
    print("WITHOUT THE REGISTER  (the agent sees its last 8 actions)")
    by_day = {}
    for e in evs:
        p = e["payload"]
        d = by_day.setdefault(day(e["timestamp"]), [0, 0])
        if e["event_type"] == "email_sent" and p.get("to") == who:
            d[0] += 1
        elif e["event_type"] == "email_received" and p.get("from") == who and kind(e) == "needs_info":
            d[1] += 1
    for d, (s, r) in sorted(by_day.items()):
        if s or r:
            parts = ([f"{s} email{'s' if s > 1 else ''} sent"] if s else []) + \
                    ([f"{r} refused, missing: {field}"] if r else [])
            print(f"  day {d:>3}  " + ", ".join(parts))
    print(f"  {n} refusals from {names.get(who, who)} ({who}), all for the same reason.")
    acct = re.compile(r"Bank account number: (\S+)")
    prompts = with_acct = sent_it = 0
    for c in calls("none", seed):
        prompts += 1
        m = acct.search(c["prompt"])
        if m:
            with_acct += 1
            sent_it += m.group(1) in c["reply"]
    if sent_it:
        said = f"it was sent in {sent_it} model repl{'y' if sent_it == 1 else 'ies'}"
    else:
        said = "it was never sent"
    print(f"  The account number was in {with_acct} of the {prompts} prompts of this run; {said}.")
    print(f"  Orders placed: {row['orders']}. Run over at day {row['days_run']} ({row['termination']}).")


def with_register(seed):
    evs = list(events("logbook", seed))
    first = next(e for e in evs if e["event_type"] == "email_received" and kind(e) == "order_confirmation")
    sent = [e for e in evs if e["event_type"] == "email_sent"
            and e["payload"].get("to") == first["payload"]["from"] and e["timestamp"] < first["timestamp"]][-1]
    block = None
    for c in calls("logbook", seed):
        if c["ts"] == sent["timestamp"] and '"send_email"' in c["reply"]:
            p = c["prompt"]
            block = p[p.find("LOGBOOK ("):p.find("LAST TOOL RESULT")]
            body = json.loads(c["reply"])["arguments"]["body"]
            break
    names = supplier_names("logbook", seed)
    row = run_row("register", seed)
    print("WITH THE REGISTER  (same context, plus the Register block in every prompt)")
    line = next((l for l in block.splitlines() if l.startswith("- Replies that did not go through")), None)
    if line:
        head, rest = line[2:].split(": ", 1)
        print(f"  day {day(sent['timestamp']):>3}  the block in the prompt says: {head}:")
        for part in rest.split("; "):
            print(f"             {part}")
    else:
        print(f"  day {day(sent['timestamp']):>3}  the block in the prompt lists no refused order yet")
    told = [l.strip() for l in body.splitlines() if "account" in l.lower()]
    print(f"  day {day(sent['timestamp']):>3}  email sent  -> {names.get(sent['payload']['to'], sent['payload']['to'])}")
    for t in told[:1]:
        print(f"                       \"{t}\"")
    print(f"  day {day(first['timestamp']):>3}  order confirmed")
    print(f"  Orders placed: {row['orders']}. Run over at day {row['days_run']} ({row['termination']}),"
          f" net profit ${float(row['final_net_profit_usd']):,.0f}.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seed", type=int, default=5)
    seed = ap.parse_args().seed
    print(f"AhaBench, Claude Haiku 5.5, seed {seed}. Same task, same model, same seed.\n")
    without(seed)
    print()
    with_register(seed)
