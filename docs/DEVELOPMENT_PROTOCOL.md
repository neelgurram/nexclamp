# Development protocol

*The rules for everything before the frozen held-out study (execution plan: "separate development
and held-out phases"). A development protocol version (for example `docs/PILOT_PROTOCOL_V1.md`)
fixes the exact settings of one development run; this document fixes the process around them.*

## 1. Phases and what each may use

| Phase | Tool | Data it may use | Output status |
|---|---|---|---|
| 0. Infrastructure smoke test | `neuraxis smoke-test` | two fixture models | infrastructure check; blocks everything below if it fails |
| 1. Model curation | `neuraxis curate-models` | reference simulations of candidate models only (no mutant) | eligibility table `manifests/models.csv`, report `docs/MODEL_CURATION_REPORT.md` |
| 2. References and numerical calibration | `neuraxis run-reference`, `calibrate-tolerances` | development models | tolerance proposal |
| 3. Variant generation | `neuraxis generate-mutants` | development models; families in the protocol | mutation and transformation manifests |
| 4. Development runs (pilots) | `neuraxis pilot` with `NEURAXIS_CONFIG_DIR=<protocol configs>` | development models and development families | **exploratory** |
| 5. Development analysis | `scripts/pilot_outputs.py`, `neuraxis analyze`, `workflows/run_robustness.py` | development results | **exploratory** |
| 6. Human audit | Neel | audit sheets, prior-art packets, case plots | recorded decisions |
| 7. Protocol selection | `neuraxis select-protocols` | development split only; kinetics family excluded | selection JSON |
| 8. Freeze | `workflows/freeze_study.py` | – | `configs/FROZEN.lock`, Git tag |
| 9. Preregistration | Neel, via AsPredicted | – | time-stamped PDF and verification URL |
| 10. Held-out evaluation | `workflows/run_heldout.py` | held-out split, once | **confirmatory** |

Phases 8-10 need Neel's explicit authorisation. Phase 10 starts only after Neel writes the exact
sentence recorded in DECISIONS D-036.

## 2. Rules that hold throughout development

1. **Protocol before data.** Every development run has a written protocol version and executable
   configs that agree (checked by a test).
   - Before the run: SHA-256 manifest, commit, private push, pre-run package.
2. **Labels.** Every record carries `project_name`, `study_phase`, `protocol_version` and the
   configuration hash.
3. **Immutable raw data.** Raw data are write-once.
   - A legitimate rerun gets new run records, via a new replicate or a new campaign.
   - A toolchain failure is kept in `_tool_failures/` and never blocks a permitted retry.
4. **One configuration per campaign.** A changed setting means a new campaign name. Finished
   campaigns are sealed and archived with per-file hashes.
5. **Fixed matrix.** No protocols, models, mutants or repetitions are added because time remains.
   - Retries are allowed only after infrastructure failures, at most 2 (PILOT_PROTOCOL_V1 section 10).
6. **No mid-batch changes.** Thresholds, exclusions and definitions never change during a running
   batch. Proposals go to the protocol's deviation log for the next version.
7. **Strata.** Model mutations (semantic) and numerical stress tests are analysed separately.
   - Numerical results are never called semantic drift.
   - Primary mutants and controls run with the reference's exact numerics.
8. **Kinetics family** (ion-channel kinetics). It may be exercised for operator correctness on
   development fixtures. Its detection results are never used to select the battery. It is labelled
   "excluded from protocol selection".
9. **No held-out access.** No held-out model or family is assigned or inspected during development.
   - Candidate models inspected during curation are disclosed as "reference behaviour inspected".
10. **Model exclusions.** They follow the inclusion and exclusion criteria mechanically, never on
    whether a model helps the hypothesis. Every exclusion is logged.
11. **Reporting.** Every report states:
    - which findings are exploratory and which confirmatory;
    - whether each analysis was prespecified;
    - the protocol version and commit;
    - any deviation.

## 3. Model inclusion and exclusion criteria (execution plan)

Implemented mechanically in `src/neuraxis/orchestration/curation.py`, criteria C01-C13:
- provenance;
- reuse rights;
- files present;
- NeuroML validation;
- execution;
- interpretable trace;
- recording location;
- response to current;
- determinism;
- refinement stability;
- runtime;
- operator support;
- protocol compatibility.

A model with any failed criterion is excluded. A model with an open criterion, such as spontaneous
activity, goes to human review. Diversity (tonic, adapting, bursting, rebound, sag, thresholds,
channel compositions) is reported per model and used to plan the split. It is never used to drop a
model after its mutation results are known.

## 4. Stopping development

The development phase ends when Neel decides. The planned evidence for that decision:
- pilot outputs 1-12;
- human audits;
- the curation report;
- a sufficient eligible model pool (spec: 8-10 development and 4-6 held-out models from distinct
  sources);
- a frozen feature panel, tolerances and selection.
