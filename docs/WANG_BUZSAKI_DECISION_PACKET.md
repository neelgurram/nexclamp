# Wang–Buzsáki model: decision packet

*Model `wangbuzsaki1996_wb` (OpenSourceBrain/WangBuzsaki1996 @ `c5322844`, MIT, NeuroML2 directory).
Prepared 2026-09-17 for Neel. The model's status in the primary study is **undecided**: it is neither
included nor excluded until Neel decides.*

## In plain English

- **The problem.** The model runs fine, but its file uses a construction the NeuroML 2.3.1 format
  rules do not allow. The format checker rejects it, and our inclusion rules require the checker to
  pass.
- **Why a fix isn't simple.** Making the file pass would mean rewriting part of the model by hand, or
  loosening our checker for this one model.
- **Recommendation.** Keep it out of the main analysis. It may be used in a clearly labelled side
  analysis.

## 1. The exact exception

- **File and line.** `NeuroML2/LEMS/WangBuzsaki.cell.nml`, line 10, reads
  `<gateHHrates type="gateHHratesInstantaneous" id="m" instances="3">`.
- **Validator result.** `jnml -validate` (jNeuroML 0.14.0, NeuroML v2.3.1 schema) rejects this with
  `cvc-complex-type.3.2.2: Attribute 'type' is not allowed to appear in element 'gateHHrates'`
  ("Validated 2 files: 1 passed, 1 failed"). The failing file is the cell file; the network file
  passes.
- **Old schema.** The file declares the older `NeuroML_v2beta5.xsd` schema location.
- **Runtime behaviour.** The `type` attribute is honoured by jLEMS at run time: it turns the sodium
  activation gate `m` into an instantaneous gate (m = m∞), as in the published model. The file is
  therefore not "wrong" for the simulator, only non-conformant to the current schema.
- **Other checks.** libNeuroML strict validation passes. The shipped simulation runs (100 ms, step
  0.001 ms, 2 pA from t = 0; 10 spikes). The smoke-test rheobase search found 0.00017 nA, consistent
  with conductances given in nS for a small cell.

## 2. Which inclusion criterion it violates

- **Criterion violated.** C04 "passes appropriate NeuroML validation" (execution plan, "Inclusion
  criteria").
- **Oracle rule.** Neuraxis's structural oracle (D-006) requires a reference's cell file and harness
  network files to validate. Only failures in *included* files, such as the Pospischil LTS channel
  files, are recorded as baseline errors.
- **Other criteria.** The curation workflow evaluates every other criterion mechanically; see
  `docs/MODEL_CURATION_REPORT.md` for this model's row.

## 3. What kind of issue it is

| Category | Affected? | Notes |
|---|---|---|
| Licensing | No | MIT for the NeuroML2 directory; the licence text was verified at the pinned commit |
| Provenance | No | commit-pinned, hash-verified snapshot |
| Validation | **Yes** | schema non-conformance of the model's own cell file |
| Manual repair | **Yes, if repaired** | a conformant file needs `<gateHHInstantaneous>` with an explicit steady-state expression, or a custom component type: a model-specific hand edit that changes the representation (not a byte-preserving transformation) |
| Numerical convergence | Not by this issue | measured separately (curation criterion C10) |
| Simulation behaviour | No | runs and spikes as expected |
| Protocol compatibility | No | all battery protocols ran in the smoke test |

## 4. Could the exception influence study outcomes?

**Structural classification.** If the error were accepted as a pre-existing baseline error, a WB
mutant would count as structurally invalid only if it introduced a *new* validation message. A mutant
whose own schema error produced exactly the same message text would be masked. No current operator
removes or edits the `type` attribute, so the practical effect is small. It still makes the oracle
weaker for this one model, and the rule would have been made after seeing the model.

**Kinetics mutations.** Gate `m` is a kinetics target (midpoint, slope). Its instantaneous
behaviour depends on the non-schema attribute, so any repair of the file would change what those
mutations test.

**No outcome data yet.** No WB mutant has been run, so nothing has been seen.

## 5. Scientific diversity lost if it is excluded

- **Cell type.** A fast-spiking interneuron from an independent source (Wang and Buzsáki 1996). The
  only other fast-spiking model in the pool is Pospischil FS, from the same source as the Pilot 1
  cells.
- **Mechanism.** Instantaneous sodium activation, a mechanism absent from the other models.
- **Scale.** Very low absolute rheobase, which tests amplitude scaling.

## 6. Exploratory sensitivity analysis only?

Yes. It can be run with the baseline-error exception, labelled "exploratory sensitivity: schema
non-conformant model accepted with a disclosed baseline error". It would be reported separately and
never pooled into the primary counts or the primary estimate.

## 7. Recommendation

- **Primary analysis: exclude.** The issue concerns validation and could only be resolved by a
  model-specific exception or a manual repair. That matches the default exclusion rule.
- **Log the exclusion.** Record it as C04 in `docs/MODEL_CURATION_REPORT.md`.
- **Optional sensitivity analysis.** If Neel wants the diversity, add WB only as the exploratory
  analysis above, prespecified in the Pilot 2 protocol before any WB mutant is run.
- **Pilot 2 default.** The PILOT_PROTOCOL_V2 matrix leaves WB out of the primary model set unless
  Neel chooses otherwise.
