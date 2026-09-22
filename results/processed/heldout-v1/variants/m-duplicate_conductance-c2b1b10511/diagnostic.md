# m-duplicate_conductance-c2b1b10511

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / duplicate_conductance
- parameters: `{"generator_seed": 20260917, "new_id": "NaTa_t_all_dup", "source_id": "NaTa_t_all"}`
- recorded edits: `[{"file": "NMC/NeuroML2/Soma_AllNML2.cell.nml", "locator": "/neuroml[@id='Soma_AllNML2']/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='NaTa_t_all_dup']", "attribute": null, "old": null, "new": "<channelDensity xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" condDensity=\"200.0 mS_per_cm2\" id=\"NaTa_t_all_dup\" ionChannel=\"NaTa_t\" ion=\"na\" erev=\"50.0 mV\"/>", "action": "insert", "note": "duplicate_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 5651.345 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.0296528898400037 | 0.016099581519417 | 0.0135533 | 0.01 | `r-f821a906ac6ddfedc3f9` | `r-d37144b8a38a40d8e296` |
| h/1 | P00_canonical | ahp_depth | exceeds | -0.540112681203027 | -1.4755045064798082 | 0.935392 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-d37144b8a38a40d8e296` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 88.0880088878417 | 96.50152588482932 | 8.41352 | 1.76176 | `r-f821a906ac6ddfedc3f9` | `r-d37144b8a38a40d8e296` |
| h/1 | P00_canonical | last_isi | exceeds | 23.589999999978545 | 18.99999999998272 | 4.59 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-d37144b8a38a40d8e296` |
| h/1 | P00_canonical | spike_count | exceeds | 5.0 | 6.0 | 1 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-d37144b8a38a40d8e296` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.02735468888737108 | 0.025339799194044124 | 0.00201489 | 0.000547094 | `s-02f79883d677a19ab9ec` | `s-853b349e2a7493dcb0b5` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 0.8735102996834598 | -0.09203015899387879 | 0.96554 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-a603b0a3edcb749582f7` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 90.98012542725024 | 98.52156066912934 | 7.54144 | 3.13776 | `r-57ea9af033cb1e2a1b46` | `r-a603b0a3edcb749582f7` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 6.8099999998659655 | 6.209999999866511 | 0.6 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-a603b0a3edcb749582f7` |
| h/1 | P04_step_2x | last_isi | exceeds | 16.709999999984802 | 15.229999999986148 | 1.48 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-a603b0a3edcb749582f7` |
| h/1 | P04_step_2x | spike_count | exceeds | 30.0 | 33.0 | 3 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-a603b0a3edcb749582f7` |
| h/1 | P05_long_step | ahp_depth | exceeds | 0.5048961029071961 | -0.3493238601644322 | 0.85422 | 0.5 | `r-a413bdc9ef17abaeb327` | `r-87230c9812320b33d936` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 87.42731093900892 | 95.86231994317168 | 8.43501 | 3.45091 | `r-a413bdc9ef17abaeb327` | `r-87230c9812320b33d936` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 10.129999999862946 | 9.06999999986391 | 1.06 | 0.5 | `r-a413bdc9ef17abaeb327` | `r-87230c9812320b33d936` |
| h/1 | P05_long_step | last_isi | exceeds | 118.6600000025901 | 115.28000000251632 | 3.38 | 2.3732 | `r-a413bdc9ef17abaeb327` | `r-87230c9812320b33d936` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 361.82999999954313 | 336.709999999566 | 25.12 | 7.2366 | `r-fc615de8a8cfe6dc7efe` | `r-ba3f0f12e5799658bb96` |
| h/1 | P06_ramp | spike_count | exceeds | 33.0 | 36.0 | 3 | 0.5 | `r-fc615de8a8cfe6dc7efe` | `r-ba3f0f12e5799658bb96` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.029665994195325708 | 0.016196219006898504 | 0.0134698 | 0.01 | `r-1175b1c4f005ecbea9cd` | `r-113732ca2e892f526e3f` |
| h/2 | P00_canonical | ahp_depth | exceeds | -0.5443046181071622 | -1.483526346090386 | 0.939222 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-113732ca2e892f526e3f` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 88.05227279779325 | 96.38659667966701 | 8.33432 | 1.76176 | `r-1175b1c4f005ecbea9cd` | `r-113732ca2e892f526e3f` |
| h/2 | P00_canonical | last_isi | exceeds | 23.579999999978554 | 18.99999999998272 | 4.58 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-113732ca2e892f526e3f` |
| h/2 | P00_canonical | spike_count | exceeds | 5.0 | 6.0 | 1 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-113732ca2e892f526e3f` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02735468888737108 | 0.025339799194044124 | 0.00201489 | 0.000547094 | `s-220825f25b753f7de32f` | `s-2117a10341f00ec50ff9` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 0.8550077082320229 | -0.13177295176228654 | 0.986781 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-09860a9e29072eaad1c7` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 89.93420410215381 | 97.78573227015204 | 7.85153 | 3.13776 | `r-2cb2390f7c947ffeefc6` | `r-09860a9e29072eaad1c7` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 6.779999999865993 | 6.1799999998665385 | 0.6 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-09860a9e29072eaad1c7` |
| h/2 | P04_step_2x | last_isi | exceeds | 16.66999999998484 | 15.199999999986176 | 1.47 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-09860a9e29072eaad1c7` |
| h/2 | P04_step_2x | spike_count | exceeds | 30.0 | 33.0 | 3 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-09860a9e29072eaad1c7` |
| h/2 | P05_long_step | ahp_depth | exceeds | 0.5178800226843094 | -0.379003481547457 | 0.896884 | 0.5 | `r-019eab9c744398314e93` | `r-8e38d5b3bfed8d1bc7fc` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 86.27700805705253 | 95.03030777281958 | 8.7533 | 3.45091 | `r-019eab9c744398314e93` | `r-8e38d5b3bfed8d1bc7fc` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 10.099999999862973 | 9.039999999863937 | 1.06 | 0.5 | `r-019eab9c744398314e93` | `r-8e38d5b3bfed8d1bc7fc` |
| h/2 | P05_long_step | last_isi | exceeds | 118.89000000259512 | 115.0500000025113 | 3.84 | 2.3732 | `r-019eab9c744398314e93` | `r-8e38d5b3bfed8d1bc7fc` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 361.7799999995432 | 336.64999999956603 | 25.13 | 7.2366 | `r-bd5adb30d6c703f0c55d` | `r-af2b1784bb1084e5d49b` |
| h/2 | P06_ramp | spike_count | exceeds | 33.0 | 36.0 | 3 | 0.5 | `r-bd5adb30d6c703f0c55d` | `r-af2b1784bb1084e5d49b` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
