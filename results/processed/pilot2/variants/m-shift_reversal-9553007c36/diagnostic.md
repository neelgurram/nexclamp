# m-shift_reversal-9553007c36

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Ca_pyr_soma_group']", "new": "90.0 mV", "old": "80.0 mV"}], "element": "channelDensity", "element_id": "Ca_pyr_soma_group", "generator_seed": 20260917, "shift_mV": 10.0}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Ca_pyr_soma_group']", "attribute": "erev", "old": "80.0 mV", "new": "90.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1504.293 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.08360766405035329 | -0.005627147147519321 | 0.0892348 | 0.01 | `r-7ce2d1a0f19cc5d24572` | `r-3726dc182fe5f782a997` |
| h/1 | P00_canonical | last_isi | exceeds | 76.88999999993013 | 84.03999999992362 | 7.15 | 1.5378 | `r-7ce2d1a0f19cc5d24572` | `r-3726dc182fe5f782a997` |
| h/1 | P00_canonical | spike_count | exceeds | 8.0 | 7.0 | 1 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-3726dc182fe5f782a997` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.00782050406393006 | 0.000204904 | 0.000152312 | `s-f72e8dc74d5f026206e4` | `s-571d0e8fad8673f3eb7c` |
| h/1 | P04_step_2x | last_isi | exceeds | 451.11999999958977 | 467.329999999575 | 16.21 | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-99da8fcc007edcec4fbb` |
| h/1 | P05_long_step | adaptation_index | definedness | -8.519410542851502e-06 | None |  | 0.01 | `r-f6700284baa99a5ef41f` | `r-4edc21a84ae47fa37557` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 37.16999999983835 | 38.20999999983741 | 1.04 | 0.7434 | `r-f6700284baa99a5ef41f` | `r-4edc21a84ae47fa37557` |
| h/1 | P05_long_step | last_isi | definedness | 586.8900000005651 | None |  | 11.7378 | `r-f6700284baa99a5ef41f` | `r-4edc21a84ae47fa37557` |
| h/1 | P05_long_step | spike_count | exceeds | 4.0 | 1.0 | 3 | 0.5 | `r-f6700284baa99a5ef41f` | `r-4edc21a84ae47fa37557` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 501.13999999941643 | 528.1099999993919 | 26.97 | 10.0228 | `r-ee8bcdd517fb72ba8d0c` | `r-fbe51ca99c0c6a90f138` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.08394194146984126 | -0.0050604420762389675 | 0.0890024 | 0.01 | `r-2526a9bbad7e1faa361e` | `r-a24df4c0618b8027aa0e` |
| h/2 | P00_canonical | last_isi | exceeds | 76.5899999999304 | 83.7399999999239 | 7.15 | 1.5378 | `r-2526a9bbad7e1faa361e` | `r-a24df4c0618b8027aa0e` |
| h/2 | P00_canonical | spike_count | exceeds | 8.0 | 7.0 | 1 | 0.5 | `r-2526a9bbad7e1faa361e` | `r-a24df4c0618b8027aa0e` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.00782050406393006 | 0.000204904 | 0.000152312 | `s-4f52e2b97721efbbe2d2` | `s-6dfa4f1589c74d8893c4` |
| h/2 | P04_step_2x | last_isi | exceeds | 450.1799999995906 | 466.42999999957584 | 16.25 | 9.0224 | `r-16be743cbc8f0485fd82` | `r-884e315f9ee611dc88cc` |
| h/2 | P05_long_step | adaptation_index | definedness | -8.532786352377084e-06 | None |  | 0.01 | `r-493fa57e11933a720397` | `r-d5bf9da1592a1d3a4f1c` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 37.10999999983841 | 38.14999999983746 | 1.04 | 0.7434 | `r-493fa57e11933a720397` | `r-d5bf9da1592a1d3a4f1c` |
| h/2 | P05_long_step | last_isi | definedness | 585.9700000005014 | None |  | 11.7378 | `r-493fa57e11933a720397` | `r-d5bf9da1592a1d3a4f1c` |
| h/2 | P05_long_step | spike_count | exceeds | 4.0 | 1.0 | 3 | 0.5 | `r-493fa57e11933a720397` | `r-d5bf9da1592a1d3a4f1c` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 501.0599999994165 | 528.019999999392 | 26.96 | 10.0228 | `r-2e3e935d6ecd1df4b94b` | `r-54257f29f2ff41e6a985` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
