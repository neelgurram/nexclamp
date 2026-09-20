# m-wrong_channel-aa3604e9d4

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `migliore2014_mt_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / wrong_channel
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pas_ModelViewParmSubset_1']", "new": "nax__sh10", "old": "pas"}], "element_id": "pas_ModelViewParmSubset_1", "generator_seed": 20260917, "new_species": "na", "old_species": "non_specific"}`
- recorded edits: `[{"file": "NeuroML2/Channels/test/MT_soma.cell.nml", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pas_ModelViewParmSubset_1']", "attribute": "ionChannel", "old": "pas", "new": "nax__sh10", "action": "set", "note": "wrong_channel"}]`
- execution overrides: `{}`
- class: **3_numerically_unstable**
- nominal-level status: numerically_unstable; runtime 788.148 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
