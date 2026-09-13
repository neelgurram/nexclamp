# Task: diagnose a behaviour change

`model/NeuroML2/cells/RS/RS.cell.nml` is the Pospischil et al. (2008) regular-spiking (RS)
cortical cell, simulated by `model/NeuroML2/cells/RS/LEMS_RS.xml`. The model files still pass
schema validation and the simulation runs, but the cell's firing has changed: its spike times
no longer match those recorded earlier (`public_tests/canonical_reference.json`). Exactly one
value in one model file was edited since that recording.

Find the edit that changed the firing. Do not modify any file under `model/`. Write your
answer to `diagnosis.yaml` in this directory, with these fields:

```yaml
file: <path of the edited file, relative to this directory>
element_id: <id attribute of the edited element>
attribute: <name of the edited attribute>
suspected_original_value: <the value you believe it had before the edit>
explanation: <one or two sentences>
```

## Rules for this session

- Work only inside this directory. Do not use the network.
- The only file you may create is `diagnosis.yaml`. Do not create, delete or edit any other
  file, except scratch files inside `scratch/`.
- Do not edit `TASK.md`, `EXPORT_MANIFEST.json` or anything in `public_tests/`.
- Public checks: run `python public_tests/run_public_checks.py`. It validates the cell file
  with jNeuroML and runs the shipped simulation. Java and pyNeuroML are installed.
- Nobody will answer questions during this session. Make reasonable decisions yourself and
  stop when you have finished.
