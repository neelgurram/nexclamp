# m-scale_conductance-ae18f4c43e

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='naChans']", "new": "150.0 mS_per_cm2", "old": "120.0 mS_per_cm2"}], "element": "channelDensity", "element_id": "naChans", "factor": 1.25, "generator_seed": 20260917}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='naChans']", "attribute": "condDensity", "old": "120.0 mS_per_cm2", "new": "150.0 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 613.925 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 95.13947677592056 | 98.40600585919444 | 3.26653 | 1.90279 | `r-5f0a94c66ff17cd98a0a` | `r-60577319b329b3cce6b4` |
| h/1 | P00_canonical | last_isi | exceeds | 16.12999999998533 | 14.569999999986749 | 1.56 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-60577319b329b3cce6b4` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.014445734580971245 | 0.00799126 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-5b1cf6bc34541e62cad7` |
| h/1 | P04_step_2x | adaptation_index | definedness | None | 0.0 |  | inf | `r-66b1007575e04915ac55` | `r-59604b72727b2cbead5d` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 92.72434234740876 | 96.61985778927826 | 3.89552 | 1.85449 | `r-66b1007575e04915ac55` | `r-59604b72727b2cbead5d` |
| h/1 | P04_step_2x | last_isi | definedness | None | 17.01999999998452 |  | inf | `r-66b1007575e04915ac55` | `r-59604b72727b2cbead5d` |
| h/1 | P04_step_2x | spike_count | exceeds | 1.0 | 30.0 | 29 | 0.5 | `r-66b1007575e04915ac55` | `r-59604b72727b2cbead5d` |
| h/1 | P05_long_step | adaptation_index | definedness | None | -2.5663727087059514e-06 |  | inf | `r-940eedfaa66e3fa96c16` | `r-15cd0326b846ce4f5961` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 91.2126808181487 | 95.7896537792231 | 4.57697 | 1.82425 | `r-940eedfaa66e3fa96c16` | `r-15cd0326b846ce4f5961` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 4.42999999986813 | 3.6299999998688577 | 0.8 | 0.5 | `r-940eedfaa66e3fa96c16` | `r-15cd0326b846ce4f5961` |
| h/1 | P05_long_step | last_isi | definedness | None | 18.550000000404907 |  | inf | `r-940eedfaa66e3fa96c16` | `r-15cd0326b846ce4f5961` |
| h/1 | P05_long_step | spike_count | exceeds | 1.0 | 108.0 | 107 | 0.5 | `r-940eedfaa66e3fa96c16` | `r-15cd0326b846ce4f5961` |
| h/1 | P08_rebound | first_spike_latency | exceeds | 5.219999999412721 | 4.5399999994133395 | 0.68 | 0.5 | `r-011ab0e03522b12f620c` | `r-d2d18ef02b200dda5240` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 95.29706954941832 | 98.56742095928152 | 3.27035 | 1.90279 | `r-d4235ef154cdc2eeb44c` | `r-7cba09a2f7798a6d48ae` |
| h/2 | P00_canonical | last_isi | exceeds | 16.059999999985394 | 14.499999999986812 | 1.56 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-7cba09a2f7798a6d48ae` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02240284133597432 | 0.014445734580971245 | 0.00795711 | 0.00044874 | `s-b96e12fd1e882cb18a94` | `s-67f54ae403118d1fa058` |
| h/2 | P04_step_2x | adaptation_index | definedness | None | 0.0 |  | inf | `r-8d6f46142acd4ec898a7` | `r-1dc0a9d2342745347517` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 92.82558822777118 | 96.72834396492894 | 3.90276 | 1.85449 | `r-8d6f46142acd4ec898a7` | `r-1dc0a9d2342745347517` |
| h/2 | P04_step_2x | last_isi | definedness | None | 16.979999999984557 |  | inf | `r-8d6f46142acd4ec898a7` | `r-1dc0a9d2342745347517` |
| h/2 | P04_step_2x | spike_count | exceeds | 1.0 | 30.0 | 29 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-1dc0a9d2342745347517` |
| h/2 | P05_long_step | adaptation_index | definedness | None | 1.0827317258705047e-13 |  | inf | `r-a455ac42295a97429d02` | `r-067fda74511560ee62d6` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 91.37988662862392 | 95.86301422269057 | 4.48313 | 1.82425 | `r-a455ac42295a97429d02` | `r-067fda74511560ee62d6` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 4.3899999998681665 | 3.599999999868885 | 0.79 | 0.5 | `r-a455ac42295a97429d02` | `r-067fda74511560ee62d6` |
| h/2 | P05_long_step | last_isi | definedness | None | 18.520000000404252 |  | inf | `r-a455ac42295a97429d02` | `r-067fda74511560ee62d6` |
| h/2 | P05_long_step | spike_count | exceeds | 1.0 | 108.0 | 107 | 0.5 | `r-a455ac42295a97429d02` | `r-067fda74511560ee62d6` |
| h/2 | P08_rebound | first_spike_latency | exceeds | 5.189999999412748 | 4.509999999413367 | 0.68 | 0.5 | `r-a628bd90e08153ec217d` | `r-7af13a9e673a69eb3166` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
