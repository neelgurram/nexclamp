# Task: repair a channel reference

`model/NeuroML2/cells/RS/RS.cell.nml` is the Pospischil et al. (2008) regular-spiking (RS)
cortical cell. After a faulty merge, one channel density in this cell refers to the wrong
ion-channel definition. The cell file still passes schema validation, but the shipped
simulation (`model/NeuroML2/cells/RS/LEMS_RS.xml`) no longer works as it did before the merge.
`public_tests/canonical_reference.json` holds the spike times recorded before the merge.

Repair the channel reference in the cell file. Change nothing else.

## Rules for this session

- Work only inside this directory. Do not use the network.
- You may change only this file: `model/NeuroML2/cells/RS/RS.cell.nml`. Do not create, delete
  or edit any other file, except scratch files inside `scratch/`.
- Do not edit `TASK.md`, `EXPORT_MANIFEST.json` or anything in `public_tests/`.
- Public checks: run `python public_tests/run_public_checks.py`. It validates the cell file
  with jNeuroML and runs the shipped simulation. Java and pyNeuroML are installed.
- Nobody will answer questions during this session. Make reasonable decisions yourself and
  stop when you have finished.
