# Task: rename a channel

`model/` contains the Pospischil et al. (2008) cortical cell models (the RS, FS, LTS and IB
cells in `model/NeuroML2/cells/`) and their shared ion-channel definitions in
`model/NeuroML2/channels/`. Each cell directory also contains the LEMS simulation shipped with
that cell.

The delayed-rectifier potassium channel currently has the NeuroML id `Kd`. Rename this channel
to `Kdr` everywhere in the model repository. All models and their shipped simulations must
keep working exactly as before.

## Rules for this session

- Work only inside this directory. Do not use the network.
- You may change, create or delete files only under `model/NeuroML2/**`. Do not create, delete
  or edit any other file, except scratch files inside `scratch/`.
- Do not edit `TASK.md`, `EXPORT_MANIFEST.json` or anything in `public_tests/`.
- Public checks: run `python public_tests/run_public_checks.py`. It validates the four cell
  files with jNeuroML and runs the shipped RS simulation
  (`model/NeuroML2/cells/RS/LEMS_RS.xml`). Java and pyNeuroML are installed.
- Nobody will answer questions during this session. Make reasonable decisions yourself and
  stop when you have finished.
