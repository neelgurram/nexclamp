# Decisions required from the researcher

*Open items only. The full history is in `DECISIONS.md` (D- entries are decided, N- entries are
Neel's). The most urgent items are first.*

| # | Decision | Options | Recommendation | Blocks |
|---|---|---|---|---|
| R-01 | **Project name.** NeurAxis, Inc. holds live US trademarks for NEURAXIS in neurostimulation (`docs/NAME_AUDIT.md`) | keep Neuraxis / rename (PerturbPrint, DriftClamp, other) | Rename before any public repository, preprint or preregistration; run the full name search on the chosen name first | preregistration, public release, private GitHub repository name |
| R-02 | **Wang–Buzsáki model**: its cell file fails schema validation (`docs/pilot/PILOT_PROTOCOL_V1_DEVIATIONS.md`) | A: record the pre-existing error as a reference baseline error (protocol V1.1) / B: replace with another independent-source model / C: run Pilot 2 with 3 models / D: edit the file (not recommended) | Under the execution plan's inclusion criteria it is excluded (C04). If kept, choose A and disclose it. | Pilot 2 |
| R-03 | **Pilot 2 go-ahead** under a revised PILOT_PROTOCOL_V1.1 (R-02 applied; package renamed) | run / revise further | Run after R-02, the pre-run manifest, the private push and the readiness gate | development data |
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
