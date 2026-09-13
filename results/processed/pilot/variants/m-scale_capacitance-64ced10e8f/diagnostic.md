# m-scale_capacitance-64ced10e8f

- model: `pospischil2008_lts`
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "2.0 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 2.0, "generator_seed": 20260913}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LTS.cell.nml", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "2.0 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2074.366 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | 0.45003406360930803 | None |  | 0.0450034 | `r-7fe8302f56856b53d535` | `r-b171fb51a8667c455640` |
| h/1 | P00_canonical | ahp_depth | exceeds | 16.573501743312846 | 24.876966913222148 | 8.30347 | 0.828675 | `r-7fe8302f56856b53d535` | `r-b171fb51a8667c455640` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.01163101444587 | 83.57326126410013 | 16.4384 | 2.00023 | `r-7fe8302f56856b53d535` | `r-b171fb51a8667c455640` |
| h/1 | P00_canonical | firing_regime | categorical | adapting | tonic |  |  | `r-7fe8302f56856b53d535` | `r-b171fb51a8667c455640` |
| h/1 | P00_canonical | first_isi | exceeds | 14.159999999987122 | 97.06999999991177 | 82.91 | 0.6 | `r-7fe8302f56856b53d535` | `r-b171fb51a8667c455640` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 31.629999999752442 | 79.92999999970851 | 48.3 | 0.6326 | `r-7fe8302f56856b53d535` | `r-b171fb51a8667c455640` |
| h/1 | P00_canonical | last_isi | exceeds | 202.1999999998161 | 97.06999999991177 | 105.13 | 4.044 | `r-7fe8302f56856b53d535` | `r-b171fb51a8667c455640` |
| h/1 | P00_canonical | mean_frequency | exceeds | 12.319822594574143 | 11.299435028272828 | 1.02039 | 0.615991 | `r-7fe8302f56856b53d535` | `r-b171fb51a8667c455640` |
| h/1 | P00_canonical | spike_count | exceeds | 4.0 | 2.0 | 2 | 0.5 | `r-7fe8302f56856b53d535` | `r-b171fb51a8667c455640` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -74.93620969696036 | -75.8008119781497 | 0.864602 | 0.5 | `r-c8dafa7919f8741d136a` | `r-90b67c5f37aa91547909` |
| h/1 | P02_weak_step | voltage_deflection | exceeds | 9.017360991923098 | 8.164717112731651 | 0.852644 | 0.5 | `r-c8dafa7919f8741d136a` | `r-90b67c5f37aa91547909` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.038658561573663 | 0.09948090977392254 | 0.0608223 | 0.000773171 | `s-3999769ed965342ea63b` | `s-3fa6a5621e85f71780ae` |
| h/1 | P04_step_2x | ahp_depth | definedness | 14.597407663981116 | None |  | 1.3737 | `r-c8dafa7919f8741d136a` | `r-90b67c5f37aa91547909` |
| h/1 | P04_step_2x | ap_amplitude | definedness | 92.73429489294529 | None |  | 1.85469 | `r-c8dafa7919f8741d136a` | `r-90b67c5f37aa91547909` |
| h/1 | P04_step_2x | ap_half_width | definedness | 0.7299999999993361 | None |  | 0.05 | `r-c8dafa7919f8741d136a` | `r-90b67c5f37aa91547909` |
| h/1 | P04_step_2x | firing_regime | categorical | single_spike | silent |  |  | `r-c8dafa7919f8741d136a` | `r-90b67c5f37aa91547909` |
| h/1 | P04_step_2x | first_spike_latency | definedness | 57.54999999981982 | None |  | 1.151 | `r-c8dafa7919f8741d136a` | `r-90b67c5f37aa91547909` |
| h/1 | P04_step_2x | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-c8dafa7919f8741d136a` | `r-90b67c5f37aa91547909` |
| h/1 | P05_long_step | ahp_depth | definedness | 14.078013743082678 | None |  | 1.31907 | `r-0e47469602e57d8257f5` | `r-58458749b766f874b70e` |
| h/1 | P05_long_step | ap_amplitude | definedness | 91.18347931093976 | None |  | 1.82367 | `r-0e47469602e57d8257f5` | `r-58458749b766f874b70e` |
| h/1 | P05_long_step | ap_half_width | definedness | 0.7199999999993452 | None |  | 0.05 | `r-0e47469602e57d8257f5` | `r-58458749b766f874b70e` |
| h/1 | P05_long_step | firing_regime | categorical | single_spike | silent |  |  | `r-0e47469602e57d8257f5` | `r-58458749b766f874b70e` |
| h/1 | P05_long_step | first_spike_latency | definedness | 77.49999999980167 | None |  | 1.55 | `r-0e47469602e57d8257f5` | `r-58458749b766f874b70e` |
| h/1 | P05_long_step | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-0e47469602e57d8257f5` | `r-58458749b766f874b70e` |
| h/1 | P07_hyperpolarizing_step | minimum_voltage | exceeds | -98.23638916015535 | -97.12671661376686 | 1.10967 | 0.5 | `r-c8dafa7919f8741d136a` | `r-90b67c5f37aa91547909` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -98.20717309417724 | -96.96281153716977 | 1.24436 | 0.5 | `r-c8dafa7919f8741d136a` | `r-90b67c5f37aa91547909` |
| h/1 | P07_hyperpolarizing_step | voltage_deflection | exceeds | -14.253602405293776 | -12.997282446288423 | 1.25632 | 0.71268 | `r-c8dafa7919f8741d136a` | `r-90b67c5f37aa91547909` |
| h/1 | P08_rebound | maximum_voltage | exceeds | -85.8170776367331 | -90.3810806274649 | 4.564 | 1 | `r-63884195eb48b9d52a9c` | `r-34bd4948915015a5782f` |
| h/2 | P00_canonical | adaptation_index | definedness | 0.4630010462892806 | None |  | 0.0450034 | `r-055cc6b1739501cecd9d` | `r-382b654b661b58f6f766` |
| h/2 | P00_canonical | ahp_depth | exceeds | 16.673553569797534 | 24.947393814086922 | 8.27384 | 0.828675 | `r-055cc6b1739501cecd9d` | `r-382b654b661b58f6f766` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 99.9338417077712 | 83.54001999245551 | 16.3938 | 2.00023 | `r-055cc6b1739501cecd9d` | `r-382b654b661b58f6f766` |
| h/2 | P00_canonical | firing_regime | categorical | adapting | tonic |  |  | `r-055cc6b1739501cecd9d` | `r-382b654b661b58f6f766` |
| h/2 | P00_canonical | first_isi | exceeds | 13.959999999987303 | 95.72999999991299 | 81.77 | 0.6 | `r-055cc6b1739501cecd9d` | `r-382b654b661b58f6f766` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 31.61999999975245 | 79.91999999970852 | 48.3 | 0.6326 | `r-055cc6b1739501cecd9d` | `r-382b654b661b58f6f766` |
| h/2 | P00_canonical | last_isi | exceeds | 202.7499999998156 | 95.72999999991299 | 107.02 | 4.044 | `r-055cc6b1739501cecd9d` | `r-382b654b661b58f6f766` |
| h/2 | P00_canonical | mean_frequency | exceeds | 12.393493415976295 | 11.386279533187073 | 1.00721 | 0.615991 | `r-055cc6b1739501cecd9d` | `r-382b654b661b58f6f766` |
| h/2 | P00_canonical | spike_count | exceeds | 4.0 | 2.0 | 2 | 0.5 | `r-055cc6b1739501cecd9d` | `r-382b654b661b58f6f766` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -74.93623204345693 | -75.80080753326449 | 0.864575 | 0.5 | `r-13bd10976ea90e0f7248` | `r-0b9cf25f0cbdf5090b0f` |
| h/2 | P02_weak_step | voltage_deflection | exceeds | 9.01733864034027 | 8.164721529642406 | 0.852617 | 0.5 | `r-13bd10976ea90e0f7248` | `r-0b9cf25f0cbdf5090b0f` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.038658561573663 | 0.09948090977392254 | 0.0608223 | 0.000773171 | `s-372d4e42bc81ae6ab2b8` | `s-c6c558afafa6e9fd4d17` |
| h/2 | P04_step_2x | ahp_depth | definedness | 15.055308659871415 | None |  | 1.3737 | `r-13bd10976ea90e0f7248` | `r-0b9cf25f0cbdf5090b0f` |
| h/2 | P04_step_2x | ap_amplitude | definedness | 92.6621055623362 | None |  | 1.85469 | `r-13bd10976ea90e0f7248` | `r-0b9cf25f0cbdf5090b0f` |
| h/2 | P04_step_2x | ap_half_width | definedness | 0.7299999999993361 | None |  | 0.05 | `r-13bd10976ea90e0f7248` | `r-0b9cf25f0cbdf5090b0f` |
| h/2 | P04_step_2x | firing_regime | categorical | single_spike | silent |  |  | `r-13bd10976ea90e0f7248` | `r-0b9cf25f0cbdf5090b0f` |
| h/2 | P04_step_2x | first_spike_latency | definedness | 57.49999999981986 | None |  | 1.151 | `r-13bd10976ea90e0f7248` | `r-0b9cf25f0cbdf5090b0f` |
| h/2 | P04_step_2x | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-13bd10976ea90e0f7248` | `r-0b9cf25f0cbdf5090b0f` |
| h/2 | P05_long_step | ahp_depth | definedness | 14.517703374227494 | None |  | 1.31907 | `r-d6d2d7202a5745e9444f` | `r-0cc342e8da8dc7662908` |
| h/2 | P05_long_step | ap_amplitude | definedness | 91.13381576739826 | None |  | 1.82367 | `r-d6d2d7202a5745e9444f` | `r-0cc342e8da8dc7662908` |
| h/2 | P05_long_step | ap_half_width | definedness | 0.7299999999993361 | None |  | 0.05 | `r-d6d2d7202a5745e9444f` | `r-0cc342e8da8dc7662908` |
| h/2 | P05_long_step | firing_regime | categorical | single_spike | silent |  |  | `r-d6d2d7202a5745e9444f` | `r-0cc342e8da8dc7662908` |
| h/2 | P05_long_step | first_spike_latency | definedness | 77.43999999980173 | None |  | 1.55 | `r-d6d2d7202a5745e9444f` | `r-0cc342e8da8dc7662908` |
| h/2 | P05_long_step | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-d6d2d7202a5745e9444f` | `r-0cc342e8da8dc7662908` |
| h/2 | P07_hyperpolarizing_step | minimum_voltage | exceeds | -98.23638153076172 | -97.12670898437145 | 1.10967 | 0.5 | `r-13bd10976ea90e0f7248` | `r-0b9cf25f0cbdf5090b0f` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -98.20716658782956 | -96.96279629363963 | 1.24437 | 0.5 | `r-13bd10976ea90e0f7248` | `r-0b9cf25f0cbdf5090b0f` |
| h/2 | P07_hyperpolarizing_step | voltage_deflection | exceeds | -14.253595904032366 | -12.997267230732731 | 1.25633 | 0.71268 | `r-13bd10976ea90e0f7248` | `r-0b9cf25f0cbdf5090b0f` |
| h/2 | P08_rebound | maximum_voltage | exceeds | -85.81714630128519 | -90.3812026977748 | 4.56406 | 1 | `r-24306981c7a9f2760a5f` | `r-71871b02c814e2e253bf` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
