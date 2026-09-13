# m-shift_reversal-2d2e2ab474

- model: `pospischil2008_rs`
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "new": "-105.0 mV", "old": "-100.0 mV"}], "element": "channelDensity", "element_id": "Kd_all", "generator_seed": 20260913, "shift_mV": -5.0}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "attribute": "erev", "old": "-100.0 mV", "new": "-105.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1645.4 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | 2.861194747922525 | 1.0964166132608995 | 1.76478 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-a255a0e68b4fe7838d16` |
| h/1 | P00_canonical | first_isi | exceeds | 28.06999999997447 | 28.649999999973943 | 0.58 | 0.5614 | `r-5171ec6a0414fa8c47f8` | `r-a255a0e68b4fe7838d16` |
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 127.61999999988399 | 8.36 | 2.7196 | `r-5171ec6a0414fa8c47f8` | `r-a255a0e68b4fe7838d16` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 3.2025415878387236 | 1.352504976912826 | 1.85004 | 1.22099 | `r-0c0f3a761516cf334965` | `r-e6c173037eedaf6c7652` |
| h/1 | P05_long_step | ahp_depth | exceeds | 2.4773294906594145 | 0.6490366541551253 | 1.82829 | 1.19998 | `r-6299bd8dadd5e9592d63` | `r-a52c5c581bac2b397085` |
| h/1 | P05_long_step | last_isi | exceeds | 78.13000000170541 | 75.95000000165783 | 2.18 | 1.5626 | `r-6299bd8dadd5e9592d63` | `r-a52c5c581bac2b397085` |
| h/1 | P05_long_step | spike_count | exceeds | 29.0 | 30.0 | 1 | 0.5 | `r-6299bd8dadd5e9592d63` | `r-a52c5c581bac2b397085` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -1.4308354873657265 | -2.1663091100055 | 0.735474 | 0.5 | `r-4a031cb8037cbebd46bc` | `r-597ad9f273a6212779f8` |
| h/2 | P00_canonical | ahp_depth | exceeds | 2.9394112752346615 | 1.181453826908836 | 1.75796 | 0.5 | `r-35d4f8d415fe0d06a895` | `r-226aee214471f6de555f` |
| h/2 | P00_canonical | first_isi | exceeds | 28.029999999974507 | 28.59999999997399 | 0.57 | 0.5614 | `r-35d4f8d415fe0d06a895` | `r-226aee214471f6de555f` |
| h/2 | P00_canonical | last_isi | exceeds | 135.78999999987656 | 127.41999999988417 | 8.37 | 2.7196 | `r-35d4f8d415fe0d06a895` | `r-226aee214471f6de555f` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 3.6095391972804407 | 1.7937890930239462 | 1.81575 | 1.22099 | `r-13ae588754662eb409bf` | `r-b453b3c86fd0e9f06e1f` |
| h/2 | P05_long_step | ahp_depth | exceeds | 2.8773233159343334 | 1.083431426999752 | 1.79389 | 1.19998 | `r-a71c890435a70aeaf61b` | `r-8da780549e5a3d6c602b` |
| h/2 | P05_long_step | last_isi | exceeds | 77.97000000170192 | 75.82000000165499 | 2.15 | 1.5626 | `r-a71c890435a70aeaf61b` | `r-8da780549e5a3d6c602b` |
| h/2 | P05_long_step | spike_count | exceeds | 29.0 | 30.0 | 1 | 0.5 | `r-a71c890435a70aeaf61b` | `r-8da780549e5a3d6c602b` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
