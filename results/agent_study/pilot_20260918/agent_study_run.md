# Agent study run

*2026-09-18T21:42:49+00:00; commit `115673a9a8a0e3d7d160c126b4ed4b0a16ecc677`; 3 trial(s); status: **FEASIBILITY PILOT (isolation partial; not the confirmatory agent study)**.*

- passed basic validation (schema, execution, canonical): **0 of 3**
- passed every layer: **0 of 3**
- **passed basic validation but failed the battery: 0 of 3**
- unauthorized edits detected: 0
- left the model unchanged: 0

| trial | task type | edit scope | hidden assertions | schema | executes | canonical | battery | category |
|---|---|---|---|---|---|---|---|---|
| `t01_unit_repair__r01` | repair_seeded_unit_error | pass | pass | pass | pass | error | not_evaluated | indeterminate |
| `t05_unit_conversion__r01` | equivalent_unit_conversion | pass | pass | pass | pass | error | not_evaluated | indeterminate |
| `t06_single_conductance_change__r01` | change_one_conductance | pass | pass | pass | pass | error | not_evaluated | indeterminate |

basic_pass_battery_fail counts edits that pass the checks a practitioner would normally run (schema validity, execution, the canonical harness) but fail the perturbation battery. That is the only quantity this study claims about agents.

**This run is not the confirmatory agent study.** Isolation was not environmental (the agent ran under an account that can read the repository), and/or the evaluation config was not frozen. It is reported as harness and feasibility evidence only.
