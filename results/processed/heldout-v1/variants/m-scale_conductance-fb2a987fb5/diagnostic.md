# m-scale_conductance-fb2a987fb5

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='Soma_AllNML2']/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Ih_all']", "new": "0.4 mS_per_cm2", "old": "0.2 mS_per_cm2"}], "element": "channelDensity", "element_id": "Ih_all", "factor": 2.0, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NMC/NeuroML2/Soma_AllNML2.cell.nml", "locator": "/neuroml[@id='Soma_AllNML2']/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Ih_all']", "attribute": "condDensity", "old": "0.2 mS_per_cm2", "new": "0.4 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 5154.188 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -0.540112681203027 | -3.8906974906806653 | 3.35058 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-747e852c94635736328c` |
| h/1 | P00_canonical | last_isi | exceeds | 23.589999999978545 | 22.339999999979682 | 1.25 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-747e852c94635736328c` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 0.8735102996834598 | -2.581690943400062 | 3.4552 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-8c353a18a7c2d87027e2` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 6.8099999998659655 | 6.169999999866548 | 0.64 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-8c353a18a7c2d87027e2` |
| h/1 | P05_long_step | ahp_depth | exceeds | 0.5048961029071961 | -2.8651916147876335 | 3.37009 | 0.5 | `r-a413bdc9ef17abaeb327` | `r-76a2213cf30a561fa390` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 10.129999999862946 | 9.099999999863883 | 1.03 | 0.5 | `r-a413bdc9ef17abaeb327` | `r-76a2213cf30a561fa390` |
| h/1 | P06_ramp | spike_count | exceeds | 33.0 | 34.0 | 1 | 0.5 | `r-fc615de8a8cfe6dc7efe` | `r-f60738cd6f34b66497e4` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -97.96501643676791 | -91.83244063262973 | 6.13258 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-8c353a18a7c2d87027e2` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -0.9663868560786995 | -4.426608240763343 | 3.46022 | 0.5 | `r-c4b56e49cd97e4a16650` | `r-a020bf47ca7aceefd3a5` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 126.55991361679921 | 123.8853492720163 | 2.67456 | 2.5312 | `r-c4b56e49cd97e4a16650` | `r-a020bf47ca7aceefd3a5` |
| h/2 | P00_canonical | ahp_depth | exceeds | -0.5443046181071622 | -3.894671856461713 | 3.35037 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-f4850fe9a49f1023e7b6` |
| h/2 | P00_canonical | last_isi | exceeds | 23.579999999978554 | 22.3199999999797 | 1.26 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-f4850fe9a49f1023e7b6` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 0.8550077082320229 | -2.599239072163897 | 3.45425 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-dc3b1b39511a6bc5d322` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 6.779999999865993 | 6.139999999866575 | 0.64 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-dc3b1b39511a6bc5d322` |
| h/2 | P05_long_step | ahp_depth | exceeds | 0.5178800226843094 | -2.8575245946231433 | 3.3754 | 0.5 | `r-019eab9c744398314e93` | `r-42329345a3058b48d4ac` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 10.099999999862973 | 9.06999999986391 | 1.03 | 0.5 | `r-019eab9c744398314e93` | `r-42329345a3058b48d4ac` |
| h/2 | P06_ramp | spike_count | exceeds | 33.0 | 34.0 | 1 | 0.5 | `r-bd5adb30d6c703f0c55d` | `r-47dd0dc0564fe484eb15` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -97.96501782989534 | -91.83244203338656 | 6.13258 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-dc3b1b39511a6bc5d322` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -0.9949755071020263 | -4.447040280661199 | 3.45206 | 0.5 | `r-c07f6c024edce4a536eb` | `r-1a74e15c7a4baa6a5087` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 125.82009888245024 | 123.16267394834532 | 2.65742 | 2.5312 | `r-c07f6c024edce4a536eb` | `r-1a74e15c7a4baa6a5087` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
