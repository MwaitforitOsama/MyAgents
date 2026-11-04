#!/usr/bin/env python3
"""Mason guard launcher: the PreToolUse hook registered in settings.json.

It only checks the agent, then loads the real rules from mason_rules.py. If the rules
can't load or crash (a bad edit, a syntax error), it asks the user instead of exiting with
an error, because Claude Code treats a hook that errors as non-blocking: it would let
the tool call through.
"""

import json
import os
import sys

AGENT = "mason"


def fail(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": "Mason guard could not load its rules (%s), so this needs the user's "
                                    "approval. Tell the user the guard is broken." % reason,
    }}))
    return 0


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0  # not our input to judge; never break normal sessions
    if data.get("agent_type") != AGENT:
        return 0
    try:
        sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
        import mason_rules
        return mason_rules.main(data)
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 2
    except BaseException as e:  # noqa: BLE001 - fail closed on anything
        return fail("%s: %s" % (type(e).__name__, e))


if __name__ == "__main__":
    sys.exit(main())
