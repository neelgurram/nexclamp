# Cross-simulator check

*2026-09-23T01:18:39+00:00; commit `63e5759c962d2b2c76b69064cc1d70d6cde2a6b1` (tree dirty: True). jNeuroML 0.14.0 / jLEMS 0.12.0; NEURON 9.0.2.*

- models checked: **6**
- exported to NEURON sources: **6 of 6**
- executed under NEURON: **6 of 6**

| model | export | .mod | runner | NEURON run | jLEMS spikes | NEURON spikes | max spike-time diff (ms) | trace RMSE (mV) |
|---|---|---|---|---|---|---|---|---|
| `hay2011_soma` | yes | 14 | LEMS_L5bPyrCellHayEtAl2011_LowDt_nrn.py | ok | 7 | 7 | 0.1820211046026543 | 2.1755151586766424 |
| `bbp2015_soma` | yes | 16 | LEMS_Soma_AllNML2_nrn.py | ok | 5 | 5 | 0.041524106193946864 | 0.5248568333151097 |
| `traub2005_testseg2` | yes | 15 | LEMS_SomaTest_nrn.py | ok | 9 | 9 | 0.03869806214082416 | 0.8671696493804661 |
| `traub2005_testseg_all` | yes | 25 | LEMS_Thalamocortical_nrn.py | ok | 4 | 4 | 0.008573859501311176 | 0.18881999493008755 |
| `smith2013_singlecomp` | yes | 9 | LEMS_singleCompAllChans_nrn.py | ok | 7 | 7 | 0.06819858448972127 | 1.4042276980331152 |
| `migliore2005_ca1_soma` | yes | 8 | LEMS_CA1PyramidalCell_nrn.py | ok | 4 | 4 | 0.05765974558663345 | 2.0662940406185806 |

Level 1 (export) is portability evidence: the model is expressed faithfully enough for a second, independently written simulator to consume it. Level 2 (agreement) is descriptive only. No cross-simulator threshold is defined, because this study's tolerances are calibrated against one integrator's own discretisation error and say nothing about the gap between two integrators.
