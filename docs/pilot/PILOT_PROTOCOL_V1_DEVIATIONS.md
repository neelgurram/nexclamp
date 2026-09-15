# PILOT_PROTOCOL_V1: deviation log

Deviations from earlier plans, and any deviation during the run. Each entry: what, why, effect,
whether it was decided before or after data were seen.

## Before any Pilot 2 data (recorded 2026-09-15 UTC)

1. **The run commit is not `633482d`.** Neel authorised running "the committed design associated
   with commit 633482d". Before the run, three non-design changes were made:
   - study labels (`study_phase`, `project_name`, `protocol_version`, `config_sha256`) added to run
     records, tables, reports and figures, as Neel's instructions require;
   - the prespecified output, reproducibility, manifest and packaging scripts;
   - the config directory renamed from `configs/pilot_v2_draft/` to `configs/pilot_protocol_v1/`,
     with a `study_metadata` block and repeated/new model lists added.

   Unchanged:
   - models;
   - protocols and their parameters;
   - primary and secondary features;
   - tolerances;
   - mutation and transform operators, exclusions, counts and seed;
   - classification rules;
   - numerical settings.

   Effect: none on any simulation or classification. Decided before data.
2. **OSF backup replaced.** OSF was unavailable (service errors). Per Neel, OSF is an optional later
   mirror. Replacement plan:
   - a pre-run commit pushed to a private GitHub remote;
   - a compressed pre-run package.

   The second independent copy of the Pilot 1 archive is still pending and does not block the pilot.
   Decided before data.
3. **Project name "Neuraxis"** in records; the code package is still `neurosem`. Decided before data.

## Technical readiness gate (preliminary run, 2026-09-15 UTC): FAILED on one item; no pilot data generated

- **Gate item 1 (tests):** passed, 1,007 passed and 1 skipped (`work/logs/full_suite_pre_protocol_v1.log`).
- **Gate item 4 (smoke):** exit 0 for all four models (`work/logs/gate_prelim_smoke.log`). Plumbing only.
- **Gate item 3 (`validate-models`): FAILED for `wangbuzsaki1996_wb`.**
  - The shipped cell file `NeuroML2/LEMS/WangBuzsaki.cell.nml` is rejected by the NeuroML v2.3.1 schema: attribute `type` is not allowed on `gateHHrates`.
  - libNeuroML strict validation passes, and the shipped harness simulates (10 spikes).
  - The relative structural oracle (D-006) requires a reference's own cell file to validate, so the WB reference stage would stop the campaign.
- **Observation for N-07:** WB rheobase 0.00017 nA (smoke search).
- **Action:**
  - stopped before the pre-run commit, push, package and campaign;
  - no change made to the oracle, the model file or the model list;
  - Neel's approval requested for a design change: accept the pre-existing cell-file schema error as a reference baseline error, replace WB, or drop WB.

## During the run

None (not started).
