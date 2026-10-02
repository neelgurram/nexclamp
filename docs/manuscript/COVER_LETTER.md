[Date]

The Editors
*Neuroinformatics*
Springer Nature

Dear Editors,

We submit our manuscript, "Canonical regression tests miss behaviour-changing faults in computational
neuron models: a preregistered held-out evaluation", for consideration as an Original Article.

Published neuron models are constantly modified: refactored, converted between units, ported between
formats and simulators. The usual evidence that such a change preserved behaviour is that the one
simulation shipped with the model still reproduces. How much protection that gives has not, to our
knowledge, been measured. We measured it.

We seeded 120 controlled single-site faults into six NeuroML models that played no part in developing
our method, alongside 48 behaviour-preserving transformations and 18 numerical stress tests. Of the 82
faults that changed behaviour, the canonical test detected 69 (0.841) and a three-protocol current-clamp
battery, chosen in advance on separate development models, detected 80 (0.976); the paired difference is
0.134 (95% cluster-bootstrap interval 0.013 to 0.221). No behaviour-preserving transformation was flagged
by any strategy. Six faults escaped the canonical test on both its summary features and its full voltage
trace, and all six were caught by the battery.

Three features of the design may be of particular interest to the journal. First, the study was
preregistered at AsPredicted (#312455) before any held-out model was simulated, with both possible
outcomes pre-committed to publication, including the outcome that canonical regression is adequate.
Second, the configuration was hash-locked and the campaign sealed, so every reported number is traceable
to a specific run record; a mechanism that refused to start the evaluation when a locked file had been
edited is reported in the deviations. Third, the software, the frozen configuration, every per-variant
record and the complete raw simulation output are publicly archived, and a human audit of 25 sampled
faults, including the six headline cases, is published with its original returned packets.

The manuscript is not under consideration elsewhere, and all authors have approved this submission. We
have no competing interests and received no funding. Use of an AI assistant in developing the software
and drafting the manuscript is disclosed in the Methods.

Yours faithfully,

Neel Gurram, on behalf of the authors
Florida Atlantic University, Jupiter, FL, USA
gurramn2025@fau.edu · ORCID 0009-0009-2441-0825
