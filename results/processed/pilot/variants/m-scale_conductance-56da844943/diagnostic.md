# m-scale_conductance-56da844943

- model: `pospischil2008_rs`
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all']", "new": "0.0875 mS_per_cm2", "old": "0.07 mS_per_cm2"}], "element": "channelDensity", "element_id": "IM_all", "factor": 1.25, "generator_seed": 20260913}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all']", "attribute": "condDensity", "old": "0.07 mS_per_cm2", "new": "0.0875 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1661.494 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.2988218828985024 | 0.5961483092869254 | 0.297326 | 0.0298822 | `r-5171ec6a0414fa8c47f8` | `r-9ac73645c86e12ac0949` |
| h/1 | P00_canonical | first_isi | exceeds | 28.06999999997447 | 31.659999999971205 | 3.59 | 0.5614 | `r-5171ec6a0414fa8c47f8` | `r-9ac73645c86e12ac0949` |
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 249.46999999977317 | 113.49 | 2.7196 | `r-5171ec6a0414fa8c47f8` | `r-9ac73645c86e12ac0949` |
| h/1 | P00_canonical | mean_frequency | exceeds | 17.03113291098414 | 10.944511327583005 | 6.08662 | 0.851557 | `r-5171ec6a0414fa8c47f8` | `r-9ac73645c86e12ac0949` |
| h/1 | P00_canonical | spike_count | exceeds | 5.0 | 4.0 | 1 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-9ac73645c86e12ac0949` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.5606515948364182 | 0.5721262208865514 | 0.0114746 | 0.011213 | `s-e75f45f43aa09d678807` | `s-b1a5762bba50d52a479f` |
| h/1 | P04_step_2x | adaptation_index | exceeds | 0.018020491828063687 | 0.03280420790877508 | 0.0147837 | 0.01 | `r-0c0f3a761516cf334965` | `r-fd20409f762963c4c12e` |
| h/1 | P04_step_2x | last_isi | exceeds | 28.16999999997438 | 37.78999999996563 | 9.62 | 0.5634 | `r-0c0f3a761516cf334965` | `r-fd20409f762963c4c12e` |
| h/1 | P04_step_2x | mean_frequency | exceeds | 44.11292909854356 | 36.36441421211172 | 7.74851 | 2.20565 | `r-0c0f3a761516cf334965` | `r-fd20409f762963c4c12e` |
| h/1 | P04_step_2x | spike_count | exceeds | 22.0 | 17.0 | 5 | 0.5 | `r-0c0f3a761516cf334965` | `r-fd20409f762963c4c12e` |
| h/1 | P05_long_step | adaptation_index | exceeds | 0.02130270892949869 | 0.04297364534361711 | 0.0216709 | 0.01 | `r-6299bd8dadd5e9592d63` | `r-738317bd97eedc831da7` |
| h/1 | P05_long_step | first_isi | exceeds | 21.2199999999807 | 22.7599999999793 | 1.54 | 0.6 | `r-6299bd8dadd5e9592d63` | `r-738317bd97eedc831da7` |
| h/1 | P05_long_step | last_isi | exceeds | 78.13000000170541 | 123.58000000269749 | 45.45 | 1.5626 | `r-6299bd8dadd5e9592d63` | `r-738317bd97eedc831da7` |
| h/1 | P05_long_step | mean_frequency | exceeds | 14.694109182274286 | 9.852370013522695 | 4.84174 | 0.734705 | `r-6299bd8dadd5e9592d63` | `r-738317bd97eedc831da7` |
| h/1 | P05_long_step | spike_count | exceeds | 29.0 | 19.0 | 10 | 0.5 | `r-6299bd8dadd5e9592d63` | `r-738317bd97eedc831da7` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 381.69999999952506 | 394.04999999951383 | 12.35 | 7.634 | `r-7054f91d1e6b5f4b29f8` | `r-edd29d951fd4a5172220` |
| h/1 | P06_ramp | mean_frequency | exceeds | 30.288956646438177 | 26.052104208443865 | 4.23685 | 1.51445 | `r-7054f91d1e6b5f4b29f8` | `r-edd29d951fd4a5172220` |
| h/1 | P06_ramp | spike_count | exceeds | 30.0 | 26.0 | 4 | 0.5 | `r-7054f91d1e6b5f4b29f8` | `r-edd29d951fd4a5172220` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.2989579287624928 | 0.5966418866957192 | 0.297684 | 0.0298822 | `r-35d4f8d415fe0d06a895` | `r-794e9c0d0d549109432a` |
| h/2 | P00_canonical | first_isi | exceeds | 28.029999999974507 | 31.60999999997125 | 3.58 | 0.5614 | `r-35d4f8d415fe0d06a895` | `r-794e9c0d0d549109432a` |
| h/2 | P00_canonical | last_isi | exceeds | 135.78999999987656 | 249.13999999977347 | 113.35 | 2.7196 | `r-35d4f8d415fe0d06a895` | `r-794e9c0d0d549109432a` |
| h/2 | P00_canonical | mean_frequency | exceeds | 17.059606264310375 | 10.961606971595842 | 6.098 | 0.851557 | `r-35d4f8d415fe0d06a895` | `r-794e9c0d0d549109432a` |
| h/2 | P00_canonical | spike_count | exceeds | 5.0 | 4.0 | 1 | 0.5 | `r-35d4f8d415fe0d06a895` | `r-794e9c0d0d549109432a` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.5606515948364182 | 0.5721262208865514 | 0.0114746 | 0.011213 | `s-3f9a22347a7b118b5e38` | `s-173f8c7e0eab95fc11d5` |
| h/2 | P04_step_2x | adaptation_index | exceeds | 0.018206269147133136 | 0.033066418846038045 | 0.0148601 | 0.01 | `r-13ae588754662eb409bf` | `r-6c8ce186ad5e6266e201` |
| h/2 | P04_step_2x | last_isi | exceeds | 28.06999999997447 | 37.68999999996572 | 9.62 | 0.5634 | `r-13ae588754662eb409bf` | `r-6c8ce186ad5e6266e201` |
| h/2 | P04_step_2x | mean_frequency | exceeds | 44.38974193423394 | 36.569363478004895 | 7.82038 | 2.20565 | `r-13ae588754662eb409bf` | `r-6c8ce186ad5e6266e201` |
| h/2 | P04_step_2x | spike_count | exceeds | 22.0 | 17.0 | 5 | 0.5 | `r-13ae588754662eb409bf` | `r-6c8ce186ad5e6266e201` |
| h/2 | P05_long_step | adaptation_index | exceeds | 0.021450084876352596 | 0.043211298708767505 | 0.0217612 | 0.01 | `r-a71c890435a70aeaf61b` | `r-4091ca8f6c8b66cb4b87` |
| h/2 | P05_long_step | first_isi | exceeds | 21.019999999980882 | 22.5399999999795 | 1.52 | 0.6 | `r-a71c890435a70aeaf61b` | `r-4091ca8f6c8b66cb4b87` |
| h/2 | P05_long_step | last_isi | exceeds | 77.97000000170192 | 123.3100000026916 | 45.34 | 1.5626 | `r-a71c890435a70aeaf61b` | `r-4091ca8f6c8b66cb4b87` |
| h/2 | P05_long_step | mean_frequency | exceeds | 14.734349834088421 | 9.882862076846704 | 4.85149 | 0.734705 | `r-a71c890435a70aeaf61b` | `r-4091ca8f6c8b66cb4b87` |
| h/2 | P05_long_step | spike_count | exceeds | 29.0 | 19.0 | 10 | 0.5 | `r-a71c890435a70aeaf61b` | `r-4091ca8f6c8b66cb4b87` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 381.6399999995251 | 393.9999999995139 | 12.36 | 7.634 | `r-2c42dd73d53f21fe7690` | `r-e0b10467288842f47021` |
| h/2 | P06_ramp | mean_frequency | exceeds | 30.358227079570092 | 26.102059050916065 | 4.25617 | 1.51445 | `r-2c42dd73d53f21fe7690` | `r-e0b10467288842f47021` |
| h/2 | P06_ramp | spike_count | exceeds | 30.0 | 26.0 | 4 | 0.5 | `r-2c42dd73d53f21fe7690` | `r-e0b10467288842f47021` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
