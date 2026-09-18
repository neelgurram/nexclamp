# Cross-simulator check

*2026-09-18T21:36:16+00:00; commit `115673a9a8a0e3d7d160c126b4ed4b0a16ecc677` (tree dirty: True). jNeuroML 0.14.0 / jLEMS 0.12.0; NEURON (not installed).*

- models checked: **7**
- exported to NEURON sources: **7 of 7**
- executed under NEURON: **0 of 7**

| model | export | .mod | runner | NEURON run | jLEMS spikes | NEURON spikes | max spike-time diff (ms) | trace RMSE (mV) |
|---|---|---|---|---|---|---|---|---|
| `pospischil2008_rs` | yes | 5 | LEMS_RS_nrn.py | not executed (no NEURON runtime) |  |  |  |  |
| `pospischil2008_lts` | yes | 7 | LEMS_LTS_nrn.py | not executed (no NEURON runtime) |  |  |  |  |
| `pospischil2008_fs` | yes | 4 | LEMS_FS_nrn.py | not executed (no NEURON runtime) |  |  |  |  |
| `nml2_hh_example` | yes | 4 | LEMS_NML2_Ex5_DetCell_nrn.py | not executed (no NEURON runtime) |  |  |  |  |
| `acnet2_pyr_soma` | yes | 7 | LEMS_m_in_b_in_nrn.py | not executed (no NEURON runtime) |  |  |  |  |
| `migliore2014_mt_soma` | yes | 7 | LEMS_OlfactoryTest_12_nrn.py | not executed (no NEURON runtime) |  |  |  |  |
| `osb_hh2_477127614` | yes | 12 | LEMS_477127614_nrn.py | not executed (no NEURON runtime) |  |  |  |  |

Level 1 (export) is portability evidence: the model is expressed faithfully enough for a second, independently written simulator to consume it. Level 2 (agreement) is descriptive only. No cross-simulator threshold is defined, because this study's tolerances are calibrated against one integrator's own discretisation error and say nothing about the gap between two integrators.
