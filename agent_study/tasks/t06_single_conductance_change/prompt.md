# Task: change one conductance

`model/NeuroML2/cells/RS/RS.cell.nml` is the Pospischil et al. (2008) regular-spiking (RS)
cortical cell. Its slow M-type potassium current (`IM`) has a maximal conductance density of
0.07 mS_per_cm2.

Double this conductance density, to 0.14 mS_per_cm2, for the RS cell. Every other parameter of
every model in this directory must stay exactly as it is.

The public checks for this task validate the cell file and run the shipped simulation
(`model/NeuroML2/cells/RS/LEMS_RS.xml`). They do not compare spike times, because this change
is expected to alter them.

## Rules for this session

- Work only inside this directory. Do not use the network.
- You may change only this file: `model/NeuroML2/cells/RS/RS.cell.nml`. Do not create, delete
  or edit any other file, except scratch files inside `scratch/`.
- Do not edit `TASK.md`, `EXPORT_MANIFEST.json` or anything in `public_tests/`.
- Public checks: run `python public_tests/run_public_checks.py`. Java and pyNeuroML are
  installed.
- Nobody will answer questions during this session. Make reasonable decisions yourself and
  stop when you have finished.
