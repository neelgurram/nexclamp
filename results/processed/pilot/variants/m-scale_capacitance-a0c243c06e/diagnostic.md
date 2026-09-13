# m-scale_capacitance-a0c243c06e

- model: `pospischil2008_rs`
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "2.0 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 2.0, "generator_seed": 20260913}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "2.0 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1714.078 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.2988218828985024 | 0.2680047225501773 | 0.0308172 | 0.0298822 | `r-5171ec6a0414fa8c47f8` | `r-44409b16744c0ec94f4e` |
| h/1 | P00_canonical | ahp_depth | exceeds | 2.861194747922525 | 11.688496167500816 | 8.8273 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-44409b16744c0ec94f4e` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 88.85420990112726 | 82.50445556805262 | 6.34975 | 1.77708 | `r-5171ec6a0414fa8c47f8` | `r-44409b16744c0ec94f4e` |
| h/1 | P00_canonical | ap_half_width | exceeds | 0.6999999999993634 | 0.8199999999992542 | 0.12 | 0.05 | `r-5171ec6a0414fa8c47f8` | `r-44409b16744c0ec94f4e` |
| h/1 | P00_canonical | first_isi | exceeds | 28.06999999997447 | 44.31999999995969 | 16.25 | 0.5614 | `r-5171ec6a0414fa8c47f8` | `r-44409b16744c0ec94f4e` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 20.749999999853287 | 41.289999999834606 | 20.54 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-44409b16744c0ec94f4e` |
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 118.13999999989261 | 17.84 | 2.7196 | `r-5171ec6a0414fa8c47f8` | `r-44409b16744c0ec94f4e` |
| h/1 | P00_canonical | mean_frequency | exceeds | 17.03113291098414 | 14.708586137177855 | 2.32255 | 0.851557 | `r-5171ec6a0414fa8c47f8` | `r-44409b16744c0ec94f4e` |
| h/1 | P00_canonical | spike_count | exceeds | 5.0 | 4.0 | 1 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-44409b16744c0ec94f4e` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.5606515948364182 | 0.5760193975821324 | 0.0153678 | 0.011213 | `s-e75f45f43aa09d678807` | `s-f121d707f711c357a63c` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 3.2025415878387236 | 11.981625254316441 | 8.77908 | 1.22099 | `r-0c0f3a761516cf334965` | `r-0988fb003e45615357db` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 89.49588775782593 | 83.2560195934047 | 6.23987 | 1.78992 | `r-0c0f3a761516cf334965` | `r-0988fb003e45615357db` |
| h/1 | P04_step_2x | ap_half_width | exceeds | 0.6999999999993634 | 0.8299999999992451 | 0.13 | 0.05 | `r-0c0f3a761516cf334965` | `r-0988fb003e45615357db` |
| h/1 | P04_step_2x | first_isi | exceeds | 13.069999999988113 | 18.039999999983593 | 4.97 | 0.5 | `r-0c0f3a761516cf334965` | `r-0988fb003e45615357db` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 10.689999999862437 | 20.88999999985316 | 10.2 | 0.5 | `r-0c0f3a761516cf334965` | `r-0988fb003e45615357db` |
| h/1 | P04_step_2x | last_isi | exceeds | 28.16999999997438 | 37.87999999996555 | 9.71 | 0.5634 | `r-0c0f3a761516cf334965` | `r-0988fb003e45615357db` |
| h/1 | P04_step_2x | mean_frequency | exceeds | 44.11292909854356 | 33.492422339485124 | 10.6205 | 2.20565 | `r-0c0f3a761516cf334965` | `r-0988fb003e45615357db` |
| h/1 | P04_step_2x | spike_count | exceeds | 22.0 | 16.0 | 6 | 0.5 | `r-0c0f3a761516cf334965` | `r-0988fb003e45615357db` |
| h/1 | P05_long_step | ahp_depth | exceeds | 2.4773294906594145 | 11.387055094403358 | 8.90973 | 1.19998 | `r-6299bd8dadd5e9592d63` | `r-0e91d131df66c248cbb7` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 89.18265915023935 | 82.87628555444243 | 6.30637 | 1.78365 | `r-6299bd8dadd5e9592d63` | `r-0e91d131df66c248cbb7` |
| h/1 | P05_long_step | ap_half_width | exceeds | 0.6999999999993634 | 0.8199999999992542 | 0.12 | 0.05 | `r-6299bd8dadd5e9592d63` | `r-0e91d131df66c248cbb7` |
| h/1 | P05_long_step | first_isi | exceeds | 21.2199999999807 | 31.659999999971205 | 10.44 | 0.6 | `r-6299bd8dadd5e9592d63` | `r-0e91d131df66c248cbb7` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 16.619999999857043 | 32.81999999984231 | 16.2 | 0.5 | `r-6299bd8dadd5e9592d63` | `r-0e91d131df66c248cbb7` |
| h/1 | P05_long_step | last_isi | exceeds | 78.13000000170541 | 96.57000000210792 | 18.44 | 1.5626 | `r-6299bd8dadd5e9592d63` | `r-0e91d131df66c248cbb7` |
| h/1 | P05_long_step | mean_frequency | exceeds | 14.694109182274286 | 11.87335773392909 | 2.82075 | 0.734705 | `r-6299bd8dadd5e9592d63` | `r-0e91d131df66c248cbb7` |
| h/1 | P05_long_step | spike_count | exceeds | 29.0 | 23.0 | 6 | 0.5 | `r-6299bd8dadd5e9592d63` | `r-0e91d131df66c248cbb7` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 381.69999999952506 | 402.629999999506 | 20.93 | 7.634 | `r-7054f91d1e6b5f4b29f8` | `r-5dde3891fe7dea48c22e` |
| h/1 | P06_ramp | mean_frequency | exceeds | 30.288956646438177 | 23.012656961352604 | 7.2763 | 1.51445 | `r-7054f91d1e6b5f4b29f8` | `r-5dde3891fe7dea48c22e` |
| h/1 | P06_ramp | spike_count | exceeds | 30.0 | 23.0 | 7 | 0.5 | `r-7054f91d1e6b5f4b29f8` | `r-5dde3891fe7dea48c22e` |
| h/1 | P09_short_pulse | ahp_depth | definedness | -1.4308354873657265 | None |  | 0.5 | `r-4a031cb8037cbebd46bc` | `r-866415d3cc534a0140cc` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 119.13114547927412 | 83.06359863387407 | 36.0675 | 2.38262 | `r-4a031cb8037cbebd46bc` | `r-866415d3cc534a0140cc` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 2.1599999998701946 | 4.549999999868021 | 2.39 | 0.5 | `r-4a031cb8037cbebd46bc` | `r-866415d3cc534a0140cc` |
| h/1 | P10_paired_pulses | ap_amplitude | exceeds | 119.13114547927412 | 83.06359863387407 | 36.0675 | 2.38262 | `r-4a031cb8037cbebd46bc` | `r-866415d3cc534a0140cc` |
| h/1 | P10_paired_pulses | first_isi | exceeds | 23.09999999997899 | 22.229999999979782 | 0.87 | 0.5 | `r-4a031cb8037cbebd46bc` | `r-866415d3cc534a0140cc` |
| h/1 | P10_paired_pulses | first_spike_latency | exceeds | 2.1599999998701946 | 4.549999999868021 | 2.39 | 0.5 | `r-4a031cb8037cbebd46bc` | `r-866415d3cc534a0140cc` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.2989579287624928 | 0.26821655365407404 | 0.0307414 | 0.0298822 | `r-35d4f8d415fe0d06a895` | `r-b9519d46091d4501329a` |
| h/2 | P00_canonical | ahp_depth | exceeds | 2.9394112752346615 | 11.751755269368488 | 8.81234 | 0.5 | `r-35d4f8d415fe0d06a895` | `r-b9519d46091d4501329a` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 88.78027725318925 | 82.51181793361825 | 6.26846 | 1.77708 | `r-35d4f8d415fe0d06a895` | `r-b9519d46091d4501329a` |
| h/2 | P00_canonical | ap_half_width | exceeds | 0.6999999999993634 | 0.8299999999992451 | 0.13 | 0.05 | `r-35d4f8d415fe0d06a895` | `r-b9519d46091d4501329a` |
| h/2 | P00_canonical | first_isi | exceeds | 28.029999999974507 | 44.18999999995981 | 16.16 | 0.5614 | `r-35d4f8d415fe0d06a895` | `r-b9519d46091d4501329a` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 20.739999999853296 | 41.279999999834615 | 20.54 | 0.5 | `r-35d4f8d415fe0d06a895` | `r-b9519d46091d4501329a` |
| h/2 | P00_canonical | last_isi | exceeds | 135.78999999987656 | 117.82999999989289 | 17.96 | 2.7196 | `r-35d4f8d415fe0d06a895` | `r-b9519d46091d4501329a` |
| h/2 | P00_canonical | mean_frequency | exceeds | 17.059606264310375 | 14.744369493919873 | 2.31524 | 0.851557 | `r-35d4f8d415fe0d06a895` | `r-b9519d46091d4501329a` |
| h/2 | P00_canonical | spike_count | exceeds | 5.0 | 4.0 | 1 | 0.5 | `r-35d4f8d415fe0d06a895` | `r-b9519d46091d4501329a` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.5606515948364182 | 0.5760193975821324 | 0.0153678 | 0.011213 | `s-3f9a22347a7b118b5e38` | `s-2bf577b6a0df1e6983dd` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 3.6095391972804407 | 12.31192836507229 | 8.70239 | 1.22099 | `r-13ae588754662eb409bf` | `r-63d355e0ec7e170efafe` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 89.44855880885186 | 83.07922363421721 | 6.36934 | 1.78992 | `r-13ae588754662eb409bf` | `r-63d355e0ec7e170efafe` |
| h/2 | P04_step_2x | ap_half_width | exceeds | 0.6999999999993634 | 0.8299999999992451 | 0.13 | 0.05 | `r-13ae588754662eb409bf` | `r-63d355e0ec7e170efafe` |
| h/2 | P04_step_2x | first_isi | exceeds | 12.92999999998824 | 17.739999999983866 | 4.81 | 0.5 | `r-13ae588754662eb409bf` | `r-63d355e0ec7e170efafe` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 10.659999999862464 | 20.859999999853187 | 10.2 | 0.5 | `r-13ae588754662eb409bf` | `r-63d355e0ec7e170efafe` |
| h/2 | P04_step_2x | last_isi | exceeds | 28.06999999997447 | 37.55999999996584 | 9.49 | 0.5634 | `r-13ae588754662eb409bf` | `r-63d355e0ec7e170efafe` |
| h/2 | P04_step_2x | mean_frequency | exceeds | 44.38974193423394 | 33.90189638736918 | 10.4878 | 2.20565 | `r-13ae588754662eb409bf` | `r-63d355e0ec7e170efafe` |
| h/2 | P04_step_2x | spike_count | exceeds | 22.0 | 16.0 | 6 | 0.5 | `r-13ae588754662eb409bf` | `r-63d355e0ec7e170efafe` |
| h/2 | P05_long_step | ahp_depth | exceeds | 2.8773233159343334 | 11.711861226400224 | 8.83454 | 1.19998 | `r-a71c890435a70aeaf61b` | `r-a73fa39fa835448e3f80` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 89.08078384555085 | 82.74891662729607 | 6.33187 | 1.78365 | `r-a71c890435a70aeaf61b` | `r-a73fa39fa835448e3f80` |
| h/2 | P05_long_step | ap_half_width | exceeds | 0.6999999999993634 | 0.8299999999992451 | 0.13 | 0.05 | `r-a71c890435a70aeaf61b` | `r-a73fa39fa835448e3f80` |
| h/2 | P05_long_step | first_isi | exceeds | 21.019999999980882 | 31.16999999997165 | 10.15 | 0.6 | `r-a71c890435a70aeaf61b` | `r-a73fa39fa835448e3f80` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 16.58999999985707 | 32.779999999842346 | 16.19 | 0.5 | `r-a71c890435a70aeaf61b` | `r-a73fa39fa835448e3f80` |
| h/2 | P05_long_step | last_isi | exceeds | 77.97000000170192 | 96.22000000210028 | 18.25 | 1.5626 | `r-a71c890435a70aeaf61b` | `r-a73fa39fa835448e3f80` |
| h/2 | P05_long_step | mean_frequency | exceeds | 14.734349834088421 | 11.933545715843485 | 2.8008 | 0.734705 | `r-a71c890435a70aeaf61b` | `r-a73fa39fa835448e3f80` |
| h/2 | P05_long_step | spike_count | exceeds | 29.0 | 23.0 | 6 | 0.5 | `r-a71c890435a70aeaf61b` | `r-a73fa39fa835448e3f80` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 381.6399999995251 | 402.5799999995061 | 20.94 | 7.634 | `r-2c42dd73d53f21fe7690` | `r-2262cbcf6cd991fa690b` |
| h/2 | P06_ramp | mean_frequency | exceeds | 30.358227079570092 | 23.10396785537305 | 7.25426 | 1.51445 | `r-2c42dd73d53f21fe7690` | `r-2262cbcf6cd991fa690b` |
| h/2 | P06_ramp | spike_count | exceeds | 30.0 | 23.0 | 7 | 0.5 | `r-2c42dd73d53f21fe7690` | `r-2262cbcf6cd991fa690b` |
| h/2 | P09_short_pulse | ahp_depth | definedness | -1.3990133539835625 | None |  | 0.5 | `r-fa41d650658e23c878d5` | `r-562ee432bd1c506b88b1` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 119.00757217662539 | 82.87817001486832 | 36.1294 | 2.38262 | `r-fa41d650658e23c878d5` | `r-562ee432bd1c506b88b1` |
| h/2 | P09_short_pulse | ap_half_width | exceeds | 0.8799999999991996 | 0.8199999999992542 | 0.06 | 0.05 | `r-fa41d650658e23c878d5` | `r-562ee432bd1c506b88b1` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 2.1499999998702037 | 4.519999999868048 | 2.37 | 0.5 | `r-fa41d650658e23c878d5` | `r-562ee432bd1c506b88b1` |
| h/2 | P10_paired_pulses | ap_amplitude | exceeds | 119.00757217662539 | 82.87817001486832 | 36.1294 | 2.38262 | `r-fa41d650658e23c878d5` | `r-562ee432bd1c506b88b1` |
| h/2 | P10_paired_pulses | first_isi | exceeds | 23.089999999979 | 22.21999999997979 | 0.87 | 0.5 | `r-fa41d650658e23c878d5` | `r-562ee432bd1c506b88b1` |
| h/2 | P10_paired_pulses | first_spike_latency | exceeds | 2.1499999998702037 | 4.519999999868048 | 2.37 | 0.5 | `r-fa41d650658e23c878d5` | `r-562ee432bd1c506b88b1` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
