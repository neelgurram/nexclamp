# m-scale_capacitance-ca8d29abe3

- model: `pospischil2008_rs`
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "1.1 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 1.1, "generator_seed": 20260913}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "1.1 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1677.827 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | 2.861194747922525 | 4.057174591061013 | 1.19598 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-183a1e02fbb01dc92a07` |
| h/1 | P00_canonical | first_isi | exceeds | 28.06999999997447 | 30.129999999972597 | 2.06 | 0.5614 | `r-5171ec6a0414fa8c47f8` | `r-183a1e02fbb01dc92a07` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 20.749999999853287 | 22.78999999985143 | 2.04 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-183a1e02fbb01dc92a07` |
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 139.11999999987353 | 3.14 | 2.7196 | `r-5171ec6a0414fa8c47f8` | `r-183a1e02fbb01dc92a07` |
| h/1 | P00_canonical | mean_frequency | exceeds | 17.03113291098414 | 16.148827595137945 | 0.882305 | 0.851557 | `r-5171ec6a0414fa8c47f8` | `r-183a1e02fbb01dc92a07` |
| h/1 | P04_step_2x | first_isi | exceeds | 13.069999999988113 | 13.789999999987458 | 0.72 | 0.5 | `r-0c0f3a761516cf334965` | `r-5f9468e9fd7a983e9e7a` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 10.689999999862437 | 11.709999999861509 | 1.02 | 0.5 | `r-0c0f3a761516cf334965` | `r-5f9468e9fd7a983e9e7a` |
| h/1 | P04_step_2x | last_isi | exceeds | 28.16999999997438 | 29.449999999973215 | 1.28 | 0.5634 | `r-0c0f3a761516cf334965` | `r-5f9468e9fd7a983e9e7a` |
| h/1 | P04_step_2x | spike_count | exceeds | 22.0 | 21.0 | 1 | 0.5 | `r-0c0f3a761516cf334965` | `r-5f9468e9fd7a983e9e7a` |
| h/1 | P05_long_step | ahp_depth | exceeds | 2.4773294906594145 | 3.6797485682145066 | 1.20242 | 1.19998 | `r-6299bd8dadd5e9592d63` | `r-8a3760d27d9cf58ac3b4` |
| h/1 | P05_long_step | first_isi | exceeds | 21.2199999999807 | 22.619999999979427 | 1.4 | 0.6 | `r-6299bd8dadd5e9592d63` | `r-8a3760d27d9cf58ac3b4` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 16.619999999857043 | 18.23999999985557 | 1.62 | 0.5 | `r-6299bd8dadd5e9592d63` | `r-8a3760d27d9cf58ac3b4` |
| h/1 | P05_long_step | last_isi | exceeds | 78.13000000170541 | 79.95000000174514 | 1.82 | 1.5626 | `r-6299bd8dadd5e9592d63` | `r-8a3760d27d9cf58ac3b4` |
| h/1 | P05_long_step | spike_count | exceeds | 29.0 | 28.0 | 1 | 0.5 | `r-6299bd8dadd5e9592d63` | `r-8a3760d27d9cf58ac3b4` |
| h/1 | P06_ramp | spike_count | exceeds | 30.0 | 29.0 | 1 | 0.5 | `r-7054f91d1e6b5f4b29f8` | `r-672d9a72aa0c3f844c7a` |
| h/2 | P00_canonical | ahp_depth | exceeds | 2.9394112752346615 | 4.133804214479838 | 1.19439 | 0.5 | `r-35d4f8d415fe0d06a895` | `r-65e9bb6ba9ae9370af4b` |
| h/2 | P00_canonical | first_isi | exceeds | 28.029999999974507 | 30.05999999997266 | 2.03 | 0.5614 | `r-35d4f8d415fe0d06a895` | `r-65e9bb6ba9ae9370af4b` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 20.739999999853296 | 22.78999999985143 | 2.05 | 0.5 | `r-35d4f8d415fe0d06a895` | `r-65e9bb6ba9ae9370af4b` |
| h/2 | P00_canonical | last_isi | exceeds | 135.78999999987656 | 138.9199999998737 | 3.13 | 2.7196 | `r-35d4f8d415fe0d06a895` | `r-65e9bb6ba9ae9370af4b` |
| h/2 | P00_canonical | mean_frequency | exceeds | 17.059606264310375 | 16.176518166251302 | 0.883088 | 0.851557 | `r-35d4f8d415fe0d06a895` | `r-65e9bb6ba9ae9370af4b` |
| h/2 | P04_step_2x | first_isi | exceeds | 12.92999999998824 | 13.639999999987594 | 0.71 | 0.5 | `r-13ae588754662eb409bf` | `r-9f6ea343b1fcde7dffc0` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 10.659999999862464 | 11.679999999861536 | 1.02 | 0.5 | `r-13ae588754662eb409bf` | `r-9f6ea343b1fcde7dffc0` |
| h/2 | P04_step_2x | last_isi | exceeds | 28.06999999997447 | 29.329999999973325 | 1.26 | 0.5634 | `r-13ae588754662eb409bf` | `r-9f6ea343b1fcde7dffc0` |
| h/2 | P04_step_2x | spike_count | exceeds | 22.0 | 21.0 | 1 | 0.5 | `r-13ae588754662eb409bf` | `r-9f6ea343b1fcde7dffc0` |
| h/2 | P05_long_step | first_isi | exceeds | 21.019999999980882 | 22.399999999979627 | 1.38 | 0.6 | `r-a71c890435a70aeaf61b` | `r-e80c0d34d818a143dd28` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 16.58999999985707 | 18.199999999855606 | 1.61 | 0.5 | `r-a71c890435a70aeaf61b` | `r-e80c0d34d818a143dd28` |
| h/2 | P05_long_step | last_isi | exceeds | 77.97000000170192 | 79.78000000174143 | 1.81 | 1.5626 | `r-a71c890435a70aeaf61b` | `r-e80c0d34d818a143dd28` |
| h/2 | P05_long_step | spike_count | exceeds | 29.0 | 28.0 | 1 | 0.5 | `r-a71c890435a70aeaf61b` | `r-e80c0d34d818a143dd28` |
| h/2 | P06_ramp | spike_count | exceeds | 30.0 | 29.0 | 1 | 0.5 | `r-2c42dd73d53f21fe7690` | `r-0667919fd0b9055e2bfa` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
