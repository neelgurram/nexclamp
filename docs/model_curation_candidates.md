# Additional reference-model candidates (model curation)

Status: candidate screen, 2026-09-13, revised the same day after review (section 7). Nothing here is
an inclusion decision or a result. Every URL, SHA, license text and citation below comes from a
response saved under `docs/m0_evidence/model_curation/`. Behaviour statements come from single
deterministic jNeuroML runs with crude NumPy screening metrics. They are **not** eFEL features and
**not** calibrated, and finite testing is **not** evidence of equivalence to the original model. No
held-out split was created or read.

All behaviour numbers are taken from `verification.json`, run `2026-09-13T16:00:56+00:00_aa8fa6a0`
(code state `cae767f83aa15e88`, all 10 models in one invocation, no code change during the run).
The one exception, harness burst and ISI grouping, is computed from that run's harness output files
and is marked as such.

Machine-readable outputs:
* `data/model_candidates.csv`: columns identical to `data/model_manifest.csv`, `inclusion=candidate`.
* `models/candidates/<repo>@<sha8>/`: pinned, byte-exact files plus `PROVENANCE.json`.
* `docs/m0_evidence/model_curation/`: `license_evidence.json`, `trees/*.tree.json`,
  `org_repos_screen.json`, `verification.json` and `figures/<model_id>.png` (Ih-blocked traces
  overlaid in red).

Reproduce with `curate_candidates.py evidence`, then `curate_candidates.py fetch`, then
`verify_candidates.py`, all in that folder. Tests: `test_model_candidates.py` in the same folder.
It lies outside pytest `testpaths`, so run it explicitly. Core-contract problems found on the way
are in `docs/build_notes/model-curation.md`.

## 1. Bottom line

* **7 verified candidates from 4 new, mutually independent source families.** All 7:
  * are MIT licensed and pinned;
  * pass `jnml -validate` on the cell file;
  * are single-compartment core-NeuroML cells;
  * run in jNeuroML 0.14.0 / jLEMS 0.12.0.

  Where a shipped OMV reference exists, the shipped harness reproduces it.
  * `prinz2004_abpd`: fills the **bursting** and **rebound** gaps (independent source). It shows a
    large depolarising recovery during hyperpolarisation, but in a spontaneously active cell. Its
    sag ratio is undefined, and whether Ih drives that recovery is **untested**: the Ih-block run of
    that protocol aborted. It does **not** yet fill the Ih/sag gap.
  * `prinz2004_lp`: same family as `prinz2004_abpd`, a spontaneously firing cell. It has the
    clearest sag in the screen (ratio 0.24 at -0.3 nA). Blocking Ih removes it, so the sag depends
    on Ih. This rests on one protocol.
  * `maex1998_golgi`: fills the **independent-source adaptation** gap. Spontaneous pacemaker with
    strong spike-frequency adaptation under depolarisation. Ih is functionally large (blocking it
    lets V fall to -162 mV instead of -75 mV at -0.1 nA), but its sag ratio is undefined.
  * `maex1998_granule`: small cerebellar granule cell. Tonic, rheobase 0.005 nA, and a weak sag
    (0.23) only at the mildest step. The block control shows this sag depends on Ih.
  * `smith2013_singlecomp`: independent regular tonic spiker (no adaptation, sag or rebound observed).
  * `migliore2014_mt_soma` (delayed, low-rate regular firing) and `migliore2014_gc_soma` (phasic
    near threshold): independent source, same family as each other.
* **The strong-sag gap remains open.** No candidate shows a defined, Ih-dependent sag in a quiescent
  cell. The Ih-dependent sags found are in a spontaneously active cell (LP) or weak (granule).
* **Fewer independent families than the headline count suggests.** With the existing six models,
  the pool would be 13 models in 7 source families: pospischil2008 (4), neuroml2_examples (1),
  wangbuzsaki1996 (1), prinz_stg (2), maex1998 (2), smith2013 (1), migliore2014 (2). Clustered
  resampling works at the family level in practice, so 4-6 held-out models means holding out whole
  families.
* **Blocking issues before any of these enter the study** (details in the build note):
  * Canonical-window selection picks the wrong pulse for the Smith and Prinz harnesses.
  * The Maex cells ship no single-cell harness.
  * The Prinz and Maex Golgi cells fire spontaneously, so rheobase normalisation falls back to
    0.1 nA and baseline-referenced features such as sag are undefined.
  * The default rheobase search (0.5 nA upper bracket) crashes jLEMS on the two small-soma granule
    cells.
* **Screened out after download:**
  * Solinas et al. 2007 soma test cells: schema-invalid, or effectively passive.
  * The Pinsky-Rinzel 1994 two-compartment model: schema-invalid cell file and a custom LEMS cell
    type, incompatible with generated current-clamp probes.

  In addition, 13 repositories with NeuroML2 cells but **no license** were excluded without
  downloading any model file.

## 2. Search procedure and scope

1. `gh api orgs/OpenSourceBrain/repos` and `orgs/NeuroML/repos` (paginated; 2047 and 31 repos,
   138 and 26 non-forks; `org_repos_screen.json`).
2. GitHub code search over the OpenSourceBrain org for NeuroML2 files containing `<cell `
   (excluding repos dominated by exported morphologies) and for `ionChannelHH` channels with `hcn`
   or `species="h"`. This located every OSB repo with an Ih channel.
3. Web searches for single-compartment NeuroML2 models with Ih, bursting or rebound (OSB, NeuroML-DB).
4. Crossref `query.bibliographic` for each original paper, then `works/<doi>` records.

**Not covered:**
* NeuroML-DB and ModelDB entries outside GitHub were not screened model by model (one web search
  each). The M0 fixture audit had already found ModelDB GitHub mirrors without LICENSE files.
* Repos in the NeuroML org other than NeuroML2 hold tools, docs or unlicensed example collections
  (`NML2_LEMS_Examples`, `Documentation`: GitHub licence `None`) and were not mined for cells.

So "at least 6 candidates exist" is shown; "these are all that exist" is not claimed.

**Order enforced per source** (`curate_candidates.py`):
1. Repository metadata, commit, LICENSE at the pinned commit (`repos/<repo>/contents/LICENSE?ref=<sha>`)
   and CITATION.md.
2. Crossref DOI records, written to `license_evidence.json`.
3. Only then the `fetch` stage. It refuses sources without `license_verified=true` in that file,
   and re-applies the current licence gate to the stored LICENSE text before any download.
   * The gate (`license_verdict`) **fails closed**. It rejects the licence, with a review reason,
     if any of these is missing: the MIT header, the permission grant, or the copyright-notice
     condition.
   * It also rejects any preamble other than the known OSB template, any restriction wording
     (`apart from`, `except`, `excluding`, `non-commercial`, ...) outside the one parsed
     exception sentence, an unparseable directory list, or text after the MIT disclaimer.
4. Files come from `raw.githubusercontent.com/<repo>/<sha>/`. The include closure is built by
   parsing each `.nml`/`.xml` file with lxml (`xml_includes`), not with a regex, which means:
   * `<include href>` / `<Include file>` are read with either quote style;
   * includes inside XML comments are ignored;
   * a file that does not parse stops the fetch.
5. Every file's git blob SHA-1 is checked against the pinned tree. `PROVENANCE.json` records
   `downloaded_utc` after the evidence timestamp. A test re-checks this; it is a consistency check,
   not proof of historical order.

## 3. Sources fetched (license verified first)

All six repositories carry the OSB MIT LICENSE (GitHub's licence API reports `NOASSERTION`
because of a preamble). The full MIT permission grant is present at the pinned commit. Directories
named in the preamble carry a citation condition instead; no candidate model file lies in them. The
fail-closed gate, re-applied to the six stored LICENSE texts, reaches the same verdicts and
exceptions as the stored evidence (tested).

| snapshot | commit (date) | MIT exceptions | CI at commit | original publication (Crossref) |
|---|---|---|---|---|
| `PyloricNetwork@e97696fc` | e97696fca408ef375db6cbb2054bf8c1e5e5de0e (2025-08-22) | none | OMV success, [run 17154770311](https://github.com/OpenSourceBrain/PyloricNetwork/actions/runs/17154770311) | Prinz AA, Billimoria CP, Marder E (2003) J Neurophysiol 90(6):3998-4015 doi:10.1152/jn.00641.2003; Prinz AA, Bucher D, Marder E (2004) Nat Neurosci 7(12):1345-1352 doi:10.1038/nn1352 |
| `GranCellLayer@cee86047` | cee8604721c8654c24d3c69cedc07edb9679d935 (2025-08-22) | none | OMV success, [run 17154398506](https://github.com/OpenSourceBrain/GranCellLayer/actions/runs/17154398506) | Maex R, De Schutter E (1998) J Neurophysiol 80(5):2521-2537 doi:10.1152/jn.1998.80.5.2521 |
| `SmithEtAl2013-L23DendriticSpikes@179c596e` | 179c596e44303ad08065d1eb7eafc23506478f99 (2025-08-22) | none | OMV success, [run 17153763040](https://github.com/OpenSourceBrain/SmithEtAl2013-L23DendriticSpikes/actions/runs/17153763040) | Smith SL, Smith IT, Branco T, Häusser M (2013) Nature 503(7474):115-120 doi:10.1038/nature12600 |
| `MiglioreEtAl14_OlfactoryBulb3D@eaad1c8f` | eaad1c8f4afc9a19ff7b2492c150e8b42cc18edf (2025-08-22) | `NEURON`, `NEURON_FULL` | OMV success, [run 17154752109](https://github.com/OpenSourceBrain/MiglioreEtAl14_OlfactoryBulb3D/actions/runs/17154752109) | Migliore M, Cavarretta F, Hines ML, Shepherd GM (2014) Front Comput Neurosci 8 doi:10.3389/fncom.2014.00050 |
| `SolinasEtAl-GolgiCell@ab450696` (screened out) | ab4506963638dda6df5cc01721022ee7c6ea51e2 (2026-05-19) | `NEURON`, `NEURON_2007` | OMV success, [run 26103954642](https://github.com/OpenSourceBrain/SolinasEtAl-GolgiCell/actions/runs/26103954642) | Solinas S, Forti L, Cesana E, Mapelli J, De Schutter E, D'Angelo E (2007) Front Cell Neurosci doi:10.3389/neuro.03.002.2007 (Crossref record lists only "Solinas"; full author list from the repo's CITATION.md) |
| `PinskyRinzelModel@a9aa9c90` (screened out) | a9aa9c90d2669c259e153d01b12e470114b767de (2025-08-22) | `XPP` | OMV success, [run 17154838367](https://github.com/OpenSourceBrain/PinskyRinzelModel/actions/runs/17154838367) | Pinsky PF, Rinzel J (1994) J Comput Neurosci 1(1-2):39-60 doi:10.1007/bf00962717 |

License evidence URLs per source (API responses in `license_evidence.json`):
* `https://api.github.com/repos/<repo>/contents/LICENSE?ref=<sha>`
* `https://github.com/<repo>/blob/<sha>/LICENSE`
* `https://api.github.com/repos/<repo>/license`

For example, [PyloricNetwork LICENSE at e97696fc](https://github.com/OpenSourceBrain/PyloricNetwork/blob/e97696fca408ef375db6cbb2054bf8c1e5e5de0e/LICENSE).
The Maex author string is "Maex R, Schutter ED" in Crossref and "Maex, R and De Schutter, E" in the
repo's CITATION.md; the CSV uses the latter.

**Include closures.** All files, with SHA-256 and git blob SHA-1, are listed in each
`PROVENANCE.json`. The original fetch used a regex over raw text. Recomputing every closure from the
pinned files with the lxml parser gives exactly the fetched file sets and the same builtin includes
for all six snapshots (tested): nothing is missing, and no file was pulled in by a commented-out
include. Every shipped harness below ran from a copy of the snapshot alone, so the closures are
complete.

| snapshot | entries fetched | resolved includes | builtin (not fetched) |
|---|---|---|---|
| PyloricNetwork | LICENSE, CITATION.md, READMEs, AB_PD_1/LP_1/PY_1 cells, LEMS_Fig2a-d, Fig2 OMV tests | Fig2a-d nets, AB_PD_3, LP_2, LP_5, PY_3, PY_4 cells, 8 STG channel files, CaPool_STG, Synapses.nml | Cells/Networks/Simulation.xml |
| GranCellLayer | Granule_98, Golgi_98, OMV tests, NeuroMLlite JSON (temperature 32.0) | 14 Gran_/Golgi_ channel and pool files, 2 passive conductances | none |
| SmithEtAl2013 | singleCompAllChans cell/net/LEMS, OMV tests, `NEURON/test/.test.mep` | na, kv, km, ca, kca, it, pas channels | Cells/Networks/Simulation.xml |
| MiglioreEtAl14 | MT_soma, GC_soma, LEMS/net for 12 degC and 35 degC, `.test.12/.35` OMV+mep | kamt, kdrmt, nax, nax__sh10, nax__sh15, pas | Cells/Networks/Simulation.xml |
| SolinasEtAl-GolgiCell | TestSoma(+_HELPER) cell/net/LEMS, OMV tests, `NEURON/test/.test.soma.mep` (citation-condition dir) | 14 Golgi channel files, 2 Ca pools | Cells/Networks/Simulation.xml |
| PinskyRinzelModel | twoCompartmentCell, LEMS_Figure2/3, OMV test + mep | 10 channel files, 3 density files, 5 parameter files | Cells/Networks/Simulation.xml |

No NeuroML/LEMS file in any candidate snapshot is byte-identical to a file in `models/raw/`
(SHA-256 comparison over all `.nml`/`.xml`).

## 4. Candidate by candidate

Common method (`verify_candidates.py`):
* `jnml -validate` on the cell file and on the harness network.
* An XML read for segment count, channel densities and non-core elements.
* The shipped harness at its own dt and length. Wall times below come from a run with 4 models in
  parallel, so they measure load, not speed.
* An injected-current response check.
* A bracketing rheobase search: 500 ms steps, 8-point grid, 3 rounds, threshold -20 mV.
* A rheobase-scaled screening battery generated by `neurosem.protocols` at dt 0.01 ms: P01, P04,
  P05, P07, P08, plus S01, a -3x rheobase 1 s step added so slow Ih can activate.

**Sag rule** (`subthreshold_metrics`):
* `sag ratio = (V_steady - V_min) / (V_baseline - V_min)`, where V_baseline is the mean of the
  50 ms before the step and V_steady is the mean of the step's last 10 %.
* It is **undefined** when a spike falls in, or up to 5 ms before, the baseline window, because
  the baseline then depends on spike phase. This applies to spontaneously active cells.
* It is also undefined when the cell spikes during the step (V_min may be an AHP).
* "Late" sag takes V_min from 30 ms after onset, and is additionally undefined when that minimum
  sits on the window edge (V still in the onset transient).
* `recovery` = V_steady - V_min(late), in mV. It needs no baseline and is the quantity compared in
  the Ih-block control.

**Ih-block control**, for cells with a `channelDensity ion="h"`:
* A work copy with that density set to 0 runs P01, P07, P08 and S01 at the same absolute currents
  and dt.
* Blocking Ih also shifts rest and so recruits other currents differently. The difference is Ih's
  net effect in this model.
* In several blocked runs the membrane was driven to non-physiological potentials and jLEMS
  aborted in an HH rate expression (build note item 7). Those comparisons are missing, not zero.
* At dt 0.025 ms the Golgi P07 step aborts even without the block; dt 0.01 ms runs.

### 4.1 `prinz2004_abpd` — STG AB/PD pacemaker (AB_PD_3)
* **Files.** `NeuroML2/AB_PD_3.cell.nml` (cell `AB_PD`); harness `NeuroML2/LEMS_Fig2a.xml`,
  output `AB_PD.dat` col 1, 10.0 degC.
* **Structure.** 1 segment (soma diameter about 141 um).
* **Channels (mS/cm2).** Na 200, Kd 50, KA 50, KCa 5, H 0.01 (erev -20 mV), CaS 4, CaT 2.5
  (Nernst), leak 0. Plus a Ca pool.
* **Validation.** Cell and harness network both valid.
* **Shipped harness.** 5000 ms at dt 0.025 ms, 145.0 s wall time for the 6-cell network.
  * AB_PD receives three pulse inputs (-0.2 nA 0-100 ms, -0.03 nA 0-1000 ms, -0.2 nA 4000-5000 ms)
    and no synapses; it is only presynaptic, so its trace is an isolated-cell response.
  * Observed: 40 spikes, V from -113.4 to +48.6 mV.
  * Grouping from the harness output file, splitting at ISI > 200 ms: **2 bursts**, 1119-1662 ms
    (22 spikes) and 2715-3192 ms (18 spikes).
  * No `.mep` is shipped; the OMV test only checks that it runs.
* **Probes.**
  * Spontaneously active: rheobase status `spontaneous`, protocols scaled with the 0.1 nA fallback.
    P01 has 4 spikes in 700 ms.
  * S01 (-0.3 nA, 1 s): V falls to -124.5 mV at +264 ms, recovers by 43.2 mV to -81.3 mV before
    release, then 13 rebound spikes. **Sag ratio undefined:** 2 spikes in the pre-step baseline
    window.
  * P08 (-0.2 nA): trough -115.7 mV at +326 ms, recovery 16.3 mV, 8 rebound spikes; sag undefined
    for the same reason.
  * P07 (-0.1 nA): 3 spikes during the step.
  * P05 (+0.15 nA, 2 s): 35 spikes in two groups.
* **Ih-block control.** P01 is unchanged (4 spikes). P07 still spikes during the step, but its
  end-of-step potential is 12.3 mV lower (-106.8 vs -94.5 mV). The blocked P08 and S01 runs
  **aborted in jLEMS**, so the Ih contribution to the large recovery is untested.
* **Expectation vs observed.** Expected: a bursting pacemaker (Prinz et al. 2004 AB/PD) with Ih
  and T-type Ca.
  * Observed: bursting in the shipped harness, and rebound spiking.
  * Hyperpolarisation shows a depolarising recovery in a spontaneously active cell, but that has
    not been shown to be sag or to depend on Ih.
* **Caveats.**
  * Slow dynamics: burst onsets 1.6 s apart, longer than the 700-1000 ms default protocols.
  * Spontaneous activity makes rheobase normalisation and sag undefined.
  * The canonical-window rule picks the 0-100 ms pulse (build note item 4).
  * The harness is a network file including LP_2 and graded synapses; mutations of "harness input"
    must target AB_PD's pulses.
* **Recommendation.** Candidate for the bursting and rebound gaps. Do not count it as filling the
  Ih/sag gap until a spike-free baseline (e.g. a silencing hold current) and a completed Ih-block
  comparison exist. Needs decisions on rheobase for spontaneously active cells and on the
  canonical window.

### 4.2 `prinz2004_lp` — STG LP neuron (LP_2)
* **Files.** `NeuroML2/LP_2.cell.nml` (cell `LP`); same harness, output `LP.dat` col 1 (`LP[0]`,
  0 nS graded synapse).
* **Channels (mS/cm2).** Na 100, Kd 50, KA 30, KCa 5, H 0.05, CaS 6, CaT 0, leak 0.02.
* **Validation.** Valid.
* **Shipped harness.** 25 spikes in 5 s, 142.8 s wall time. From the output file: median ISI
  209.9 ms, maximum 238.2 ms.
* **Probes.** Spontaneously active (P01: 4 spikes; fallback scale).
  * S01 (-0.3 nA, 1 s): no spike before or during the step. **Sag ratio 0.24** (late sag 0.24),
    trough -70.6 mV at +253 ms, recovery 6.5 mV, 16 rebound spikes.
  * P07 (-0.1 nA) and P08 (-0.2 nA): one spike during the step, so sag is undefined. 3 and 10
    rebound spikes.
* **Ih-block control.** P01 is unchanged (4 spikes). In S01, sag falls from 0.24 to about zero
  (0.0001), recovery from 6.5 to 0.003 mV, and the end-of-step potential is 9.8 mV lower. Rebound
  spikes fall from 16 to 10. Within this screen the sag at S01 depends on Ih; the rebound depends
  on it only partly.
* **Correlation.** Same paper, channel files and harness as `prinz2004_abpd`; family `prinz_stg`.
* **Recommendation.** Useful only as a family-mate, never split from AB_PD across
  discovery/held-out. Its recorded trace receives no stimulus at all in the shipped harness, so its
  canonical protocol is a spontaneous-activity test. It gives the clearest Ih-dependent sag in the
  screen, but only from one protocol.

### 4.3 `maex1998_granule` — cerebellar granule cell (Granule_98)
* **Files.** `NeuroML2/Granule_98.cell.nml`; **no single-cell harness shipped** (upstream tests
  the 3D network only, with jNeuroML_NEURON). 32.0 degC, from the repo's NeuroMLlite JSON.
* **Structure.** 1 segment, diameter 10 um.
* **Channels (mS/cm2).** NaF 55.7, KDr 8.90, KCa 17.98, KA 1.15, CaHVA 0.908 (fixed erev 80 mV),
  H 0.0309 (erev -42 mV), leak 0.033. Plus a Ca pool.
* **Validation.** Valid.
* **Probes.** A 0.05 nA injection aborts jLEMS mid-run (build note item 1), because of the very
  high input resistance. At 0.005 nA it runs. Results:
  * Silent at rest (P01 mean -62.9 mV). Rheobase 0.0051 nA (bracket 0.0001 nA).
  * Tonic, non-adapting firing: P04 (0.0102 nA) gives 18 spikes, ISI 30.5 then 28.2 ms, ratio 0.93;
    P05 ratio 0.93.
  * P07 (-0.0051 nA): minimum -85.8 mV at +42 ms, steady -80.6 mV, **sag ratio 0.23**, recovery
    5.2 mV.
  * P08 (-0.010 nA) and S01 (-0.015 nA): V near -105 and -130 mV, sag 0.01 and 0.
  * No rebound spikes.
* **Ih-block control.**
  * Rest is 5.3 mV more negative (-68.2 mV).
  * P07: sag and recovery fall to 0, and the end-of-step potential falls from -80.6 to -114.2 mV.
  * P08: steady -163.4 mV with Ih blocked.
  * The blocked S01 run aborted.
* **Expectation vs observed.** Expected: an Ih-carrying granule cell with sag. Observed: a small
  sag at the mildest hyperpolarisation only, which the block control attributes to Ih. Ih also
  sets the resting potential and limits hyperpolarisation.
* **Recommendation.** Candidate with caveats. It is the only small-soma, high-input-resistance cell
  in the pool, which gives very distinct thresholds. Requires an authored canonical harness and a
  rheobase bracket that adapts to small cells. Weak evidence for the sag gap.

### 4.4 `maex1998_golgi` — cerebellar Golgi cell (Golgi_98)
* **Files.** `NeuroML2/Golgi_98.cell.nml`; no single-cell harness; 32.0 degC.
* **Structure.** 1 segment, diameter 30 um.
* **Channels (mS/cm2).** NaF 40.0, KDr 6.79, KA 0.525, KCa 0.572, CaHVA 0.832 (Nernst), H 0.171,
  leak 0.033.
* **Validation.** Valid.
* **Probes.**
  * Spontaneous pacemaking: P01 has 5 spikes in 700 ms, ISI 138 ms, CV 0.002.
  * **Strong adaptation** under depolarisation: P04 at +0.2 nA gives 45 spikes, first ISI 4.1 ms,
    last 13.5 ms (ratio 3.3); P05 ratio 3.5.
  * Rebound spikes: 3 after P07, 4 after P08 and S01.
  * **Sag ratio undefined** in P07, P08 and S01. There is a spike in the pre-step baseline window,
    and the late minimum lies on the 30 ms window edge (onset transient).
  * Baseline-free recovery: 12.5 mV (P07), 6.2 mV (P08), 2.6 mV (S01).
* **Ih-block control.**
  * P01: 3 instead of 5 spikes.
  * P07 (-0.1 nA): no recovery (0.0001 mV), and V ends at -162.2 mV instead of -75.2 mV.
  * The blocked P08 and S01 runs aborted in jLEMS.
  * Ih strongly limits hyperpolarisation in this cell. Whether that appears as a sag with a defined
    ratio is not established.
* **Recommendation.** Candidate for the independent-source adapting model. Needs an authored
  canonical harness (build note item 5) and the spontaneous-rheobase decision. Correlated with
  `maex1998_granule` (same paper; separate channel files).

### 4.5 `smith2013_singlecomp` — single-compartment cell with the Smith et al. 2013 channel set
* **Files.** `NeuroML2/singleCompAllChans.cell.nml` (cell `cell`); harness
  `NeuroML2/LEMS_singleCompAllChans.xml`, output `jlems_sccct.dat` col 1, 35 degC.
* **Structure.** 1 segment.
* **Channels (S/cm2).** na 0.1, kv 0.01, km 2.2e-4, kca 3e-4, ca 5e-5, it 3e-4 (both Ca channels
  with fixed erev 140 mV), pas 1.43e-4. No Ca pool: the `intracellularProperties` element is empty.
* **Validation.** Valid.
* **Shipped harness.** -0.01 nA 100-200 ms, +0.05 nA 300-400 ms; 600 ms at dt 0.001 ms, 46.5 s.
  7 spikes vs 7 in the NEURON `.mep`; max paired deviation 0.109 ms.
* **Probes.** Rheobase 0.0219 nA (bracket 0.0015 nA). Tonic, **non-adapting**: ISI ratio 1.01 (P04)
  and 1.02 (P05). No sag (recovery below 0.002 mV), no rebound. No h density, so no block control.
* **Expectation vs observed.** Km and KCa suggested adaptation, but none was seen at 1.5-2x
  rheobase. It is a regular tonic spiker with a distinct threshold.
* **Caveats.** An OSB-assembled test cell, not a published single-compartment model (notes: "A
  single segment/compartment cell"). Canonical window picks the hyperpolarising pulse (build note
  item 4).
* **Recommendation.** Independent tonic-spiking candidate with a well-defined rheobase and an
  exact OMV reference. Do not count it as the adapting model.

### 4.6 `migliore2014_mt_soma` — mitral-cell soma from the 3D olfactory bulb model
* **Files.** `NeuroML2/Channels/test/MT_soma.cell.nml` (cell `MT_soma`); harness
  `LEMS_OlfactoryTest_12.xml`, output `CG_MT_soma_0.0.dat` col 1, 12.0 degC.
* **Structure.** 1 segment (20 x 25 um).
* **Channels (mS/cm2).** nax__sh10 40, kamt 4, kdrmt 0.1, pas 0.0833. Cm 1.8 uF/cm2.
* **Validation.** Valid.
* **Shipped harness.** 60 pA 20-80 ms, 100 ms at dt 0.01 ms, 12.4 s. 1 spike, 0.06 ms from the
  `.mep` spike time.
* **Probes.** Rheobase 0.0248 nA. P04 gives 7 spikes, latency 18 ms, ISI 73-79 ms: low-rate
  regular firing. Slight ISI lengthening in P05 (ratio 1.24). No sag, no rebound (no h channel).
* **Caveats.** A soma-only test cell exported from a multicompartment mitral cell ("exported from
  NEURON ModelView"). The shipped harness is only 100 ms and one spike long: a weak canonical test.
* **Recommendation.** Independent candidate: low-threshold, slow regular firing with A-type K.

### 4.7 `migliore2014_gc_soma` — granule-cell soma from the same model
* **Files.** `GC_soma.cell.nml`; same harness, output `CG_GC_soma_0.0.dat`.
* **Structure.** 1 segment, 8 um. Cm 4 uF/cm2.
* **Channels (mS/cm2).** nax 40, kdrmt 6, kamt 4, pas 0.133.
* **Validation.** Valid.
* **Shipped harness.** 2 spikes vs 2 in the `.mep`; max deviation 0.15 ms; 8.4 s.
* **Probes.** A 0.05 nA injection aborts jLEMS (small soma, build note item 1). At 0.005 nA:
  * Rheobase 0.0026 nA.
  * **Phasic** near threshold: P04 (2x rheobase, 500 ms) gives 1 spike at 36 ms latency; P05
    (1.5x, 2 s) gives 2 spikes 1238 ms apart.
  * No sag, no rebound.
* **Correlation.** Same family and channel files (kamt, kdrmt, pas) as `migliore2014_mt_soma`.
* **Recommendation.** Candidate with caveats. The phasic response is a distinct behaviour class,
  but sparse spiking leaves few defined spike features. Needs a rheobase bracket that adapts to
  small cells.

### 4.8 Screened out after download (not in the CSV)
* **`solinas2007_soma_helper`** (`TestSoma_HELPER.cell.nml`, a `cell2CaPools` with NaT, KV, CaHVA,
  CaLVA and leak active; all hcn channels commented out).
  * Its harness (dt 0.0005 ms, 370.9 s) reproduces the NEURON pacemaking reference: 52/52 spikes,
    median deviation 0.33 ms, max 3.5 ms.
  * But the cell file **fails `jnml -validate`**: `<include file=...>` is not allowed. Validating
    its network crashes jNeuroML with a NullPointerException (build note item 2), and generated
    probes cannot resolve its channels (`No component found: LeakCond`).
  * Excluded on the "passes current NeuroML validation" criterion.
* **`solinas2007_testsoma`** (`TestSoma.cell.nml`).
  * Valid, but only leak and CaHVA are active; every Na, K and hcn density is commented out.
  * The harness shows one Ca-driven depolarisation to +101.6 mV, and most generated probes abort
    in jLEMS.
  * Not a spiking neuron model.
* **`pinskyrinzel1994`** (`twoCompartmentCell.cell.nml`).
  * Two compartments via a custom LEMS `ComponentType`. The cell file **fails `jnml -validate`**
    (`<neuroml>` lacks `id`).
  * Its shipped `LEMS_Figure2.xml` reproduces the OMV reference exactly (Fig2A: 15/15 spikes, max
    deviation 0.005 ms, at the -25 mV threshold), and the bursting is real.
  * But generated probes fail (`No such type twoCompartmentCell`: the type is only reachable
    through the LEMS includes).
  * Reading the XML, the `Vs`/`Vd` time derivatives do not include `iSyn`, so NeuroML
    `pulseGenerator` inputs would have no effect even if the model built.
  * Incompatible with the protocol battery and the channel-density mutation operators.

### 4.9 Screened without download
* **No license (excluded by rule).** For each repo, GitHub's licence API returned 404 and the
  pinned tree has no LICENSE/LICENCE/COPYING file (responses in `license_evidence.json`):
  * GranuleCell, Cerebellum3DDemo, CerebellarNucleusNeuron, HNN, OSBv2_Showcase, ACnet2
  * BahlEtAl2012_ReducedL5PyrCell, PINGnets, Ferrante2009-DentateGyrusGranuleCell
  * IonChannelGenealogyShowcase, NetPyNEShowcase, GranularLayerSolinasNieusDAngelo2010, MOOSEShowcase

  Several contain attractive single-compartment cells (e.g. the CerebellarNucleusNeuron soma with
  HCN/CaT, the HNN single-compartment basket cells), which are unusable without a license.
* **Licensed but not suitable** (judged from file listings or repo metadata; model files not fetched):
  * VervaekeEtAl-GolgiCellNetwork: its only cell is a 1.4 MB morphology.
  * M1NetworkModel: HDF5 networks with Izhikevich-type `izhi2007b.mod`.
  * NeuroMLSBMLShowcase: passive BallAndStick.
  * EDENShowcase: a copy named `NML2_SingleCompHHCell.nml`, like the existing HH fixture; not
    fetched or hashed.
  * FergusonEtAl2013-PVFastFiringCell: NeuroML2 content not inspected; related repos are
    Izhikevich-based, so it was not pursued.
  * IzhikevichModel (BSD-3-Clause) and FitzHugh-Nagumo: abstract, not conductance-based.
* **Unlicensed abstract models:** HindmarshRose1984, MorrisLecarModel.

## 5. Correlation with the existing six models

| candidate | shares source/files with existing models? | family |
|---|---|---|
| prinz2004_abpd, prinz2004_lp | no (STG channel set, 10 degC) | prinz_stg |
| maex1998_granule, maex1998_golgi | no (cerebellar CML channel set) | maex1998 |
| smith2013_singlecomp | no | smith2013 |
| migliore2014_mt_soma, migliore2014_gc_soma | no | migliore2014 |

Kinetic *types* still overlap: most channels are HH-rate `ionChannelHH` gates similar in form to
the Pospischil and HH fixtures, and the Maex, Smith and Migliore Na/K channels are ChannelML- or
NEURON-derived. Independence here means independent parameterisation and authorship, not
independent formalism.

## 6. Recommendation summary

| model_id | behaviour gap filled (screening evidence) | recommend | blocking decisions |
|---|---|---|---|
| prinz2004_abpd | bursting (harness), rebound; hyperpolarisation recovery with Ih role untested | yes (not for the sag gap) | spontaneous rheobase and sag baseline; canonical window; slow time scale |
| prinz2004_lp | Ih-dependent sag (one protocol), rebound, spontaneous firing | only with AB_PD, same split | as above; unstimulated canonical trace |
| maex1998_golgi | adaptation (independent source), pacemaker, rebound; large Ih effect, sag ratio undefined | yes | no shipped harness; spontaneous rheobase |
| maex1998_granule | tonic non-adapting; very low rheobase (0.005 nA); weak Ih-dependent sag | with caveats | no shipped harness; rheobase bracket for small somata |
| smith2013_singlecomp | tonic regular spiking, distinct threshold | yes | canonical window |
| migliore2014_mt_soma | low-threshold delayed/regular firing | yes | very short canonical harness |
| migliore2014_gc_soma | phasic firing near threshold | with caveats | rheobase bracket for small somata; sparse spike features |

A reasonable split cannot be chosen here, because splits must be made without inspecting
held-out behaviour. The 4 new families plus the 3 existing ones allow 4-6 held-out models only if
at least two whole families are held out.

## 7. Review fixes (2026-09-13)

* **Sag numbers withdrawn and recomputed.** The first version quoted "sag (late)" 0.60 (AB_PD)
  and 0.22 (LP), which no delivered code produced.
  * The AB_PD value also came from a baseline window that contains spikes (-59.7 to +46.2 mV), so
    it measured spike phase, not Ih.
  * The late-window rule and the spike-contamination checks now live in `subthreshold_metrics`, and
    every quoted sag ratio must exist in `verification.json` (tested).
  * The Ih-block control was added. The claim that AB_PD fills the Ih/sag gap is withdrawn.
* **Licence gate fails closed** (`license_verdict`), and the fetch stage re-applies it to the stored
  text. Stored verdicts are unchanged for all six sources.
* **Include closure is parsed with lxml** (`xml_includes`). Recomputed closures equal the fetched
  snapshots.
* **One run, one code state.** `verification.json` now holds a single run (all 10 models).
  * Each record carries `run_id` and `code_state_id`: the SHA-256 of the core modules used, this
    script and the simulator version.
  * A partial re-run refuses to merge records from another code state.
  * All figures were regenerated in that run.
* **Tests.** Tests that only compare stored evidence are named `test_evidence_*`. Live checks now
  cover:
  * the licence gate and the include parser;
  * closure equality with the snapshots;
  * the sag rule;
  * the Ih block, including a jLEMS run showing the Golgi cell hyperpolarises more without Ih.

  The test file still sits outside `testpaths` (build note item 6).
