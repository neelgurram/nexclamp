# m-scale_capacitance-767ea7d652

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "0.5 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "0.5 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4682.854 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -0.4594799502835798 | -1.1547810862224992 | 0.695301 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-88e9c50dc76872593b43` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 90.78240967397937 | 101.4714698899486 | 10.6891 | 1.81565 | `r-a22266676a5c9c51fe6b` | `r-88e9c50dc76872593b43` |
| h/1 | P00_canonical | last_isi | exceeds | 15.789999999985639 | 11.569999999989477 | 4.22 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-88e9c50dc76872593b43` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 9.0 | 2 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-88e9c50dc76872593b43` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.020148896933269586 | 0.019465883477904518 | 0.000683013 | 0.000402978 | `s-606c2ee73d10b43bdee7` | `s-3b48f9f9e826d105dcd2` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 0.8740316797887999 | -0.2131327412929238 | 1.08716 | 0.5 | `r-49ced7acda977f37b12b` | `r-a3aa472a80dcbca2915a` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 89.04202652392433 | 100.32822797564754 | 11.2862 | 3.5976 | `r-49ced7acda977f37b12b` | `r-a3aa472a80dcbca2915a` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 8.549999999864383 | 4.199999999868339 | 4.35 | 0.5 | `r-49ced7acda977f37b12b` | `r-a3aa472a80dcbca2915a` |
| h/1 | P04_step_2x | last_isi | exceeds | 36.64999999996667 | 16.399999999985084 | 20.25 | 0.733 | `r-49ced7acda977f37b12b` | `r-a3aa472a80dcbca2915a` |
| h/1 | P04_step_2x | spike_count | exceeds | 15.0 | 31.0 | 16 | 0.5 | `r-49ced7acda977f37b12b` | `r-a3aa472a80dcbca2915a` |
| h/1 | P05_long_step | ahp_depth | exceeds | 0.4605490137727344 | -0.3208979390422826 | 0.781447 | 0.5 | `r-b99907e8e6510bd22247` | `r-a42815f07e1c8d12ac66` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 85.6294059753018 | 97.48492050631543 | 11.8555 | 3.92393 | `r-b99907e8e6510bd22247` | `r-a42815f07e1c8d12ac66` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 12.769999999860545 | 6.079999999866629 | 6.69 | 0.5 | `r-b99907e8e6510bd22247` | `r-a42815f07e1c8d12ac66` |
| h/1 | P05_long_step | last_isi | exceeds | 142.97000000312073 | 137.55000000300242 | 5.42 | 3.03 | `r-b99907e8e6510bd22247` | `r-a42815f07e1c8d12ac66` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 368.589999999537 | 357.0199999995475 | 11.57 | 7.3718 | `r-da1341cbf9665d4e7639` | `r-5edfce5299f7fcdb1e4d` |
| h/1 | P06_ramp | spike_count | exceeds | 24.0 | 33.0 | 9 | 0.5 | `r-da1341cbf9665d4e7639` | `r-5edfce5299f7fcdb1e4d` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 1.7699999998705493 | 0.9699999998712769 | 0.8 | 0.5 | `r-ad42eb643e1748725abb` | `r-66c902a020abe1d127b8` |
| h/2 | P00_canonical | ahp_depth | exceeds | -0.46474839399847667 | -1.1770766083899389 | 0.712328 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-ddec99e79f07079bec39` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 90.22942352330233 | 101.23296356058958 | 11.0035 | 1.81565 | `r-ebfd6e5f8d6b9e916dfe` | `r-ddec99e79f07079bec39` |
| h/2 | P00_canonical | last_isi | exceeds | 15.769999999985657 | 11.559999999989486 | 4.21 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-ddec99e79f07079bec39` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 9.0 | 2 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-ddec99e79f07079bec39` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.020148896933269586 | 0.019465883477904518 | 0.000683013 | 0.000402978 | `s-dcf9a3a6907c5d4ed514` | `s-d98e9b4dc05c2f9bee69` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 0.9101022720341234 | -0.2508234481799292 | 1.16093 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-e854eac5c78dc7cd143c` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 87.8428268328099 | 99.22156144150401 | 11.3787 | 3.5976 | `r-1e40b84a0cfdecc32574` | `r-e854eac5c78dc7cd143c` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 8.50999999986442 | 4.1799999998683575 | 4.33 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-e854eac5c78dc7cd143c` |
| h/2 | P04_step_2x | last_isi | exceeds | 36.55999999996675 | 16.319999999985157 | 20.24 | 0.733 | `r-1e40b84a0cfdecc32574` | `r-e854eac5c78dc7cd143c` |
| h/2 | P04_step_2x | spike_count | exceeds | 15.0 | 31.0 | 16 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-e854eac5c78dc7cd143c` |
| h/2 | P05_long_step | ahp_depth | exceeds | 0.5531686782819634 | -0.34704537200968844 | 0.900214 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-ac392fefe715f2dcb93a` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 84.32143019785677 | 96.30850220490474 | 11.9871 | 3.92393 | `r-cbc91d57fa8b8448b73b` | `r-ac392fefe715f2dcb93a` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 12.729999999860581 | 6.049999999866657 | 6.68 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-ac392fefe715f2dcb93a` |
| h/2 | P05_long_step | last_isi | exceeds | 143.98000000314278 | 137.52000000300177 | 6.46 | 3.03 | `r-cbc91d57fa8b8448b73b` | `r-ac392fefe715f2dcb93a` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 368.53999999953703 | 356.95999999954756 | 11.58 | 7.3718 | `r-1b54cfe9f9ae3444183f` | `r-194a2975e7a2be631b7b` |
| h/2 | P06_ramp | spike_count | exceeds | 24.0 | 33.0 | 9 | 0.5 | `r-1b54cfe9f9ae3444183f` | `r-194a2975e7a2be631b7b` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 1.7499999998705675 | 0.9499999998712951 | 0.8 | 0.5 | `r-12a8ce0ecdd4bde4c832` | `r-d2586606aeb5c6387fbf` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
