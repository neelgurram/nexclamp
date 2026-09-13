# Task: restore the stimulus protocol

`model/` contains the Pospischil et al. (2008) regular-spiking (RS) cortical cell model and
the simulation shipped with it: `model/NeuroML2/cells/RS/LEMS_RS.xml`, which simulates the
network defined in `model/NeuroML2/cells/RS/RS.net.nml`.

The shipped simulation is documented as follows: a 1000 ms simulation of one RS cell that
receives a single current step of 0.75 nA starting at 300 ms and lasting 400 ms. Somebody
changed the stimulus protocol. The simulation no longer matches this description or the spike
times recorded before the change (`public_tests/canonical_reference.json`).

Restore the stimulus protocol so that it matches the documentation. Do not change the cell or
channel models.

## Rules for this session

- Work only inside this directory. Do not use the network.
- You may change only these files: `model/NeuroML2/cells/RS/RS.net.nml` and
  `model/NeuroML2/cells/RS/LEMS_RS.xml`. Do not create, delete or edit any other file, except
  scratch files inside `scratch/`.
- Do not edit `TASK.md`, `EXPORT_MANIFEST.json` or anything in `public_tests/`.
- Public checks: run `python public_tests/run_public_checks.py`. It validates the model with
  jNeuroML and runs the shipped simulation. Java and pyNeuroML are installed.
- Nobody will answer questions during this session. Make reasonable decisions yourself and
  stop when you have finished.
