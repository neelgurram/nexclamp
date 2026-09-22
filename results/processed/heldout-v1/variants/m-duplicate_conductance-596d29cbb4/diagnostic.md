# m-duplicate_conductance-596d29cbb4

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / duplicate_conductance
- parameters: `{"generator_seed": 20260917, "new_id": "NaTa_t_all_dup", "source_id": "NaTa_t_all"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='NaTa_t_all_dup']", "attribute": null, "old": null, "new": "<channelDensity xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" condDensity=\"300.0 mS_per_cm2\" id=\"NaTa_t_all_dup\" ionChannel=\"NaTa_t\" ion=\"na\" erev=\"50.0 mV\"/>", "action": "insert", "note": "duplicate_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4933.013 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -0.4594799502835798 | -2.0251575892957874 | 1.56568 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-a4903b7c86de5d7bd01c` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 90.78240967397937 | 100.45598603012863 | 9.67358 | 1.81565 | `r-a22266676a5c9c51fe6b` | `r-a4903b7c86de5d7bd01c` |
| h/1 | P00_canonical | last_isi | exceeds | 15.789999999985639 | 14.659999999986667 | 1.13 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-a4903b7c86de5d7bd01c` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.020148896933269586 | 0.018099856567174374 | 0.00204904 | 0.000402978 | `s-606c2ee73d10b43bdee7` | `s-c21e3cdd41426c2ada16` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 0.8740316797887999 | -0.747279680887857 | 1.62131 | 0.5 | `r-49ced7acda977f37b12b` | `r-4aa3036eaf42024ea796` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 89.04202652392433 | 99.6297645630415 | 10.5877 | 3.5976 | `r-49ced7acda977f37b12b` | `r-4aa3036eaf42024ea796` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 8.549999999864383 | 7.729999999865129 | 0.82 | 0.5 | `r-49ced7acda977f37b12b` | `r-4aa3036eaf42024ea796` |
| h/1 | P04_step_2x | last_isi | exceeds | 36.64999999996667 | 21.97999999998001 | 14.67 | 0.733 | `r-49ced7acda977f37b12b` | `r-4aa3036eaf42024ea796` |
| h/1 | P04_step_2x | spike_count | exceeds | 15.0 | 23.0 | 8 | 0.5 | `r-49ced7acda977f37b12b` | `r-4aa3036eaf42024ea796` |
| h/1 | P05_long_step | ahp_depth | exceeds | 0.4605490137727344 | -1.0186496149677424 | 1.4792 | 0.5 | `r-b99907e8e6510bd22247` | `r-0114baff8a3e668697cf` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 85.6294059753018 | 97.72978972664717 | 12.1004 | 3.92393 | `r-b99907e8e6510bd22247` | `r-0114baff8a3e668697cf` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 12.769999999860545 | 11.259999999861918 | 1.51 | 0.5 | `r-b99907e8e6510bd22247` | `r-0114baff8a3e668697cf` |
| h/1 | P05_long_step | last_isi | exceeds | 142.97000000312073 | 151.7100000033115 | 8.74 | 3.03 | `r-b99907e8e6510bd22247` | `r-0114baff8a3e668697cf` |
| h/1 | P05_long_step | spike_count | exceeds | 14.0 | 13.0 | 1 | 0.5 | `r-b99907e8e6510bd22247` | `r-0114baff8a3e668697cf` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 368.589999999537 | 333.64999999956876 | 34.94 | 7.3718 | `r-da1341cbf9665d4e7639` | `r-0130199b3b5c790ff55c` |
| h/1 | P06_ramp | spike_count | exceeds | 24.0 | 27.0 | 3 | 0.5 | `r-da1341cbf9665d4e7639` | `r-0130199b3b5c790ff55c` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -1.140654904681412 | -1.8564029108683258 | 0.715748 | 0.5 | `r-ad42eb643e1748725abb` | `r-5d76dcca3af7b3d4fb59` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 126.03113174260383 | 128.88272857692982 | 2.8516 | 2.52062 | `r-ad42eb643e1748725abb` | `r-5d76dcca3af7b3d4fb59` |
| h/2 | P00_canonical | ahp_depth | exceeds | -0.46474839399847667 | -2.044562935234495 | 1.57981 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-29d6b5acac097ccec276` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 90.22942352330233 | 100.19184875740828 | 9.96243 | 1.81565 | `r-ebfd6e5f8d6b9e916dfe` | `r-29d6b5acac097ccec276` |
| h/2 | P00_canonical | last_isi | exceeds | 15.769999999985657 | 14.639999999986685 | 1.13 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-29d6b5acac097ccec276` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.020148896933269586 | 0.018099856567174374 | 0.00204904 | 0.000402978 | `s-dcf9a3a6907c5d4ed514` | `s-8e878b2c11967a562d4e` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 0.9101022720341234 | -0.7812927068070223 | 1.69139 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-8be55f193801eca828d6` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 87.8428268328099 | 98.92243575052714 | 11.0796 | 3.5976 | `r-1e40b84a0cfdecc32574` | `r-8be55f193801eca828d6` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 8.50999999986442 | 7.689999999865165 | 0.82 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-8be55f193801eca828d6` |
| h/2 | P04_step_2x | last_isi | exceeds | 36.55999999996675 | 21.919999999980064 | 14.64 | 0.733 | `r-1e40b84a0cfdecc32574` | `r-8be55f193801eca828d6` |
| h/2 | P04_step_2x | spike_count | exceeds | 15.0 | 23.0 | 8 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-8be55f193801eca828d6` |
| h/2 | P05_long_step | ahp_depth | exceeds | 0.5531686782819634 | -1.0432937444033854 | 1.59646 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-98acef0fee084457b188` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 84.32143019785677 | 96.85442734228803 | 12.533 | 3.92393 | `r-cbc91d57fa8b8448b73b` | `r-98acef0fee084457b188` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 12.729999999860581 | 11.229999999861946 | 1.5 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-98acef0fee084457b188` |
| h/2 | P05_long_step | last_isi | exceeds | 143.98000000314278 | 151.4800000033065 | 7.5 | 3.03 | `r-cbc91d57fa8b8448b73b` | `r-98acef0fee084457b188` |
| h/2 | P05_long_step | spike_count | exceeds | 14.0 | 13.0 | 1 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-98acef0fee084457b188` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 368.53999999953703 | 333.5899999995688 | 34.95 | 7.3718 | `r-1b54cfe9f9ae3444183f` | `r-aafd0a38bd4b2d106094` |
| h/2 | P06_ramp | spike_count | exceeds | 24.0 | 28.0 | 4 | 0.5 | `r-1b54cfe9f9ae3444183f` | `r-aafd0a38bd4b2d106094` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -1.1669317245499542 | -1.8790252507519511 | 0.712094 | 0.5 | `r-12a8ce0ecdd4bde4c832` | `r-9a2b70caa2b88f0d378a` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 125.19136047490628 | 128.45422363436683 | 3.26286 | 2.52062 | `r-12a8ce0ecdd4bde4c832` | `r-9a2b70caa2b88f0d378a` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
