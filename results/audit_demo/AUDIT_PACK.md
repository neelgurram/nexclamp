# Audit pack: campaign `pilot`

*20 of 52 mutants, sampled with seed 20260913 so the selection is reproducible. Generated 2026-09-19T00:03:33+00:00 at commit `a2313356740177c3833f552df49b382c7340828b` (tree dirty: False).*

## How to audit

For each mutant below, three questions. They take a minute each once you have the model file open.

1. **Does the edit match its label?** The operator name claims a specific kind of change (a conductance scaled, a reversal potential shifted, a channel reference broken). Read the old → new values and say whether that is what happened.
2. **Is the assigned class plausible?** `5_non_equivalent` means the behaviour changed reproducibly; `4_equivalent_within_tested_domain` means it did not; `2_non_executable` means the model would not run. Does that match the diagnostic?
3. **Is the detection plausible?** If protocols are listed as detecting it, does the diagnostic show a difference big enough to believe?

Record your answers in `AUDIT_SHEET.csv`. **Disagreement is the useful output** - if an edit looks mislabelled or a class looks wrong, say so; that is what the audit is for.

---

## 1. `m-duplicate_conductance-e09481d53c`

- **operator**: `duplicate_conductance`  ·  **family**: reference
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P04_step_2x;P05_long_step
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/cells/LTS/LTS.cell.nml` · `/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all_dup']` · **None**: `None` → `<channelDensity xmlns="http://www.neuroml.org/schema/neuroml2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" condDensity="0.005 S_per_cm2" id="Kd_all_dup" ionChannel="Kd" ion="k" erev="-100.0 mV"/>`

**Diagnostic recorded by the campaign**

```
# m-duplicate_conductance-e09481d53c

- model: `pospischil2008_lts`
- kind/family/operator: mutant / reference / duplicate_conductance
- parameters: `{"generator_seed": 20260913, "new_id": "Kd_all_dup", "source_id": "Kd_all"}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LTS.cell.nml", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all_dup']", "attribute": null, "old": null, "new": "<channelDensity xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" condDensity=\"0.005 S_per_cm2\" id=\"Kd_all_dup\" ionChannel=\"Kd\" ion=\"k\" erev=\"-100.0 mV\"/>", "action": "insert", "note": "duplicate_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1614.421 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.45003406360930803 | 0.10673969458726523 | 0.343294 | 0.0450034 | `r-7fe8302f56856b53d535` | `r-a51c908837fe9f2a76ef` |
| h/1 | P00_canonical | ahp_depth | exceeds | 16.573501743312846 | 7.096504367830278 | 9.477 | 0.828675 | `r-7fe8302f56856b53d535` | `r-a51c908837fe9f2a76ef` |
| h/1 | P00_canonical | ap_half_width | exceeds | 0.7799999999992906 | 0.629999999999427 | 0.15 | 0.05 | `r-7fe8302f56856b53d535` | `r-a51c908837fe9f2a76ef` |
| h/1 | P00_canonical | first_isi | exceeds | 14.159999999987122 | 36.059999999967204 | 21.9 | 0.6 | `r-7fe8302f56856b53d535` | `r-a51c908837fe9f2a76ef` |
| h/1 | P00_canonical | last_isi | exceeds | 202.1999999998161 | 120.09999999989077 | 82.1 | 4.044 | `r-7fe8302f56856b53d535` | `r-a51c908837fe9f2a76ef` |
| h/1 | P00_canonical | mean_frequency | exceeds | 12.319822594574143 | 13.337601365790292 | 1.01778 | 0.615991 | `r-7fe8302f56856b53d535` | `r-a51c908837fe9f2a76ef` |
| h/1 | P00_canonical | spike_count | exceeds | 4.0 | 5.0 | 1 | 0.5 | `r-7fe8302f56856b53d535` | `r-a51c908837fe9f2a76ef` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 14.597407663981116 | 5.78886731974255 | 8.80854 | 1.3737 | `r-c8dafa7919f8741d136a` | `r-5cc710c096466537cd1f` |
| h/1 | P04_step_2x | ap_half_width | exceeds | 0.7299999999993361 | 0.5899999999994634 | 0.14 | 0.05 | `r-c8dafa7919f8741d136a` | `r-5cc710c096466537cd1f` |
| h/1 | P05_long_step | ahp_depth | exceeds | 14.078013743082678 | 5.581637705485022 | 8.49638 | 1.31907 | `r-0e47469602e57d8257f5` | `r-351b3f0b3a3884d6b072` |
| h/1 | P05_long_step | ap_half_width | exceeds | 0.7199999999993452 | 0.5799999999994725 | 0.14 | 0.05 | `r-0e47469602e57d8257f5` | `r-351b3f0b3a3884d6b072` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.4630010462892806 | 0.10773920221562774 | 0.355262 | 0.0450034 | `r-055cc6b1739501cecd9d` | `r-ca85caa3c394414f4151` |
| h/2 | P00_canonical | ahp_depth | exceeds | 16.673553569797534 | 7.198928936004663 | 9.47462 | 0.828675 | `r-055cc6b1739501cecd9d` | `r-ca85caa3c394414f4151` |
| h/2 | P00_canonical | ap_half_width | exceeds | 0.7799999999992906 | 0.629999999999427 | 0.15 | 0.05 | `r-055cc6b1739501cecd9d` | `r-ca85caa3c394414f4151` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 2. `m-increase_dt-b7cdfa6b5c`

- **operator**: `increase_dt`  ·  **family**: numerical
- **assigned class**: `6_silent_under_canonical`
- **detected by**: P04_step_2x;P05_long_step
- **structurally valid**: True  ·  **execution overrides**: {"dt_factor": 4}

**The edit**

- `NeuroML2/cells/RS/LEMS_RS.xml` · `/Lems[1]/Component[@id='sim1']` · **step**: `0.001ms` → `0.004ms`

**Diagnostic recorded by the campaign**

```
# m-increase_dt-b7cdfa6b5c

- model: `pospischil2008_rs`
- kind/family/operator: mutant / numerical / increase_dt
- parameters: `{"changes": [{"attribute": "step", "locator": "/Lems[1]/Component[@id='sim1']", "new": "0.004ms", "old": "0.001ms"}], "factor": 4, "generator_seed": 20260913}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/LEMS_RS.xml", "locator": "/Lems[1]/Component[@id='sim1']", "attribute": "step", "old": "0.001ms", "new": "0.004ms", "action": "set", "note": "increase_dt"}]`
- execution overrides: `{"dt_factor": 4}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 467.741 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P04_step_2x | ahp_depth | exceeds | 3.2025415878387236 | 0.6488381869395425 | 2.5537 | 1.22099 | `r-0c0f3a761516cf334965` | `r-605ee5761cd35be1936f` |
| h/1 | P04_step_2x | first_isi | exceeds | 13.069999999988113 | 13.91999999998734 | 0.85 | 0.5 | `r-0c0f3a761516cf334965` | `r-605ee5761cd35be1936f` |
| h/1 | P04_step_2x | spike_count | exceeds | 22.0 | 21.0 | 1 | 0.5 | `r-0c0f3a761516cf334965` | `r-605ee5761cd35be1936f` |
| h/1 | P05_long_step | ahp_depth | exceeds | 2.4773294906594145 | -0.03440255861407593 | 2.51173 | 1.19998 | `r-6299bd8dadd5e9592d63` | `r-c20358157b324799821e` |
| h/1 | P05_long_step | first_isi | exceeds | 21.2199999999807 | 22.41999999997961 | 1.2 | 0.6 | `r-6299bd8dadd5e9592d63` | `r-c20358157b324799821e` |
| h/1 | P05_long_step | spike_count | exceeds | 29.0 | 28.0 | 1 | 0.5 | `r-6299bd8dadd5e9592d63` | `r-c20358157b324799821e` |
| h/1 | P06_ramp | spike_count | exceeds | 30.0 | 29.0 | 1 | 0.5 | `r-7054f91d1e6b5f4b29f8` | `r-45c205d76e09d28f04f5` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -1.4308354873657265 | -2.928793229418318 | 1.49796 | 0.5 | `r-4a031cb8037cbebd46bc` | `r-b3fc83e42bd3fe8c4296` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | 119.13114547927412 | None |  | 2.38262 | `r-4a031cb8037cbebd46bc` | `r-b3fc83e42bd3fe8c4296` |
| h/1 | P09_short_pulse | ap_half_width | definedness | 0.8799999999991996 | None |  | 0.05 | `r-4a031cb8037cbebd46bc` | `r-b3fc83e42bd3fe8c4296` |
| h/1 | P10_paired_pulses | ap_amplitude | definedness | 119.13114547927412 | None |  | 2.38262 | `r-4a031cb8037cbebd46bc` | `r-b3fc83e42bd3fe8c4296` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 3.6095391972804407 | 2.3726109263133566 | 1.23693 | 1.22099 | `r-13ae588754662eb409bf` | `r-17ce2b6d2b90076cf023` |
| h/2 | P04_step_2x | spike_count | exceeds | 22.0 | 21.0 | 1 | 0.5 | `r-13ae588754662eb409bf` | `r-17ce2b6d2b90076cf023` |
| h/2 | P05_long_step | ahp_depth | exceeds | 2.8773233159343334 | 1.6613867390951782 | 1.21594 | 1.19998 | `r-a71c890435a70aeaf61b` | `r-07f5989b6d2f1bfe2c76` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 3. `m-omit_include-0307bc9abe`

- **operator**: `omit_include`  ·  **family**: reference
- **assigned class**: `1_structurally_invalid`
- **detected by**: nothing
- **structurally valid**: False  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/cells/LTS/LTS.cell.nml` · `/neuroml[@id='LTS']/include[5]` · **None**: `<include xmlns="http://www.neuroml.org/schema/neuroml2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" href="../../channels/IT/IT.channel.nml"/>` → `None`

*No diagnostic file for this variant.*

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 4. `m-omit_include-1e5a6df120`

- **operator**: `omit_include`  ·  **family**: reference
- **assigned class**: `1_structurally_invalid`
- **detected by**: nothing
- **structurally valid**: False  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/cells/RS/RS.cell.nml` · `/neuroml[@id='RS']/include[3]` · **None**: `<include xmlns="http://www.neuroml.org/schema/neuroml2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" href="../../channels/Leak/Leak.channel.nml"/>` → `None`

*No diagnostic file for this variant.*

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 5. `m-omit_include-323831e37a`

- **operator**: `omit_include`  ·  **family**: reference
- **assigned class**: `2_non_executable`
- **detected by**: nothing
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/cells/RS/RS.cell.nml` · `/neuroml[@id='RS']/include[4]` · **None**: `<include xmlns="http://www.neuroml.org/schema/neuroml2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" href="../../channels/Na/Na.channel.nml"/>` → `None`

**Diagnostic recorded by the campaign**

```
# m-omit_include-323831e37a

- model: `pospischil2008_rs`
- kind/family/operator: mutant / reference / omit_include
- parameters: `{"generator_seed": 20260913, "href": "../../channels/Na/Na.channel.nml", "removed": "<include xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" href=\"../../channels/Na/Na.channel.nml\"/>"}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/include[4]", "attribute": null, "old": "<include xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" href=\"../../channels/Na/Na.channel.nml\"/>", "new": null, "action": "remove", "note": "omit_include"}]`
- execution overrides: `{}`
- class: **2_non_executable**
- nominal-level status: build_error; runtime 48.259 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 6. `m-recording_resolution-46bcb819ee`

- **operator**: `recording_resolution`  ·  **family**: numerical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical
- **structurally valid**: True  ·  **execution overrides**: {"sample_every_ms": 0.25}

**The edit**

- no edit recorded

**Diagnostic recorded by the campaign**

```
# m-recording_resolution-46bcb819ee

- model: `pospischil2008_lts`
- kind/family/operator: mutant / numerical / recording_resolution
- parameters: `{"generator_seed": 20260913, "sample_every_ms": 0.25}`
- recorded edits: `[]`
- execution overrides: `{"sample_every_ms": 0.25}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1598.175 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.01163101444587 | 97.15863402358048 | 2.853 | 2.00023 | `r-7fe8302f56856b53d535` | `r-0553a9c85faf2a4d3b3a` |
| h/1 | P00_canonical | ap_half_width | exceeds | 0.7799999999992906 | 0.8499999999992269 | 0.07 | 0.05 | `r-7fe8302f56856b53d535` | `r-0553a9c85faf2a4d3b3a` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 99.9338417077712 | 96.62106215859443 | 3.31278 | 2.00023 | `r-055cc6b1739501cecd9d` | `r-30419fb2699d680a303a` |
| h/2 | P00_canonical | ap_half_width | exceeds | 0.7799999999992906 | 0.8599999999992178 | 0.08 | 0.05 | `r-055cc6b1739501cecd9d` | `r-30419fb2699d680a303a` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 7. `m-recording_resolution-7d6e4357af`

- **operator**: `recording_resolution`  ·  **family**: numerical
- **assigned class**: `6_silent_under_canonical`
- **detected by**: P05_long_step;P09_short_pulse
- **structurally valid**: True  ·  **execution overrides**: {"sample_every_ms": 0.25}

**The edit**

- no edit recorded

**Diagnostic recorded by the campaign**

```
# m-recording_resolution-7d6e4357af

- model: `pospischil2008_rs`
- kind/family/operator: mutant / numerical / recording_resolution
- parameters: `{"generator_seed": 20260913, "sample_every_ms": 0.25}`
- recorded edits: `[]`
- execution overrides: `{"sample_every_ms": 0.25}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 1449.85 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P05_long_step | ap_amplitude | exceeds | 89.18265915023935 | 84.4117355294313 | 4.77092 | 1.78365 | `r-6299bd8dadd5e9592d63` | `r-23a42b89179af0150565` |
| h/1 | P05_long_step | ap_half_width | exceeds | 0.6999999999993634 | 0.7799999999992906 | 0.08 | 0.05 | `r-6299bd8dadd5e9592d63` | `r-23a42b89179af0150565` |
| h/1 | P09_short_pulse | ap_half_width | exceeds | 0.8799999999991996 | 0.9699999999991178 | 0.09 | 0.05 | `r-4a031cb8037cbebd46bc` | `r-69682a360336c0b1303a` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 89.44855880885186 | 86.93050001503505 | 2.51806 | 1.78992 | `r-13ae588754662eb409bf` | `r-996e9431f4326b1dbc4c` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 89.08078384555085 | 82.36533351582165 | 6.71545 | 1.78365 | `r-a71c890435a70aeaf61b` | `r-db007c32dac81a51cd9e` |
| h/2 | P05_long_step | ap_half_width | exceeds | 0.6999999999993634 | 0.7699999999992997 | 0.07 | 0.05 | `r-a71c890435a70aeaf61b` | `r-db007c32dac81a51cd9e` |
| h/2 | P09_short_pulse | ap_half_width | exceeds | 0.8799999999991996 | 0.9799999999991087 | 0.1 | 0.05 | `r-fa41d650658e23c878d5` | `r-7be5f11eae92d24f09ae` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 8. `m-recording_resolution-7d86fbc601`

- **operator**: `recording_resolution`  ·  **family**: numerical
- **assigned class**: `4_equivalent_within_tested_domain`
- **detected by**: nothing
- **structurally valid**: True  ·  **execution overrides**: {"sample_every_ms": 0.05}

**The edit**

- no edit recorded

**Diagnostic recorded by the campaign**

```
# m-recording_resolution-7d86fbc601

- model: `pospischil2008_lts`
- kind/family/operator: mutant / numerical / recording_resolution
- parameters: `{"generator_seed": 20260913, "sample_every_ms": 0.05}`
- recorded edits: `[]`
- execution overrides: `{"sample_every_ms": 0.05}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 704.892 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 9. `m-scale_conductance-56da844943`

- **operator**: `scale_conductance`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P03_rheobase;P04_step_2x;P05_long_step;P06_ramp
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/cells/RS/RS.cell.nml` · `/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all']` · **condDensity**: `0.07 mS_per_cm2` → `0.0875 mS_per_cm2`

**Diagnostic recorded by the campaign**

```
# m-scale_conductance-56da844943

- model: `pospischil2008_rs`
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all']", "new": "0.0875 mS_per_cm2", "old": "0.07 mS_per_cm2"}], "element": "channelDensity", "element_id": "IM_all", "factor": 1.25, "generator_seed": 20260913}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all']", "attribute": "condDensity", "old": "0.07 mS_per_cm2", "new": "0.0875 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1661.494 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.2988218828985024 | 0.5961483092869254 | 0.297326 | 0.0298822 | `r-5171ec6a0414fa8c47f8` | `r-9ac73645c86e12ac0949` |
| h/1 | P00_canonical | first_isi | exceeds | 28.06999999997447 | 31.659999999971205 | 3.59 | 0.5614 | `r-5171ec6a0414fa8c47f8` | `r-9ac73645c86e12ac0949` |
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 249.46999999977317 | 113.49 | 2.7196 | `r-5171ec6a0414fa8c47f8` | `r-9ac73645c86e12ac0949` |
| h/1 | P00_canonical | mean_frequency | exceeds | 17.03113291098414 | 10.944511327583005 | 6.08662 | 0.851557 | `r-5171ec6a0414fa8c47f8` | `r-9ac73645c86e12ac0949` |
| h/1 | P00_canonical | spike_count | exceeds | 5.0 | 4.0 | 1 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-9ac73645c86e12ac0949` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.5606515948364182 | 0.5721262208865514 | 0.0114746 | 0.011213 | `s-e75f45f43aa09d678807` | `s-b1a5762bba50d52a479f` |
| h/1 | P04_step_2x | adaptation_index | exceeds | 0.018020491828063687 | 0.03280420790877508 | 0.0147837 | 0.01 | `r-0c0f3a761516cf334965` | `r-fd20409f762963c4c12e` |
| h/1 | P04_step_2x | last_isi | exceeds | 28.16999999997438 | 37.78999999996563 | 9.62 | 0.5634 | `r-0c0f3a761516cf334965` | `r-fd20409f762963c4c12e` |
| h/1 | P04_step_2x | mean_frequency | exceeds | 44.11292909854356 | 36.36441421211172 | 7.74851 | 2.20565 | `r-0c0f3a761516cf334965` | `r-fd20409f762963c4c12e` |
| h/1 | P04_step_2x | spike_count | exceeds | 22.0 | 17.0 | 5 | 0.5 | `r-0c0f3a761516cf334965` | `r-fd20409f762963c4c12e` |
| h/1 | P05_long_step | adaptation_index | exceeds | 0.02130270892949869 | 0.04297364534361711 | 0.0216709 | 0.01 | `r-6299bd8dadd5e9592d63` | `r-738317bd97eedc831da7` |
| h/1 | P05_long_step | first_isi | exceeds | 21.2199999999807 | 22.7599999999793 | 1.54 | 0.6 | `r-6299bd8dadd5e9592d63` | `r-738317bd97eedc831da7` |
| h/1 | P05_long_step | last_isi | exceeds | 78.13000000170541 | 123.58000000269749 | 45.45 | 1.5626 | `r-6299bd8dadd5e9592d63` | `r-738317bd97eedc831da7` |
| h/1 | P05_long_step | mean_frequency | exceeds | 14.694109182274286 | 9.852370013522695 | 4.84174 | 0.734705 | `r-6299bd8dadd5e9592d63` | `r-738317bd97eedc831da7` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 10. `m-scale_conductance-fa05b19484`

- **operator**: `scale_conductance`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P05_long_step
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/cells/RS/RS.cell.nml` · `/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityVShift[@id='Na_all']` · **condDensity**: `50.0 mS_per_cm2` → `45.0 mS_per_cm2`

**Diagnostic recorded by the campaign**

```
# m-scale_conductance-fa05b19484

- model: `pospischil2008_rs`
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityVShift[@id='Na_all']", "new": "45.0 mS_per_cm2", "old": "50.0 mS_per_cm2"}], "element": "channelDensityVShift", "element_id": "Na_all", "factor": 0.9, "generator_seed": 20260913}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityVShift[@id='Na_all']", "attribute": "condDensity", "old": "50.0 mS_per_cm2", "new": "45.0 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1662.956 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 145.27999999986793 | 9.3 | 2.7196 | `r-5171ec6a0414fa8c47f8` | `r-dac995eb6d373954ec3d` |
| h/1 | P05_long_step | last_isi | exceeds | 78.13000000170541 | 79.88000000174361 | 1.75 | 1.5626 | `r-6299bd8dadd5e9592d63` | `r-a4cf886c8333383bda2f` |
| h/1 | P05_long_step | spike_count | exceeds | 29.0 | 28.0 | 1 | 0.5 | `r-6299bd8dadd5e9592d63` | `r-a4cf886c8333383bda2f` |
| h/2 | P00_canonical | last_isi | exceeds | 135.78999999987656 | 145.02999999986815 | 9.24 | 2.7196 | `r-35d4f8d415fe0d06a895` | `r-5246dce83f2b61542ac0` |
| h/2 | P05_long_step | last_isi | exceeds | 77.97000000170192 | 79.69000000173946 | 1.72 | 1.5626 | `r-a71c890435a70aeaf61b` | `r-bbae3c10fed62c22ba3b` |
| h/2 | P05_long_step | spike_count | exceeds | 29.0 | 28.0 | 1 | 0.5 | `r-a71c890435a70aeaf61b` | `r-bbae3c10fed62c22ba3b` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 11. `m-scale_gate_time_constant-244443ee5f`

- **operator**: `scale_gate_time_constant`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P04_step_2x;P05_long_step;P06_ramp;P09_short_pulse
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/channels/Na/Na.channel.nml` · `/neuroml[@id='Na']/ionChannel[@id='Na']/gate[@id='h']/q10Settings[1]` · **None**: `None` → `<q10Settings xmlns="http://www.neuroml.org/schema/neuroml2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" type="q10Fixed" fixedQ10="1.25"/>`

**Diagnostic recorded by the campaign**

```
# m-scale_gate_time_constant-244443ee5f

- model: `pospischil2008_rs`
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"channel": "Na", "factor": 1.25, "gate": "h", "generator_seed": 20260913, "mechanism": "q10_insert"}`
- recorded edits: `[{"file": "NeuroML2/channels/Na/Na.channel.nml", "locator": "/neuroml[@id='Na']/ionChannel[@id='Na']/gate[@id='h']/q10Settings[1]", "attribute": null, "old": null, "new": "<q10Settings xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" type=\"q10Fixed\" fixedQ10=\"1.25\"/>", "action": "insert", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1703.864 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.2988218828985024 | 0.22322672820662412 | 0.0755952 | 0.0298822 | `r-5171ec6a0414fa8c47f8` | `r-7dbd1fc334c0e6a4a023` |
| h/1 | P00_canonical | ahp_depth | exceeds | 2.861194747922525 | 3.9489938201904238 | 1.0878 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-7dbd1fc334c0e6a4a023` |
| h/1 | P00_canonical | first_isi | exceeds | 28.06999999997447 | 26.74999999997567 | 1.32 | 0.5614 | `r-5171ec6a0414fa8c47f8` | `r-7dbd1fc334c0e6a4a023` |
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 141.37999999987142 | 5.4 | 2.7196 | `r-5171ec6a0414fa8c47f8` | `r-7dbd1fc334c0e6a4a023` |
| h/1 | P00_canonical | mean_frequency | exceeds | 17.03113291098414 | 15.59900166391288 | 1.43213 | 0.851557 | `r-5171ec6a0414fa8c47f8` | `r-7dbd1fc334c0e6a4a023` |
| h/1 | P00_canonical | spike_count | exceeds | 5.0 | 6.0 | 1 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-7dbd1fc334c0e6a4a023` |
| h/1 | P04_step_2x | last_isi | exceeds | 28.16999999997438 | 26.669999999975744 | 1.5 | 0.5634 | `r-0c0f3a761516cf334965` | `r-c93a95647e79ab528cf4` |
| h/1 | P04_step_2x | mean_frequency | exceeds | 44.11292909854356 | 46.51350914097004 | 2.40058 | 2.20565 | `r-0c0f3a761516cf334965` | `r-c93a95647e79ab528cf4` |
| h/1 | P04_step_2x | spike_count | exceeds | 22.0 | 23.0 | 1 | 0.5 | `r-0c0f3a761516cf334965` | `r-c93a95647e79ab528cf4` |
| h/1 | P05_long_step | ap_half_width | exceeds | 0.6999999999993634 | 0.6399999999994179 | 0.06 | 0.05 | `r-6299bd8dadd5e9592d63` | `r-0499213f80a8244094a6` |
| h/1 | P05_long_step | first_isi | exceeds | 21.2199999999807 | 20.389999999981455 | 0.83 | 0.6 | `r-6299bd8dadd5e9592d63` | `r-0499213f80a8244094a6` |
| h/1 | P05_long_step | last_isi | exceeds | 78.13000000170541 | 72.21000000157619 | 5.92 | 1.5626 | `r-6299bd8dadd5e9592d63` | `r-0499213f80a8244094a6` |
| h/1 | P05_long_step | mean_frequency | exceeds | 14.694109182274286 | 15.872203164178078 | 1.17809 | 0.734705 | `r-6299bd8dadd5e9592d63` | `r-0499213f80a8244094a6` |
| h/1 | P05_long_step | spike_count | exceeds | 29.0 | 31.0 | 2 | 0.5 | `r-6299bd8dadd5e9592d63` | `r-0499213f80a8244094a6` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 12. `m-scale_gate_time_constant-834b272d00`

- **operator**: `scale_gate_time_constant`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/channels/Na/Na.channel.nml` · `/neuroml[@id='Na']/ionChannel[@id='Na']/gate[@id='m']/q10Settings[1]` · **None**: `None` → `<q10Settings xmlns="http://www.neuroml.org/schema/neuroml2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" type="q10Fixed" fixedQ10="2"/>`

**Diagnostic recorded by the campaign**

```
# m-scale_gate_time_constant-834b272d00

- model: `pospischil2008_lts`
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"channel": "Na", "factor": 2.0, "gate": "m", "generator_seed": 20260913, "mechanism": "q10_insert"}`
- recorded edits: `[{"file": "NeuroML2/channels/Na/Na.channel.nml", "locator": "/neuroml[@id='Na']/ionChannel[@id='Na']/gate[@id='m']/q10Settings[1]", "attribute": null, "old": null, "new": "<q10Settings xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" type=\"q10Fixed\" fixedQ10=\"2\"/>", "action": "insert", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2132.2 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.45003406360930803 | 0.34741584772601103 | 0.102618 | 0.0450034 | `r-7fe8302f56856b53d535` | `r-61fd46efb75fd0f9275c` |
| h/1 | P00_canonical | ahp_depth | exceeds | 16.573501743312846 | 15.382126010896684 | 1.19138 | 0.828675 | `r-7fe8302f56856b53d535` | `r-61fd46efb75fd0f9275c` |
| h/1 | P00_canonical | first_isi | exceeds | 14.159999999987122 | 16.14999999998531 | 1.99 | 0.6 | `r-7fe8302f56856b53d535` | `r-61fd46efb75fd0f9275c` |
| h/1 | P00_canonical | last_isi | exceeds | 202.1999999998161 | 206.34999999981233 | 4.15 | 4.044 | `r-7fe8302f56856b53d535` | `r-61fd46efb75fd0f9275c` |
| h/1 | P00_canonical | mean_frequency | exceeds | 12.319822594574143 | 11.301350511403374 | 1.01847 | 0.615991 | `r-7fe8302f56856b53d535` | `r-61fd46efb75fd0f9275c` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.4630010462892806 | 0.35755270664611927 | 0.105448 | 0.0450034 | `r-055cc6b1739501cecd9d` | `r-4f5e5b4eae4a0f451328` |
| h/2 | P00_canonical | ahp_depth | exceeds | 16.673553569797534 | 15.482879741672534 | 1.19067 | 0.828675 | `r-055cc6b1739501cecd9d` | `r-4f5e5b4eae4a0f451328` |
| h/2 | P00_canonical | first_isi | exceeds | 13.959999999987303 | 15.91999999998552 | 1.96 | 0.6 | `r-055cc6b1739501cecd9d` | `r-4f5e5b4eae4a0f451328` |
| h/2 | P00_canonical | last_isi | exceeds | 202.7499999998156 | 207.01999999981172 | 4.27 | 4.044 | `r-055cc6b1739501cecd9d` | `r-4f5e5b4eae4a0f451328` |
| h/2 | P00_canonical | mean_frequency | exceeds | 12.393493415976295 | 11.350737797974237 | 1.04276 | 0.615991 | `r-055cc6b1739501cecd9d` | `r-4f5e5b4eae4a0f451328` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 13. `m-scale_gate_time_constant-bac677a78d`

- **operator**: `scale_gate_time_constant`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/channels/IM/IM.channel.nml` · `/neuroml[@id='IM']/ionChannel[@id='IM']/gate[@id='p']/q10Settings[1]` · **None**: `None` → `<q10Settings xmlns="http://www.neuroml.org/schema/neuroml2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" type="q10Fixed" fixedQ10="1.25"/>`

**Diagnostic recorded by the campaign**

```
# m-scale_gate_time_constant-bac677a78d

- model: `pospischil2008_lts`
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"channel": "IM", "factor": 1.25, "gate": "p", "generator_seed": 20260913, "mechanism": "q10_insert"}`
- recorded edits: `[{"file": "NeuroML2/channels/IM/IM.channel.nml", "locator": "/neuroml[@id='IM']/ionChannel[@id='IM']/gate[@id='p']/q10Settings[1]", "attribute": null, "old": null, "new": "<q10Settings xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" type=\"q10Fixed\" fixedQ10=\"1.25\"/>", "action": "insert", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2145.869 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.45003406360930803 | 0.2448155292982877 | 0.205219 | 0.0450034 | `r-7fe8302f56856b53d535` | `r-20eb30c924c2c50fc1f1` |
| h/1 | P00_canonical | last_isi | exceeds | 202.1999999998161 | 206.4899999998122 | 4.29 | 4.044 | `r-7fe8302f56856b53d535` | `r-20eb30c924c2c50fc1f1` |
| h/1 | P00_canonical | mean_frequency | exceeds | 12.319822594574143 | 10.586491636687365 | 1.73333 | 0.615991 | `r-7fe8302f56856b53d535` | `r-20eb30c924c2c50fc1f1` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.4630010462892806 | 0.25765754837144395 | 0.205343 | 0.0450034 | `r-055cc6b1739501cecd9d` | `r-ee20c7a950056f089a81` |
| h/2 | P00_canonical | last_isi | exceeds | 202.7499999998156 | 207.34999999981142 | 4.6 | 4.044 | `r-055cc6b1739501cecd9d` | `r-ee20c7a950056f089a81` |
| h/2 | P00_canonical | mean_frequency | exceeds | 12.393493415976295 | 10.649343734208268 | 1.74415 | 0.615991 | `r-055cc6b1739501cecd9d` | `r-ee20c7a950056f089a81` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 14. `m-shift_initial_voltage-fa992f061c`

- **operator**: `shift_initial_voltage`  ·  **family**: biophysical
- **assigned class**: `4_equivalent_within_tested_domain`
- **detected by**: nothing
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/cells/RS/RS.cell.nml` · `/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/initMembPotential[1]` · **value**: `-70.0 mV` → `-75.0 mV`

**Diagnostic recorded by the campaign**

```
# m-shift_initial_voltage-fa992f061c

- model: `pospischil2008_rs`
- kind/family/operator: mutant / biophysical / shift_initial_voltage
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/initMembPotential[1]", "new": "-75.0 mV", "old": "-70.0 mV"}], "element": "initMembPotential", "element_id": null, "generator_seed": 20260913, "shift_mV": -5.0}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/initMembPotential[1]", "attribute": "value", "old": "-70.0 mV", "new": "-75.0 mV", "action": "set", "note": "shift_initial_voltage"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 630.416 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 15. `m-shift_reversal-5c87169260`

- **operator**: `shift_reversal`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P04_step_2x;P05_long_step
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/cells/LTS/LTS.cell.nml` · `/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']` · **erev**: `-100.0 mV` → `-95.0 mV`

**Diagnostic recorded by the campaign**

```
# m-shift_reversal-5c87169260

- model: `pospischil2008_lts`
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "new": "-95.0 mV", "old": "-100.0 mV"}], "element": "channelDensity", "element_id": "Kd_all", "generator_seed": 20260913, "shift_mV": 5.0}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LTS.cell.nml", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "attribute": "erev", "old": "-100.0 mV", "new": "-95.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2076.718 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.45003406360930803 | 0.7172279644532592 | 0.267194 | 0.0450034 | `r-7fe8302f56856b53d535` | `r-e4e026235ff465541cad` |
| h/1 | P00_canonical | ahp_depth | exceeds | 16.573501743312846 | 19.1799317970314 | 2.60643 | 0.828675 | `r-7fe8302f56856b53d535` | `r-e4e026235ff465541cad` |
| h/1 | P00_canonical | first_isi | exceeds | 14.159999999987122 | 10.399999999990541 | 3.76 | 0.6 | `r-7fe8302f56856b53d535` | `r-e4e026235ff465541cad` |
| h/1 | P00_canonical | last_isi | exceeds | 202.1999999998161 | 225.1199999997953 | 22.92 | 4.044 | `r-7fe8302f56856b53d535` | `r-e4e026235ff465541cad` |
| h/1 | P00_canonical | mean_frequency | exceeds | 12.319822594574143 | 13.148379462252691 | 0.828557 | 0.615991 | `r-7fe8302f56856b53d535` | `r-e4e026235ff465541cad` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 14.597407663981116 | 16.920031870525193 | 2.32262 | 1.3737 | `r-c8dafa7919f8741d136a` | `r-dde03969c4b9f75a0ff2` |
| h/1 | P04_step_2x | firing_regime | categorical | single_spike | tonic |  |  | `r-c8dafa7919f8741d136a` | `r-dde03969c4b9f75a0ff2` |
| h/1 | P04_step_2x | first_isi | definedness | None | 57.09999999994807 |  | inf | `r-c8dafa7919f8741d136a` | `r-dde03969c4b9f75a0ff2` |
| h/1 | P04_step_2x | last_isi | definedness | None | 57.09999999994807 |  | inf | `r-c8dafa7919f8741d136a` | `r-dde03969c4b9f75a0ff2` |
| h/1 | P04_step_2x | mean_frequency | definedness | None | 17.44439598782424 |  | inf | `r-c8dafa7919f8741d136a` | `r-dde03969c4b9f75a0ff2` |
| h/1 | P04_step_2x | spike_count | exceeds | 1.0 | 2.0 | 1 | 0.5 | `r-c8dafa7919f8741d136a` | `r-dde03969c4b9f75a0ff2` |
| h/1 | P05_long_step | ahp_depth | exceeds | 14.078013743082678 | 16.27267011515299 | 2.19466 | 1.31907 | `r-0e47469602e57d8257f5` | `r-0021a0beebd16a20cb27` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.4630010462892806 | 0.7255621844882975 | 0.262561 | 0.0450034 | `r-055cc6b1739501cecd9d` | `r-64e03728e18c6cfafbc8` |
| h/2 | P00_canonical | ahp_depth | exceeds | 16.673553569797534 | 19.279411418918627 | 2.60586 | 0.828675 | `r-055cc6b1739501cecd9d` | `r-64e03728e18c6cfafbc8` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 16. `m-shift_reversal-8c42fb9d1f`

- **operator**: `shift_reversal`  ·  **family**: biophysical
- **assigned class**: `5_non_equivalent`
- **detected by**: P00_canonical;P04_step_2x;P05_long_step;P06_ramp
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/cells/RS/RS.cell.nml` · `/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all']` · **erev**: `-100.0 mV` → `-95.0 mV`

**Diagnostic recorded by the campaign**

```
# m-shift_reversal-8c42fb9d1f

- model: `pospischil2008_rs`
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all']", "new": "-95.0 mV", "old": "-100.0 mV"}], "element": "channelDensity", "element_id": "IM_all", "generator_seed": 20260913, "shift_mV": 5.0}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all']", "attribute": "erev", "old": "-100.0 mV", "new": "-95.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1665.731 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.2988218828985024 | 0.1958150759218347 | 0.103007 | 0.0298822 | `r-5171ec6a0414fa8c47f8` | `r-45fcdf2e68e6863c652f` |
| h/1 | P00_canonical | first_isi | exceeds | 28.06999999997447 | 26.84999999997558 | 1.22 | 0.5614 | `r-5171ec6a0414fa8c47f8` | `r-45fcdf2e68e6863c652f` |
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 115.83999999989464 | 20.14 | 2.7196 | `r-5171ec6a0414fa8c47f8` | `r-45fcdf2e68e6863c652f` |
| h/1 | P00_canonical | mean_frequency | exceeds | 17.03113291098414 | 18.055430170647178 | 1.0243 | 0.851557 | `r-5171ec6a0414fa8c47f8` | `r-45fcdf2e68e6863c652f` |
| h/1 | P00_canonical | spike_count | exceeds | 5.0 | 6.0 | 1 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-45fcdf2e68e6863c652f` |
| h/1 | P04_step_2x | last_isi | exceeds | 28.16999999997438 | 25.039999999977226 | 3.13 | 0.5634 | `r-0c0f3a761516cf334965` | `r-5e578bef69dbace28f56` |
| h/1 | P04_step_2x | mean_frequency | exceeds | 44.11292909854356 | 48.408823034237884 | 4.29589 | 2.20565 | `r-0c0f3a761516cf334965` | `r-5e578bef69dbace28f56` |
| h/1 | P04_step_2x | spike_count | exceeds | 22.0 | 23.0 | 1 | 0.5 | `r-0c0f3a761516cf334965` | `r-5e578bef69dbace28f56` |
| h/1 | P05_long_step | last_isi | exceeds | 78.13000000170541 | 64.63000000141074 | 13.5 | 1.5626 | `r-6299bd8dadd5e9592d63` | `r-1372350a9302ee1e3835` |
| h/1 | P05_long_step | mean_frequency | exceeds | 14.694109182274286 | 17.43464571771925 | 2.74054 | 0.734705 | `r-6299bd8dadd5e9592d63` | `r-1372350a9302ee1e3835` |
| h/1 | P05_long_step | spike_count | exceeds | 29.0 | 34.0 | 5 | 0.5 | `r-6299bd8dadd5e9592d63` | `r-1372350a9302ee1e3835` |
| h/1 | P06_ramp | mean_frequency | exceeds | 30.288956646438177 | 32.3706438723719 | 2.08169 | 1.51445 | `r-7054f91d1e6b5f4b29f8` | `r-ff5a33b9a6c3a2f9a67e` |
| h/1 | P06_ramp | spike_count | exceeds | 30.0 | 32.0 | 2 | 0.5 | `r-7054f91d1e6b5f4b29f8` | `r-ff5a33b9a6c3a2f9a67e` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.2989579287624928 | 0.19599711253105992 | 0.102961 | 0.0298822 | `r-35d4f8d415fe0d06a895` | `r-b111fa058bc93c767ff1` |
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 17. `m-solver_config-f0ab9d8f86`

- **operator**: `solver_config`  ·  **family**: numerical
- **assigned class**: `4_equivalent_within_tested_domain`
- **detected by**: nothing
- **structurally valid**: True  ·  **execution overrides**: {"integrator_method": "eulertree"}

**The edit**

- `NeuroML2/cells/LTS/LEMS_LTS.xml` · `/Lems[1]/Component[@id='sim1']/Meta[1]` · **None**: `None` → `<Meta xmlns="http://www.neuroml.org/lems/0.7.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" for="jlems" method="eulertree"/>`

**Diagnostic recorded by the campaign**

```
# m-solver_config-f0ab9d8f86

- model: `pospischil2008_lts`
- kind/family/operator: mutant / numerical / solver_config
- parameters: `{"generator_seed": 20260913, "mechanism": "insert_meta", "method": "eulertree"}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LEMS_LTS.xml", "locator": "/Lems[1]/Component[@id='sim1']/Meta[1]", "attribute": null, "old": null, "new": "<Meta xmlns=\"http://www.neuroml.org/lems/0.7.2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" for=\"jlems\" method=\"eulertree\"/>", "action": "insert", "note": "solver_config"}]`
- execution overrides: `{"integrator_method": "eulertree"}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 721.771 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 18. `m-wrong_channel-9d7d66750b`

- **operator**: `wrong_channel`  ·  **family**: reference
- **assigned class**: `3_numerically_unstable`
- **detected by**: nothing
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/cells/RS/RS.cell.nml` · `/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']` · **ionChannel**: `LeakConductance` → `Kd`

**Diagnostic recorded by the campaign**

```
# m-wrong_channel-9d7d66750b

- model: `pospischil2008_rs`
- kind/family/operator: mutant / reference / wrong_channel
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "new": "Kd", "old": "LeakConductance"}], "element_id": "LeakConductance_all", "generator_seed": 20260913, "new_species": "k", "old_species": "non_specific"}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "attribute": "ionChannel", "old": "LeakConductance", "new": "Kd", "action": "set", "note": "wrong_channel"}]`
- execution overrides: `{}`
- class: **3_numerically_unstable**
- nominal-level status: numerically_unstable; runtime 493.619 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 19. `m-wrong_channel-b78286d788`

- **operator**: `wrong_channel`  ·  **family**: reference
- **assigned class**: `2_non_executable`
- **detected by**: nothing
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/cells/LTS/LTS.cell.nml` · `/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']` · **ionChannel**: `Kd` → `Na`

**Diagnostic recorded by the campaign**

```
# m-wrong_channel-b78286d788

- model: `pospischil2008_lts`
- kind/family/operator: mutant / reference / wrong_channel
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "new": "Na", "old": "Kd"}], "element_id": "Kd_all", "generator_seed": 20260913, "new_species": "na", "old_species": "k"}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LTS.cell.nml", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "attribute": "ionChannel", "old": "Kd", "new": "Na", "action": "set", "note": "wrong_channel"}]`
- execution overrides: `{}`
- class: **2_non_executable**
- nominal-level status: build_error; runtime 704.233 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---

## 20. `m-wrong_compatible_component-c51f0c7ae1`

- **operator**: `wrong_compatible_component`  ·  **family**: reference
- **assigned class**: `2_non_executable`
- **detected by**: nothing
- **structurally valid**: True  ·  **execution overrides**: {}

**The edit**

- `NeuroML2/cells/LTS/LTS.cell.nml` · `/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all']` · **ionChannel**: `IM` → `Kd`

**Diagnostic recorded by the campaign**

```
# m-wrong_compatible_component-c51f0c7ae1

- model: `pospischil2008_lts`
- kind/family/operator: mutant / reference / wrong_compatible_component
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all']", "new": "Kd", "old": "IM"}], "element_id": "IM_all", "generator_seed": 20260913, "new_species": "k", "old_species": "k"}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LTS.cell.nml", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all']", "attribute": "ionChannel", "old": "IM", "new": "Kd", "action": "set", "note": "wrong_compatible_component"}]`
- execution overrides: `{}`
- class: **2_non_executable**
- nominal-level status: build_error; runtime 659.242 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
```

**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes

---
