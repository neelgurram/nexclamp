# m-scale_capacitance-8d53b9976a

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "0.8 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.8, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml", "locator": "/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "0.8 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 7999.145 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.5216693418942094 | 0.5961538461539415 | 0.0744845 | 0.0521669 | `r-068a1eafd4afbbd6d23e` | `r-4ad81b10de1d72340581` |
| h/1 | P00_canonical | ahp_depth | exceeds | -8.248406196708032 | -10.326367164725468 | 2.07796 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-4ad81b10de1d72340581` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 74.70865440368996 | 80.04728317258994 | 5.33863 | 1.49417 | `r-068a1eafd4afbbd6d23e` | `r-4ad81b10de1d72340581` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 2.950000000000788 | 2.2700000000006817 | 0.68 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-4ad81b10de1d72340581` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -3.06435100805065 | -11.189402613277124 | 8.12505 | 1.14578 | `r-96e71f2e3b8549494d50` | `r-3bc2dc6596dd3a852a90` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 29.099999999845693 | 2.6099999998697854 | 26.49 | 0.582 | `r-96e71f2e3b8549494d50` | `r-3bc2dc6596dd3a852a90` |
| h/1 | P05_long_step | ahp_depth | exceeds | -2.799466059340233 | -5.095271143619044 | 2.29581 | 1.17341 | `r-74af15e68cf19cbae102` | `r-fc4a06e8bc4503feecb2` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 72.98996734843095 | 75.77654838611471 | 2.78658 | 1.4598 | `r-74af15e68cf19cbae102` | `r-fc4a06e8bc4503feecb2` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 42.88999999983315 | 41.709999999834224 | 1.18 | 0.8578 | `r-74af15e68cf19cbae102` | `r-fc4a06e8bc4503feecb2` |
| h/1 | P05_long_step | last_isi | exceeds | 24.470000000534128 | 22.670000000494838 | 1.8 | 1.11 | `r-74af15e68cf19cbae102` | `r-fc4a06e8bc4503feecb2` |
| h/1 | P05_long_step | spike_count | exceeds | 83.0 | 90.0 | 7 | 3 | `r-74af15e68cf19cbae102` | `r-fc4a06e8bc4503feecb2` |
| h/1 | P06_ramp | spike_count | exceeds | 70.0 | 78.0 | 8 | 3 | `r-6afcc4c87334b55f282e` | `r-9269b327a9b6d21b0be2` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -2.697613642280899 | -4.39458754979708 | 1.69697 | 1.32669 | `r-289063c903c8c366c952` | `r-176bddb948ef38ceccb4` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 96.16110801631415 | 99.10417175347601 | 2.94306 | 1.92322 | `r-289063c903c8c366c952` | `r-176bddb948ef38ceccb4` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.5214881334190068 | 0.5960151150808239 | 0.074527 | 0.0521669 | `r-87bcc3cd30685deaf603` | `r-2cf7d013c6de31004b72` |
| h/2 | P00_canonical | ahp_depth | exceeds | -8.213585962703469 | -10.287668408446315 | 2.07408 | 0.5 | `r-87bcc3cd30685deaf603` | `r-2cf7d013c6de31004b72` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 74.66815185545984 | 79.96150207520454 | 5.29335 | 1.49417 | `r-87bcc3cd30685deaf603` | `r-2cf7d013c6de31004b72` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 2.950000000000788 | 2.26000000000068 | 0.69 | 0.5 | `r-87bcc3cd30685deaf603` | `r-2cf7d013c6de31004b72` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -2.68242419940799 | -10.81773718764066 | 8.13531 | 1.14578 | `r-6290d36f97e6ddeb2b58` | `r-acfa56f4438db6817340` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 29.029999999845757 | 2.559999999869831 | 26.47 | 0.582 | `r-6290d36f97e6ddeb2b58` | `r-acfa56f4438db6817340` |
| h/2 | P05_long_step | ahp_depth | exceeds | -2.408330571497629 | -4.685679997780866 | 2.27735 | 1.17341 | `r-f1a8b6a7a66c54d9b827` | `r-84d0f90ea012bd3fed09` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 72.5536842363497 | 75.27048110683268 | 2.7168 | 1.4598 | `r-f1a8b6a7a66c54d9b827` | `r-84d0f90ea012bd3fed09` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 42.819999999833215 | 41.6299999998343 | 1.19 | 0.8578 | `r-f1a8b6a7a66c54d9b827` | `r-84d0f90ea012bd3fed09` |
| h/2 | P05_long_step | last_isi | exceeds | 24.840000000542204 | 23.140000000505097 | 1.7 | 1.11 | `r-f1a8b6a7a66c54d9b827` | `r-84d0f90ea012bd3fed09` |
| h/2 | P05_long_step | spike_count | exceeds | 82.0 | 88.0 | 6 | 3 | `r-f1a8b6a7a66c54d9b827` | `r-84d0f90ea012bd3fed09` |
| h/2 | P06_ramp | spike_count | exceeds | 69.0 | 77.0 | 8 | 3 | `r-ce6273bb85e534e50ecc` | `r-2a329bba4da63d0efb7b` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -2.255384099392458 | -3.940066899461769 | 1.68468 | 1.32669 | `r-5eb7b54961cd58341dac` | `r-b13ae148484ae6eb8638` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 95.5725460033362 | 98.48275756678697 | 2.91021 | 1.92322 | `r-5eb7b54961cd58341dac` | `r-b13ae148484ae6eb8638` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
