"""Leakage barriers between discovery selection and held-out data (Milestone 7 exit criterion).

All held-out files used here are synthetic fixtures in ``tmp_path``; the repository's own
held-out directory is never read.
"""

from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
import textwrap
from pathlib import Path

import numpy as np
import pytest

import neuraxis.selection
import neuraxis.selection.splits as splits_module
from neuraxis.config import study
from neuraxis.provenance import sha256_file
from neuraxis.schemas import dumps
from neuraxis.selection.greedy import (
    greedy_cost_sensitive,
    greedy_max_coverage,
    random_count_matched,
    random_runtime_matched,
    selection_settings,
)
from neuraxis.selection.matrix import DetectionMatrix
from neuraxis.selection.splits import (
    ACCESS_LOG_FILE,
    DISCOVERY_FAMILIES_FILE,
    DISCOVERY_FILES,
    DISCOVERY_MODELS_FILE,
    FROZEN_LOCK_FILE,
    HELDOUT_DIR,
    HELDOUT_FAMILIES_FILE,
    HELDOUT_MODELS_FILE,
    SPLITS_HASH_FILE,
    DiscoveryView,
    FrozenSplitError,
    HeldoutGate,
    LeakageError,
    SplitIntegrityError,
    discovery_view,
    format_hash_manifest,
    freeze_splits,
    parse_hash_manifest,
    read_access_log,
    read_id_list,
    verify_split_hashes,
)

MANIFEST = ("model_id,source_family,inclusion\n"
            "disc_a,src_a,include\ndisc_b,src_b,include\nheld_c,src_c,include\nheld_d,src_a,include\n")
CONFIGS = ("configs/study.yaml", "configs/tolerances.yaml")


def make_root(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    files = {
        "data/model_manifest.csv": MANIFEST,
        DISCOVERY_MODELS_FILE: "disc_a\ndisc_b\n",
        DISCOVERY_FAMILIES_FILE: "biophysical\nreference\n",
        HELDOUT_MODELS_FILE: "held_c\nheld_d\n",
        HELDOUT_FAMILIES_FILE: "numerical\n",
        "configs/study.yaml": "status: synthetic-test\n",
        "configs/tolerances.yaml": "abs_floor: {}\n",
    }
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(text.encode("utf-8"))
    return root


def write_lock(root: Path) -> Path:
    lock = root / FROZEN_LOCK_FILE
    lock.write_bytes(format_hash_manifest(root, [SPLITS_HASH_FILE, *CONFIGS]).encode("utf-8"))
    return lock


def synthetic_matrix(models=("disc_a", "disc_b"), families=("biophysical", "reference"), n=40, p=8,
                     seed=0) -> DetectionMatrix:
    rng = np.random.default_rng(seed)
    ids = [f"mut{i:03d}" for i in range(n)]
    pids = [f"P{j + 1:02d}_synthetic" for j in range(p)]
    return DetectionMatrix(ids, pids, rng.random((n, p)) < 0.25,
                           {m: models[i % len(models)] for i, m in enumerate(ids)},
                           {m: families[i % len(families)] for i, m in enumerate(ids)},
                           {q: float(rng.integers(1, 6) * 20000) for q in pids})


# One guard implementation, used in-process (via monkeypatch) and in a fresh interpreter.
GUARD_SRC = textwrap.dedent('''
    import builtins, io, os, pathlib

    class HeldoutReadBlocked(RuntimeError):
        pass

    def install(heldout_dir, attempts, set_attr):
        base = os.path.normcase(os.path.abspath(os.fspath(heldout_dir)))

        def blocked(p):
            if p is None or isinstance(p, int):
                return False
            try:
                s = os.fspath(p)
            except TypeError:
                return False
            if isinstance(s, bytes):
                s = os.fsdecode(s)
            a = os.path.normcase(os.path.abspath(s))
            if a == base or a.startswith(base + os.sep):
                attempts.append(a)
                return True
            return False

        real = dict(open=builtins.open, listdir=os.listdir, scandir=os.scandir, stat=os.stat,
                    path_open=pathlib.Path.open, read_text=pathlib.Path.read_text,
                    read_bytes=pathlib.Path.read_bytes)

        def g_open(file, *a, **k):
            if blocked(file):
                raise HeldoutReadBlocked(f"open {file}")
            return real["open"](file, *a, **k)

        def g_listdir(path=None):
            if blocked(path):
                raise HeldoutReadBlocked(f"listdir {path}")
            return real["listdir"]() if path is None else real["listdir"](path)

        def g_scandir(path="."):
            if blocked(path):
                raise HeldoutReadBlocked(f"scandir {path}")
            return real["scandir"](path)

        def g_stat(path, *a, **k):
            if blocked(path):
                raise HeldoutReadBlocked(f"stat {path}")
            return real["stat"](path, *a, **k)

        def g_path_open(self, *a, **k):
            if blocked(self):
                raise HeldoutReadBlocked(f"Path.open {self}")
            return real["path_open"](self, *a, **k)

        def g_read_text(self, *a, **k):
            if blocked(self):
                raise HeldoutReadBlocked(f"Path.read_text {self}")
            return real["read_text"](self, *a, **k)

        def g_read_bytes(self):
            if blocked(self):
                raise HeldoutReadBlocked(f"Path.read_bytes {self}")
            return real["read_bytes"](self)

        set_attr(builtins, "open", g_open)
        set_attr(io, "open", g_open)
        set_attr(os, "listdir", g_listdir)
        set_attr(os, "scandir", g_scandir)
        set_attr(os, "stat", g_stat)
        set_attr(pathlib.Path, "open", g_path_open)
        set_attr(pathlib.Path, "read_text", g_read_text)
        set_attr(pathlib.Path, "read_bytes", g_read_bytes)
''')


@pytest.fixture
def heldout_guard(monkeypatch):
    ns: dict = {}
    exec(GUARD_SRC, ns)  # noqa: S102 -- test-local source, shared verbatim with the fresh-interpreter test

    def install(heldout_dir: Path) -> tuple[list[str], type]:
        attempts: list[str] = []
        ns["install"](heldout_dir, attempts, monkeypatch.setattr)
        return attempts, ns["HeldoutReadBlocked"]

    return install


# ---------------------------------------------------------------------- (1) dynamic leakage test
def test_discovery_selection_end_to_end_never_touches_heldout(tmp_path, heldout_guard):
    root = make_root(tmp_path)
    freeze_splits(root)
    lock = write_lock(root)
    matrix_csv = root / "results" / "processed" / "synthetic" / "detection_matrix.csv"
    synthetic_matrix().to_csv(matrix_csv)

    attempts, blocked_error = heldout_guard(root / HELDOUT_DIR)
    # the guard is live: every route to the held-out files is refused and recorded
    with pytest.raises(blocked_error), open(root / HELDOUT_MODELS_FILE, encoding="utf-8"):
        pass
    with pytest.raises(blocked_error):
        (root / HELDOUT_FAMILIES_FILE).read_text(encoding="utf-8")
    with pytest.raises(blocked_error):
        HeldoutGate(root, lock, "negative control: the gate must hit the guard")
    assert attempts
    attempts.clear()

    view = discovery_view(root, require_frozen=True)
    settings = selection_settings(study())
    m = view.filter_matrix(DetectionMatrix.from_csv(matrix_csv))
    sel = greedy_max_coverage(m, settings.budget_k)
    cost_sel = greedy_cost_sensitive(m, sel.costs[-1])
    count_rates = random_count_matched(m, len(sel.protocols), 500, settings.seed)
    runtime_rates = random_runtime_matched(m, sel.costs[-1], 500, settings.seed)
    out = matrix_csv.parent / "selection.json"
    out.write_text(dumps({"greedy": sel, "cost_sensitive": cost_sel,
                          "random_count_mean": float(count_rates.mean()),
                          "random_runtime_mean": float(runtime_rates.mean())}), encoding="utf-8")

    assert attempts == []
    assert view.frozen and view.models == ("disc_a", "disc_b")
    assert 1 <= len(sel.protocols) <= settings.budget_k
    assert json.loads(out.read_text(encoding="utf-8"))["greedy"]["protocols"] == sel.protocols
    assert count_rates.shape == runtime_rates.shape == (500,)


def test_import_and_discovery_selection_in_fresh_interpreter(tmp_path, repo_root):
    """Import-time behaviour too: the guard is installed before neuraxis.selection is imported."""
    root = make_root(tmp_path)
    freeze_splits(root)
    matrix_csv = root / "matrix.csv"
    synthetic_matrix(seed=4).to_csv(matrix_csv)
    script = GUARD_SRC + textwrap.dedent(f'''
        import sys
        attempts = []
        install({str(root / HELDOUT_DIR)!r}, attempts, setattr)
        assert not any(k.startswith("neurosem") for k in sys.modules)
        import neuraxis.selection.matrix, neuraxis.selection.greedy
        from neuraxis.selection import (DetectionMatrix, discovery_view, greedy_max_coverage,
                                        random_count_matched, random_runtime_matched)
        view = discovery_view(pathlib.Path({str(root)!r}), require_frozen=True)
        m = view.filter_matrix(DetectionMatrix.from_csv({str(matrix_csv)!r}))
        sel = greedy_max_coverage(m, 3)
        random_count_matched(m, 3, 200, 1)
        random_runtime_matched(m, sel.costs[-1], 200, 1)
        print("ATTEMPTS", len(attempts))
        print("SELECTED", ",".join(sel.protocols))
        try:
            open({str(root / HELDOUT_MODELS_FILE)!r}, encoding="utf-8")
        except HeldoutReadBlocked:
            print("CONTROL_BLOCKED", len(attempts))
    ''')
    proc = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, timeout=180,
                          cwd=repo_root, check=False)
    assert proc.returncode == 0, proc.stderr
    assert "ATTEMPTS 0" in proc.stdout
    assert "SELECTED P" in proc.stdout
    assert "CONTROL_BLOCKED 1" in proc.stdout          # the guard was live in that interpreter


# ---------------------------------------------------------------------- (2) static tests
SELECTION_DIR = Path(neuraxis.selection.__file__).parent
# Every spelling in use: the directory name, identifiers, and the specification's prose.
HELDOUT_WORD = re.compile(r"held[-_ ]?out", re.IGNORECASE)


@pytest.mark.parametrize("text", ["heldout", "HeldOut", "held_out", "held-out", "Held out", "HELDOUT_DIR"])
def test_heldout_pattern_catches_every_spelling(text):
    assert HELDOUT_WORD.search(f"x = '{text}'")


def test_no_selection_module_except_splits_mentions_heldout():
    """Full text, docstrings and comments included: the strictest reading of the barrier."""
    modules = sorted(SELECTION_DIR.rglob("*.py"))
    assert {"matrix.py", "greedy.py", "splits.py", "__init__.py"} <= {p.name for p in modules}
    offenders = [p.relative_to(SELECTION_DIR).as_posix() for p in modules
                 if p.name != "splits.py" and HELDOUT_WORD.search(p.read_text(encoding="utf-8"))]
    assert offenders == []


def _docstring_nodes(tree: ast.AST) -> set[int]:
    """ids of docstring constants; prose explaining the barrier is not access to held-out data."""
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) \
                    and isinstance(first.value.value, str):
                out.add(id(first.value))
    return out


def _tainted_definitions(source: str) -> set[str]:
    """Top-level definitions of a module that reference 'heldout' in code (not docstrings)
    or use a definition that does."""
    tree = ast.parse(source)
    docstrings = _docstring_nodes(tree)
    defs: dict[str, ast.AST] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defs[node.name] = node
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    defs[t.id] = node
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            defs[node.target.id] = node

    def mentions(node: ast.AST) -> bool:
        for n in ast.walk(node):
            if id(n) in docstrings:
                continue
            text = (n.value if isinstance(n, ast.Constant) and isinstance(n.value, str) else
                    n.id if isinstance(n, ast.Name) else n.attr if isinstance(n, ast.Attribute) else
                    n.arg if isinstance(n, ast.arg) else
                    n.name if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) else "")
            if HELDOUT_WORD.search(text):
                return True
        return False

    tainted = {name for name, node in defs.items() if mentions(node)}
    changed = True
    while changed:
        changed = False
        for name, node in defs.items():
            if name not in tainted and {n.id for n in ast.walk(node) if isinstance(n, ast.Name)} & tainted:
                tainted.add(name)
                changed = True
    return tainted


def test_heldout_access_in_splits_is_confined_to_gate_and_freeze():
    tainted = _tainted_definitions((SELECTION_DIR / "splits.py").read_text(encoding="utf-8"))
    allowed = {"HELDOUT_DIR", "HELDOUT_MODELS_FILE", "HELDOUT_FAMILIES_FILE", "REQUIRED_SPLIT_FILES",
               "ACCESS_LOG_FILE", "Split", "_read_split", "_require_frozen_split_files", "_append_log",
               "read_access_log", "HeldoutGate", "_manifest_checks", "freeze_splits"}
    assert "HeldoutGate" in tainted and "freeze_splits" in tainted       # the analysis is not vacuous
    assert tainted <= allowed, sorted(tainted - allowed)
    assert not tainted & {"discovery_view", "DiscoveryView", "verify_split_hashes", "read_id_list",
                          "parse_hash_manifest", "format_hash_manifest", "LeakageError"}


@pytest.mark.parametrize("planted", ['"data/splits/held-out/x.txt"', '"data/splits/heldout/x.txt"',
                                     "HELDOUT_MODELS_FILE"])
def test_confinement_analysis_catches_planted_references(planted):
    source = (SELECTION_DIR / "splits.py").read_text(encoding="utf-8")
    source = source.replace("def discovery_view(root: Path, require_frozen: bool = False) -> DiscoveryView:\n",
                            "def discovery_view(root: Path, require_frozen: bool = False) -> DiscoveryView:\n"
                            f"    _planted = {planted}\n", 1)
    assert "_planted" in source
    assert "discovery_view" in _tainted_definitions(source)


def test_confinement_analysis_ignores_docstrings_only():
    source = 'def f():\n    """Never reads held-out data."""\n    return 1\n'
    assert _tainted_definitions(source) == set()
    assert _tainted_definitions('def f():\n    return "held-out"\n') == {"f"}


# ---------------------------------------------------------------------- (3) filter_matrix
def test_filter_matrix_accepts_discovery_rows_and_returns_a_copy(tmp_path):
    root = make_root(tmp_path)
    view = discovery_view(root)
    assert not view.frozen
    assert view.families == ("biophysical", "reference")
    assert view.excluded_families == ("stimulus", "numerical", "kinetics")
    m = synthetic_matrix()
    out = view.filter_matrix(m)
    assert out == m and out is not m
    out.detected[0, 0] = not out.detected[0, 0]
    assert out.detected[0, 0] != m.detected[0, 0]


@pytest.mark.parametrize("model, family", [("held_c", "biophysical"), ("disc_a", "numerical"),
                                           ("unknown_model", "reference"), ("disc_b", "stimulus")])
def test_filter_matrix_raises_on_any_non_discovery_row(tmp_path, model, family):
    view = discovery_view(make_root(tmp_path))
    m = synthetic_matrix()
    model_of, family_of = dict(m.model_of), dict(m.family_of)
    model_of[m.mutant_ids[7]], family_of[m.mutant_ids[7]] = model, family
    bad = DetectionMatrix(m.mutant_ids, m.protocol_ids, m.detected, model_of, family_of, m.cost)
    with pytest.raises(LeakageError, match="1 of 40"):
        view.filter_matrix(bad)
    assert view.discovery_mask(bad).sum() == 39


def test_discovery_view_built_from_contract_fields_is_usable():
    """ARCHITECTURE.md constructs DiscoveryView(models, excluded_families); families are then derived."""
    view = DiscoveryView(("disc_a", "disc_b"), ("stimulus", "numerical", "kinetics"))
    assert view.families == ("biophysical", "reference")
    m = synthetic_matrix()
    assert view.filter_matrix(m) == m
    with pytest.raises(LeakageError):
        DiscoveryView(("disc_a",), ("biophysical", "stimulus", "numerical")).filter_matrix(m)
    with pytest.raises(ValueError):
        DiscoveryView(("disc_a",), ("not_a_family",))
    with pytest.raises(ValueError):
        DiscoveryView(("disc_a",), ("stimulus",), ("stimulus", "reference"))


def test_split_id_lists_reject_a_byte_order_mark(tmp_path):
    root = make_root(tmp_path)
    (root / DISCOVERY_MODELS_FILE).write_bytes("\ufeffdisc_a\ndisc_b\n".encode("utf-8"))
    with pytest.raises(ValueError, match="byte-order mark"):
        read_id_list(root / DISCOVERY_MODELS_FILE)
    with pytest.raises(ValueError, match="byte-order mark"):
        discovery_view(root)
    with pytest.raises(ValueError, match="byte-order mark"):
        freeze_splits(root)


def test_discovery_view_verifies_frozen_discovery_files_only(tmp_path):
    root = make_root(tmp_path)
    with pytest.raises(SplitIntegrityError):
        discovery_view(root, require_frozen=True)
    freeze_splits(root)
    assert discovery_view(root, require_frozen=True).frozen
    # a change to a held-out file is caught by the full check, not by the discovery view
    (root / HELDOUT_FAMILIES_FILE).write_bytes(b"numerical\nstimulus\n")
    discovery_view(root, require_frozen=True)
    with pytest.raises(SplitIntegrityError, match="changed since freeze"):
        verify_split_hashes(root)
    (root / DISCOVERY_MODELS_FILE).write_bytes(b"disc_a\n")
    with pytest.raises(SplitIntegrityError, match="discovery_models"):
        discovery_view(root)


# ---------------------------------------------------------------------- (4) HeldoutGate
def test_heldout_gate_refuses_without_a_matching_lock(tmp_path):
    root = make_root(tmp_path)
    freeze_splits(root)
    log_before = (root / ACCESS_LOG_FILE).read_bytes()
    lock = root / FROZEN_LOCK_FILE
    with pytest.raises(SplitIntegrityError, match="not found"):
        HeldoutGate(root, lock, "evaluate")
    lock.write_bytes(format_hash_manifest(root, [SPLITS_HASH_FILE]).encode())        # configs not recorded
    with pytest.raises(SplitIntegrityError, match="does not record"):
        HeldoutGate(root, lock, "evaluate")
    write_lock(root)
    with pytest.raises(LeakageError):
        HeldoutGate(root, lock, "   ")
    (root / "configs/tolerances.yaml").write_bytes(b"abs_floor: {spike_count: 1}\n")  # edited after lock
    with pytest.raises(SplitIntegrityError, match="changed since freeze"):
        HeldoutGate(root, lock, "evaluate")
    write_lock(root)
    (root / "configs/features.yaml").write_bytes(b"new: config\n")                     # unlocked new config
    with pytest.raises(SplitIntegrityError, match="features.yaml"):
        HeldoutGate(root, FROZEN_LOCK_FILE, "evaluate")
    (root / "configs/features.yaml").unlink()
    (root / HELDOUT_MODELS_FILE).write_bytes(b"held_c\n")                              # split edited after freeze
    with pytest.raises(SplitIntegrityError):
        HeldoutGate(root, lock, "evaluate")
    assert (root / ACCESS_LOG_FILE).read_bytes() == log_before                       # refusals open nothing


def test_heldout_gate_refuses_an_adhoc_lock_outside_configs(tmp_path):
    """A lock with matching hashes written anywhere but <root>/configs/FROZEN.lock must not open the gate."""
    root = make_root(tmp_path)
    freeze_splits(root)
    log_before = (root / ACCESS_LOG_FILE).read_bytes()
    text = format_hash_manifest(root, [SPLITS_HASH_FILE, *CONFIGS]).encode("utf-8")
    for adhoc in (tmp_path / "my_adhoc.lock", root / "configs" / "OTHER.lock", root / "FROZEN.lock"):
        adhoc.write_bytes(text)
        with pytest.raises(SplitIntegrityError, match="refusing lock file"):
            HeldoutGate(root, adhoc, "peek")
    assert not (root / FROZEN_LOCK_FILE).exists()
    # an equivalent spelling of the real lock path is accepted once the lock exists
    write_lock(root)
    HeldoutGate(root, root / "configs" / ".." / FROZEN_LOCK_FILE, "evaluate")
    assert (root / ACCESS_LOG_FILE).read_bytes() != log_before
    assert read_access_log(root)[-1]["frozen_lock"] == FROZEN_LOCK_FILE


def test_heldout_gate_requires_the_study_config_in_the_lock(tmp_path):
    """With configs/ empty, a lock recording only SPLITS.sha256 must not open the gate."""
    root = make_root(tmp_path)
    freeze_splits(root)
    for rel in CONFIGS:
        (root / rel).unlink()
    lock = root / FROZEN_LOCK_FILE
    lock.write_bytes(format_hash_manifest(root, [SPLITS_HASH_FILE]).encode("utf-8"))
    with pytest.raises(SplitIntegrityError, match="study.yaml"):
        HeldoutGate(root, lock, "evaluate")
    # recording a study.yaml that does not exist does not help either
    lock.write_bytes(format_hash_manifest(root, [SPLITS_HASH_FILE]).encode("utf-8")
                     + f"{'0' * 64}  configs/study.yaml\n".encode())
    with pytest.raises(SplitIntegrityError, match="missing: configs/study.yaml"):
        HeldoutGate(root, lock, "evaluate")
    assert [r["event"] for r in read_access_log(root)] == ["splits_frozen"]


def test_heldout_gate_opens_with_matching_lock_and_logs_each_access(tmp_path, monkeypatch):
    root = make_root(tmp_path)
    freeze_splits(root)
    lock = write_lock(root)
    fake_commit = "0123456789abcdef0123456789abcdef01234567"
    git_calls: list[Path] = []

    def fake_git_state(repo):
        git_calls.append(Path(repo))
        return fake_commit, False

    monkeypatch.setattr(splits_module, "git_state", fake_git_state)
    gate = HeldoutGate(root, FROZEN_LOCK_FILE, "final held-out evaluation")
    split = gate.split()
    assert split.discovery_models == ("disc_a", "disc_b")
    assert split.heldout_models == ("held_c", "held_d")
    assert split.heldout_families == ("numerical",)
    log = root / ACCESS_LOG_FILE
    first = log.read_bytes()
    records = [r for r in read_access_log(root) if r["event"] == "heldout_gate_opened"]
    assert len(records) == 1
    rec = records[0]
    assert rec["reason"] == "final held-out evaluation"
    assert rec["timestamp_utc"]
    assert rec["git_commit"] == fake_commit and rec["git_dirty"] is False      # logged verbatim
    assert git_calls == [root]                                                 # commit of the repository root
    assert rec["frozen_lock_sha256"] == sha256_file(lock)
    assert rec["splits_sha256"] == sha256_file(root / SPLITS_HASH_FILE)
    HeldoutGate(root, lock, "robustness re-analysis")
    second = log.read_bytes()
    assert second.startswith(first) and second.count(b"\n") == first.count(b"\n") + 1
    # the gate re-verifies before reading
    (root / DISCOVERY_FAMILIES_FILE).write_bytes(b"biophysical\n")
    with pytest.raises(SplitIntegrityError):
        gate.split()


# ---------------------------------------------------------------------- freezing
def test_freeze_writes_hashes_and_refuses_silent_overwrite(tmp_path):
    root = make_root(tmp_path)
    res = freeze_splits(root)
    assert res.status == "frozen"
    entries = parse_hash_manifest((root / SPLITS_HASH_FILE).read_text(encoding="utf-8"))
    assert set(entries) == {DISCOVERY_MODELS_FILE, DISCOVERY_FAMILIES_FILE, HELDOUT_MODELS_FILE,
                            HELDOUT_FAMILIES_FILE}
    assert all(sha256_file(root / rel) == h for rel, h in entries.items())
    assert any("held_d" in w and "src_a" in w for w in res.warnings)      # correlated source family
    assert [r["event"] for r in read_access_log(root)] == ["splits_frozen"]

    assert freeze_splits(root).status == "unchanged"
    assert len(read_access_log(root)) == 1

    (root / DISCOVERY_MODELS_FILE).write_bytes(b"disc_a\ndisc_b\ndisc_c\n")
    manifest_before = (root / SPLITS_HASH_FILE).read_bytes()
    with pytest.raises(ValueError):                                     # disc_c is not in the manifest
        freeze_splits(root, force_reason="add model")
    (root / DISCOVERY_MODELS_FILE).write_bytes(b"disc_b\ndisc_a\n")
    with pytest.raises(FrozenSplitError):
        freeze_splits(root)
    with pytest.raises(FrozenSplitError):
        freeze_splits(root, force_reason="  ")
    assert (root / SPLITS_HASH_FILE).read_bytes() == manifest_before

    res = freeze_splits(root, force_reason="reordered discovery list")
    assert res.status == "refrozen"
    last = read_access_log(root)[-1]
    assert last["event"] == "splits_refrozen" and last["reason"] == "reordered discovery list"
    assert last["previous_splits_sha256"] and last["previous_splits_sha256"] != last["splits_sha256"]


@pytest.mark.parametrize("rel, content, error", [
    (HELDOUT_MODELS_FILE, b"held_c\ndisc_a\n", LeakageError),           # overlapping models
    (HELDOUT_FAMILIES_FILE, b"reference\n", LeakageError),              # overlapping families
    (HELDOUT_FAMILIES_FILE, b"not_a_family\n", ValueError),
    (HELDOUT_FAMILIES_FILE, b"\n", ValueError),                         # empty list
    (DISCOVERY_MODELS_FILE, b"disc_a\ndisc_a\n", ValueError),           # duplicate id
])
def test_freeze_rejects_invalid_splits(tmp_path, rel, content, error):
    root = make_root(tmp_path)
    (root / rel).write_bytes(content)
    with pytest.raises(error):
        freeze_splits(root)
    assert not (root / SPLITS_HASH_FILE).exists()


def test_freeze_requires_all_split_files(tmp_path):
    root = make_root(tmp_path)
    (root / HELDOUT_MODELS_FILE).unlink()
    with pytest.raises(FileNotFoundError):
        freeze_splits(root)


def test_freeze_script_cli(tmp_path, repo_root):
    root = make_root(tmp_path)
    script = [sys.executable, str(repo_root / "scripts" / "freeze_splits.py"), "--root", str(root)]
    first = subprocess.run(script, capture_output=True, text=True, timeout=120, check=False)
    assert first.returncode == 0, first.stderr
    assert first.stdout.startswith("frozen:") and "WARNING" in first.stdout
    (root / DISCOVERY_FAMILIES_FILE).write_bytes(b"biophysical\n")
    refused = subprocess.run(script, capture_output=True, text=True, timeout=120, check=False)
    assert refused.returncode == 2 and "REFUSED" in refused.stderr
    forced = subprocess.run([*script, "--force-with-reason", "drop reference family"], capture_output=True,
                            text=True, timeout=120, check=False)
    assert forced.returncode == 0, forced.stderr
    assert read_access_log(root)[-1]["reason"] == "drop reference family"
    (root / HELDOUT_FAMILIES_FILE).write_bytes(b"biophysical\n")
    invalid = subprocess.run([*script, "--force-with-reason", "x"], capture_output=True, text=True, timeout=120,
                             check=False)
    assert invalid.returncode == 1 and "INVALID SPLIT" in invalid.stderr


# ---------------------------------------------------------------------- repository split files
def test_repository_discovery_split_is_the_provisional_pilot(repo_root, models):
    view = discovery_view(repo_root)
    assert view.models == ("pospischil2008_rs", "pospischil2008_lts")
    assert view.families == ("biophysical", "reference", "numerical")
    assert view.excluded_families == ("stimulus", "kinetics")
    for mid in view.models:
        assert models[mid].inclusion == "include"
    for rel in DISCOVERY_FILES:
        data = (repo_root / rel).read_bytes()
        assert b"\r" not in data and not data.startswith(b"\xef\xbb\xbf") and data.endswith(b"\n")
