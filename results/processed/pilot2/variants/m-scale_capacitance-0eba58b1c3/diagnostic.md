# m-scale_capacitance-0eba58b1c3

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/specificCapacitance[1]", "new": "0.8 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.8, "generator_seed": 20260917}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "0.8 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 584.991 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 95.13947677592056 | 97.14858627300546 | 2.00911 | 1.90279 | `r-5f0a94c66ff17cd98a0a` | `r-69c6fb93bebe030ea257` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.019841540878355306 | 0.00259545 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-74503cb5b6eaac39bdda` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 3.5399999998689395 | 2.9999999998694307 | 0.54 | 0.5 | `r-66b1007575e04915ac55` | `r-08c2f70900d24c6b7146` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 91.2126808181487 | 93.39929580778312 | 2.18661 | 1.82425 | `r-940eedfaa66e3fa96c16` | `r-4caf4c1f9747f4577235` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 4.42999999986813 | 3.679999999868812 | 0.75 | 0.5 | `r-940eedfaa66e3fa96c16` | `r-4caf4c1f9747f4577235` |
| h/1 | P08_rebound | first_spike_latency | exceeds | 5.219999999412721 | 4.269999999413585 | 0.95 | 0.5 | `r-011ab0e03522b12f620c` | `r-35d82a541f4f97b97d02` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 95.29706954941832 | 97.3439064023932 | 2.04684 | 1.90279 | `r-d4235ef154cdc2eeb44c` | `r-fa180c167d90c1a455cc` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02240284133597432 | 0.019807390205587052 | 0.00259545 | 0.00044874 | `s-b96e12fd1e882cb18a94` | `s-c5800da5de23133c7fa8` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 92.82558822777118 | 94.69114685176646 | 1.86556 | 1.85449 | `r-8d6f46142acd4ec898a7` | `r-892ca6056e7852e73d18` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 3.509999999868967 | 2.969999999869458 | 0.54 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-892ca6056e7852e73d18` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 91.37988662862392 | 93.48636245868497 | 2.10648 | 1.82425 | `r-a455ac42295a97429d02` | `r-f6ac20cda998d65ba51d` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 4.3899999998681665 | 3.6499999998688395 | 0.74 | 0.5 | `r-a455ac42295a97429d02` | `r-f6ac20cda998d65ba51d` |
| h/2 | P08_rebound | first_spike_latency | exceeds | 5.189999999412748 | 4.239999999413612 | 0.95 | 0.5 | `r-a628bd90e08153ec217d` | `r-f0facc795c1acfff02e6` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
