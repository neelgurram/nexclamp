# Model selection

*Status: draft, 2026-09-13. Sources: final specification ("Model selection"),
`data/model_manifest.csv`, `models/raw/*/PROVENANCE.json`, and the Milestone 0 evidence in
`docs/m0_evidence/fixtures/fixture_candidates.json` and `fixture_verify.json`. Behaviour
descriptions marked **expected** are expectations from upstream reference files or
channel content, not NeuroSem results. No held-out assignment is made or implied here.*

## 1. Inclusion criteria

The specification requires every reference model to meet all of the following. The table
shows how NeuroSem checks each one.

| # | Criterion (specification) | How NeuroSem checks it |
|---|---|---|
| 1 | Traceable public source | `source_url` + pinned `commit`; files fetched from commit-pinned raw URLs (`scripts/fetch_models.py`) |
| 2 | License permitting intended use and redistribution, or handled without redistribution | License text read at the pinned commit before download; recorded in `license`, `license_url` and `PROVENANCE.json` |
| 3 | Passes current NeuroML validation | `jnml -validate` (jNeuroML 0.14.0) is authoritative; libNeuroML 0.6.7 check recorded as informational (section 6) |
| 4 | Executes deterministically in the frozen environment | Repeated runs must give the same conclusions within predeclared tolerance (Milestone 2 exit test) |
| 5 | Completes candidate protocols within practical runtime | Cost in cell-steps per protocol (`docs/protocol_catalog.md`) plus measured wall time |
| 6 | Produces interpretable voltage output | Harness has a membrane-voltage `OutputColumn` (`harness_v_column`) |
| 7 | Responds meaningfully to current injection | Rheobase search returns status `ok` (not `not_found`), and the reference is not spontaneously active |
| 8 | Scientific provenance to a publication or established repository | `citation` verified against Crossref/PubMed in M0 evidence |
| 9 | No unavailable proprietary dependency | Only NeuroML/LEMS files plus open tools (jNeuroML, eFEL) |

**Diversity goals.** The specification prefers a small set spanning tonic spiking,
spike-frequency adaptation, bursting, rebound firing, sag, and distinct excitability
thresholds. It asks to begin with single-compartment or simple models and to add only a
few multicompartment models once the pipeline is stable.

Current coverage of the diversity goals. Every entry is **expected**, from upstream
reference spike times or channel content, and none has been confirmed with NeuroSem
protocols yet.

| Behaviour | Candidate(s) | Basis | Status |
|---|---|---|---|
| Tonic spiking | FS, HH example, Wang-Buzsaki | Near-constant ISIs in OMV reference spike times | expected |
| Spike-frequency adaptation | RS | Reference ISIs 28.0, 39.4, 68.7, 135.4 ms; IM channel present | expected |
| Bursting | IB (label only); LTS early spike pair | Reference spike groups | expected, weak |
| Rebound firing | LTS | IT (T-type Ca) present; no upstream test exercises hyperpolarisation | expected, unverified |
| Sag | none | No manifest model contains an Ih/HCN channel | **gap** (section 7) |
| Distinct thresholds | all | Different leak and channel densities | to measure (rheobase) |

## 2. Provenance record

The specification lists the fields to record for each model. This table shows where each
one lives.

| Specification field | NeuroSem location | Notes |
|---|---|---|
| Internal ID | `model_id` | stable key used everywhere |
| Model name | `name` | |
| Scientific citation | `citation` | DOI included; M0 evidence verified DOIs via Crossref |
| Source URL | `source_url` + `commit` | commit SHA pin, not a branch |
| Download date | `download_date`; `PROVENANCE.json` `downloaded_utc` | |
| License and license URL | `license`, `license_url`; `PROVENANCE.json` `license` | per-directory carve-outs recorded in text |
| Original files | `PROVENANCE.json` `files` (path, URL, bytes) | |
| SHA-256 hashes | `PROVENANCE.json` `files.*.sha256` and `hash_check` | `match` = equals the M0-recorded hash; `not-prerecorded` = LICENSE/CITATION files hashed at fetch time |
| Required includes | **not a manifest column**; derivable from the cell file's `<include>` elements | listed in section 3 |
| Simulator version | `simulator` names the tool only; the version and jar SHA-256 are recorded per run (`RunRecord.simulator_version`, environment digest) | model-level version gap, see section 9 |
| Known expected behaviour | `expected_behavior` | phrased as expectation until simulated |
| Inclusion decision and reason | `inclusion` (`include` / `candidate` / `exclude`) and `inclusion_reason` | |

NeuroSem adds fields the pipeline needs: `snapshot`, `cell_file`, `cell_id`,
`harness_lems`, `harness_output_file`, `harness_v_column`, `temperature` and
`source_family`. Models that share a `source_family` are treated as correlated.

## 3. Current manifest (2026-09-13)

Two models are included for the pilot. The other four are candidates, either for the
full study or as fixtures.

| model_id | inclusion | source_family | snapshot (commit) | license (as recorded) |
|---|---|---|---|---|
| `pospischil2008_rs` | **include** (pilot fixture 1) | pospischil2008 | PospischilEtAl2008@049081c3 | MIT (NeuroML2 directory) |
| `pospischil2008_lts` | **include** (pilot fixture 2) | pospischil2008 | PospischilEtAl2008@049081c3 | MIT (NeuroML2 directory) |
| `pospischil2008_fs` | candidate | pospischil2008 | PospischilEtAl2008@049081c3 | MIT (NeuroML2 directory) |
| `pospischil2008_ib` | candidate | pospischil2008 | PospischilEtAl2008@049081c3 | MIT (NeuroML2 directory) |
| `nml2_hh_example` | candidate | neuroml2_examples | NeuroML2@a5f5dadc | LGPL-3.0 |
| `wangbuzsaki1996_wb` | candidate | wangbuzsaki1996 | WangBuzsaki1996@c5322844 | MIT (NeuroML2 directory) |

Model contents and shipped canonical harness, read from the pinned files:

| model_id | channels (density, erev) | includes | init V | shipped harness (canonical protocol) |
|---|---|---|---|---|
| RS | Leak 0.1 mS/cm2 (-70 mV); Kd 5.0 mS/cm2 (-100); IM 0.07 mS/cm2 (-100); Na 50 mS/cm2 (+50, `channelDensityVShift`) | Kd, IM, Leak, Na | -70 mV | 0.75 nA step, 300-700 ms; 1000 ms at step 0.001 ms; 36 degC |
| LTS | Leak 1e-5 S/cm2 (-85); Na 0.05 S/cm2 (+50); Kd 0.005 S/cm2 (-100); IM 3e-5 S/cm2 (-100); IT 4e-4 S/cm2 (Nernst, ca) + Ca pool | Leak, Na, Kd, IM, IT, Ca | -84 mV | 0.15 nA step, 400-800 ms; 1000 ms at 0.001 ms; 36 degC |
| FS | Leak 0.15 mS/cm2 (-70); Na 50 (+50); Kd 10 (-100) | Kd, IM (included but no IM density), Leak, Na | -70 mV | 0.5 nA, 300-710 ms; 1000 ms at 0.001 ms |
| IB | Leak 0.01 mS/cm2 (-85); Na 50; Kd 5; IM 0.03; IL 1.7e-4 S/cm2 (fixed erev 120.2547 mV) + Ca pool | Leak, Na, Kd, IM, IL, Ca | -84 mV | 0.15 nA from 500 ms for 2000 ms, **but the simulation is 1000 ms** (step outlasts the run) |
| HH example | leak 3.0 S/m2 (-54.3); Na 120 mS/cm2 (+50); K 360 S/m2 (-77); channels defined in the same file | none | -65 mV | 0.08 nA, 100-200 ms; 300 ms at 0.01 ms |
| Wang-Buzsaki | Na 35 mS/cm2 (+55, instantaneous m via custom gate type); K 9 mS/cm2 (-90); leak 0.1 mS/cm2 (-65) | none | -70 mV | 2 pA from **0 ms**, 100 ms; 100 ms at 0.001 ms; 37 degC |

Upstream expected behaviour (OMV `.mep` reference spike times, generated upstream and
**not** by NeuroSem):

- RS: 320.554, 348.522, 387.944, 456.69, 592.105 ms. Five spikes with lengthening
  intervals, so adaptation is **expected**.
- LTS: 431.423, 445.189, 517.237, 720.422 ms, plus Ca-concentration crossings at 430.315
  and 443.502 ms. An early spike pair aligned with Ca transients is consistent with a
  low-threshold Ca response (interpretation unverified).
- FS: 20 spikes from 317.023 to 700.299 ms, ISIs about 20.17 ms. Tonic firing is
  **expected**.
- IB: 8 spikes from 617.725 to 672.085 ms. A bursting-type onset is suggested by the label
  only.
- HH example: 7 spikes from 102.22 to 198.6 ms, about 16 ms apart.
- Wang-Buzsaki: 10 spikes from 8.901 to 97.311 ms, about 9.82 ms apart.

Development observation (not a study result): `docs/pilot/dt_probe.md` reran the RS, LTS
and FS harnesses in jNeuroML at six time steps. RS and FS early spikes are stable to about
0.1 ms, but the LTS third spike moves about 50 ms across the tested range.

## 4. Why RS and LTS are the pilot pair

- Both come from one peer-reviewed paper (Pospischil et al. 2008, Biol Cybern 99:427-441,
  DOI verified via Crossref, ModelDB 123623). Both are commit-pinned, and their NeuroML2
  files are MIT.
- Both are true single-compartment conductance-based cells (one soma segment, diameter
  96 um).
- Their behaviours differ in ways the pilot protocols need. RS has the slow IM current
  (adaptation **expected**). LTS adds the T-type Ca current and a Ca pool, so hyperpolarising
  and rebound protocols should be informative (**expected, unverified**).
- Their upstream OMV spike-time tests passed in the repository's CI at the pinned commit
  (GitHub Actions run 30447139603). Passing that finite test is not proof of correctness.

## 5. Known correlation of the four Pospischil cells

RS, LTS, FS and IB are **not independent models**. They share:

- **The same paper, the same conversion to NeuroML, the same repository and the same
  commit** (OpenSourceBrain/PospischilEtAl2008 @ 049081c3).
- **Byte-identical channel files.** The M0 evidence records the same SHA-256 for these
  files in every Pospischil cell's file list:

  | file | SHA-256 (prefix) | used by |
  |---|---|---|
  | `channels/Na/Na.channel.nml` | `7b019f44...` | RS, LTS, FS, IB |
  | `channels/Kd/Kd.channel.nml` | `6cc779cd...` | RS, LTS, FS, IB |
  | `channels/IM/IM.channel.nml` | `9a1fbbc8...` | RS, LTS, IB (FS includes it without a density) |
  | `channels/Leak/Leak.channel.nml` | `41eb0263...` | RS, LTS, FS, IB |
  | `channels/Ca/Ca.nml` | `2bd89c88...` | LTS, IB |

- **The same gating kinetics.** All Na, Kd and IM rate and time-course expressions are the
  same custom LEMS `ComponentType`s. The cells differ mainly in densities, reversal
  potentials, soma size (FS 67 um) and the extra IT or IL channel.

Consequences:

1. A mutation operator that hits a shared channel file makes the same change in the
   same kinetics across all four cells. Detection outcomes across them are therefore
   expected to correlate.
2. Statistical clustering must allow for this. The planned cluster is the base model, and
   a sensitivity analysis clusters by `source_family` (`docs/statistical_plan.md`).
3. **A Pospischil cell in the held-out set is not an unseen model** if another Pospischil
   cell is in the discovery set. Doing so would overstate generalisation. How to split
   source families is a decision for Neel, made before any split file is created.
4. The pilot pair is acceptable for a pipeline pilot but gives **one** independent source.
   The full study needs 12-16 models. The manifest currently spans only three source
   families: pospischil2008, neuroml2_examples and wangbuzsaki1996.

## 6. The LTS validator disagreement

**Facts (from M0 evidence and the manifest):**

- libNeuroML 0.6.7 marks `IT.channel.nml`, `LTS.cell.nml` and `LTS.net.nml` **invalid**.
  The message is that gate `s` has type `IT_s_gate`, which is not in the schema's
  `gateTypes` enumeration (`gateHHrates`, `gateHHratesTau`, `gateHHtauInf`, `gateHHratesInf`,
  `gateHHratesTauInf`, `gateHHInstantaneous`, `gateKS`, `gateFractional`). `IT_s_gate` is a
  custom LEMS `ComponentType` defined in the same file, extending `gateHHtauInf`.
- `jnml -validate` **accepts** `LTS.net.nml` and `LTS.cell.nml`. This was shown in the
  upstream CI log at the pinned commit, and the manifest records LTS as valid under
  `jnml -validate`.
- The M0 verification corrected one detail. libNeuroML's `validate_neuroml2` runs generateDS
  object validation derived from the v2.3.1 schema, not a raw XSD check. Full XSD
  validation from Python goes through jnml and needs Java.
- PyLEMS 0.6.9 cannot simulate LTS. It raises ZeroDivisionError on the first step, which is
  inferred (not confirmed) to come from the tau = 0 `IT_s_gate`. jNeuroML runs it. LTS
  therefore has no Java-free execution path.
- Whether `jnml -validate` descends into included channel files was recorded as unverified
  in M0. `IT.channel.nml` has no standalone upstream validate test.

**Decision in force (ARCHITECTURE.md, validation layer):** `jnml -validate` is the
authoritative structural oracle. The libNeuroML result is stored as informational only.
Otherwise every LTS mutant would be class 1 by construction.

**Consequences to keep in mind:**

- "Structurally valid" in NeuroSem means *valid according to jNeuroML 0.14.0*. The
  validator version is part of the definition and must be reported.
- Validity rules for custom `ComponentType`s are weaker than for core types. A mutation
  inside custom LEMS dynamics may pass `jnml -validate` and fail only at build or run time
  (class 2).
- Transformations such as renaming or unit conversion must handle LEMS-level references and
  expressions inside `IT.channel.nml` and `Ca.nml`, not only NeuroML attributes.

## 7. Open gap: no licensed single-compartment Ih / sag model

- The specification's diversity goals include a sag response, and protocol
  `P07_hyperpolarizing_step` measures `sag_ratio`.
- None of the six manifest models contains an Ih (HCN) channel. This was checked from
  their channel lists: RS Na/Kd/IM/Leak, LTS +IT/Ca, FS Na/Kd/Leak, IB +IL/Ca, HH Na/K/leak,
  Wang-Buzsaki Na/K/leak. Sag ratio is therefore **expected** to carry little information
  in every current model.
- The M0 search found no clearly licensed, minimal single-compartment NeuroML cell with Ih:
  - GitHub code search for `hcn` in OpenSourceBrain `.nml` files returned mostly
    multicompartment Blue Brain and Allen cells and stand-alone channel files.
  - OpenSourceBrain repositories for an Ih thalamic relay model (McCormick & Pape 1990) and
    a TC-cell T-current model (Destexhe et al. 1998) had no LICENSE and no `.nml` files.
  - NeuroML-DB states no model-level license, so each model would need tracing to its
    original source. No individual record was evaluated.
- Options for Neel (no choice is made here):
  1. Continue the search, for example NeuroML-DB records traced to licensed sources, or
     licensed OSB repositories with Ih channel files.
  2. Keep sag as a planned feature but report it as uninformative for the current models.
  3. Drop sag from the diversity goals with a documented reason.

  Writing a new Ih model ourselves would not meet the provenance criterion (publication or
  established repository).

## 8. Candidate-specific issues

- **FS:** includes `IM.channel.nml` but assigns no IM density. An `omit_include` of IM is
  therefore expected to be a no-op, and IM-targeted operators have no density site. Soma
  diameter is 67 um.
- **IB:** the shipped step (500 ms delay, 2000 ms) outlasts the 1000 ms simulation. The
  canonical analysis window is clipped to the simulation end. It also includes `Ca.nml`
  (missing from the original M0 candidate list, fixed in the snapshot) and has custom rate
  `ComponentType`s in `IL.channel.nml`.
- **Wang-Buzsaki:** the shipped stimulus starts at 0 ms, so the canonical protocol has no
  pre-stimulus baseline (eFEL's baseline window would be empty). The instantaneous Na m
  gate is a custom gate type. The firing regime is similar to FS and HH.
- **HH example:** a textbook implementation in the NeuroML2 specification repository, not a
  curated conversion of a specific published model file. It is LGPL-3.0, so redistributing
  modified mutant files is a licensing decision. Its channels are inline, with core
  `HHExpRate`/`HHSigmoidRate`/`HHExpLinearRate` rate types.
- **All Pospischil cells:** the OMV `.mep` reference files sit in `NEURON_MODIFIED/`, which
  the repository LICENSE excludes from MIT (citation condition only). The NeuroML2 files are
  MIT. The cell files declare an old beta schema location (`NeuroML_v2beta4.xsd`), but
  validity is judged against the tools' current schema.

## 9. Excluded or not selected (M0 evidence)

| Source | Reason |
|---|---|
| OpenSourceBrain/AllenInstituteNeuroML | Allen Cell Types content under Allen terms of use (no open license); large morphologies; GLIF versions are integrate-and-fire |
| NeuroML-DB | No model-level license statement; records not evaluated |
| OpenSourceBrain/hh-testing | No LICENSE |
| OpenSourceBrain/hodgkin_huxley_tutorial | Repository not found (HTTP 404) |
| OSB Ih relay-neuron and TC T-current repositories | No LICENSE and no `.nml` files |
| OpenSourceBrain/IzhikevichModel | BSD-3-Clause, but not conductance-based; not inspected |
| OpenSourceBrain/SolinasEtAl-GolgiCell | License present; single-compartment status not established; not evaluated |

## 10. Known gaps in the manifest and decisions for Neel

1. **Model count.** There are 6 manifest rows (2 included) against the specification's
   12-16 reference models for the full study.
2. **Independent sources.** There are 3 source families. Held-out generalisation claims
   need held-out models whose sources are independent of discovery models.
3. **Sag gap** (section 7).
4. **Model-level simulator version.** The manifest records only `jNeuroML`. Decide whether
   to add the version and jar hash to the model record, or rely on per-run records.
5. **Required includes.** Decide whether to add an explicit column or derive it from files.
6. **LGPL handling** if the HH example is used in the study.
7. **Whether the `.mep` reference files** (citation-condition license) may be vendored or
   only referenced by URL and hash.
8. **Validator oracle.** Confirm that `jnml -validate` stays the structural oracle for the
   frozen study, and record the exact jNeuroML version.
