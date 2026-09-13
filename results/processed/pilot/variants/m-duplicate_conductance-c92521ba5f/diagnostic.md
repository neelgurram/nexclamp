# m-duplicate_conductance-c92521ba5f

- model: `pospischil2008_rs`
- kind/family/operator: mutant / reference / duplicate_conductance
- parameters: `{"generator_seed": 20260913, "new_id": "Kd_all_dup", "source_id": "Kd_all"}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all_dup']", "attribute": null, "old": null, "new": "<channelDensity xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" condDensity=\"5.0 mS_per_cm2\" id=\"Kd_all_dup\" ionChannel=\"Kd\" ion=\"k\" erev=\"-100.0 mV\"/>", "action": "insert", "note": "duplicate_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1909.883 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.2988218828985024 | 0.1429851278163409 | 0.155837 | 0.0298822 | `r-5171ec6a0414fa8c47f8` | `r-c1f92ddfaa765e4b602f` |
| h/1 | P00_canonical | ahp_depth | exceeds | 2.861194747922525 | -5.0035055516492974 | 7.8647 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-c1f92ddfaa765e4b602f` |
| h/1 | P00_canonical | ap_half_width | exceeds | 0.6999999999993634 | 0.5699999999994816 | 0.13 | 0.05 | `r-5171ec6a0414fa8c47f8` | `r-c1f92ddfaa765e4b602f` |
| h/1 | P00_canonical | first_isi | exceeds | 28.06999999997447 | 28.989999999973634 | 0.92 | 0.5614 | `r-5171ec6a0414fa8c47f8` | `r-c1f92ddfaa765e4b602f` |
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 112.60999999989758 | 23.37 | 2.7196 | `r-5171ec6a0414fa8c47f8` | `r-c1f92ddfaa765e4b602f` |
| h/1 | P00_canonical | spike_count | exceeds | 5.0 | 7.0 | 2 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-c1f92ddfaa765e4b602f` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 3.2025415878387236 | -5.039371215806526 | 8.24191 | 1.22099 | `r-0c0f3a761516cf334965` | `r-345de44055f94eb9c729` |
| h/1 | P04_step_2x | ap_half_width | exceeds | 0.6999999999993634 | 0.5599999999994907 | 0.14 | 0.05 | `r-0c0f3a761516cf334965` | `r-345de44055f94eb9c729` |
| h/1 | P04_step_2x | first_isi | exceeds | 13.069999999988113 | 14.499999999986812 | 1.43 | 0.5 | `r-0c0f3a761516cf334965` | `r-345de44055f94eb9c729` |
| h/1 | P04_step_2x | last_isi | exceeds | 28.16999999997438 | 24.6299999999776 | 3.54 | 0.5634 | `r-0c0f3a761516cf334965` | `r-345de44055f94eb9c729` |
| h/1 | P04_step_2x | mean_frequency | exceeds | 44.11292909854356 | 47.94663331254335 | 3.8337 | 2.20565 | `r-0c0f3a761516cf334965` | `r-345de44055f94eb9c729` |
| h/1 | P04_step_2x | spike_count | exceeds | 22.0 | 23.0 | 1 | 0.5 | `r-0c0f3a761516cf334965` | `r-345de44055f94eb9c729` |
| h/1 | P05_long_step | ahp_depth | exceeds | 2.4773294906594145 | -5.603931152340664 | 8.08126 | 1.19998 | `r-6299bd8dadd5e9592d63` | `r-e4979aaebd7b41ef87ff` |
| h/1 | P05_long_step | ap_half_width | exceeds | 0.6999999999993634 | 0.5699999999994816 | 0.13 | 0.05 | `r-6299bd8dadd5e9592d63` | `r-e4979aaebd7b41ef87ff` |
| h/1 | P05_long_step | first_isi | exceeds | 21.2199999999807 | 22.699999999979354 | 1.48 | 0.6 | `r-6299bd8dadd5e9592d63` | `r-e4979aaebd7b41ef87ff` |
| h/1 | P05_long_step | last_isi | exceeds | 78.13000000170541 | 58.80000000128348 | 19.33 | 1.5626 | `r-6299bd8dadd5e9592d63` | `r-e4979aaebd7b41ef87ff` |
| h/1 | P05_long_step | mean_frequency | exceeds | 14.694109182274286 | 18.997740809175323 | 4.30363 | 0.734705 | `r-6299bd8dadd5e9592d63` | `r-e4979aaebd7b41ef87ff` |
| h/1 | P05_long_step | spike_count | exceeds | 29.0 | 37.0 | 8 | 0.5 | `r-6299bd8dadd5e9592d63` | `r-e4979aaebd7b41ef87ff` |
| h/1 | P06_ramp | spike_count | exceeds | 30.0 | 31.0 | 1 | 0.5 | `r-7054f91d1e6b5f4b29f8` | `r-c78812d1b5ca99ba04d1` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -1.4308354873657265 | -7.088153564452725 | 5.65732 | 0.5 | `r-4a031cb8037cbebd46bc` | `r-fbc2637a9114ada9075e` |
| h/1 | P09_short_pulse | ap_half_width | exceeds | 0.8799999999991996 | 0.7099999999993543 | 0.17 | 0.05 | `r-4a031cb8037cbebd46bc` | `r-fbc2637a9114ada9075e` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.2989579287624928 | 0.14308410877921884 | 0.155874 | 0.0298822 | `r-35d4f8d415fe0d06a895` | `r-6decade35f605f8943d5` |
| h/2 | P00_canonical | ahp_depth | exceeds | 2.9394112752346615 | -4.905437316894535 | 7.84485 | 0.5 | `r-35d4f8d415fe0d06a895` | `r-6decade35f605f8943d5` |
| h/2 | P00_canonical | ap_half_width | exceeds | 0.6999999999993634 | 0.5699999999994816 | 0.13 | 0.05 | `r-35d4f8d415fe0d06a895` | `r-6decade35f605f8943d5` |
| h/2 | P00_canonical | first_isi | exceeds | 28.029999999974507 | 28.93999999997368 | 0.91 | 0.5614 | `r-35d4f8d415fe0d06a895` | `r-6decade35f605f8943d5` |
| h/2 | P00_canonical | last_isi | exceeds | 135.78999999987656 | 112.50999999989767 | 23.28 | 2.7196 | `r-35d4f8d415fe0d06a895` | `r-6decade35f605f8943d5` |
| h/2 | P00_canonical | spike_count | exceeds | 5.0 | 7.0 | 2 | 0.5 | `r-35d4f8d415fe0d06a895` | `r-6decade35f605f8943d5` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 3.6095391972804407 | -4.5332296244184676 | 8.14277 | 1.22099 | `r-13ae588754662eb409bf` | `r-49161186252a47186b37` |
| h/2 | P04_step_2x | ap_half_width | exceeds | 0.6999999999993634 | 0.5699999999994816 | 0.13 | 0.05 | `r-13ae588754662eb409bf` | `r-49161186252a47186b37` |
| h/2 | P04_step_2x | first_isi | exceeds | 12.92999999998824 | 14.35999999998694 | 1.43 | 0.5 | `r-13ae588754662eb409bf` | `r-49161186252a47186b37` |
| h/2 | P04_step_2x | last_isi | exceeds | 28.06999999997447 | 24.5199999999777 | 3.55 | 0.5634 | `r-13ae588754662eb409bf` | `r-49161186252a47186b37` |
| h/2 | P04_step_2x | mean_frequency | exceeds | 44.38974193423394 | 48.26761243211493 | 3.87787 | 2.20565 | `r-13ae588754662eb409bf` | `r-49161186252a47186b37` |
| h/2 | P04_step_2x | spike_count | exceeds | 22.0 | 23.0 | 1 | 0.5 | `r-13ae588754662eb409bf` | `r-49161186252a47186b37` |
| h/2 | P05_long_step | ahp_depth | exceeds | 2.8773233159343334 | -5.1052053324434326 | 7.98253 | 1.19998 | `r-a71c890435a70aeaf61b` | `r-50fdf10cc3a46222dec3` |
| h/2 | P05_long_step | ap_half_width | exceeds | 0.6999999999993634 | 0.5599999999994907 | 0.14 | 0.05 | `r-a71c890435a70aeaf61b` | `r-50fdf10cc3a46222dec3` |
| h/2 | P05_long_step | first_isi | exceeds | 21.019999999980882 | 22.499999999979536 | 1.48 | 0.6 | `r-a71c890435a70aeaf61b` | `r-50fdf10cc3a46222dec3` |
| h/2 | P05_long_step | last_isi | exceeds | 77.97000000170192 | 58.69000000128108 | 19.28 | 1.5626 | `r-a71c890435a70aeaf61b` | `r-50fdf10cc3a46222dec3` |
| h/2 | P05_long_step | mean_frequency | exceeds | 14.734349834088421 | 19.051247856709896 | 4.3169 | 0.734705 | `r-a71c890435a70aeaf61b` | `r-50fdf10cc3a46222dec3` |
| h/2 | P05_long_step | spike_count | exceeds | 29.0 | 37.0 | 8 | 0.5 | `r-a71c890435a70aeaf61b` | `r-50fdf10cc3a46222dec3` |
| h/2 | P06_ramp | mean_frequency | exceeds | 30.358227079570092 | 32.00160008003719 | 1.64337 | 1.51445 | `r-2c42dd73d53f21fe7690` | `r-eeaf51f5f9146fab05d8` |
| h/2 | P06_ramp | spike_count | exceeds | 30.0 | 32.0 | 2 | 0.5 | `r-2c42dd73d53f21fe7690` | `r-eeaf51f5f9146fab05d8` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -1.3990133539835625 | -6.540256296792407 | 5.14124 | 0.5 | `r-fa41d650658e23c878d5` | `r-f006a6a76507b6b08959` |
| h/2 | P09_short_pulse | ap_half_width | exceeds | 0.8799999999991996 | 0.7099999999993543 | 0.17 | 0.05 | `r-fa41d650658e23c878d5` | `r-f006a6a76507b6b08959` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
