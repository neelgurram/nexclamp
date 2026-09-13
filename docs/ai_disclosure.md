# AI-use disclosure (draft)

*Status: DRAFT, 2026-09-13. This file adapts the specification's suggested disclosure to
what has actually happened so far. The authoritative record is `AI_USE_LOG.md`, which
this file summarises and must never contradict. Re-check the chosen venue's policy at
submission. Statements marked **[to confirm: Neel]** describe work whose AI-assistance
details only Neel can confirm.*

## 1. Policy requirements this disclosure must meet

From the Milestone 0 venue and policy evidence (`docs/m0_evidence/tools/venues-policy.*.json`,
retrieved 2026-09-13):

- **IEEE author guidance.** Any AI-generated content in an article (text, figures, images,
  code, among others) is disclosed in the **acknowledgments**. The disclosure names the AI
  system, identifies the sections affected and briefly explains the extent of use. Using AI
  only to edit grammar is generally outside the policy, but disclosure is still recommended.
- **IEEE PSPB Operations Manual (amended 25 June 2026).**
  - Authors are responsible for all content and must check AI output for accuracy and
    plagiarism.
  - AI-generated data that simulate a process must be labelled.
  - Code and data release is recommended when AI is the subject of study.
  - Authorship is reserved for individuals.
- **The specification's own rule.** Claude Code may help build the repository, but the
  human author controls scientific ground truth, experimental design, thresholds,
  exclusions, interpretation and final claims.
- Other venues differ. JOSS requires naming tools, stating where and how they were used,
  and that humans reviewed the output and made the core design decisions. bioRxiv asks for
  AI use to be described like other computational methods.

The IEEE wording covers *any* AI-generated content, which is broader than the
specification's phrase "substantive use". This project follows the broader IEEE wording.

## 2. What AI has done so far (as of 2026-09-13)

The project keeps two roles of AI strictly separate (`AI_USE_LOG.md`).

### Role 1: development assistant (the only role used so far)

| Work | Tool / model | Record |
|---|---|---|
| Milestone 0 audit: extraction of the handoff; verification of tool versions, licenses and APIs; prior-art sweep; name-conflict search; fixture screening; Milestone 0 document drafts | Claude Code desktop app, Claude Opus 5 (`claude-opus-5`), multi-agent workflow run `wf_4db58141-488` | `AI_USE_LOG.md` Entry 001 |
| Software implementation after Milestone 0: core modules (`schemas`, `units`, `provenance`, `config`, `models`, `simulators`, `protocols`), validation modules in progress, the development time-step probe (`docs/pilot/dt_probe.md`) | Claude Code sessions **[to confirm: Neel: session dates, model identifier, and human review performed]** | **No log entry yet**, to be added |
| Scientific documentation drafted on 2026-09-13: `docs/glossary.md`, `model_selection.md`, `protocol_catalog.md`, `mutation_catalog.md`, `statistical_plan.md`, `preregistration_draft.md`, `neel_learning_guide.md`, this file; `scripts/build_protocol_manifest.py` and `data/protocol_manifest.csv` | Claude Code subagent in a workflow orchestration run, Claude Opus 5 (`claude-opus-5`) | **No log entry yet**, to be added |

What the AI did **not** do, per `AI_USE_LOG.md` and the rules of every run so far:

- It generated no study results and made no manuscript claims. The time-step probe is a
  labelled development observation on pilot models.
- It created and accessed no held-out split.
- It did not decide inclusion criteria, tolerances, exclusions or interpretation. Every
  such value in `configs/` is marked provisional and awaits Neel's approval.

### Role 2: experimental subject (Milestone 9)

**None has happened.** No frozen agent prompts, isolated trials, transcripts or hidden
evaluations exist.

## 3. Human review status

- Entry 001 asks Neel to spot-check citations in `docs/novelty_matrix.csv` before any
  novelty claim is written.
- **Human review of the post-M0 software and of the documents listed above has not yet
  been recorded.** Until it is, the review sentence of the disclosure below must not be
  used.

## 4. Draft disclosure text (for acknowledgments)

Use only after every bracketed condition is true. Delete sentences that do not apply.

> Claude Code (Anthropic; model Claude Opus 5, identifier `claude-opus-5`, used between
> [first date] and [last date]) was used to assist with a literature and tool audit,
> software scaffolding, implementation, debugging, refactoring, test implementation and
> drafting of documentation for NeuroSem. [Condition: Neel has reviewed all generated code.]
> All generated code was reviewed by the author and evaluated through deterministic unit
> and integration tests, controlled mutations, numerical-convergence checks and
> reproduction of reference simulations. [Condition: the relevant sections were drafted with
> AI assistance.] AI assistance was used in drafting [list manuscript sections], which the
> author revised and verified. Scientific ground truth, inclusion criteria, tolerance
> calibration, held-out evaluation, statistical analysis and interpretation remained under
> the author's control. A complete log of AI use, including tasks, files changed, tests
> run and review outcomes, is provided in `AI_USE_LOG.md` in the software archive
> [DOI].

If Milestone 9 is carried out, add:

> In a separately identified experiment (Section [X]), Claude Code [version], model
> [identifier], was evaluated as a coding agent using frozen prompts, isolated sessions,
> fixed permissions and budgets, and hidden deterministic evaluation procedures. Raw
> transcripts and patches are archived [where redistribution is permitted]. Conclusions
> are restricted to the evaluated configuration.

## 5. Checklist before submission

1. `AI_USE_LOG.md` has an entry for every AI-assisted session. Each entry has date, tool
   and model identifier, task, prompt or transcript path, files changed, human review,
   tests executed, problems found, and accepted, modified or rejected.
2. The entries missing today (post-M0 software; the 2026-09-13 documentation) are filled
   in.
3. Every AI-drafted manuscript section is listed by name in the acknowledgment.
4. Citations were checked by a human, since IEEE Access rejects articles with fabricated
   references.
5. No AI-generated number appears in the manuscript unless it is reproduced from raw
   results by the workflow.
6. The target venue's current AI policy has been re-read and this text adapted to it.
7. The agent study, if run, is disclosed separately from development assistance.
