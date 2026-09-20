# m-scale_conductance-d67ea70a4a

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IL_all']", "new": "0.3364827015392 mS_per_cm2", "old": "0.420603376924 mS_per_cm2"}], "element": "channelDensity", "element_id": "IL_all", "factor": 0.8, "generator_seed": 20260917}`
- recorded edits: `[{"file": "cells/HH2/HH2_477127614.cell.nml", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IL_all']", "attribute": "condDensity", "old": "0.420603376924 mS_per_cm2", "new": "0.3364827015392 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 3350.558 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P05_long_step | spike_count | exceeds | 36.0 | 35.0 | 1 | 0.5 | `r-5fe7a143f3c88a372d40` | `r-872a3f5b7004f0941d79` |
| h/2 | P05_long_step | spike_count | exceeds | 36.0 | 35.0 | 1 | 0.5 | `r-317893116e9cb0c903c3` | `r-f7b45e0845b27673a5d9` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
