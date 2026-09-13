# m-scale_conductance-fa05b19484

- model: `pospischil2008_rs`
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityVShift[@id='Na_all']", "new": "45.0 mS_per_cm2", "old": "50.0 mS_per_cm2"}], "element": "channelDensityVShift", "element_id": "Na_all", "factor": 0.9, "generator_seed": 20260913}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityVShift[@id='Na_all']", "attribute": "condDensity", "old": "50.0 mS_per_cm2", "new": "45.0 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1662.956 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 145.27999999986793 | 9.3 | 2.7196 | `r-5171ec6a0414fa8c47f8` | `r-dac995eb6d373954ec3d` |
| h/1 | P05_long_step | last_isi | exceeds | 78.13000000170541 | 79.88000000174361 | 1.75 | 1.5626 | `r-6299bd8dadd5e9592d63` | `r-a4cf886c8333383bda2f` |
| h/1 | P05_long_step | spike_count | exceeds | 29.0 | 28.0 | 1 | 0.5 | `r-6299bd8dadd5e9592d63` | `r-a4cf886c8333383bda2f` |
| h/2 | P00_canonical | last_isi | exceeds | 135.78999999987656 | 145.02999999986815 | 9.24 | 2.7196 | `r-35d4f8d415fe0d06a895` | `r-5246dce83f2b61542ac0` |
| h/2 | P05_long_step | last_isi | exceeds | 77.97000000170192 | 79.69000000173946 | 1.72 | 1.5626 | `r-a71c890435a70aeaf61b` | `r-bbae3c10fed62c22ba3b` |
| h/2 | P05_long_step | spike_count | exceeds | 29.0 | 28.0 | 1 | 0.5 | `r-a71c890435a70aeaf61b` | `r-bbae3c10fed62c22ba3b` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
