# m-scale_conductance-f937b97f50

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='kChans']", "new": "324 S_per_m2", "old": "360 S_per_m2"}], "element": "channelDensity", "element_id": "kChans", "factor": 0.9, "generator_seed": 20260917}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='kChans']", "attribute": "condDensity", "old": "360 S_per_m2", "new": "324 S_per_m2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 611.981 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | last_isi | exceeds | 16.12999999998533 | 14.929999999986421 | 1.2 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-56eb26d40d67d8d07726` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.018407212622088658 | 0.00402978 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-2e1b8920372c31a4c6f0` |
| h/1 | P04_step_2x | adaptation_index | definedness | None | -1.123999640320115e-05 |  | inf | `r-66b1007575e04915ac55` | `r-b1b304cdfe4a52835b8a` |
| h/1 | P04_step_2x | last_isi | definedness | None | 18.529999999983147 |  | inf | `r-66b1007575e04915ac55` | `r-b1b304cdfe4a52835b8a` |
| h/1 | P04_step_2x | spike_count | exceeds | 1.0 | 27.0 | 26 | 0.5 | `r-66b1007575e04915ac55` | `r-b1b304cdfe4a52835b8a` |
| h/2 | P00_canonical | last_isi | exceeds | 16.059999999985394 | 14.869999999986476 | 1.19 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-e97f30cfb2df0a7c4cb3` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02240284133597432 | 0.018373061949320403 | 0.00402978 | 0.00044874 | `s-b96e12fd1e882cb18a94` | `s-8966edb0c1a7b619c3e8` |
| h/2 | P04_step_2x | adaptation_index | definedness | None | 0.0 |  | inf | `r-8d6f46142acd4ec898a7` | `r-e2a1a8be0d08550e99d9` |
| h/2 | P04_step_2x | last_isi | definedness | None | 18.499999999983174 |  | inf | `r-8d6f46142acd4ec898a7` | `r-e2a1a8be0d08550e99d9` |
| h/2 | P04_step_2x | spike_count | exceeds | 1.0 | 27.0 | 26 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-e2a1a8be0d08550e99d9` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
