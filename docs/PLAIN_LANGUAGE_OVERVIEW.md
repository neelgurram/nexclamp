# Neuraxis in plain language

*Working name Neuraxis (provisional; see `docs/NAME_AUDIT.md`).*

## What it is

- **A computer model of a neuron is a set of equations.** They describe the membrane voltage, the ion
  channels, their conductances and the membrane capacitance.
- **A simulator runs those equations.** It injects a virtual current into the model cell and computes
  how the voltage changes over time. Large voltage peaks are action potentials ("spikes").
- **Model files get edited all the time.** People and software change them, for example when
  converting units, renaming things or tidying files.
- **An edited file can still look fine.** It can pass the format checker, run without crashing, and
  give the familiar answer on the one standard test, while behaving differently under another input.
  - Example: both versions fire five spikes on the standard test, but only the original fires a
    rebound spike after a brief hyperpolarising input.

## The question

How much protection does a model's own standard test really give when the model is edited, and when do extra tests add information the standard test cannot? Either answer is useful.

*Internal study identifier: `neuron_model_behavioral_validation` (independent of the provisional name).*

## What Neuraxis does

1. **Tests many conditions.** It runs each model under several current-injection protocols, not just
   one.
2. **Measures each response.** It extracts interpretable measurements: spike count, first-spike
   latency, firing frequency, spike height and width, adaptation, sag, rebound.
3. **Builds a fingerprint.** All the measurements across all protocols form the model's
   **perturbation fingerprint**.
4. **Calibrates against controlled faults.** It makes small, controlled faults in models ("mutants")
   and harmless edits ("valid transformations"). It then checks which tests notice the faults and
   whether any test falsely flags the harmless edits.
5. **Picks a small battery.** It chooses a small set of protocols that catches many real behaviour
   changes without running every possible simulation.
6. **Checks on unseen material.** That small set is then tested on models, and on a kind of fault,
   that were not used to choose it.

## What it is not

- **It does not prove two models are equivalent.** Passing the tests means only "no difference
  found in the tested conditions".
- **It builds on existing tools.** It does not claim to have invented NeuroML, LEMS, pyNeuroML,
  jNeuroML, SciUnit/NeuronUnit, eFEL, regression testing, mutation testing, metamorphic testing or
  greedy coverage selection.
- **It is not a benchmark of AI coding assistants.** An AI assistant may be studied later as one
  secondary source of model edits.

## How the study is kept honest

- **Development data.** Practice runs (pilots) are used to build and tune the method. Their results
  are labelled exploratory.
- **The final test.** Before it runs, the method, thresholds, models and analysis are frozen and
  publicly preregistered (AsPredicted). The final test uses models and a fault family that the
  method never used for its choices.
- **Integrity.** Raw results are never overwritten. Every run records exactly what was run, with
  which software, and when.
- **What we know so far.** On the first practice run, the standard test caught every real model
  change. Whether hidden changes exist is an open question, and a negative answer would be reported
  too.
