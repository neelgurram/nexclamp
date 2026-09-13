# m-wrong_channel-091a20b452

- model: `pospischil2008_lts`
- kind/family/operator: mutant / reference / wrong_channel
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "new": "Kd", "old": "LeakConductance"}], "element_id": "LeakConductance_all", "generator_seed": 20260913, "new_species": "k", "old_species": "non_specific"}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LTS.cell.nml", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "attribute": "ionChannel", "old": "LeakConductance", "new": "Kd", "action": "set", "note": "wrong_channel"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1665.31 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.45003406360930803 | 0.03809091058698056 | 0.411943 | 0.0450034 | `r-7fe8302f56856b53d535` | `r-adde62f41c398f7d80a4` |
| h/1 | P00_canonical | ahp_depth | exceeds | 16.573501743312846 | 3.359445470829641 | 13.2141 | 0.828675 | `r-7fe8302f56856b53d535` | `r-adde62f41c398f7d80a4` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.01163101444587 | 90.023464205251 | 9.98817 | 2.00023 | `r-7fe8302f56856b53d535` | `r-adde62f41c398f7d80a4` |
| h/1 | P00_canonical | ap_half_width | exceeds | 0.7799999999992906 | 0.7099999999993543 | 0.07 | 0.05 | `r-7fe8302f56856b53d535` | `r-adde62f41c398f7d80a4` |
| h/1 | P00_canonical | baseline_voltage | exceeds | -83.95132461929322 | -72.40068234827105 | 11.5506 | 0.5 | `r-7fe8302f56856b53d535` | `r-adde62f41c398f7d80a4` |
| h/1 | P00_canonical | firing_regime | categorical | adapting | tonic |  |  | `r-7fe8302f56856b53d535` | `r-adde62f41c398f7d80a4` |
| h/1 | P00_canonical | first_isi | exceeds | 14.159999999987122 | 40.68999999996299 | 26.53 | 0.6 | `r-7fe8302f56856b53d535` | `r-adde62f41c398f7d80a4` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 31.629999999752442 | 21.849999999761337 | 9.78 | 0.6326 | `r-7fe8302f56856b53d535` | `r-adde62f41c398f7d80a4` |
| h/1 | P00_canonical | last_isi | exceeds | 202.1999999998161 | 71.55999999993492 | 130.64 | 4.044 | `r-7fe8302f56856b53d535` | `r-adde62f41c398f7d80a4` |
| h/1 | P00_canonical | mean_frequency | exceeds | 12.319822594574143 | 18.355841090888635 | 6.03602 | 0.615991 | `r-7fe8302f56856b53d535` | `r-adde62f41c398f7d80a4` |
| h/1 | P00_canonical | spike_count | exceeds | 4.0 | 7.0 | 3 | 0.5 | `r-7fe8302f56856b53d535` | `r-adde62f41c398f7d80a4` |
| h/1 | P01_baseline | baseline_voltage | exceeds | -83.95357068888346 | -78.14327456410878 | 5.8103 | 0.5 | `r-c8dafa7919f8741d136a` | `r-ceb8b9cd39b82fb46b15` |
| h/1 | P01_baseline | steady_state_voltage | exceeds | -83.95030975341797 | -63.65543526622182 | 20.2949 | 0.5 | `r-c8dafa7919f8741d136a` | `r-ceb8b9cd39b82fb46b15` |
| h/1 | P02_weak_step | baseline_voltage | exceeds | -83.95357068888346 | -78.14327456410878 | 5.8103 | 0.5 | `r-c8dafa7919f8741d136a` | `r-ceb8b9cd39b82fb46b15` |
| h/1 | P02_weak_step | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-c8dafa7919f8741d136a` | `r-ceb8b9cd39b82fb46b15` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -74.93620969696036 | -56.916664794921864 | 18.0195 | 0.5 | `r-c8dafa7919f8741d136a` | `r-ceb8b9cd39b82fb46b15` |
| h/1 | P02_weak_step | voltage_deflection | exceeds | 9.017360991923098 | 21.226609769186915 | 12.2092 | 0.5 | `r-c8dafa7919f8741d136a` | `r-ceb8b9cd39b82fb46b15` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.038658561573663 | 0.006693531862577692 | 0.031965 | 0.000773171 | `s-3999769ed965342ea63b` | `s-2b717f9f08330c8b10ba` |
| h/1 | P04_step_2x | adaptation_index | definedness | None | 0.05423745783054194 |  | inf | `r-c8dafa7919f8741d136a` | `r-ceb8b9cd39b82fb46b15` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 14.597407663981116 | 8.515993375143935 | 6.08141 | 1.3737 | `r-c8dafa7919f8741d136a` | `r-ceb8b9cd39b82fb46b15` |
| h/1 | P04_step_2x | burst_count | definedness | None | 1.0 |  | inf | `r-c8dafa7919f8741d136a` | `r-ceb8b9cd39b82fb46b15` |
| h/1 | P04_step_2x | firing_regime | categorical | single_spike | tonic |  |  | `r-c8dafa7919f8741d136a` | `r-ceb8b9cd39b82fb46b15` |
| h/1 | P04_step_2x | first_isi | definedness | None | 56.169999999948914 |  | inf | `r-c8dafa7919f8741d136a` | `r-ceb8b9cd39b82fb46b15` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 57.54999999981982 | 34.11999999984113 | 23.43 | 1.151 | `r-c8dafa7919f8741d136a` | `r-ceb8b9cd39b82fb46b15` |
| h/1 | P04_step_2x | last_isi | definedness | None | 146.0199999998672 |  | inf | `r-c8dafa7919f8741d136a` | `r-ceb8b9cd39b82fb46b15` |
| h/1 | P04_step_2x | mean_frequency | definedness | None | 10.169215750093246 |  | inf | `r-c8dafa7919f8741d136a` | `r-ceb8b9cd39b82fb46b15` |
| h/1 | P04_step_2x | spike_count | exceeds | 1.0 | 5.0 | 4 | 0.5 | `r-c8dafa7919f8741d136a` | `r-ceb8b9cd39b82fb46b15` |
| h/1 | P05_long_step | adaptation_index | definedness | None | 0.009823969630080979 |  | inf | `r-0e47469602e57d8257f5` | `r-0374aae4d776d82d30fb` |
| h/1 | P05_long_step | ahp_depth | exceeds | 14.078013743082678 | 8.301683682761123 | 5.77633 | 1.31907 | `r-0e47469602e57d8257f5` | `r-0374aae4d776d82d30fb` |
| h/1 | P05_long_step | burst_count | definedness | None | 1.0 |  | inf | `r-0e47469602e57d8257f5` | `r-0374aae4d776d82d30fb` |
| h/1 | P05_long_step | firing_regime | categorical | single_spike | tonic |  |  | `r-0e47469602e57d8257f5` | `r-0374aae4d776d82d30fb` |
| h/1 | P05_long_step | first_isi | definedness | None | 93.50999999991495 |  | inf | `r-0e47469602e57d8257f5` | `r-0374aae4d776d82d30fb` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 77.49999999980167 | 40.9699999998349 | 36.53 | 1.55 | `r-0e47469602e57d8257f5` | `r-0374aae4d776d82d30fb` |
| h/1 | P05_long_step | last_isi | definedness | None | 204.54000000413066 |  | inf | `r-0e47469602e57d8257f5` | `r-0374aae4d776d82d30fb` |
| h/1 | P05_long_step | mean_frequency | definedness | None | 5.676393941732449 |  | inf | `r-0e47469602e57d8257f5` | `r-0374aae4d776d82d30fb` |
| h/1 | P05_long_step | spike_count | exceeds | 1.0 | 11.0 | 10 | 0.5 | `r-0e47469602e57d8257f5` | `r-0374aae4d776d82d30fb` |
| h/1 | P06_ramp | firing_regime | categorical | silent | tonic |  |  | `r-c024e83a8b15d13b8e57` | `r-0ad870cd34ca56427b51` |
| h/1 | P06_ramp | first_spike_latency | definedness | None | 179.1899999997092 |  | inf | `r-c024e83a8b15d13b8e57` | `r-0ad870cd34ca56427b51` |
| h/1 | P06_ramp | mean_frequency | definedness | None | 6.487328085812523 |  | inf | `r-c024e83a8b15d13b8e57` | `r-0ad870cd34ca56427b51` |
| h/1 | P06_ramp | spike_count | exceeds | 0.0 | 6.0 | 6 | 0.5 | `r-c024e83a8b15d13b8e57` | `r-0ad870cd34ca56427b51` |
| h/1 | P07_hyperpolarizing_step | baseline_voltage | exceeds | -83.95357068888346 | -78.14327456410878 | 5.8103 | 0.5 | `r-c8dafa7919f8741d136a` | `r-ceb8b9cd39b82fb46b15` |
| h/1 | P07_hyperpolarizing_step | minimum_voltage | exceeds | -98.23638916015535 | -143.25192260742188 | 45.0155 | 0.5 | `r-c8dafa7919f8741d136a` | `r-ceb8b9cd39b82fb46b15` |
| h/1 | P07_hyperpolarizing_step | sag_ratio | exceeds | 0.002045539263618266 | 0.05123578516186008 | 0.0491902 | 0.02 | `r-c8dafa7919f8741d136a` | `r-ceb8b9cd39b82fb46b15` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -98.20717309417724 | -139.91602990409552 | 41.7089 | 0.5 | `r-c8dafa7919f8741d136a` | `r-ceb8b9cd39b82fb46b15` |
| h/1 | P07_hyperpolarizing_step | voltage_deflection | exceeds | -14.253602405293776 | -61.772755339986745 | 47.5192 | 0.71268 | `r-c8dafa7919f8741d136a` | `r-ceb8b9cd39b82fb46b15` |
| h/1 | P08_rebound | maximum_voltage | exceeds | -85.8170776367331 | -210.58029174804688 | 124.763 | 1 | `r-63884195eb48b9d52a9c` | `r-d2acf79d400a73dd8fb2` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | None | 90.08529281759718 |  | inf | `r-f1b536f2cdb580580ef6` | `r-2f5feca7ecfbb9ac00df` |
| h/1 | P09_short_pulse | ap_half_width | definedness | None | 0.7099999999993543 |  | inf | `r-f1b536f2cdb580580ef6` | `r-2f5feca7ecfbb9ac00df` |
| h/1 | P09_short_pulse | first_spike_latency | definedness | None | 48.93999999982765 |  | inf | `r-f1b536f2cdb580580ef6` | `r-2f5feca7ecfbb9ac00df` |
| h/1 | P09_short_pulse | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-f1b536f2cdb580580ef6` | `r-2f5feca7ecfbb9ac00df` |
| h/1 | P10_paired_pulses | ap_amplitude | definedness | None | 90.88811111631213 |  | inf | `r-f1b536f2cdb580580ef6` | `r-2f5feca7ecfbb9ac00df` |
| h/1 | P10_paired_pulses | first_spike_latency | definedness | None | 34.06999999984117 |  | inf | `r-f1b536f2cdb580580ef6` | `r-2f5feca7ecfbb9ac00df` |
| h/1 | P10_paired_pulses | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-f1b536f2cdb580580ef6` | `r-2f5feca7ecfbb9ac00df` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.4630010462892806 | 0.0383227041962291 | 0.424678 | 0.0450034 | `r-055cc6b1739501cecd9d` | `r-0ca91424d18b89561bbb` |
| h/2 | P00_canonical | ahp_depth | exceeds | 16.673553569797534 | 3.4434899444777045 | 13.2301 | 0.828675 | `r-055cc6b1739501cecd9d` | `r-0ca91424d18b89561bbb` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 99.9338417077712 | 89.94649505835484 | 9.98735 | 2.00023 | `r-055cc6b1739501cecd9d` | `r-0ca91424d18b89561bbb` |
| h/2 | P00_canonical | ap_half_width | exceeds | 0.7799999999992906 | 0.7099999999993543 | 0.07 | 0.05 | `r-055cc6b1739501cecd9d` | `r-0ca91424d18b89561bbb` |
| h/2 | P00_canonical | baseline_voltage | exceeds | -83.95132456588748 | -72.40036097719255 | 11.551 | 0.5 | `r-055cc6b1739501cecd9d` | `r-0ca91424d18b89561bbb` |
| h/2 | P00_canonical | firing_regime | categorical | adapting | tonic |  |  | `r-055cc6b1739501cecd9d` | `r-0ca91424d18b89561bbb` |
| h/2 | P00_canonical | first_isi | exceeds | 13.959999999987303 | 40.53999999996313 | 26.58 | 0.6 | `r-055cc6b1739501cecd9d` | `r-0ca91424d18b89561bbb` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 31.61999999975245 | 21.839999999761346 | 9.78 | 0.6326 | `r-055cc6b1739501cecd9d` | `r-0ca91424d18b89561bbb` |
| h/2 | P00_canonical | last_isi | exceeds | 202.7499999998156 | 71.52999999993494 | 131.22 | 4.044 | `r-055cc6b1739501cecd9d` | `r-0ca91424d18b89561bbb` |
| h/2 | P00_canonical | mean_frequency | exceeds | 12.393493415976295 | 18.381870224023494 | 5.98838 | 0.615991 | `r-055cc6b1739501cecd9d` | `r-0ca91424d18b89561bbb` |
| h/2 | P00_canonical | spike_count | exceeds | 4.0 | 7.0 | 3 | 0.5 | `r-055cc6b1739501cecd9d` | `r-0ca91424d18b89561bbb` |
| h/2 | P01_baseline | baseline_voltage | exceeds | -83.9535706837972 | -78.14287766011698 | 5.81069 | 0.5 | `r-13bd10976ea90e0f7248` | `r-fa57f476719ea1c45037` |
| h/2 | P01_baseline | steady_state_voltage | exceeds | -83.95030975341797 | -63.65549406814528 | 20.2948 | 0.5 | `r-13bd10976ea90e0f7248` | `r-fa57f476719ea1c45037` |
| h/2 | P02_weak_step | baseline_voltage | exceeds | -83.9535706837972 | -78.14287766011698 | 5.81069 | 0.5 | `r-13bd10976ea90e0f7248` | `r-fa57f476719ea1c45037` |
| h/2 | P02_weak_step | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-13bd10976ea90e0f7248` | `r-fa57f476719ea1c45037` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -74.93623204345693 | -56.98907160186768 | 17.9472 | 0.5 | `r-13bd10976ea90e0f7248` | `r-fa57f476719ea1c45037` |
| h/2 | P02_weak_step | voltage_deflection | exceeds | 9.01733864034027 | 21.1538060582493 | 12.1365 | 0.5 | `r-13bd10976ea90e0f7248` | `r-fa57f476719ea1c45037` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.038658561573663 | 0.006693531862577692 | 0.031965 | 0.000773171 | `s-372d4e42bc81ae6ab2b8` | `s-3b501b5efe8ce4e71dfc` |
| h/2 | P04_step_2x | adaptation_index | definedness | None | 0.056279138137183146 |  | inf | `r-13bd10976ea90e0f7248` | `r-fa57f476719ea1c45037` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 15.055308659871415 | 8.957727513632605 | 6.09758 | 1.3737 | `r-13bd10976ea90e0f7248` | `r-fa57f476719ea1c45037` |
| h/2 | P04_step_2x | burst_count | definedness | None | 1.0 |  | inf | `r-13bd10976ea90e0f7248` | `r-fa57f476719ea1c45037` |
| h/2 | P04_step_2x | firing_regime | categorical | single_spike | tonic |  |  | `r-13bd10976ea90e0f7248` | `r-fa57f476719ea1c45037` |
| h/2 | P04_step_2x | first_isi | definedness | None | 53.55999999995129 |  | inf | `r-13bd10976ea90e0f7248` | `r-fa57f476719ea1c45037` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 57.49999999981986 | 34.06999999984117 | 23.43 | 1.151 | `r-13bd10976ea90e0f7248` | `r-fa57f476719ea1c45037` |
| h/2 | P04_step_2x | last_isi | definedness | None | 146.70999999986657 |  | inf | `r-13bd10976ea90e0f7248` | `r-fa57f476719ea1c45037` |
| h/2 | P04_step_2x | mean_frequency | definedness | None | 10.210749877482952 |  | inf | `r-13bd10976ea90e0f7248` | `r-fa57f476719ea1c45037` |
| h/2 | P04_step_2x | spike_count | exceeds | 1.0 | 5.0 | 4 | 0.5 | `r-13bd10976ea90e0f7248` | `r-fa57f476719ea1c45037` |
| h/2 | P05_long_step | adaptation_index | definedness | None | 0.010107975135221093 |  | inf | `r-d6d2d7202a5745e9444f` | `r-6a15ec307086ad6c6da3` |
| h/2 | P05_long_step | ahp_depth | exceeds | 14.517703374227494 | 8.738237462364097 | 5.77947 | 1.31907 | `r-d6d2d7202a5745e9444f` | `r-6a15ec307086ad6c6da3` |
| h/2 | P05_long_step | burst_count | definedness | None | 1.0 |  | inf | `r-d6d2d7202a5745e9444f` | `r-6a15ec307086ad6c6da3` |
| h/2 | P05_long_step | firing_regime | categorical | single_spike | tonic |  |  | `r-d6d2d7202a5745e9444f` | `r-6a15ec307086ad6c6da3` |
| h/2 | P05_long_step | first_isi | definedness | None | 90.46999999991772 |  | inf | `r-d6d2d7202a5745e9444f` | `r-6a15ec307086ad6c6da3` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 77.43999999980173 | 40.91999999983494 | 36.52 | 1.55 | `r-d6d2d7202a5745e9444f` | `r-6a15ec307086ad6c6da3` |
| h/2 | P05_long_step | last_isi | definedness | None | 206.11000000435456 |  | inf | `r-d6d2d7202a5745e9444f` | `r-6a15ec307086ad6c6da3` |
| h/2 | P05_long_step | mean_frequency | definedness | None | 5.647513040613358 |  | inf | `r-d6d2d7202a5745e9444f` | `r-6a15ec307086ad6c6da3` |
| h/2 | P05_long_step | spike_count | exceeds | 1.0 | 11.0 | 10 | 0.5 | `r-d6d2d7202a5745e9444f` | `r-6a15ec307086ad6c6da3` |
| h/2 | P06_ramp | firing_regime | categorical | silent | tonic |  |  | `r-9fb3d7dd0f85829f88b3` | `r-43160f4c0c0d0c75d33e` |
| h/2 | P06_ramp | first_spike_latency | definedness | None | 179.10999999970926 |  | inf | `r-9fb3d7dd0f85829f88b3` | `r-43160f4c0c0d0c75d33e` |
| h/2 | P06_ramp | mean_frequency | definedness | None | 6.4796915666882136 |  | inf | `r-9fb3d7dd0f85829f88b3` | `r-43160f4c0c0d0c75d33e` |
| h/2 | P06_ramp | spike_count | exceeds | 0.0 | 6.0 | 6 | 0.5 | `r-9fb3d7dd0f85829f88b3` | `r-43160f4c0c0d0c75d33e` |
| h/2 | P07_hyperpolarizing_step | baseline_voltage | exceeds | -83.9535706837972 | -78.14287766011698 | 5.81069 | 0.5 | `r-13bd10976ea90e0f7248` | `r-fa57f476719ea1c45037` |
| h/2 | P07_hyperpolarizing_step | minimum_voltage | exceeds | -98.23638153076172 | -143.25201416015625 | 45.0156 | 0.5 | `r-13bd10976ea90e0f7248` | `r-fa57f476719ea1c45037` |
| h/2 | P07_hyperpolarizing_step | sag_ratio | exceeds | 0.0020454617263496017 | 0.05124040627761139 | 0.0491949 | 0.02 | `r-13bd10976ea90e0f7248` | `r-fa57f476719ea1c45037` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -98.20716658782956 | -139.91579555350978 | 41.7086 | 0.5 | `r-13bd10976ea90e0f7248` | `r-fa57f476719ea1c45037` |
| h/2 | P07_hyperpolarizing_step | voltage_deflection | exceeds | -14.253595904032366 | -61.7729178933928 | 47.5193 | 0.71268 | `r-13bd10976ea90e0f7248` | `r-fa57f476719ea1c45037` |
| h/2 | P08_rebound | maximum_voltage | exceeds | -85.81714630128519 | -210.5807647705078 | 124.764 | 1 | `r-24306981c7a9f2760a5f` | `r-e87bd3df861b4a293587` |
| h/2 | P09_short_pulse | ap_amplitude | definedness | None | 89.98345947466694 |  | inf | `r-93824a6227b003d6e2e7` | `r-70125af582c75f190050` |
| h/2 | P09_short_pulse | ap_half_width | definedness | None | 0.7199999999993452 |  | inf | `r-93824a6227b003d6e2e7` | `r-70125af582c75f190050` |
| h/2 | P09_short_pulse | first_spike_latency | definedness | None | 48.85999999982772 |  | inf | `r-93824a6227b003d6e2e7` | `r-70125af582c75f190050` |
| h/2 | P09_short_pulse | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-93824a6227b003d6e2e7` | `r-70125af582c75f190050` |
| h/2 | P10_paired_pulses | ap_amplitude | definedness | None | 90.78250885164422 |  | inf | `r-93824a6227b003d6e2e7` | `r-70125af582c75f190050` |
| h/2 | P10_paired_pulses | first_spike_latency | definedness | None | 34.01999999984122 |  | inf | `r-93824a6227b003d6e2e7` | `r-70125af582c75f190050` |
| h/2 | P10_paired_pulses | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-93824a6227b003d6e2e7` | `r-70125af582c75f190050` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
