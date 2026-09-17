# m-shift_reversal-80b6724096

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL_REHEARSAL | designation: Infrastructure rehearsal of the analysis pipeline on a Pilot 1 model; not study data; never reported as a result and never pooled with anything*

- model: `pospischil2008_rs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "new": "-98.0 mV", "old": "-100.0 mV"}], "element": "channelDensity", "element_id": "Kd_all", "generator_seed": 20260917, "shift_mV": 2.0}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "attribute": "erev", "old": "-100.0 mV", "new": "-98.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1163.278 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | 2.861194747922525 | 3.590610631311506 | 0.729416 | 0.5 | `r-3c4719e59bf2e9991e12` | `r-fef67337d0cd2370a91e` |
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 139.29999999987336 | 3.32 | 2.7196 | `r-3c4719e59bf2e9991e12` | `r-fef67337d0cd2370a91e` |
| h/2 | P00_canonical | ahp_depth | exceeds | 2.9394112752346615 | 3.666103472391768 | 0.726692 | 0.5 | `r-d4ef4781c8007010e9af` | `r-e6c1ecb525b545ac234c` |
| h/2 | P00_canonical | last_isi | exceeds | 135.78999999987656 | 139.10999999987354 | 3.32 | 2.7196 | `r-d4ef4781c8007010e9af` | `r-e6c1ecb525b545ac234c` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
