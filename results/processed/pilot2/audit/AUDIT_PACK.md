# Audit pack: campaign `pilot2`

*20 of 103 mutants, sampled with seed 20260917 so the selection is reproducible. Generated 2026-09-20T00:32:26+00:00 at commit `930f50d9da3dee011e60420dc7bc60977de2848a` (tree dirty: False).*

## How to audit

For each mutant below, three questions. They take a minute each once you have the model file open.

1. **Does the edit match its label?** The operator name claims a specific kind of change (a conductance scaled, a reversal potential shifted, a channel reference broken). Read the old → new values and say whether that is what happened.
2. **Is the assigned class plausible?** `5_non_equivalent` means the behaviour changed reproducibly; `4_equivalent_within_tested_domain` means it did not; `2_non_executable` means the model would not run. Does that match the diagnostic?
3. **Is the detection plausible?** If protocols are listed as detecting it, does the diagnostic show a difference big enough to believe?

Record your answers in `AUDIT_SHEET.csv`. **Disagreement is the useful output** - if an edit looks mislabelled or a class looks wrong, say so; that is what the audit is for.

---

## 1. `m-duplicate_conductance-06ea96d790`

- **operator**: `duplicate_conductance`  ·  **family**: reference
- **assigned class**: `6_silent_under_canonical`
- **detected by**: P03_rheobase;P04_step_2x;P05_long_step
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `cells/HH2/HH2_477127614.cell.nml` · `/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all_dup']` · **None**: `None` → `<channelDensity xmlns="http://www.neuroml.org/schema/neuroml2" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="IM_all_dup" ionChannel="IM" condDensity="0.0165717583065 mS_per_cm2" erev="-92.3418670162 mV" ion="k"/>`

**Diagnostic recorded by the campaign**

```
# m-duplicate_conductance-06ea96d790

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / duplicate_conductance
- parameters: `{"generator_seed": 20260917, "new_id": "IM_all_dup", "source_id": "IM_all"}`
- recorded edits: `[{"file": "cells/HH2/HH2_477127614.cell.nml", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all_dup']", "attribute": null, "old": null, "new": "<channelDensity xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" id=\"IM_all_dup\" ionChannel=\"IM\" condDensity=\"0.0165717583065 mS_per_cm2\" erev=\"-92.3418670162 mV\" ion=\"k\"/>", "action": "insert", "note": "duplicate_conductance"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 4094.174 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P03_rheobase | rheobase | exceeds | 0.06447647018646267 | 0.06669626391639916 | 0.00221979 | 0.00128953 | `s-bd435463250c35027583` | `s-6cf5215c49bde44ddac4` |
| h/1 | P04_step_2x | last_isi | exceeds | 32.02999999997087 | 34.859999999968295 | 2.83 | 1.59 | `r-d2b3788dfa4671532754` | `r-d1f8922381fe884b4be0` |
| h/1 | P05_long_step | last_isi | exceeds | 56.07000000122389 | 64.30000000140353 | 8.23 | 2.61 | `r-5fe7a143f3c88a372d40` | `r-2c1bd8dcd6f601d7d9f7` |
| h/1 | P05_long_step | spike_count | exceeds | 36.0 | 32.0 | 4 | 0.5 | `r-5fe7a143f3c88a372d40` | `r-2c1bd8dcd6f601d7d9f7` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.06447647018646267 | 0.06669626391639916 | 0.00221979 | 0.00128953 | `s-4d054cac6fc39c11b1f5` | `s-947e37e5a42c19a5a6f7` |
| h/2 | P04_step_2x | last_isi | exceeds | 31.49999999997135 | 34.17999999996891 | 2.68 | 1.59 | `r-ae1b79422775c8a979b7` | `r-328993ca03d18da5f610` |
| h/2 | P05_long_step | last_isi | exceeds | 55.2000000012049 | 63.45000000138498 | 8.25 | 2.61 | `r-317893116e9cb0c903c3` | `r-672375e7feb7452feb7e` |
| h/2 | P05_long_step | spike_count | exceeds | 36.0 | 32.0 | 4 | 0.5 | `r-317893116e9cb0c903c3` | `r-672375e7feb7452feb7e` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 2. `m-recording_resolution-6959ac57de`

- **operator**: `recording_resolution`  ·  **family**: numerical
- **assigned class**: `4_equivalent_within_tested_domain`
- **detected by**: nothing
- **structurally valid**: True  ·  **execution overrides**: {"sample_every_ms": 0.05}

**The edit**

- no edit recorded

**Diagnostic recorded by the campaign**

```
# m-recording_resolution-6959ac57de

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: numerical_robustness
- kind/family/operator: mutant / numerical / recording_resolution
- parameters: `{"generator_seed": 20260917, "sample_every_ms": 0.05}`
- recorded edits: `[]`
- execution overrides: `{"sample_every_ms": 0.05}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1261.468 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 3. `m-recording_resolution-a5f502f6d0`

- **operator**: `recording_resolution`  ·  **family**: numerical
- **assigned class**: `4_equivalent_within_tested_domain`
- **detected by**: nothing
- **structurally valid**: True  ·  **execution overrides**: {"sample_every_ms": 0.05}

**The edit**

- no edit recorded

**Diagnostic recorded by the campaign**

```
# m-recording_resolution-a5f502f6d0

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: numerical_robustness
- kind/family/operator: mutant / numerical / recording_resolution
- parameters: `{"generator_seed": 20260917, "sample_every_ms": 0.05}`
- recorded edits: `[]`
- execution overrides: `{"sample_every_ms": 0.05}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 3358.131 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 4. `m-scale_capacitance-e015416fbf`

- **operator**: `scale_capacitance`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P03_rheobase;P04_step_2x;P05_long_step;P08_rebound
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `examples/NML2_SingleCompHHCell.nml` · `/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/specificCapacitance[1]` · **value**: `1.0 uF_per_cm2` → `0.5 uF_per_cm2`

**Diagnostic recorded by the campaign**

```
# m-scale_capacitance-e015416fbf

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/specificCapacitance[1]", "new": "0.5 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "0.5 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 606.371 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 95.13947677592056 | 106.54727935768 | 11.4078 | 1.90279 | `r-5f0a94c66ff17cd98a0a` | `r-05ee1b09bc7fa73032b3` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 2.5200000000155427 | 1.6500000000150976 | 0.87 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-05ee1b09bc7fa73032b3` |
| h/1 | P00_canonical | last_isi | exceeds | 16.12999999998533 | 14.939999999986412 | 1.19 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-05ee1b09bc7fa73032b3` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.015777610818933134 | 0.00665938 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-f82fa8fc0fcda59eeaee` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 92.72434234740876 | 97.59160614109814 | 4.86726 | 1.85449 | `r-66b1007575e04915ac55` | `r-84ec206da21c9b4d9c32` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 3.5399999998689395 | 2.1999999998701583 | 1.34 | 0.5 | `r-66b1007575e04915ac55` | `r-84ec206da21c9b4d9c32` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 91.2126808181487 | 96.6381721508676 | 5.42549 | 1.82425 | `r-940eedfaa66e3fa96c16` | `r-a4f61a55211f85270455` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 4.42999999986813 | 2.639999999869758 | 1.79 | 0.5 | `r-940eedfaa66e3fa96c16` | `r-a4f61a55211f85270455` |
| h/1 | P08_rebound | first_spike_latency | exceeds | 5.219999999412721 | 2.929999999414804 | 2.29 | 0.5 | `r-011ab0e03522b12f620c` | `r-846fba9437a8895f47af` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 95.29706954941832 | 106.67462158180226 | 11.3776 | 1.90279 | `r-d4235ef154cdc2eeb44c` | `r-714e0c8a0a3353751312` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 2.460000000015512 | 1.600000000015072 | 0.86 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-714e0c8a0a3353751312` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 5. `m-scale_capacitance-e86da299c1`

- **operator**: `scale_capacitance`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P03_rheobase;P04_step_2x;P05_long_step;P06_ramp;P09_short_pulse
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml` · `/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]` · **value**: `2.84 uF_per_cm2` → `1.42 uF_per_cm2`

**Diagnostic recorded by the campaign**

```
# m-scale_capacitance-e86da299c1

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "1.42 uF_per_cm2", "old": "2.84 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "2.84 uF_per_cm2", "new": "1.42 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1479.886 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.04901504481984 | 115.19244766190107 | 15.1434 | 2.00098 | `r-7ce2d1a0f19cc5d24572` | `r-d3372013b99a41353508` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 32.640000000015604 | 31.470000000015006 | 1.17 | 0.6528 | `r-7ce2d1a0f19cc5d24572` | `r-d3372013b99a41353508` |
| h/1 | P00_canonical | last_isi | exceeds | 76.88999999993013 | 67.94999999993826 | 8.94 | 1.5378 | `r-7ce2d1a0f19cc5d24572` | `r-d3372013b99a41353508` |
| h/1 | P00_canonical | spike_count | exceeds | 8.0 | 9.0 | 1 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-d3372013b99a41353508` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.006795983880882453 | 0.000819616 | 0.000152312 | `s-f72e8dc74d5f026206e4` | `s-8125cdf65ae78e98b10e` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 98.06893539575677 | 103.36754607915228 | 5.29861 | 1.96138 | `r-85c49aecb0e07f4c5069` | `r-59d2b4f3b4022be4c6a8` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 25.40999999984905 | 12.319999999860954 | 13.09 | 0.5082 | `r-85c49aecb0e07f4c5069` | `r-59d2b4f3b4022be4c6a8` |
| h/1 | P04_step_2x | last_isi | exceeds | 451.11999999958977 | 415.5399999996221 | 35.58 | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-59d2b4f3b4022be4c6a8` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 98.06814575218911 | 103.21031951683564 | 5.14217 | 1.96136 | `r-f6700284baa99a5ef41f` | `r-9398cf72774d89fd5cde` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 37.16999999983835 | 17.36999999985636 | 19.8 | 0.7434 | `r-f6700284baa99a5ef41f` | `r-9398cf72774d89fd5cde` |
| h/1 | P05_long_step | last_isi | exceeds | 586.8900000005651 | 524.0399999995234 | 62.85 | 11.7378 | `r-f6700284baa99a5ef41f` | `r-9398cf72774d89fd5cde` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 6. `m-scale_conductance-10ff293ca8`

- **operator**: `scale_conductance`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P02_weak_step;P03_rheobase;P04_step_2x;P05_long_step;P06_ramp;P07_hyperpolarizing_step
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/cells/FS/FS.cell.nml` · `/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']` · **condDensity**: `0.15 mS_per_cm2` → `0.075 mS_per_cm2`

**Diagnostic recorded by the campaign**

```
# m-scale_conductance-10ff293ca8

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "new": "0.075 mS_per_cm2", "old": "0.15 mS_per_cm2"}], "element": "channelDensity", "element_id": "LeakConductance_all", "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/cells/FS/FS.cell.nml", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "attribute": "condDensity", "old": "0.15 mS_per_cm2", "new": "0.075 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 896.915 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | first_spike_latency | exceeds | 17.199999999856516 | 10.069999999863 | 7.13 | 0.5 | `r-4cceac4cec0eb866659f` | `r-3eb3dae08757c4be7ae7` |
| h/1 | P00_canonical | last_isi | exceeds | 20.21999999998161 | 13.209999999987986 | 7.01 | 0.5 | `r-4cceac4cec0eb866659f` | `r-3eb3dae08757c4be7ae7` |
| h/1 | P00_canonical | spike_count | exceeds | 20.0 | 31.0 | 11 | 0.5 | `r-4cceac4cec0eb866659f` | `r-3eb3dae08757c4be7ae7` |
| h/1 | P02_weak_step | spike_count | exceeds | 0.0 | 6.0 | 6 | 0.5 | `r-54e05e4e4388308e9268` | `r-021307729cf1e7122622` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -60.91402953033431 | -55.51094929559746 | 5.40308 | 0.5 | `r-54e05e4e4388308e9268` | `r-021307729cf1e7122622` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.384297520661157 | 0.17894952530564853 | 0.205348 | 0.00768595 | `s-208b51a847cba1e6aceb` | `s-e452bf28638b0a2e122d` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 8.009999999864874 | 6.349999999866384 | 1.66 | 0.5 | `r-54e05e4e4388308e9268` | `r-021307729cf1e7122622` |
| h/1 | P04_step_2x | last_isi | exceeds | 10.539999999990414 | 8.919999999991887 | 1.62 | 0.5 | `r-54e05e4e4388308e9268` | `r-021307729cf1e7122622` |
| h/1 | P04_step_2x | spike_count | exceeds | 47.0 | 56.0 | 9 | 3 | `r-54e05e4e4388308e9268` | `r-021307729cf1e7122622` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 12.669999999860636 | 8.609999999864328 | 4.06 | 0.5 | `r-d95212df9ca6b2b4efff` | `r-259e7b6f88afc8ca662d` |
| h/1 | P05_long_step | last_isi | exceeds | 15.610000000340733 | 11.640000000254076 | 3.97 | 0.5 | `r-d95212df9ca6b2b4efff` | `r-259e7b6f88afc8ca662d` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 7. `m-scale_conductance-1f40a5f389`

- **operator**: `scale_conductance`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P02_weak_step;P03_rheobase;P04_step_2x;P05_long_step;P06_ramp;P07_hyperpolarizing_step
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `cells/HH2/HH2_477127614.cell.nml` · `/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']` · **condDensity**: `0.104238630103 mS_per_cm2` → `0.208477260206 mS_per_cm2`

**Diagnostic recorded by the campaign**

```
# m-scale_conductance-1f40a5f389

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "new": "0.208477260206 mS_per_cm2", "old": "0.104238630103 mS_per_cm2"}], "element": "channelDensity", "element_id": "LeakConductance_all", "factor": 2.0, "generator_seed": 20260917}`
- recorded edits: `[{"file": "cells/HH2/HH2_477127614.cell.nml", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "attribute": "condDensity", "old": "0.104238630103 mS_per_cm2", "new": "0.208477260206 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1448.958 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | first_spike_latency | exceeds | 28.91999999987314 | 49.14999999985474 | 20.23 | 0.5784 | `r-50990666ac8ec9a46823` | `r-b6ef0b5d472dfb983baa` |
| h/1 | P00_canonical | last_isi | exceeds | 25.819999999976517 | 48.58999999995581 | 22.77 | 6.6 | `r-50990666ac8ec9a46823` | `r-b6ef0b5d472dfb983baa` |
| h/1 | P00_canonical | spike_count | exceeds | 28.0 | 15.0 | 13 | 9 | `r-50990666ac8ec9a46823` | `r-b6ef0b5d472dfb983baa` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -60.68582479858395 | -65.92117814178464 | 5.23535 | 0.5 | `r-d2b3788dfa4671532754` | `r-f70c65e5d87d4486323e` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.06447647018646267 | 0.13329007581449354 | 0.0688136 | 0.00128953 | `s-bd435463250c35027583` | `s-63632ed635d7aea18d4d` |
| h/1 | P04_step_2x | adaptation_index | definedness | 0.004400096639213388 | None |  | 0.01 | `r-d2b3788dfa4671532754` | `r-f70c65e5d87d4486323e` |
| h/1 | P04_step_2x | ahp_depth | definedness | 11.031660542810322 | None |  | 1.26162 | `r-d2b3788dfa4671532754` | `r-f70c65e5d87d4486323e` |
| h/1 | P04_step_2x | ap_amplitude | definedness | 65.66345214961734 | None |  | 1.31327 | `r-d2b3788dfa4671532754` | `r-f70c65e5d87d4486323e` |
| h/1 | P04_step_2x | first_spike_latency | definedness | 41.14999999983473 | None |  | 0.823 | `r-d2b3788dfa4671532754` | `r-f70c65e5d87d4486323e` |
| h/1 | P04_step_2x | last_isi | definedness | 32.02999999997087 | None |  | 1.59 | `r-d2b3788dfa4671532754` | `r-f70c65e5d87d4486323e` |
| h/1 | P04_step_2x | spike_count | exceeds | 15.0 | 0.0 | 15 | 3 | `r-d2b3788dfa4671532754` | `r-f70c65e5d87d4486323e` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 8. `m-scale_conductance-8d921084f4`

- **operator**: `scale_conductance`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P03_rheobase;P04_step_2x;P05_long_step;P06_ramp
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/cells/FS/FS.cell.nml` · `/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Na_all']` · **condDensity**: `50.0 mS_per_cm2` → `62.5 mS_per_cm2`

**Diagnostic recorded by the campaign**

```
# m-scale_conductance-8d921084f4

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Na_all']", "new": "62.5 mS_per_cm2", "old": "50.0 mS_per_cm2"}], "element": "channelDensity", "element_id": "Na_all", "factor": 1.25, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/cells/FS/FS.cell.nml", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Na_all']", "attribute": "condDensity", "old": "50.0 mS_per_cm2", "new": "62.5 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 925.981 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -4.832305908199814 | -5.515747070309203 | 0.683441 | 0.5 | `r-4cceac4cec0eb866659f` | `r-5567f02389795c6ec4b6` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 87.45660400498362 | 89.45839691326167 | 2.00179 | 1.74913 | `r-4cceac4cec0eb866659f` | `r-5567f02389795c6ec4b6` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 17.199999999856516 | 16.23999999985739 | 0.96 | 0.5 | `r-4cceac4cec0eb866659f` | `r-5567f02389795c6ec4b6` |
| h/1 | P00_canonical | last_isi | exceeds | 20.21999999998161 | 19.43999999998232 | 0.78 | 0.5 | `r-4cceac4cec0eb866659f` | `r-5567f02389795c6ec4b6` |
| h/1 | P00_canonical | spike_count | exceeds | 20.0 | 21.0 | 1 | 0.5 | `r-4cceac4cec0eb866659f` | `r-5567f02389795c6ec4b6` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.384297520661157 | 0.37497438699542385 | 0.00932313 | 0.00768595 | `s-208b51a847cba1e6aceb` | `s-a9264b3fc05cffce0044` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 88.51488494896842 | 90.39295959601024 | 1.87807 | 1.7703 | `r-54e05e4e4388308e9268` | `r-c0256a1d41eb91e6e4c9` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 87.90636062789724 | 89.86414337277284 | 1.95778 | 1.75813 | `r-d95212df9ca6b2b4efff` | `r-73b02f2397ed958f46cb` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 12.669999999860636 | 12.129999999861127 | 0.54 | 0.5 | `r-d95212df9ca6b2b4efff` | `r-73b02f2397ed958f46cb` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 363.4899999995416 | 355.2899999995491 | 8.2 | 7.2698 | `r-5888f8cf54a64bb2eb2f` | `r-ab098fe004c83682311f` |
| h/1 | P06_ramp | spike_count | exceeds | 61.0 | 62.0 | 1 | 0.5 | `r-5888f8cf54a64bb2eb2f` | `r-ab098fe004c83682311f` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 9. `m-scale_conductance-ae18f4c43e`

- **operator**: `scale_conductance`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P03_rheobase;P04_step_2x;P05_long_step;P08_rebound
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `examples/NML2_SingleCompHHCell.nml` · `/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='naChans']` · **condDensity**: `120.0 mS_per_cm2` → `150.0 mS_per_cm2`

**Diagnostic recorded by the campaign**

```
# m-scale_conductance-ae18f4c43e

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='naChans']", "new": "150.0 mS_per_cm2", "old": "120.0 mS_per_cm2"}], "element": "channelDensity", "element_id": "naChans", "factor": 1.25, "generator_seed": 20260917}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='naChans']", "attribute": "condDensity", "old": "120.0 mS_per_cm2", "new": "150.0 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 613.925 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 95.13947677592056 | 98.40600585919444 | 3.26653 | 1.90279 | `r-5f0a94c66ff17cd98a0a` | `r-60577319b329b3cce6b4` |
| h/1 | P00_canonical | last_isi | exceeds | 16.12999999998533 | 14.569999999986749 | 1.56 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-60577319b329b3cce6b4` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.014445734580971245 | 0.00799126 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-5b1cf6bc34541e62cad7` |
| h/1 | P04_step_2x | adaptation_index | definedness | None | 0.0 |  | inf | `r-66b1007575e04915ac55` | `r-59604b72727b2cbead5d` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 92.72434234740876 | 96.61985778927826 | 3.89552 | 1.85449 | `r-66b1007575e04915ac55` | `r-59604b72727b2cbead5d` |
| h/1 | P04_step_2x | last_isi | definedness | None | 17.01999999998452 |  | inf | `r-66b1007575e04915ac55` | `r-59604b72727b2cbead5d` |
| h/1 | P04_step_2x | spike_count | exceeds | 1.0 | 30.0 | 29 | 0.5 | `r-66b1007575e04915ac55` | `r-59604b72727b2cbead5d` |
| h/1 | P05_long_step | adaptation_index | definedness | None | -2.5663727087059514e-06 |  | inf | `r-940eedfaa66e3fa96c16` | `r-15cd0326b846ce4f5961` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 91.2126808181487 | 95.7896537792231 | 4.57697 | 1.82425 | `r-940eedfaa66e3fa96c16` | `r-15cd0326b846ce4f5961` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 4.42999999986813 | 3.6299999998688577 | 0.8 | 0.5 | `r-940eedfaa66e3fa96c16` | `r-15cd0326b846ce4f5961` |
| h/1 | P05_long_step | last_isi | definedness | None | 18.550000000404907 |  | inf | `r-940eedfaa66e3fa96c16` | `r-15cd0326b846ce4f5961` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 10. `m-scale_conductance-f937b97f50`

- **operator**: `scale_conductance`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P03_rheobase;P04_step_2x
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `examples/NML2_SingleCompHHCell.nml` · `/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='kChans']` · **condDensity**: `360 S_per_m2` → `324 S_per_m2`

**Diagnostic recorded by the campaign**

```
# m-scale_conductance-f937b97f50

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='kChans']", "new": "324 S_per_m2", "old": "360 S_per_m2"}], "element": "channelDensity", "element_id": "kChans", "factor": 0.9, "generator_seed": 20260917}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='kChans']", "attribute": "condDensity", "old": "360 S_per_m2", "new": "324 S_per_m2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 611.981 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | last_isi | exceeds | 16.12999999998533 | 14.929999999986421 | 1.2 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-56eb26d40d67d8d07726` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.018407212622088658 | 0.00402978 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-2e1b8920372c31a4c6f0` |
| h/1 | P04_step_2x | adaptation_index | definedness | None | -1.123999640320115e-05 |  | inf | `r-66b1007575e04915ac55` | `r-b1b304cdfe4a52835b8a` |
| h/1 | P04_step_2x | last_isi | definedness | None | 18.529999999983147 |  | inf | `r-66b1007575e04915ac55` | `r-b1b304cdfe4a52835b8a` |
| h/1 | P04_step_2x | spike_count | exceeds | 1.0 | 27.0 | 26 | 0.5 | `r-66b1007575e04915ac55` | `r-b1b304cdfe4a52835b8a` |
| h/2 | P00_canonical | last_isi | exceeds | 16.059999999985394 | 14.869999999986476 | 1.19 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-e97f30cfb2df0a7c4cb3` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02240284133597432 | 0.018373061949320403 | 0.00402978 | 0.00044874 | `s-b96e12fd1e882cb18a94` | `s-8966edb0c1a7b619c3e8` |
| h/2 | P04_step_2x | adaptation_index | definedness | None | 0.0 |  | inf | `r-8d6f46142acd4ec898a7` | `r-e2a1a8be0d08550e99d9` |
| h/2 | P04_step_2x | last_isi | definedness | None | 18.499999999983174 |  | inf | `r-8d6f46142acd4ec898a7` | `r-e2a1a8be0d08550e99d9` |
| h/2 | P04_step_2x | spike_count | exceeds | 1.0 | 27.0 | 26 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-e2a1a8be0d08550e99d9` |

```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 11. `m-scale_gate_slope-6f355edc68`

- **operator**: `scale_gate_slope`  ·  **family**: kinetics
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P02_weak_step;P03_rheobase;P04_step_2x;P05_long_step;P06_ramp;P07_hyperpolarizing_step;P08_rebound;P09_short_pulse
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `examples/NML2_SingleCompHHCell.nml` · `/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/forwardRate[1]` · **scale**: `10mV` → `12.5mV`
- `examples/NML2_SingleCompHHCell.nml` · `/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/reverseRate[1]` · **scale**: `-18mV` → `-22.5mV`

**Diagnostic recorded by the campaign**

```
# m-scale_gate_slope-6f355edc68

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / scale_gate_slope
- parameters: `{"changes": [{"attribute": "scale", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/forwardRate[1]", "new": "12.5mV", "old": "10mV"}, {"attribute": "scale", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/reverseRate[1]", "new": "-22.5mV", "old": "-18mV"}], "channel": "naChan", "factor": 1.25, "gate": "m", "generator_seed": 20260917, "mechanism": "rates"}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/forwardRate[1]", "attribute": "scale", "old": "10mV", "new": "12.5mV", "action": "set", "note": "scale_gate_slope"}, {"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/reverseRate[1]", "attribute": "scale", "old": "-18mV", "new": "-22.5mV", "action": "set", "note": "scale_gate_slope"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 254.777 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -10.343139648437372 | -23.00288783366684 | 12.6597 | 0.517157 | `r-5f0a94c66ff17cd98a0a` | `r-89ab37845776d6dde041` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 95.13947677592056 | 81.40997505163996 | 13.7295 | 1.90279 | `r-5f0a94c66ff17cd98a0a` | `r-89ab37845776d6dde041` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 2.5200000000155427 | 7.180000000017927 | 4.66 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-89ab37845776d6dde041` |
| h/1 | P00_canonical | last_isi | exceeds | 16.12999999998533 | 12.859999999988304 | 3.27 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-89ab37845776d6dde041` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 8.0 | 1 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-89ab37845776d6dde041` |
| h/1 | P02_weak_step | spike_count | exceeds | 0.0 | 30.0 | 30 | 0.5 | `r-66b1007575e04915ac55` | `r-6489506df8371ec997e1` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -64.08310811767565 | -59.08461007939556 | 4.9985 | 0.5 | `r-66b1007575e04915ac55` | `r-6489506df8371ec997e1` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.0 | 0.022437 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-b805716222206afd104c` |
| h/1 | P04_step_2x | adaptation_index | definedness | None | -1.1015156855833627e-05 |  | inf | `r-66b1007575e04915ac55` | `r-6489506df8371ec997e1` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -10.697937011716306 | -16.907464818449988 | 6.20953 | 0.534897 | `r-66b1007575e04915ac55` | `r-6489506df8371ec997e1` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 92.72434234740876 | 90.01217651488619 | 2.71217 | 1.85449 | `r-66b1007575e04915ac55` | `r-6489506df8371ec997e1` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 12. `m-shift_forward_rate_midpoint-26075274d4`

- **operator**: `shift_forward_rate_midpoint`  ·  **family**: kinetics
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P02_weak_step;P03_rheobase;P04_step_2x;P05_long_step;P06_ramp
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `LEMSexamples/morphologies/Kdr_pyr.channel.nml` · `/neuroml[@id='Kdr_pyr']/ionChannel[@id='Kdr_pyr']/gate[@id='n']/forwardRate[1]` · **midpoint**: `-2.49e-2V` → `-1.99e-2V`

**Diagnostic recorded by the campaign**

```
# m-shift_forward_rate_midpoint-26075274d4

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_forward_rate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='Kdr_pyr']/ionChannel[@id='Kdr_pyr']/gate[@id='n']/forwardRate[1]", "new": "-1.99e-2V", "old": "-2.49e-2V"}], "channel": "Kdr_pyr", "delta_mV": 5.0, "gate": "n", "generator_seed": 20260917, "mechanism": "forward_rate"}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/Kdr_pyr.channel.nml", "locator": "/neuroml[@id='Kdr_pyr']/ionChannel[@id='Kdr_pyr']/gate[@id='n']/forwardRate[1]", "attribute": "midpoint", "old": "-2.49e-2V", "new": "-1.99e-2V", "action": "set", "note": "shift_forward_rate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1381.356 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.08360766405035329 | -0.026568783862177505 | 0.110176 | 0.01 | `r-7ce2d1a0f19cc5d24572` | `r-096dc4273f8b10fd509b` |
| h/1 | P00_canonical | ahp_depth | exceeds | -7.047089353288882 | 0.40819819859105166 | 7.45529 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-096dc4273f8b10fd509b` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.04901504481984 | 97.74502563455034 | 2.30399 | 2.00098 | `r-7ce2d1a0f19cc5d24572` | `r-096dc4273f8b10fd509b` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 32.640000000015604 | 36.29000000001747 | 3.65 | 0.6528 | `r-7ce2d1a0f19cc5d24572` | `r-096dc4273f8b10fd509b` |
| h/1 | P00_canonical | spike_count | exceeds | 8.0 | 7.0 | 1 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-096dc4273f8b10fd509b` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -66.2136446029663 | -65.30295373992912 | 0.910691 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-75bc8d3abd4d2f78f95f` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.00560071033399358 | 0.00201489 | 0.000152312 | `s-f72e8dc74d5f026206e4` | `s-e926c540e77a67af6004` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -7.019535802205411 | -2.6654319458002504 | 4.3541 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-75bc8d3abd4d2f78f95f` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 25.40999999984905 | 140.82999999974408 | 115.42 | 0.5082 | `r-85c49aecb0e07f4c5069` | `r-75bc8d3abd4d2f78f95f` |
| h/1 | P04_step_2x | last_isi | definedness | 451.11999999958977 | None |  | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-75bc8d3abd4d2f78f95f` |
| h/1 | P04_step_2x | spike_count | exceeds | 2.0 | 1.0 | 1 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-75bc8d3abd4d2f78f95f` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 13. `m-shift_gate_midpoint-cdbd253d57`

- **operator**: `shift_gate_midpoint`  ·  **family**: kinetics
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P02_weak_step;P03_rheobase;P04_step_2x;P05_long_step;P07_hyperpolarizing_step;P08_rebound;P09_short_pulse
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `examples/NML2_SingleCompHHCell.nml` · `/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/forwardRate[1]` · **midpoint**: `-40mV` → `-35mV`
- `examples/NML2_SingleCompHHCell.nml` · `/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/reverseRate[1]` · **midpoint**: `-65mV` → `-60mV`

**Diagnostic recorded by the campaign**

```
# m-shift_gate_midpoint-cdbd253d57

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_gate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/forwardRate[1]", "new": "-35mV", "old": "-40mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/reverseRate[1]", "new": "-60mV", "old": "-65mV"}], "channel": "naChan", "delta_mV": 5.0, "gate": "m", "generator_seed": 20260917, "mechanism": "rates"}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/forwardRate[1]", "attribute": "midpoint", "old": "-40mV", "new": "-35mV", "action": "set", "note": "shift_gate_midpoint"}, {"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/reverseRate[1]", "attribute": "midpoint", "old": "-65mV", "new": "-60mV", "action": "set", "note": "shift_gate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 599.695 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | -7.74713208133793e-05 | None |  | 0.01 | `r-5f0a94c66ff17cd98a0a` | `r-b88f32fc4385160d3f1f` |
| h/1 | P00_canonical | ahp_depth | definedness | -10.343139648437372 | None |  | 0.517157 | `r-5f0a94c66ff17cd98a0a` | `r-b88f32fc4385160d3f1f` |
| h/1 | P00_canonical | ap_amplitude | definedness | 95.13947677592056 | None |  | 1.90279 | `r-5f0a94c66ff17cd98a0a` | `r-b88f32fc4385160d3f1f` |
| h/1 | P00_canonical | first_spike_latency | definedness | 2.5200000000155427 | None |  | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-b88f32fc4385160d3f1f` |
| h/1 | P00_canonical | last_isi | definedness | 16.12999999998533 | None |  | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-b88f32fc4385160d3f1f` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 0.0 | 7 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-b88f32fc4385160d3f1f` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -64.08310811767565 | -64.9108287597655 | 0.827721 | 0.5 | `r-66b1007575e04915ac55` | `r-33e48155ce0adc773e25` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.09825148555426541 | 0.0758145 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-00a354bc32385158ed74` |
| h/1 | P04_step_2x | ahp_depth | definedness | -10.697937011716306 | None |  | 0.534897 | `r-66b1007575e04915ac55` | `r-33e48155ce0adc773e25` |
| h/1 | P04_step_2x | ap_amplitude | definedness | 92.72434234740876 | None |  | 1.85449 | `r-66b1007575e04915ac55` | `r-33e48155ce0adc773e25` |
| h/1 | P04_step_2x | first_spike_latency | definedness | 3.5399999998689395 | None |  | 0.5 | `r-66b1007575e04915ac55` | `r-33e48155ce0adc773e25` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 14. `m-shift_reversal-296104fa71`

- **operator**: `shift_reversal`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P02_weak_step;P03_rheobase;P04_step_2x;P05_long_step;P06_ramp;P07_hyperpolarizing_step;P09_short_pulse
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/cells/FS/FS.cell.nml` · `/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']` · **erev**: `-70.0 mV` → `-80.0 mV`

**Diagnostic recorded by the campaign**

```
# m-shift_reversal-296104fa71

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "new": "-80.0 mV", "old": "-70.0 mV"}], "element": "channelDensity", "element_id": "LeakConductance_all", "generator_seed": 20260917, "shift_mV": -10.0}`
- recorded edits: `[{"file": "NeuroML2/cells/FS/FS.cell.nml", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "attribute": "erev", "old": "-70.0 mV", "new": "-80.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1397.804 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | 0.0 | None |  | 0.01 | `r-4cceac4cec0eb866659f` | `r-2efd7faf9e7ad0b0269c` |
| h/1 | P00_canonical | ahp_depth | definedness | -4.832305908199814 | None |  | 0.5 | `r-4cceac4cec0eb866659f` | `r-2efd7faf9e7ad0b0269c` |
| h/1 | P00_canonical | ap_amplitude | definedness | 87.45660400498362 | None |  | 1.74913 | `r-4cceac4cec0eb866659f` | `r-2efd7faf9e7ad0b0269c` |
| h/1 | P00_canonical | first_spike_latency | definedness | 17.199999999856516 | None |  | 0.5 | `r-4cceac4cec0eb866659f` | `r-2efd7faf9e7ad0b0269c` |
| h/1 | P00_canonical | last_isi | definedness | 20.21999999998161 | None |  | 0.5 | `r-4cceac4cec0eb866659f` | `r-2efd7faf9e7ad0b0269c` |
| h/1 | P00_canonical | spike_count | exceeds | 20.0 | 0.0 | 20 | 0.5 | `r-4cceac4cec0eb866659f` | `r-2efd7faf9e7ad0b0269c` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -60.91402953033431 | -70.91663496704085 | 10.0026 | 0.5 | `r-54e05e4e4388308e9268` | `r-784aab310d80ae66255a` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.384297520661157 | 0.595895089133256 | 0.211598 | 0.00768595 | `s-208b51a847cba1e6aceb` | `s-5c2fd06b8d08dac27de0` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -4.612907409655477 | 4.6017837524567256 | 9.21469 | 1.51774 | `r-54e05e4e4388308e9268` | `r-784aab310d80ae66255a` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 8.009999999864874 | 15.679999999857898 | 7.67 | 0.5 | `r-54e05e4e4388308e9268` | `r-784aab310d80ae66255a` |
| h/1 | P04_step_2x | last_isi | exceeds | 10.539999999990414 | 16.539999999984957 | 6 | 0.5 | `r-54e05e4e4388308e9268` | `r-784aab310d80ae66255a` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 15. `m-shift_reversal-2c628fb0f6`

- **operator**: `shift_reversal`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P02_weak_step;P03_rheobase;P04_step_2x;P05_long_step;P06_ramp;P07_hyperpolarizing_step;P08_rebound
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml` · `/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_pyr_all']` · **erev**: `-66.0 mV` → `-61.0 mV`

**Diagnostic recorded by the campaign**

```
# m-shift_reversal-2c628fb0f6

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_pyr_all']", "new": "-61.0 mV", "old": "-66.0 mV"}], "element": "channelDensity", "element_id": "LeakConductance_pyr_all", "generator_seed": 20260917, "shift_mV": 5.0}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_pyr_all']", "attribute": "erev", "old": "-66.0 mV", "new": "-61.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1495.592 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.08360766405035329 | -0.013803017073637663 | 0.0974107 | 0.01 | `r-7ce2d1a0f19cc5d24572` | `r-a2a47d0560066a50aee0` |
| h/1 | P00_canonical | ahp_depth | exceeds | -7.047089353288882 | -0.615015553065831 | 6.43207 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-a2a47d0560066a50aee0` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.04901504481984 | 97.19705963123461 | 2.85196 | 2.00098 | `r-7ce2d1a0f19cc5d24572` | `r-a2a47d0560066a50aee0` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 32.640000000015604 | 35.41000000001702 | 2.77 | 0.6528 | `r-7ce2d1a0f19cc5d24572` | `r-a2a47d0560066a50aee0` |
| h/1 | P00_canonical | last_isi | exceeds | 76.88999999993013 | 71.91999999993465 | 4.97 | 1.5378 | `r-7ce2d1a0f19cc5d24572` | `r-a2a47d0560066a50aee0` |
| h/1 | P02_weak_step | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-dc905c17af1e27b88607` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -66.2136446029663 | -69.32851186372204 | 3.11487 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-dc905c17af1e27b88607` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.0025271497848507614 | 0.00508845 | 0.000152312 | `s-f72e8dc74d5f026206e4` | `s-5dd600ac3c198b3ab039` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -7.019535802205411 | -5.050780899047098 | 1.96875 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-dc905c17af1e27b88607` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 25.40999999984905 | 68.08999999981023 | 42.68 | 0.5082 | `r-85c49aecb0e07f4c5069` | `r-dc905c17af1e27b88607` |
| h/1 | P04_step_2x | last_isi | exceeds | 451.11999999958977 | 361.3599999996714 | 89.76 | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-dc905c17af1e27b88607` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 16. `m-shift_reversal-2ebe75d071`

- **operator**: `shift_reversal`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P06_ramp
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/cells/FS/FS.cell.nml` · `/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']` · **erev**: `-100.0 mV` → `-102.0 mV`

**Diagnostic recorded by the campaign**

```
# m-shift_reversal-2ebe75d071

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "new": "-102.0 mV", "old": "-100.0 mV"}], "element": "channelDensity", "element_id": "Kd_all", "generator_seed": 20260917, "shift_mV": -2.0}`
- recorded edits: `[{"file": "NeuroML2/cells/FS/FS.cell.nml", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "attribute": "erev", "old": "-100.0 mV", "new": "-102.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 943.725 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -4.832305908199814 | -5.663406372074732 | 0.8311 | 0.5 | `r-4cceac4cec0eb866659f` | `r-de3c292bb6f4ac8f995f` |
| h/1 | P06_ramp | spike_count | exceeds | 61.0 | 60.0 | 1 | 0.5 | `r-5888f8cf54a64bb2eb2f` | `r-fca84687f54423d7430d` |
| h/2 | P00_canonical | ahp_depth | exceeds | -4.734680175792306 | -5.562149047842723 | 0.827469 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-19692e77773ce19a20d2` |
| h/2 | P06_ramp | spike_count | exceeds | 61.0 | 60.0 | 1 | 0.5 | `r-b0adc3019253aae3e3e8` | `r-d06b569c258ff266d83c` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 17. `m-shift_reversal-7be708c601`

- **operator**: `shift_reversal`  ·  **family**: biophysical
- **assigned class**: `4_equivalent_within_tested_domain`
- **detected by**: nothing
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/Channels/test/MT_soma.cell.nml` · `/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kdrmt_all']` · **erev**: `-90.0 mV` → `-88.0 mV`

**Diagnostic recorded by the campaign**

```
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
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 18. `m-shift_reversal-a84a36ad81`

- **operator**: `shift_reversal`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P03_rheobase;P04_step_2x;P05_long_step;P09_short_pulse
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `examples/NML2_SingleCompHHCell.nml` · `/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='naChans']` · **erev**: `50.0 mV` → `45.0 mV`

**Diagnostic recorded by the campaign**

```
# m-shift_reversal-a84a36ad81

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='naChans']", "new": "45.0 mV", "old": "50.0 mV"}], "element": "channelDensity", "element_id": "naChans", "generator_seed": 20260917, "shift_mV": -5.0}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='naChans']", "attribute": "erev", "old": "50.0 mV", "new": "45.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 616.585 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 95.13947677592056 | 90.14626693705294 | 4.99321 | 1.90279 | `r-5f0a94c66ff17cd98a0a` | `r-89a1a2b96b8a791c108a` |
| h/1 | P00_canonical | last_isi | exceeds | 16.12999999998533 | 17.11999999998443 | 0.99 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-89a1a2b96b8a791c108a` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-89a1a2b96b8a791c108a` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.02424697766546001 | 0.00180999 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-d6b9f28d863b9c4e6677` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 92.72434234740876 | 87.60686111578283 | 5.11748 | 1.85449 | `r-66b1007575e04915ac55` | `r-bfa06c762a4dba558f04` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 91.2126808181487 | 85.9803009043604 | 5.23238 | 1.82425 | `r-940eedfaa66e3fa96c16` | `r-aea1e8518b9b5ef4c003` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 106.45812988261622 | 101.81092071497223 | 4.64721 | 2.12916 | `r-efc8f2fd727ba1854c5f` | `r-096e7f15ef4c7758cd7b` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 95.29706954941832 | 90.31406402572833 | 4.98301 | 1.90279 | `r-d4235ef154cdc2eeb44c` | `r-45421d731021d98553bd` |
| h/2 | P00_canonical | last_isi | exceeds | 16.059999999985394 | 17.049999999984493 | 0.99 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-45421d731021d98553bd` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-45421d731021d98553bd` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02240284133597432 | 0.02424697766546001 | 0.00184414 | 0.00044874 | `s-b96e12fd1e882cb18a94` | `s-ead643a8a37cb0adb809` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 19. `m-shift_reversal-c7e1f18cfe`

- **operator**: `shift_reversal`  ·  **family**: biophysical
- **assigned class**: `6_silent_under_canonical`
- **detected by**: P04_step_2x;P05_long_step
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `cells/HH2/HH2_477127614.cell.nml` · `/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']` · **erev**: `-92.3418670162 mV` → `-87.3418670162 mV`

**Diagnostic recorded by the campaign**

```
# m-shift_reversal-c7e1f18cfe

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "new": "-87.3418670162 mV", "old": "-92.3418670162 mV"}], "element": "channelDensity", "element_id": "Kd_all", "generator_seed": 20260917, "shift_mV": 5.0}`
- recorded edits: `[{"file": "cells/HH2/HH2_477127614.cell.nml", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "attribute": "erev", "old": "-92.3418670162 mV", "new": "-87.3418670162 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 3354.286 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P04_step_2x | ahp_depth | exceeds | 11.031660542810322 | 12.96729893747787 | 1.93564 | 1.26162 | `r-d2b3788dfa4671532754` | `r-653f0a5cbe743bf80944` |
| h/1 | P04_step_2x | last_isi | exceeds | 32.02999999997087 | 29.03999999997359 | 2.99 | 1.59 | `r-d2b3788dfa4671532754` | `r-653f0a5cbe743bf80944` |
| h/1 | P05_long_step | ahp_depth | exceeds | 10.79554604085748 | 12.72887654368644 | 1.93333 | 1.25504 | `r-5fe7a143f3c88a372d40` | `r-a7c29b454b2ad49d8e38` |
| h/1 | P05_long_step | last_isi | exceeds | 56.07000000122389 | 51.680000001128064 | 4.39 | 2.61 | `r-5fe7a143f3c88a372d40` | `r-a7c29b454b2ad49d8e38` |
| h/1 | P05_long_step | spike_count | exceeds | 36.0 | 39.0 | 3 | 0.5 | `r-5fe7a143f3c88a372d40` | `r-a7c29b454b2ad49d8e38` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 11.452200846353144 | 13.348872136439269 | 1.89667 | 1.26162 | `r-ae1b79422775c8a979b7` | `r-999541f7d8e534e7d3bf` |
| h/2 | P04_step_2x | last_isi | exceeds | 31.49999999997135 | 28.49999999997408 | 3 | 1.59 | `r-ae1b79422775c8a979b7` | `r-999541f7d8e534e7d3bf` |
| h/2 | P05_long_step | ahp_depth | exceeds | 11.21389289347907 | 13.108393620816123 | 1.8945 | 1.25504 | `r-317893116e9cb0c903c3` | `r-92465a91e66909f0c0f7` |
| h/2 | P05_long_step | last_isi | exceeds | 55.2000000012049 | 50.78000000110842 | 4.42 | 2.61 | `r-317893116e9cb0c903c3` | `r-92465a91e66909f0c0f7` |
| h/2 | P05_long_step | spike_count | exceeds | 36.0 | 40.0 | 4 | 0.5 | `r-317893116e9cb0c903c3` | `r-92465a91e66909f0c0f7` |

```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 20. `m-wrong_channel-9899c39ee8`

- **operator**: `wrong_channel`  ·  **family**: reference
- **assigned class**: `2_non_executable`
- **detected by**: nothing
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/cells/FS/FS.cell.nml` · `/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']` · **ionChannel**: `Kd` → `Na`

**Diagnostic recorded by the campaign**

```
# m-wrong_channel-9899c39ee8

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / wrong_channel
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "new": "Na", "old": "Kd"}], "element_id": "Kd_all", "generator_seed": 20260917, "new_species": "na", "old_species": "k"}`
- recorded edits: `[{"file": "NeuroML2/cells/FS/FS.cell.nml", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "attribute": "ionChannel", "old": "Kd", "new": "Na", "action": "set", "note": "wrong_channel"}]`
- execution overrides: `{}`
- class: **2_non_executable**
- nominal-level status: build_error; runtime 404.025 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---
