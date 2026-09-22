# m-shift_forward_rate_midpoint-3567e7da5d

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_forward_rate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='cal']/ionChannel[@id='cal']/gate[@id='m']/forwardRate[1]", "new": "10mV", "old": "5mV"}], "channel": "cal", "delta_mV": 5.0, "gate": "m", "generator_seed": 20260917, "mechanism": "forward_rate"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/cal.channel.nml", "locator": "/neuroml[@id='cal']/ionChannel[@id='cal']/gate[@id='m']/forwardRate[1]", "attribute": "midpoint", "old": "5mV", "new": "10mV", "action": "set", "note": "shift_forward_rate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 7928.029 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -8.248406196708032 | -8.95960055299053 | 0.711194 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-f3568b54fe741ab02b8f` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -63.19053124313325 | -62.14721578292818 | 1.04332 | 0.5 | `r-96e71f2e3b8549494d50` | `r-07707ba5f0cf681dd37c` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.06143706031008811 | 0.0453520934362407 | 0.016085 | 0.00122874 | `s-fa4d0c2502716e8c3739` | `s-f6d951f022fc0157a882` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -3.06435100805065 | -9.666789372710838 | 6.60244 | 1.14578 | `r-96e71f2e3b8549494d50` | `r-07707ba5f0cf681dd37c` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 71.33246612267223 | 68.96096229797476 | 2.3715 | 1.42665 | `r-96e71f2e3b8549494d50` | `r-07707ba5f0cf681dd37c` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 29.099999999845693 | 3.0299999998694034 | 26.07 | 0.582 | `r-96e71f2e3b8549494d50` | `r-07707ba5f0cf681dd37c` |
| h/1 | P05_long_step | ahp_depth | exceeds | -2.799466059340233 | -5.169017155971716 | 2.36955 | 1.17341 | `r-74af15e68cf19cbae102` | `r-7c2a6f673aa002882300` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 42.88999999983315 | 26.929999999847666 | 15.96 | 0.8578 | `r-74af15e68cf19cbae102` | `r-7c2a6f673aa002882300` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 382.869999999524 | 288.03999999961025 | 94.83 | 7.6574 | `r-6afcc4c87334b55f282e` | `r-98409a9e0614ebfff4ca` |
| h/2 | P00_canonical | ahp_depth | exceeds | -8.213585962703469 | -8.924379035607899 | 0.710793 | 0.5 | `r-87bcc3cd30685deaf603` | `r-3eeb4b13f8436972dfd9` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -63.19052997512787 | -62.14721236038178 | 1.04332 | 0.5 | `r-6290d36f97e6ddeb2b58` | `r-b5b4ee2f9ff049c4f65f` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.06143706031008811 | 0.0453520934362407 | 0.016085 | 0.00122874 | `s-54b0d60082a59a1582ae` | `s-11557b259a9c14eeec38` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -2.68242419940799 | -9.32167945351624 | 6.63926 | 1.14578 | `r-6290d36f97e6ddeb2b58` | `r-b5b4ee2f9ff049c4f65f` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 71.00378608656828 | 68.79989433214689 | 2.20389 | 1.42665 | `r-6290d36f97e6ddeb2b58` | `r-b5b4ee2f9ff049c4f65f` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 29.029999999845757 | 2.979999999869449 | 26.05 | 0.582 | `r-6290d36f97e6ddeb2b58` | `r-b5b4ee2f9ff049c4f65f` |
| h/2 | P05_long_step | ahp_depth | exceeds | -2.408330571497629 | -4.796792368571431 | 2.38846 | 1.17341 | `r-f1a8b6a7a66c54d9b827` | `r-41e59adaac6d015a33a8` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 42.819999999833215 | 26.84999999984774 | 15.97 | 0.8578 | `r-f1a8b6a7a66c54d9b827` | `r-41e59adaac6d015a33a8` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 382.78999999952407 | 287.9599999996103 | 94.83 | 7.6574 | `r-ce6273bb85e534e50ecc` | `r-59e814592bb5d35b6114` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
