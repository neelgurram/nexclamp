# Human audit: returned verdicts

*25 faults, 2 auditors. Compiled 2026-10-02T23:03:16+00:00 at commit `572aa596fae6` (tree dirty: True) by `scripts/audit_results.py` from the auditors' own returned files in `returned/`, which are preserved unmodified.*

## Auditors

- **Naithik**: Auditor name: Naithik Somisetti; worked alone / unseen check: No
- **Samyak**: Auditor name: Samyak Singh; Date completed: 2026-09-22; I worked alone and did not see the automated check (Yes / No): No

## Clarification of the audit conditions (recorded 2026-10-02)

Both returned packets answer "No" to the printed statement "I worked alone and did not see the
automated check". The supervising author (N. Gurram) states that both auditors in fact worked
**completely independently of each other and without access to the automated re-check**: the two
audits were carried out in the same room under his observation specifically so that the auditors did
not talk or compare answers, and neither was given anything beyond the audit packet. The "No" marks
are therefore mis-marks of a compound statement, not a report of shared or assisted work.

This is recorded as a statement by the supervising author, made after the packets were returned. The
packets themselves are preserved unmodified in `returned/`, so the original marks remain visible.

The auditors are two of the study's authors, so the audit is independent of the analysis software and
of each other, but it is not an audit by people outside the author list. The manuscript says so.

## Verdict counts

| Question | Naithik | Samyak | both answered the same |
|---|---|---|---|
| **Q1** (edit matches its label) | Unsure 4, Yes 21 | Unsure 5, Yes 20 | 24/25 |
| **Q2** (assigned class plausible) | No 1, Unsure 1, Yes 23 | Unsure 1, Yes 24 | 24/25 |
| **Q3** (detection plausible) | No 8, Unsure 2, Yes 15 | No 7, Unsure 2, Yes 16 | 24/25 |

## Faults where either auditor did not answer Yes

### Fault 2: `m-scale_conductance-75492a609a`

- hay2011_soma, operator `scale_conductance`, assigned class `4_equivalent_within_tested_domain`
- Naithik: Q1=Yes, Q2=Yes, Q3=No; Samyak: Q1=Yes, Q2=Yes, Q3=No
- automated re-check: clear
- *Naithik*: "​ ​ 0.0675 x 0.5 = 0.03375 exactly. Header states “Detected (features) by: nothing.” Class 4 was satisfied."
- *Samyak*: "As per the table and the detected features, there simply were no features detected in this test."

### Fault 4: `m-scale_gate_time_constant-31e82d8467`

- migliore2005_ca1_soma, operator `scale_gate_time_constant`, assigned class `4_equivalent_within_tested_domain`
- Naithik: Q1=Unsure, Q2=Yes, Q3=No; Samyak: Q1=Unsure, Q2=Yes, Q3=No
- automated re-check: clear
- *Naithik*: "​ ​ The edit sets fixed Q10 from 1 to 0.8. This is an implementation of scale time constant by 0.8, but Q10 scaling is temperature dependent, so I am not fully sure that the resulting τ scale factor is exactly 0.8 from the diff alone."
- *Samyak*: "As for question 1, the editing in the code modifies the temperature parameter to be Q10=0.8, rather than directly scaling the time constant. This creates uncertainties about whether the Q10 adjustment was completed in the pursuit of satisfying the “factor 0.8” description. As for question 3, the feature table detected no entries for this edit. Due to the fact that the metrics of the summary displayed no change within tolerance."

### Fault 6: `m-shift_reversal-e5f14f8fb3`

- hay2011_soma, operator `shift_reversal`, assigned class `4_equivalent_within_tested_domain`
- Naithik: Q1=Unsure, Q2=Yes, Q3=No; Samyak: Q1=Unsure, Q2=Yes, Q3=No
- automated re-check: clear
- *Naithik*: "​ ​ Erev -85 to 95mV is a 10mV shift. The label says by a few mV, which reads as a stretch for 10mV. However, Class 4 rule itself is satisfied. Header confirms that Detected (features) by: nothing. Q3 is N/A"
- *Samyak*: "For question 1, the reversal potential shifted 10 mV. The description for this is “a few mV”, making the large factor of 10 mV seem minor, creating uncertainties about how well the edit matches its label. For question 3, under test protocols, the reversal potential shift did not produce measurable change in the target summary metrics."

### Fault 7: `m-duplicate_conductance-49ae908693`

- smith2013_singlecomp, operator `duplicate_conductance`, assigned class `4_equivalent_within_tested_domain`
- Naithik: Q1=Yes, Q2=Yes, Q3=No; Samyak: Q1=Yes, Q2=Yes, Q3=No
- automated re-check: clear
- *Naithik*: "​ ​ Clean single line duplicate added. Zero detections anywhere. unambiguous Class 4 and unambiguous N/A."
- *Samyak*: "There are zero detections present across the tables. Furthermore, failure to trigger automated detections stems from adding the duplicate line."

### Fault 9: `m-increase_dt-1086ebecdc`

- traub2005_testseg2, operator `increase_dt`, assigned class `6_silent_under_canonical`
- Naithik: Q1=Unsure, Q2=Yes, Q3=Yes; Samyak: Q1=Unsure, Q2=Yes, Q3=Yes
- automated re-check: clear
- *Samyak*: "Integration step size was accurately increased by 4x. But the code lines create uncertainties about whether an unintended secondary edit occurred."

### Fault 10: `m-increase_dt-9ff98cb7be`

- smith2013_singlecomp, operator `increase_dt`, assigned class `6_silent_under_canonical`
- Naithik: Q1=Yes, Q2=No, Q3=No; Samyak: Q1=Unsure, Q2=Yes, Q3=Yes
- automated re-check: clear
- *Naithik*: "​ ​ 0.001 to 0.004ms matches factor 4. Same header line diff noise caveat at fault 9. Class 6 is satisfied. P00_canonical absent from feature table; P09_short_pulse detected at both h,h2."
- *Samyak*: "In this case, the expected numerical stress test specification of a 4x increase in time step size was matched. However, there are uncertainties about whether there was an unintentional second edit."

### Fault 13: `m-scale_conductance-056f6e95e6`

- migliore2005_ca1_soma, operator `scale_conductance`, assigned class `5_non_equivalent`
- Naithik: Q1=Yes, Q2=Yes, Q3=Unsure; Samyak: Q1=Yes, Q2=Yes, Q3=Unsure
- automated re-check: clear
- *Naithik*: "​ ​ 0.05 x 2 = 0.1 exactly. Most feature rows are robust. However, one row lists Tolerance = inf, which cannot logically be exceeded. This is a different and more serious category of issue than a thin margin, and this is why Q3 stays Unsure regardless of how strong the other rows are regardless of how strong the other rows are."
- *Samyak*: "One of the feature rows has “tolerance=inf”, which exceeds computable mathematics, creating uncertainties about the mathematical validity of the data."

### Fault 18: `m-scale_gate_time_constant-97ff619aea`

- smith2013_singlecomp, operator `scale_gate_time_constant`, assigned class `6_silent_under_canonical`
- Naithik: Q1=Unsure, Q2=Yes, Q3=Yes; Samyak: Q1=Unsure, Q2=Yes, Q3=Yes
- automated re-check: clear
- *Naithik*: "​ ​ Same concern like before in fault 4, which is that Q10 is not a direct time constant multiplier, so I am not able to confirm form the diff alone that this produces exactly a 0.5 x τ scaling as the label says."
- *Samyak*: "Here, with no previous temperature factor, the edit provides Q10=0.5. This creates uncertainties about whether this newly introduced Q10 value accurately matches the label of scaling the gate time constant."

### Fault 21: `m-shift_gate_midpoint-f1b7d12414`

- migliore2005_ca1_soma, operator `shift_gate_midpoint`, assigned class `5_non_equivalent`
- Naithik: Q1=Yes, Q2=Unsure, Q3=Yes; Samyak: Q1=Yes, Q2=Unsure, Q3=Yes
- automated re-check: clear
- *Naithik*: "​ ​ Both midpoints shift -30 to -20, q10Setting context line correctly untouched. The h/2 feature rows are truncated out of the packet, and unlike some other Class 5 faults I am not able to find a direct canonical feature row. I am marking this unsure just to be sure instead of assuming its fine."
- *Samyak*: "Both of the midpoints shift from -30 to -20. There is no detectable canonical feature row."

### Fault 22: `m-shift_reversal-293fd11ac3`

- traub2005_testseg_all, operator `shift_reversal`, assigned class `5_non_equivalent`
- Naithik: Q1=Yes, Q2=Yes, Q3=Unsure; Samyak: Q1=Yes, Q2=Yes, Q3=Unsure
- automated re-check: clear
- *Naithik*: "​ ​ Erev 50 to 45mV, a 5mV shift, matching the few mV line comfortably. P00_canonical directly exceeds tolerance at both h and h/2. Class 5 is satisfied. I am flagging Q3 as unsure because the effect size looks disproportionate to the edit."
- *Samyak*: "An extremely large change in the inter-spike interval of 3118% was caused by a small 5 mV reversal potential shift. This creates uncertainties about the sensitivity of the low density persistent sodium channels."

### Fault 23: `m-solver_config-c16c7918b3`

- bbp2015_soma, operator `solver_config`, assigned class `4_equivalent_within_tested_domain`
- Naithik: Q1=Yes, Q2=Yes, Q3=No; Samyak: Q1=Yes, Q2=Yes, Q3=No
- automated re-check: clear
- *Naithik*: "​ ​ The header confirms that no feature differences exceeded tolerance. This is also fully consistent with class 4. There was also a Single <Meta for="jlems" method="eulertree"/> line added, nothing else touched ​"
- *Samyak*: "The header confirms that no feature differences exceeded tolerance. The integration settings were altered by changes in the solver configuration, which did not produce reportable data."

### Fault 24: `m-wrong_channel-36578b9f51`

- hay2011_soma, operator `wrong_channel`, assigned class `2_non_executable`
- Naithik: Q1=Yes, Q2=Yes, Q3=No; Samyak: Q1=Yes, Q2=Yes, Q3=No
- automated re-check: clear
- *Naithik*: "​ ​ ionChannel swapped from Ca_LVAst to pas while ion=”ca” is left in place."
- *Samyak*: "After loading the incompatible channel mechanism, the model displayed a build and compilation error. This led to the feature crashing, leading to a lack of data results."

### Fault 25: `m-wrong_compatible_component-0638e400a0`

- migliore2005_ca1_soma, operator `wrong_compatible_component`, assigned class `3_numerically_unstable`
- Naithik: Q1=Yes, Q2=Yes, Q3=No; Samyak: Q1=Yes, Q2=Yes, Q3=No
- automated re-check: clear
- *Naithik*: "​ ​ ionChannel swapped kdr→kap, both potassium channels with ion="k" and erev left identical"
- *Samyak*: "The substitution of this component created numerical solver instability and integration failure. This integration failure led to NaN outputs, therefore leading to a lack of reportable results."

