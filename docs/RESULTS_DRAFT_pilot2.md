# Results draft: campaign `pilot2`

*Generated 2026-09-20T01:39:49+00:00 from recorded outputs at commit `5c92b4abe541a2c6d49ac636ad8509c58ae811e1` (tree dirty: True). Numbers are copied, never computed here. Bracketed lines are prompts for the researcher.*

> **development_pilot** - Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate

Protocol version `PILOT2_PROTOCOL`, study `neuron_model_behavioral_validation`.

## 1. Attrition

Exact counts at every stage; no percentage appears in this section without its counts.

| stage | n |
|---|---|
| variants generated (all strata) | 143 |
| primary semantic mutants | 88 |
| structurally valid and executable | 81 |
| numerically stable | 80 |
| admissible by frozen class (feature panel) | 75 |
| admissible including trace-only detection | 76 |
| equivalent within the tested domain | 5 |

### Faults detected only by full-trace comparison

The frozen classification uses the feature panel alone. These faults were classed **equivalent within the tested domain** - every summary feature inside tolerance on every protocol - yet full-trace comparison detected them reproducibly. They are reported here explicitly because a class-based count drops them, and they are the clearest evidence that feature-based regression testing is structurally blind to some real changes.

| variant | model | operator | frozen class |
|---|---|---|---|
| m-shift_reversal-7be708c601 | migliore2014_mt_soma | shift_reversal | 4_equivalent_within_tested_domain |

## 2. Per-model results (the generalization units)

Five models is a small number of clusters, so per-model values are reported beside any pooled figure and never replaced by it (amendment S-01, section 11.1). The right-hand columns repeat the same quantity over the mutants that carry **no prior outcome exposure** (section 11.3).

| model | mutants | admissible | canonical detected | rate | admissible (unexposed) | canonical detected (unexposed) | rate (unexposed) |
|---|---|---|---|---|---|---|---|
| acnet2_pyr_soma | 20 | 19 | 19 | 1.000 | 16 | 16 | 1.000 |
| migliore2014_mt_soma | 17 | 15 | 13 | 0.867 | 13 | 11 | 0.846 |
| nml2_hh_example | 18 | 17 | 17 | 1.000 | 14 | 14 | 1.000 |
| osb_hh2_477127614 | 17 | 12 | 8 | 0.667 | 11 | 7 | 0.636 |
| pospischil2008_fs | 16 | 13 | 13 | 1.000 | 13 | 13 | 1.000 |

Prior-exposure manifest: `manifests/PILOT2_EXPOSED_VARIANTS.csv` (9 variants).

## 3. Validation levels A-E

Levels B (canonical features) and C (canonical full trace) are never merged.

| group | n_generated | A_basic_pass | B_canonical_feature | C_canonical_trace | D_multi_protocol | E_full_battery | feature_level_canonical_survivors | full_trace_canonical_survivors |
|---|---|---|---|---|---|---|---|---|
| model_mutants__all_models | 88 | 80 | 67 | 60 | 75 | 76 | 9 | 6 |
| numerical_stress_tests__all_models | 15 | 14 | 1 | 1 | 3 | 3 | 2 | 1 |
| harmless_controls__all_models | 40 | 40 | 0 | 0 | 0 | 0 | 0 | 0 |
| model_mutants__model__acnet2_pyr_soma | 20 | 19 | 18 | 18 | 19 | 19 | 1 | 0 |
| harmless_controls__model__acnet2_pyr_soma | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 |
| numerical_stress_tests__model__acnet2_pyr_soma | 3 | 3 | 0 | 1 | 1 | 1 | 1 | 0 |
| model_mutants__model__migliore2014_mt_soma | 17 | 15 | 11 | 13 | 15 | 15 | 4 | 2 |
| harmless_controls__model__migliore2014_mt_soma | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 |
| numerical_stress_tests__model__migliore2014_mt_soma | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| model_mutants__model__nml2_hh_example | 18 | 17 | 17 | 17 | 17 | 17 | 0 | 0 |
| harmless_controls__model__nml2_hh_example | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 |
| numerical_stress_tests__model__nml2_hh_example | 3 | 3 | 1 | 0 | 1 | 1 | 0 | 0 |
| model_mutants__model__osb_hh2_477127614 | 17 | 16 | 8 | 0 | 12 | 12 | 4 | 4 |
| harmless_controls__model__osb_hh2_477127614 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 |
| numerical_stress_tests__model__osb_hh2_477127614 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| model_mutants__model__pospischil2008_fs | 16 | 13 | 13 | 12 | 12 | 13 | 0 | 0 |
| harmless_controls__model__pospischil2008_fs | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 |
| numerical_stress_tests__model__pospischil2008_fs | 3 | 3 | 0 | 0 | 1 | 1 | 1 | 1 |

## 4. Unique protocol contribution

Variants that **only** this protocol detected. A protocol that contributes nothing unique is reported as contributing nothing, and cost-matched comparison is required before any battery is called useful (S-01, section 11.2).

| protocol_id | is_canonical | n_detected_only_by_this_protocol | models | analysis_families | variant_ids |
|---|---|---|---|---|---|
| P00_canonical | True | 1 | pospischil2008_fs | maximal_conductance | m-scale_conductance-b734d01a94 |
| P02_weak_step | False | 0 |  |  |  |
| P04_step_2x | False | 0 |  |  |  |
| P05_long_step | False | 0 |  |  |  |
| P06_ramp | False | 0 |  |  |  |
| P07_hyperpolarizing_step | False | 0 |  |  |  |
| P08_rebound | False | 0 |  |  |  |
| P09_short_pulse | False | 0 |  |  |  |
| P03_rheobase | False | 0 |  |  |  |

## 5. Canonical survivors

Each apparent survivor carries its h/4 confirmation status; unconfirmed survivors are never counted as hidden drift.

| variant_id | model_id | model_set | stratum | kind | family | operator | params | class |
|---|---|---|---|---|---|---|---|---|
| m-scale_conductance-44150b501c | acnet2_pyr_soma | other_model | primary_semantic | mutant | biophysical | scale_conductance | {"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_pyr_all']", "new": "0.11360408 mS_per_cm2", "old": "0.1420051 mS_per_cm2"}], "element": "channelDensity", "element_id": "LeakConductance_pyr_all", "factor": 0.8, "generator_seed": 20260917} | 6_silent_under_canonical |
| m-scale_conductance-0fd04dc708 | migliore2014_mt_soma | other_model | primary_semantic | mutant | biophysical | scale_conductance | {"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nax_ModelViewParmSubset_1']", "new": "44.0 mS_per_cm2", "old": "40.0 mS_per_cm2"}], "element": "channelDensity", "element_id": "nax_ModelViewParmSubset_1", "factor": 1.1, "generator_seed": 20260917} | 6_silent_under_canonical |
| m-scale_conductance-a9d05675ab | migliore2014_mt_soma | other_model | primary_semantic | mutant | biophysical | scale_conductance | {"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pas_ModelViewParmSubset_1']", "new": "0.07499997 mS_per_cm2", "old": "0.0833333 mS_per_cm2"}], "element": "channelDensity", "element_id": "pas_ModelViewParmSubset_1", "factor": 0.9, "generator_seed": 20260917} | 6_silent_under_canonical |
| m-shift_reversal-7be708c601 | migliore2014_mt_soma | other_model | primary_semantic | mutant | biophysical | shift_reversal | {"changes": [{"attribute": "erev", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kdrmt_all']", "new": "-88.0 mV", "old": "-90.0 mV"}], "element": "channelDensity", "element_id": "kdrmt_all", "generator_seed": 20260917, "shift_mV": 2.0} | 4_equivalent_within_tested_domain |
| m-shift_gate_midpoint-c36e1e57f0 | migliore2014_mt_soma | other_model | primary_semantic | mutant | kinetics | shift_gate_midpoint | {"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='h']/forwardRate[1]", "new": "-60mV", "old": "-70mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='h']/reverseRate[1]", "new": "-60mV", "old": "-70mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='h']/steadyState[1]", "new": "-31.7mV", "old": "-41.7mV"}], "channel": "kamt", "delta_mV": 10.0, "gate": "h", "generator_seed": 20260917, "mechanism": "rates_and_steady_state"} | 6_silent_under_canonical |
| m-scale_conductance-d67ea70a4a | osb_hh2_477127614 | other_model | primary_semantic | mutant | biophysical | scale_conductance | {"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IL_all']", "new": "0.3364827015392 mS_per_cm2", "old": "0.420603376924 mS_per_cm2"}], "element": "channelDensity", "element_id": "IL_all", "factor": 0.8, "generator_seed": 20260917} | 6_silent_under_canonical |
| m-shift_reversal-c7e1f18cfe | osb_hh2_477127614 | other_model | primary_semantic | mutant | biophysical | shift_reversal | {"changes": [{"attribute": "erev", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "new": "-87.3418670162 mV", "old": "-92.3418670162 mV"}], "element": "channelDensity", "element_id": "Kd_all", "generator_seed": 20260917, "shift_mV": 5.0} | 6_silent_under_canonical |
| m-duplicate_conductance-06ea96d790 | osb_hh2_477127614 | other_model | primary_semantic | mutant | reference | duplicate_conductance | {"generator_seed": 20260917, "new_id": "IM_all_dup", "source_id": "IM_all"} | 6_silent_under_canonical |
| m-wrong_compatible_component-a12a6658b4 | osb_hh2_477127614 | other_model | primary_semantic | mutant | reference | wrong_compatible_component | {"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all']", "new": "Kd", "old": "IM"}], "element_id": "IM_all", "generator_seed": 20260917, "new_species": "k", "old_species": "k"} | 6_silent_under_canonical |

## 6. Valid-transformation controls (own table, never pooled)

A control classified non-equivalent is a false positive of the method.

| rows |
|---|
| 0 |

## 7. Kinetics: atomic versus compound

Reported separately and never pooled into one kinetics number.

| variant_id | model_id | model_set | stratum | kind | family | operator | params | class |
|---|---|---|---|---|---|---|---|---|
| m-shift_gate_midpoint-e68b2bd3be | acnet2_pyr_soma | other_model | primary_semantic | mutant | kinetics | shift_gate_midpoint | {"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='Ca_pyr']/ionChannel[@id='Ca_pyr']/gate[@id='m']/forwardRate[1]", "new": "1e-2V", "old": "5e-03V"}, {"attribute": "midpoint", "locator": "/neuroml[@id='Ca_pyr']/ionChannel[@id='Ca_pyr']/gate[@id='m']/reverseRate[1]", "new": "-3.9e-3V", "old": "-8.9e-3V"}], "channel": "Ca_pyr", "delta_mV": 5.0, "gate": "m", "generator_seed": 20260917, "mechanism": "rates"} | 5_non_equivalent |
| m-shift_gate_midpoint-3c7134e6ec | acnet2_pyr_soma | other_model | primary_semantic | mutant | kinetics | shift_gate_midpoint | {"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='Na_pyr']/ionChannel[@id='Na_pyr']/gate[@id='h']/forwardRate[1]", "new": "-3.3e-2V", "old": "-4.3e-2V"}, {"attribute": "midpoint", "locator": "/neuroml[@id='Na_pyr']/ionChannel[@id='Na_pyr']/gate[@id='h']/reverseRate[1]", "new": "-1e-2V", "old": "-2e-2V"}], "channel": "Na_pyr", "delta_mV": 10.0, "gate": "h", "generator_seed": 20260917, "mechanism": "rates"} | 5_non_equivalent |
| m-scale_gate_slope-d122bda225 | acnet2_pyr_soma | other_model | primary_semantic | mutant | kinetics | scale_gate_slope | {"changes": [{"attribute": "scale", "locator": "/neuroml[@id='Ca_pyr']/ionChannel[@id='Ca_pyr']/gate[@id='m']/forwardRate[1]", "new": "0.0173625V", "old": "0.01389V"}, {"attribute": "scale", "locator": "/neuroml[@id='Ca_pyr']/ionChannel[@id='Ca_pyr']/gate[@id='m']/reverseRate[1]", "new": "-0.00625V", "old": "-0.005V"}], "channel": "Ca_pyr", "factor": 1.25, "gate": "m", "generator_seed": 20260917, "mechanism": "rates"} | 5_non_equivalent |
| m-shift_forward_rate_midpoint-26075274d4 | acnet2_pyr_soma | other_model | primary_semantic | mutant | kinetics | shift_forward_rate_midpoint | {"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='Kdr_pyr']/ionChannel[@id='Kdr_pyr']/gate[@id='n']/forwardRate[1]", "new": "-1.99e-2V", "old": "-2.49e-2V"}], "channel": "Kdr_pyr", "delta_mV": 5.0, "gate": "n", "generator_seed": 20260917, "mechanism": "forward_rate"} | 5_non_equivalent |
| m-shift_gate_midpoint-f6ccf19d87 | migliore2014_mt_soma | other_model | primary_semantic | mutant | kinetics | shift_gate_midpoint | {"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='m']/forwardRate[1]", "new": "-50mV", "old": "-45mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='m']/reverseRate[1]", "new": "-50mV", "old": "-45mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='m']/steadyState[1]", "new": "12.5mV", "old": "17.5mV"}], "channel": "kamt", "delta_mV": -5.0, "gate": "m", "generator_seed": 20260917, "mechanism": "rates_and_steady_state"} | 5_non_equivalent |
| m-shift_gate_midpoint-c36e1e57f0 | migliore2014_mt_soma | other_model | primary_semantic | mutant | kinetics | shift_gate_midpoint | {"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='h']/forwardRate[1]", "new": "-60mV", "old": "-70mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='h']/reverseRate[1]", "new": "-60mV", "old": "-70mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='h']/steadyState[1]", "new": "-31.7mV", "old": "-41.7mV"}], "channel": "kamt", "delta_mV": 10.0, "gate": "h", "generator_seed": 20260917, "mechanism": "rates_and_steady_state"} | 6_silent_under_canonical |
| m-scale_gate_slope-15951a0f18 | migliore2014_mt_soma | other_model | primary_semantic | mutant | kinetics | scale_gate_slope | {"changes": [{"attribute": "scale", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='m']/forwardRate[1]", "new": "8mV", "old": "10mV"}, {"attribute": "scale", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='m']/reverseRate[1]", "new": "10.666666664mV", "old": "13.33333333mV"}, {"attribute": "scale", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='m']/steadyState[1]", "new": "11.2mV", "old": "14mV"}], "channel": "kamt", "factor": 0.8, "gate": "m", "generator_seed": 20260917, "mechanism": "rates_and_steady_state"} | 5_non_equivalent |
| m-shift_gate_midpoint-cdbd253d57 | nml2_hh_example | other_model | primary_semantic | mutant | kinetics | shift_gate_midpoint | {"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/forwardRate[1]", "new": "-35mV", "old": "-40mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/reverseRate[1]", "new": "-60mV", "old": "-65mV"}], "channel": "naChan", "delta_mV": 5.0, "gate": "m", "generator_seed": 20260917, "mechanism": "rates"} | 5_non_equivalent |
| m-shift_gate_midpoint-6ea0967285 | nml2_hh_example | other_model | primary_semantic | mutant | kinetics | shift_gate_midpoint | {"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='kChan']/gateHHrates[@id='n']/forwardRate[1]", "new": "-45mV", "old": "-55mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='kChan']/gateHHrates[@id='n']/reverseRate[1]", "new": "-55mV", "old": "-65mV"}], "channel": "kChan", "delta_mV": 10.0, "gate": "n", "generator_seed": 20260917, "mechanism": "rates"} | 5_non_equivalent |
| m-scale_gate_slope-6f355edc68 | nml2_hh_example | other_model | primary_semantic | mutant | kinetics | scale_gate_slope | {"changes": [{"attribute": "scale", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/forwardRate[1]", "new": "12.5mV", "old": "10mV"}, {"attribute": "scale", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/reverseRate[1]", "new": "-22.5mV", "old": "-18mV"}], "channel": "naChan", "factor": 1.25, "gate": "m", "generator_seed": 20260917, "mechanism": "rates"} | 5_non_equivalent |
| m-shift_forward_rate_midpoint-c7610b4176 | nml2_hh_example | other_model | primary_semantic | mutant | kinetics | shift_forward_rate_midpoint | {"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='h']/forwardRate[1]", "new": "-70mV", "old": "-65mV"}], "channel": "naChan", "delta_mV": -5.0, "gate": "h", "generator_seed": 20260917, "mechanism": "forward_rate"} | 5_non_equivalent |
| m-shift_channel_vshift-8dac96bdae | osb_hh2_477127614 | other_model | primary_semantic | mutant | kinetics | shift_channel_vshift | {"changes": [{"attribute": "vShift", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityVShift[@id='Na_all']", "new": "-3.20080138951 mV", "old": "1.79919861049 mV"}], "channel": "Na", "delta_mV": -5.0, "element_id": "Na_all", "generator_seed": 20260917} | 5_non_equivalent |

## 8. Uncertain cases

Listed explicitly rather than forced into a class.

| variant_id | model_id | model_set | stratum | kind | family | operator | params | class |
|---|---|---|---|---|---|---|---|---|
| m-scale_conductance-44150b501c | acnet2_pyr_soma | other_model | primary_semantic | mutant | biophysical | scale_conductance | {"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_pyr_all']", "new": "0.11360408 mS_per_cm2", "old": "0.1420051 mS_per_cm2"}], "element": "channelDensity", "element_id": "LeakConductance_pyr_all", "factor": 0.8, "generator_seed": 20260917} | 6_silent_under_canonical |
| m-increase_dt-22bc5325eb | acnet2_pyr_soma | other_model | numerical_robustness | mutant | numerical | increase_dt | {"changes": [{"attribute": "step", "locator": "/Lems[1]/Component[@id='sim1']", "new": "0.01ms", "old": "0.0025ms"}], "factor": 4, "generator_seed": 20260917} | 4_equivalent_within_tested_domain |
| m-omit_include-b072277531 | acnet2_pyr_soma | other_model | primary_semantic | mutant | reference | omit_include | {"generator_seed": 20260917, "href": "Ca_conc.nml", "removed": "<include xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" href=\"Ca_conc.nml\"/>"} | 2_non_executable |
| m-wrong_channel-aa3604e9d4 | migliore2014_mt_soma | other_model | primary_semantic | mutant | reference | wrong_channel | {"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pas_ModelViewParmSubset_1']", "new": "nax__sh10", "old": "pas"}], "element_id": "pas_ModelViewParmSubset_1", "generator_seed": 20260917, "new_species": "na", "old_species": "non_specific"} | 3_numerically_unstable |
| m-omit_include-a855d45581 | migliore2014_mt_soma | other_model | primary_semantic | mutant | reference | omit_include | {"generator_seed": 20260917, "href": "../kamt.channel.nml", "removed": "<include xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" href=\"../kamt.channel.nml\"/>"} | 1_structurally_invalid |
| m-wrong_channel-c9e7967952 | nml2_hh_example | other_model | primary_semantic | mutant | reference | wrong_channel | {"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='kChans']", "new": "naChan", "old": "kChan"}], "element_id": "kChans", "generator_seed": 20260917, "new_species": "na", "old_species": "k"} | 2_non_executable |
| m-increase_dt-445bb4bee3 | osb_hh2_477127614 | other_model | numerical_robustness | mutant | numerical | increase_dt | {"changes": [{"attribute": "step", "locator": "/Lems[1]/Component[@id='sim1']", "new": "0.1ms", "old": "0.025ms"}], "factor": 4, "generator_seed": 20260917} | 3_numerically_unstable |
| m-omit_include-90b7ac2f0a | osb_hh2_477127614 | other_model | primary_semantic | mutant | reference | omit_include | {"generator_seed": 20260917, "href": "IM.channel.nml", "removed": "<include xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" href=\"IM.channel.nml\"/>"} | 1_structurally_invalid |
| m-increase_dt-2391bb7a93 | pospischil2008_fs | other_model | numerical_robustness | mutant | numerical | increase_dt | {"changes": [{"attribute": "step", "locator": "/Lems[1]/Component[@id='sim1']", "new": "0.004ms", "old": "0.001ms"}], "factor": 4, "generator_seed": 20260917} | 6_silent_under_canonical |
| m-wrong_channel-9899c39ee8 | pospischil2008_fs | other_model | primary_semantic | mutant | reference | wrong_channel | {"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "new": "Na", "old": "Kd"}], "element_id": "Kd_all", "generator_seed": 20260917, "new_species": "na", "old_species": "k"} | 2_non_executable |
| m-omit_include-658ec2d5f5 | pospischil2008_fs | other_model | primary_semantic | mutant | reference | omit_include | {"generator_seed": 20260917, "href": "../../channels/Kd/Kd.channel.nml", "removed": "<include xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" href=\"../../channels/Kd/Kd.channel.nml\"/>"} | 1_structurally_invalid |
| m-wrong_compatible_component-d7c10346bc | pospischil2008_fs | other_model | primary_semantic | mutant | reference | wrong_compatible_component | {"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "new": "IM", "old": "Kd"}], "element_id": "Kd_all", "generator_seed": 20260917, "new_species": "k", "old_species": "k"} | 2_non_executable |

## 9. Numerical robustness stratum (separate analysis)

These are convergence stress tests. They never enter the semantic denominator and are never described as hidden semantic drift.

| class | n |
|---|---|
| 3_numerically_unstable | 1 |
| 4_equivalent_within_tested_domain | 12 |
| 5_non_equivalent | 1 |
| 6_silent_under_canonical | 1 |

## 10. Branch classification

- primary branch: **B_feature_level_insufficiency**
- precedence: D_pipeline_uncertainty > A_hidden_drift_supported > B_feature_level_insufficiency > C_canonical_adequacy > indeterminate

```json
{
  "n_semantic_mutants": 88,
  "n_E_admissible": 76,
  "n_controls": 40,
  "control_false_positives": 0,
  "control_false_positive_rate": 0.0,
  "controls_not_passing_basic_validation": 0,
  "feature_level_survivors": 9,
  "feature_survivors_unconfirmed_h4": 1,
  "confirmed_full_trace_survivors": 2,
  "confirmed_full_trace_survivor_models": [
    "migliore2014_mt_soma"
  ],
  "full_trace_survivors_unclassifiable": 4,
  "unclassifiable_models": [
    "osb_hh2_477127614"
  ],
  "models_without_canonical_trace": [
    "osb_hh2_477127614"
  ],
  "feature_survivors_detected_by_canonical_trace": 2,
  "refinement_excluded_fraction": 0.0,
  "canonical_B_or_C_detection_rate": 0.9210526315789473
}
```

Rules were fixed before the data existed and are not re-tuned. Branch A is never forced.

## 11. Claims this dataset does not support

- no claim of universal behavioural equivalence: an undetected difference is evidence about the tested protocols and features, not proof that two models behave identically;
- no claim of broad biological validation: these are single-compartment or somatic cells from a handful of papers;
- every coverage figure is conditional on the empirical reference battery, the frozen tolerance table and the models tested;
- nothing here is confirmatory.

## 12. For the researcher to write

- [ ] [One sentence: what the canonical-versus-battery comparison shows, in plain language.]
- [ ] [One sentence: whether any protocol earned its compute, citing section 4.]
- [ ] [One sentence: what the controls and the numerical stratum say about method noise.]
- [ ] [Limitations paragraph: model count, single simulator unless the cross-simulator check ran, RMSE insensitivity on spiking protocols, and the exposed variants.]

