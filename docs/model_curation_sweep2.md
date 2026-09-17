# Additional reference-model candidates: sweep 2

Status: desk research only, 2026-09-16. **Nothing in this sweep was simulated, validated or downloaded
into the project.** Every path, commit, licence and DOI below comes from a GitHub API response, a
file fetched from `raw.githubusercontent.com` at the pinned commit, or a Crossref record. Files were
read into a temporary scratch folder outside the repository. Behaviour statements are copied from the
reference files each repository ships (OMV `.mep` spike times, tuning notes). They are **not** our
own results. No held-out split was created or read.

Machine-readable output: `data/model_candidates_sweep2.csv`. Its first 20 columns match
`data/model_candidates.csv`. Seven more columns follow: `doi`, `behaviors`, `step_and_length`,
`custom_component_types`, `redistribution`, `attribution` and `dependencies`. All rows have
`inclusion=candidate` and `download_date=2026-09-16`.

## 1. Plain-English summary

We looked for more small, openly shared neuron models that jNeuroML can run and that ship their own
test simulation. **11 candidates** were found. They come from 10 source publications and 9 source
families. None repeats a model from sweep 1 (`docs/model_curation_candidates.md`).

* **Six have a clean permissive licence (MIT)**, but two of them share channel files, so they count
  as one family:
  * `hay2011_soma` and `bbp2015_soma` (same channel files);
  * `migliore2005_ca1_soma`;
  * `osb_hh2_477127614`;
  * `boyle2008_muscle`.
* **Four have a copyleft licence** (GPL or LGPL):
  * `traub2005_testseg2` and `traub2005_testseg_all` (GPL-2.0, same family);
  * `acnet2_pyr_soma` (LGPL-3.0). Its upstream repository has no licence of its own.
  * `solinas2007_goc_gurnani` (GPL-3.0). This one has real validity problems.
* **Two have no licence at all:** `bahl2012_soma` and `bezaire2016_olm`. They cannot be copied
  into the study repository without the authors' permission. They are listed because they fill
  behaviour gaps.

Where sweep 1 left a gap:
* **Sag / Ih.** Candidates with Ih:
  * `traub2005_testseg_all` (anomalous rectifier `ar`);
  * `hay2011_soma` and `bbp2015_soma` (Ih 0.2 mS/cm2);
  * `bezaire2016_olm` (somatic HCN);
  * `solinas2007_goc_gurnani` (HCN1/HCN2).

  None of these has been shown to sag. That still needs a simulation with an Ih-block control, as
  in sweep 1.
* **Rebound.** T-type Ca is present in the Hay/BBP cells (Ca_LVAst), in `traub2005_testseg_all`
  (cat) and in the Golgi cell (CaLVA). Rebound is untested.
* **Adaptation / phasic firing.** The shipped references show it directly:
  * `acnet2_pyr_soma` (ISI 18 → 108 ms);
  * `bbp2015_soma` (ISI 17.5 → 23.6 ms);
  * `traub2005_testseg2` (ISI 5.8 → 7.6 ms);
  * `bahl2012_soma` (3 spikes, then silence during a 500 ms step).
* **Different channel composition.** `boyle2008_muscle` has no Na channel at all: its spikes are
  carried by Ca.
* **Different thresholds:**
  * `migliore2005_ca1_soma` has a 7.5 µm soma, so we expect a very low rheobase.
  * `osb_hh2_477127614` was tuned to fire only above about 60-70 pA.

**Every candidate defines custom LEMS ComponentTypes** in its channel or pool files (1 to 45 types
each; listed in the CSV). This is the same situation as the Pospischil LTS fixture. The candidates
pass `jnml -validate` upstream (OMV validate tests), but they may fail a strict libNeuroML XSD check.

## 2. Method

1. **Repository lists.**
   * Listed every non-fork repository in the OpenSourceBrain and NeuroML GitHub organisations
     (the sweep 1 list, 164 repositories).
   * Checked each repository's root for a `LICENSE`/`LICENCE`/`COPYING` file with the GitHub
     contents API. 47 had one.
   * Also listed the 1909 OSB forks. They are mostly ModelDB mirrors. We checked their licence
     fields (67 non-empty) and inspected the two non-numeric forks (NicolettiEtAl2024_MN_IN,
     Maki-MarttunenEtAl2020).
2. **File trees.** For licensed repositories not mined in sweep 1, we fetched the recursive git tree
   at `commits/HEAD`. We then looked for `*.cell.nml`, `LEMS_*.xml`, `.omt` and `.mep` files.
3. **Extra searches.**
   * GitHub code search for NeuroML2 cell content outside OSB. This found `harshagurnani/GoCModel_Basic`
     and `mbezaire/ca1`.
   * The NeuroML-DB API (`/api/search`, `/api/model`) for cells and their compartment counts
     (194 cells found).
4. **Per candidate**, all at the pinned commit:
   * read the cell file, harness LEMS file and network file;
   * parsed the full `<Include>`/`<include>` closure with an XML parser, and recorded every
     `<ComponentType>` it defines;
   * read the output file and column for the soma voltage, and the simulation `step` and `length`;
   * read the `networkWithTemperature` value;
   * read the OMV `.omt`/`.mep` files;
   * read LICENSE and CITATION.md from `raw.githubusercontent.com`;
   * checked the GitHub check-runs at that commit;
   * checked each DOI with `api.crossref.org/works/<DOI>`.

   All include closures resolved inside the repository, with one exception: the Golgi-cell harness
   (see its row).

**Not done:**
* No `jnml -validate` runs and no simulations.
* No check of how Q10/temperature handling interacts with the 6.3 degC harness temperatures.
* No per-model screening of NeuroML-DB entries beyond compartment counts.

## 3. Candidates

| model_id | snapshot (commit) | cell file → cell id | harness → output, V column | dt; length; temp | licence | shipped reference / expected behaviour | family |
|---|---|---|---|---|---|---|---|
| hay2011_soma | L5bPyrCellHayEtAl2011@a813a88a | `neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml` → `Soma_AllCML` | `neuroConstruct/generatedNeuroML2/LEMS_L5bPyrCellHayEtAl2011_LowDt.xml` → `CG_TestCML_0.dat`, col 1 | 0.0025 ms; 600 ms; 6.3 degC | MIT (NEURON dir excepted) | 7 spikes, mild ISI lengthening; Ih + Ca_LVAst + SK | hay2011_bbp_channels |
| bbp2015_soma | BlueBrainProjectShowcase@9ab1b393 | `NMC/NeuroML2/Soma_AllNML2.cell.nml` → `Soma_AllNML2` | `NMC/NeuroML2/LEMS_Soma_AllNML2.xml` → `CG_TestCML_0.dat`, col 1 | 0.001 ms; 600 ms; 6.3 degC | MIT (NMC/parser/L* excepted) | 5 spikes, ISI 17.5 → 23.6 ms (adapting) | hay2011_bbp_channels |
| migliore2005_ca1_soma | CA1PyramidalCell@b854fd29 | `neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml` → `SomaOnly_allCml` | `neuroConstruct/generatedNeuroML2/LEMS_CA1PyramidalCell.xml` → `CG_CML_0.0.dat`, col 1 | 0.001 ms; 100 ms; 35 degC | MIT | 4 spikes, ISI ~18.3 ms (tonic); A-type K, small Ih | migliore2005 |
| traub2005_testseg2 | Thalamocortical@5d1c9aea | `neuroConstruct/generatedNeuroML2/TestSeg_test2.cell.nml` → `TestSeg_test2` | `neuroConstruct/generatedNeuroML2/LEMS_SomaTest.xml` → `CG_tester_0.0.dat`, col 1 | 0.001 ms; 100 ms; 6.3 degC | GPL-2.0 | 9 spikes, ISI 5.8 → 7.6 ms (fast, adapting) | traub2005 |
| traub2005_testseg_all | Thalamocortical@5d1c9aea | `neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml` → `TestSeg_all` | `neuroConstruct/generatedNeuroML2/LEMS_Thalamocortical.xml` → `CG_CML_0.0.dat`, col 1 | 0.0005 ms; 100 ms; 6.3 degC | GPL-2.0 | 4 irregular spikes; ar (Ih-like), CaT, CaL, KAHP, KC | traub2005 |
| osb_hh2_477127614 | MultiscaleISN@f0783475 | `cells/HH2/HH2_477127614.cell.nml` → `HH2_477127614` | `cells/HH2/LEMS_477127614.xml` → `Allen2stage_STAGE2.Pop0.v.dat`, col 7 (7 cell copies at 7 currents) | 0.025 ms; 1000 ms; 34 degC | MIT | tuning notes: silent ≤60 pA, 5 spikes at 70 pA, 48 at 170 pA | osb_allen_hh2 (Pospischil kinetics) |
| boyle2008_muscle | muscle_model@2b3c65f4 | `NeuroML2/SingleCompMuscle.cell.nml` → `SingleCompMuscleCell` | `NeuroML2/LEMS_MuscleStim.xml` → `m_v.dat`, col 1 | 0.01 ms; 300 ms; not set | MIT (OpenWorm) | 1 Ca spike at 37.6 ms; no Na channel | boyle2008 |
| acnet2_pyr_soma | NeuroML2@a5f5dadc | `LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml` → `pyr_soma_m_in_b_in` | `LEMSexamples/morphologies/LEMS_m_in_b_in.xml` → `pyramidal_soma_0.dat`, col 1 | 0.0025 ms; 700 ms; 6.3 degC | LGPL-3.0 (upstream ACnet2 unlicensed) | 8 spikes, ISI 18 → 108 → ~76 ms (strong adaptation) | acnet2_traub1991 |
| solinas2007_goc_gurnani | GoCModel_Basic@90950b59 | `Cells/Golgi/GoC.cell.nml` → `GoCl` (5 segments) | `Network/LEMS_sim_V2_OneGoC_GoC.xml` → `../Data_OneGoC/sim_V2_OneGoC_GoC.v.dat`, col 1 | 0.0025 ms; 1000 ms; 23 degC | GPL-3.0 | spontaneous pacemaking (README, 2-9 Hz); HCN1/2, CaLVA, SK2, BK; no reference file | solinas2007 |
| bahl2012_soma | BahlEtAl2012_ReducedL5PyrCell@8275beaa | `NeuroML2/pyr_soma_cell.nml` → `pyr_cell` | `NeuroML2/LEMS_pyr_single_comp.xml` → `pyr_single_comp.dat`, col 1 | 0.005 ms; 700 ms; 37 degC | **unclear (none)** | 3 spikes at 102-132 ms, then silent (phasic) | bahl2012 |
| bezaire2016_olm | ca1@a8655fa8 (mbezaire/ca1) | `NeuroML2/cells/olm.cell.nml` → `olmcell` (8 segments) | `NeuroML2/cells/tests/LEMS_olm.xml` → `olm.dat`, col 1 | 0.001 ms; 300 ms; 34 degC | **unclear (none)** | 14 spikes, ISI 16.2 → 14.2 ms; somatic HCN | bezaire2016 |

Full commits:

| snapshot | full commit | commit date |
|---|---|---|
| L5bPyrCellHayEtAl2011 | `a813a88af8eb77fc59ef70bb3e5aef6397e682f7` | 2025-11-14 |
| BlueBrainProjectShowcase | `9ab1b3935e6df511bd84837c1b20f99a4b97555a` | 2025-08-22 |
| CA1PyramidalCell | `b854fd29bc6643c7b2e5b2d59b63b0998c0dff32` | 2025-08-22 |
| Thalamocortical | `5d1c9aea16598092b6a2e75974465b9f4cd7ccc7` | 2024-07-31 |
| MultiscaleISN | `f07834754d68263a03b6ab8d66b72f2049c6daf6` | 2025-11-25 |
| muscle_model (openworm) | `2b3c65f4e58f2088633ecbdb930f55701581ea7d` | 2025-05-15 |
| NeuroML2 (NeuroML) | `a5f5dadccd23606e683eaa0dd58dd2c3b2a7ed58` | 2026-09-02 |
| GoCModel_Basic (harshagurnani) | `90950b59d5dc3e285f2c05cf9d26e39a4357c2ab` | 2023-08-10 |
| BahlEtAl2012_ReducedL5PyrCell | `8275beaa52267801720d1664856d13e5d56bd11c` | 2025-08-22 |
| ca1 (mbezaire) | `a8655fa8614687276b82d88599c818dc29cb522f` | 2025-08-22 |

Publications (all DOIs resolved in Crossref):

| model_id | publication |
|---|---|
| hay2011_soma | Hay et al. 2011, PLoS Comput Biol 7(7):e1002107, doi:10.1371/journal.pcbi.1002107 |
| bbp2015_soma | Markram et al. 2015, Cell 163(2):456-492, doi:10.1016/j.cell.2015.09.029 |
| migliore2005_ca1_soma | Migliore, Ferrante & Ascoli 2005, J Neurophysiol 94(6):4145-4155, doi:10.1152/jn.00521.2005 |
| traub2005_* | Traub et al. 2005, J Neurophysiol 93(4):2194-2232, doi:10.1152/jn.00983.2004 |
| osb_hh2_477127614 | Sadeh et al. 2017, J Neurosci 37(49):12050-12067, doi:10.1523/JNEUROSCI.0963-17.2017. This is the repository's citation; no publication describes the tuned cell itself. |
| boyle2008_muscle | Boyle & Cohen 2008, Biosystems 94(1-2):170-181, doi:10.1016/j.biosystems.2008.05.025 |
| acnet2_pyr_soma | Beeman 2013, BMC Neurosci 14(Suppl 1):P23, doi:10.1186/1471-2202-14-S1-P23. Channels from Traub et al. 1991, J Neurophysiol 66(2):635-650, doi:10.1152/jn.1991.66.2.635. |
| solinas2007_goc_gurnani | Solinas et al. 2007, Front Cell Neurosci, doi:10.3389/neuro.03.002.2007 |
| bahl2012_soma | Bahl et al. 2012, J Neurosci Methods 210(1):22-34, doi:10.1016/j.jneumeth.2012.04.006 |
| bezaire2016_olm | Bezaire et al. 2016, eLife 5:e18566, doi:10.7554/eLife.18566 |

### Per-candidate cautions

* **hay2011_soma / bbp2015_soma.**
  * Both are OSB-assembled "single segment/compartment" test cells, not published
    single-compartment models.
  * They use the same channel files and the Hay Ca-pool ComponentType, so they must never be split
    across discovery and held-out sets.
  * Their reference spike trains come from NEURON and are used as the jNeuroML OMV reference.
    GitHub check-runs at both commits report jNeuroML success.
* **migliore2005_ca1_soma.**
  * The canonical run is short: 100 ms and 4 spikes.
  * The very small soma needs the small-cell rheobase bracket already flagged in sweep 1.
  * The Na channel lineage (`nax`) is shared with Migliore et al. 2014.
* **traub2005_*.**
  * Both are artificial channel-comparison cells.
  * There are no GitHub check-runs at this 2024 commit.
  * GPL-2.0 means copyleft obligations if files are redistributed.
  * `TestSeg_all` needs dt 0.0005 ms.
* **osb_hh2_477127614.**
  * It has only a validation OMV test. The behaviour numbers are optimiser metadata.
  * The harness is a 7-cell f-I protocol, so the column choice matters.
  * Its Na, Kd, IM and IL kinetics are the Pospischil ones: effectively related to the existing
    `pospischil2008` family.
  * The Allen Cell Types data it was tuned to may carry Allen terms. The AllenInstituteNeuroML
    repository explicitly excepts Allen-reused material; MultiscaleISN does not mention it.
* **boyle2008_muscle.**
  * It is a muscle cell with a resting potential near -28 mV (NeuroML-DB NMLCL001548), so the
    shipped harness holds it at -120 pA.
  * A comment in the shipped Ca pool file questions whether the pool suits the muscle model.
* **acnet2_pyr_soma.**
  * The LGPL-3.0 grant is the NeuroML2 repository's. OpenSourceBrain/ACnet2 itself has no licence.
  * The four `pyr_soma_*` files are the same cell with different file layouts.
* **solinas2007_goc_gurnani.** Low confidence:
  * The harness includes `../../Mechanisms/*.nml` from `Network/`, which points outside the
    repository. The cell file's own includes do resolve.
  * `CaLVA` is a `channelDensityNernst` on ion `ca2`, but the `ca2` species is commented out.
  * The output directory `../Data_OneGoC/` is not in the tree.
  * The cell file also holds a `network` element.
  * There is no CI.
  * The README warns of voltage runaway unless dt ≤ 0.001 ms, but the harness uses 0.0025 ms.
* **bahl2012_soma, bezaire2016_olm.**
  * Neither has a licence.
  * Bezaire is multicompartmental (8 segments). Its jNeuroML_NEURON and NEURON check-runs failed
    at this commit; jNeuroML_NetPyNE succeeded.
  * Bahl's NEURON:8.2.6 run failed while its jNeuroML run succeeded.

## 4. Rejected or not pursued

| repository (licence) | reason |
|---|---|
| OpenSourceBrain/AllenInstituteNeuroML (MIT, Allen-reused material excepted) | `Cell_*.cell.nml` are full perisomatic morphologies (~300 KB each); GLIF models are not conductance-based. The tuned single-compartment `tune/tuned_cells/AllenHH` and `HH2` cells have no harness of their own: the `tune/prototypes` harnesses target the untuned prototype cell `RS`. AllenHH channels are Hay/BBP-lineage, and Allen terms may apply. |
| OpenSourceBrain/BlueBrainProjectShowcase, other NMC cells (MIT) | Full morphologies, 0.27-2.1 MB each (NeuroML-DB: tens to hundreds of compartments). |
| OpenSourceBrain/L5bPyrCellHayEtAl2011, `L5PC.cell.nml` (MIT) | 1.19 MB; 642 compartments (NeuroML-DB NMLCL000073). |
| OpenSourceBrain/CA1PyramidalCell, `CA1.cell.nml` (MIT) | 762 KB; 3008 compartments (NeuroML-DB NMLCL000001). |
| OpenSourceBrain/Thalamocortical, full Traub cells (GPL-2.0) | 763-1472 compartments each (NeuroML-DB); too slow for jLEMS batteries. |
| OpenSourceBrain/FergusonEtAl2013-PVFastFiringCell (MIT-type) | The only NeuroML2 cell is an Izhikevich-type custom component (`IzhikevichFerguson.xml`), not conductance-based. |
| OpenSourceBrain/MultiscaleISN, `L23_NoHotSpot` / `L23_Retuned` (MIT) | Multicompartment Smith et al. 2013 cells (~0.76-0.85 MB). The `singleCompAllChans` copy duplicates sweep 1. `HH2_476686112` has no harness in this repository. |
| OpenSourceBrain/SadehEtAl2017-InhibitionStabilizedNetworks (MIT-type) | No `.cell.nml` files; PyNN/NEST spiking-network code. |
| OpenSourceBrain/EDENShowcase (MIT) | Only a copy of the HH example and an Izhikevich 2007 cell. |
| OpenSourceBrain/NeuroMLSBMLShowcase (MIT) | Passive BallAndStick (as in sweep 1). |
| OpenSourceBrain/destexhe_jcns_2009 (BSD-3-Clause) | NEURON/`.oc` integrate-and-fire network code; no NeuroML. |
| Brunel2000, PotjansDiesmann2014 (GPL-3.0), IzhikevichModel (BSD-3), FitzHugh-Nagumo | Not conductance-based single-cell models. |
| NeuroML/NeuroML2, other LEMS examples (LGPL-3.0) | Variants of the HH example already in the pool (Ex1, Ex5, Ex10, Ex18, Ex24), abstract models (Ex0 IaF, Ex2 Izh, Ex8 AdEx, Ex9 FN), and Ex22 Pinsky-Rinzel (custom cell type, screened out in sweep 1). `pyr_4_sym` is multicompartment. |
| NeuroML/NeuroMLlite (LGPL-3.0) | `acnet2/bask.cell.nml` is a 2-compartment basket cell with no single-cell harness (only the network example Ex4); `hhcell` duplicates HH. |
| NeuroML/pyNeuroML (LGPL-3.0) | `examples/test_data` holds copies of cells from other sources (ACnet2 basket, OLM, HH). |
| openworm/c302 (MIT) | Cells are multi-segment morphologies with generic parameter sets inside generated networks. The single-compartment Boyle & Cohen muscle is taken from `muscle_model` instead. |
| harshagurnani/GoCModel_Basic, other cells (GPL-3.0) | The 10-compartment reduced Golgi cells come from a PhD thesis (no DOI); the reconstructed morphologies are 1.4 MB. |
| andrisecker/CA1-Oriens-Lacunosum-Moleculare---Lawrence-et-al.-2006 (no licence; the parent agmccrei repository also has none) | `LawrenceOLM.cell.nml` has 1065 segments; its OMV test is jNeuroML_NEURON only. |
| mbezaire/ca1, other cells (no licence) | 45-53 compartments (NeuroML-DB) or full pyramidal morphology. |
| OpenSourceBrain/BahlEtAl2012_ReducedL5PyrCell, `pyr.cell.nml` (no licence) | 27-segment multicompartment version; only a jNeuroML_NEURON OMV test. |
| OpenSourceBrain/HNN (no licence) | Single-compartment `CELL_HH_simple_L2Basket/L5Basket` exist, but there is no licence and no harness (validation test only). |
| OpenSourceBrain/CerebellarNucleusNeuron, GranCellSolinasEtAl10 (no licence) | No `.cell.nml` in the tree at HEAD (only NEURON tests and GHK/Nernst `.omt` stubs); unlicensed anyway. |
| OpenSourceBrain/Ferrante2009-DentateGyrusGranuleCell, TobinEtAl2017 (no licence) | Multicompartment (250 KB granule cell; neuroConstruct projection neurons). |
| OpenSourceBrain/BartosEtAl2002, OSB_Samples, NEURONShowcase, XPPShowcase, ghk-nernst (no licence) | Synapse tests only, copies of HH/BBP cells, or abstract models. |
| OSB forks NicolettiEtAl2024_MN_IN, Maki-MarttunenEtAl2020 | No NeuroML files (ModelDB NEURON mirrors); the first has no licence, the second has per-cell BBP LICENSE files. |
| NeuroML-DB | Used for cross-checks only. Its single-compartment cells are the HH, Pospischil, Izhikevich, Prinz and Pinsky-Rinzel cells (already covered), the Ferguson Izhikevich-type cell, the Boyle muscle (taken from GitHub), the Maex mossy-fibre stub and five Dura-Bernal 2017 M1 cells. The Dura-Bernal cell files were not inspected; sweep 1 judged M1NetworkModel Izhikevich-based. NeuroML-DB gives no commit or licence to pin. |

## 5. Which candidates look best for diversity

The recommended order to simulate is below. Screening should use the same `verify_candidates.py`
battery and Ih-block control as sweep 1, after the licence gate.

1. **`traub2005_testseg_all`**: the best single shot at the sag/rebound gap (ar + cat + cal, AHP
   and C-type K), with a jNeuroML reference. Accept GPL-2.0, or keep the files fetch-only.
2. **`hay2011_soma`** (or `bbp2015_soma`, but not both in different splits): MIT, Ih + T-type Ca +
   SK, quiescent-looking cell, NEURON-matched reference. `bbp2015_soma` has the more clearly
   adapting reference.
3. **`acnet2_pyr_soma`**: the clearest adaptation in any shipped reference, with a minimal
   4-channel set. Resolve the upstream-licence question first.
4. **`migliore2005_ca1_soma`**: MIT, A-type-K-dominated tonic firing, very small soma (threshold
   diversity).
5. **`boyle2008_muscle`**: MIT, the only Na-free, Ca-spiking cell (channel-composition diversity).
   It is not a neuron, which the study should decide on explicitly.
6. **`osb_hh2_477127614`**: MIT, data-tuned high threshold with a steep f-I relation. Treat it as
   related to `pospischil2008`.
7. **Conditional:**
   * `bahl2012_soma` (phasic firing) and `bezaire2016_olm` (HCN interneuron) need licence
     clearance from the authors.
   * `solinas2007_goc_gurnani` (HCN pacemaker) needs its harness and `ca2` problems fixed before
     it can be trusted.

**Pool size if all licensed candidates survive screening.** Sweep 1 had 13 models in 7 families.
The 8 licensed candidates other than the Golgi cell add 6 families (`hay2011_bbp_channels`,
`migliore2005`, `traub2005`, `boyle2008`, `acnet2_traub1991`, `osb_allen_hh2`). That gives 21 models
in 13 families, or 22 in 14 with the Golgi cell. `osb_allen_hh2` is correlated with Pospischil, and
`migliore2005` may be grouped with `migliore2014`. That leaves room
to hold out whole families while keeping 12-16 models.
