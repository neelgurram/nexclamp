# m-scale_conductance-a5d53b94c4

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL_REHEARSAL | designation: Infrastructure rehearsal of the analysis pipeline on a Pilot 1 model; not study data; never reported as a result and never pooled with anything*

- model: `pospischil2008_rs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityVShift[@id='Na_all']", "new": "55.0 mS_per_cm2", "old": "50.0 mS_per_cm2"}], "element": "channelDensityVShift", "element_id": "Na_all", "factor": 1.1, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityVShift[@id='Na_all']", "attribute": "condDensity", "old": "50.0 mS_per_cm2", "new": "55.0 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1165.512 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 128.9199999998828 | 7.06 | 2.7196 | `r-3c4719e59bf2e9991e12` | `r-14e47b9c603c8eb2fd4a` |
| h/2 | P00_canonical | last_isi | exceeds | 135.78999999987656 | 128.75999999988295 | 7.03 | 2.7196 | `r-d4ef4781c8007010e9af` | `r-fab8eb732a5aebcc73bb` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
