# m-shift_initial_voltage-11bd93c6c3

- model: `pospischil2008_lts`
- kind/family/operator: mutant / biophysical / shift_initial_voltage
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/initMembPotential[1]", "new": "-89.0 mV", "old": "-84.0 mV"}], "element": "initMembPotential", "element_id": null, "generator_seed": 20260913, "shift_mV": -5.0}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LTS.cell.nml", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/initMembPotential[1]", "attribute": "value", "old": "-84.0 mV", "new": "-89.0 mV", "action": "set", "note": "shift_initial_voltage"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2121.144 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.45003406360930803 | 0.5217439910564562 | 0.0717099 | 0.0450034 | `r-7fe8302f56856b53d535` | `r-79de4763dc91bb514603` |
| h/1 | P00_canonical | first_isi | exceeds | 14.159999999987122 | 13.379999999987831 | 0.78 | 0.6 | `r-7fe8302f56856b53d535` | `r-79de4763dc91bb514603` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.038658561573663 | 0.036814425244177315 | 0.00184414 | 0.000773171 | `s-3999769ed965342ea63b` | `s-3282c53c29195c2bd4b5` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 77.49999999980167 | 75.50999999980348 | 1.99 | 1.55 | `r-0e47469602e57d8257f5` | `r-383bd9f87697d1445690` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.4630010462892806 | 0.5347076461769117 | 0.0717066 | 0.0450034 | `r-055cc6b1739501cecd9d` | `r-da7a2ae281f178b3b0b2` |
| h/2 | P00_canonical | first_isi | exceeds | 13.959999999987303 | 13.189999999988004 | 0.77 | 0.6 | `r-055cc6b1739501cecd9d` | `r-da7a2ae281f178b3b0b2` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.038658561573663 | 0.036814425244177315 | 0.00184414 | 0.000773171 | `s-372d4e42bc81ae6ab2b8` | `s-0ff33d80e00c05ba81f7` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 77.43999999980173 | 75.44999999980354 | 1.99 | 1.55 | `r-d6d2d7202a5745e9444f` | `r-b9ea5041c5dcc894b4f4` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
