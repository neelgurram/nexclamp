# Development note: time-step sensitivity of jLEMS on the Pospischil fixtures

*Date: 2026-09-13. Type: development probe on discovery/pilot models (allowed by the
specification to guide development). This is not a study result.*

## What was run

The shipped harness of each cell (`LEMS_<cell>.xml`: 400 ms step, 1000 ms simulated) was
run with jNeuroML 0.14.0 / jLEMS 0.12.0 on Temurin 21.0.12.1 (Windows 11). Only the
`step` attribute was changed. Spike times are upward crossings of 0 mV, linearly
interpolated. Script: `scratchpad/dtprobe/probe.py` (reproduced by
`neurosem calibrate-tolerances` in the pipeline).

## Observations

| cell | dt (ms) | wall time (s) | spikes | spike times (ms) |
|---|---|---|---|---|
| RS | 0.05 | 1.4 | 5 | 321.18, 354.02, 401.50, 491.47, 646.10 |
| RS | 0.025 | 1.7 | 5 | 320.89, 351.32, 394.61, 472.81, 618.16 |
| RS | 0.01 | 2.8 | 5 | 320.68, 349.64, 390.59, 462.91, 602.38 |
| RS | 0.005 | 3.8 | 5 | 320.63, 349.09, 389.28, 459.82, 597.35 |
| RS | 0.0025 | 6.9 | 5 | 320.59, 348.81, 388.62, 458.31, 594.87 |
| RS | 0.001 | 16.2 | 5 | 320.57, 348.64, 388.23, 457.41, 593.40 |
| LTS | 0.05 | 1.6 | 4 | 432.21, 473.79, 573.03, 712.72 |
| LTS | 0.025 | 2.1 | 4 | 431.83, 458.78, 577.43, 755.52 |
| LTS | 0.01 | 3.1 | 4 | 431.58, 449.81, 556.80, 749.21 |
| LTS | 0.005 | 6.0 | 4 | 431.51, 447.35, 540.53, 738.24 |
| LTS | 0.0025 | 10.6 | 4 | 431.46, 446.23, 529.56, 730.07 |
| LTS | 0.001 | 20.7 | 4 | 431.44, 445.60, 522.30, 724.49 |
| FS | 0.05 | 1.4 | 18 | first 317.65, 340.31, ... |
| FS | 0.025 | 1.6 | 19 | first 317.36, 338.84, ... |
| FS | 0.01 | 2.6 | 20 | first 317.15, 337.86, ... |
| FS | 0.005 | 3.8 | 20 | first 317.09, 337.54, ... |
| FS | 0.0025 | 6.1 | 20 | first 317.06, 337.37, ... |
| FS | 0.001 | 16.0 | 20 | first 317.04, 337.26, ... |

Shipped OMV reference spike times (generated with modified NEURON scripts):
RS 320.554, 348.522, 387.944, 456.69, 592.105; LTS 431.423, 445.189, 517.237, 720.422.

## What this means (plain English)

1. **The error shrinks in proportion to the step.** Halving dt roughly halves the change in
   each spike time (for example, RS spike 5 moves 5.0, 2.5 and 1.5 ms as dt goes from 0.01
   to 0.001 ms). That is the signature of a first-order method. It agrees with the audit's
   reading of the jLEMS source: standard NeuroML models are integrated with fixed-step
   forward Euler.
2. **Some features are fragile, and not equally.** The LTS third spike moves about 50 ms
   across the tested range and is still moving at dt = 0.001 ms. The first spikes of all
   cells are stable to about 0.1 ms. So the tolerance rule's refinement term
   `c * |f_h - f_h/2|` is essential: a single global tolerance would either flag solver
   error as "drift" or hide real changes in stable features.
3. **Cost.** Each run costs roughly 15-35 microseconds per simulated cell-step plus about
   1 s of JVM start-up.

## Decision taken (see DECISIONS.md)

Nominal h = 0.005 ms with refinement to h/2 = 0.0025 ms and h/4 = 0.00125 ms. This keeps
one pilot variant's full battery near a minute of CPU while keeping stable features well
resolved. Fragile (model, protocol, feature) combinations are handled by the refinement
term, or are excluded when a feature's defined/undefined state itself changes under
refinement. This choice is provisional until preregistration.
