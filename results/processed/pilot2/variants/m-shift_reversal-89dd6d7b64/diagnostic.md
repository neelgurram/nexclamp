# m-shift_reversal-89dd6d7b64

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IL_all']", "new": "63.671643065 mV", "old": "58.671643065 mV"}], "element": "channelDensity", "element_id": "IL_all", "generator_seed": 20260917, "shift_mV": 5.0}`
- recorded edits: `[{"file": "cells/HH2/HH2_477127614.cell.nml", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IL_all']", "attribute": "erev", "old": "58.671643065 mV", "new": "63.671643065 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 486.133 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
