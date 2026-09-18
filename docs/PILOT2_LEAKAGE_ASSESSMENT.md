# Pilot 2 leakage assessment

*Written 2026-09-18 at commit `17b9b06`, after Neel ordered a pre-launch audit. Read-only with
respect to every existing artefact: nothing was deleted, moved, regenerated or sanitised, and no
simulation was run for this document. Machine-readable evidence:
`results/audits/PILOT2_PRELAUNCH_EVIDENCE_INVENTORY.csv` (4,540 files hashed),
`results/audits/PILOT2_KINETICS_OVERLAP_AUDIT.csv` (48 executions),
`results/audits/PILOT2_PRELAUNCH_AUDIT_SUMMARY.json`.*

## Summary in plain English

- Before the Pilot 2 campaign started, the four kinetics operators were run on the Pilot 2 models
  themselves to check the operators worked. Those checks **simulated the models and produced spike
  counts**, which were printed, read by the assistant and reported to Neel.
- **Nine** of those checks are the *same edit* as one of the frozen Pilot 2 mutants. For those nine,
  the canonical harness's answer is already known.
- The Pilot 2 protocol document was edited **one minute after** those outcomes appeared, so its
  header sentence "frozen before execution" is not accurate as written.
- The campaign itself then started and ran 38 of 143 variants before being stopped. Nothing from it
  was aggregated, plotted, summarised or looked at.
- Pilot 2 was always designated **exploratory development data, never confirmatory**, so no
  confirmatory claim was damaged. What was damaged is the claim that the design was frozen before
  any Pilot 2 outcome was seen.

## 1. What was executed (Phase A)

`scripts/kinetics_validation.py --only-models --models <the five Pilot 2 models> --max-sites 6`
ran on 2026-09-17, finishing 21:19:14 UTC. Evidence:
`results/audits/kinetics_pilot2/kinetics_validation.json` plus 48 before/after plots and the raw
runs under `results/audits/kinetics_pilot2/raw/`.

| model | operators with sites | executions | operators with no site |
|---|---|---|---|
| `acnet2_pyr_soma` | midpoint, slope, forward rate | 18 | channel vShift |
| `migliore2014_mt_soma` | midpoint, slope | 10 | forward rate, vShift |
| `nml2_hh_example` | midpoint, slope, forward rate | 18 | vShift |
| `osb_hh2_477127614` | channel vShift | 2 | midpoint, slope, forward rate |
| `pospischil2008_fs` | — | **0** | all four (custom LEMS rate types) |

Recovered per execution (in the overlap CSV): model id, operator, site index, channel, gate,
mechanism, magnitude, derived severity, protocol (`P00_canonical`), edit list with old and new
attribute values, affected equation types, atomicity, schema validity, simulation status, spike
counts before and after, maximum absolute voltage difference, plot path.

**Missing evidence, reported as missing rather than reconstructed:**

- the workspace **model tree hash** per validation site was not stored in the validation table (the
  runs exist under `results/audits/kinetics_pilot2/raw/`, but the table does not bind site → run id);
- per-site **run ids**, trace file paths and feature hashes are likewise not in the table;
- the validation used a workspace materialised from the same pinned snapshot as the frozen campaign,
  but this is inferred from the shared `load_models()` path, not from a recorded hash comparison.

## 2. What outcomes were produced (Phase B)

For all 48 executions the run produced: execution status (`ok` in 48/48), **spike count before and
after**, **maximum absolute voltage difference from the reference**, a schema-validity flag, a
single-change enforcement flag, a harness-unchanged flag, and a **before/after voltage plot**. Full
traces were written under the audit raw directory. No eFEL feature table, no RMSE, no spike-timing
metric and no detection classification were computed.

**Provenance of the two figures quoted in conversation:**

| reported | actual source |
|---|---|
| "7 → 30 spikes" | `nml2_hh_example`, `shift_gate_midpoint`, site 0, mild, canonical protocol; row 1 of that model's block in `kinetics_validation.json`; plot `plots/nml2_hh_example_shift_gate_midpoint_0.png` |
| "28 → 0 spikes" | `osb_hh2_477127614`, `shift_channel_vshift`, site 1, mild, canonical protocol; plot `plots/osb_hh2_477127614_shift_channel_vshift_1.png` |

## 3. What was observed (Phase C)

Against the seven-level scale:

| level | applies? | evidence |
|---|---|---|
| 1. generated but blinded | **no** | no blinding mechanism exists in this repository |
| 2. written but not summarised | no | the script prints a per-site table by design |
| 3. automatically summarised in logs | **yes** | `results/audits/kinetics_pilot2/kinetics_validation.json` and the task log |
| 4. explicitly printed in the conversation | **yes** | 48-row table printed; per-model summary computed and printed |
| 5. inspected by the assistant | **yes** | the assistant read the table and computed per-model maxima |
| 6. inspected by a human | **yes, conservatively** | the assistant reported "7 → 30" and "28 → 0" to Neel in chat |
| 7. used to justify a design decision | **yes** | see section 4 |

There is no basis for claiming non-exposure. The assistant's own prior message stated the
behavioural effects, and the repository confirms that statement was accurate.

## 4. Did exposure influence the design (Phase D)

Timeline from file modification times and commit timestamps (local clock, 2026-09-17):

| time | artefact | relation to exposure |
|---|---|---|
| 16:41 | `configs/pilot2_frozen.yaml` written: models, families, operators, severities, protocols, sites-per-severity | **before** |
| ~17:14–17:19 | kinetics validation executed on the five Pilot 2 models | **exposure** |
| 17:19 | `kinetics_validation.json` written | exposure |
| 17:20 | `docs/PILOT2_PROTOCOL.md` modified | **after** |
| 17:56 | commit `cffd026`, message "Pilot 2 frozen before execution" | after |
| 19:20 | `manifests/PILOT2_*` regenerated; commit `17b9b06` | after |
| 23:21 | readiness run (READY) | after |
| 00:45 | authorization gate (AUTHORIZED); campaign launched | after |

**What changed after exposure, and my honest reading of each:**

| design artefact | changed after exposure? | assessment |
|---|---|---|
| model selection | no | fixed at 16:41, and the five were chosen from curation criteria only |
| mutation family and operator set | **decision at ~17:00, documentation at 17:20** | the choice to use all four kinetics operators was made before the run, for the stated reason that `shift_forward_rate_midpoint` is the only atomic one; the *documented justification* was written after |
| mutation site selection | no | sites are drawn by seeded rule in `severity.select_sites`; the frozen manifest was generated from the config |
| severity definitions | no | `severity.py` bands predate the run |
| protocol selection | no | fixed at 16:41 |
| threshold calibration | no | `configs/tolerances.yaml` untouched since before the run |
| branch rules | no | `BRANCH_RULES` predates the run |
| **applicability statements** | **yes** | the protocol's per-model applicability table, "no eligible site" reasons and maximum-voltage-difference sentence were written from the exposed output |
| **atomic vs compound definition** | **yes** | corrected at 17:20 *because* the recorded output labelled `shift_channel_vshift` atomic, contradicting the earlier text |
| exclusions | no | `wrong_segment_group`, `shift_initial_voltage` excluded at 16:41 |
| analysis code, statistical plan, authorization conditions | no | unchanged since before the run |

None of the post-exposure edits changed a threshold, a denominator, a rule or which variants run.
They were descriptive. But two design artefacts were authored with the outcomes in hand, and the
ordering cannot be undone, so the conservative reading is **possible design influence**.

## 5. Was the unseen-family condition compromised (Phase E)

- The family intended to be held back from **protocol selection** is `kinetics`
  (`strata.SELECTION_EXCLUDED_FAMILIES`, D-037/D-042). Its purpose is that the protocol battery was
  never tuned to detect kinetics faults.
- That specific condition is **intact**: the battery was selected before any kinetics operator
  existed, and nothing in the selection code consumes kinetics outcomes. `SELECTION_EXCLUDED_FAMILIES`
  is enforced in code and tested.
- What is **not** intact is the weaker but still valuable property that the kinetics family's
  behaviour on the Pilot 2 models was unseen before the campaign. Nine frozen kinetics mutants have a
  known canonical-harness spike-count response.
- Exposure is **variant-specific, not family-wide or model-wide**: 9 of 12 frozen kinetics mutants;
  0 of the 76 non-kinetics primary semantic mutants; 0 of the 40 controls; 0 of the 15 numerical
  stress tests. `pospischil2008_fs` had no kinetics site, so it carries no exposure at all.

**Exact statement of what remains defensible** (see the decision document for the full list): the
claim "the perturbation battery was never selected using kinetics information" survives. The claim
"no Pilot 2 outcome was observed before the campaign" does not.

## 6. Overlap counts (Phase 4)

From `results/audits/PILOT2_KINETICS_OVERLAP_AUDIT.csv`:

| quantity | count |
|---|---|
| validation executions on Pilot 2 models | 48 |
| exact overlaps with a frozen Pilot 2 mutant (same model, operator, channel, gate, magnitude) | **9** |
| of the 88 primary semantic mutants | 9 (10.2%) |
| of the 12 frozen kinetics mutants | 9 (75%) |
| same model and operator but a different site | 39 |
| affected models | 4 of 5 (`pospischil2008_fs` unaffected) |
| affected operators / families | 4 operators, 1 analysis family (`gating_voltage_dependence`) |
| affected protocols | 1 (`P00_canonical`, the comparator) |
| primary outcomes exposed | 48 execution statuses, 48 spike-count pairs, 48 voltage-difference maxima, 48 plots |
| executions whose status cannot be reconstructed | 0 |

The nine exact overlaps:

| model | operator | severity | canonical spikes before → after |
|---|---|---|---|
| `acnet2_pyr_soma` | `shift_gate_midpoint` | mild | 8 → 10 |
| `acnet2_pyr_soma` | `scale_gate_slope` | mild | 8 → 7 |
| `acnet2_pyr_soma` | `shift_forward_rate_midpoint` | mild | 8 → 8 |
| `migliore2014_mt_soma` | `shift_gate_midpoint` | mild | 1 → 1 |
| `migliore2014_mt_soma` | `scale_gate_slope` | mild | 1 → 2 |
| `nml2_hh_example` | `shift_gate_midpoint` | mild | 7 → 0 |
| `nml2_hh_example` | `scale_gate_slope` | mild | 7 → 19 |
| `nml2_hh_example` | `shift_forward_rate_midpoint` | mild | 7 → 1 |
| `osb_hh2_477127614` | `shift_channel_vshift` | mild | 28 → 41 |

Because a changed canonical spike count is exactly what validation level B and level C detect, the
canonical-detection outcome for these nine mutants is effectively already known: eight of nine
changed the canonical spike count and one (`acnet2` forward rate, 8 → 8) did not.

## 7. The partial campaign

| quantity | value |
|---|---|
| raw run records written | 564 |
| variants begun | 38 of 143 (27 primary semantic, 8 controls, 3 numerical) |
| models touched | 2 (`acnet2_pyr_soma` 31, `migliore2014_mt_soma` 7) |
| h fingerprints / h2 fingerprints / detection files | 30 / 21 / 27 |
| `classification.csv`, `pilot_report.md`, `pilot_v2_outputs/` | **none written** |
| summarised, plotted or inspected | **no** |

Every variant directory name matches an id in the frozen `PILOT2_VARIANTS.csv`; nothing outside the
frozen matrix was executed. The run was stopped between variants, so partial state is confined to
in-flight workspaces under `work/`; all recorded raw results are content-addressed and complete.

## 8. Classification (Phase 5)

**L5 — confirmatory run already started**, with an underlying **L4** component.

- **L5** applies on the letter of the definition: "the nominal Pilot 2 campaign began". It did, for
  38 of 143 variants.
- **L4** applies to the kinetics exposure: outcomes were exposed while two design artefacts were
  still being authored, and the ordering cannot be undone.
- Lower categories are refused: L2 is impossible (no blinding exists), L3 is refused because the
  protocol text was demonstrably edited after exposure.

**Material qualifier, stated so the classification is not over-read:** Pilot 2 is not a confirmatory
study and never was. Its protocol, configuration and every run record carry
`study_phase: development_pilot` and a designation string forbidding pooling with the confirmatory
held-out estimate. The L5 label describes contamination of a *held-out* design that Pilot 2 was
never part of. The genuine casualty is narrower and is stated exactly in
`docs/PILOT2_PRELAUNCH_DECISION.md`.
