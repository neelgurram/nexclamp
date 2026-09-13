# m-increase_dt-b7cdfa6b5c

- model: `pospischil2008_rs`
- kind/family/operator: mutant / numerical / increase_dt
- parameters: `{"changes": [{"attribute": "step", "locator": "/Lems[1]/Component[@id='sim1']", "new": "0.004ms", "old": "0.001ms"}], "factor": 4, "generator_seed": 20260913}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/LEMS_RS.xml", "locator": "/Lems[1]/Component[@id='sim1']", "attribute": "step", "old": "0.001ms", "new": "0.004ms", "action": "set", "note": "increase_dt"}]`
- execution overrides: `{"dt_factor": 4}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 467.741 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P04_step_2x | ahp_depth | exceeds | 3.2025415878387236 | 0.6488381869395425 | 2.5537 | 1.22099 | `r-0c0f3a761516cf334965` | `r-605ee5761cd35be1936f` |
| h/1 | P04_step_2x | first_isi | exceeds | 13.069999999988113 | 13.91999999998734 | 0.85 | 0.5 | `r-0c0f3a761516cf334965` | `r-605ee5761cd35be1936f` |
| h/1 | P04_step_2x | spike_count | exceeds | 22.0 | 21.0 | 1 | 0.5 | `r-0c0f3a761516cf334965` | `r-605ee5761cd35be1936f` |
| h/1 | P05_long_step | ahp_depth | exceeds | 2.4773294906594145 | -0.03440255861407593 | 2.51173 | 1.19998 | `r-6299bd8dadd5e9592d63` | `r-c20358157b324799821e` |
| h/1 | P05_long_step | first_isi | exceeds | 21.2199999999807 | 22.41999999997961 | 1.2 | 0.6 | `r-6299bd8dadd5e9592d63` | `r-c20358157b324799821e` |
| h/1 | P05_long_step | spike_count | exceeds | 29.0 | 28.0 | 1 | 0.5 | `r-6299bd8dadd5e9592d63` | `r-c20358157b324799821e` |
| h/1 | P06_ramp | spike_count | exceeds | 30.0 | 29.0 | 1 | 0.5 | `r-7054f91d1e6b5f4b29f8` | `r-45c205d76e09d28f04f5` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -1.4308354873657265 | -2.928793229418318 | 1.49796 | 0.5 | `r-4a031cb8037cbebd46bc` | `r-b3fc83e42bd3fe8c4296` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | 119.13114547927412 | None |  | 2.38262 | `r-4a031cb8037cbebd46bc` | `r-b3fc83e42bd3fe8c4296` |
| h/1 | P09_short_pulse | ap_half_width | definedness | 0.8799999999991996 | None |  | 0.05 | `r-4a031cb8037cbebd46bc` | `r-b3fc83e42bd3fe8c4296` |
| h/1 | P10_paired_pulses | ap_amplitude | definedness | 119.13114547927412 | None |  | 2.38262 | `r-4a031cb8037cbebd46bc` | `r-b3fc83e42bd3fe8c4296` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 3.6095391972804407 | 2.3726109263133566 | 1.23693 | 1.22099 | `r-13ae588754662eb409bf` | `r-17ce2b6d2b90076cf023` |
| h/2 | P04_step_2x | spike_count | exceeds | 22.0 | 21.0 | 1 | 0.5 | `r-13ae588754662eb409bf` | `r-17ce2b6d2b90076cf023` |
| h/2 | P05_long_step | ahp_depth | exceeds | 2.8773233159343334 | 1.6613867390951782 | 1.21594 | 1.19998 | `r-a71c890435a70aeaf61b` | `r-07f5989b6d2f1bfe2c76` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
