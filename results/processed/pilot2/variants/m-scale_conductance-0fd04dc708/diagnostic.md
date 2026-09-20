# m-scale_conductance-0fd04dc708

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `migliore2014_mt_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nax_ModelViewParmSubset_1']", "new": "44.0 mS_per_cm2", "old": "40.0 mS_per_cm2"}], "element": "channelDensity", "element_id": "nax_ModelViewParmSubset_1", "factor": 1.1, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/Channels/test/MT_soma.cell.nml", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nax_ModelViewParmSubset_1']", "attribute": "condDensity", "old": "40.0 mS_per_cm2", "new": "44.0 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 3939.801 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.024110374974386995 | 0.000580561 | 0.000493819 | `s-41b22c8fa120e2b12315` | `s-7dffc68ff96c9f32dc71` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 27.809999999846866 | 27.07999999984753 | 0.73 | 0.5562 | `r-2e016fe90119b688bc84` | `r-4c74079ffc39bebf36f3` |
| h/1 | P05_long_step | last_isi | exceeds | 112.64000000245869 | 109.88000000239845 | 2.76 | 2.2528 | `r-2e016fe90119b688bc84` | `r-4c74079ffc39bebf36f3` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 400.72999999950775 | 391.7799999995159 | 8.95 | 8.0146 | `r-0cd5f319bb80295395e1` | `r-6a9621571e31cb7ca7ac` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.024110374974386995 | 0.000580561 | 0.000493819 | `s-2231bc09093d4c365d9c` | `s-a86824677274f91b4af5` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 27.769999999846902 | 27.039999999847566 | 0.73 | 0.5562 | `r-002bf860824963a1f621` | `r-1256a4c965bdb3694c5e` |
| h/2 | P05_long_step | last_isi | exceeds | 112.62000000245826 | 109.86000000239801 | 2.76 | 2.2528 | `r-002bf860824963a1f621` | `r-1256a4c965bdb3694c5e` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 400.6799999995078 | 391.72999999951594 | 8.95 | 8.0146 | `r-046a6f9c0b3cbbc75058` | `r-a67cbe4e8a292617f99b` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
