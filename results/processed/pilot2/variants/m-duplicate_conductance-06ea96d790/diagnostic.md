# m-duplicate_conductance-06ea96d790

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / duplicate_conductance
- parameters: `{"generator_seed": 20260917, "new_id": "IM_all_dup", "source_id": "IM_all"}`
- recorded edits: `[{"file": "cells/HH2/HH2_477127614.cell.nml", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all_dup']", "attribute": null, "old": null, "new": "<channelDensity xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" id=\"IM_all_dup\" ionChannel=\"IM\" condDensity=\"0.0165717583065 mS_per_cm2\" erev=\"-92.3418670162 mV\" ion=\"k\"/>", "action": "insert", "note": "duplicate_conductance"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 4094.174 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P03_rheobase | rheobase | exceeds | 0.06447647018646267 | 0.06669626391639916 | 0.00221979 | 0.00128953 | `s-bd435463250c35027583` | `s-6cf5215c49bde44ddac4` |
| h/1 | P04_step_2x | last_isi | exceeds | 32.02999999997087 | 34.859999999968295 | 2.83 | 1.59 | `r-d2b3788dfa4671532754` | `r-d1f8922381fe884b4be0` |
| h/1 | P05_long_step | last_isi | exceeds | 56.07000000122389 | 64.30000000140353 | 8.23 | 2.61 | `r-5fe7a143f3c88a372d40` | `r-2c1bd8dcd6f601d7d9f7` |
| h/1 | P05_long_step | spike_count | exceeds | 36.0 | 32.0 | 4 | 0.5 | `r-5fe7a143f3c88a372d40` | `r-2c1bd8dcd6f601d7d9f7` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.06447647018646267 | 0.06669626391639916 | 0.00221979 | 0.00128953 | `s-4d054cac6fc39c11b1f5` | `s-947e37e5a42c19a5a6f7` |
| h/2 | P04_step_2x | last_isi | exceeds | 31.49999999997135 | 34.17999999996891 | 2.68 | 1.59 | `r-ae1b79422775c8a979b7` | `r-328993ca03d18da5f610` |
| h/2 | P05_long_step | last_isi | exceeds | 55.2000000012049 | 63.45000000138498 | 8.25 | 2.61 | `r-317893116e9cb0c903c3` | `r-672375e7feb7452feb7e` |
| h/2 | P05_long_step | spike_count | exceeds | 36.0 | 32.0 | 4 | 0.5 | `r-317893116e9cb0c903c3` | `r-672375e7feb7452feb7e` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
