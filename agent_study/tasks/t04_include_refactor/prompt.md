# Task: refactor included files

`model/examples/NML2_SingleCompHHCell.nml` defines three ion channels (`passiveChan`,
`naChan` and `kChan`) inline, together with the Hodgkin-Huxley cell that uses them. The
simulation shipped with it is `model/LEMSexamples/LEMS_NML2_Ex5_DetCell.xml`.

Refactor the model so that each ion channel is defined in its own NeuroML file named
`model/examples/channels/<channel id>.channel.nml` (for example
`model/examples/channels/naChan.channel.nml`) and is included from
`model/examples/NML2_SingleCompHHCell.nml`, which must no longer define any ion channel
itself. The model's behaviour must not change.

## Rules for this session

- Work only inside this directory. Do not use the network.
- You may change or create files only under `model/examples/**`, and you may change
  `model/LEMSexamples/LEMS_NML2_Ex5_DetCell.xml`. Do not create, delete or edit any other file,
  except scratch files inside `scratch/`.
- Do not edit `TASK.md`, `EXPORT_MANIFEST.json` or anything in `public_tests/`.
- Public checks: run `python public_tests/run_public_checks.py`. It validates the cell file
  with jNeuroML and runs the shipped simulation. Java and pyNeuroML are installed.
- Nobody will answer questions during this session. Make reasonable decisions yourself and
  stop when you have finished.
