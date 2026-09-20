# m-wrong_compatible_component-a12a6658b4

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / wrong_compatible_component
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all']", "new": "Kd", "old": "IM"}], "element_id": "IM_all", "generator_seed": 20260917, "new_species": "k", "old_species": "k"}`
- recorded edits: `[{"file": "cells/HH2/HH2_477127614.cell.nml", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all']", "attribute": "ionChannel", "old": "IM", "new": "Kd", "action": "set", "note": "wrong_compatible_component"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 3726.989 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P03_rheobase | rheobase | exceeds | 0.06447647018646267 | 0.062051772419916676 | 0.0024247 | 0.00128953 | `s-bd435463250c35027583` | `s-2b625eb6bdf78212dd20` |
| h/1 | P04_step_2x | last_isi | exceeds | 32.02999999997087 | 29.679999999973006 | 2.35 | 1.59 | `r-d2b3788dfa4671532754` | `r-66a7f4b9e1b439f46b01` |
| h/1 | P05_long_step | last_isi | exceeds | 56.07000000122389 | 49.410000001078515 | 6.66 | 2.61 | `r-5fe7a143f3c88a372d40` | `r-a22fa9b32906dca4fa21` |
| h/1 | P05_long_step | spike_count | exceeds | 36.0 | 40.0 | 4 | 0.5 | `r-5fe7a143f3c88a372d40` | `r-a22fa9b32906dca4fa21` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.06447647018646267 | 0.062051772419916676 | 0.0024247 | 0.00128953 | `s-4d054cac6fc39c11b1f5` | `s-866bd7688c7be3fb87af` |
| h/2 | P04_step_2x | last_isi | exceeds | 31.49999999997135 | 29.119999999973516 | 2.38 | 1.59 | `r-ae1b79422775c8a979b7` | `r-b8b0133fbc560b0fcf55` |
| h/2 | P05_long_step | last_isi | exceeds | 55.2000000012049 | 48.55000000105974 | 6.65 | 2.61 | `r-317893116e9cb0c903c3` | `r-9b7e85278ca258a133d1` |
| h/2 | P05_long_step | spike_count | exceeds | 36.0 | 41.0 | 5 | 0.5 | `r-317893116e9cb0c903c3` | `r-9b7e85278ca258a133d1` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
