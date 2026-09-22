# Audit pack: campaign `heldout-v1` (targeted: the 6 confirmed full-trace canonical survivors)

*6 of 138 mutants, chosen by name (targeted: the 6 confirmed full-trace canonical survivors), not sampled. Generated 2026-09-22T15:14:08+00:00 at commit `4de0e9d67ffca2de3a8f626fe16bd10a80950a31` (tree dirty: False).*

## How to audit

For each mutant below, three questions. They take a minute each once you have the model file open.

1. **Does the edit match its label?** The operator name claims a specific kind of change (a conductance scaled, a reversal potential shifted, a channel reference broken). Read the old → new values and say whether that is what happened.
2. **Is the assigned class plausible?** `5_non_equivalent` means the behaviour changed reproducibly; `4_equivalent_within_tested_domain` means it did not; `2_non_executable` means the model would not run. Does that match the diagnostic?
3. **Is the detection plausible?** If protocols are listed as detecting it, does the diagnostic show a difference big enough to believe?

Record your answers in `AUDIT_SHEET.csv`. **Disagreement is the useful output** - if an edit looks mislabelled or a class looks wrong, say so; that is what the audit is for.

---

## 1. `m-scale_conductance-211745202a`

- **operator**: `scale_conductance`  ·  **family**: biophysical
- **assigned class**: `6_silent_under_canonical`
- **detected by**: P05_long_step
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml` · `/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityNernst[@id='Ca_HVA_all']` · **condDensity**: `0.992 mS_per_cm2` → `1.0912 mS_per_cm2`

**Diagnostic recorded by the campaign**

```
# m-scale_conductance-211745202a

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityNernst[@id='Ca_HVA_all']", "new": "1.0912 mS_per_cm2", "old": "0.992 mS_per_cm2"}], "element": "channelDensityNernst", "element_id": "Ca_HVA_all", "factor": 1.1, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityNernst[@id='Ca_HVA_all']", "attribute": "condDensity", "old": "0.992 mS_per_cm2", "new": "1.0912 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 10777.708 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P05_long_step | last_isi | exceeds | 142.97000000312073 | 148.30000000288578 | 5.33 | 3.03 | `r-b99907e8e6510bd22247` | `r-366bafc2c9bd474d5ba3` |
| h/1 | P05_long_step | spike_count | exceeds | 14.0 | 13.0 | 1 | 0.5 | `r-b99907e8e6510bd22247` | `r-366bafc2c9bd474d5ba3` |
| h/2 | P05_long_step | last_isi | exceeds | 143.98000000314278 | 149.34000000316496 | 5.36 | 3.03 | `r-cbc91d57fa8b8448b73b` | `r-7aff52af6d554a0a23b3` |
| h/2 | P05_long_step | spike_count | exceeds | 14.0 | 13.0 | 1 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-7aff52af6d554a0a23b3` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 2. `m-scale_conductance-75492a609a`

- **operator**: `scale_conductance`  ·  **family**: biophysical
- **assigned class**: `4_equivalent_within_tested_domain`
- **detected by**: nothing
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml` · `/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Im_all']` · **condDensity**: `0.0675 mS_per_cm2` → `0.03375 mS_per_cm2`

**Diagnostic recorded by the campaign**

```
# m-scale_conductance-75492a609a

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Im_all']", "new": "0.03375 mS_per_cm2", "old": "0.0675 mS_per_cm2"}], "element": "channelDensity", "element_id": "Im_all", "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Im_all']", "attribute": "condDensity", "old": "0.0675 mS_per_cm2", "new": "0.03375 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 10866.323 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 3. `m-scale_gate_time_constant-02eb4e0b90`

- **operator**: `scale_gate_time_constant`  ·  **family**: biophysical
- **assigned class**: `6_silent_under_canonical`
- **detected by**: P05_long_step
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `neuroConstruct/generatedNeuroML2/Ca_HVA.channel.nml` · `/neuroml[@id='Ca_HVA']/ionChannel[@id='Ca_HVA']/gate[@id='m']/forwardRate[1]` · **rate**: `0.209per_ms` → `0.26125per_ms`
- `neuroConstruct/generatedNeuroML2/Ca_HVA.channel.nml` · `/neuroml[@id='Ca_HVA']/ionChannel[@id='Ca_HVA']/gate[@id='m']/reverseRate[1]` · **rate**: `0.94per_ms` → `1.175per_ms`

**Diagnostic recorded by the campaign**

```
# m-scale_gate_time_constant-02eb4e0b90

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"changes": [{"attribute": "rate", "locator": "/neuroml[@id='Ca_HVA']/ionChannel[@id='Ca_HVA']/gate[@id='m']/forwardRate[1]", "new": "0.26125per_ms", "old": "0.209per_ms"}, {"attribute": "rate", "locator": "/neuroml[@id='Ca_HVA']/ionChannel[@id='Ca_HVA']/gate[@id='m']/reverseRate[1]", "new": "1.175per_ms", "old": "0.94per_ms"}], "channel": "Ca_HVA", "factor": 1.25, "gate": "m", "generator_seed": 20260917, "mechanism": "rate_parameters"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/Ca_HVA.channel.nml", "locator": "/neuroml[@id='Ca_HVA']/ionChannel[@id='Ca_HVA']/gate[@id='m']/forwardRate[1]", "attribute": "rate", "old": "0.209per_ms", "new": "0.26125per_ms", "action": "set", "note": "scale_gate_time_constant"}, {"file": "neuroConstruct/generatedNeuroML2/Ca_HVA.channel.nml", "locator": "/neuroml[@id='Ca_HVA']/ionChannel[@id='Ca_HVA']/gate[@id='m']/reverseRate[1]", "attribute": "rate", "old": "0.94per_ms", "new": "1.175per_ms", "action": "set", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 10787.712 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P05_long_step | last_isi | exceeds | 142.97000000312073 | 153.4100000033486 | 10.44 | 3.03 | `r-b99907e8e6510bd22247` | `r-fa9e902cc0d05131563a` |
| h/1 | P05_long_step | spike_count | exceeds | 14.0 | 13.0 | 1 | 0.5 | `r-b99907e8e6510bd22247` | `r-fa9e902cc0d05131563a` |
| h/2 | P05_long_step | last_isi | exceeds | 143.98000000314278 | 154.36000000336935 | 10.38 | 3.03 | `r-cbc91d57fa8b8448b73b` | `r-1c8c55be264e3d964924` |
| h/2 | P05_long_step | spike_count | exceeds | 14.0 | 13.0 | 1 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-1c8c55be264e3d964924` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 4. `m-scale_gate_time_constant-31e82d8467`

- **operator**: `scale_gate_time_constant`  ·  **family**: biophysical
- **assigned class**: `4_equivalent_within_tested_domain`
- **detected by**: nothing
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `neuroConstruct/generatedNeuroML2/kad.channel.nml` · `/neuroml[@id='kad']/ionChannel[@id='kad']/gate[@id='l']/q10Settings[1]` · **fixedQ10**: `1` → `0.8`

**Diagnostic recorded by the campaign**

```
# m-scale_gate_time_constant-31e82d8467

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"changes": [{"attribute": "fixedQ10", "locator": "/neuroml[@id='kad']/ionChannel[@id='kad']/gate[@id='l']/q10Settings[1]", "new": "0.8", "old": "1"}], "channel": "kad", "factor": 0.8, "gate": "l", "generator_seed": 20260917, "mechanism": "q10_scale"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/kad.channel.nml", "locator": "/neuroml[@id='kad']/ionChannel[@id='kad']/gate[@id='l']/q10Settings[1]", "attribute": "fixedQ10", "old": "1", "new": "0.8", "action": "set", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 6118.647 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 5. `m-scale_gate_time_constant-de97b02e71`

- **operator**: `scale_gate_time_constant`  ·  **family**: biophysical
- **assigned class**: `6_silent_under_canonical`
- **detected by**: P05_long_step
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NMC/NeuroML2/Ca_HVA.channel.nml` · `/neuroml[@id='Ca_HVA']/ionChannel[@id='Ca_HVA']/gate[@id='m']/forwardRate[1]` · **rate**: `0.209per_ms` → `0.26125per_ms`
- `NMC/NeuroML2/Ca_HVA.channel.nml` · `/neuroml[@id='Ca_HVA']/ionChannel[@id='Ca_HVA']/gate[@id='m']/reverseRate[1]` · **rate**: `0.94per_ms` → `1.175per_ms`

**Diagnostic recorded by the campaign**

```
# m-scale_gate_time_constant-de97b02e71

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"changes": [{"attribute": "rate", "locator": "/neuroml[@id='Ca_HVA']/ionChannel[@id='Ca_HVA']/gate[@id='m']/forwardRate[1]", "new": "0.26125per_ms", "old": "0.209per_ms"}, {"attribute": "rate", "locator": "/neuroml[@id='Ca_HVA']/ionChannel[@id='Ca_HVA']/gate[@id='m']/reverseRate[1]", "new": "1.175per_ms", "old": "0.94per_ms"}], "channel": "Ca_HVA", "factor": 1.25, "gate": "m", "generator_seed": 20260917, "mechanism": "rate_parameters"}`
- recorded edits: `[{"file": "NMC/NeuroML2/Ca_HVA.channel.nml", "locator": "/neuroml[@id='Ca_HVA']/ionChannel[@id='Ca_HVA']/gate[@id='m']/forwardRate[1]", "attribute": "rate", "old": "0.209per_ms", "new": "0.26125per_ms", "action": "set", "note": "scale_gate_time_constant"}, {"file": "NMC/NeuroML2/Ca_HVA.channel.nml", "locator": "/neuroml[@id='Ca_HVA']/ionChannel[@id='Ca_HVA']/gate[@id='m']/reverseRate[1]", "attribute": "rate", "old": "0.94per_ms", "new": "1.175per_ms", "action": "set", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 12139.369 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P05_long_step | last_isi | exceeds | 118.6600000025901 | 127.2500000027776 | 8.59 | 2.3732 | `r-a413bdc9ef17abaeb327` | `r-08ea8f23288a8448e79d` |
| h/1 | P05_long_step | spike_count | exceeds | 16.0 | 15.0 | 1 | 0.5 | `r-a413bdc9ef17abaeb327` | `r-08ea8f23288a8448e79d` |
| h/2 | P05_long_step | last_isi | exceeds | 118.89000000259512 | 127.41000000278109 | 8.52 | 2.3732 | `r-019eab9c744398314e93` | `r-1546b6c6ba113e2022d0` |
| h/2 | P05_long_step | spike_count | exceeds | 16.0 | 15.0 | 1 | 0.5 | `r-019eab9c744398314e93` | `r-1546b6c6ba113e2022d0` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 6. `m-shift_reversal-e5f14f8fb3`

- **operator**: `shift_reversal`  ·  **family**: biophysical
- **assigned class**: `4_equivalent_within_tested_domain`
- **detected by**: nothing
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml` · `/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Im_all']` · **erev**: `-85.0 mV` → `-95.0 mV`

**Diagnostic recorded by the campaign**

```
# m-shift_reversal-e5f14f8fb3

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Im_all']", "new": "-95.0 mV", "old": "-85.0 mV"}], "element": "channelDensity", "element_id": "Im_all", "generator_seed": 20260917, "shift_mV": -10.0}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Im_all']", "attribute": "erev", "old": "-85.0 mV", "new": "-95.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 10688.727 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---
