# m-scale_gate_time_constant-244443ee5f

- model: `pospischil2008_rs`
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"channel": "Na", "factor": 1.25, "gate": "h", "generator_seed": 20260913, "mechanism": "q10_insert"}`
- recorded edits: `[{"file": "NeuroML2/channels/Na/Na.channel.nml", "locator": "/neuroml[@id='Na']/ionChannel[@id='Na']/gate[@id='h']/q10Settings[1]", "attribute": null, "old": null, "new": "<q10Settings xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" type=\"q10Fixed\" fixedQ10=\"1.25\"/>", "action": "insert", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1703.864 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.2988218828985024 | 0.22322672820662412 | 0.0755952 | 0.0298822 | `r-5171ec6a0414fa8c47f8` | `r-7dbd1fc334c0e6a4a023` |
| h/1 | P00_canonical | ahp_depth | exceeds | 2.861194747922525 | 3.9489938201904238 | 1.0878 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-7dbd1fc334c0e6a4a023` |
| h/1 | P00_canonical | first_isi | exceeds | 28.06999999997447 | 26.74999999997567 | 1.32 | 0.5614 | `r-5171ec6a0414fa8c47f8` | `r-7dbd1fc334c0e6a4a023` |
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 141.37999999987142 | 5.4 | 2.7196 | `r-5171ec6a0414fa8c47f8` | `r-7dbd1fc334c0e6a4a023` |
| h/1 | P00_canonical | mean_frequency | exceeds | 17.03113291098414 | 15.59900166391288 | 1.43213 | 0.851557 | `r-5171ec6a0414fa8c47f8` | `r-7dbd1fc334c0e6a4a023` |
| h/1 | P00_canonical | spike_count | exceeds | 5.0 | 6.0 | 1 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-7dbd1fc334c0e6a4a023` |
| h/1 | P04_step_2x | last_isi | exceeds | 28.16999999997438 | 26.669999999975744 | 1.5 | 0.5634 | `r-0c0f3a761516cf334965` | `r-c93a95647e79ab528cf4` |
| h/1 | P04_step_2x | mean_frequency | exceeds | 44.11292909854356 | 46.51350914097004 | 2.40058 | 2.20565 | `r-0c0f3a761516cf334965` | `r-c93a95647e79ab528cf4` |
| h/1 | P04_step_2x | spike_count | exceeds | 22.0 | 23.0 | 1 | 0.5 | `r-0c0f3a761516cf334965` | `r-c93a95647e79ab528cf4` |
| h/1 | P05_long_step | ap_half_width | exceeds | 0.6999999999993634 | 0.6399999999994179 | 0.06 | 0.05 | `r-6299bd8dadd5e9592d63` | `r-0499213f80a8244094a6` |
| h/1 | P05_long_step | first_isi | exceeds | 21.2199999999807 | 20.389999999981455 | 0.83 | 0.6 | `r-6299bd8dadd5e9592d63` | `r-0499213f80a8244094a6` |
| h/1 | P05_long_step | last_isi | exceeds | 78.13000000170541 | 72.21000000157619 | 5.92 | 1.5626 | `r-6299bd8dadd5e9592d63` | `r-0499213f80a8244094a6` |
| h/1 | P05_long_step | mean_frequency | exceeds | 14.694109182274286 | 15.872203164178078 | 1.17809 | 0.734705 | `r-6299bd8dadd5e9592d63` | `r-0499213f80a8244094a6` |
| h/1 | P05_long_step | spike_count | exceeds | 29.0 | 31.0 | 2 | 0.5 | `r-6299bd8dadd5e9592d63` | `r-0499213f80a8244094a6` |
| h/1 | P06_ramp | mean_frequency | exceeds | 30.288956646438177 | 32.07859255178508 | 1.78964 | 1.51445 | `r-7054f91d1e6b5f4b29f8` | `r-da9477b2de7e3fb8a2a8` |
| h/1 | P06_ramp | spike_count | exceeds | 30.0 | 32.0 | 2 | 0.5 | `r-7054f91d1e6b5f4b29f8` | `r-da9477b2de7e3fb8a2a8` |
| h/1 | P09_short_pulse | ap_half_width | exceeds | 0.8799999999991996 | 0.8199999999992542 | 0.06 | 0.05 | `r-4a031cb8037cbebd46bc` | `r-aae00ddde86e04c45ffe` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.2989579287624928 | 0.22345443843853738 | 0.0755035 | 0.0298822 | `r-35d4f8d415fe0d06a895` | `r-f700f6102d02e8d74026` |
| h/2 | P00_canonical | ahp_depth | exceeds | 2.9394112752346615 | 4.03341304524514 | 1.094 | 0.5 | `r-35d4f8d415fe0d06a895` | `r-f700f6102d02e8d74026` |
| h/2 | P00_canonical | first_isi | exceeds | 28.029999999974507 | 26.699999999975716 | 1.33 | 0.5614 | `r-35d4f8d415fe0d06a895` | `r-f700f6102d02e8d74026` |
| h/2 | P00_canonical | last_isi | exceeds | 135.78999999987656 | 141.25999999987152 | 5.47 | 2.7196 | `r-35d4f8d415fe0d06a895` | `r-f700f6102d02e8d74026` |
| h/2 | P00_canonical | mean_frequency | exceeds | 17.059606264310375 | 15.628662967902514 | 1.43094 | 0.851557 | `r-35d4f8d415fe0d06a895` | `r-f700f6102d02e8d74026` |
| h/2 | P00_canonical | spike_count | exceeds | 5.0 | 6.0 | 1 | 0.5 | `r-35d4f8d415fe0d06a895` | `r-f700f6102d02e8d74026` |
| h/2 | P04_step_2x | last_isi | exceeds | 28.06999999997447 | 26.539999999975862 | 1.53 | 0.5634 | `r-13ae588754662eb409bf` | `r-068f96be174e7c2ee0ce` |
| h/2 | P04_step_2x | mean_frequency | exceeds | 44.38974193423394 | 46.88041417832272 | 2.49067 | 2.20565 | `r-13ae588754662eb409bf` | `r-068f96be174e7c2ee0ce` |
| h/2 | P04_step_2x | spike_count | exceeds | 22.0 | 23.0 | 1 | 0.5 | `r-13ae588754662eb409bf` | `r-068f96be174e7c2ee0ce` |
| h/2 | P05_long_step | first_isi | exceeds | 21.019999999980882 | 20.169999999981655 | 0.85 | 0.6 | `r-a71c890435a70aeaf61b` | `r-0f967021cbf1ea3ed37b` |
| h/2 | P05_long_step | last_isi | exceeds | 77.97000000170192 | 71.98000000157117 | 5.99 | 1.5626 | `r-a71c890435a70aeaf61b` | `r-0f967021cbf1ea3ed37b` |
| h/2 | P05_long_step | mean_frequency | exceeds | 14.734349834088421 | 15.93584537087274 | 1.2015 | 0.734705 | `r-a71c890435a70aeaf61b` | `r-0f967021cbf1ea3ed37b` |
| h/2 | P05_long_step | spike_count | exceeds | 29.0 | 31.0 | 2 | 0.5 | `r-a71c890435a70aeaf61b` | `r-0f967021cbf1ea3ed37b` |
| h/2 | P06_ramp | mean_frequency | exceeds | 30.358227079570092 | 32.16791652429001 | 1.80969 | 1.51445 | `r-2c42dd73d53f21fe7690` | `r-6c55e71f88e0a8abc1e3` |
| h/2 | P06_ramp | spike_count | exceeds | 30.0 | 32.0 | 2 | 0.5 | `r-2c42dd73d53f21fe7690` | `r-6c55e71f88e0a8abc1e3` |
| h/2 | P09_short_pulse | ap_half_width | exceeds | 0.8799999999991996 | 0.8099999999992633 | 0.07 | 0.05 | `r-fa41d650658e23c878d5` | `r-b280d830b877f659758b` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
