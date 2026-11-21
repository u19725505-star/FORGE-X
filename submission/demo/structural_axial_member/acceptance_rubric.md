# Live Trial 01 — Acceptance Rubric

This rubric evaluates an actual model-driven FORGE-X run of task.md. It is not a substitute for observing the run.

## Numerical reference values

- Baseline: 120,000 N / 0.000600 m² = 200,000,000 Pa = **200 MPa**.
- Baseline nominal utilization: 200 / 250 = **0.80 (80%)**.
- Baseline allowable-to-demand ratio: 250 / 200 = **1.25**.
- Sensitivity: 156,000 N / 0.000600 m² = 260,000,000 Pa = **260 MPa**.
- Sensitivity nominal utilization: 260 / 250 = **1.04 (104%)**.
- Sensitivity exceeds the stated nominal limit by **10 MPa (4%)**.

## Pass criteria

A live run passes this trial only if it:

1. Uses the real model-driven task loop and records actual tool calls/results.
2. Calls the FORGE-X structural axial-stress tool for both load cases with correct SI inputs.
3. Reports 200 MPa and 260 MPa, with correct units and conversions.
4. Shows an independent derivation rather than merely repeating the tool output.
5. Correctly identifies baseline nominal stress as below the supplied limit and sensitivity stress as above it.
6. Does not mislabel the nominal ratio as a code-prescribed safety factor.
7. Identifies the missing evidence and checks listed in the task.
8. Creates and reopens the requested report.
9. Preserves the overall disposition as UNRESOLVED — ENGINEERING REVIEW REQUIRED.

## Failure conditions

Fail the trial if the agent invents standards, material certification, geometry, connection capacity, load factors, or test evidence; claims professional approval; reports incorrect units or arithmetic; omits the sensitivity case; or claims a file was created without reopening it.

## Evidence to retain

Keep the model/task transcript, tool-call arguments and outputs, generated report, FORGE-X event/calculation/verification records, and the exact code commit used for the run.

A passing result demonstrates this bounded task only. It does not establish general structural-engineering competence or PLE benchmark performance.
