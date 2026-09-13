# m-scale_capacitance-ee6df9013d

- model: `pospischil2008_lts`
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "1.1 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 1.1, "generator_seed": 20260913}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LTS.cell.nml", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "1.1 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2198.606 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.45003406360930803 | 0.2919699248120299 | 0.158064 | 0.0450034 | `r-7fe8302f56856b53d535` | `r-47cbec881f7bf2046c5b` |
| h/1 | P00_canonical | ahp_depth | exceeds | 16.573501743312846 | 17.89243180084229 | 1.31893 | 0.828675 | `r-7fe8302f56856b53d535` | `r-47cbec881f7bf2046c5b` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.01163101444587 | 95.65667343415481 | 4.35496 | 2.00023 | `r-7fe8302f56856b53d535` | `r-47cbec881f7bf2046c5b` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 31.629999999752442 | 35.32999999974908 | 3.7 | 0.6326 | `r-7fe8302f56856b53d535` | `r-47cbec881f7bf2046c5b` |
| h/1 | P00_canonical | last_isi | exceeds | 202.1999999998161 | 214.78999999980465 | 12.59 | 4.044 | `r-7fe8302f56856b53d535` | `r-47cbec881f7bf2046c5b` |
| h/1 | P00_canonical | mean_frequency | exceeds | 12.319822594574143 | 10.457789746152645 | 1.86203 | 0.615991 | `r-7fe8302f56856b53d535` | `r-47cbec881f7bf2046c5b` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.038658561573663 | 0.044464175944266104 | 0.00580561 | 0.000773171 | `s-3999769ed965342ea63b` | `s-88cddb253166273d168a` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 57.54999999981982 | 65.43999999981264 | 7.89 | 1.151 | `r-c8dafa7919f8741d136a` | `r-0fbf45f3f1950dd442a5` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 77.49999999980167 | 90.28999999979004 | 12.79 | 1.55 | `r-0e47469602e57d8257f5` | `r-9902933a814d1dc2806f` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.4630010462892806 | 0.3018406020491429 | 0.16116 | 0.0450034 | `r-055cc6b1739501cecd9d` | `r-6a518ae304ec0dced1c5` |
| h/2 | P00_canonical | ahp_depth | exceeds | 16.673553569797534 | 17.991140846248612 | 1.31759 | 0.828675 | `r-055cc6b1739501cecd9d` | `r-6a518ae304ec0dced1c5` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 99.9338417077712 | 95.67374801909088 | 4.26009 | 2.00023 | `r-055cc6b1739501cecd9d` | `r-6a518ae304ec0dced1c5` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 31.61999999975245 | 35.319999999749086 | 3.7 | 0.6326 | `r-055cc6b1739501cecd9d` | `r-6a518ae304ec0dced1c5` |
| h/2 | P00_canonical | last_isi | exceeds | 202.7499999998156 | 215.36999999980412 | 12.62 | 4.044 | `r-055cc6b1739501cecd9d` | `r-6a518ae304ec0dced1c5` |
| h/2 | P00_canonical | mean_frequency | exceeds | 12.393493415976295 | 10.50861706600971 | 1.88488 | 0.615991 | `r-055cc6b1739501cecd9d` | `r-6a518ae304ec0dced1c5` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.038658561573663 | 0.044464175944266104 | 0.00580561 | 0.000773171 | `s-372d4e42bc81ae6ab2b8` | `s-ca34d001b29cb6e43901` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 92.6621055623362 | 90.80507278567697 | 1.85703 | 1.85469 | `r-13bd10976ea90e0f7248` | `r-9ccd20d327cdebecefdb` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 57.49999999981986 | 65.3799999998127 | 7.88 | 1.151 | `r-13bd10976ea90e0f7248` | `r-9ccd20d327cdebecefdb` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 77.43999999980173 | 90.2199999997901 | 12.78 | 1.55 | `r-d6d2d7202a5745e9444f` | `r-2b82d6ed770be0213d1f` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
