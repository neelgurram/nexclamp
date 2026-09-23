# Online Resource 1: methods detail

*Generated 2026-09-23T01:25:17+00:00 by `scripts/build_supplement.py` at commit `9c66f82e30fa` (tree dirty: False). Every table is read from the repository's recorded files.*

## 1 Model screening criteria

Applied to the unmodified model only; a model is eligible only if it meets all thirteen.

| Criterion | Requirement |
|---|---|
| `C01_provenance` | identifiable scientific provenance (citation, source URL and pinned commit recorded) |
| `C02_reuse_rights` | documented reuse rights (licence recorded, not unclear) |
| `C03_files_present` | required files present (cell file and shipped simulation file) |
| `C04_validation` | passes NeuroML validation (cell and harness network files; relative oracle, D-006) |
| `C05_executes` | shipped simulation executes without manual intervention |
| `C06_trace_interpretable` | membrane-voltage trace finite and within -130..+80 mV |
| `C07_recording_location` | recording location resolved (harness output column read) |
| `C08_responds_to_current` | responds to current injection (rheobase found; at least one spike at 2x rheobase) |
| `C09_deterministic` | deterministic re-execution (bitwise-identical battery traces) |
| `C10_refinement_stable` | features stable under refinement (under 25% of reference entries excluded between h and h/2) |
| `C11_runtime` | estimated per-variant runtime within the budget |
| `C12_operators` | supports several mutation operators (at least 3 semantic operators with a site) |
| `C13_protocols_compatible` | every configured protocol runs and yields a feature table |

The runtime criterion (C11) used a budget of 4,200 s of estimated simulator time per variant, raised from 1,800 s before any held-out model was mutated (deviation X-25, Online Resource 2).

## 2 Models

Held-out models (confirmatory evaluation):

| Model | Source family | Publication | Licence | Repository | Commit |
|---|---|---|---|---|---|
| `#` |  |  |  |  |  |
| `Held-out` |  |  |  |  |  |
| `evaluation` |  |  |  |  |  |
| `models.` |  |  |  |  |  |
| `Assigned` |  |  |  |  |  |
| `2026-09-20` |  |  |  |  |  |
| `from` |  |  |  |  |  |
| `curation-v4.` |  |  |  |  |  |
| `#` |  |  |  |  |  |
| `ALL` |  |  |  |  |  |
| `SIX` |  |  |  |  |  |
| `eligible` |  |  |  |  |  |
| `models` |  |  |  |  |  |
| `from` |  |  |  |  |  |
| `sources` |  |  |  |  |  |
| `never` |  |  |  |  |  |
| `used` |  |  |  |  |  |
| `in` |  |  |  |  |  |
| `development` |  |  |  |  |  |
| `were` |  |  |  |  |  |
| `taken,` |  |  |  |  |  |
| `so` |  |  |  |  |  |
| `no` |  |  |  |  |  |
| `#` |  |  |  |  |  |
| `selection` |  |  |  |  |  |
| `discretion` |  |  |  |  |  |
| `was` |  |  |  |  |  |
| `exercised:` |  |  |  |  |  |
| `6` |  |  |  |  |  |
| `models,` |  |  |  |  |  |
| `4` |  |  |  |  |  |
| `independent` |  |  |  |  |  |
| `source` |  |  |  |  |  |
| `repositories.` |  |  |  |  |  |
| `#` |  |  |  |  |  |
| `None` |  |  |  |  |  |
| `has` |  |  |  |  |  |
| `ever` |  |  |  |  |  |
| `been` |  |  |  |  |  |
| `mutated` |  |  |  |  |  |
| `and` |  |  |  |  |  |
| `no` |  |  |  |  |  |
| `detection` |  |  |  |  |  |
| `outcome` |  |  |  |  |  |
| `exists` |  |  |  |  |  |
| `for` |  |  |  |  |  |
| `any` |  |  |  |  |  |
| `of` |  |  |  |  |  |
| `them.` |  |  |  |  |  |
| `hay2011_soma` | hay2011_bbp_channels | Hay E, Hill S, Schuermann F, Markram H, Segev I (2011). Models of Neocortical Layer 5b Pyramidal Cells Capturing a Wide  | MIT (OSB LICENSE; exception: NEURON directory, cite-on-use c | https://github.com/OpenSourceBrain/L5bPyrCellHayEtAl2011 | a813a88af8eb |
| `bbp2015_soma` | hay2011_bbp_channels | Markram H, Muller E, Ramaswamy S, Reimann MW, et al. (2015). Reconstruction and Simulation of Neocortical Microcircuitry | MIT (OSB LICENSE; exception: NMC/parser/L* directories carry | https://github.com/OpenSourceBrain/BlueBrainProjectShowcase | 9ab1b3935e6d |
| `traub2005_testseg2` | traub2005 | Traub RD, Contreras D, Cunningham MO, Murray H, LeBeau FEN, Roopun A, Bibbig A, Wilent WB, Higley MJ, Whittington MA (20 | GPL-2.0 (LICENSE preamble: applies to everything except dire | https://github.com/OpenSourceBrain/Thalamocortical | 5d1c9aea1659 |
| `traub2005_testseg_all` | traub2005 | Traub RD, Contreras D, Cunningham MO, Murray H, LeBeau FEN, Roopun A, Bibbig A, Wilent WB, Higley MJ, Whittington MA (20 | GPL-2.0 (LICENSE preamble: applies to everything except dire | https://github.com/OpenSourceBrain/Thalamocortical | 5d1c9aea1659 |
| `smith2013_singlecomp` | smith2013 | Smith SL, Smith IT, Branco T, Häusser M (2013). Dendritic spikes enhance stimulus selectivity in cortical neurons in viv | MIT | https://github.com/OpenSourceBrain/SmithEtAl2013-L23DendriticSpikes | 179c596e4430 |
| `migliore2005_ca1_soma` | migliore2005 | Migliore M, Ferrante M, Ascoli GA (2005). Signal Propagation in Oblique Dendrites of CA1 Pyramidal Cells. Journal of Neu | MIT (OSB LICENSE, no exceptions) | https://github.com/OpenSourceBrain/CA1PyramidalCell | b854fd29bc66 |

Development models (method fixing; never evaluated confirmatorily):

| Model | Source family | Publication | Licence | Repository | Commit |
|---|---|---|---|---|---|
| `#` |  |  |  |  |  |
| `Development` |  |  |  |  |  |
| `models:` |  |  |  |  |  |
| `every` |  |  |  |  |  |
| `model` |  |  |  |  |  |
| `whose` |  |  |  |  |  |
| `mutation` |  |  |  |  |  |
| `outcomes` |  |  |  |  |  |
| `have` |  |  |  |  |  |
| `been` |  |  |  |  |  |
| `seen.` |  |  |  |  |  |
| `#` |  |  |  |  |  |
| `Pilot` |  |  |  |  |  |
| `1` |  |  |  |  |  |
| `(2026-09-13)` |  |  |  |  |  |
| `and` |  |  |  |  |  |
| `Pilot` |  |  |  |  |  |
| `2` |  |  |  |  |  |
| `(2026-09-19).` |  |  |  |  |  |
| `These` |  |  |  |  |  |
| `can` |  |  |  |  |  |
| `never` |  |  |  |  |  |
| `be` |  |  |  |  |  |
| `held` |  |  |  |  |  |
| `out.` |  |  |  |  |  |
| `pospischil2008_rs` | pospischil2008 | Pospischil M, Toledo-Rodriguez M, Monier C, Piwkowska Z, Bal T, Fregnac Y, Markram H, Destexhe A (2008). Minimal Hodgkin | MIT (NeuroML2 directory) | https://github.com/OpenSourceBrain/PospischilEtAl2008 | 049081c39357 |
| `pospischil2008_lts` | pospischil2008 | Pospischil M, Toledo-Rodriguez M, Monier C, Piwkowska Z, Bal T, Fregnac Y, Markram H, Destexhe A (2008). Minimal Hodgkin | MIT (NeuroML2 directory) | https://github.com/OpenSourceBrain/PospischilEtAl2008 | 049081c39357 |
| `pospischil2008_fs` | pospischil2008 | Pospischil M, Toledo-Rodriguez M, Monier C, Piwkowska Z, Bal T, Fregnac Y, Markram H, Destexhe A (2008). Minimal Hodgkin | MIT (NeuroML2 directory) | https://github.com/OpenSourceBrain/PospischilEtAl2008 | 049081c39357 |
| `nml2_hh_example` | neuroml2_examples | Hodgkin AL, Huxley AF (1952). A quantitative description of membrane current and its application to conduction and excit | LGPL-3.0 | https://github.com/NeuroML/NeuroML2 | a5f5dadccd23 |
| `acnet2_pyr_soma` | acnet2_traub1991 | Beeman D (2013). A modeling study of cortical waves in primary auditory cortex. BMC Neuroscience 14(Suppl 1):P23. doi:10 | LGPL-3.0 (LICENSE.lesser) | https://github.com/NeuroML/NeuroML2 | a5f5dadccd23 |
| `migliore2014_mt_soma` | migliore2014 | Migliore M, Cavarretta F, Hines ML, Shepherd GM (2014). Distributed organization of a brain microcircuit analyzed by thr | MIT | https://github.com/OpenSourceBrain/MiglioreEtAl14_OlfactoryBulb3D | eaad1c8f4afc |
| `osb_hh2_477127614` | osb_allen_hh2 | Repository CITATION.md: Sadeh S, Silver RA, Mrsic-Flogel TD, Muir DR (2017). Assessing the Role of Inhibition in Stabili | MIT (OSB LICENSE, no exceptions stated) | https://github.com/OpenSourceBrain/MultiscaleISN | f07834754d68 |

## 3 Protocols

Stimulus amplitudes are multiples of each model's own measured rheobase. Every protocol begins with a settling period of 300 ms. The canonical protocol is each model's shipped simulation, run unchanged.

| Protocol | Description | Parameters |
|---|---|---|
| `P02_weak_step` | Weak depolarising step (0.5 x rheobase) | multiple 0.5, duration_ms 500, post_ms 200 |
| `P03_rheobase` | Rheobase search (500 ms steps, bracketing grid) | duration_ms 500, post_ms 0 |
| `P04_step_2x` | Step at 2 x rheobase | multiple 2.0, duration_ms 500, post_ms 200 |
| `P05_long_step` | Long suprathreshold step (1.5 x rheobase, 2 s) | multiple 1.5, duration_ms 2000, post_ms 200 |
| `P06_ramp` | Depolarising ramp 0 -> 3 x rheobase over 1 s | finish_multiple 3.0, duration_ms 1000, post_ms 200 |
| `P07_hyperpolarizing_step` | Hyperpolarising step (-1 x rheobase) | multiple -1.0, duration_ms 500, post_ms 200 |
| `P08_rebound` | Hyperpolarisation (-2 x rheobase, 500 ms) then release | multiple 2.0, duration_ms 500, post_window_ms 300 |
| `P09_short_pulse` | Short suprathreshold pulse (3 ms, 10 x rheobase) | multiple 10.0, pulse_ms 3, window_ms 60, post_ms 140 |

Protocols selected on the development models and frozen before the held-out evaluation: `P05_long_step`, `P04_step_2x`, `P06_ramp` (budget k = 4; the greedy rule stopped early).

## 4 Features and tolerances

A feature difference counts only if it exceeds tau = max(absolute floor, relative x |f_h|, 3 x |f_h - f_h/2|), and only if it reproduces at h and at h/2.

| Feature | Absolute floor | Relative term |
|---|---|---|
| `baseline_voltage` | 0.5 | 0.0 |
| `steady_state_voltage` | 0.5 | 0.0 |
| `voltage_deflection` | 0.5 | 0.05 |
| `sag_ratio` | 0.02 | 0.05 |
| `minimum_voltage` | 0.5 | 0.0 |
| `maximum_voltage` | 1.0 | 0.0 |
| `spike_count` | 0.5 | 0.0 |
| `mean_frequency` | 0.5 | 0.05 |
| `first_spike_latency` | 0.5 | 0.02 |
| `ap_amplitude` | 1.0 | 0.02 |
| `ap_half_width` | 0.05 | 0.05 |
| `ahp_depth` | 0.5 | 0.05 |
| `first_isi` | 0.5 | 0.02 |
| `last_isi` | 0.5 | 0.02 |
| `adaptation_index` | 0.01 | 0.1 |
| `burst_count` | 0.5 | 0.0 |
| `rheobase` | 0.0 | 0.02 |

Categorical features: `firing_regime` (exact). A feature defined in one model and undefined in the other counts as a difference (True). Sensitivity multipliers: 0.5, 1.0, 2.0, 4.0.

Full-trace comparison (reported separately, never merged with features): spike count, spike timing with tau_shift = max(0.5 ms, 3 x the reference's own h vs h/2 shift), and root-mean-square voltage difference with tau_rmse = max(0.5 mV, 3 x the reference's own h vs h/2 RMSE).

## 5 Fault operators and variants generated

| Stratum | Family | Operator | Variants |
|---|---|---|---|
| control | explicit_default | `explicit_default` | 6 |
| control | factoring | `factor_file` | 6 |
| control | formatting | `add_comments` | 6 |
| control | formatting | `xml_formatting` | 6 |
| control | literal_format | `numeric_literal_format` | 6 |
| control | renaming | `rename_identifier` | 6 |
| control | reordering | `reorder_independent` | 6 |
| control | unit_conversion | `unit_conversion` | 6 |
| numerical_robustness | numerical | `increase_dt` | 6 |
| numerical_robustness | numerical | `recording_resolution` | 6 |
| numerical_robustness | numerical | `solver_config` | 6 |
| primary_semantic | biophysical | `scale_capacitance` | 12 |
| primary_semantic | biophysical | `scale_conductance` | 24 |
| primary_semantic | biophysical | `scale_gate_time_constant` | 12 |
| primary_semantic | biophysical | `shift_reversal` | 24 |
| primary_semantic | kinetics | `scale_gate_slope` | 6 |
| primary_semantic | kinetics | `shift_forward_rate_midpoint` | 6 |
| primary_semantic | kinetics | `shift_gate_midpoint` | 12 |
| primary_semantic | reference | `duplicate_conductance` | 6 |
| primary_semantic | reference | `omit_include` | 6 |
| primary_semantic | reference | `wrong_channel` | 6 |
| primary_semantic | reference | `wrong_compatible_component` | 6 |

Severities: mild, strong, defined by prespecified bands of |ln k| for multiplicative changes and of millivolts for shifts. Sites were chosen by a seeded generator (seed 20260917) fixed before generation.

## 6 Software environment

| Item | Value |
|---|---|
| campaign | heldout-v1 |
| campaign_role | confirmatory_heldout |
| config_set_sha256 | 1e5bb74663a737efb630a73fff2009feb035b37e56f52dcee708ac370ac79e23 |
| designation | Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data |
| project_name | Neuraxis |
| protocol_version | HELDOUT_PROTOCOL_V1 |
| study_id | neuron_model_behavioral_validation |
| study_phase | confirmatory_heldout |

Simulator: jNeuroML 0.14.0 / jLEMS 0.12.0 on Temurin JDK 21.0.12.1+1; Python 3.12.10; pyNeuroML 1.3.22; libNeuroML 0.6.7; eFEL 5.7.34. Every run records its own software versions, inputs and outputs under a content-addressed identifier.

