# AI Use Log

This log records every substantive use of generative AI in NeuroSem. IEEE requires that
the selected venue's AI-disclosure policy be followed. That policy is verified in
`DEPENDENCY_AUDIT.md` / `PRIOR_ART_AUDIT.md` and must be re-checked at submission. Only
humans are authors, and the human author is responsible for all content.

**Two roles of AI in this project must never be mixed:**

1. **Development assistant.** Claude Code helps plan, audit, write software and write
   documents. Everything it produces is reviewed by Neel. This role is logged below.
2. **Experimental subject** (Milestone 9 only, optional). Frozen, isolated Claude Code
   trials scored by hidden tests. These are logged separately under
   `results/agent_study/` with full transcripts. None exist yet.

---

## Entry 001 — Milestone 0 audit

| Field | Value |
|---|---|
| Date | 2026-09-13 |
| Human operator | Neel Gurram |
| Tool | Claude Code (desktop app, Windows 11) |
| Model | Claude Opus 5 (`claude-opus-5`); subagents inherit the same model |
| Mode | Multi-agent "workflow" orchestration (ultracode), run ID `wf_4db58141-488` (research phase) |
| Input | `NEUROSEM_CLAUDE_HANDOFF.pdf` (SHA-256 `ba1db26a…d054d`) |
| Branch | `m0-audit` |
| Permissions | Web search/fetch, local shell, file writes restricted to this repo and a temporary scratch folder; no system-wide installs |

**What the AI did**
- Extracted the handoff text (pypdf) and archived the original PDF.
- Ran parallel research agents to verify tool versions, licenses and APIs from primary
  sources (PyPI JSON API, GitHub, official docs). A second, independent agent fact-checked
  each report, including installing packages in throwaway virtual environments to inspect
  real APIs.
- Ran a multi-source prior-art sweep (Google Scholar/Semantic Scholar, PubMed/bioRxiv/
  Europe PMC, IEEE Xplore/ACM DL/DBLP, arXiv/OpenAlex, GitHub/PyPI/Zenodo, citation
  snowballing, adjacent fields). It added a deep-read verification pass per candidate, a
  completeness critic with gap rounds, and adversarial "anticipation" and "obviousness"
  reviews of the closest works.
- Searched for project-name conflicts and screened fixture models for license and
  provenance.
- Critiqued the handoff through five lenses (statistics, neuroscience, numerics,
  software testing, integrity/venue), with an adversarial skeptic per lens.
- Drafted the Milestone 0 documents from the saved evidence.

**What the AI did not do**
- It generated no data, simulations or results, and made no manuscript claims.
- It created and accessed no held-out split.
- It copied no model files into the repository. Fixture files were downloaded only to a
  temporary scratch folder, after their license was checked.

**Human verification required.** Neel must spot-check citations in
`docs/novelty_matrix.csv`, especially the closest-prior-work rows, before any novelty claim
is written. AI-verified is not the same as human-verified.

---

## Entry 002: Implementation (Milestones 1-7 infrastructure) and pilot preparation

| Field | Value |
|---|---|
| Date | 2026-09-13 |
| Human instruction | Neel attached `NEUROSEM_FINAL_SPEC.pdf` and wrote "keep going, and build out the entire thing" (see DECISIONS.md D-003) |
| Tool / model | Claude Code desktop, Claude Opus 5 (`claude-opus-5`) |
| Orchestration | Main session wrote the core layers. Workflow `wf_dd699b26-8ce` ran parallel module builders, each followed by an adversarial reviewer and a fixer |
| Transcripts | Claude Code session transcripts under `~/.claude/projects/C--Users-gurra-Continuum/` (session d876c622-…); workflow journals in its `subagents/workflows/` folder |
| Branch | `m0-audit` |

**Written by the main session:**
- `schemas.py`, `units.py`, `provenance.py`, `config.py`, `models.py`, `cli.py`
- `simulators/*`, `protocols/*`, `validation/*`
- `experiments/{campaign,pilot,discovery,heldout}.py`
- configs, model manifest, `docs/ARCHITECTURE.md`, `DECISIONS.md`
- validation-layer unit tests

**Written by workflow agents (listed in their reports):**
- modules: features, mutations, transforms, selection/splits, analysis/figures, agent-study harness
- tests for the core modules
- infrastructure: Docker, CI, lock file, Java bootstrap, CITATION
- scientific documentation and a model-curation sweep

**Tests executed.** Unit and integration tests via pytest, including real jNeuroML runs. Development probes on the pilot models:
- time-step convergence (`docs/pilot/dt_probe.md`);
- smoke runs of the full protocol battery.

**Problems found and handled:**
1. jNeuroML's validator does not check included files.
2. Upstream LTS channel files fail standalone validation.

Both led to the relative structural oracle (D-006).

**Accepted, modified, or rejected.** All code is pending Neel's review. Nothing has been released.

**Scientific control.** The following remain provisional and are listed for Neel's decision in DECISIONS.md:
- tolerance constants
- pilot thresholds
- splits and exclusions
- all interpretation
