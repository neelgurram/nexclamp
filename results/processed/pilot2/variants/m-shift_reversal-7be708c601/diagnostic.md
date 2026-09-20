# m-shift_reversal-7be708c601

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `migliore2014_mt_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kdrmt_all']", "new": "-88.0 mV", "old": "-90.0 mV"}], "element": "channelDensity", "element_id": "kdrmt_all", "generator_seed": 20260917, "shift_mV": 2.0}`
- recorded edits: `[{"file": "NeuroML2/Channels/test/MT_soma.cell.nml", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kdrmt_all']", "attribute": "erev", "old": "-90.0 mV", "new": "-88.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 4188.372 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
