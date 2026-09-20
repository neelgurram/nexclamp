# m-scale_capacitance-8ea1c6d58b

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "3.414260892192 uF_per_cm2", "old": "4.26782611524 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.8, "generator_seed": 20260917}`
- recorded edits: `[{"file": "cells/HH2/HH2_477127614.cell.nml", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "4.26782611524 uF_per_cm2", "new": "3.414260892192 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1468.998 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 68.17416534535639 | 72.82069473330293 | 4.64653 | 3.91218 | `r-50990666ac8ec9a46823` | `r-a132480269df45322b4f` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 28.91999999987314 | 23.2499999998783 | 5.67 | 0.5784 | `r-50990666ac8ec9a46823` | `r-a132480269df45322b4f` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 11.031660542810322 | 8.450941390999468 | 2.58072 | 1.26162 | `r-d2b3788dfa4671532754` | `r-742773b9865cc7339d90` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 65.66345214961734 | 70.15508270387674 | 4.49163 | 1.31327 | `r-d2b3788dfa4671532754` | `r-742773b9865cc7339d90` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 41.14999999983473 | 32.95999999984218 | 8.19 | 0.823 | `r-d2b3788dfa4671532754` | `r-742773b9865cc7339d90` |
| h/1 | P04_step_2x | last_isi | exceeds | 32.02999999997087 | 28.70999999997389 | 3.32 | 1.59 | `r-d2b3788dfa4671532754` | `r-742773b9865cc7339d90` |
| h/1 | P05_long_step | ahp_depth | exceeds | 10.79554604085748 | 8.191091842657706 | 2.60445 | 1.25504 | `r-5fe7a143f3c88a372d40` | `r-8850dd3cabb9abba21ea` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 65.26353454776816 | 69.75899505766375 | 4.49546 | 1.30527 | `r-5fe7a143f3c88a372d40` | `r-8850dd3cabb9abba21ea` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 65.31999999981275 | 52.219999999824665 | 13.1 | 1.3064 | `r-5fe7a143f3c88a372d40` | `r-8850dd3cabb9abba21ea` |
| h/1 | P05_long_step | last_isi | exceeds | 56.07000000122389 | 49.240000001074804 | 6.83 | 2.61 | `r-5fe7a143f3c88a372d40` | `r-8850dd3cabb9abba21ea` |
| h/1 | P05_long_step | spike_count | exceeds | 36.0 | 41.0 | 5 | 0.5 | `r-5fe7a143f3c88a372d40` | `r-8850dd3cabb9abba21ea` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 415.89999999949396 | 402.9999999995057 | 12.9 | 8.318 | `r-0957e33747fc542d9104` | `r-898c877228dab0b3f8e2` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 66.87010574454787 | 71.5401786818266 | 4.67007 | 3.91218 | `r-cff06a8ac591df54f373` | `r-dbb3f8a0a66a4cf39db3` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 28.749999999873296 | 23.079999999878453 | 5.67 | 0.5784 | `r-cff06a8ac591df54f373` | `r-dbb3f8a0a66a4cf39db3` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 11.452200846353144 | 8.901730481466636 | 2.55047 | 1.26162 | `r-ae1b79422775c8a979b7` | `r-38090822c1a8dd139c4b` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 65.3342704782316 | 69.83417892534348 | 4.49991 | 1.31327 | `r-ae1b79422775c8a979b7` | `r-38090822c1a8dd139c4b` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 41.10999999983477 | 32.91999999984222 | 8.19 | 0.823 | `r-ae1b79422775c8a979b7` | `r-38090822c1a8dd139c4b` |
| h/2 | P04_step_2x | last_isi | exceeds | 31.49999999997135 | 28.26999999997429 | 3.23 | 1.59 | `r-ae1b79422775c8a979b7` | `r-38090822c1a8dd139c4b` |
| h/2 | P05_long_step | ahp_depth | exceeds | 11.21389289347907 | 8.639359418240254 | 2.57453 | 1.25504 | `r-317893116e9cb0c903c3` | `r-d325a1835e76c9389f6d` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 64.9877738975208 | 69.39426803771799 | 4.40649 | 1.30527 | `r-317893116e9cb0c903c3` | `r-d325a1835e76c9389f6d` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 65.27999999981279 | 52.1799999998247 | 13.1 | 1.3064 | `r-317893116e9cb0c903c3` | `r-d325a1835e76c9389f6d` |
| h/2 | P05_long_step | last_isi | exceeds | 55.2000000012049 | 48.5800000010604 | 6.62 | 2.61 | `r-317893116e9cb0c903c3` | `r-d325a1835e76c9389f6d` |
| h/2 | P05_long_step | spike_count | exceeds | 36.0 | 42.0 | 6 | 0.5 | `r-317893116e9cb0c903c3` | `r-d325a1835e76c9389f6d` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 415.849999999494 | 402.94999999950574 | 12.9 | 8.318 | `r-24b7e809e0450dd29615` | `r-29b78717a6daae01a836` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
