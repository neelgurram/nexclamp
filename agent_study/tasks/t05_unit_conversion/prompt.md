# Task: convert units

`model/examples/NML2_SingleCompHHCell.nml` is the NeuroML 2 single-compartment
Hodgkin-Huxley example cell. Its channel conductance densities are written in a mixture of
units.

Rewrite every `condDensity` value in this file in `mS_per_cm2`, without changing any physical
value or anything else in the model.

## Rules for this session

- Work only inside this directory. Do not use the network.
- You may change only this file: `model/examples/NML2_SingleCompHHCell.nml`. Do not create,
  delete or edit any other file, except scratch files inside `scratch/`.
- Do not edit `TASK.md`, `EXPORT_MANIFEST.json` or anything in `public_tests/`.
- Public checks: run `python public_tests/run_public_checks.py`. It validates the cell file
  with jNeuroML and runs the shipped simulation
  (`model/LEMSexamples/LEMS_NML2_Ex5_DetCell.xml`). Java and pyNeuroML are installed.
- Nobody will answer questions during this session. Make reasonable decisions yourself and
  stop when you have finished.
