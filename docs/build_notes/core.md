# Build note: core-tests (tests for the already-implemented core modules)

Owner: core-tests. Environment: Windows 11, Python 3.12 venv, pyneuroml 1.3.22 (bundled
jNeuroML 0.14.0 / jLEMS 0.12.0), libNeuroML 0.6.7, Temurin 21.0.12.1, branch `m0-audit`.
Date of all measurements: 2026-09-13.

Test files:

| file | what it covers |
|---|---|
| `tests/unit/test_units.py` | parse / SI table (hand-derived factors for every unit) / convert / degC offset / `format_number` (never `e+`, round-trips 5000 random doubles incl. subnormals) / formatted strings vs the real NeuroML_v2.3.1.xsd patterns |
| `tests/unit/test_provenance.py` | hashes (FIPS vector), canonical JSON, tree manifests + exclusion rules, `write_immutable` (read-only, identical rewrite no-op, different content raises, no tmp leftovers), environment digest, git state, relpath |
| `tests/unit/test_rheobase_search.py` | `search` on fake counters with exact hand-derived brackets (monotonic, expansion, clamp, spontaneous, not_found, non-monotonic, non-reproducible, errors), `count_upward_crossings` |
| `tests/unit/test_protocol_definitions.py` | every template's instantiation, integer-ms edges on every refinement grid, windows, rheobase scaling, chirp/noise raise, config overrides, feature/tolerance catalogue consistency |
| `tests/unit/test_generate_xml.py` | network/LEMS XML structure (lxml), XSD validation against the installed v2.3.1 schema, `write_probe` bundles, grouping, harness step/length parsing on every shipped harness |
| `tests/unit/test_models_manifest.py` | manifest columns, rows checked against snapshot files (cell ids, harness OutputFile/column), round trip, workspace materialisation (byte-exact, writable, raw untouched), `neurosem.config` |
| `tests/integration/test_jneuroml_adapter.py` | real jnml: validate valid / schema-invalid / bad reference / broken include / truncated / mixed / missing file; shortened RS harness run; stale output; sampling; spaces in paths; BUILD_ERROR, RUNTIME_ERROR, TIMEOUT, TOOL_FAILURE; UNSTABLE rule on synthetic `.dat` through real `load_dat`; a real blow-up |
| `tests/integration/test_probe_battery.py` | all 9 implemented templates on RS (rheobase 0.1 nA, settle 300 ms, dt 0.025 ms) grouped by length; exact onset timing; jnml -validate of generated networks; the Meta integrator fact; `make_step_counter` on a real simulation |

Result at hand-off: 367 tests in these eight files, 358 passed and 9 `xfail(strict=False)`
that pin the defects below (each xfail reason links an anchor here); 63 s for all eight files
together (unit files about 8 s; `test_jneuroml_adapter.py` about 17 s; `test_probe_battery.py` about 26-35 s).
Whole-suite collection (`pytest -q -x --co`) succeeded with 687 tests collected, including other modules' files.

---

## Defects found (keep the tests; fix the modules)

<a id="generate-element-order"></a>
### 1. `generate.network_xml` writes schema-invalid networks when a ramp precedes a pulse (severity: high)

`NeuroMLDocument` in NeuroML_v2.3.1.xsd is an `xs:sequence`; its `InputTypes` group
fixes the order `pulseGenerator*, pulseGeneratorDL*, sineGenerator*, sineGeneratorDL*,
rampGenerator*, ...`. `network_xml` emits generators in protocol order, so the default
battery (P06_ramp comes before P07/P08/P09/P10 pulses) produces a `pulseGenerator` after
a `rampGenerator`.

Reproduction (both validators agree):

```python
from neurosem.models import load_models, materialize
from neurosem.protocols.definitions import DEFAULT_TEMPLATES, batched
from neurosem.protocols.generate import write_probe
from neurosem.schemas import ExecConfig
from neurosem.simulators.jneuroml import JNeuroML
ws = materialize(load_models()["pospischil2008_rs"], Path("work/tmp/x/rs"))
b = write_probe(ws, [t.instantiate(0.1, 300) for t in batched(DEFAULT_TEMPLATES)], ExecConfig(0.025))
JNeuroML().validate([b.net_file]).valid   # False: "is not valid against the schema ... NeuroML_v2.3.1.xsd"
```

lxml against the installed XSD reports
`Element 'pulseGenerator': This element is not expected. Expected is one of ( rampGenerator, ...)`.
Measured: default order → invalid (jnml and lxml); pulses only → valid; ramp first then pulses → invalid;
pulses first then ramp → valid. jLEMS still *runs* the file (it does not enforce element order), which is
why the battery simulations succeed, but any structural check of generated probe files, or reuse of
them as NeuroML documents, fails. `run_battery` hides it only because `group_by_length` happens to put
P06 alone in its group with the default catalogue; any config change that gives a ramp the same length
as a pulse protocol exposes it.

Proposed patch (`src/neurosem/protocols/generate.py`, inside `network_xml`), replacing the
component loop:

```python
    inputs: list[tuple[str, str, str]] = []
    pulse_lines: list[str] = []
    ramp_lines: list[str] = []
    for p in protocols:
        pop = population_id(p.protocol_id)
        for i, comp in enumerate(p.components):
            cid = f"{pop}_c{i}"
            xml = _component_xml(cid, comp)              # raises ValueError for unsupported kinds, as before
            (pulse_lines if comp.kind == "pulse" else ramp_lines).append(xml)
            inputs.append((cid, pop, p.protocol_id))
    lines += pulse_lines + ramp_lines                    # XSD InputTypes sequence: pulseGenerator before rampGenerator
```

Component ids, populations and inputLists are unchanged, so simulated traces are expected to be
identical (jLEMS resolves generators by id); confirm by rerunning `tests/integration/test_probe_battery.py`.
Pinned by: `test_generate_xml.py::test_full_battery_network_is_schema_valid`,
`::test_ramp_before_pulse_order_is_schema_valid`,
`test_probe_battery.py::test_one_file_full_battery_network_passes_jnml_validation`.

<a id="jnml-blowup-status"></a>
### 2. A numerical blow-up during stepping is classified `BUILD_ERROR` (severity: medium)

`JNeuroML.run_lems` decides `RUNTIME_ERROR` vs `BUILD_ERROR` only by whether the output
contains `Finished N steps`, which jLEMS prints after the *last* step. A simulation that
diverges mid-run throws before that line, so it is labelled a build failure. Under
`fingerprint.classify` that is class 2 (non-executable) instead of class 3 (numerically
unstable), so solver-configuration and dt mutants that blow up are misclassified.

Reproduction: RS, one population, 100 nA pulse from 10 to 30 ms, `ExecConfig(0.1)`, 50 ms.

```python
p = [ConcreteProtocol("U1", "step", (StimulusComponent("pulse", 10, 20, 100.0),), 50, AnalysisWindow(10, 30), ())]
b = write_probe(ws, p, ExecConfig(0.1), tag="blowup")
JNeuroML().run_lems(b.lems_file, [b.output]).status   # RunStatus.BUILD_ERROR
```

Message: `SEVERE: (ERROR) org.lemsml.jlems.core.run.RuntimeError: Error at PathDerivedVariable eval() ...`;
the state dump in the output shows `r = Infinity, t = 0.0113 (s), v = -172.61 (V)`, i.e. the integrator
had already stepped past the 10 ms onset and diverged. Ladder measured (dt 0.1 ms): 5 nA and 20 nA OK
(|v| ≤ 87.4 mV); 100 and 1000 nA throw. At dt 0.5 ms even 5 nA throws. In none of these cases did jLEMS
write out-of-bound voltages to the `.dat`: it throws first, so the existing `UNSTABLE` check on traces
is never reached for this model (it still covers NaN/out-of-bound output, tested with synthetic files).

Proposed patch (`src/neurosem/simulators/jneuroml.py`, `run_lems`, replacing the returncode branch):

```python
        if proc.returncode != 0:
            if "org.lemsml.jlems.core.run.RuntimeError" in out:          # thrown while stepping, not while building
                diverged = re.search(r"=\s*-?(?:Infinity|NaN)\b", out) is not None
                status = RunStatus.UNSTABLE if diverged else RunStatus.RUNTIME_ERROR
            elif ran:
                status = RunStatus.RUNTIME_ERROR
            else:
                status = RunStatus.BUILD_ERROR
            return SimResult(status, proc.returncode, runtime, {}, cmd, _first_error(out), tail)
```
Evidence limits: the `core.run.RuntimeError` marker and the `Infinity` state dump were seen for this
one failure mode only (Kd rate evaluation); build failures seen so far raise
`org.lemsml.jlems.core.sim.ContentError` (missing include, unknown target). A stricter alternative is to
also parse `v = <number>` from the dump and apply `PHYSICAL_V_BOUND_MV` (in volts).
Pinned by: `test_jneuroml_adapter.py::test_real_numerical_blowup_is_unstable_not_build_error`.

<a id="rheobase-inverted-bracket"></a>
### 3. `rheobase.search` can return `status="ok"` with an inverted bracket (severity: medium)

In the bracketing phase, after an expansion `lo` is the previous (silent) `hi`. If the new
grid spikes already at its first point (`i == 0`), `amps[i - 1]` wraps to the *last* point:

```python
calls = {"n": 0}
def counter(amps):
    calls["n"] += 1
    return [0] * len(amps) if calls["n"] == 1 else [1] * len(amps)
r = search(counter, hi_nA=0.5, grid=11, rounds=4)
# r.status == "ok", r.lower_nA == 2.0, r.upper_nA == 0.5, r.resolution_nA == -1.5, r.rheobase_nA == 0.5
```

A deterministic simulator cannot trigger it (the first point of the new grid equals the
previously silent amplitude), but a non-reproducible response (a flaky run, a stochastic
model, a counter bug) silently yields a negative resolution and a wrong rheobase with
status ok. The refinement phase already guards the same case ("lower bracket edge spiked;
bracket kept").

Proposed patch (`src/neurosem/protocols/rheobase.py`, bracketing phase):

```python
        idx = np.flatnonzero(counts > 0)
        if idx.size:
            i = int(idx[0])
            if i == 0:        # lo (> 0) was silent in the previous grid and now spikes: not reproducible
                history[-1]["note"] = "previously silent amplitude spiked; response not reproducible"
                return RheobaseResult(None, "error", None, None, n_sims, history)
            lo, hi = float(amps[i - 1]), float(amps[i])
            break
```

Pinned by: `test_rheobase_search.py::test_lower_edge_spiking_after_expansion_never_returns_inverted_bracket`.

<a id="units-kelvin-not-xsd"></a>
### 4. `units.UNITS` lists `K`, which the NeuroML temperature pattern forbids (severity: low, hazard)

`Nml2Quantity_temperature` in v2.3.1 is `...[\s]*(degC)`. `units_for("temperature")` returns
`["K", "degC"]`, so a `unit_conversion` transform that trusts `units_for` would write a
schema-invalid `temperature="309.15 K"`. Every other supported dimension's units are a subset of the
XSD units (tested). Keeping `K` for SI conversion is reasonable; the fix is to expose the schema
subset, e.g.

```python
XSD_UNITS = {"temperature": ("degC",), ...}          # or: def schema_units_for(dimension) -> list[str]
```

or at minimum document in `units_for` that it is not XSD-filtered. The ARCHITECTURE transform contract
("only unit strings permitted by the NeuroML v2.3.1 XSD pattern") then has a single source.
Pinned by: `test_units.py::test_every_neurosem_unit_is_permitted_by_xsd[temperature]`.

<a id="units-molar-missing"></a>
### 5. `units.parse` rejects the schema-valid concentration unit `M` (severity: low)

`Nml2Quantity_concentration` allows `mol_per_m3|mol_per_cm3|M|mM`; `parse("1 M")` raises
`unknown unit 'M'`. Patch: add `"M": ("concentration", 1e3, 0.0)` (1 mol/L = 1000 mol/m3).
Not covered at all (whole dimensions absent): resistance (`ohm|kohm|Mohm`), permeability,
currentDensity, rhoFactor, conductancePerVoltage. A scan of every quantity-like attribute in
`models/raw/**/*.nml|xml` (151 values) found only one unparseable value, `96485.3 C_per_mol` on a
LEMS `<Constant>` in `PospischilEtAl2008/NeuroML2/channels/Ca/Ca.nml`, which is a LEMS dimension, not an
Nml2Quantity; mutation/transform code must not assume every numeric attribute parses.
Pinned by: `test_units.py::test_every_xsd_unit_is_parseable[concentration]`.

<a id="models-manifest-validation"></a>
### 6. `models.load_models` validation gaps (severity: low)

(a) A header-only manifest with wrong columns loads as `{}` without error, because missing columns
are computed from `rows[0]` and fall back to `MANIFEST_COLUMNS` when there are no rows.
(b) Duplicate `model_id` rows silently overwrite each other (last row wins).

Patch:

```python
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        header = reader.fieldnames or []
    missing = set(MANIFEST_COLUMNS) - set(header)
    if missing:
        raise ValueError(f"model manifest missing columns: {sorted(missing)}")
    ids = [r["model_id"] for r in rows]
    if dup := sorted({i for i in ids if ids.count(i) > 1}):
        raise ValueError(f"duplicate model_id in manifest: {dup}")
```

Pinned by: `test_models_manifest.py::test_header_only_manifest_with_wrong_columns_is_rejected`,
`::test_duplicate_model_ids_are_rejected`.

---

## Empirical tool facts recorded by these tests

<a id="jlems-meta"></a>
### jLEMS ignores `<Meta for="jlems" method=...>` for this core-type cell (no observable effect)

Setup: RS workspace, probe with P02_weak_step + P04_step_2x (rheobase 0.1 nA, settle 100 ms, 800 ms,
dt 0.025 ms), generated by `lems_xml` with `ExecConfig.integrator_method` in
`{None, "rk4", "eulertree", "bogus"}`.

- The four OutputFiles are **byte-identical** (sha256 `4ae44c0d0a9134feb2bcfe32db311f226a34209ed2cf685e9a7b8086d1f686d6`).
- The full jnml console output of every run contains no line mentioning `meta`, `method`, `rk4`,
  `euler` or `unrecognized`, including for the invalid value `bogus`.
- On a separate 100 ms hyperpolarising step, `method="rk4"` and no Meta gave identical sampled
  voltages at all 5 dt levels tested (0.1 to 0.00625 ms).

This matches the audit's source reading that `rk4` is a no-op under jnml's `sim.run()`, and goes
further: `eulertree` and even an invalid method string also change nothing observable through jnml
0.14.0 (so the audit's "eulertree changes the path" does not show up in results for this model).
Consequence for `mutations` (`solver_config` operator): expect these mutants to be equivalent under
jNeuroML; they are still worth running as no-op controls. The fact is pinned by
`test_probe_battery.py::test_meta_integrator_method_does_not_change_trace`, which will fail if a
future jar starts honouring Meta.

Related evidence on the default integrator (one model, one protocol, not a pinned test): errors of
V(50 ms) and V(79 ms) under a -0.1 nA step relative to dt = 0.00625 ms shrank by factors of 1.3-5.3 per
halving of dt from 0.1 ms, consistent with first order and not with 4th-order RK4 (factor ~16). The
ratios are noisy because errors approach the output resolution (see below). This supports
`configs/study.yaml`'s forward-Euler statement.

### jLEMS OutputFile format

Tab-separated, trailing tab, SI units, about 7 significant digits, e.g. `2.5E-5\t-0.07000154\t`.
The voltage resolution is therefore about 1e-5 mV; the time grid has relative jitter below 1e-6
(measured 0.024999999999977 to 0.025000000000034 ms). `load_dat` converts correctly (tested on real and
synthetic files).

### Other measured behaviour

- `jnml -validate`: valid → rc 0, "All valid"; schema violation → rc 1 with `cvc-pattern-valid` message;
  bad channel reference → rc 1, "Valid against schema" plus `Test: 10025 (Ion channel in channelDensity
  should exist) failed!`; broken `<include href>` → the same Test 10025 failure (the missing include is
  reported as a missing channel); truncated XML → rc 1, invalid; mixed batch → summary
  `Validated 2 files: 1 passed, 1 failed`.
- `jnml -validate` on a **nonexistent path** prints usage text plus `File does not exist` and no summary
  line; the adapter returns `valid=None` ("unrecognised validator output"), i.e. tool failure. Suggest
  checking `Path.is_file()` first and raising `FileNotFoundError`, so a caller error is not recorded
  as a tool failure (not pinned as xfail; current behaviour is tested as "never valid").
- Missing `<Include>` in a LEMS file → rc 1, `ContentError: Can't find file at path: NoSuch.net.nml`
  → `BUILD_ERROR`. Unknown simulation target → `ContentError: No component found: no_such_net` → `BUILD_ERROR`.
- Workspace paths containing spaces work for both validation and runs.
- All populations of a batched probe are uncoupled: RS P04's trace in the 9-cell group is bit-identical
  to the same protocol in a 2-cell run, and every trace is bit-identical to the zero-current baseline
  until its stimulus onset. Pulse onsets become visible within 2 dt after `delay`; the ramp (starting
  from 0 nA) within 1 ms, limited by output resolution.

<a id="p09-charge"></a>
### P09/P10 suprathreshold only at a realistic rheobase

The battery integration test scales by an assumed 0.1 nA (as assigned). At that scaling P09
(1 nA x 3 ms) only reaches -61.6 mV and P10 -60.8 mV, with no spikes, so the test asserts timing
only. Scratch check (not a pinned test): `rheobase.search` with the `configs/study.yaml` parameters
on RS at **dt 0.025 ms** (not the nominal 0.005 ms) gave 0.56065 nA (bracket [0.56055, 0.56065],
5 simulations, 1.92 M cell-steps). At that rheobase P09 fires 1 spike and P10 2 spikes inside their
windows. Note that with 0.1 nA scaling most "spiking" protocols are subthreshold for RS; the battery
test is about stimulus timing, not firing.

---

## Hazards and suggestions for other module owners (no test failure)

- **Workspace tree hash changes after probing**: `write_probe` writes `ns_*.net.nml`, `LEMS_ns_*.xml`
  and (after a run) `ns_*_v.dat` into the workspace, so `Workspace.tree_sha256()` differs before and
  after a battery (tested in `test_generate_xml.py::test_write_probe_changes_workspace_tree_hash`).
  `execution`/`mutations`: compute `VariantRecord.tree_sha256` before generating probes, or exclude
  generated names.
- **`tree_manifest` exclusion is by file name at any depth** (a nested `sub/variant.json` is also
  excluded) and ignores empty directories; tested as the current contract.
- **`ProtocolTemplate.instantiate` does not enforce integer-ms `settle_ms`**; a non-integer settle
  would silently move stimulus edges off the refinement grids. Suggest
  `if not float(settle_ms).is_integer(): raise ValueError(...)`.
- **P10 "20 ms apart"** means a 20 ms gap between the end of pulse 1 and the start of pulse 2
  (onsets 23 ms apart); the description could say so.
- **`JNeuroML.version_info` uses `functools.cache` on a method**: the cache keeps the instance alive
  and ignores later changes to `java`/`jar` on the same instance.
- **`JNeuroML(java=None)` auto-discovers Java**, so "java is None" can only be tested by setting the
  attribute after construction (the tests do that).
