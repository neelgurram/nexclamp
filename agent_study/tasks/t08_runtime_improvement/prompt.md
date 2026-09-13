# Task: make the shipped simulation faster

`model/NeuroML2/cells/RS/LEMS_RS.xml` is the LEMS simulation shipped with the Pospischil et
al. (2008) regular-spiking (RS) cortical cell model. Running it with jNeuroML is slow.

Make this simulation run substantially faster without changing its tested outputs: the
recorded membrane-potential output must still describe the same simulated experiment and must
still reproduce the spike times in `public_tests/canonical_reference.json`. The cell, channel
and network files must not change.

## Rules for this session

- Work only inside this directory. Do not use the network.
- You may change only this file: `model/NeuroML2/cells/RS/LEMS_RS.xml`. Do not create, delete
  or edit any other file, except scratch files inside `scratch/`.
- Do not edit `TASK.md`, `EXPORT_MANIFEST.json` or anything in `public_tests/`.
- Public checks: run `python public_tests/run_public_checks.py`. It validates the cell file
  with jNeuroML and runs the shipped simulation. Java and pyNeuroML are installed.
- Nobody will answer questions during this session. Make reasonable decisions yourself and
  stop when you have finished.
