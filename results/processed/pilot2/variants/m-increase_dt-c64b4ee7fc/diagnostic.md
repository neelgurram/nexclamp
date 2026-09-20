# m-increase_dt-c64b4ee7fc

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: numerical_robustness
- kind/family/operator: mutant / numerical / increase_dt
- parameters: `{"changes": [{"attribute": "step", "locator": "/Lems[1]/Simulation[@id='sim1']", "new": "0.04ms", "old": "0.01ms"}], "factor": 4, "generator_seed": 20260917}`
- recorded edits: `[{"file": "LEMSexamples/LEMS_NML2_Ex5_DetCell.xml", "locator": "/Lems[1]/Simulation[@id='sim1']", "attribute": "step", "old": "0.01ms", "new": "0.04ms", "action": "set", "note": "increase_dt"}]`
- execution overrides: `{"dt_factor": 4}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 400.947 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-3013fddbc7ac921875b3` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | 106.45812988261622 | None |  | 2.12916 | `r-efc8f2fd727ba1854c5f` | `r-181fcf99436c493fcf3a` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-8716afecfc0c36585381` |
| h/2 | P09_short_pulse | ap_amplitude | definedness | 106.43966293307548 | None |  | 2.12916 | `r-2c9f7eaf5c4d0d4f33d4` | `r-19cc7315bac33e1f0a89` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
