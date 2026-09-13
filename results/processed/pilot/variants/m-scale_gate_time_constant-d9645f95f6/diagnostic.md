# m-scale_gate_time_constant-d9645f95f6

- model: `pospischil2008_rs`
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"channel": "Kd", "factor": 2.0, "gate": "n", "generator_seed": 20260913, "mechanism": "q10_insert"}`
- recorded edits: `[{"file": "NeuroML2/channels/Kd/Kd.channel.nml", "locator": "/neuroml[@id='Kd']/ionChannel[@id='Kd']/gate[@id='n']/q10Settings[1]", "attribute": null, "old": null, "new": "<q10Settings xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" type=\"q10Fixed\" fixedQ10=\"2\"/>", "action": "insert", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1683.528 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.2988218828985024 | 0.19920398604449005 | 0.0996179 | 0.0298822 | `r-5171ec6a0414fa8c47f8` | `r-737529255eb4f60bbbb4` |
| h/1 | P00_canonical | ahp_depth | exceeds | 2.861194747922525 | 13.111057418820408 | 10.2499 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-737529255eb4f60bbbb4` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 88.85420990112726 | 85.72747039903527 | 3.12674 | 1.77708 | `r-5171ec6a0414fa8c47f8` | `r-737529255eb4f60bbbb4` |
| h/1 | P00_canonical | ap_half_width | exceeds | 0.6999999999993634 | 0.5499999999994998 | 0.15 | 0.05 | `r-5171ec6a0414fa8c47f8` | `r-737529255eb4f60bbbb4` |
| h/1 | P00_canonical | first_isi | exceeds | 28.06999999997447 | 19.0199999999827 | 9.05 | 0.5614 | `r-5171ec6a0414fa8c47f8` | `r-737529255eb4f60bbbb4` |
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 122.54999999988854 | 13.43 | 2.7196 | `r-5171ec6a0414fa8c47f8` | `r-737529255eb4f60bbbb4` |
| h/1 | P00_canonical | mean_frequency | exceeds | 17.03113291098414 | 19.14608462571815 | 2.11495 | 0.851557 | `r-5171ec6a0414fa8c47f8` | `r-737529255eb4f60bbbb4` |
| h/1 | P00_canonical | spike_count | exceeds | 5.0 | 7.0 | 2 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-737529255eb4f60bbbb4` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 3.2025415878387236 | 13.305713890079495 | 10.1032 | 1.22099 | `r-0c0f3a761516cf334965` | `r-d5300717bf59d5478afb` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 89.49588775782593 | 86.65063858028458 | 2.84525 | 1.78992 | `r-0c0f3a761516cf334965` | `r-d5300717bf59d5478afb` |
| h/1 | P04_step_2x | ap_half_width | exceeds | 0.6999999999993634 | 0.5499999999994998 | 0.15 | 0.05 | `r-0c0f3a761516cf334965` | `r-d5300717bf59d5478afb` |
| h/1 | P04_step_2x | first_isi | exceeds | 13.069999999988113 | 8.999999999991815 | 4.07 | 0.5 | `r-0c0f3a761516cf334965` | `r-d5300717bf59d5478afb` |
| h/1 | P04_step_2x | last_isi | exceeds | 28.16999999997438 | 22.3199999999797 | 5.85 | 0.5634 | `r-0c0f3a761516cf334965` | `r-d5300717bf59d5478afb` |
| h/1 | P04_step_2x | mean_frequency | exceeds | 44.11292909854356 | 58.05805805812572 | 13.9451 | 2.20565 | `r-0c0f3a761516cf334965` | `r-d5300717bf59d5478afb` |
| h/1 | P04_step_2x | spike_count | exceeds | 22.0 | 29.0 | 7 | 0.5 | `r-0c0f3a761516cf334965` | `r-d5300717bf59d5478afb` |
| h/1 | P05_long_step | ahp_depth | exceeds | 2.4773294906594145 | 12.661575553894153 | 10.1842 | 1.19998 | `r-6299bd8dadd5e9592d63` | `r-0f8a81ca109a956dd6c3` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 89.18265915023935 | 86.27140045211424 | 2.91126 | 1.78365 | `r-6299bd8dadd5e9592d63` | `r-0f8a81ca109a956dd6c3` |
| h/1 | P05_long_step | ap_half_width | exceeds | 0.6999999999993634 | 0.5599999999994907 | 0.14 | 0.05 | `r-6299bd8dadd5e9592d63` | `r-0f8a81ca109a956dd6c3` |
| h/1 | P05_long_step | first_isi | exceeds | 21.2199999999807 | 14.599999999986721 | 6.62 | 0.6 | `r-6299bd8dadd5e9592d63` | `r-0f8a81ca109a956dd6c3` |
| h/1 | P05_long_step | last_isi | exceeds | 78.13000000170541 | 62.480000001363805 | 15.65 | 1.5626 | `r-6299bd8dadd5e9592d63` | `r-0f8a81ca109a956dd6c3` |
| h/1 | P05_long_step | mean_frequency | exceeds | 14.694109182274286 | 18.521021359208127 | 3.82691 | 0.734705 | `r-6299bd8dadd5e9592d63` | `r-0f8a81ca109a956dd6c3` |
| h/1 | P05_long_step | spike_count | exceeds | 29.0 | 37.0 | 8 | 0.5 | `r-6299bd8dadd5e9592d63` | `r-0f8a81ca109a956dd6c3` |
| h/1 | P06_ramp | mean_frequency | exceeds | 30.288956646438177 | 40.29374137466282 | 10.0048 | 1.51445 | `r-7054f91d1e6b5f4b29f8` | `r-3c38ca0a5fdaf704624e` |
| h/1 | P06_ramp | spike_count | exceeds | 30.0 | 40.0 | 10 | 0.5 | `r-7054f91d1e6b5f4b29f8` | `r-3c38ca0a5fdaf704624e` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -1.4308354873657265 | -0.8396184463501015 | 0.591217 | 0.5 | `r-4a031cb8037cbebd46bc` | `r-f4ceb49cd2b39f4c34ac` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 119.13114547927412 | 116.42499542379628 | 2.70615 | 2.38262 | `r-4a031cb8037cbebd46bc` | `r-f4ceb49cd2b39f4c34ac` |
| h/1 | P09_short_pulse | ap_half_width | exceeds | 0.8799999999991996 | 0.7299999999993361 | 0.15 | 0.05 | `r-4a031cb8037cbebd46bc` | `r-f4ceb49cd2b39f4c34ac` |
| h/1 | P10_paired_pulses | ap_amplitude | exceeds | 119.13114547927412 | 116.42499542379628 | 2.70615 | 2.38262 | `r-4a031cb8037cbebd46bc` | `r-f4ceb49cd2b39f4c34ac` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.2989579287624928 | 0.1996090880296555 | 0.0993488 | 0.0298822 | `r-35d4f8d415fe0d06a895` | `r-0df290cbb03f501b324b` |
| h/2 | P00_canonical | ahp_depth | exceeds | 2.9394112752346615 | 13.194061391198062 | 10.2547 | 0.5 | `r-35d4f8d415fe0d06a895` | `r-0df290cbb03f501b324b` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 88.78027725318925 | 85.72493743942586 | 3.05534 | 1.77708 | `r-35d4f8d415fe0d06a895` | `r-0df290cbb03f501b324b` |
| h/2 | P00_canonical | ap_half_width | exceeds | 0.6999999999993634 | 0.5599999999994907 | 0.14 | 0.05 | `r-35d4f8d415fe0d06a895` | `r-0df290cbb03f501b324b` |
| h/2 | P00_canonical | first_isi | exceeds | 28.029999999974507 | 18.939999999982774 | 9.09 | 0.5614 | `r-35d4f8d415fe0d06a895` | `r-0df290cbb03f501b324b` |
| h/2 | P00_canonical | last_isi | exceeds | 135.78999999987656 | 122.45999999988862 | 13.33 | 2.7196 | `r-35d4f8d415fe0d06a895` | `r-0df290cbb03f501b324b` |
| h/2 | P00_canonical | mean_frequency | exceeds | 17.059606264310375 | 19.1943842715973 | 2.13478 | 0.851557 | `r-35d4f8d415fe0d06a895` | `r-0df290cbb03f501b324b` |
| h/2 | P00_canonical | spike_count | exceeds | 5.0 | 7.0 | 2 | 0.5 | `r-35d4f8d415fe0d06a895` | `r-0df290cbb03f501b324b` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 3.6095391972804407 | 13.742004559842009 | 10.1325 | 1.22099 | `r-13ae588754662eb409bf` | `r-7e3ef93636c6dfbf612e` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 89.44855880885186 | 86.46248245266405 | 2.98608 | 1.78992 | `r-13ae588754662eb409bf` | `r-7e3ef93636c6dfbf612e` |
| h/2 | P04_step_2x | ap_half_width | exceeds | 0.6999999999993634 | 0.5599999999994907 | 0.14 | 0.05 | `r-13ae588754662eb409bf` | `r-7e3ef93636c6dfbf612e` |
| h/2 | P04_step_2x | first_isi | exceeds | 12.92999999998824 | 8.819999999991978 | 4.11 | 0.5 | `r-13ae588754662eb409bf` | `r-7e3ef93636c6dfbf612e` |
| h/2 | P04_step_2x | last_isi | exceeds | 28.06999999997447 | 22.119999999979882 | 5.95 | 0.5634 | `r-13ae588754662eb409bf` | `r-7e3ef93636c6dfbf612e` |
| h/2 | P04_step_2x | mean_frequency | exceeds | 44.38974193423394 | 58.94788194169019 | 14.5581 | 2.20565 | `r-13ae588754662eb409bf` | `r-7e3ef93636c6dfbf612e` |
| h/2 | P04_step_2x | spike_count | exceeds | 22.0 | 29.0 | 7 | 0.5 | `r-13ae588754662eb409bf` | `r-7e3ef93636c6dfbf612e` |
| h/2 | P05_long_step | ahp_depth | exceeds | 2.8773233159343334 | 13.090664075216537 | 10.2133 | 1.19998 | `r-a71c890435a70aeaf61b` | `r-9e4cecdeceb11506cd02` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 89.08078384555085 | 86.02643203932986 | 3.05435 | 1.78365 | `r-a71c890435a70aeaf61b` | `r-9e4cecdeceb11506cd02` |
| h/2 | P05_long_step | ap_half_width | exceeds | 0.6999999999993634 | 0.5599999999994907 | 0.14 | 0.05 | `r-a71c890435a70aeaf61b` | `r-9e4cecdeceb11506cd02` |
| h/2 | P05_long_step | first_isi | exceeds | 21.019999999980882 | 14.289999999987003 | 6.73 | 0.6 | `r-a71c890435a70aeaf61b` | `r-9e4cecdeceb11506cd02` |
| h/2 | P05_long_step | last_isi | exceeds | 77.97000000170192 | 62.28000000135944 | 15.69 | 1.5626 | `r-a71c890435a70aeaf61b` | `r-9e4cecdeceb11506cd02` |
| h/2 | P05_long_step | mean_frequency | exceeds | 14.734349834088421 | 18.612419010792433 | 3.87807 | 0.734705 | `r-a71c890435a70aeaf61b` | `r-9e4cecdeceb11506cd02` |
| h/2 | P05_long_step | spike_count | exceeds | 29.0 | 37.0 | 8 | 0.5 | `r-a71c890435a70aeaf61b` | `r-9e4cecdeceb11506cd02` |
| h/2 | P06_ramp | mean_frequency | exceeds | 30.358227079570092 | 41.13203382863246 | 10.7738 | 1.51445 | `r-2c42dd73d53f21fe7690` | `r-7f018868614a1d66d440` |
| h/2 | P06_ramp | spike_count | exceeds | 30.0 | 41.0 | 11 | 0.5 | `r-2c42dd73d53f21fe7690` | `r-7f018868614a1d66d440` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -1.3990133539835625 | -0.8334844843546563 | 0.565529 | 0.5 | `r-fa41d650658e23c878d5` | `r-08da7d80ab6969884367` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 119.00757217662539 | 116.13793563952757 | 2.86964 | 2.38262 | `r-fa41d650658e23c878d5` | `r-08da7d80ab6969884367` |
| h/2 | P09_short_pulse | ap_half_width | exceeds | 0.8799999999991996 | 0.7299999999993361 | 0.15 | 0.05 | `r-fa41d650658e23c878d5` | `r-08da7d80ab6969884367` |
| h/2 | P10_paired_pulses | ap_amplitude | exceeds | 119.00757217662539 | 116.13793563952757 | 2.86964 | 2.38262 | `r-fa41d650658e23c878d5` | `r-08da7d80ab6969884367` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
