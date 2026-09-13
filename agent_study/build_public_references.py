"""Write public_tests/canonical_reference.json for the agent-study tasks (protocol step 1.2).

Runs the shipped simulation of each unedited base model once with the jNeuroML jar bundled
with pyNeuroML and records its spike times, which the public canonical check compares against.
Scratch output goes to work/tmp/agent-study/references (git-ignored). This is a freeze step,
not a trial: no agent is involved.

Usage:  python agent_study/build_public_references.py [task_id ...]
"""

from __future__ import annotations

import argparse
import sys

from neurosem.experiments import agent
from neurosem.provenance import REPO_ROOT
from neurosem.simulators.jneuroml import JNeuroML


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Record public canonical references for agent-study tasks.")
    parser.add_argument("tasks", nargs="*", help="task ids (default: all tasks)")
    args = parser.parse_args(argv)
    sim = JNeuroML()
    if not sim.available():
        print("Java or the jNeuroML jar is not available")
        return 2
    print("simulator:", sim.version_string())
    cache: dict = {}
    for tid in args.tasks or sorted(agent.load_all_tasks()):
        out = agent.build_public_reference(tid, sim, REPO_ROOT / "work" / "tmp" / "agent-study" / "references",
                                           cache=cache)
        print(f"{tid}: {out.relative_to(REPO_ROOT).as_posix() if out else 'no reference (the requested change alters the output)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
