# m-shift_gate_midpoint-10216538ab

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_gate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='Ih']/ionChannel[@id='Ih']/gate[@id='m']/forwardRate[1]", "new": "-159.9mV", "old": "-154.9mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='Ih']/ionChannel[@id='Ih']/gate[@id='m']/reverseRate[1]", "new": "-5mV", "old": "0mV"}], "channel": "Ih", "delta_mV": -5.0, "gate": "m", "generator_seed": 20260917, "mechanism": "rates"}`
- recorded edits: `[{"file": "NMC/NeuroML2/Ih.channel.nml", "locator": "/neuroml[@id='Ih']/ionChannel[@id='Ih']/gate[@id='m']/forwardRate[1]", "attribute": "midpoint", "old": "-154.9mV", "new": "-159.9mV", "action": "set", "note": "shift_gate_midpoint"}, {"file": "NMC/NeuroML2/Ih.channel.nml", "locator": "/neuroml[@id='Ih']/ionChannel[@id='Ih']/gate[@id='m']/reverseRate[1]", "attribute": "midpoint", "old": "0mV", "new": "-5mV", "action": "set", "note": "shift_gate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 5111.174 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -0.540112681203027 | 1.942526444807669 | 2.48264 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-fd4538d5106e8b91431b` |
| h/1 | P00_canonical | last_isi | exceeds | 23.589999999978545 | 24.28999999997791 | 0.7 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-fd4538d5106e8b91431b` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 0.8735102996834598 | 3.191688130696406 | 2.31818 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-51a91ed6c58e116064d2` |
| h/1 | P05_long_step | ahp_depth | exceeds | 0.5048961029071961 | 2.7482448323572015 | 2.24335 | 0.5 | `r-a413bdc9ef17abaeb327` | `r-108a570a984e718acc6c` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 10.129999999862946 | 10.769999999862364 | 0.64 | 0.5 | `r-a413bdc9ef17abaeb327` | `r-108a570a984e718acc6c` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -97.96501643676791 | -101.48302180786166 | 3.51801 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-51a91ed6c58e116064d2` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -0.9663868560786995 | 1.3717647298169027 | 2.33815 | 0.5 | `r-c4b56e49cd97e4a16650` | `r-ec375f84ce2f10c31e42` |
| h/2 | P00_canonical | ahp_depth | exceeds | -0.5443046181071622 | 1.9382031923765055 | 2.48251 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-4f066ddba586a8e05709` |
| h/2 | P00_canonical | last_isi | exceeds | 23.579999999978554 | 24.28999999997791 | 0.71 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-4f066ddba586a8e05709` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 0.8550077082320229 | 3.172720848083088 | 2.31771 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-a87ab400212b1646c641` |
| h/2 | P05_long_step | ahp_depth | exceeds | 0.5178800226843094 | 2.7653340682966387 | 2.24745 | 0.5 | `r-019eab9c744398314e93` | `r-8a1bd149aff749b1dcfe` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 10.099999999862973 | 10.739999999862391 | 0.64 | 0.5 | `r-019eab9c744398314e93` | `r-8a1bd149aff749b1dcfe` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -97.96501782989534 | -101.48302320251497 | 3.51801 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-a87ab400212b1646c641` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -0.9949755071020263 | 1.3366078720100916 | 2.33158 | 0.5 | `r-c07f6c024edce4a536eb` | `r-f6147263d45aa02f2b42` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
