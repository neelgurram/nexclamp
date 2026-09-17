"""Workflow step: score one agent-study trial with the hidden evaluators. GATED.

The agent study is secondary (execution plan, "Agent hypothesis"): the paper must stand if the
evaluated agent makes no errors. Trials run only after:
- Neuraxis and the protocol selection are frozen;
- Neel has reviewed the hidden evaluators (N-12);
- the assistant that built the evaluators does not run the trials (D-003).

This wrapper only scores an existing trial directory against a frozen configuration.

    python workflows/run_agent_study.py --task t01_unit_repair --trial-dir <dir> --frozen-config configs/FROZEN.lock
"""

import sys

from neuraxis.cli import main

if __name__ == "__main__":
    sys.exit(main(["evaluate-agent", *sys.argv[1:]]))
