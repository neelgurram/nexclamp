# Build note: `neurosem.transforms`

Module: `src/neurosem/transforms/` (ARCHITECTURE.md section 3.5). Items below need a decision or
a change outside this module, or record tool behaviour found while building it.

## 1. Contract / integration items

1. **`Site` is defined locally.** `mutations/base.py` did not exist when this module was built,
   so `transforms.formatting.Site` repeats the section 3.4 shape (`operator, file, locator,
   params`). Suggest one shared definition (e.g. `mutations.base.Site` re-exported, or a small
   `neurosem.sites` module) once `mutations` lands.
2. **`model_overrides` must be applied by execution code.** `Workspace.model` is a frozen
   `ModelRecord`. A variant produced by renaming the cell has `model_overrides={"cell_id": ...}`;
   `protocols.generate.write_probe` reads `ws.model.cell_id`, so `validation.execution` must build
   the probe from `Workspace(ws.root, dc.replace(ws.model, **variant.model_overrides))`.
   Helper provided: `neurosem.transforms.apply_model_overrides(ws, overrides)`. Without it a
   correct rename would surface as `BUILD_ERROR`, a false detection.
3. **`data/valid_transforms.csv` has one extra column.** Section 2 says "same columns as the
   mutation manifest plus `no_change`". `transforms.write_manifest` appends
   `model_overrides_json` after `no_change`, because a cell rename cannot be reproduced from the
   manifest without it. Please either accept the column in ARCHITECTURE.md or move overrides into
   `params_json`.
4. **Locators in rename edits refer to the pre-edit document** (the renamed element's own
   locator contains the old id). This is stated in each `Edit.note`.

## 2. Tool behaviour observed (jNeuroML 0.14.0, this machine)

These are observations from the module's tests, not study results.

1. **Warnings make `JNeuroML.validate` return `valid=False`.** `jnml -validate` exits 0 and
   prints `Validated 1 files: 0 passed, 1 passed with warnings`. The core adapter requires the
   summary to contain "All valid", so warnings count as invalid. Seen with check 100005 ("Segment
   Group used in the include element of segmentGroup should probably be defined BEFORE it is
   used ... for optimal portability") after reordering segment groups. The transforms module now
   never reorders segment groups. Whether warnings should mean "structurally invalid" (mutant
   class 1) is a decision for `validation.structural`; it is not changed here.
2. **`jnml -validate` rejects LEMS files** (`cvc-elt.1.a: Cannot find the declaration of element
   'Lems'`). Edits to a shipped harness (rename paths, reordered `<Include>`, comments,
   formatting) can only be checked by running the harness. The integration test runs a
   shortened copy (60 ms at dt 0.025 ms) and compares the voltage column.
3. **Two pristine LTS dependency files fail validation when validated on their own.**
   `NeuroML2/channels/IT/IT.channel.nml` fails with `cvc-enumeration-valid: Value 'IT_s_gate'`
   (a custom gate type) and `NeuroML2/channels/Ca/Ca.nml` fails with `cvc-complex-type.2.4.a` at
   `decayingPoolConcentrationModelPosp`. `LTS.cell.nml`, which includes both, validates. Only the
   first schema error is printed, so later errors in these files are hidden. Consequences:
   - The integration test requires the cell file and network files to be valid. Any other touched
     file must be valid, or have validation messages identical to the pristine file.
   - `factor_file` moves a component only if every NeuroML element in it is typed by the XSD.
     Otherwise the new file would be invalid by construction (seen with the Ca-pool
     `ComponentType` containing `<Child>`).
4. **`segmentGroup="all"` validates even where no group `all` is defined** (HH example), so the
   XSD default is honoured by jNeuroML's reference checks (test 10006).
5. **`jnml -validate` follows includes** for reference tests (10025, "Ion channel in
   channelDensity should exist"). A broken rename or factoring is therefore caught at the
   NeuroML level, not only when a simulation is built.

## 3. Design decisions worth reviewing

- Edits are byte-preserving: a quote-aware scanner gives element spans, and edits are range
  replacements. Scanner and lxml are cross-checked on every load, so a variant differs from its
  parent only where the `Edit` list says.
- Unit strings come from the `Nml2Quantity_*` XSD patterns of libNeuroML's NeuroML_v2.3.1.xsd.
  Unit factors come from `NeuroMLCoreDimensions.xml` inside the pyNeuroML jNeuroML jar. Units
  with an offset (`degC`) are never converted.
- Comments are not rewritten by `rename_identifier`. For example, the HH harness keeps
  `hhpop[0]` inside commented-out `<Line>` elements, which no tool reads.
- `rdf:about` values equal to a renamed id (or `#id`) inside the renamed element are updated.
- Rename sites are offered only for definitions that are unique for their kind in everything
  their scope can see. Segment groups whose id is an XSD default (`all`) are never renamed.

## 4. Tests

- `tests/unit/test_transforms.py` needs no Java: it checks the XSD and unit sources,
  Decimal exactness, schema patterns, kind- and scope-correct renames, include reachability
  after factoring, semantic identity of the no-change controls, and determinism.
- `tests/integration/test_transforms_validate.py` (`jnml`) has three tests:
  - `test_every_transform_validates_with_jnml`: a seeded sample of 4 sites per operator,
    plus shortened harness runs for LEMS edits.
  - `test_probe_traces_match_reference`: 300 ms probes compared with numpy.
  - `test_all_sites_validate_with_jnml` (also marked `slow`): every site of every operator,
    validated only, with no harness runs.
- jnml is called with at most 100 files per invocation, because Windows limits a command line
  to 32 767 characters.

## 5. Test observations (exploration, not claims)

During development, one variant per operator per model (RS, LTS, HH) was probed for 300 ms at
dt 0.025 ms with a depolarising and a hyperpolarising step. Short harness copies were also run
for every sampled variant that edited a LEMS file. All compared voltage columns were bitwise
identical to the reference. Last-bit differences remain possible in principle (see the
docstring of `transforms/units.py`). This observation covers a finite subset at one dt and is
not evidence of equivalence in general.
