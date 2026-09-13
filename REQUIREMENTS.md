# NeuroSem requirements traceability (Milestone 0 document)

Working name: NeuroSem (see DECISIONS.md N-10 on renaming). Human author and decision-maker: Neel Gurram.
Software built by Claude Code. Date of inspection: 2026-09-13. Branch `m0-audit`, HEAD `d323afa`
(implementation commits `3cdb957` and `d323afa`).

## In plain English

- This file lists every requirement in the final specification, one numbered line each.
- Each line says whether the repository already meets it, and where to look.
- Most of the software is built and has tests. "Built" does not mean it is scientifically checked.
- Several steps need you, Neel, on purpose. Examples: audit 20 mutants by hand, look at protocol plots, choose the held-out split, write the preregistration.
- Some choices are still open, such as final tolerances and pilot thresholds. They are listed as "decision pending".
- The Milestone 6 pilot is running now. It has no results yet, so nothing here is a finding.
- The Milestone 0 papers now all exist (they were written in parallel with this file); the prior-art citations still need your spot-check.
- No study result exists and no novelty is claimed.

## How this was checked

- **Authority.** The authoritative source is `docs/handoff/NEUROSEM_FINAL_SPEC.pdf`, read through its text extraction `docs/handoff/NEUROSEM_FINAL_SPEC.extracted.md`. Spec section names below are that document's headings.
- **Earlier handoff.** Rows marked "(handoff)" come only from the earlier `NEUROSEM_CLAUDE_HANDOFF.extracted.md`. The final spec supersedes it where they differ (D-002); it does not repeat those items.
- **Method.** Every status comes from inspecting files: code, configs, test names, `git status` (read-only) and file existence. No test was run for this document. `pytest --collect-only` collects 980 tests.
- **Working tree, not only HEAD.** `DEPENDENCY_AUDIT.md`, `LICENSE_AUDIT.md` and `docs/NAME_CONFLICT_AUDIT.md` exist but are untracked. `CHANGELOG.md` and `DECISIONS.md` have uncommitted edits.
- **Pilot.** Campaign `pilot` is running (a `neurosem` process was active during inspection). Its files under `results/processed/pilot/` and `results/raw/pilot/` are incomplete. They were used only to confirm formats and generated scope, never outcomes. **Pilot: running; results pending.**
- **Untested orchestration.** No test directly exercises `experiments/campaign.py`, `pilot.py`, `discovery.py` or `heldout.py`. Two exceptions: `tests/unit/test_science_docs.py` string-checks `heldout.py`, and `tests/unit/test_analyze_sensitivity.py` tests only `analyze.tolerance_sensitivity`. The `cli.py` commands have no behavioural tests.

Status vocabulary:

| Status | Meaning |
|---|---|
| implemented | code or document exists and a test, config key or document backs it |
| partially implemented | some of the requirement exists; the gap is stated |
| not implemented | nothing found in the repository |
| gated by design | deliberately blocked until preregistration or freeze, or until someone other than the builder acts (DECISIONS.md D-003) |
| human step pending | needs Neel (or another human) to perform or review something |
| decision pending | needs a choice from Neel; usually listed as N-xx in DECISIONS.md |

Paths are relative to `C:/Users/gurra/NeuroSem`. "Test" means a pytest function name.

---

## 1. Framing, novelty boundary and prior art

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-001 | Executive decision; Existing validation | Reuse NeuroML validation, simulation and eFEL capabilities instead of rebuilding them, and do not claim them as new | implemented | `src/neurosem/simulators/jneuroml.py` (calls the jNeuroML jar, D-005), `src/neurosem/features/efel_adapter.py`; `tests/integration/test_jneuroml_adapter.py`, `tests/unit/test_efel_adapter.py`; `DEPENDENCY_AUDIT.md` (untracked) says "Built in NeuroSem" is not a novelty claim |
| R-002 | Executive decision; AI-assisted development policy | Claude Code is a development assistant; it must not define the title, the main hypothesis or the principal novelty | implemented | `AI_USE_LOG.md` ("Two roles of AI"), `docs/ai_disclosure.md`, `configs/agent_policy.yaml` header |
| R-003 | Candidate empirical discoveries | Candidate discoveries are hypotheses and must not be written as findings before data collection | implemented | `src/neurosem/experiments/pilot.py` report header ("not a confirmatory result"); test `test_palette_is_okabe_ito_and_titles_make_no_claims` (`tests/unit/test_figures.py`) |
| R-004 | Required novelty sweep | Search Google Scholar, PubMed, IEEE Xplore, ACM DL, WoS/Scopus, Semantic Scholar, arXiv/bioRxiv, GitHub/PyPI/Zenodo with the listed term combinations | partially implemented | 1,552 queries across the required sources except Web of Science/Scopus (no access); several APIs rate-limited; the final spec's two added terms run only 4-5 times (`PRIOR_ART_AUDIT.md` sections 1 and 7) |
| R-005 | Required novelty sweep | Create `docs/novelty_matrix.csv` with the specified columns (citation, year, model type, mutations, multiple stimuli, features, protocol optimisation, held-out evaluation, AI transformations, software, distinction) | implemented | `docs/novelty_matrix.csv` (335 verified works, spec columns plus provenance), built by `scripts/build_novelty_matrix.py`; summary in `docs/m0_evidence/prior_art/novelty_matrix_summary.json` |
| R-006 | Required novelty sweep | Absence from a search is not proof of novelty; citations must be human-checked before any novelty claim | human step pending | `AI_USE_LOG.md` Entry 001 ("Neel must spot-check citations"); `docs/ai_disclosure.md` section 3 |

## 2. Study design and definitions

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-007 | Operational definitions | Define reference model, transformation, valid transformation, mutant, admissible non-equivalent mutant, canonical protocol, perturbation fingerprint, silent semantic drift and empirical semantic certificate | implemented | `docs/glossary.md` section 1; test `test_glossary_covers_operational_definitions_and_required_terms` (`tests/unit/test_science_docs.py`) |
| R-008 | Fingerprint definition | F(m) = {f(m,p) : p in P, f in E}; detection when at least one prespecified protocol-feature difference exceeds its calibrated tolerance | implemented | `src/neurosem/validation/fingerprint.py` (`build_fingerprint`, `compare`); test `test_compare_exceeds_definedness_categorical_and_multiplier` (`tests/unit/test_convergence_fingerprint.py`). Definedness changes and firing-regime changes also count as detections (`configs/tolerances.yaml: definedness_mismatch_is_detection`, `categorical`) |
| R-009 | Operational definitions | An empirical certificate is evidence of tested preservation, not a proof of equivalence | implemented | `docs/glossary.md` section 1 (checked by `test_glossary_covers_operational_definitions_and_required_terms`) |
| R-010 | Research questions | The design must be able to answer RQ1-RQ7 | partially implemented | Code paths: RQ1 `analysis/metrics.silent_survival_rate`; RQ2 and RQ4 `experiments/heldout.py`; RQ3 `selection/greedy.random_*`; RQ5 needs a held-out family (unassigned, N-02); RQ6 `metrics.by_family` and the detection matrix; RQ7 `experiments/agent.py`. No RQ has been answered |
| R-011 | Primary hypothesis; Primary endpoint | Held-out detection rate of the selected battery versus canonical regression | gated by design | `src/neurosem/experiments/heldout.py` (`paired_comparison(battery, canonical, ...)` behind `HeldoutGate`). Only string-level tests: `test_detection_rule_matches_heldout_code`, `test_quoted_heldout_bootstrap_resamples_match_code` |
| R-012 | Secondary endpoints | Detection rate versus cost-matched random batteries | implemented | `selection/greedy.py` `random_count_matched`, `random_runtime_matched`; `experiments/analyze.py`; `tests/unit/test_greedy_selection.py` |
| R-013 | Secondary endpoints | Silent-survival rate after canonical testing | implemented | `analysis/metrics.silent_survival_rate`; test `test_silent_survival_rate_uses_admissible_denominator` |
| R-014 | Secondary endpoints | False-positive rate on valid transformations | implemented | `metrics.false_positive_rate`, `false_positive_summary`; test `test_false_positive_rate_and_summary` |
| R-015 | Secondary endpoints | Detection rate by mutation family | implemented | `metrics.by_family`; test `test_by_family_counts_and_intervals` |
| R-016 | Secondary endpoints | Protocols needed to reach increasing levels of exhaustive-battery coverage | implemented | `metrics.coverage_curve`, `protocols_to_reach`; tests `test_coverage_curve_hand_computed`, `test_protocols_to_reach_levels`. Coverage levels are decision pending (`docs/statistical_plan.md` section 10 item 6) |
| R-017 | Secondary endpoints | Runtime and simulations per detected mutant | implemented | `metrics.runtime_per_detection`; test `test_runtime_per_detection`; cost is simulated cell-steps (D-015) |
| R-018 | Secondary endpoints | Agent-task success under basic versus NeuroSem validation | implemented | `configs/agent_policy.yaml: scoring.basic_validation / neurosem_validation`; `experiments/agent.summarize_scores`; test `test_summarize_scores_reports_the_permitted_claim_fraction`. No trials exist |

## 3. Pilot and full-study scope

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-019 | Solo-feasible scope: Pilot | 2 reference models | implemented | `configs/study.yaml: pilot.models` (pospischil2008_rs, pospischil2008_lts); `data/model_manifest.csv` inclusion=include (D-017) |
| R-020 | Solo-feasible scope: Pilot | 4 candidate protocols | decision pending | The pilot runs every implemented protocol: `campaign.py` instantiates `batched(templates_from_config(...))`, i.e. P01, P02 and P04-P10, plus P03 and P00_canonical. This deviation from the pilot target is not recorded in DECISIONS.md |
| R-021 | Solo-feasible scope: Pilot | 3-5 extracted features | decision pending | `configs/features.yaml` defines 18 features, all used in the pilot; the deviation is not recorded in DECISIONS.md |
| R-022 | Solo-feasible scope: Pilot | 3 mutation families | implemented | `configs/study.yaml: pilot.mutation_families` = biophysical, reference, numerical (stimulus excluded, D-009) |
| R-023 | Solo-feasible scope: Pilot | 5-10 mutants per model | decision pending | `pilot.mutants_per_operator: 2`. Generated scope (not an outcome): 26 mutants per model in `results/processed/pilot/mutation_manifest.csv`, 52 in total. That exceeds the per-model target but is inside Milestone 6's 20-60. `docs/mutation_catalog.md` section 5.4 notes that targets are not config values |
| R-024 | Solo-feasible scope: Pilot | 4-6 valid transformations | decision pending | `pilot.transforms_per_operator: 1`. Generated per model: 7 valid transforms plus 2 no-change controls (`results/processed/pilot/valid_transforms.csv`) |
| R-025 | Solo-feasible scope: Pilot | jNeuroML only | implemented | `configs/study.yaml: simulator: jneuroml`; `simulators/neuron.py` is an unused stub |
| R-026 | Solo-feasible scope: Pilot | Pilot success = one admissible canonical-passing mutant reproducibly detected elsewhere, stable features under refinement, and no widespread false positives | partially implemented | `experiments/pilot.write_report` checks three criteria (`crit1`-`crit3`). There is no direct test. Thresholds (<25% features excluded, <=10% false positives) are provisional (N-04) |
| R-027 | Full solo study | 12-16 reference models | not implemented | `data/model_manifest.csv` has 6 rows, 2 included; `docs/model_selection.md` section 10 item 1 |
| R-028 | Full solo study | 8-10 discovery and 4-6 held-out models | decision pending | N-02; `data/splits/discovery_models.txt` (2 provisional pilot models); `data/splits/heldout/` contains only README.md |
| R-029 | Full solo study | 10-16 candidate protocols | implemented | 10 implemented (P01-P10) in `src/neurosem/protocols/definitions.py` and `data/protocol_manifest.csv`; P11 and P12 deferred (R-054, R-055) |
| R-030 | Full solo study | 6-8 mutation families | partially implemented | `schemas.MutationFamily` has 4 families (stimulus, biophysical, reference, numerical), which is what the spec itself enumerates. How to reach 6-8 is undecided |
| R-031 | Full solo study | 100-160 admissible mutants | gated by design | Needs the frozen full study (D-003) |
| R-032 | Full solo study | 24-40 valid transformations | gated by design | 8 transform operators exist (R-077..R-084); the full-study count needs the frozen study |
| R-033 | Full solo study | 20-30 Claude Code tasks | partially implemented | 9 task definitions, one per task type (`agent_study/tasks/t01..t09`); `docs/build_notes/agent-study.md` says nine is not a sample size |
| R-034 | Full solo study | 4-6 cross-simulator models (optional) | decision pending | N-08; `src/neurosem/simulators/neuron.py` is a stub (NEURON not installed) |
| R-035 | Full solo study | Counts are planning bounds; use a pilot runtime estimate or power analysis; reduce mutants before sacrificing curation, provenance, controls or held-out evaluation | decision pending | `docs/preregistration_draft.md` section 14 (template with blanks); the runtime estimate needs pilot results (pending) |

## 4. Model inclusion criteria, diversity and provenance fields

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-036 | Model selection: Inclusion criteria | Traceable public source | implemented | `data/model_manifest.csv` `source_url`, `commit`; `models/raw/*/PROVENANCE.json`; test `test_manifest_provenance_fields` (`tests/unit/test_models_manifest.py`) |
| R-037 | Inclusion criteria | License permits intended use and redistribution, or no redistribution | partially implemented | `license` and `license_url` columns; `LICENSE_AUDIT.md` (untracked); redistribution of mutated LGPL files is undecided (N-05, D-018) |
| R-038 | Inclusion criteria | Passes current NeuroML validation | implemented | `src/neurosem/validation/structural.py` (relative oracle over the include closure, D-006); `neurosem validate-models`; test `test_structural_check_reference_and_broken_reference` (`tests/unit/test_execution_canonical.py`) |
| R-039 | Inclusion criteria | Executes deterministically in the frozen environment | implemented | `experiments/campaign.reference_stage` writes `determinism.json` (bitwise-identical battery traces across replicates); test `test_cache_immutability_reproducibility_and_feature_rekeying` (`tests/integration/test_run_recorder.py`) |
| R-040 | Inclusion criteria | Completes candidate protocols within a practical runtime | partially implemented | `configs/study.yaml: numerics.timeout_s: 7200`; no runtime inclusion threshold is defined |
| R-041 | Inclusion criteria | Produces interpretable voltage output | implemented | manifest `harness_output_file`, `harness_v_column`; test `test_harness_output_file_and_column_exist` |
| R-042 | Inclusion criteria | Responds meaningfully to current injection | partially implemented | `src/neurosem/protocols/rheobase.py` reports spontaneous and not-found cases (`tests/unit/test_rheobase_search.py`); the inclusion rule for not-found or error is unspecified (`docs/protocol_catalog.md` section 8 item 2) |
| R-043 | Inclusion criteria | Scientific provenance linking to a publication or established repository | implemented | manifest `citation`; `docs/model_selection.md` section 8 notes that the HH example is a textbook implementation |
| R-044 | Inclusion criteria | No unavailable proprietary dependencies | implemented | `docs/model_selection.md` section 9 (e.g. Allen content excluded for its terms of use) |
| R-045 | Diversity goals | Span tonic spiking, adaptation, bursting, rebound, sag and distinct thresholds | decision pending | `docs/model_selection.md` section 7: no licensed Ih/sag model found; three options are listed for Neel |
| R-046 | Diversity goals | Begin with single-compartment models; add few multicompartment models later | implemented | Pilot fixtures are single-compartment; test `test_reduce_spatial_discretization_single_vs_multi_compartment` |
| R-047 | Provenance record | Internal ID, model name, citation, source URL, download date, license and license URL | implemented | `schemas.ModelRecord` and `data/model_manifest.csv` columns; test `test_manifest_columns_match_dataclass` |
| R-048 | Provenance record | Original files, SHA-256 hashes, required includes | implemented | `models/raw/<snapshot>/PROVENANCE.json` (per-file url, sha256, hash_check); `scripts/fetch_models.py` follows includes; test `test_all_snapshots_present` |
| R-049 | Provenance record | Simulator version | partially implemented | The manifest `simulator` column says only "jNeuroML"; the version is recorded per run in `RunRecord.simulator_version`; `docs/model_selection.md` section 10 item 4 (decision) |
| R-050 | Provenance record | Known expected behaviour | implemented | manifest `expected_behavior` (some entries say "to confirm by simulation") |
| R-051 | Provenance record | Inclusion or exclusion decision and reason | implemented | manifest `inclusion`, `inclusion_reason` |

## 5. Protocols 1-12

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-052 | Protocol battery 1-10 | Implement P01 zero-current baseline, P02 weak step, P03 rheobase search, P04 step at a fixed rheobase multiple (2x), P05 long step, P06 ramp, P07 hyperpolarising step, P08 rebound, P09 short pulse, P10 paired pulses | implemented | `src/neurosem/protocols/definitions.py`, `generate.py`, `rheobase.py`; `data/protocol_manifest.csv`; tests `tests/unit/test_protocol_definitions.py` (`test_steps`, `test_ramp`, `test_short_pulse`, `test_rebound_window_follows_release`), `tests/unit/test_generate_xml.py`, `tests/integration/test_probe_battery.py`, `tests/unit/test_rheobase_search.py` |
| R-053 | Protocol battery | Model-specific rheobase normalisation | implemented | D-010; test `test_timing_does_not_depend_on_rheobase_and_amplitudes_scale_linearly` |
| R-054 | Protocol battery 11 | Deterministic chirp, only if stable | not implemented | `data/protocol_manifest.csv` implemented=false: "no chirp type" in NeuroML v2.3.1 core; deferral permitted by the spec |
| R-055 | Protocol battery 12 | Frozen pseudo-random waveform, later extension only | not implemented | `data/protocol_manifest.csv` implemented=false; `docs/protocol_catalog.md` section 7 |
| R-056 | Protocol battery | Amplitudes are appropriate for models with very low rheobase | decision pending | N-07 (LTS short pulses, ramp and rebound evoke no response in smoke runs, D-010) |
| R-057 | Canonical protocol (definition) | One canonical protocol as the conventional regression baseline | implemented | `src/neurosem/validation/canonical.py` (shipped harness, D-008, D-021 window rule); test `test_canonical_protocol_windows_from_shipped_harnesses` |
| R-058 | Canonical protocol | Canonical metric: the same features and tolerances, or an OMV-style spike-time check | decision pending | N-06 |

## 6. Features

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-059 | Initial features | Baseline voltage | implemented | `configs/features.yaml: baseline_voltage` (eFEL `voltage_base`); `tests/unit/test_efel_adapter.py` |
| R-060 | Initial features | Steady-state voltage | implemented | `steady_state_voltage` (eFEL `steady_state_voltage_stimend`, D-016) |
| R-061 | Initial features | Voltage deflection | implemented | `voltage_deflection` (eFEL `voltage_deflection_vb_ssse`); test `test_deflection_direction_follows_stimulus_sign` |
| R-062 | Initial features | Sag ratio | implemented | `sag_ratio` (eFEL `sag_ratio1`, `requires: hyperpolarizing`); test `test_sag_ratio_requires_a_hyperpolarizing_protocol`. Expected to be uninformative without an Ih model (R-045) |
| R-063 | Initial features | Rheobase | implemented | `rheobase` (NeuroSem search); test `test_rheobase_floor_uses_search_resolution` |
| R-064 | Initial features | Spike count | implemented | `spike_count` (eFEL `spike_count_stimint`); test `test_no_spike_trace_counts_zero_and_gates_spike_features` |
| R-065 | Initial features | Mean firing frequency | implemented | `mean_frequency` (min_spikes 2) |
| R-066 | Initial features | First-spike latency | implemented | `first_spike_latency` (eFEL `time_to_first_spike`) |
| R-067 | Initial features | Action-potential amplitude | implemented | `ap_amplitude` (eFEL `AP_amplitude`, first); test `test_spiking_trace_aggregation_matches_raw_efel_arrays` |
| R-068 | Initial features | Action-potential half-width | implemented | `ap_half_width` (eFEL `AP_duration_half_width`) |
| R-069 | Initial features | After-hyperpolarisation depth | implemented | `ahp_depth` (eFEL `AHP_depth`, min_spikes 1, D-021); `docs/protocol_catalog.md` section 8 item 1 notes that P09 `ahp_depth` is not_applicable by configuration |
| R-070 | Initial features | First and last interspike intervals | implemented | `first_isi`, `last_isi` (eFEL `all_ISI_values`) |
| R-071 | Initial features | Adaptation index | implemented | `adaptation_index` (eFEL `adaptation_index2`) |
| R-072 | Initial features | Burst count | implemented | `burst_count` (eFEL `strict_burst_number`) |
| R-073 | Initial features | Qualitative firing regime | implemented | `src/neurosem/features/regimes.py`; `tests/unit/test_regimes.py` |
| R-074 | Feature extraction; Initial features | Record eFEL version, interpolation, stimulation windows, thresholds and undefined-feature behaviour; use eFEL only where well defined | implemented | `configs/features.yaml` (`efel_version`, `settings`, `min_spikes`, `requires`); tests `test_settings_are_reset_before_every_extraction`, `test_min_spikes_gating_overrides_numbers_efel_would_return`, `test_efel_settings_rejects_bad_names_and_types` |
| R-075 | Initial features | Record missing or undefined features explicitly; never replace them with zero | implemented | `FeatureValue.state`; test `test_undefined_efel_result_is_recorded_not_zeroed_and_warning_captured` |
| R-076 | Initial features (derived) | One spike threshold (-20 mV) for all models, or a per-model threshold | decision pending | `docs/protocol_catalog.md` section 8 item 4 |

## 7. Valid transformations

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-077 | Valid transformations | Equivalent physical-unit conversion | implemented | `transforms/units.py` `unit_conversion`; tests `test_decimal_unit_conversion_is_exact`, `test_unit_conversion_every_attribute_exact_and_schema_valid` |
| R-078 | Valid transformations | XML formatting or comments | implemented | `transforms/formatting.py` `xml_formatting`, `add_comments` (no-change kind); test `test_no_change_controls_are_semantically_identical` |
| R-079 | Valid transformations | Numerically equivalent literal formatting | implemented | `transforms/units.py` `numeric_literal_format`; test `test_numeric_literal_format_preserves_decimal_values` |
| R-080 | Valid transformations | Identifier renaming with every reference updated | implemented | `transforms/identifiers.py` `rename_identifier`; tests `test_rename_ion_channel_updates_every_file_that_includes_it`, `test_rename_cell_updates_network_harness_and_model_overrides` |
| R-081 | Valid transformations | File factoring with references preserved | implemented | `transforms/factoring.py` `factor_file`; test `test_factor_file_keeps_references_resolvable_for_probe_and_harness` |
| R-082 | Valid transformations | Reordering semantically independent elements | implemented | `reorder_independent`; test `test_reorder_preserves_multiset_and_changes_order` |
| R-083 | Valid transformations | Replacing an inherited default with the same explicit value | implemented | `transforms/units.py` `explicit_default`; test `test_explicit_default_values_come_from_xsd_default_declarations` |
| R-084 | Valid transformations | All transform operators are registered under the binding names | implemented | `transforms/__init__.py REGISTRY`; test `test_registry_has_exactly_the_binding_names` |
| R-085 | Valid transformations | Verify each valid transformation by structural inspection and the exhaustive high-resolution battery before inclusion | partially implemented | Every site validates with jnml (`tests/integration/test_transforms_validate.py::test_every_transform_validates_with_jnml`, `test_probe_traces_match_reference`). In the campaign every transform is fingerprinted at h and h/2 and any detection counts as a false positive. No separate pre-inclusion gate that drops a transform was found |
| R-086 | Valid transformations (handoff) | Transforms used for the false-positive estimate are counted separately from mutants | implemented | `VariantKind.VALID_TRANSFORM` / `NO_CHANGE`; `metrics.false_positive_summary` |

## 8. Mutation families, operators and classification

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-087 | Mutation families: Stimulus | Change input amplitude | implemented | `mutations/stimulus.py` `stim_amplitude`; test `test_stim_amplitude_edits_harness_network_file` |
| R-088 | Stimulus | Change onset | implemented | `stim_onset`; test `test_stim_onset_and_duration` |
| R-089 | Stimulus | Change duration | implemented | `stim_duration`; test `test_stim_onset_and_duration` |
| R-090 | Stimulus | Change total simulation time | implemented | `sim_length`; test `test_sim_length_on_component_and_simulation_syntax` |
| R-091 | Stimulus | Record the wrong variable | implemented | `record_wrong_variable`; test `test_record_wrong_variable_uses_existing_state_paths` |
| R-092 | Biophysical | Scale maximal conductance | implemented | `mutations/biophysics.py` `scale_conductance`; test `test_scale_conductance_covers_all_channel_density_kinds` |
| R-093 | Biophysical | Change reversal potential | implemented | `shift_reversal`; test `test_shift_reversal_skips_nernst` |
| R-094 | Biophysical | Change membrane capacitance | implemented | `scale_capacitance`; test `test_scale_capacitance_and_initial_voltage` |
| R-095 | Biophysical | Scale a channel time constant | implemented | `scale_gate_time_constant`, registered with `allow_q10_fallback=True` (D-021 q10Fixed mechanism); tests `test_scale_gate_time_constant_scales_both_core_rates`, `test_scale_gate_q10_fallback_inserts_in_schema_order`. `q10ExpTemp` gates are inapplicable. `docs/build_notes/mutations.md` section 1.2 predates D-021 |
| R-096 | Biophysical | Change initial voltage | implemented | `shift_initial_voltage`; test `test_scale_capacitance_and_initial_voltage` |
| R-097 | Biophysical | Apply a channel to the wrong segment group | implemented | `wrong_segment_group`; test `test_wrong_segment_group_inserts_attribute_with_existing_group` |
| R-098 | Reference | Reference the wrong channel definition | implemented | `mutations/references.py` `wrong_channel`; test `test_channel_swaps_are_partitioned_by_species` |
| R-099 | Reference | Omit a required include | implemented | `omit_include`; test `test_omit_include`. jnml does not check `channelDensityVShift` references (D-020, N-11) |
| R-100 | Reference | Duplicate a conductance assignment | implemented | `duplicate_conductance`; test `test_duplicate_conductance_inserts_after_original` |
| R-101 | Reference | Point to a wrong but dimensionally compatible component | implemented | `wrong_compatible_component`; test `test_channel_swaps_are_partitioned_by_species` |
| R-102 | Numerical | Increase integration time step | implemented | `mutations/numerical.py` `increase_dt` (factors x4, x10, x20, D-021); test `test_increase_dt_edits_step_and_sets_override` |
| R-103 | Numerical | Alter solver configuration | implemented | `solver_config`; tests `test_solver_config_adds_meta_in_harness_namespace`, `test_meta_integrator_method_does_not_change_trace` (expected no-op for core types) |
| R-104 | Numerical | Reduce spatial discretisation | implemented | `reduce_spatial_discretization`; test `test_reduce_spatial_discretization_single_vs_multi_compartment`. It has 0 sites on single-compartment models, so the pilot never exercises it |
| R-105 | Numerical | Change recording resolution enough to corrupt features | implemented | `recording_resolution` (execution override only, D-009); test `test_recording_resolution_changes_only_exec_overrides` |
| R-106 | Mutation families | Operator registry matches the binding operator table | implemented | `mutations/base.py REGISTRY`; test `test_registry_matches_binding_operator_table` |
| R-107 | Mutation families | Single-fault mutants in the primary study | implemented | `mutations/base.enforce_single_operator`; tests in `tests/unit/test_mutations_base.py` (e.g. `test_enforcement_rejects_edits_in_two_elements`, `test_enforcement_rejects_second_fault_carried_by_overrides`); test `test_record_check_rejects_mislabelled_or_compound_fault` |
| R-108 | Mutation families | Compound faults only in a secondary stress test | not implemented | No compound-fault generator; only mentioned in `docs/mutation_catalog.md` section 2 and `docs/glossary.md` |
| R-109 | Mutation families (derived) | Whether the stimulus family, which only the canonical test can see and which can never be class 6, belongs in the primary population | decision pending | D-009; `docs/build_notes/science-docs.md` section 3; `docs/statistical_plan.md` section 10 item 5 |
| R-110 | Mutant classification | Classify every mutant into the 6 classes | implemented | `schemas.MutantClass`, `validation/fingerprint.classify`; test `test_classification_cascade` |
| R-111 | Mutant classification | Class 3 "executable but numerically unstable" is distinguished from crashes | implemented | `simulators/jneuroml.py` (D-020); tests `test_real_numerical_blowup_is_unstable_not_build_error`, `test_observed_divergent_groups_are_numerically_unstable` |
| R-112 | Mutant classification | Non-equivalence must be reproducible; the same rule applies to every protocol including canonical | implemented | D-013, D-021; `fingerprint.reproducible_keys` (detection at h and h/2). Whether to keep this rule is listed in `docs/statistical_plan.md` section 10 item 2 |
| R-113 | Mutant classification | Only classes 5 and 6 enter the detection-rate denominator; crashes and schema errors are reported separately | implemented | `metrics.silent_survival_rate`, `metrics.validation_cascade`; tests `test_silent_survival_rate_uses_admissible_denominator`, `test_validation_cascade_counts_exhaustive_battery` |
| R-114 | Mutant classification (derived) | Class of variants whose harness runs but whose battery fails to build | decision pending | Flag `canonical_runs_but_battery_failed` (D-020); `docs/statistical_plan.md` section 10 item 9 |

## 9. Tolerance calibration

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-115 | Tolerance calibration step 1 | Run each reference model and protocol at nominal h | implemented | `configs/study.yaml: numerics.dt_nominal_ms: 0.005` (D-007); `campaign.reference_stage` (`fingerprint_L1.json`) |
| R-116 | Step 2 | Repeat at h/2 | implemented | `refinement_factors: [1, 2, 4]`; `fingerprint_L2.json` |
| R-117 | Step 3 | Repeat at h/4 when practical | implemented | `fingerprint_L4.json`; `convergence.convergence_report` (d12, d24, observed order); test `test_convergence_report_observed_order` |
| R-118 | Step 4 | Interpolate traces to a common time grid | partially implemented | `features/trace_metrics.align`, `resample`; test `test_align_puts_different_steps_on_one_grid_within_overlap_and_window`. These are not called by `validation/convergence.py` or `experiments/campaign.py` |
| R-119 | Step 5 | Compare trace and feature differences | partially implemented | Feature differences only (`results/processed/<campaign>/convergence.csv` columns d12, d24); no trace-level (RMSE or max-difference) comparison in calibration |
| R-120 | Step 6 | Repeat stochastic protocols with fixed seeds | partially implemented | `RunRecord.seed` is recorded; no stochastic protocol exists (P12 deferred), so no seeded repeats are defined |
| R-121 | Step 7 | Feature-specific absolute and relative tolerance floors | implemented | `configs/tolerances.yaml: features`; `convergence.calibrate`; test `test_tau_is_max_of_three_terms_and_names_the_limiting_term` |
| R-122 | Conceptual rule | tau = max(abs_floor, rel*abs(f), c*abs(f_h - f_h/2)) | implemented | `configs/tolerances.yaml: c_refinement: 3.0`; test `test_tau_is_max_of_three_terms_and_names_the_limiting_term` |
| R-123 | Tolerance calibration (derived) | Features whose definedness or regime changes under refinement are excluded, not silently dropped | implemented | D-014; test `test_state_changes_under_refinement_are_excluded_not_dropped` |
| R-124 | Tolerance calibration | Justify constants from discovery/reference runs and sensitivity analysis | decision pending | N-03. `configs/tolerances.yaml` says `calibrate-tolerances` writes `results/processed/tolerance_proposal.yaml`, but no code writes that file (grep found no match) |
| R-125 | Step 8 | Freeze tolerances before held-out evaluation | gated by design | `selection/splits.HeldoutGate` requires `configs/FROZEN.lock` hashing every `configs/*.yaml`; test `test_heldout_gate_requires_the_study_config_in_the_lock`. No code writes `FROZEN.lock` (none found) and the file does not exist |
| R-126 | Tolerance calibration | Never adjust constants to improve held-out performance | gated by design | Same lock (R-125); `configs/study.yaml` header "Never edit after held-out access" |

## 10. Protocol selection and baselines

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-127 | Protocol selection | Binary matrix: admissible discovery mutants x protocols | implemented | `selection/matrix.DetectionMatrix`; `campaign.aggregate` writes `detection_matrix.csv`; `tests/unit/test_selection_matrix.py` |
| R-128 | Protocol selection steps 1-4 | Greedy maximum coverage to budget k | implemented | `selection/greedy.greedy_max_coverage`; tests `test_greedy_sequence_curve_and_costs`, `test_tie_break_lower_cost_then_protocol_id`, `test_greedy_meets_the_1_minus_1_over_e_guarantee`; `configs/study.yaml: selection.budget_k: 4` |
| R-129 | Step 5 | Freeze the selected set | partially implemented | `experiments/discovery.select_protocols` writes a selection file; per the `heldout.py` docstring the lock should include the frozen selection, but no lock writer exists (R-125) |
| R-130 | Step 6 | Evaluate on held-out models and mutation families | gated by design | `experiments/heldout.evaluate_heldout` behind `HeldoutGate` |
| R-131 | Protocol selection: compare | Canonical protocol alone | implemented | `discovery.py` `rates.canonical`; `analyze.py` curve "canonical" |
| R-132 | Compare | Random sets with the same protocol count | implemented | `greedy.random_count_matched`; tests `test_count_matched_is_seeded_and_reproducible`, `test_count_matched_mean_matches_exact_expectation` |
| R-133 | Compare | Random sets with comparable runtime | implemented | `greedy.random_runtime_matched` (cost = cell-steps, D-015); test `test_runtime_matched_sets_fit_budget_and_are_maximal`. The sampling algorithm is open (`docs/statistical_plan.md` section 10 item 8) |
| R-134 | Compare | Full candidate battery | implemented | `discovery.py` `rates.exhaustive`; `analyze.py` curve "exhaustive" |
| R-135 | Protocol selection | Optional cost-sensitive objective | implemented | `greedy.greedy_cost_sensitive`; tests `test_cost_sensitive_*` |
| R-136 | Protocol selection | No complicated machine-learning model unless it clearly helps | implemented | Only greedy and random selection exist in `src/neurosem/selection/` |
| R-137 | Protocol selection (derived) | Budget k, whether P00_canonical is a candidate, and how P03 is charged | decision pending | `docs/statistical_plan.md` section 10 items 1 and 7; `docs/protocol_catalog.md` section 8 item 5 |

## 11. Train-test separation and leakage controls

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-138 | Discovery set | Discovery data may be used to develop operators, calibrate tolerances, select protocols, debug features and choose the analysis | implemented | `data/splits/discovery_models.txt`, `discovery_families.txt` (provisional pilot split); `data/splits/README.md` |
| R-139 | Held-out model set | Held-out models must not influence selection or thresholds | gated by design | `selection/splits.discovery_view` never opens `heldout/`; test `test_discovery_selection_end_to_end_never_touches_heldout` |
| R-140 | Held-out mutation family | Exclude at least one mutation family from selection; use it only in final evaluation | decision pending | N-02; `data/splits/heldout/` has no `heldout_families.txt`; `stimulus` is outside discovery but not assigned as held out (`data/splits/README.md`) |
| R-141 | Leakage controls | Store held-out manifests in a separate path | implemented | `data/splits/heldout/` read only by `HeldoutGate`; test `test_heldout_access_in_splits_is_confined_to_gate_and_freeze`. No held-out files exist yet |
| R-142 | Leakage controls; Milestone 7 exit | Selection code cannot read held-out labels | implemented | tests `test_no_selection_module_except_splits_mentions_heldout`, `test_import_and_discovery_selection_in_fresh_interpreter`, `test_filter_matrix_raises_on_any_non_discovery_row` (`tests/unit/test_splits_leakage.py`) |
| R-143 | Leakage controls | Freeze split files with hashes (tooling) | implemented | `scripts/freeze_splits.py`, `splits.freeze_splits`; tests `test_freeze_writes_hashes_and_refuses_silent_overwrite`, `test_freeze_script_cli` |
| R-144 | Leakage controls | Actually freeze the splits | human step pending | `data/splits/SPLITS.sha256` absent; depends on R-028 and R-140 |
| R-145 | Leakage controls | Log every run touching held-out data | partially implemented | `HeldoutGate` appends one JSON line per gate opening to `results/heldout_access.log` (test `test_heldout_gate_opens_with_matching_lock_and_logs_each_access`); individual simulation run records carry no held-out flag |
| R-146 | Leakage controls | Do not repeatedly inspect held-out failures and redesign around them | human step pending | Process discipline; `configs/study.yaml` header; no code can enforce this |
| R-147 | Leakage controls | Second final lockbox only if enough models remain | decision pending | `docs/preregistration_draft.md` line 122 "[NEEL DECISION REQUIRED]"; `docs/glossary.md` "Lockbox" |

## 12. Statistical analysis and preregistration

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-148 | Statistical analysis | Report transparent paired counts, not only aggregate accuracy | implemented | `metrics.paired_counts`; test `test_paired_counts_table` |
| R-149 | Primary analysis | Detection rates for the selected battery and canonical regression on held-out mutants | gated by design | `experiments/heldout.py` |
| R-150 | Primary analysis | Paired difference in detection rate | implemented | `analysis/bootstrap.paired_comparison`; test `test_paired_comparison_report_is_consistent` |
| R-151 | Primary analysis | Confidence interval by resampling base models | implemented | `bootstrap.cluster_bootstrap_diff`; tests `test_bootstrap_resamples_base_models_not_mutants`, `test_bootstrap_ci_coverage_under_clustered_null` |
| R-152 | Primary analysis | Exact paired test where supported | implemented | `bootstrap.exact_mcnemar`, `cluster_permutation_test`; tests `test_exact_mcnemar_matches_scipy_binomtest_grid`, `test_sign_flip_is_at_cluster_level` |
| R-153 | Secondary analysis | Selected versus random cost-matched batteries | implemented | `experiments/analyze.analyze_campaign` (count- and runtime-matched curves); in-sample only on discovery data |
| R-154 | Secondary analysis | Mutation-family-specific detection | implemented | `analyze.py` `metrics.by_family`; test `test_by_family_counts_and_intervals` |
| R-155 | Secondary analysis | False-positive rates on valid transformations | implemented | `metrics.false_positive_summary`; test `test_false_positive_rate_and_summary` |
| R-156 | Secondary analysis | Coverage versus number of protocols | implemented | `metrics.coverage_curve`; test `test_coverage_curve_hand_computed` |
| R-157 | Secondary analysis | Runtime-adjusted coverage | implemented | `coverage_curve` cost axis, `runtime_per_detection`; test `test_runtime_per_detection` |
| R-158 | Secondary analysis | Robustness to stricter and looser tolerances | implemented | `analyze.reclassify`, `tolerance_sensitivity`; `configs/tolerances.yaml: sensitivity_multipliers: [0.5, 1.0, 2.0, 4.0]`; test `test_rates_exclude_not_evaluable_and_count_them` |
| R-159 | Statistical analysis | Account for clustering of mutants within base models | partially implemented | Cluster bootstrap and permutation (R-151, R-152); `SmallClusterWarning` for few models; the source-family clustering rule is open (`docs/statistical_plan.md` section 10 item 10; Pospischil cells are correlated, D-017) |
| R-160 | Statistical analysis (derived) | Material effect size and decision rule | decision pending | `docs/statistical_plan.md` section 4.5 "[decision: Neel]" |
| R-161 | Preregister | Primary hypothesis | human step pending | `docs/preregistration_draft.md` section 1 (template); test `test_preregistration_draft_covers_every_required_item_with_blanks` |
| R-162 | Preregister | Primary endpoint | human step pending | `docs/preregistration_draft.md` section 2 |
| R-163 | Preregister | Inclusion and exclusion rules | human step pending | `docs/preregistration_draft.md` section 4 |
| R-164 | Preregister | Model and mutation splits | human step pending | `docs/preregistration_draft.md` section 5; test `test_preregistration_draft_does_not_assign_heldout_models` |
| R-165 | Preregister | Canonical protocol | human step pending | `docs/preregistration_draft.md` section 6 |
| R-166 | Preregister | Candidate protocols | human step pending | `docs/preregistration_draft.md` section 7 |
| R-167 | Preregister | Tolerance policy | human step pending | `docs/preregistration_draft.md` section 9 |
| R-168 | Preregister | Primary statistical comparison | human step pending | `docs/preregistration_draft.md` section 10 |
| R-169 | Preregister | Handling of undefined features | human step pending | `docs/preregistration_draft.md` section 11 |
| R-170 | Preregister | Treatment of crashes and equivalent mutants | human step pending | `docs/preregistration_draft.md` section 12 |

## 13. Claude Code experiment

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-171 | Position in manuscript | Secondary subsection "Application to AI-assisted neuronal-model transformation"; Claude not in the paper title | not implemented | No `manuscript/` directory |
| R-172 | Task types | Repair a seeded unit error | implemented | `agent_study/tasks/t01_unit_repair/`; test `test_nine_tasks_cover_the_specification_task_types` |
| R-173 | Task types | Restore a changed stimulus protocol | implemented | `agent_study/tasks/t02_stimulus_restore/` |
| R-174 | Task types | Rename a channel safely | implemented | `agent_study/tasks/t03_channel_rename/` |
| R-175 | Task types | Refactor included model files | implemented | `agent_study/tasks/t04_include_refactor/`; test `test_refactored_hh_model_validates_and_reproduces_reference` |
| R-176 | Task types | Convert a quantity to an equivalent unit | implemented | `agent_study/tasks/t05_unit_conversion/`; test `test_score_trial_real_layers_on_hh_unit_conversion` |
| R-177 | Task types | Change one specified conductance while preserving all other parameters | implemented | `agent_study/tasks/t06_single_conductance_change/` (no `canonical_reference.json` in its public tests) |
| R-178 | Task types | Repair a channel reference | implemented | `agent_study/tasks/t07_channel_reference_repair/` |
| R-179 | Task types | Improve runtime without changing tested outputs | implemented | `agent_study/tasks/t08_runtime_improvement/`; its success threshold (at least a 2x step reduction) is provisional (`docs/build_notes/agent-study.md`) |
| R-180 | Task types | Diagnose why a schema-valid model changed firing behaviour | implemented | `agent_study/tasks/t09_behaviour_diagnosis/` |
| R-181 | Task types (derived) | Hidden specs and evaluators reviewed, ideally revised, by a human other than the builder; permanent storage location | decision pending | D-022, N-12; `agent_study/hidden/*/hidden_checks.yaml` (Git-ignored, `status: provisional`), `agent_study/HIDDEN_MANIFEST.sha256` |
| R-182 | Isolation protocol | Freeze NeuroSem before agent testing | human step pending | `agent.freeze_hashes`, `load_frozen_config`; test `test_load_frozen_config_requires_every_hash_and_refuses_provisional`. No frozen agent config exists |
| R-183 | Isolation protocol | Give the agent only public tests | implemented | `agent.prepare_trial`; `configs/agent_policy.yaml: export.framework_include: []`; test `test_prepare_trial_exports_only_public_material` |
| R-184 | Isolation protocol | Hide selected perturbation protocols and answer keys | implemented | `agent.MANDATORY_EXCLUDES`, `scan_for_leaks`; tests `test_export_tree_never_exports_hidden_material_even_if_everything_is_included`, `test_prompts_do_not_reveal_hidden_checks`, `test_exported_timestamps_do_not_reveal_the_seeded_file` |
| R-185 | Isolation protocol | Start every trial from the same clean commit | implemented | `prepare_trial` refuses uncommitted inputs; tests `test_prepare_trial_refuses_uncommitted_inputs`, `test_prepare_trial_is_deterministic_and_refuses_unsafe_locations` |
| R-186 | Isolation protocol | Fresh, isolated sessions | human step pending | `configs/agent_policy.yaml: isolation` (fresh session, dedicated OS account/VM); `docs/build_notes/agent-study.md` says OS-level isolation is a human responsibility |
| R-187 | Isolation protocol | Record Claude Code version, model identifier, access date, permissions, budget, prompts, transcripts, patches, logs and costs | implemented | `agent.TrialLog` fields (`claude_code_version`, `model_identifier`, `access_date`, `permissions_sha256`, `budget`, `prompt_sha256`, `transcript_path`, `patch_path`, `logs`, `costs`); tests `test_trial_log_validation`, `test_trial_log_rehashes_files_and_checks_the_patch` |
| R-188 | Isolation protocol | Prohibit manual intervention during autonomous trials | partially implemented | `TrialLog.human_interventions` must be empty (`validate_trial_log`); enforcement during a trial is procedural (`docs/agent_study_protocol.md` section 3) |
| R-189 | Isolation protocol | Score outputs with deterministic hidden tests | implemented | `agent.score_trial`, `neurosem evaluate-agent`; tests `test_score_trial_cascade_and_error_handling`, `test_hidden_evaluators_on_correct_and_wrong_solutions` |
| R-190 | Isolation protocol | Audit every patch manually after automatic scoring | human step pending | `docs/agent_study_protocol.md` section 5; `configs/agent_policy.yaml: scoring.manual_patch_audit_after_scoring: required` |
| R-191 | Isolation protocol (derived, D-003) | Trials are not run by the assistant that built the evaluator | gated by design | DECISIONS.md D-003; `configs/agent_policy.yaml` header ("The harness never launches an agent") |
| R-192 | Isolation protocol (derived) | Approve budgets, permissions and the public spike-time tolerance before freezing | decision pending | `configs/agent_policy.yaml` (`status: provisional`; 80 turns, 60 min, 15 USD; `spike_time_abs_tol_ms: 1.0`) |
| R-193 | Permitted claim | Only "under the evaluated configuration, a specified fraction passed basic checks but failed frozen perturbation tests" | implemented | `docs/agent_study_protocol.md` "Permitted claim"; test `test_summarize_scores_reports_the_permitted_claim_fraction` |
| R-194 | Prohibited claim | Never claim coding agents generally cannot be trusted in computational neuroscience | implemented | `docs/agent_study_protocol.md` "Prohibited claim" |
| R-195 | AI-assisted development policy | Human controls scientific ground truth, design, thresholds, exclusions, interpretation and final claims | human step pending | DECISIONS.md "Decisions Neel must make" (N-01..N-12); `AI_USE_LOG.md` Entry 002: "All code is pending Neel's review" |
| R-196 | AI-assisted development policy | Disclose substantive generative-AI use; suggested disclosure text | partially implemented | `docs/ai_disclosure.md` (draft). Sections 2-3 still say "No log entry yet" and "[to confirm: Neel ...]", which is stale against `AI_USE_LOG.md` Entry 002 |

## 14. AI-use-log fields (`AI_USE_LOG.md`)

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-197 | AI_USE_LOG.md | Date and time | partially implemented | Entries 001 and 002 record a date (2026-09-13) but no time |
| R-198 | AI_USE_LOG.md | Tool and model identifier | implemented | Both entries: Claude Code desktop, `claude-opus-5` |
| R-199 | AI_USE_LOG.md | Task requested | implemented | Entry 001 "Input"; Entry 002 "Human instruction" |
| R-200 | AI_USE_LOG.md | Prompt or transcript path | partially implemented | Entry 002 gives a transcript folder and session id. Entry 001's field table gives a workflow run id, but no transcript path appears in that table |
| R-201 | AI_USE_LOG.md | Files changed | partially implemented | Entry 002 lists modules and directories, not a per-file list |
| R-202 | AI_USE_LOG.md | Human review performed | human step pending | Entry 002: "All code is pending Neel's review" |
| R-203 | AI_USE_LOG.md | Tests executed | implemented | Entry 002 "Tests executed" |
| R-204 | AI_USE_LOG.md | Problems found | implemented | Entry 002 "Problems found and handled" |
| R-205 | AI_USE_LOG.md | Accepted, modified or rejected | human step pending | Entry 002 "Accepted, modified, or rejected": pending review |

## 15. Repository architecture

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-206 | Repository architecture | README.md, LICENSE, CITATION.cff, pyproject.toml | implemented | Files present; test `test_citation_cff_core_fields` |
| R-207 | Repository architecture | environment.yml | partially implemented | Present; test `test_environment_yml_is_python312_plus_lock`; never tested with conda (`docs/REPRODUCING.md`) |
| R-208 | Repository architecture | Dockerfile | partially implemented | Present; test `test_dockerfile_pins_base_digest_java_and_runs_unprivileged`; "NEVER BUILT" (Dockerfile header, `docs/REPRODUCING.md`) |
| R-209 | Repository architecture | Makefile | partially implemented | Present; test `test_makefile_targets_and_tab_indented_recipes`; never executed (GNU make not installed) |
| R-210 | Repository architecture | `.github/workflows/ci.yml` | partially implemented | Present; test `test_ci_workflow_structure`; never run (no GitHub remote, N-01) |
| R-211 | Repository architecture | `configs/` study, tolerances, features and agent_policy YAML | implemented | All four present, all `status: provisional` |
| R-212 | Repository architecture | `data/model_manifest.csv`, `data/protocol_manifest.csv`, `data/splits/` | implemented | Present; test `test_committed_manifest_is_up_to_date` |
| R-213 | Repository architecture | `data/mutation_manifest.csv`, `data/valid_transforms.csv` | partially implemented | Not in `data/`; written per campaign at `results/processed/<campaign>/mutation_manifest.csv` and `valid_transforms.csv` (`docs/ARCHITECTURE.md` section 2 still lists `data/`) |
| R-214 | Repository architecture | `models/raw`, `models/curated`, `models/snapshots` | partially implemented | `models/raw/` holds commit-pinned snapshots, and `models/candidates/` exists; `curated/` and `snapshots/` are absent |
| R-215 | Repository architecture | `src/neurosem/` cli, schemas, provenance and simulators (base, jneuroml, neuron) | implemented | Files present (`neuron.py` is a stub) |
| R-216 | Repository architecture | `protocols/`, `features/`, `mutations/`, `transforms/`, `validation/`, `selection/`, `analysis/` with the listed files | implemented | All listed files present; extra `transforms/formatting.py` |
| R-217 | Repository architecture | `experiments/` pilot, discovery, heldout, agent | implemented | Present, plus `campaign.py` and `analyze.py`; no direct tests for pilot, discovery, heldout or campaign (see "How this was checked") |
| R-218 | Repository architecture | `tests/unit`, `tests/integration`, `tests/regression`, `tests/fixtures` | partially implemented | `unit/` and `integration/` present (980 tests collected); `regression/` and `fixtures/` absent (fixture models live in `models/raw/`) |
| R-219 | Repository architecture | `workflows/` run_reference, generate_mutants, calibrate_tolerances, select_protocols, evaluate_heldout | implemented | All five present as thin wrappers over `neurosem.cli.main` |
| R-220 | Repository architecture | `results/raw`, `processed`, `tables`, `figures` | partially implemented | `raw/` and `processed/` exist (pilot, incomplete); `tables/` and `figures/` absent (created by `analyze`, not yet run) |
| R-221 | Repository architecture | `docs/` glossary, model_selection, protocol_catalog, mutation_catalog, statistical_plan, ai_disclosure | implemented | Present; tests `test_doc_exists_and_has_title`, `test_mutation_catalog_covers_every_operator_and_transform`, `test_protocol_catalog_timing_table_matches_code` |
| R-222 | Repository architecture | `docs/novelty_matrix.csv` | implemented | `docs/novelty_matrix.csv` (same as R-005) |
| R-223 | Repository architecture | `manuscript/manuscript.md`, `supplement.md` | not implemented | Absent |

## 16. Per-simulation data requirements and suggested commands

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-224 | Data requirements | Unique run ID | implemented | `schemas.RunRecord.run_id`, content-addressed (D-012); `validation/execution.RunRecorder`; `tests/integration/test_run_recorder.py` |
| R-225 | Data requirements | Model ID and file hash | implemented | `model_id`, `variant_tree_sha256`; the inputs hash is folded into `run_id` (`docs/ARCHITECTURE.md` section 2); test `test_inputs_manifest_changes_when_any_reachable_file_changes` |
| R-226 | Data requirements | Source-model snapshot | partially implemented | No `snapshot` field in `RunRecord`; derivable from `model_id` through the manifest `snapshot` column plus `variant_tree_sha256` |
| R-227 | Data requirements | Protocol ID | implemented | `protocol_ids` |
| R-228 | Data requirements | Mutation or transformation ID | implemented | `variant_id` |
| R-229 | Data requirements | Simulator and version | implemented | `simulator`, `simulator_version` (e.g. "jNeuroML 0.14.0 / jLEMS 0.12.0" in a pilot `run.json`) |
| R-230 | Data requirements | Time step and duration | implemented | `dt_ms`, `duration_ms` |
| R-231 | Data requirements | Random seed, if relevant | implemented | `seed` |
| R-232 | Data requirements | Container/environment digest | implemented | `environment_digest` (Python environment, Java, jar hash; `container_image` when `NEUROSEM_CONTAINER_IMAGE` is set); test `test_environment_digest_extra_changes_digest_without_leaking_into_cache`. No container has been built |
| R-233 | Data requirements | Execution status and runtime | implemented | `status`, `runtime_s` |
| R-234 | Data requirements | Trace path and hash | implemented | `trace_path`, `trace_sha256` (traces Git-ignored, hash tracked, D-012) |
| R-235 | Data requirements | Feature-table path and hash | implemented | `feature_path`, `feature_sha256` |
| R-236 | Data requirements | Timestamp and Git commit | implemented | `timestamp_utc`, `git_commit`, `git_dirty` (D-023); tests `test_git_state_in_repository`, `test_utc_now_is_iso_utc` |
| R-237 | Data requirements | Raw results are immutable | implemented | `provenance.write_immutable`; tests `test_write_immutable_creates_read_only_file`, `test_different_content_raises_and_preserves_original` |
| R-238 | Data requirements | Derived results reproducible from raw outputs with one workflow command | partially implemented | `neurosem reproduce-paper` (`experiments/analyze.reproduce_paper`); never run (`docs/REPRODUCING.md`) |
| R-239 | Suggested commands | `validate-models`, `run-reference`, `calibrate-tolerances`, `generate-mutants`, `classify-mutants`, `build-fingerprints`, `select-protocols --budget`, `evaluate-agent`, `analyze`, `reproduce-paper` | implemented | `src/neurosem/cli.py` subparsers; `validate-models` ran on RS (`docs/REPRODUCING.md`); the other commands have no behavioural test |
| R-240 | Suggested commands | `evaluate-heldout` | gated by design | `cli.py` help "GATED held-out evaluation (requires configs/FROZEN.lock)" |

## 17. Milestone deliverables and exit criteria

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-241 | Milestone 0 | Dependency and version audit | implemented | `DEPENDENCY_AUDIT.md` (untracked); `docs/m0_evidence/tools/*.verify.json`; D-004 |
| R-242 | Milestone 0 | License audit | implemented | `LICENSE_AUDIT.md` (untracked); `docs/m0_evidence/model_curation/license_evidence.json` |
| R-243 | Milestone 0 | Name-conflict search | implemented | `docs/NAME_CONFLICT_AUDIT.md` (untracked); `docs/m0_evidence/names/`; outcome N-10 |
| R-244 | Milestone 0 | Prior-art matrix | implemented | `docs/novelty_matrix.csv` and `PRIOR_ART_AUDIT.md` (with novelty stress test); human spot-check of closeness-3 rows pending |
| R-245 | Milestone 0 | Risk register | implemented | `RISK_REGISTER.md` (45 risks, handoff-assumption review, pivot-criterion mapping) |
| R-246 | Milestone 0 | Decision log | implemented | `DECISIONS.md` (D-001..D-023, N-01..N-12) |
| R-247 | Milestone 0 (handoff) | Also PLAN.md, REQUIREMENTS.md, CHANGELOG.md, AI_USE_LOG.md | implemented | `PLAN.md`, `REQUIREMENTS.md` (this file), `CHANGELOG.md`, `AI_USE_LOG.md` present |
| R-248 | Milestone 0 | Stop before implementation and request approval | implemented | D-003 records Neel's instruction of 2026-09-13 and the gates kept |
| R-249 | Milestone 1 | Python package and frozen dependencies | implemented | `pyproject.toml`, `requirements.lock`; fresh Windows install verified (`docs/REPRODUCING.md`); test `test_lock_satisfies_pyproject_requirements` |
| R-250 | Milestone 1 | jNeuroML execution and eFEL installation | implemented | D-004; `tests/integration/test_jneuroml_adapter.py::test_version_info_matches_audited_versions`; `tests/unit/test_efel_adapter.py` |
| R-251 | Milestone 1 | Docker environment and continuous integration | partially implemented | See R-208, R-210 (never built or run) |
| R-252 | Milestone 1 | Two tiny fixture models | implemented | `pospischil2008_rs`, `pospischil2008_lts` in `models/raw/PospischilEtAl2008@049081c3/` (D-017) |
| R-253 | Milestone 1 exit | One command validates and simulates both fixtures on a clean installation | partially implemented | `neurosem smoke` (`scripts/smoke_jnml.py`) validates, runs the harness, finds rheobase and runs the battery. Clean installs checked only as a Windows venv plus an emulated Docker context running `validate-models` on RS; no clean-install smoke of both fixtures is recorded |
| R-254 | Milestone 2 | Trace format | implemented | `trace_metrics.pack_traces` / `unpack_traces`; test `test_pack_unpack_round_trip_matches_the_npz_format` |
| R-255 | Milestone 2 | Provenance records and feature extraction | implemented | R-224..R-237, R-074 |
| R-256 | Milestone 2 | Deterministic rerun test | implemented | `determinism.json` (reference stage); test `test_cache_immutability_reproducibility_and_feature_rekeying` |
| R-257 | Milestone 2 | Basic plots for manual inspection | not implemented | No trace-inspection plotting step found in `campaign.py` or `scripts/smoke_jnml.py`; only the paper figures in `analysis/figures.py` |
| R-258 | Milestone 2 exit | Repeated runs give the same conclusions within predeclared tolerance | partially implemented | Bitwise battery determinism per reference; no test reruns a campaign and compares classifications |
| R-259 | Milestone 3 | Weak and strong steps, rheobase search, long step, ramp, hyperpolarisation and rebound | implemented | R-052 |
| R-260 | Milestone 3 exit | Protocol timing and current amplitudes independently tested | implemented | tests `test_pulse_onset_is_exactly_at_settle`, `test_second_paired_pulse_starts_where_protocol_says`, `test_edges_fall_on_every_refinement_grid`, `test_protocol_catalog_timing_table_matches_code` |
| R-261 | Milestone 3 exit | Protocol timing and amplitudes visually verified | human step pending | No visual-verification record found |
| R-262 | Milestone 4 | Three pilot families, one-change-per-mutant enforcement, machine-readable provenance, validity and execution classification | implemented | R-022, R-107, R-110, R-111; `mutations/base.write_manifest`, `variant.json`; test `test_generation_writes_loadable_variants_and_manifest` |
| R-263 | Milestone 4 exit | At least 20 manually audited mutants match their labels | human step pending | `campaign.aggregate` writes `mutant_audit_sheet.csv` for the pilot (running; not yet written); `pilot.py` states that a human must audit at least 20 |
| R-264 | Milestone 5 | eFEL adapter, trace metrics, convergence calibration, per-mutant diagnostic reports, detection matrix | implemented | `features/`, `validation/convergence.py`, `campaign._write_diagnostic` (`variants/<id>/diagnostic.md`), `detection_matrix.csv`; no direct test of `_write_diagnostic` |
| R-265 | Milestone 5 exit | Every detected mutant linked to protocol, feature, threshold and evidence trace | partially implemented | `fingerprint.Detection` carries `protocol_id`, `feature`, `tau`, `ref_run_id`, `var_run_id`; `write_detections`. No test asserts this for every detection in a campaign; pilot outputs pending |
| R-266 | Milestone 6 | Run 2-6 models and 20-60 mutants | partially implemented | Campaign `pilot`, 2 models, 52 generated mutants: running; results pending |
| R-267 | Milestone 6 | Continue only if canonical misses reproducible non-equivalent mutants that other protocols detect without unacceptable false positives | human step pending | `pilot_report.md` (to be generated by `pilot.write_report`); decision by Neel; thresholds N-04 |
| R-268 | Milestone 6 | If no hidden drift exists, do not manufacture it; reframe or stop | implemented | `experiments/pilot.py` docstring and report logic ("recommends reframing or stopping") |
| R-269 | Milestone 7 | Frozen discovery and held-out splits | human step pending | R-028, R-140, R-144 |
| R-270 | Milestone 7 | Greedy coverage selection, random cost-matched baselines, leakage tests | implemented | R-128, R-132, R-133, R-142 |
| R-271 | Milestone 8 | Preregistration | human step pending | `docs/preregistration_draft.md` (template); `docs/preregistration.md` absent |
| R-272 | Milestone 8 | Frozen configurations and hashes | gated by design | `configs/FROZEN.lock` absent; no writer exists (R-125) |
| R-273 | Milestone 8 | Full execution logs and statistical analysis | gated by design | Analysis code exists (R-148..R-158); execution awaits the freeze |
| R-274 | Milestone 8 | Robustness and ablation analyses | partially implemented | Tolerance robustness implemented (R-158); no ablation code (`docs/preregistration_draft.md` line 238 blank) |
| R-275 | Milestone 9 | Frozen prompts | partially implemented | `agent_study/tasks/*/prompt.md`, hashed by `agent.freeze_hashes`; status provisional |
| R-276 | Milestone 9 | Isolated Claude Code trials, raw transcripts and patches, hidden evaluation results | gated by design | D-003; none exist (`AI_USE_LOG.md`: "None exist yet") |
| R-277 | Milestone 9 | Manual patch audit | human step pending | R-190 |
| R-278 | Milestone 10 | Public repository | decision pending | N-01 (no remote) |
| R-279 | Milestone 10 | Versioned release and DOI-minting archive | gated by design | D-003 ("no public release or DOI without Neel"); rename recommended first (N-10) |
| R-280 | Milestone 10 | Reproduction guide | partially implemented | `docs/REPRODUCING.md` covers the environment and pipeline commands; there are no paper results yet to reproduce |
| R-281 | Milestone 10 | Manuscript and supplement | not implemented | No `manuscript/` |
| R-282 | Milestone 10 | Data, code and AI-use statements | partially implemented | `docs/ai_disclosure.md` (draft), `CITATION.cff`, `LICENSE`; no data statement |
| R-283 | Milestone 10 | Venue-specific IEEE formatting only after choosing a target | gated by design | Venue not chosen (handoff "Final decision rule") |

## 18. Required controls

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-284 | Required controls | No-change controls (formatting and documentation edits preserve behaviour) | implemented | R-078; `VariantKind.NO_CHANGE` |
| R-285 | Required controls | Valid-transformation controls estimate false positives | implemented | R-077..R-085, R-155 |
| R-286 | Required controls | Deterministic mutation controls verify validator sensitivity | implemented | Seeded deterministic generation; test `test_generation_is_deterministic_and_uses_documented_rng` |
| R-287 | Required controls | Canonical baseline | implemented | R-057 (metric choice N-06) |
| R-288 | Required controls | Random battery baseline | implemented | R-132, R-133 |
| R-289 | Required controls | Exhaustive empirical battery | implemented | R-134 (10 implemented protocols; P11 and P12 deferred) |
| R-290 | Required controls | Numerical-refinement control | implemented | R-112, R-123; D-013, D-014 |
| R-291 | Required controls | Held-out models | decision pending | R-028 |
| R-292 | Required controls | Held-out mutation family | decision pending | R-140 |
| R-293 | Required controls | Agent isolation | partially implemented | R-183..R-186 (OS-level isolation is a human step) |

## 19. Required figures

Each figure function takes processed tables and is tested on synthetic inputs in `tests/unit/test_figures.py`. No figure has been produced (`results/figures/` absent).

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-294 | Required figures 1 | Concept: similar canonical responses but divergence under another stimulus | implemented | `analysis/figures.fig1_concept`; test `test_fig1_concept` |
| R-295 | Required figures 2 | Validation cascade | implemented | `fig2_validation_cascade`; tests `test_fig2_validation_cascade`, `test_fig2_battery_cascade_does_not_call_missed_mutants_equivalent` |
| R-296 | Required figures 3 | Detection heat map grouped by model and family | implemented | `fig3_detection_heatmap`; test `test_fig3_detection_heatmap` |
| R-297 | Required figures 4 | Efficiency curve: canonical, random, selected and exhaustive | implemented | `fig4_efficiency_curve`; test `test_fig4_efficiency_curve` |
| R-298 | Required figures 5 | Held-out generalisation | gated by design | `fig5_heldout_generalization` exists (test `test_fig5_heldout_generalization`); its data need held-out evaluation |
| R-299 | Required figures 6 | False positives and tolerance sensitivity | implemented | `fig6_false_positives`; test `test_fig6_false_positives` |
| R-300 | Required figures 7 | Two or three interpretable case studies | implemented | `fig7_case_studies`, `analyze.case_traces`; test `test_fig7_case_studies`. Choosing the cases is Neel's interpretation |
| R-301 | Required figures 8 | AI case study by validation layer, clearly secondary | gated by design | `fig8_agent_case_study` exists (test `test_fig8_agent_case_study`); needs trials (R-276) |

## 20. Success and pivot criteria

Status here describes whether the repository can evaluate the criterion. **No criterion has been evaluated.**

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-302 | Success criteria | Hidden, reproducible drift in more than isolated contrived examples | human step pending | Counts from `classification.csv` (class 6); pilot running, results pending; the judgement is Neel's |
| R-303 | Success criteria | Drift includes interpretable feature or firing-regime changes | human step pending | `firing_regime` categorical detection (R-073), `diagnostic.md`, fig7; interpretation is Neel's |
| R-304 | Success criteria | Selected battery materially outperforms canonical | gated by design | R-011; effect size open (R-160) |
| R-305 | Success criteria | Selected battery outperforms cost-matched random selection | gated by design | Held-out comparison (R-130) |
| R-306 | Success criteria | Results generalise to models excluded from selection | gated by design | R-130, R-139 |
| R-307 | Success criteria | False positives on valid transformations are low and transparently reported | decision pending | `metrics.false_positive_summary` with interval; "low" is N-04 (provisional <=10%) |
| R-308 | Success criteria | Conclusions survive reasonable tolerance changes | implemented | R-158 |
| R-309 | Success criteria | Results do not depend entirely on Claude Code errors | implemented | The primary population is controlled mutants; the agent study is separate (`AI_USE_LOG.md` two roles, `docs/agent_study_protocol.md`) |
| R-310 | Success criteria | Code and data reproduce the paper's tables and figures | partially implemented | R-238 (`reproduce-paper` never run) |
| R-311 | Failure and pivot criteria | Existing validation detects nearly every meaningful mutation | decision pending | `metrics.validation_cascade` computes it; "nearly every" is undefined |
| R-312 | Failure and pivot criteria | Most mutations only crash or violate schema | implemented | `metrics.class_counts`, `validation_cascade`; test `test_class_counts_include_zero_classes` |
| R-313 | Failure and pivot criteria | Selected protocols do not beat random on held-out models | gated by design | R-130 |
| R-314 | Failure and pivot criteria | False positives remain high | decision pending | N-04 |
| R-315 | Failure and pivot criteria | Result depends on one unstable model | partially implemented | Per-model clusters exist in the bootstrap; no leave-one-model-out or per-model sensitivity analysis found (grep found none) |
| R-316 | Failure and pivot criteria | Findings vanish under numerical refinement | implemented | Reproducibility at h/2 is part of admissibility (R-112); exclusions counted (R-123) |

## 21. Mandatory Claude operating rules (handoff) and related handoff items

The final specification does not repeat these rules; they come from `NEUROSEM_CLAUDE_HANDOFF.extracted.md`. Nothing in the final spec contradicts them.

| ID | Spec section | Requirement (paraphrase) | Status | Evidence |
|---|---|---|---|---|
| R-317 | Mandatory rules (handoff) | Never fabricate papers, APIs, versions, licenses, results or citations | human step pending | Versions verified (`docs/m0_evidence/tools/*.verify.json`, D-004); citation spot-check by Neel still pending (R-006) |
| R-318 | Mandatory rules (handoff) | Verify current APIs and licenses from primary sources | implemented | `docs/m0_evidence/tools/*.research.json` and `*.verify.json`; `LICENSE_AUDIT.md`; `.tools/jdk_provenance.json` (D-004) |
| R-319 | Mandatory rules (handoff) | Do not silently change scientific scope | partially implemented | Changes recorded in D-008, D-009, D-013, D-014 and D-021; the pilot's protocol, feature and mutant counts exceed the pilot targets with no DECISIONS entry (R-020, R-021, R-023, R-024) |
| R-320 | Mandatory rules (handoff) | Do not run held-out evaluation during development | gated by design | D-003; `HeldoutGate`; no `FROZEN.lock` and no `results/heldout_access.log` exist |
| R-321 | Mandatory rules (handoff) | Do not tune thresholds after held-out inspection | gated by design | R-125, R-126 |
| R-322 | Mandatory rules (handoff) | Do not call finite testing a formal equivalence proof | implemented | R-009; class 4 is "equivalent within tested domain" (`schemas.MutantClass`) |
| R-323 | Mandatory rules (handoff) | Do not treat every parameter change as a defect | implemented | Equivalent mutants are not misses (`docs/mutation_catalog.md` section 5.1); test `test_fig2_battery_cascade_does_not_call_missed_mutants_equivalent` |
| R-324 | Mandatory rules (handoff) | Do not write result claims before data exist | implemented | R-003; this document makes no result claims |
| R-325 | Mandatory rules (handoff) | Add tests before or with implementation | partially implemented | 980 tests collected; `experiments/campaign.py`, `pilot.py`, `discovery.py`, `heldout.py`, most of `analyze.py`, and CLI behaviour lack direct tests |
| R-326 | Mandatory rules (handoff) | Use a branch and a milestone report for each stage | partially implemented | D-001 says one branch per milestone, but M0-M7 work is all on `m0-audit`; no milestone reports found (the pilot report is pending) |
| R-327 | Mandatory rules (handoff) | Stop for Neel's approval after every milestone | partially implemented | D-003: one instruction was taken as approval for M1-M7 while the integrity gates were kept; M6 and later decisions still need Neel |
| R-328 | Mandatory rules (handoff) | Explain all scientific decisions in plain English | implemented | DECISIONS.md; `docs/neel_learning_guide.md` |
| R-329 | Neel's required knowledge (handoff) | Before the frozen study Neel can explain the 14 listed concepts without Claude | human step pending | `docs/neel_learning_guide.md`; test `test_learning_guide_has_fourteen_items_each_with_two_question_self_check` |
| R-330 | Recommended publication sequence | Complete the novelty review before expanding; freeze before the held-out experiment; no simultaneous journal and conference submission; check the current venue call | human step pending | R-004, R-005 (novelty review incomplete); R-271, R-272; venue not chosen |

---

## Status counts

| Status | Count |
|---|---|
| implemented | 196 |
| partially implemented | 47 |
| not implemented | 8 |
| gated by design | 23 |
| human step pending | 30 |
| decision pending | 26 |
| **Total** | **330** |

"Implemented" means the code or document exists with a test, config key or document behind it. It does not mean scientific validation, and it does not mean Neel has reviewed it (AI_USE_LOG.md Entry 002: all code pending review).

## Most important gaps for the pilot (Milestone 6)

1. **Pilot results are pending.** The run is in progress. The continue-or-pivot decision (R-267) and pilot success criteria (R-026) wait for `pilot_report.md` and your review.
2. **Manual audit of at least 20 mutants** (R-263). This is the Milestone 4 exit criterion. The audit sheet is written by the pilot.
3. **Pilot decision thresholds** (N-04: at most 25% features excluded, at most 10% false positives) are provisional (R-026, R-307, R-314). "Nearly every mutation detected" has no operational threshold (R-311).
4. **Pilot scope exceeds the specification's pilot targets.** 10 protocols instead of 4, 18 features instead of 3-5, 26 mutants per model instead of 5-10, 7 valid transforms per model instead of 4-6. This is not recorded as a decision (R-020, R-021, R-023, R-024, R-319).
5. **Visual verification of protocol timing** has not been done (R-261). Basic trace plots for manual inspection do not exist (R-257). Low-rheobase amplitudes for LTS are unresolved (N-07, R-056).
6. **Tolerance calibration compares features, not traces** (R-118, R-119). The `tolerance_proposal.yaml` promised by `configs/tolerances.yaml` has no writer (R-124). Final constants are N-03.
7. **The pipeline that produces the pilot has no direct tests.** `campaign.py`, `pilot.py`, the diagnostics and the detection-link exit criterion are untested (R-264, R-265, R-325).
8. **Canonical metric choice (N-06) and stimulus-family treatment** are open (R-058, R-109). The pilot models have no sag/Ih behaviour (R-045). `reduce_spatial_discretization` is never exercised on single-compartment models (R-104).

## Most important gaps for the frozen study (Milestones 7-10)

1. **Model set.** 6 manifest models, 2 included, from 3 source families, against 12-16 needed with independent held-out sources (R-027, R-028, R-159).
2. **Splits.** No held-out models or family assigned (N-02) and no `SPLITS.sha256` (R-140, R-144, R-269).
3. **Freeze mechanism.** Nothing writes `configs/FROZEN.lock`, yet the held-out gate, tolerance freeze and frozen selection depend on it (R-125, R-129, R-272).
4. **Preregistration** is a template with blanks. Items still open: effect size and decision rule, clustering rule, budget k, whether canonical is a candidate, P03 cost, lockbox and ablations (R-160..R-170, R-137, R-147, R-274).
5. **Milestone 0 documents: complete, pending review.** `docs/novelty_matrix.csv`, `PRIOR_ART_AUDIT.md`, `RISK_REGISTER.md` and `PLAN.md` were written in parallel with this file. Citations need your spot-check before any novelty claim (R-005, R-244, R-006).
6. **Reproducibility infrastructure never executed.** Docker, CI, Make and conda have never run, and `reproduce-paper` has never run (R-207..R-210, R-238). There is no GitHub remote (N-01).
7. **Mutation scope.** 4 families against a 6-8 target (R-030). No compound-fault stress test (R-108).
8. **Agent study.** 9 task definitions against 20-30 planned (R-033). Hidden evaluators were written by the builder and need independent review and a permanent home (N-12, R-181). OS-level isolation, the frozen agent config and the manual patch audit are human steps (R-182, R-186, R-190). Budgets and permissions await approval (R-192).
9. **Release and manuscript.** No manuscript, no data statement, and the AI disclosure draft is stale against the log (R-196, R-281, R-282). A rename is recommended before any public release (N-10).
10. **AI_USE_LOG fields.** No time of day, no per-file change lists, and human review and acceptance still pending (R-197, R-200, R-201, R-202, R-205).
