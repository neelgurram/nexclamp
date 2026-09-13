# NeuroSem architecture and module contracts

This file is the implementation contract. Every module below has a fixed public API so
that modules can be built and tested independently. Names, signatures and file formats
here are binding for implementers; change them only by editing this file first.

Core modules already implemented and verified against real jNeuroML runs:
`schemas.py`, `units.py`, `provenance.py`, `config.py`, `models.py`,
`simulators/base.py`, `simulators/jneuroml.py`, `protocols/definitions.py`,
`protocols/generate.py`, `protocols/rheobase.py`.

### Implementation notes that refine the contract (validation/experiments layer, 2026-09-13)

- `RunRecorder.run_rheobase(ws, variant, level_exec, rcfg, settle_ms) -> RheobaseOutcome(result, status,
  search_id, record, cached)`. It stores one immutable `results/raw/<campaign>/<search_id>/rheobase.json` (spike
  counts per amplitude, cost, provenance) instead of per-simulation traces.
- `RunRecorder.run_canonical(ws, variant, canonical_proto, level_factor, replicate)` refines the shipped harness
  step by `level_factor` in a staging copy; the analysis window always comes from the REFERENCE harness.
- `convergence.calibrate(fp_by_factor, model_id, tol_cfg, features_cfg)` is keyed by refinement factor (1, 2, 4),
  not by float dt. `TolEntry` adds `kind`, `state_h`, `state_h2`, `note`; `tau=None` means excluded, `inf` means
  "undefined in reference at both levels" (only a definedness change can detect).
- `Fingerprint` adds `level_factor`, `messages`, `runtime_s`, `cell_steps`; `Detection` adds `variant_id`,
  `model_id`, `level_factor`. Fingerprint tables include `P00_canonical` and `P03_rheobase` (`{"rheobase": ...}`).
- `classify(structural_valid, fp_h, fp_h2, det_h, det_h2)` takes the boolean validity. SILENT = reproducible
  non-canonical detection with no canonical detection at the nominal level.
- Orchestration lives in `experiments/campaign.py` (reference, calibrate, generate, variant, aggregate stages);
  `experiments/pilot.py`, `discovery.py`, `heldout.py` and `analyze.py` build on it.

## 1. Data flow

```
models/raw/<snapshot>/            pinned upstream model files (tracked, byte-exact)
        │  models.materialize()
        ▼
work/variants/<model_id>/<variant_id>/   writable workspace + variant.json   (git-ignored, regenerable)
        │  mutations.* / transforms.*  (edit files, record Edit list)
        ▼
validation.structural.check()     jnml -validate (authoritative) + libNeuroML strict (informational)
        │
validation.execution.run_battery()   batched probe runs (protocols.generate) at dt levels
validation.execution.run_canonical()  shipped harness (canonical protocol)
        │      every simulation -> RunRecorder -> results/raw/<campaign>/<run_id>/{run.json, traces.npz}
        ▼
features.efel_adapter.extract()   FeatureTable per protocol (from the *stored* trace representation)
        │
validation.fingerprint             Fingerprint = rheobase + FeatureTables for all protocols at one dt
validation.convergence.calibrate   ToleranceTable from reference fingerprints at h, h/2 (, h/4)
validation.fingerprint.compare     list[Detection] (protocol, feature, values, tau, evidence run ids)
        │
validation.classify (in fingerprint.py)   MutantClass 1..6 per variant
        │
selection.matrix -> selection.greedy / random baselines (DISCOVERY split only)
        │
analysis.metrics / analysis.bootstrap / analysis.figures
```

## 2. Directory and file formats

| Path | Tracked | Content |
|---|---|---|
| `data/model_manifest.csv` | yes | `ModelRecord` rows (columns = dataclass fields) |
| `data/protocol_manifest.csv` | yes | generated from templates: `protocol_id,kind,description,params_json,features,implemented,not_implemented_reason` |
| `data/mutation_manifest.csv` | yes | one row per mutant: `variant_id,model_id,family,operator,params_json,edits_json,exec_overrides_json,description,generator_seed` |
| `data/valid_transforms.csv` | yes | same columns as mutation manifest, `family` = transform category, plus `no_change` flag |
| `data/splits/discovery_models.txt` | yes | one model_id per line |
| `data/splits/heldout/heldout_models.txt` | yes | held-out model ids (read ONLY by `selection.splits.HeldoutGate`) |
| `data/splits/heldout/heldout_families.txt` | yes | held-out mutation families |
| `data/splits/SPLITS.sha256` | yes | `sha256  relative/path` lines for all split files |
| `work/variants/<model>/<variant>/` | no | workspace + `variant.json` (`schemas.dumps(VariantRecord)`) |
| `results/raw/<campaign>/<run_id>/run.json` | yes | `RunRecord` (immutable) |
| `results/raw/<campaign>/<run_id>/traces.npz` | no (hash in run.json) | per trace name `<name>__v` float32 mV and `<name>__t` = `[t0_ms, dt_ms, n]` float64 |
| `results/raw/<campaign>/<run_id>/features.json` | yes | `{protocol_id: {feature: FeatureValue-dict}}` (immutable) |
| `results/processed/<campaign>/` | yes | derived CSV/JSON (fingerprints, tolerances, detections, classification, matrices) |
| `results/tables/`, `results/figures/` | yes | paper tables and figures |
| `results/heldout_access.log` | yes | append-only log of every held-out access |

Traces are stored as float32 millivolts on a uniform time grid; **features are always
extracted from the stored representation**, so every derived number reproduces exactly
from raw files. Time grids are verified uniform (relative jitter < 1e-6) before storage.

`run_id` is content addressed: `r-` + first 20 hex of SHA-256 over
`{inputs_sha256, protocol_ids, dt_ms, exec_config, simulator jar_sha256, run_kind, replicate}`
where `inputs_sha256` hashes every file the simulation reads (cell file + transitive
includes + generated probe/harness XML). Identical inputs reuse existing results
(the cache), which is how stimulus-only mutants reuse the reference battery.

## 3. Module contracts

### 3.1 `features/efel_adapter.py`

```python
@dataclass(frozen=True)
class FeatureValue:
    name: str
    value: float | str | None        # str only for categorical features
    state: str                       # "defined" | "undefined" | "not_applicable"
    unit: str
    source: str                      # e.g. "efel:AP_amplitude[first]" or "neurosem:firing_regime"

FeatureTable = dict[str, FeatureValue]

def efel_settings(cfg: dict) -> dict            # validated settings dict (unknown names -> ValueError)
def extract(trace: Trace, protocol: ConcreteProtocol, cfg: dict) -> FeatureTable
def extract_all(traces: dict[str, Trace], protocols: Sequence[ConcreteProtocol], cfg: dict) -> dict[str, FeatureTable]
def feature_table_to_json(ft: FeatureTable) -> dict ; def feature_table_from_json(d: dict) -> FeatureTable
```
Rules: call `efel.reset()` then set every configured setting before each trace; trace dict
`{"T": t_ms, "V": v_mV, "stim_start": [window.start_ms], "stim_end": [window.end_ms]}`;
compute `spike_count` first; a feature with `min_spikes > spike_count` is `not_applicable`;
eFEL `None` is `undefined`; `agg: first|last|scalar` picks element 0, -1, or requires size 1;
`requires: hyperpolarizing` makes the feature `not_applicable` unless the protocol's
summed stimulus amplitude is negative. Only features listed in `protocol.features` are
returned. `rheobase` is filled by the fingerprint layer, not here. `firing_regime` comes
from `features.regimes`. Capture eFEL warnings into `FeatureValue.source` suffix
`"|warn"`? No: record warnings in a returned side channel `extract(..., warnings: list | None)`.

### 3.2 `features/regimes.py`

```python
def firing_regime(trace: Trace, window: AnalysisWindow, ft: FeatureTable, cfg: dict) -> str
```
Labels (first match wins): `silent` (0 spikes), `single_spike` (1), `depolarization_block`,
`bursting` (`burst_count >= bursting_min_bursts`), `adapting` (`adaptation_index > adapting_min_index`),
`tonic`. Must never raise for short/odd traces.

### 3.3 `features/trace_metrics.py`

```python
def uniform_grid(t0_ms: float, dt_ms: float, n: int) -> np.ndarray
def is_uniform(t_ms: np.ndarray, rel_tol: float = 1e-6) -> bool
def resample(trace: Trace, grid_ms: np.ndarray) -> np.ndarray           # linear
def align(a: Trace, b: Trace, dt_ms: float, window: AnalysisWindow | None = None) -> tuple[np.ndarray, np.ndarray, np.ndarray]
def rmse(a: Trace, b: Trace, dt_ms: float, window: AnalysisWindow | None = None) -> float
def max_abs_diff(a: Trace, b: Trace, dt_ms: float, window: AnalysisWindow | None = None) -> float
def spike_times(trace: Trace, threshold_mV: float) -> np.ndarray          # interpolated upward crossings
def decimate(trace: Trace, every_ms: float) -> Trace
def pack_traces(traces: dict[str, Trace]) -> bytes ; def unpack_traces(data: bytes) -> dict[str, Trace]   # npz format of §2
```

### 3.4 `mutations/`

```python
# mutations/base.py
@dataclass(frozen=True)
class Site:                        # one concrete place an operator can act
    operator: str
    file: str                      # relative to workspace root
    locator: str
    params: dict

class MutationOperator(Protocol):
    name: str                      # e.g. "scale_conductance"
    family: MutationFamily
    def sites(self, ws: Workspace) -> list[Site]               # deterministic order
    def apply(self, ws: Workspace, site: Site) -> tuple[list[Edit], dict, dict]   # edits, exec_overrides, model_overrides

REGISTRY: dict[str, MutationOperator]
def generate_mutants(model: ModelRecord, operators: Sequence[str], n_per_operator: int, seed: int,
                     root: Path) -> list[VariantRecord]         # materialize + apply + write variant.json
def xml_changes(before: Path, after: Path) -> list[dict]        # semantic diff of two XML files (ignores whitespace/comments/attr order)
def enforce_single_operator(ref: Workspace, var: Workspace, record: VariantRecord) -> None
    # raises MutationError unless: all changed files/elements are covered by record.edits,
    # all edits lie inside ONE target element (or exec_overrides only), no unrecorded change exists
def load_variant(path: Path) -> tuple[Workspace, VariantRecord]
def write_manifest(records: Sequence[VariantRecord], path: Path) -> None
```
Operators (names are binding):

| family | operator | target | notes |
|---|---|---|---|
| stimulus | `stim_amplitude` | harness network input amplitude | factors from params |
| stimulus | `stim_onset` | harness input delay | shift ms |
| stimulus | `stim_duration` | harness input duration | factor |
| stimulus | `sim_length` | harness Simulation length | factor |
| stimulus | `record_wrong_variable` | harness OutputColumn quantity of the v column | switch to another existing state path |
| biophysical | `scale_conductance` | `channelDensity*/@condDensity` | factors e.g. 0.5, 0.8, 1.25, 2 |
| biophysical | `shift_reversal` | `channelDensity*/@erev` | +-5, +-10 mV |
| biophysical | `scale_capacitance` | `specificCapacitance/@value` | factor |
| biophysical | `scale_gate_time_constant` | core HH gate rates (both forward and reverse `rate` of one gate) or `timeCourse` | factor k on rates = tau/k; skip custom LEMS gates (record as inapplicable) |
| biophysical | `shift_initial_voltage` | `initMembPotential/@value` | +-5 mV |
| biophysical | `wrong_segment_group` | `channelDensity*/@segmentGroup` | to another existing group |
| reference | `wrong_channel` | `channelDensity*/@ionChannel` | another channel id defined in includes |
| reference | `omit_include` | cell file `<include>` | remove one |
| reference | `duplicate_conductance` | duplicate one `channelDensity*` with a new id | |
| reference | `wrong_compatible_component` | `@ionChannel` swapped to a channel of the same ion species | |
| numerical | `increase_dt` | harness `step` x factor AND `exec_overrides.dt_factor` | |
| numerical | `solver_config` | harness `<Meta method>` AND `exec_overrides.integrator_method` | expected no-op for core types (audit) |
| numerical | `reduce_spatial_discretization` | multicompartment only | returns no sites for single-compartment models |
| numerical | `recording_resolution` | `exec_overrides.sample_every_ms` | post-hoc output sampling; no file edit |

### 3.5 `transforms/`

Same `Site`/operator protocol with `family` = transform category and
`kind = VariantKind.VALID_TRANSFORM` (or `NO_CHANGE` for formatting/comments).
Registry names: `unit_conversion` (Decimal-exact, only unit strings permitted by the
NeuroML v2.3.1 XSD pattern for that dimension), `xml_formatting`, `add_comments`,
`numeric_literal_format`, `rename_identifier` (all references across all files, and
`model_overrides["cell_id"]` when the cell is renamed), `factor_file` (move one component
to a new included file), `reorder_independent`, `explicit_default`.
`generate_transforms(model, operators, n_per_operator, seed, root) -> list[VariantRecord]`.
Every transform must pass jnml validation in its unit tests.

### 3.6 `validation/`

```python
# structural.py
@dataclass
class StructuralResult:
    valid: bool | None; jnml: ValidationResult; libneuroml_strict: bool | None; libneuroml_messages: list[str]; files: list[str]
def check(ws: Workspace, sim: Simulator) -> StructuralResult     # cell file, and harness network file if it is NeuroML

# execution.py
@dataclass
class RunOutput:
    record: RunRecord; traces: dict[str, Trace]; status: RunStatus; cached: bool
class RunRecorder:
    def __init__(self, campaign: str, results_root: Path, sim: Simulator): ...
    def run_battery(self, ws, variant: VariantRecord, protocols: Sequence[ConcreteProtocol], exec_cfg: ExecConfig,
                    replicate: int = 0) -> RunOutput          # groups by length, merges traces, one record per group
    def run_canonical(self, ws, variant: VariantRecord, replicate: int = 0) -> RunOutput
    def run_rheobase(self, ws, variant: VariantRecord, exec_cfg: ExecConfig, rcfg: dict) -> tuple[RheobaseResult, list[RunRecord]]
def run_parallel(tasks: Sequence[Callable[[], Any]], workers: int) -> list[Any]   # thread pool; exceptions captured

# canonical.py
def canonical_protocol(ws: Workspace) -> ConcreteProtocol    # window from the harness network's first pulseGenerator; features = CANONICAL_FEATURES

# fingerprint.py
@dataclass
class Fingerprint:
    model_id: str; variant_id: str; dt_ms: float; status: RunStatus
    rheobase: RheobaseResult | None
    tables: dict[str, FeatureTable]           # includes "P00_canonical" and "P03_rheobase"
    run_ids: dict[str, str]                   # protocol_id -> run_id
@dataclass
class Detection:
    protocol_id: str; feature: str; reason: str   # exceeds | definedness | categorical
    ref_value: float | str | None; var_value: float | str | None; diff: float | None; tau: float | None
    ref_run_id: str; var_run_id: str
def build_fingerprint(rec: RunRecorder, ws, variant, protocols, exec_cfg, cfgs) -> Fingerprint
def compare(ref: Fingerprint, var: Fingerprint, tol: "ToleranceTable", multiplier: float = 1.0) -> list[Detection]
def classify(structural: StructuralResult, fp_h: Fingerprint, fp_h2: Fingerprint | None,
             det_h: list[Detection], det_h2: list[Detection] | None) -> MutantClass
    # 1 invalid; 2 BUILD/RUNTIME/TIMEOUT; 3 UNSTABLE; else non-equivalent iff some (protocol, feature)
    # is detected at h AND at h/2; SILENT iff non-equivalent and no canonical detection at h; else EQUIVALENT

# convergence.py
@dataclass
class TolEntry:
    model_id: str; protocol_id: str; feature: str
    f_h: float | None; f_h2: float | None; f_h4: float | None
    abs_floor: float; rel_term: float; refine_term: float; tau: float | None; limiting: str
class ToleranceTable:
    def tau(self, model_id: str, protocol_id: str, feature: str) -> float | None
    def to_csv(self, path: Path) -> None ; @classmethod def from_csv(cls, path: Path) -> "ToleranceTable"
def calibrate(ref_by_dt: dict[float, Fingerprint], model_id: str, tol_cfg: dict) -> list[TolEntry]
def convergence_report(ref_by_dt: dict[float, Fingerprint]) -> list[dict]   # per feature: |f_h - f_h2|, |f_h2 - f_h4|, observed order
```

### 3.7 `selection/`

```python
# matrix.py
@dataclass
class DetectionMatrix:
    mutant_ids: list[str]; protocol_ids: list[str]; detected: np.ndarray    # bool [n_mutants, n_protocols]
    model_of: dict[str, str]; family_of: dict[str, str]; cost: dict[str, float]   # protocol cost in cell-steps
    def rate(self, protocols: Sequence[str], rows: np.ndarray | None = None) -> float
    def to_csv(self, path) / from_csv(cls, path)
# greedy.py
@dataclass
class Selection:
    protocols: list[str]; coverage_curve: list[float]; costs: list[float]; tie_breaks: list[str]
def greedy_max_coverage(m: DetectionMatrix, k: int, candidates: Sequence[str] | None = None) -> Selection
    # deterministic ties: lower cost, then protocol_id
def greedy_cost_sensitive(m: DetectionMatrix, cost_budget: float, candidates=None) -> Selection
def random_count_matched(m, k, draws, seed, candidates=None) -> np.ndarray     # detection rates per draw
def random_runtime_matched(m, cost_budget, draws, seed, candidates=None) -> np.ndarray
# splits.py
class LeakageError(RuntimeError)
@dataclass(frozen=True)
class Split: discovery_models: tuple[str, ...]; heldout_models: tuple[str, ...]; heldout_families: tuple[str, ...]
def verify_split_hashes(root: Path) -> None
def discovery_view(root: Path) -> "DiscoveryView"          # never opens data/splits/heldout/
class DiscoveryView:
    models: tuple[str, ...]; excluded_families: tuple[str, ...]   # read from data/splits/discovery_*.txt only
    def filter_matrix(self, m: DetectionMatrix) -> DetectionMatrix   # raises LeakageError on any non-discovery row
class HeldoutGate:
    def __init__(self, root: Path, frozen_lock: Path, reason: str): ...  # requires configs/FROZEN.lock whose hashes match; logs access
    def split(self) -> Split
```
Leakage test (M7 exit criterion): importing `neurosem.selection.greedy`/`matrix` and running
discovery selection must not open any file under `data/splits/heldout/` (verified by
patching `builtins.open`/`Path.open` in tests) and a static test greps `selection/` for
`heldout` access outside `splits.HeldoutGate`.

### 3.8 `analysis/`

```python
# metrics.py
def paired_counts(a: np.ndarray, b: np.ndarray) -> dict      # both, only_a, only_b, neither
def detection_rate(detected_any: np.ndarray) -> float
def silent_survival_rate(classes: Sequence[MutantClass]) -> float
def false_positive_rate(transform_detected: np.ndarray) -> float
def by_family(...) ; def coverage_curve(...) ; def runtime_per_detection(...)
# bootstrap.py
def cluster_bootstrap_diff(a, b, clusters, n_boot, seed, ci=0.95) -> dict   # resample base models with replacement
def exact_mcnemar(only_a: int, only_b: int) -> float                        # two-sided exact binomial p
def cluster_permutation_test(a, b, clusters, n_perm, seed) -> float         # sign-flip within clusters
# figures.py  -- one function per required figure, each takes processed tables and an output path
fig1_concept, fig2_validation_cascade, fig3_detection_heatmap, fig4_efficiency_curve,
fig5_heldout_generalization, fig6_false_positives, fig7_case_studies, fig8_agent_case_study
```

### 3.9 `experiments/` and `cli.py`

`cli.py` exposes the specification's commands, each a thin wrapper:
`validate-models, run-reference, calibrate-tolerances, generate-mutants, classify-mutants,
build-fingerprints, select-protocols --budget K, evaluate-heldout, evaluate-agent, analyze,
reproduce-paper`, plus `fetch-models`, `pilot`, `smoke`. Every command takes
`--campaign NAME` and `--models ID ...` where relevant, prints what it did, and never
touches held-out data unless it is `evaluate-heldout` (which uses `HeldoutGate`).

`experiments/pilot.py` runs M6 end-to-end on the pilot models and writes
`results/processed/<campaign>/pilot_report.md` evaluating the specification's pilot
success criteria from data (and saying plainly when they are not met).
