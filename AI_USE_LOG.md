# AI Use Log

This log records every substantive use of generative AI in NeuroSem. IEEE requires that
the selected venue's AI-disclosure policy be followed. That policy is verified in
`docs/DEPENDENCY_AUDIT.md` / `PRIOR_ART_AUDIT.md` and must be re-checked at submission. Only
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

**Build workflow `wf_dd699b26-8ce` (completed).**
- **Agents:** 28 in total, no errors. Ten modules each had one builder and one adversarial reviewer, with fixers where the review found medium-or-worse issues.
- **Usage:** about 6.8 M subagent tokens, 1506 tool uses, about 103 minutes.
- **Builder notes:** each builder recorded contract changes and defects in `docs/build_notes/`.

**Integration (main session).** The main session then:
1. Ran an end-to-end integration check on real pilot variants. It surfaced a misclassified numerical blow-up and a jnml validator coverage gap (D-020).
2. Applied the builders' defect reports to the core modules (D-021).
3. Aligned the class-6 rule with the primary endpoint (D-021).
4. Kept hidden agent-study evaluators out of Git (D-022).

Every change came with updated or new tests. The full suite was run before committing `3cdb957`.

**Interruption and rescoping (2026-09-13, about 18:30 UTC).** A usage session limit stopped two workflows partway through.

- **Research workflow `wf_4db58141-488`:** 84 of 133 agents finished. The rest were lost: the second-round prior-art deep reads, the third critic round, and the novelty stress test.
- **Documents workflow `wf_7ab5e6e4-e5a`:** 3 of 9 agents finished.

On Neel's instruction ("Try again") the remaining work was redone without workflow orchestration, using individual background subagents:
- `REQUIREMENTS.md`, `RISK_REGISTER.md` and `PLAN.md` were written;
- `LICENSE_AUDIT.md` and `docs/DEPENDENCY_AUDIT.md` were fact-checked and fixed;
- three deep-read batches covered all 73 second-round candidates estimated at closeness 3;
- one novelty stress test covered the closest verified works.

The main session fixed the name audit from its fact-check findings. It also built `docs/novelty_matrix.csv` with `scripts/build_novelty_matrix.py` and wrote `PRIOR_ART_AUDIT.md`.

Scope that was dropped is recorded openly: 144 second-round candidates at estimated closeness 2 were not deep-read, and the third critic round did not run (`PRIOR_ART_AUDIT.md` section 7).

**Accepted, modified, or rejected.** All code is pending Neel's review. Nothing has been released.

**Scientific control.** The following remain provisional and are listed for Neel's decision in DECISIONS.md:
- tolerance constants
- pilot thresholds
- splits and exclusions
- all interpretation

---

## Entry 003: Pilot role, preservation and bounded iteration 2

| Field | Value |
|---|---|
| Date | 2026-09-13 |
| Human instruction | Neel's "Pilot scope and purpose" direction (DECISIONS D-026, D-027) |
| Tool / model | Claude Code desktop, Claude Opus 5 (`claude-opus-5`), main session only |
| Branch | `m0-audit` |

**What the AI did**
- Recorded Neel's direction as D-026 (pilot is exploratory and never pooled), D-027 (preservation and sealing) and D-028 (iteration 1 exceeded the bounds).
- Wrote the campaign registry and its guards (`experiments/registry.py`) and wired them into `make_context`, the pilot and `evaluate_heldout`, with unit tests.
- Tagged the iteration-1 code (`pilot-v1-code`), archived and sealed campaign `pilot` (`scripts/archive_campaign.py`), and wrote `docs/pilot/PILOT_REGISTER.md`.
- Drafted pilot iteration 2 (`docs/pilot/pilot_v2_design.md`, `configs/pilot_v2_draft/`) from iteration-1 data, and added the post-pilot freeze sequence to `PLAN.md`.

**What the AI did not do**
- It ran no new simulations and did not run iteration 2.
- It accessed no held-out data.
- It uploaded no archive.
- It changed no tolerance, feature or protocol in `configs/`.

**Human decisions pending:** N-14 (iteration-2 design), N-15 (numerical family), N-16 (archive storage).

---

## Entry 004: Pilot 2 revision after Neel's N-14, N-15 and N-16 decisions

| Field | Value |
|---|---|
| Date | 2026-09-13 |
| Human instruction | Neel's written decisions on N-14 (approved with modifications), N-15 (separate numerical experiment) and N-16 (redundant private storage) |
| Tool / model | Claude Code desktop, Claude Opus 5 (`claude-opus-5`), main session only |

**What the AI did**
- Implemented the primary/secondary feature panels and the semantic/numerical strata with tests.
- Reanalysed sealed Pilot 1 read-only.
- Verified the local archive by full extraction and created a Git bundle.
- Revised the Pilot 2 design and draft config, using a generation-only dry run of mutants with no simulation.

**What the AI did not do**
- It did not run Pilot 2 or any simulation.
- It uploaded no data. The second backup location was asked and dismissed, so it stays pending.
- It accessed no held-out data.

---

## Entry 005: Neuraxis development pilot (PILOT_PROTOCOL_V1)

| Field | Value |
|---|---|
| Date | 2026-09-14/15 |
| Human instruction | Neel's replacement archival plan and authorisation of the development/pilot phase (DECISIONS D-033 to D-038) |
| Tool / model | Claude Code desktop, Claude Opus 5 (`claude-opus-5`), main session only |

**What the AI did**
- Wrote the pilot protocol, deviation log, labelling code, prespecified output and reproducibility scripts, the pre-run manifest and package scripts, and their tests.
- Created a private GitHub repository under the logged-in account and pushed the pre-run commit, as instructed.
- Ran the technical readiness gate and the fixed pilot matrix. These runs are recorded in `manifests/` and `results/processed/pilot-v2/`.

**What the AI did not do**
- It did not change the design during the run.
- It accessed no held-out data.
- It made no public release or OSF upload.

---

## Entry 006: Neuraxis execution-plan build

| Field | Value |
|---|---|
| Date | 2026-09-16 |
| Human instruction | Neel attached "Neuraxis: Complete Claude Code Experiment and Publication Execution Plan" and asked to build it out on top of the existing work |
| Tool / model | Claude Code desktop, Claude Opus 5 (`claude-opus-5`); three background research subagents (name audit, prior-art matrix, model-curation sweep) |

**What the AI did**
- Inventoried the repository.
- Renamed the package.
- Extended run records and fixed retry handling.
- Implemented model curation, the infrastructure smoke test and the kinetics mutation family, with tests.
- Wrote the workflows, manifests and required documents.
- **Name audit subagent:** searched package indexes, GitHub, GitLab, literature databases and the USPTO.
- **Prior-art subagent:** built a 36-row matrix and read the full texts of the five closest works.
- **Curation subagent:** searched OpenSourceBrain for further licensed models.
- Ran the clean-environment smoke test and model curation (reference simulations only).

**What the AI did not do**
- It generated no mutant results.
- It did not run Pilot 2.
- It accessed no held-out data.
- It made no public release, did not use OSF, and did not upload anything.

**Human verification required**
- Name decision.
- The five prior-art packets.
- Licence review.
- The Wang–Buzsáki decision.
- Mutant audits.

