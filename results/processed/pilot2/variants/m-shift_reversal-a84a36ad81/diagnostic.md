# m-shift_reversal-a84a36ad81

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='naChans']", "new": "45.0 mV", "old": "50.0 mV"}], "element": "channelDensity", "element_id": "naChans", "generator_seed": 20260917, "shift_mV": -5.0}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='naChans']", "attribute": "erev", "old": "50.0 mV", "new": "45.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 616.585 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 95.13947677592056 | 90.14626693705294 | 4.99321 | 1.90279 | `r-5f0a94c66ff17cd98a0a` | `r-89a1a2b96b8a791c108a` |
| h/1 | P00_canonical | last_isi | exceeds | 16.12999999998533 | 17.11999999998443 | 0.99 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-89a1a2b96b8a791c108a` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-89a1a2b96b8a791c108a` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.02424697766546001 | 0.00180999 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-d6b9f28d863b9c4e6677` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 92.72434234740876 | 87.60686111578283 | 5.11748 | 1.85449 | `r-66b1007575e04915ac55` | `r-bfa06c762a4dba558f04` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 91.2126808181487 | 85.9803009043604 | 5.23238 | 1.82425 | `r-940eedfaa66e3fa96c16` | `r-aea1e8518b9b5ef4c003` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 106.45812988261622 | 101.81092071497223 | 4.64721 | 2.12916 | `r-efc8f2fd727ba1854c5f` | `r-096e7f15ef4c7758cd7b` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 95.29706954941832 | 90.31406402572833 | 4.98301 | 1.90279 | `r-d4235ef154cdc2eeb44c` | `r-45421d731021d98553bd` |
| h/2 | P00_canonical | last_isi | exceeds | 16.059999999985394 | 17.049999999984493 | 0.99 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-45421d731021d98553bd` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-45421d731021d98553bd` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02240284133597432 | 0.02424697766546001 | 0.00184414 | 0.00044874 | `s-b96e12fd1e882cb18a94` | `s-ead643a8a37cb0adb809` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 92.82558822777118 | 87.7086944595151 | 5.11689 | 1.85449 | `r-8d6f46142acd4ec898a7` | `r-c1e8d2030732f59318af` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 91.37988662862392 | 86.03727340806732 | 5.34261 | 1.82425 | `r-a455ac42295a97429d02` | `r-3acd6e1b2e160989eaf4` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 106.43966293307548 | 101.79677581805484 | 4.64289 | 2.12916 | `r-2c9f7eaf5c4d0d4f33d4` | `r-245c286eefe7e6ed1196` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
