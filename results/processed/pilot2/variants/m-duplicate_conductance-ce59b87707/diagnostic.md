# m-duplicate_conductance-ce59b87707

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / duplicate_conductance
- parameters: `{"generator_seed": 20260917, "new_id": "naChans_dup", "source_id": "naChans"}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='naChans_dup']", "attribute": null, "old": null, "new": "<channelDensity xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" id=\"naChans_dup\" ionChannel=\"naChan\" condDensity=\"120.0 mS_per_cm2\" erev=\"50.0 mV\" ion=\"na\"/>", "action": "insert", "note": "duplicate_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 310.467 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -10.343139648437372 | -7.302795223437428 | 3.04034 | 0.517157 | `r-5f0a94c66ff17cd98a0a` | `r-e3558a263c009a6c9735` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 95.13947677592056 | 105.3365745542886 | 10.1971 | 1.90279 | `r-5f0a94c66ff17cd98a0a` | `r-e3558a263c009a6c9735` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 2.5200000000155427 | 1.4600000000150004 | 1.06 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-e3558a263c009a6c9735` |
| h/1 | P00_canonical | last_isi | exceeds | 16.12999999998533 | 13.399999999987813 | 2.73 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-e3558a263c009a6c9735` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 8.0 | 1 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-e3558a263c009a6c9735` |
| h/1 | P02_weak_step | spike_count | exceeds | 0.0 | 28.0 | 28 | 0.5 | `r-66b1007575e04915ac55` | `r-3f6cb2a07edec9fa0c03` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -64.08310811767565 | -55.947426024239746 | 8.13568 | 0.5 | `r-66b1007575e04915ac55` | `r-3f6cb2a07edec9fa0c03` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.0 | 0.022437 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-468a5e1efe282e12e649` |
| h/1 | P04_step_2x | adaptation_index | definedness | None | 0.0 |  | inf | `r-66b1007575e04915ac55` | `r-3f6cb2a07edec9fa0c03` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -10.697937011716306 | -22.470312140440633 | 11.7724 | 0.534897 | `r-66b1007575e04915ac55` | `r-3f6cb2a07edec9fa0c03` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 92.72434234740876 | 100.00539016869567 | 7.28105 | 1.85449 | `r-66b1007575e04915ac55` | `r-3f6cb2a07edec9fa0c03` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 3.5399999998689395 | 11.649999999861564 | 8.11 | 0.5 | `r-66b1007575e04915ac55` | `r-3f6cb2a07edec9fa0c03` |
| h/1 | P04_step_2x | last_isi | definedness | None | 14.90999999998644 |  | inf | `r-66b1007575e04915ac55` | `r-3f6cb2a07edec9fa0c03` |
| h/1 | P04_step_2x | spike_count | exceeds | 1.0 | 33.0 | 32 | 0.5 | `r-66b1007575e04915ac55` | `r-3f6cb2a07edec9fa0c03` |
| h/1 | P05_long_step | adaptation_index | definedness | None | -2.5599999090505306e-06 |  | inf | `r-940eedfaa66e3fa96c16` | `r-27a04d4a84010326953b` |
| h/1 | P05_long_step | ahp_depth | exceeds | -10.81385040282855 | -22.577100775696913 | 11.7633 | 0.540693 | `r-940eedfaa66e3fa96c16` | `r-27a04d4a84010326953b` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 91.2126808181487 | 100.40879440452511 | 9.19611 | 1.82425 | `r-940eedfaa66e3fa96c16` | `r-27a04d4a84010326953b` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 4.42999999986813 | 12.339999999860936 | 7.91 | 0.5 | `r-940eedfaa66e3fa96c16` | `r-27a04d4a84010326953b` |
| h/1 | P05_long_step | last_isi | definedness | None | 15.620000000340951 |  | inf | `r-940eedfaa66e3fa96c16` | `r-27a04d4a84010326953b` |
| h/1 | P05_long_step | spike_count | exceeds | 1.0 | 128.0 | 127 | 0.5 | `r-940eedfaa66e3fa96c16` | `r-27a04d4a84010326953b` |
| h/1 | P06_ramp | first_spike_latency | definedness | None | 15.91999999985768 |  | inf | `r-b32245eb811666b0240b` | `r-deff08f87ccd02fdb8de` |
| h/1 | P06_ramp | spike_count | exceeds | 0.0 | 63.0 | 63 | 0.5 | `r-b32245eb811666b0240b` | `r-deff08f87ccd02fdb8de` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -67.26261677551295 | -66.31535114898708 | 0.947266 | 0.5 | `r-66b1007575e04915ac55` | `r-3f6cb2a07edec9fa0c03` |
| h/1 | P08_rebound | first_spike_latency | exceeds | 5.219999999412721 | 3.5199999994142672 | 1.7 | 0.5 | `r-011ab0e03522b12f620c` | `r-097b566a41a1a9341f12` |
| h/1 | P08_rebound | spike_count | exceeds | 1.0 | 16.0 | 15 | 0.5 | `r-011ab0e03522b12f620c` | `r-097b566a41a1a9341f12` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -11.226577758789873 | -22.89404108331407 | 11.6675 | 0.561329 | `r-efc8f2fd727ba1854c5f` | `r-fe0a03ff1cea15679d27` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 106.45812988261622 | 101.40050125234882 | 5.05763 | 2.12916 | `r-efc8f2fd727ba1854c5f` | `r-fe0a03ff1cea15679d27` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 1.4599999998708313 | 16.67999999985699 | 15.22 | 0.5 | `r-efc8f2fd727ba1854c5f` | `r-fe0a03ff1cea15679d27` |
| h/1 | P09_short_pulse | spike_count | exceeds | 1.0 | 3.0 | 2 | 0.5 | `r-efc8f2fd727ba1854c5f` | `r-fe0a03ff1cea15679d27` |
| h/2 | P00_canonical | ahp_depth | exceeds | -10.327699567887592 | -7.791117566225495 | 2.53658 | 0.517157 | `r-d4235ef154cdc2eeb44c` | `r-10fcaa19648b9c65ed4d` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 95.29706954941832 | 106.72631835921044 | 11.4292 | 1.90279 | `r-d4235ef154cdc2eeb44c` | `r-10fcaa19648b9c65ed4d` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 2.460000000015512 | 1.3100000000149237 | 1.15 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-10fcaa19648b9c65ed4d` |
| h/2 | P00_canonical | last_isi | exceeds | 16.059999999985394 | 13.339999999987867 | 2.72 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-10fcaa19648b9c65ed4d` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 8.0 | 1 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-10fcaa19648b9c65ed4d` |
| h/2 | P02_weak_step | spike_count | exceeds | 0.0 | 28.0 | 28 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-84f63844efcc277b5c1d` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -64.08310755462634 | -56.12003482346868 | 7.96307 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-84f63844efcc277b5c1d` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02240284133597432 | 0.0 | 0.0224028 | 0.00044874 | `s-b96e12fd1e882cb18a94` | `s-0a3d7787945c1f60caa1` |
| h/2 | P04_step_2x | adaptation_index | definedness | None | 0.0 |  | inf | `r-8d6f46142acd4ec898a7` | `r-84f63844efcc277b5c1d` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -10.691650390625 | -22.248606442990564 | 11.557 | 0.534897 | `r-8d6f46142acd4ec898a7` | `r-84f63844efcc277b5c1d` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 92.82558822777118 | 100.10460662958032 | 7.27902 | 1.85449 | `r-8d6f46142acd4ec898a7` | `r-84f63844efcc277b5c1d` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 3.509999999868967 | 10.9499999998622 | 7.44 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-84f63844efcc277b5c1d` |
| h/2 | P04_step_2x | last_isi | definedness | None | 14.879999999986467 |  | inf | `r-8d6f46142acd4ec898a7` | `r-84f63844efcc277b5c1d` |
| h/2 | P04_step_2x | spike_count | exceeds | 1.0 | 33.0 | 32 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-84f63844efcc277b5c1d` |
| h/2 | P05_long_step | adaptation_index | definedness | None | 2.5665705112253726e-06 |  | inf | `r-a455ac42295a97429d02` | `r-03606ab34e8d937fb2aa` |
| h/2 | P05_long_step | ahp_depth | exceeds | -10.808036804201677 | -22.35560107189724 | 11.5476 | 0.540693 | `r-a455ac42295a97429d02` | `r-03606ab34e8d937fb2aa` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 91.37988662862392 | 100.52138900908369 | 9.1415 | 1.82425 | `r-a455ac42295a97429d02` | `r-03606ab34e8d937fb2aa` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 4.3899999998681665 | 11.649999999861564 | 7.26 | 0.5 | `r-a455ac42295a97429d02` | `r-03606ab34e8d937fb2aa` |
| h/2 | P05_long_step | last_isi | definedness | None | 15.590000000340297 |  | inf | `r-a455ac42295a97429d02` | `r-03606ab34e8d937fb2aa` |
| h/2 | P05_long_step | spike_count | exceeds | 1.0 | 128.0 | 127 | 0.5 | `r-a455ac42295a97429d02` | `r-03606ab34e8d937fb2aa` |
| h/2 | P06_ramp | first_spike_latency | definedness | None | 15.239999999858298 |  | inf | `r-4dc549d9b01b28a8eeb4` | `r-9bd703740e6d3f5873c8` |
| h/2 | P06_ramp | spike_count | exceeds | 0.0 | 63.0 | 63 | 0.5 | `r-4dc549d9b01b28a8eeb4` | `r-9bd703740e6d3f5873c8` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -67.26261789703395 | -66.31535227050807 | 0.947266 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-84f63844efcc277b5c1d` |
| h/2 | P08_rebound | first_spike_latency | exceeds | 5.189999999412748 | 3.4899999994142945 | 1.7 | 0.5 | `r-a628bd90e08153ec217d` | `r-a764d68738c7b98d786d` |
| h/2 | P08_rebound | spike_count | exceeds | 1.0 | 16.0 | 15 | 0.5 | `r-a628bd90e08153ec217d` | `r-a764d68738c7b98d786d` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -11.22248840332071 | -22.672846555295294 | 11.4504 | 0.561329 | `r-2c9f7eaf5c4d0d4f33d4` | `r-ba83c947ba0f195d44ab` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 106.43966293307548 | 101.49507522739432 | 4.94459 | 2.12916 | `r-2c9f7eaf5c4d0d4f33d4` | `r-ba83c947ba0f195d44ab` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 1.4399999998708495 | 16.279999999857353 | 14.84 | 0.5 | `r-2c9f7eaf5c4d0d4f33d4` | `r-ba83c947ba0f195d44ab` |
| h/2 | P09_short_pulse | spike_count | exceeds | 1.0 | 3.0 | 2 | 0.5 | `r-2c9f7eaf5c4d0d4f33d4` | `r-ba83c947ba0f195d44ab` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
