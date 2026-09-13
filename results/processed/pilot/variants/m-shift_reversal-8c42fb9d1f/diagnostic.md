# m-shift_reversal-8c42fb9d1f

- model: `pospischil2008_rs`
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all']", "new": "-95.0 mV", "old": "-100.0 mV"}], "element": "channelDensity", "element_id": "IM_all", "generator_seed": 20260913, "shift_mV": 5.0}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all']", "attribute": "erev", "old": "-100.0 mV", "new": "-95.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1665.731 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.2988218828985024 | 0.1958150759218347 | 0.103007 | 0.0298822 | `r-5171ec6a0414fa8c47f8` | `r-45fcdf2e68e6863c652f` |
| h/1 | P00_canonical | first_isi | exceeds | 28.06999999997447 | 26.84999999997558 | 1.22 | 0.5614 | `r-5171ec6a0414fa8c47f8` | `r-45fcdf2e68e6863c652f` |
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 115.83999999989464 | 20.14 | 2.7196 | `r-5171ec6a0414fa8c47f8` | `r-45fcdf2e68e6863c652f` |
| h/1 | P00_canonical | mean_frequency | exceeds | 17.03113291098414 | 18.055430170647178 | 1.0243 | 0.851557 | `r-5171ec6a0414fa8c47f8` | `r-45fcdf2e68e6863c652f` |
| h/1 | P00_canonical | spike_count | exceeds | 5.0 | 6.0 | 1 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-45fcdf2e68e6863c652f` |
| h/1 | P04_step_2x | last_isi | exceeds | 28.16999999997438 | 25.039999999977226 | 3.13 | 0.5634 | `r-0c0f3a761516cf334965` | `r-5e578bef69dbace28f56` |
| h/1 | P04_step_2x | mean_frequency | exceeds | 44.11292909854356 | 48.408823034237884 | 4.29589 | 2.20565 | `r-0c0f3a761516cf334965` | `r-5e578bef69dbace28f56` |
| h/1 | P04_step_2x | spike_count | exceeds | 22.0 | 23.0 | 1 | 0.5 | `r-0c0f3a761516cf334965` | `r-5e578bef69dbace28f56` |
| h/1 | P05_long_step | last_isi | exceeds | 78.13000000170541 | 64.63000000141074 | 13.5 | 1.5626 | `r-6299bd8dadd5e9592d63` | `r-1372350a9302ee1e3835` |
| h/1 | P05_long_step | mean_frequency | exceeds | 14.694109182274286 | 17.43464571771925 | 2.74054 | 0.734705 | `r-6299bd8dadd5e9592d63` | `r-1372350a9302ee1e3835` |
| h/1 | P05_long_step | spike_count | exceeds | 29.0 | 34.0 | 5 | 0.5 | `r-6299bd8dadd5e9592d63` | `r-1372350a9302ee1e3835` |
| h/1 | P06_ramp | mean_frequency | exceeds | 30.288956646438177 | 32.3706438723719 | 2.08169 | 1.51445 | `r-7054f91d1e6b5f4b29f8` | `r-ff5a33b9a6c3a2f9a67e` |
| h/1 | P06_ramp | spike_count | exceeds | 30.0 | 32.0 | 2 | 0.5 | `r-7054f91d1e6b5f4b29f8` | `r-ff5a33b9a6c3a2f9a67e` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.2989579287624928 | 0.19599711253105992 | 0.102961 | 0.0298822 | `r-35d4f8d415fe0d06a895` | `r-b111fa058bc93c767ff1` |
| h/2 | P00_canonical | first_isi | exceeds | 28.029999999974507 | 26.809999999975616 | 1.22 | 0.5614 | `r-35d4f8d415fe0d06a895` | `r-b111fa058bc93c767ff1` |
| h/2 | P00_canonical | last_isi | exceeds | 135.78999999987656 | 115.73999999989474 | 20.05 | 2.7196 | `r-35d4f8d415fe0d06a895` | `r-b111fa058bc93c767ff1` |
| h/2 | P00_canonical | mean_frequency | exceeds | 17.059606264310375 | 18.08100289298387 | 1.0214 | 0.851557 | `r-35d4f8d415fe0d06a895` | `r-b111fa058bc93c767ff1` |
| h/2 | P00_canonical | spike_count | exceeds | 5.0 | 6.0 | 1 | 0.5 | `r-35d4f8d415fe0d06a895` | `r-b111fa058bc93c767ff1` |
| h/2 | P04_step_2x | last_isi | exceeds | 28.06999999997447 | 24.9599999999773 | 3.11 | 0.5634 | `r-13ae588754662eb409bf` | `r-e7185d7886217209d533` |
| h/2 | P04_step_2x | mean_frequency | exceeds | 44.38974193423394 | 48.30237285412281 | 3.91263 | 2.20565 | `r-13ae588754662eb409bf` | `r-e7185d7886217209d533` |
| h/2 | P04_step_2x | spike_count | exceeds | 22.0 | 24.0 | 2 | 0.5 | `r-13ae588754662eb409bf` | `r-e7185d7886217209d533` |
| h/2 | P05_long_step | last_isi | exceeds | 77.97000000170192 | 64.5000000014079 | 13.47 | 1.5626 | `r-a71c890435a70aeaf61b` | `r-89dd767ea5af83bb40a0` |
| h/2 | P05_long_step | mean_frequency | exceeds | 14.734349834088421 | 17.483056861048237 | 2.74871 | 0.734705 | `r-a71c890435a70aeaf61b` | `r-89dd767ea5af83bb40a0` |
| h/2 | P05_long_step | spike_count | exceeds | 29.0 | 34.0 | 5 | 0.5 | `r-a71c890435a70aeaf61b` | `r-89dd767ea5af83bb40a0` |
| h/2 | P06_ramp | mean_frequency | exceeds | 30.358227079570092 | 33.07939053732382 | 2.72116 | 1.51445 | `r-2c42dd73d53f21fe7690` | `r-d020f3fc97949ace1566` |
| h/2 | P06_ramp | spike_count | exceeds | 30.0 | 33.0 | 3 | 0.5 | `r-2c42dd73d53f21fe7690` | `r-d020f3fc97949ace1566` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
