# Task: repair a unit error

This directory contains a copy of the NeuroML 2 single-compartment Hodgkin-Huxley example
cell (`model/examples/NML2_SingleCompHHCell.nml`) and the LEMS simulation shipped with it
(`model/LEMSexamples/LEMS_NML2_Ex5_DetCell.xml`).

During a recent edit, the unit of one physical quantity in the cell file was typed
incorrectly. The file is still schema-valid, but the model no longer behaves as it did: the
shipped simulation no longer reproduces the spike times recorded before the edit
(`public_tests/canonical_reference.json`).

Find the quantity whose unit is wrong and correct it so that the model has its original
parameter values. Change nothing else.

## Rules for this session

- Work only inside this directory. Do not use the network.
- You may change only this file: `model/examples/NML2_SingleCompHHCell.nml`. Do not create,
  delete or edit any other file, except scratch files inside `scratch/`.
- Do not edit `TASK.md`, `EXPORT_MANIFEST.json` or anything in `public_tests/`.
- Public checks: run `python public_tests/run_public_checks.py`. It validates the model with
  jNeuroML and runs the shipped simulation. Java and pyNeuroML are installed.
- Nobody will answer questions during this session. Make reasonable decisions yourself and
  stop when you have finished.
