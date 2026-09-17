# Decisions required from the researcher

*Open items only. The full history is in `DECISIONS.md` (D- entries are decided, N- entries are
Neel's). The most urgent items are first.*

| # | Decision | Options | Recommendation | Blocks |
|---|---|---|---|---|
| R-01 | **Project name** | – | **Decided 2026-09-17: the planned public name is PerturbPrint** (D-050); internal identifier `neuron_model_behavioral_validation`. Rename plan: `docs/RENAME_PLAN.md`, executed after Pilot 2 | closed |
| R-02 | **Wang–Buzsáki model** | – | **Decided 2026-09-17: excluded from the primary study, kept as a documented candidate** (D-051); never hand-repaired for inclusion; exploratory sensitivity use only if prespecified | closed |
| R-03 | **Pilot 2 go-ahead** | – | **Decided 2026-09-17: automatic authorisation** under PILOT2_PROTOCOL, conditional on curation yielding at least four eligible new models, a clean full suite, a clean smoke test, committed pre-run files, isolated held-out models and unchanged Pilot 1 data. Any failed condition stops the run and is reported. Protocol, configuration and matrix are frozen (D-054); readiness testing is the remaining gate | in progress |
| R-04 | **Model pool** for the confirmatory study (N-09), from `docs/MODEL_CURATION_REPORT.md` | which eligible models, which sources are development and which held out (N-02) | At least 8-10 development and 4-6 held-out models; held-out models from sources not used in development | split freeze |
| R-05 | **Kinetics family scope** (D-037, X-14) | new operators only / also move `scale_gate_time_constant` | New operators only, because tau scaling was used and inspected in Pilot 1 | preregistration |
| R-06 | **Code licence** Apache-2.0 (provisional per the plan) | confirm / other | Confirm after the compatibility re-read of `LICENSE_AUDIT.md` sections 7-8 (L-01, L-11) | public release |
| R-07 | **Human audits** | – | Audit at least 20 mutants (sheet produced by each pilot); inspect the five prior-art packets; review the hidden agent-study evaluators (N-12) | publication claims, agent study |
| R-08 | **Tolerance constants and pilot thresholds** (N-03, N-04) | – | Decide on development evidence only, before the freeze | freeze |
| R-09 | **Low-rheobase amplitudes** (N-07; Wang–Buzsáki smoke rheobase 0.00017 nA) | – | Review with development data | freeze |
| R-10 | **Second independent copy of the Pilot 1 archive** (N-16) | external drive / OSF when available / other cloud you control | An external drive now; OSF later as a mirror | none (not blocking) |
| R-11 | **Canonical metric** (N-06) and **NEURON cross-simulator** (N-08) | – | Keep the same features and tolerances; NEURON deferred | freeze |
| R-12 | **Preregistration submission** (D-036) | – | After the freeze: submit `docs/CONFIRMATORY_PREREGISTRATION_DRAFT.md` through AsPredicted, then send the time-stamped PDF, the verification URL and the exact authorisation sentence | held-out evaluation |
| R-13 | **Documentation and data licences** (L-02, L-03) | CC-BY-4.0 / CC0 / other | CC-BY-4.0 for docs; state a data licence at the first Zenodo deposit | release |
| R-14 | **Package namespace at rename.** Keep the `neurosem` alias until the hidden-evaluator review (N-12), or drop both aliases at rename time | drop both / keep `neurosem` temporarily | Drop both: nothing is published, and the only affected files are the Git-ignored hidden checks, which the rename commit updates and re-hashes (`docs/RENAME_PLAN.md`) | rename |
| R-15 | **Type-checking policy.** mypy is now pinned; a baseline run reports 95 findings, all annotation gaps rather than defects | enforce in CI later / keep as a recorded baseline | Keep as a baseline for now; tighten module by module after Pilot 2 | none |

