# m-scale_capacitance-7648f6033e

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='Soma_AllNML2']/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "0.5 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NMC/NeuroML2/Soma_AllNML2.cell.nml", "locator": "/neuroml[@id='Soma_AllNML2']/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "0.5 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 5113.855 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.0296528898400037 | 0.01825161980440402 | 0.0114013 | 0.01 | `r-f821a906ac6ddfedc3f9` | `r-479435c23a50be75338b` |
| h/1 | P00_canonical | ahp_depth | exceeds | -0.540112681203027 | -1.0418877158597297 | 0.501775 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-479435c23a50be75338b` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 88.0880088878417 | 98.54535675612749 | 10.4573 | 1.76176 | `r-f821a906ac6ddfedc3f9` | `r-479435c23a50be75338b` |
| h/1 | P00_canonical | last_isi | exceeds | 23.589999999978545 | 15.009999999986348 | 8.58 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-479435c23a50be75338b` |
| h/1 | P00_canonical | spike_count | exceeds | 5.0 | 7.0 | 2 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-479435c23a50be75338b` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.02735468888737108 | 0.026705826104774268 | 0.000648863 | 0.000547094 | `s-02f79883d677a19ab9ec` | `s-564bfa76ec997a67cbbf` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 0.8735102996834598 | 0.02559791819153645 | 0.847912 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-163412bb0f5bd37f4930` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 90.98012542725024 | 100.77965927159796 | 9.79953 | 3.13776 | `r-57ea9af033cb1e2a1b46` | `r-163412bb0f5bd37f4930` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 6.8099999998659655 | 3.369999999869094 | 3.44 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-163412bb0f5bd37f4930` |
| h/1 | P04_step_2x | last_isi | exceeds | 16.709999999984802 | 12.179999999988922 | 4.53 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-163412bb0f5bd37f4930` |
| h/1 | P04_step_2x | spike_count | exceeds | 30.0 | 41.0 | 11 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-163412bb0f5bd37f4930` |
| h/1 | P05_long_step | ahp_depth | exceeds | 0.5048961029071961 | -0.15180076344910276 | 0.656697 | 0.5 | `r-a413bdc9ef17abaeb327` | `r-f7bf85712380f5329ffb` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 87.42731093900892 | 97.96766280169656 | 10.5404 | 3.45091 | `r-a413bdc9ef17abaeb327` | `r-f7bf85712380f5329ffb` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 10.129999999862946 | 4.839999999867757 | 5.29 | 0.5 | `r-a413bdc9ef17abaeb327` | `r-f7bf85712380f5329ffb` |
| h/1 | P05_long_step | last_isi | exceeds | 118.6600000025901 | 112.69000000245978 | 5.97 | 2.3732 | `r-a413bdc9ef17abaeb327` | `r-f7bf85712380f5329ffb` |
| h/1 | P05_long_step | spike_count | exceeds | 16.0 | 17.0 | 1 | 0.5 | `r-a413bdc9ef17abaeb327` | `r-f7bf85712380f5329ffb` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 361.82999999954313 | 352.4399999995517 | 9.39 | 7.2366 | `r-fc615de8a8cfe6dc7efe` | `r-ce69c5c66870bce68759` |
| h/1 | P06_ramp | spike_count | exceeds | 33.0 | 43.0 | 10 | 0.5 | `r-fc615de8a8cfe6dc7efe` | `r-ce69c5c66870bce68759` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -0.9663868560786995 | 2.999642717996437 | 3.96603 | 0.5 | `r-c4b56e49cd97e4a16650` | `r-c625a4e90ca049df4570` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 1.4399999998708495 | 0.7999999998714316 | 0.64 | 0.5 | `r-c4b56e49cd97e4a16650` | `r-c625a4e90ca049df4570` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.029665994195325708 | 0.018264679229826344 | 0.0114013 | 0.01 | `r-1175b1c4f005ecbea9cd` | `r-5576f90d9bbf7892b3ae` |
| h/2 | P00_canonical | ahp_depth | exceeds | -0.5443046181071622 | -1.0513590794560628 | 0.507054 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-5576f90d9bbf7892b3ae` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 88.05227279779325 | 98.35371779784687 | 10.3014 | 1.76176 | `r-1175b1c4f005ecbea9cd` | `r-5576f90d9bbf7892b3ae` |
| h/2 | P00_canonical | last_isi | exceeds | 23.579999999978554 | 14.999999999986358 | 8.58 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-5576f90d9bbf7892b3ae` |
| h/2 | P00_canonical | spike_count | exceeds | 5.0 | 7.0 | 2 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-5576f90d9bbf7892b3ae` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02735468888737108 | 0.026705826104774268 | 0.000648863 | 0.000547094 | `s-220825f25b753f7de32f` | `s-c533f9bdc3d6df1f8f1d` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 0.8550077082320229 | -0.019310170489106326 | 0.874318 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-8c027deb3d3c996ff391` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 89.93420410215381 | 99.93968962269867 | 10.0055 | 3.13776 | `r-2cb2390f7c947ffeefc6` | `r-8c027deb3d3c996ff391` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 6.779999999865993 | 3.3399999998691214 | 3.44 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-8c027deb3d3c996ff391` |
| h/2 | P04_step_2x | last_isi | exceeds | 16.66999999998484 | 12.14999999998895 | 4.52 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-8c027deb3d3c996ff391` |
| h/2 | P04_step_2x | spike_count | exceeds | 30.0 | 41.0 | 11 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-8c027deb3d3c996ff391` |
| h/2 | P05_long_step | ahp_depth | exceeds | 0.5178800226843094 | -0.1900789082836809 | 0.707959 | 0.5 | `r-019eab9c744398314e93` | `r-c12f7583748496066bf9` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 86.27700805705253 | 96.79376219282899 | 10.5168 | 3.45091 | `r-019eab9c744398314e93` | `r-c12f7583748496066bf9` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 10.099999999862973 | 4.8099999998677845 | 5.29 | 0.5 | `r-019eab9c744398314e93` | `r-c12f7583748496066bf9` |
| h/2 | P05_long_step | last_isi | exceeds | 118.89000000259512 | 112.3700000024528 | 6.52 | 2.3732 | `r-019eab9c744398314e93` | `r-c12f7583748496066bf9` |
| h/2 | P05_long_step | spike_count | exceeds | 16.0 | 17.0 | 1 | 0.5 | `r-019eab9c744398314e93` | `r-c12f7583748496066bf9` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 361.7799999995432 | 352.3899999995517 | 9.39 | 7.2366 | `r-bd5adb30d6c703f0c55d` | `r-5952121dd3e131788815` |
| h/2 | P06_ramp | spike_count | exceeds | 33.0 | 43.0 | 10 | 0.5 | `r-bd5adb30d6c703f0c55d` | `r-5952121dd3e131788815` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -0.9949755071020263 | 2.9205473124261943 | 3.91552 | 0.5 | `r-c07f6c024edce4a536eb` | `r-8b01467377e2c1bad2a4` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 1.4299999998708586 | 0.7899999998714407 | 0.64 | 0.5 | `r-c07f6c024edce4a536eb` | `r-8b01467377e2c1bad2a4` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
