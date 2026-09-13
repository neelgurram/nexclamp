# m-increase_dt-f3e1491a0a

- model: `pospischil2008_rs`
- kind/family/operator: mutant / numerical / increase_dt
- parameters: `{"changes": [{"attribute": "step", "locator": "/Lems[1]/Component[@id='sim1']", "new": "0.01ms", "old": "0.001ms"}], "factor": 10, "generator_seed": 20260913}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/LEMS_RS.xml", "locator": "/Lems[1]/Component[@id='sim1']", "attribute": "step", "old": "0.001ms", "new": "0.01ms", "action": "set", "note": "increase_dt"}]`
- execution overrides: `{"dt_factor": 10}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 221.962 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | 2.861194747922525 | 1.4173081970233028 | 1.44389 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-1c4820e6fbe31b3e8ad3` |
| h/1 | P00_canonical | first_isi | exceeds | 28.06999999997447 | 28.95999999997366 | 0.89 | 0.5614 | `r-5171ec6a0414fa8c47f8` | `r-1c4820e6fbe31b3e8ad3` |
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 139.4699999998732 | 3.49 | 2.7196 | `r-5171ec6a0414fa8c47f8` | `r-1c4820e6fbe31b3e8ad3` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 3.2025415878387236 | -4.973398513676926 | 8.17594 | 1.22099 | `r-0c0f3a761516cf334965` | `r-5c98fda7119a9e5d8d24` |
| h/1 | P04_step_2x | first_isi | exceeds | 13.069999999988113 | 15.599999999985812 | 2.53 | 0.5 | `r-0c0f3a761516cf334965` | `r-5c98fda7119a9e5d8d24` |
| h/1 | P04_step_2x | last_isi | exceeds | 28.16999999997438 | 29.799999999972897 | 1.63 | 0.5634 | `r-0c0f3a761516cf334965` | `r-5c98fda7119a9e5d8d24` |
| h/1 | P04_step_2x | mean_frequency | exceeds | 44.11292909854356 | 40.66693777963275 | 3.44599 | 2.20565 | `r-0c0f3a761516cf334965` | `r-5c98fda7119a9e5d8d24` |
| h/1 | P04_step_2x | spike_count | exceeds | 22.0 | 20.0 | 2 | 0.5 | `r-0c0f3a761516cf334965` | `r-5c98fda7119a9e5d8d24` |
| h/1 | P05_long_step | ahp_depth | exceeds | 2.4773294906594145 | -5.569795913587882 | 8.04713 | 1.19998 | `r-6299bd8dadd5e9592d63` | `r-5e81827f9cb79086ed5f` |
| h/1 | P05_long_step | first_isi | exceeds | 21.2199999999807 | 24.74999999997749 | 3.53 | 0.6 | `r-6299bd8dadd5e9592d63` | `r-5e81827f9cb79086ed5f` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 16.619999999857043 | 17.14999999985656 | 0.53 | 0.5 | `r-6299bd8dadd5e9592d63` | `r-5e81827f9cb79086ed5f` |
| h/1 | P05_long_step | last_isi | exceeds | 78.13000000170541 | 81.05000000176915 | 2.92 | 1.5626 | `r-6299bd8dadd5e9592d63` | `r-5e81827f9cb79086ed5f` |
| h/1 | P05_long_step | spike_count | exceeds | 29.0 | 28.0 | 1 | 0.5 | `r-6299bd8dadd5e9592d63` | `r-5e81827f9cb79086ed5f` |
| h/1 | P06_ramp | mean_frequency | exceeds | 30.288956646438177 | 27.3003033367321 | 2.98865 | 1.51445 | `r-7054f91d1e6b5f4b29f8` | `r-48ce36d358862272061d` |
| h/1 | P06_ramp | spike_count | exceeds | 30.0 | 27.0 | 3 | 0.5 | `r-7054f91d1e6b5f4b29f8` | `r-48ce36d358862272061d` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -1.4308354873657265 | -8.127977676367323 | 6.69714 | 0.5 | `r-4a031cb8037cbebd46bc` | `r-aacef9f28da2651f9a05` |
| h/2 | P00_canonical | ahp_depth | exceeds | 2.9394112752346615 | 2.227993247992643 | 0.711418 | 0.5 | `r-35d4f8d415fe0d06a895` | `r-92e170a20ed89555539b` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 3.6095391972804407 | -0.2445769332729668 | 3.85412 | 1.22099 | `r-13ae588754662eb409bf` | `r-74eb017f3984049d0bbb` |
| h/2 | P04_step_2x | first_isi | exceeds | 12.92999999998824 | 14.179999999987103 | 1.25 | 0.5 | `r-13ae588754662eb409bf` | `r-74eb017f3984049d0bbb` |
| h/2 | P04_step_2x | last_isi | exceeds | 28.06999999997447 | 28.919999999973697 | 0.85 | 0.5634 | `r-13ae588754662eb409bf` | `r-74eb017f3984049d0bbb` |
| h/2 | P04_step_2x | spike_count | exceeds | 22.0 | 21.0 | 1 | 0.5 | `r-13ae588754662eb409bf` | `r-74eb017f3984049d0bbb` |
| h/2 | P05_long_step | ahp_depth | exceeds | 2.8773233159343334 | -0.9139128707761586 | 3.79124 | 1.19998 | `r-a71c890435a70aeaf61b` | `r-9446f19db62560f2ca94` |
| h/2 | P05_long_step | first_isi | exceeds | 21.019999999980882 | 22.809999999979254 | 1.79 | 0.6 | `r-a71c890435a70aeaf61b` | `r-9446f19db62560f2ca94` |
| h/2 | P05_long_step | spike_count | exceeds | 29.0 | 28.0 | 1 | 0.5 | `r-a71c890435a70aeaf61b` | `r-9446f19db62560f2ca94` |
| h/2 | P06_ramp | spike_count | exceeds | 30.0 | 29.0 | 1 | 0.5 | `r-2c42dd73d53f21fe7690` | `r-94816cffe6c55b8185e1` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -1.3990133539835625 | -3.754849150085775 | 2.35584 | 0.5 | `r-fa41d650658e23c878d5` | `r-6bf7cfb235d3cfc4c4d0` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
