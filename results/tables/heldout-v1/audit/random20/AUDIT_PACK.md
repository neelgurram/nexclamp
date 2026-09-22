# Audit pack: campaign `heldout-v1`

*20 of 138 mutants, sampled with seed 20260917 so the selection is reproducible. Generated 2026-09-22T15:14:08+00:00 at commit `4de0e9d67ffca2de3a8f626fe16bd10a80950a31` (tree dirty: False).*

## How to audit

For each mutant below, three questions. They take a minute each once you have the model file open.

1. **Does the edit match its label?** The operator name claims a specific kind of change (a conductance scaled, a reversal potential shifted, a channel reference broken). Read the old → new values and say whether that is what happened.
2. **Is the assigned class plausible?** `5_non_equivalent` means the behaviour changed reproducibly; `4_equivalent_within_tested_domain` means it did not; `2_non_executable` means the model would not run. Does that match the diagnostic?
3. **Is the detection plausible?** If protocols are listed as detecting it, does the diagnostic show a difference big enough to believe?

Record your answers in `AUDIT_SHEET.csv`. **Disagreement is the useful output** - if an edit looks mislabelled or a class looks wrong, say so; that is what the audit is for.

---

## 1. `m-duplicate_conductance-49ae908693`

- **operator**: `duplicate_conductance`  ·  **family**: reference
- **assigned class**: `4_equivalent_within_tested_domain`
- **detected by**: nothing
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/singleCompAllChans.cell.nml` · `/neuroml[@id='cell']/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='ca_all_dup']` · **None**: `None` → `<channelDensity xmlns="http://www.neuroml.org/schema/neuroml2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" condDensity="0.5e-4 S_per_cm2" id="ca_all_dup" ionChannel="ca" ion="ca" erev="140.0 mV"/>`

**Diagnostic recorded by the campaign**

```
# m-duplicate_conductance-49ae908693

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / duplicate_conductance
- parameters: `{"generator_seed": 20260917, "new_id": "ca_all_dup", "source_id": "ca_all"}`
- recorded edits: `[{"file": "NeuroML2/singleCompAllChans.cell.nml", "locator": "/neuroml[@id='cell']/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='ca_all_dup']", "attribute": null, "old": null, "new": "<channelDensity xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" condDensity=\"0.5e-4 S_per_cm2\" id=\"ca_all_dup\" ionChannel=\"ca\" ion=\"ca\" erev=\"140.0 mV\"/>", "action": "insert", "note": "duplicate_conductance"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 980.218 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 2. `m-duplicate_conductance-f1055b2803`

- **operator**: `duplicate_conductance`  ·  **family**: reference
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P03_rheobase;P04_step_2x;P05_long_step;P06_ramp;P09_short_pulse
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml` · `/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kdr_all_dup']` · **None**: `None` → `<channelDensity xmlns="http://www.neuroml.org/schema/neuroml2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" condDensity="10.0 mS_per_cm2" id="kdr_all_dup" ionChannel="kdr" ion="k" erev="-90.0 mV"/>`

**Diagnostic recorded by the campaign**

```
# m-duplicate_conductance-f1055b2803

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / duplicate_conductance
- parameters: `{"generator_seed": 20260917, "new_id": "kdr_all_dup", "source_id": "kdr_all"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kdr_all_dup']", "attribute": null, "old": null, "new": "<channelDensity xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" condDensity=\"10.0 mS_per_cm2\" id=\"kdr_all_dup\" ionChannel=\"kdr\" ion=\"k\" erev=\"-90.0 mV\"/>", "action": "insert", "note": "duplicate_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 3432.248 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -11.854831069263057 | -16.481418173111507 | 4.62659 | 0.592742 | `r-1855c6a207dcec8ed210` | `r-1e3a3480776f1a2c3ba4` |
| h/1 | P00_canonical | last_isi | exceeds | 18.329999999996353 | 19.40999999999641 | 1.08 | 0.5 | `r-1855c6a207dcec8ed210` | `r-1e3a3480776f1a2c3ba4` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.0006830134553650707 | 0.000102452 | 6.83013e-05 | `s-b1b4baffdde7651e5212` | `s-6666d6cd966cfa7696d4` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -14.775756835937727 | -18.76663208007767 | 3.99088 | 0.738788 | `r-0925b86f96a976919154` | `r-a8785fab935981a65bea` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 16.069999999857544 | 17.57999999985617 | 1.51 | 0.5 | `r-0925b86f96a976919154` | `r-a8785fab935981a65bea` |
| h/1 | P04_step_2x | last_isi | exceeds | 40.059999999963566 | 41.39999999996235 | 1.34 | 0.8012 | `r-0925b86f96a976919154` | `r-a8785fab935981a65bea` |
| h/1 | P04_step_2x | spike_count | exceeds | 13.0 | 12.0 | 1 | 0.5 | `r-0925b86f96a976919154` | `r-a8785fab935981a65bea` |
| h/1 | P05_long_step | ahp_depth | exceeds | -15.073226928710938 | -18.987228393554688 | 3.914 | 0.753661 | `r-4ab59c3e1336e488abd6` | `r-1cb566d9fda5525060ab` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 23.149999999851104 | 26.929999999847666 | 3.78 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-1cb566d9fda5525060ab` |
| h/1 | P05_long_step | last_isi | exceeds | 51.510000001124354 | 54.380000001187 | 2.87 | 1.0302 | `r-4ab59c3e1336e488abd6` | `r-1cb566d9fda5525060ab` |
| h/1 | P05_long_step | spike_count | exceeds | 39.0 | 37.0 | 2 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-1cb566d9fda5525060ab` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 3. `m-increase_dt-1086ebecdc`

- **operator**: `increase_dt`  ·  **family**: numerical
- **assigned class**: `6_silent_under_canonical`
- **detected by**: P04_step_2x;P05_long_step;P09_short_pulse
- **structurally valid**: True  ·  **execution overrides**: {"dt_factor": 4}

**The edit**

- `neuroConstruct/generatedNeuroML2/LEMS_SomaTest.xml` · `/Lems[1]/Component[@id='sim1']` · **step**: `0.001ms` → `0.004ms`

**Diagnostic recorded by the campaign**

```
# m-increase_dt-1086ebecdc

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: numerical_robustness
- kind/family/operator: mutant / numerical / increase_dt
- parameters: `{"changes": [{"attribute": "step", "locator": "/Lems[1]/Component[@id='sim1']", "new": "0.004ms", "old": "0.001ms"}], "factor": 4, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/LEMS_SomaTest.xml", "locator": "/Lems[1]/Component[@id='sim1']", "attribute": "step", "old": "0.001ms", "new": "0.004ms", "action": "set", "note": "increase_dt"}]`
- execution overrides: `{"dt_factor": 4}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 4244.191 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P04_step_2x | ahp_depth | exceeds | -5.43348429870143 | -9.857047598513958 | 4.42356 | 1.14528 | `r-531ed8bf9e8ec22d7778` | `r-b802b6afee05fcd2508a` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 76.68460655583269 | 79.81501006754402 | 3.1304 | 1.89637 | `r-531ed8bf9e8ec22d7778` | `r-b802b6afee05fcd2508a` |
| h/1 | P05_long_step | ahp_depth | exceeds | -5.300969345084837 | -9.8301013971748 | 4.52913 | 1.15254 | `r-c181d8dc3f2e9e1a86cf` | `r-b7c4314662117788e8bc` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 77.26993942349823 | 80.348255157643 | 3.07832 | 1.98255 | `r-c181d8dc3f2e9e1a86cf` | `r-b7c4314662117788e8bc` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -8.488179428100779 | -11.637315512319745 | 3.14914 | 1.08676 | `r-f411679bd6f2a1231337` | `r-124b6807b6d36e9968cf` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | 90.83680152686651 | None |  | 1.81674 | `r-f411679bd6f2a1231337` | `r-124b6807b6d36e9968cf` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -5.051723726911618 | -6.419106249471852 | 1.36738 | 1.14528 | `r-c4e93fb668595b0fb26c` | `r-f4bd187382e6295b1b4a` |
| h/2 | P04_step_2x | spike_count | exceeds | 18.0 | 19.0 | 1 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-f4bd187382e6295b1b4a` |
| h/2 | P05_long_step | ahp_depth | exceeds | -4.916790255219169 | -6.3045333658653675 | 1.38774 | 1.15254 | `r-c41be102b8e8611b929c` | `r-4254824c006ae8f03b98` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -8.125927218107364 | -9.304373578344212 | 1.17845 | 1.08676 | `r-4bcc4e2fdcca97c21eee` | `r-93d23ba8256ca3e63fc7` |

```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 4. `m-increase_dt-9ff98cb7be`

- **operator**: `increase_dt`  ·  **family**: numerical
- **assigned class**: `6_silent_under_canonical`
- **detected by**: P09_short_pulse
- **structurally valid**: True  ·  **execution overrides**: {"dt_factor": 4}

**The edit**

- `NeuroML2/LEMS_singleCompAllChans.xml` · `/Lems[1]/Component[@id='sim1']` · **step**: `0.001 ms` → `0.004 ms`

**Diagnostic recorded by the campaign**

```
# m-increase_dt-9ff98cb7be

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: numerical_robustness
- kind/family/operator: mutant / numerical / increase_dt
- parameters: `{"changes": [{"attribute": "step", "locator": "/Lems[1]/Component[@id='sim1']", "new": "0.004 ms", "old": "0.001 ms"}], "factor": 4, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/LEMS_singleCompAllChans.xml", "locator": "/Lems[1]/Component[@id='sim1']", "attribute": "step", "old": "0.001 ms", "new": "0.004 ms", "action": "set", "note": "increase_dt"}]`
- execution overrides: `{"dt_factor": 4}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 2192.279 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P04_step_2x | ahp_depth | exceeds | -12.946651097611621 | 134.4641600018608 | 147.411 | 0.647333 | `r-d2cafd1fc897dbfd8130` | `r-50d0636dd5bd16e9d578` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -13.72103464253783 | 123.24873889333371 | 136.97 | 0.686052 | `r-83f9184aaeefc65499cb` | `r-0cc45cec00e9cb3f994f` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | 134.16434859879257 | None |  | 2.68329 | `r-83f9184aaeefc65499cb` | `r-0cc45cec00e9cb3f994f` |
| h/2 | P09_short_pulse | ap_amplitude | definedness | 133.76337051196737 | None |  | 2.68329 | `r-dc583bb05cf4bf59d02c` | `r-1a321840c45f7404e51c` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 5. `m-scale_capacitance-8d53b9976a`

- **operator**: `scale_capacitance`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P04_step_2x;P05_long_step;P06_ramp;P09_short_pulse
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml` · `/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]` · **value**: `1.0 uF_per_cm2` → `0.8 uF_per_cm2`

**Diagnostic recorded by the campaign**

```
# m-scale_capacitance-8d53b9976a

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "0.8 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.8, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml", "locator": "/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "0.8 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 7999.145 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.5216693418942094 | 0.5961538461539415 | 0.0744845 | 0.0521669 | `r-068a1eafd4afbbd6d23e` | `r-4ad81b10de1d72340581` |
| h/1 | P00_canonical | ahp_depth | exceeds | -8.248406196708032 | -10.326367164725468 | 2.07796 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-4ad81b10de1d72340581` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 74.70865440368996 | 80.04728317258994 | 5.33863 | 1.49417 | `r-068a1eafd4afbbd6d23e` | `r-4ad81b10de1d72340581` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 2.950000000000788 | 2.2700000000006817 | 0.68 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-4ad81b10de1d72340581` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -3.06435100805065 | -11.189402613277124 | 8.12505 | 1.14578 | `r-96e71f2e3b8549494d50` | `r-3bc2dc6596dd3a852a90` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 29.099999999845693 | 2.6099999998697854 | 26.49 | 0.582 | `r-96e71f2e3b8549494d50` | `r-3bc2dc6596dd3a852a90` |
| h/1 | P05_long_step | ahp_depth | exceeds | -2.799466059340233 | -5.095271143619044 | 2.29581 | 1.17341 | `r-74af15e68cf19cbae102` | `r-fc4a06e8bc4503feecb2` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 72.98996734843095 | 75.77654838611471 | 2.78658 | 1.4598 | `r-74af15e68cf19cbae102` | `r-fc4a06e8bc4503feecb2` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 42.88999999983315 | 41.709999999834224 | 1.18 | 0.8578 | `r-74af15e68cf19cbae102` | `r-fc4a06e8bc4503feecb2` |
| h/1 | P05_long_step | last_isi | exceeds | 24.470000000534128 | 22.670000000494838 | 1.8 | 1.11 | `r-74af15e68cf19cbae102` | `r-fc4a06e8bc4503feecb2` |
| h/1 | P05_long_step | spike_count | exceeds | 83.0 | 90.0 | 7 | 3 | `r-74af15e68cf19cbae102` | `r-fc4a06e8bc4503feecb2` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 6. `m-scale_capacitance-8f1d58bf3d`

- **operator**: `scale_capacitance`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P04_step_2x;P05_long_step;P06_ramp;P09_short_pulse
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml` · `/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]` · **value**: `1.0 uF_per_cm2` → `0.5 uF_per_cm2`

**Diagnostic recorded by the campaign**

```
# m-scale_capacitance-8f1d58bf3d

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "0.5 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml", "locator": "/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "0.5 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 8012.994 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.5216693418942094 | 0.03544515455543932 | 0.486224 | 0.0521669 | `r-068a1eafd4afbbd6d23e` | `r-9c186180273349ccc400` |
| h/1 | P00_canonical | ahp_depth | exceeds | -8.248406196708032 | -14.57066472371455 | 6.32226 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-9c186180273349ccc400` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 74.70865440368996 | 96.1608352661301 | 21.4522 | 1.49417 | `r-068a1eafd4afbbd6d23e` | `r-9c186180273349ccc400` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 2.950000000000788 | 1.4000000000005457 | 1.55 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-9c186180273349ccc400` |
| h/1 | P00_canonical | last_isi | exceeds | 23.700000000004948 | 4.670000000002389 | 19.03 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-9c186180273349ccc400` |
| h/1 | P00_canonical | spike_count | exceeds | 4.0 | 6.0 | 2 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-9c186180273349ccc400` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -3.06435100805065 | -14.858714540973594 | 11.7944 | 1.14578 | `r-96e71f2e3b8549494d50` | `r-3088fe90902c2a8ab4e1` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 71.33246612267223 | 97.07684516484903 | 25.7444 | 1.42665 | `r-96e71f2e3b8549494d50` | `r-3088fe90902c2a8ab4e1` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 29.099999999845693 | 1.4299999998708586 | 27.67 | 0.582 | `r-96e71f2e3b8549494d50` | `r-3088fe90902c2a8ab4e1` |
| h/1 | P04_step_2x | spike_count | exceeds | 51.0 | 63.0 | 12 | 3 | `r-96e71f2e3b8549494d50` | `r-3088fe90902c2a8ab4e1` |
| h/1 | P05_long_step | ahp_depth | exceeds | -2.799466059340233 | -15.335879763290492 | 12.5364 | 1.17341 | `r-74af15e68cf19cbae102` | `r-d4540ff1ab10d4740fe7` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 7. `m-scale_conductance-056f6e95e6`

- **operator**: `scale_conductance`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P02_weak_step;P03_rheobase;P04_step_2x;P05_long_step;P06_ramp;P07_hyperpolarizing_step;P08_rebound;P09_short_pulse
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml` · `/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='hd_all']` · **condDensity**: `0.05 mS_per_cm2` → `0.1 mS_per_cm2`

**Diagnostic recorded by the campaign**

```
# m-scale_conductance-056f6e95e6

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='hd_all']", "new": "0.1 mS_per_cm2", "old": "0.05 mS_per_cm2"}], "element": "channelDensity", "element_id": "hd_all", "factor": 2.0, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='hd_all']", "attribute": "condDensity", "old": "0.05 mS_per_cm2", "new": "0.1 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1117.288 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | None | 2.134102529053085e-13 |  | inf | `r-1855c6a207dcec8ed210` | `r-966f5de15e3931bbd9fe` |
| h/1 | P00_canonical | ahp_depth | exceeds | -11.854831069263057 | -16.242066207809827 | 4.38724 | 0.592742 | `r-1855c6a207dcec8ed210` | `r-966f5de15e3931bbd9fe` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 5.420000000001174 | 2.720000000000752 | 2.7 | 0.5 | `r-1855c6a207dcec8ed210` | `r-966f5de15e3931bbd9fe` |
| h/1 | P00_canonical | last_isi | exceeds | 18.329999999996353 | 17.230000000003926 | 1.1 | 0.5 | `r-1855c6a207dcec8ed210` | `r-966f5de15e3931bbd9fe` |
| h/1 | P00_canonical | spike_count | exceeds | 3.0 | 4.0 | 1 | 0.5 | `r-1855c6a207dcec8ed210` | `r-966f5de15e3931bbd9fe` |
| h/1 | P02_weak_step | spike_count | exceeds | 0.0 | 11.0 | 11 | 0.5 | `r-0925b86f96a976919154` | `r-9d0fbecae44384747ef9` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -65.0228273132324 | -65.66653187537734 | 0.643705 | 0.5 | `r-0925b86f96a976919154` | `r-9d0fbecae44384747ef9` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.0 | 0.000580561 | 6.83013e-05 | `s-b1b4baffdde7651e5212` | `s-65fd674d2d18de2cb284` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -14.775756835937727 | -16.69309456624417 | 1.91734 | 0.738788 | `r-0925b86f96a976919154` | `r-9d0fbecae44384747ef9` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 16.069999999857544 | 16.89999999985679 | 0.83 | 0.5 | `r-0925b86f96a976919154` | `r-9d0fbecae44384747ef9` |
| h/1 | P04_step_2x | last_isi | exceeds | 40.059999999963566 | 29.469999999973197 | 10.59 | 0.8012 | `r-0925b86f96a976919154` | `r-9d0fbecae44384747ef9` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 8. `m-scale_conductance-2956a62118`

- **operator**: `scale_conductance`  ·  **family**: biophysical
- **assigned class**: `6_silent_under_canonical`
- **detected by**: P04_step_2x
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NMC/NeuroML2/Soma_AllNML2.cell.nml` · `/neuroml[@id='Soma_AllNML2']/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityNernst[@id='Ca_LVAst_all']` · **condDensity**: `3.43 mS_per_cm2` → `3.087 mS_per_cm2`

**Diagnostic recorded by the campaign**

```
# m-scale_conductance-2956a62118

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='Soma_AllNML2']/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityNernst[@id='Ca_LVAst_all']", "new": "3.087 mS_per_cm2", "old": "3.43 mS_per_cm2"}], "element": "channelDensityNernst", "element_id": "Ca_LVAst_all", "factor": 0.9, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NMC/NeuroML2/Soma_AllNML2.cell.nml", "locator": "/neuroml[@id='Soma_AllNML2']/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityNernst[@id='Ca_LVAst_all']", "attribute": "condDensity", "old": "3.43 mS_per_cm2", "new": "3.087 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 11953.381 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P04_step_2x | spike_count | exceeds | 30.0 | 29.0 | 1 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-5802429264cf80aefa9e` |
| h/2 | P04_step_2x | spike_count | exceeds | 30.0 | 29.0 | 1 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-a1a90cfa3b6cff5a7b78` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 9. `m-scale_conductance-c2b2371643`

- **operator**: `scale_conductance`  ·  **family**: biophysical
- **assigned class**: `6_silent_under_canonical`
- **detected by**: P04_step_2x;P05_long_step;P06_ramp
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml` · `/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='na3_all']` · **condDensity**: `25.0 mS_per_cm2` → `22.5 mS_per_cm2`

**Diagnostic recorded by the campaign**

```
# m-scale_conductance-c2b2371643

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='na3_all']", "new": "22.5 mS_per_cm2", "old": "25.0 mS_per_cm2"}], "element": "channelDensity", "element_id": "na3_all", "factor": 0.9, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='na3_all']", "attribute": "condDensity", "old": "25.0 mS_per_cm2", "new": "22.5 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 7375.718 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P04_step_2x | spike_count | exceeds | 13.0 | 12.0 | 1 | 0.5 | `r-0925b86f96a976919154` | `r-5666b4f7f44cf4c608b8` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 23.149999999851104 | 23.929999999850395 | 0.78 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-4f815599b9280eced4d6` |
| h/1 | P05_long_step | last_isi | exceeds | 51.510000001124354 | 52.6300000011488 | 1.12 | 1.0302 | `r-4ab59c3e1336e488abd6` | `r-4f815599b9280eced4d6` |
| h/1 | P05_long_step | spike_count | exceeds | 39.0 | 38.0 | 1 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-4f815599b9280eced4d6` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 396.20999999951187 | 406.99999999950205 | 10.79 | 7.9242 | `r-7e89f1dc706a0ef0fd1a` | `r-e5fb4d2947d42b0f02c7` |
| h/2 | P04_step_2x | spike_count | exceeds | 13.0 | 12.0 | 1 | 0.5 | `r-6797defd923ff2562240` | `r-529478d655694a3c7160` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 23.10999999985114 | 23.88999999985043 | 0.78 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-22d561bf6e3cac8168f7` |
| h/2 | P05_long_step | last_isi | exceeds | 51.560000001125445 | 52.68000000114989 | 1.12 | 1.0302 | `r-a3b84bbc3dc843d0e573` | `r-22d561bf6e3cac8168f7` |
| h/2 | P05_long_step | spike_count | exceeds | 39.0 | 38.0 | 1 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-22d561bf6e3cac8168f7` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 396.1499999995119 | 406.9399999995021 | 10.79 | 7.9242 | `r-8a56ade2f92e09dafdaf` | `r-c7a738357aa8a1920448` |

```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 10. `m-scale_conductance-c9ac5a125c`

- **operator**: `scale_conductance`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P02_weak_step;P03_rheobase;P04_step_2x;P05_long_step;P06_ramp;P07_hyperpolarizing_step;P09_short_pulse
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `neuroConstruct/generatedNeuroML2/TestSeg_test2.cell.nml` · `/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='ka_all']` · **condDensity**: `15.0 mS_per_cm2` → `7.5 mS_per_cm2`

**Diagnostic recorded by the campaign**

```
# m-scale_conductance-c9ac5a125c

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='ka_all']", "new": "7.5 mS_per_cm2", "old": "15.0 mS_per_cm2"}], "element": "channelDensity", "element_id": "ka_all", "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_test2.cell.nml", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='ka_all']", "attribute": "condDensity", "old": "15.0 mS_per_cm2", "new": "7.5 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4601.371 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -7.977452861728821 | -6.88505470693412 | 1.0924 | 0.5 | `r-a309e30f4eac6329447d` | `r-8383195efdf2bd1f1e62` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 76.03836822509587 | 80.32566833494114 | 4.2873 | 1.52077 | `r-a309e30f4eac6329447d` | `r-8383195efdf2bd1f1e62` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 2.9100000000007817 | 2.330000000000691 | 0.58 | 0.5 | `r-a309e30f4eac6329447d` | `r-8383195efdf2bd1f1e62` |
| h/1 | P00_canonical | last_isi | exceeds | 7.590000000003883 | 6.740000000003448 | 0.85 | 0.5 | `r-a309e30f4eac6329447d` | `r-8383195efdf2bd1f1e62` |
| h/1 | P00_canonical | spike_count | exceeds | 9.0 | 10.0 | 1 | 0.5 | `r-a309e30f4eac6329447d` | `r-8383195efdf2bd1f1e62` |
| h/1 | P02_weak_step | spike_count | exceeds | 0.0 | 2.0 | 2 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-1b0454bcf47d8bacfba4` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -63.11310723342887 | -59.61384217454062 | 3.49927 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-1b0454bcf47d8bacfba4` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.01710948705689502 | 0.007069189263028482 | 0.0100403 | 0.00034219 | `s-b9450aacc8ce67e5b927` | `s-26dc8b71a984b4cd102d` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -5.43348429870143 | -6.8190852063496905 | 1.3856 | 1.14528 | `r-531ed8bf9e8ec22d7778` | `r-1b0454bcf47d8bacfba4` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 53.72999999982329 | 21.859999999852278 | 31.87 | 1.0746 | `r-531ed8bf9e8ec22d7778` | `r-1b0454bcf47d8bacfba4` |
| h/1 | P04_step_2x | last_isi | exceeds | 25.62999999997669 | 15.79999999998563 | 9.83 | 1.29 | `r-531ed8bf9e8ec22d7778` | `r-1b0454bcf47d8bacfba4` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 11. `m-scale_gate_slope-039828a4db`

- **operator**: `scale_gate_slope`  ·  **family**: kinetics
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P04_step_2x;P05_long_step;P07_hyperpolarizing_step;P09_short_pulse
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NMC/NeuroML2/Ih.channel.nml` · `/neuroml[@id='Ih']/ionChannel[@id='Ih']/gate[@id='m']/forwardRate[1]` · **scale**: `-11.9mV` → `-9.52mV`
- `NMC/NeuroML2/Ih.channel.nml` · `/neuroml[@id='Ih']/ionChannel[@id='Ih']/gate[@id='m']/reverseRate[1]` · **scale**: `33.1mV` → `26.48mV`

**Diagnostic recorded by the campaign**

```
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
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 12. `m-scale_gate_time_constant-02eb4e0b90`

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

## 13. `m-scale_gate_time_constant-97ff619aea`

- **operator**: `scale_gate_time_constant`  ·  **family**: biophysical
- **assigned class**: `6_silent_under_canonical`
- **detected by**: P03_rheobase;P06_ramp
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/it.channel.nml` · `/neuroml[@id='it']/ionChannel[@id='it']/gate[@id='h']/q10Settings[1]` · **None**: `None` → `<q10Settings xmlns="http://www.neuroml.org/schema/neuroml2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" type="q10Fixed" fixedQ10="0.5"/>`

**Diagnostic recorded by the campaign**

```
# m-scale_gate_time_constant-97ff619aea

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"channel": "it", "factor": 0.5, "gate": "h", "generator_seed": 20260917, "mechanism": "q10_insert"}`
- recorded edits: `[{"file": "NeuroML2/it.channel.nml", "locator": "/neuroml[@id='it']/ionChannel[@id='it']/gate[@id='h']/q10Settings[1]", "attribute": null, "old": null, "new": "<q10Settings xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" type=\"q10Fixed\" fixedQ10=\"0.5\"/>", "action": "insert", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 5516.653 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.022368690663206067 | 0.000717164 | 0.000433031 | `s-d8858d31b993a1ff480b` | `s-24c5eae5e37ce68ba598` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 403.0899999995056 | 389.19999999951824 | 13.89 | 8.0618 | `r-fb29aefdef0f8e35dca0` | `r-38fa85c0261a860b13a2` |
| h/1 | P06_ramp | spike_count | exceeds | 35.0 | 36.0 | 1 | 0.5 | `r-fb29aefdef0f8e35dca0` | `r-38fa85c0261a860b13a2` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.022368690663206067 | 0.000717164 | 0.000433031 | `s-cfaadc06f539b47bcf96` | `s-aa66a7f31b3ce9cfb57e` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 403.0099999995057 | 389.1299999995183 | 13.88 | 8.0618 | `r-032d38f7b50aa7c6bdca` | `r-945f80b69f62599872e0` |
| h/2 | P06_ramp | spike_count | exceeds | 35.0 | 36.0 | 1 | 0.5 | `r-032d38f7b50aa7c6bdca` | `r-945f80b69f62599872e0` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 14. `m-shift_forward_rate_midpoint-3567e7da5d`

- **operator**: `shift_forward_rate_midpoint`  ·  **family**: kinetics
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P02_weak_step;P03_rheobase;P04_step_2x;P05_long_step;P06_ramp
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `neuroConstruct/generatedNeuroML2/cal.channel.nml` · `/neuroml[@id='cal']/ionChannel[@id='cal']/gate[@id='m']/forwardRate[1]` · **midpoint**: `5mV` → `10mV`

**Diagnostic recorded by the campaign**

```
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
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 15. `m-shift_gate_midpoint-0bf496636d`

- **operator**: `shift_gate_midpoint`  ·  **family**: kinetics
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P04_step_2x;P05_long_step;P06_ramp
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `neuroConstruct/generatedNeuroML2/km.channel.nml` · `/neuroml[@id='km']/ionChannel[@id='km']/gate[@id='m']/forwardRate[1]` · **midpoint**: `-20mV` → `-10mV`
- `neuroConstruct/generatedNeuroML2/km.channel.nml` · `/neuroml[@id='km']/ionChannel[@id='km']/gate[@id='m']/reverseRate[1]` · **midpoint**: `-43mV` → `-33mV`

**Diagnostic recorded by the campaign**

```
# m-shift_gate_midpoint-0bf496636d

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_gate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='km']/ionChannel[@id='km']/gate[@id='m']/forwardRate[1]", "new": "-10mV", "old": "-20mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='km']/ionChannel[@id='km']/gate[@id='m']/reverseRate[1]", "new": "-33mV", "old": "-43mV"}], "channel": "km", "delta_mV": 10.0, "gate": "m", "generator_seed": 20260917, "mechanism": "rates"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/km.channel.nml", "locator": "/neuroml[@id='km']/ionChannel[@id='km']/gate[@id='m']/forwardRate[1]", "attribute": "midpoint", "old": "-20mV", "new": "-10mV", "action": "set", "note": "shift_gate_midpoint"}, {"file": "neuroConstruct/generatedNeuroML2/km.channel.nml", "locator": "/neuroml[@id='km']/ionChannel[@id='km']/gate[@id='m']/reverseRate[1]", "attribute": "midpoint", "old": "-43mV", "new": "-33mV", "action": "set", "note": "shift_gate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4577.422 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.017936897992228234 | 0.003829550021039614 | 0.0141073 | 0.01 | `r-a309e30f4eac6329447d` | `r-7da34e325896436ec767` |
| h/1 | P00_canonical | last_isi | exceeds | 7.590000000003883 | 6.130000000003136 | 1.46 | 0.5 | `r-a309e30f4eac6329447d` | `r-7da34e325896436ec767` |
| h/1 | P00_canonical | spike_count | exceeds | 9.0 | 10.0 | 1 | 0.5 | `r-a309e30f4eac6329447d` | `r-7da34e325896436ec767` |
| h/1 | P04_step_2x | adaptation_index | exceeds | 0.004861353302673796 | -0.01131672312993306 | 0.0161781 | 0.01 | `r-531ed8bf9e8ec22d7778` | `r-e3d9e11af34e87ec95a9` |
| h/1 | P04_step_2x | last_isi | exceeds | 25.62999999997669 | 12.129999999988968 | 13.5 | 1.29 | `r-531ed8bf9e8ec22d7778` | `r-e3d9e11af34e87ec95a9` |
| h/1 | P04_step_2x | spike_count | exceeds | 18.0 | 28.0 | 10 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-e3d9e11af34e87ec95a9` |
| h/1 | P05_long_step | last_isi | exceeds | 46.560000001016306 | 27.700000000604632 | 18.86 | 2.61 | `r-c181d8dc3f2e9e1a86cf` | `r-889219cf337d75647944` |
| h/1 | P05_long_step | spike_count | exceeds | 42.0 | 70.0 | 28 | 3 | `r-c181d8dc3f2e9e1a86cf` | `r-889219cf337d75647944` |
| h/1 | P06_ramp | spike_count | exceeds | 27.0 | 41.0 | 14 | 3 | `r-8c44150a9a017555d35c` | `r-c38f4045b1daaf185580` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.018020148454594893 | 0.004069014951416039 | 0.0139511 | 0.01 | `r-82914471c1c753634231` | `r-b7ea2c237da7ffe9401b` |
| h/2 | P00_canonical | last_isi | exceeds | 7.610000000003893 | 6.140000000003141 | 1.47 | 0.5 | `r-82914471c1c753634231` | `r-b7ea2c237da7ffe9401b` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 16. `m-shift_gate_midpoint-f1b7d12414`

- **operator**: `shift_gate_midpoint`  ·  **family**: kinetics
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P02_weak_step;P03_rheobase;P04_step_2x;P05_long_step;P06_ramp;P09_short_pulse
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `neuroConstruct/generatedNeuroML2/nax.channel.nml` · `/neuroml[@id='nax']/ionChannel[@id='nax']/gate[@id='m']/forwardRate[1]` · **midpoint**: `-30mV` → `-20mV`
- `neuroConstruct/generatedNeuroML2/nax.channel.nml` · `/neuroml[@id='nax']/ionChannel[@id='nax']/gate[@id='m']/reverseRate[1]` · **midpoint**: `-30mV` → `-20mV`

**Diagnostic recorded by the campaign**

```
# m-shift_gate_midpoint-f1b7d12414

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_gate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='nax']/ionChannel[@id='nax']/gate[@id='m']/forwardRate[1]", "new": "-20mV", "old": "-30mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='nax']/ionChannel[@id='nax']/gate[@id='m']/reverseRate[1]", "new": "-20mV", "old": "-30mV"}], "channel": "nax", "delta_mV": 10.0, "gate": "m", "generator_seed": 20260917, "mechanism": "rates"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/nax.channel.nml", "locator": "/neuroml[@id='nax']/ionChannel[@id='nax']/gate[@id='m']/forwardRate[1]", "attribute": "midpoint", "old": "-30mV", "new": "-20mV", "action": "set", "note": "shift_gate_midpoint"}, {"file": "neuroConstruct/generatedNeuroML2/nax.channel.nml", "locator": "/neuroml[@id='nax']/ionChannel[@id='nax']/gate[@id='m']/reverseRate[1]", "attribute": "midpoint", "old": "-30mV", "new": "-20mV", "action": "set", "note": "shift_gate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 3088.009 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.14028549194009 | 93.24039840693817 | 6.89989 | 2.00281 | `r-1855c6a207dcec8ed210` | `r-16e89293d0d6edc7c678` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 5.420000000001174 | 15.440000000001518 | 10.02 | 0.5 | `r-1855c6a207dcec8ed210` | `r-16e89293d0d6edc7c678` |
| h/1 | P00_canonical | last_isi | exceeds | 18.329999999996353 | 30.159999999995136 | 11.83 | 0.5 | `r-1855c6a207dcec8ed210` | `r-16e89293d0d6edc7c678` |
| h/1 | P00_canonical | spike_count | exceeds | 3.0 | 2.0 | 1 | 0.5 | `r-1855c6a207dcec8ed210` | `r-16e89293d0d6edc7c678` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -65.0228273132324 | -65.98750321502683 | 0.964676 | 0.5 | `r-0925b86f96a976919154` | `r-1d3b15547e02626f091f` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.002732053821460283 | 0.00215149 | 6.83013e-05 | `s-b1b4baffdde7651e5212` | `s-cd80646e6e55af2bd523` |
| h/1 | P04_step_2x | adaptation_index | definedness | 1.2482836100362002e-05 | None |  | 0.01 | `r-0925b86f96a976919154` | `r-1d3b15547e02626f091f` |
| h/1 | P04_step_2x | ahp_depth | definedness | -14.775756835937727 | None |  | 0.738788 | `r-0925b86f96a976919154` | `r-1d3b15547e02626f091f` |
| h/1 | P04_step_2x | ap_amplitude | definedness | 100.46828841971717 | None |  | 2.00937 | `r-0925b86f96a976919154` | `r-1d3b15547e02626f091f` |
| h/1 | P04_step_2x | first_spike_latency | definedness | 16.069999999857544 | None |  | 0.5 | `r-0925b86f96a976919154` | `r-1d3b15547e02626f091f` |
| h/1 | P04_step_2x | last_isi | definedness | 40.059999999963566 | None |  | 0.8012 | `r-0925b86f96a976919154` | `r-1d3b15547e02626f091f` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 17. `m-shift_reversal-293fd11ac3`

- **operator**: `shift_reversal`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P05_long_step
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml` · `/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nap_all']` · **erev**: `50.0 mV` → `45.0 mV`

**Diagnostic recorded by the campaign**

```
# m-shift_reversal-293fd11ac3

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nap_all']", "new": "45.0 mV", "old": "50.0 mV"}], "element": "channelDensity", "element_id": "nap_all", "generator_seed": 20260917, "shift_mV": -5.0}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml", "locator": "/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nap_all']", "attribute": "erev", "old": "50.0 mV", "new": "45.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 8012.079 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | 0.5216693418942094 | None |  | 0.0521669 | `r-068a1eafd4afbbd6d23e` | `r-36051761fd8522397121` |
| h/1 | P00_canonical | last_isi | exceeds | 23.700000000004948 | 7.609999999998486 | 16.09 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-36051761fd8522397121` |
| h/1 | P00_canonical | spike_count | exceeds | 4.0 | 3.0 | 1 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-36051761fd8522397121` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 42.88999999983315 | 43.829999999832296 | 0.94 | 0.8578 | `r-74af15e68cf19cbae102` | `r-362a3084e57b5edd6775` |
| h/2 | P00_canonical | adaptation_index | definedness | 0.5214881334190068 | None |  | 0.0521669 | `r-87bcc3cd30685deaf603` | `r-b6398ef2ed6c77615e09` |
| h/2 | P00_canonical | last_isi | exceeds | 23.72000000000496 | 7.609999999998486 | 16.11 | 0.5 | `r-87bcc3cd30685deaf603` | `r-b6398ef2ed6c77615e09` |
| h/2 | P00_canonical | spike_count | exceeds | 4.0 | 3.0 | 1 | 0.5 | `r-87bcc3cd30685deaf603` | `r-b6398ef2ed6c77615e09` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 42.819999999833215 | 43.75999999983236 | 0.94 | 0.8578 | `r-f1a8b6a7a66c54d9b827` | `r-752a498a9b92ab039a0b` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 18. `m-solver_config-c16c7918b3`

- **operator**: `solver_config`  ·  **family**: numerical
- **assigned class**: `4_equivalent_within_tested_domain`
- **detected by**: nothing
- **structurally valid**: True  ·  **execution overrides**: {"integrator_method": "eulertree"}

**The edit**

- `NMC/NeuroML2/LEMS_Soma_AllNML2.xml` · `/Lems[1]/Component[@id='sim1']/Meta[1]` · **None**: `None` → `<Meta xmlns="http://www.neuroml.org/lems/0.7.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" for="jlems" method="eulertree"/>`

**Diagnostic recorded by the campaign**

```
# m-solver_config-c16c7918b3

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: numerical_robustness
- kind/family/operator: mutant / numerical / solver_config
- parameters: `{"generator_seed": 20260917, "mechanism": "insert_meta", "method": "eulertree"}`
- recorded edits: `[{"file": "NMC/NeuroML2/LEMS_Soma_AllNML2.xml", "locator": "/Lems[1]/Component[@id='sim1']/Meta[1]", "attribute": null, "old": null, "new": "<Meta xmlns=\"http://www.neuroml.org/lems/0.7.2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" for=\"jlems\" method=\"eulertree\"/>", "action": "insert", "note": "solver_config"}]`
- execution overrides: `{"integrator_method": "eulertree"}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 12210.975 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 19. `m-wrong_channel-36578b9f51`

- **operator**: `wrong_channel`  ·  **family**: reference
- **assigned class**: `2_non_executable`
- **detected by**: nothing
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml` · `/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityNernst[@id='Ca_LVAst_all']` · **ionChannel**: `Ca_LVAst` → `pas`

**Diagnostic recorded by the campaign**

```
# m-wrong_channel-36578b9f51

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / wrong_channel
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityNernst[@id='Ca_LVAst_all']", "new": "pas", "old": "Ca_LVAst"}], "element_id": "Ca_LVAst_all", "generator_seed": 20260917, "new_species": "non_specific", "old_species": "ca"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityNernst[@id='Ca_LVAst_all']", "attribute": "ionChannel", "old": "Ca_LVAst", "new": "pas", "action": "set", "note": "wrong_channel"}]`
- execution overrides: `{}`
- class: **2_non_executable**
- nominal-level status: build_error; runtime 1552.856 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 20. `m-wrong_compatible_component-0638e400a0`

- **operator**: `wrong_compatible_component`  ·  **family**: reference
- **assigned class**: `3_numerically_unstable`
- **detected by**: nothing
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml` · `/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kdr_all']` · **ionChannel**: `kdr` → `kap`

**Diagnostic recorded by the campaign**

```
# m-wrong_compatible_component-0638e400a0

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / wrong_compatible_component
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kdr_all']", "new": "kap", "old": "kdr"}], "element_id": "kdr_all", "generator_seed": 20260917, "new_species": "k", "old_species": "k"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kdr_all']", "attribute": "ionChannel", "old": "kdr", "new": "kap", "action": "set", "note": "wrong_compatible_component"}]`
- execution overrides: `{}`
- class: **3_numerically_unstable**
- nominal-level status: numerically_unstable; runtime 1481.42 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---
