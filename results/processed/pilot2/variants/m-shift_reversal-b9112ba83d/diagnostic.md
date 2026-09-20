# m-shift_reversal-b9112ba83d

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='kChans']", "new": "-79mV", "old": "-77mV"}], "element": "channelDensity", "element_id": "kChans", "generator_seed": 20260917, "shift_mV": -2.0}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='kChans']", "attribute": "erev", "old": "-77mV", "new": "-79mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 596.921 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -10.343139648437372 | -11.686882019042883 | 1.34374 | 0.517157 | `r-5f0a94c66ff17cd98a0a` | `r-bc0264e43c7943f729fc` |
| h/1 | P00_canonical | last_isi | exceeds | 16.12999999998533 | 16.67999999998483 | 0.55 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-bc0264e43c7943f729fc` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-bc0264e43c7943f729fc` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -64.08310811767565 | -64.68765371093737 | 0.604546 | 0.5 | `r-66b1007575e04915ac55` | `r-6407e5d4409f9fd3f0a2` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.02547640188511714 | 0.00303941 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-c91c93aabacb03ea88f9` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -10.697937011716306 | -12.03691101074341 | 1.33897 | 0.534897 | `r-66b1007575e04915ac55` | `r-6407e5d4409f9fd3f0a2` |
| h/1 | P05_long_step | ahp_depth | exceeds | -10.81385040282855 | -12.149620056147 | 1.33577 | 0.540693 | `r-940eedfaa66e3fa96c16` | `r-fd0573406775a6144698` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -67.26261677551295 | -67.79650654602077 | 0.53389 | 0.5 | `r-66b1007575e04915ac55` | `r-6407e5d4409f9fd3f0a2` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -11.226577758789873 | -12.568519592285966 | 1.34194 | 0.561329 | `r-efc8f2fd727ba1854c5f` | `r-2272e886615a12f4a20d` |
| h/2 | P00_canonical | ahp_depth | exceeds | -10.327699567887592 | -11.669702436539978 | 1.342 | 0.517157 | `r-d4235ef154cdc2eeb44c` | `r-5be97d295230c4b6c29c` |
| h/2 | P00_canonical | last_isi | exceeds | 16.059999999985394 | 16.619999999984884 | 0.56 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-5be97d295230c4b6c29c` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-5be97d295230c4b6c29c` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -64.08310755462634 | -64.68765314788806 | 0.604546 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-ddfa94fbcc2a10bf0822` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02240284133597432 | 0.025442251212348884 | 0.00303941 | 0.00044874 | `s-b96e12fd1e882cb18a94` | `s-cee611c03587d7d55ed9` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -10.691650390625 | -12.029846191402171 | 1.3382 | 0.534897 | `r-8d6f46142acd4ec898a7` | `r-ddfa94fbcc2a10bf0822` |
| h/2 | P05_long_step | ahp_depth | exceeds | -10.808036804201677 | -12.143096923830583 | 1.33506 | 0.540693 | `r-a455ac42295a97429d02` | `r-3a11ec310f15ca13c8ec` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -67.26261789703395 | -67.79650766754176 | 0.53389 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-ddfa94fbcc2a10bf0822` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -11.22248840332071 | -12.56378936767618 | 1.3413 | 0.561329 | `r-2c9f7eaf5c4d0d4f33d4` | `r-cec304ce85a682f928d8` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
