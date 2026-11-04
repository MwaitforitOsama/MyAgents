#!/usr/bin/env python3
"""Runs guard-cases.txt against plumb_guard.py. Exit 0 if every case matches."""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
GUARD = os.path.join(HERE, "..", "plumb_guard.py")
REPO = os.path.realpath(os.path.join(HERE, "..", "..", ".."))
CWD = "/Users/me/proj"


def run(agent, tool, value):
    payload = {"hook_event_name": "PreToolUse", "tool_name": tool, "cwd": CWD,
               "tool_input": {"command": value} if tool == "Bash" else {"file_path": value}}
    if agent != "-":
        payload["agent_type"] = agent
    proc = subprocess.run([sys.executable, GUARD], input=json.dumps(payload),
                          capture_output=True, text=True)
    return proc.returncode, proc.stderr.strip()


def main():
    failures = total = 0
    verbose = "-v" in sys.argv
    with open(os.path.join(HERE, "guard-cases.txt")) as f:
        for n, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            expect, agent, tool, value = line.split("\t", 3)
            value = value.replace("{REPO}", REPO).replace("\\n", "\n")
            code, err = run(agent, tool, value)
            got = {0: "ALLOW", 2: "BLOCK"}.get(code, "ERROR(%d)" % code)
            total += 1
            if got != expect:
                failures += 1
                print("FAIL line %d: expected %s, got %s\n  %s %s\n  %s" % (n, expect, got, tool, value, err))
            elif verbose:
                print("ok   %s %s" % (expect, value))
    print("%d/%d guard cases passed" % (total - failures, total))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
