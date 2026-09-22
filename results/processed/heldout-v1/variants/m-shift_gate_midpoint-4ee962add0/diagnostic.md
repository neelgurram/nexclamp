# m-shift_gate_midpoint-4ee962add0

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_gate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='NaTs2_t']/ionChannel[@id='NaTs2_t']/gate[@id='m']/forwardRate[1]", "new": "-22mV", "old": "-32mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='NaTs2_t']/ionChannel[@id='NaTs2_t']/gate[@id='m']/reverseRate[1]", "new": "-22mV", "old": "-32mV"}], "channel": "NaTs2_t", "delta_mV": 10.0, "gate": "m", "generator_seed": 20260917, "mechanism": "rates"}`
- recorded edits: `[{"file": "NMC/NeuroML2/NaTs2_t.channel.nml", "locator": "/neuroml[@id='NaTs2_t']/ionChannel[@id='NaTs2_t']/gate[@id='m']/forwardRate[1]", "attribute": "midpoint", "old": "-32mV", "new": "-22mV", "action": "set", "note": "shift_gate_midpoint"}, {"file": "NMC/NeuroML2/NaTs2_t.channel.nml", "locator": "/neuroml[@id='NaTs2_t']/ionChannel[@id='NaTs2_t']/gate[@id='m']/reverseRate[1]", "attribute": "midpoint", "old": "-32mV", "new": "-22mV", "action": "set", "note": "shift_gate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 5101.086 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 88.0880088878417 | 85.34998321131638 | 2.73803 | 1.76176 | `r-f821a906ac6ddfedc3f9` | `r-6a4da87d2db59398d8b0` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 87.42731093900892 | 83.70965767396493 | 3.71765 | 3.45091 | `r-a413bdc9ef17abaeb327` | `r-c0fe8feca5a071fa91d5` |
| h/1 | P05_long_step | last_isi | exceeds | 118.6600000025901 | 110.23000000240609 | 8.43 | 2.3732 | `r-a413bdc9ef17abaeb327` | `r-c0fe8feca5a071fa91d5` |
| h/1 | P05_long_step | spike_count | exceeds | 16.0 | 17.0 | 1 | 0.5 | `r-a413bdc9ef17abaeb327` | `r-c0fe8feca5a071fa91d5` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 88.05227279779325 | 85.13166428195234 | 2.92061 | 1.76176 | `r-1175b1c4f005ecbea9cd` | `r-5121d9063fba0a8af3d1` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 86.27700805705253 | 82.81064605082179 | 3.46636 | 3.45091 | `r-019eab9c744398314e93` | `r-8b2d389a2f9ffe6a3323` |
| h/2 | P05_long_step | last_isi | exceeds | 118.89000000259512 | 110.41000000241002 | 8.48 | 2.3732 | `r-019eab9c744398314e93` | `r-8b2d389a2f9ffe6a3323` |
| h/2 | P05_long_step | spike_count | exceeds | 16.0 | 17.0 | 1 | 0.5 | `r-019eab9c744398314e93` | `r-8b2d389a2f9ffe6a3323` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
