# m-scale_gate_slope-039828a4db

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / scale_gate_slope
- parameters: `{"changes": [{"attribute": "scale", "locator": "/neuroml[@id='Ih']/ionChannel[@id='Ih']/gate[@id='m']/forwardRate[1]", "new": "-9.52mV", "old": "-11.9mV"}, {"attribute": "scale", "locator": "/neuroml[@id='Ih']/ionChannel[@id='Ih']/gate[@id='m']/reverseRate[1]", "new": "26.48mV", "old": "33.1mV"}], "channel": "Ih", "factor": 0.8, "gate": "m", "generator_seed": 20260917, "mechanism": "rates"}`
- recorded edits: `[{"file": "NMC/NeuroML2/Ih.channel.nml", "locator": "/neuroml[@id='Ih']/ionChannel[@id='Ih']/gate[@id='m']/forwardRate[1]", "attribute": "scale", "old": "-11.9mV", "new": "-9.52mV", "action": "set", "note": "scale_gate_slope"}, {"file": "NMC/NeuroML2/Ih.channel.nml", "locator": "/neuroml[@id='Ih']/ionChannel[@id='Ih']/gate[@id='m']/reverseRate[1]", "attribute": "scale", "old": "33.1mV", "new": "26.48mV", "action": "set", "note": "scale_gate_slope"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 5212.786 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -0.540112681203027 | 0.6558638657474916 | 1.19598 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-8994c88bd67be5d91e91` |
| h/1 | P00_canonical | last_isi | exceeds | 23.589999999978545 | 24.09999999997808 | 0.51 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-8994c88bd67be5d91e91` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 0.8735102996834598 | 3.669889839174033 | 2.79638 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-de8e23b11968d5c823f6` |
| h/1 | P05_long_step | ahp_depth | exceeds | 0.5048961029071961 | 3.21420899200524 | 2.70931 | 0.5 | `r-a413bdc9ef17abaeb327` | `r-56ec401dfaed699cf114` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 10.129999999862946 | 10.899999999862246 | 0.77 | 0.5 | `r-a413bdc9ef17abaeb327` | `r-56ec401dfaed699cf114` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -97.96501643676791 | -99.3950543273929 | 1.43004 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-de8e23b11968d5c823f6` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -0.9663868560786995 | 1.8545135574346716 | 2.8209 | 0.5 | `r-c4b56e49cd97e4a16650` | `r-b4d295b686315ee3dfc0` |
| h/2 | P00_canonical | ahp_depth | exceeds | -0.5443046181071622 | 0.6516096513350362 | 1.19591 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-e957f6b181b3ccad82ae` |
| h/2 | P00_canonical | last_isi | exceeds | 23.579999999978554 | 24.09999999997808 | 0.52 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-e957f6b181b3ccad82ae` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 0.8550077082320229 | 3.6508141682955113 | 2.79581 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-d1e052205398bf67f922` |
| h/2 | P05_long_step | ahp_depth | exceeds | 0.5178800226843094 | 3.23192226155426 | 2.71404 | 0.5 | `r-019eab9c744398314e93` | `r-713feb4726de9610ac0f` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 10.099999999862973 | 10.869999999862273 | 0.77 | 0.5 | `r-019eab9c744398314e93` | `r-713feb4726de9610ac0f` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -97.96501782989534 | -99.39505568389926 | 1.43004 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-d1e052205398bf67f922` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -0.9949755071020263 | 1.8180886433903112 | 2.81306 | 0.5 | `r-c07f6c024edce4a536eb` | `r-a0c868dc6c502436ac9c` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
