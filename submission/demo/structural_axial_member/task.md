# FORGE-X Live Trial 01 — Axial Tie-Member Verification

## Mission

Act as FORGE-X, an engineering analysis agent. Analyze the supplied axial tie-member case using the available engineering tools. Do not assume that a numerical calculation alone establishes structural adequacy.

## Supplied design brief

| Parameter | Value |
|---|---:|
| Service tensile force, F | 120,000 N |
| Net cross-sectional area, A | 0.000600 m² |
| Specified allowable tensile stress | 250 MPa |
| Load case for sensitivity check | 156,000 N |
| Member length | Not supplied |
| Connection / net-section details | Not supplied |
| Applicable design code and load factors | Not supplied |

For this demonstration only, use the stated allowable stress as the comparison limit. Do not invent a design code, load factor, material certification, connection capacity, or missing geometry.

## Required agent behavior

1. Interpret the task as a structural axial-stress check. State the idealizations: concentric axial load, uniform net area, prismatic member, and linear nominal stress calculation.
2. Convert units explicitly. Use the FORGE-X forge_x_calculate tool with discipline structural, method axial_stress, and SI inputs for the 120,000 N case.
3. Independently verify the result by a distinct calculation route. Do not simply repeat the same tool call and describe it as independent verification. Show the governing equation, substituted values, and units.
4. Calculate utilization = calculated stress / stated allowable stress, and the corresponding ratio of allowable stress to calculated stress. Label these as simple nominal ratios, not a code-prescribed safety factor.
5. Run the sensitivity case at 156,000 N using the same area and the FORGE-X tool. Determine whether the nominal stress exceeds the stated allowable limit.
6. Identify missing information that prevents a complete structural design conclusion. At minimum discuss member length and deformation, connection capacity, stability / buckling relevance, material and section evidence, load combinations, and applicable design standard.
7. Create structural_demo_report.md in the task working directory. Include inputs, assumptions, equations, tool outputs, independent check, sensitivity result, limitations, and a clear status for each check.
8. Re-open the report with the available file-reading tool and verify it exists and contains the key results before finishing.

## Required decision language

For the baseline case, report only whether the calculated nominal axial stress is below the supplied allowable-stress value under the stated idealizations.

For the sensitivity case, report whether the calculated nominal stress exceeds the supplied limit.

Do not describe either result as a certified design, code-compliant design, safe-to-build approval, or professional engineering signoff. If evidence is missing, mark the overall engineering disposition UNRESOLVED — ENGINEERING REVIEW REQUIRED.

## Completion response

Summarize the baseline stress, nominal utilization, sensitivity result, unresolved design checks, and exact report path. Be explicit about which steps were actually performed and which could not be verified.
