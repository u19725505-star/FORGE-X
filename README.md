# FORGE-X

**Federated Orchestration and Reasoning for Grounded Engineering**

FORGE-X is an evidence-grounded autonomous engineering-agent research project being developed for Google Research's Physical Engineering's Last Exam (PLE).

## Research objective

Build an engineering workflow that connects source evidence, physical and constraint reasoning, tool execution, independent verification, and traceable deliverables. The system is designed to distinguish verified results from unresolved or unsupported claims.

## Intended architecture

1. **Evidence Fabric** — capture extracted facts, units, source locations, provenance, and confidence.
2. **Engineering Knowledge Graph** — represent entities, physical relationships, dependencies, and uncertainty.
3. **Discipline-aware reasoning** — route structural, civil, electrical, and mechanical work to appropriate calculation and analysis methods.
4. **Tool-driven execution** — coordinate calculations and supported tools through the official PLE interaction protocol.
5. **Independent verification** — check outputs, preserve counterexamples, and report PASS, FAIL, or UNRESOLVED.
6. **Proof-carrying deliverables** — retain assumptions, evidence references, inputs, outputs, verification results, and unresolved issues.

## Current development status

The Kaggle development notebook has established a candidate integration against the pinned official PLE repository and completed local structural, compilation, and contract checks. These checks are development evidence only; they are **not** proof of successful official PLE task completion or benchmark performance.

The next validation stage is to run the official PLE evaluation and artifact checks in a Docker-capable GitHub Actions environment, then evaluate against the official tasks using the competition-provided model configuration.

## Reproducibility and integrity

- Official reference repository: https://github.com/google-research/ple
- Pinned reference commit: `8320f0402fdca9f42476607f72bcfd5271cd50c9`
- Development environment: Kaggle notebooks
- Planned validation environment: GitHub Actions
- Budget constraint: zero-cost tools and hosted resources only; usage limits and current free-tier terms must be respected.

## Important limitations

- A passing local test does not establish engineering correctness for a real project.
- Missing or unauthenticated evidence must not be treated as verified.
- Synthetic fixtures must be labeled as synthetic and kept separate from official PLE task results.
- Do not commit API keys, access tokens, private data, or other secrets.

## Repository contents

The official-submission candidate and validation workflow will be added after the exact generated bundle is transferred and checked against its recorded manifest. This repository README does not itself constitute a competition submission.

## License

The applicable license will be added after confirming the license requirements and provenance of the official starter files and project contributions.

## Live engineering demonstration

The first bounded demonstration challenge and its acceptance rubric are maintained at:

- `submission/demo/structural_axial_member/task.md`
- `submission/demo/structural_axial_member/acceptance_rubric.md`

The trial checks a nominal axial-stress case and a sensitivity case. Its reference values are 200 MPa and 260 MPa respectively, against a supplied 250 MPa comparison limit. It explicitly requires a distinct independent derivation, a written report, and unresolved status for design items not supported by the supplied evidence.

**Important:** this is an internal demonstration brief, not an official PLE benchmark task and not evidence that a live model run has occurred. GitHub Actions currently validates the submission, deterministic engineering methods, and an offline task-loop simulation. A real model-driven run must be performed through the PLE evaluation environment or another properly configured model endpoint.

## Official PLE evaluation path

PLE has two distinct evaluation workflows; do not confuse them:

### Local public development-set evaluation

- The official runner evaluates 29 public tasks and writes evaluator-produced files into `submission/artifacts/`.
- The task dataset is gated on Hugging Face. The operator must request dataset access and provide an `HF_TOKEN` with read permission.
- A local run requires Docker, `uv`, Harbor 0.20.0 with `websockets`, sufficient disk/CPU/RAM, the dataset access above, a model endpoint, and a judge endpoint for rubric-graded tasks.
- For a `google-cloud/<model>` entry, the official local workflow uses `kit/model_proxy`; Google Cloud project authentication and billing may apply. Do not assume this is zero-cost.
- Start with one selected public task using `uv run python eval/run.py ../submission --tasks <task-id> --trials 1`; expand only after the first run is measured and its artifacts are reviewed.
- Never hand-create or edit `submission/artifacts/`. Generate artifacts with the official runner and validate them with `uv run python -m kit artifacts ../submission`.

### Hosted competition evaluation

- Competition entries are submitted through Kaggle.
- The hosted evaluator supplies credentials for the declared Google-sponsored model; entries must use an allowed `google-cloud/<model>` identifier and must not contain personal model API keys.
- The competition page lists 56 hidden test tasks, with a six-hour limit per task.
- Hosted evaluation and local public development-set evaluation are separate workflows. A successful CI build is not a benchmark score.

### Current FORGE-X evidence

- GitHub Actions validates Python syntax, deterministic tool behavior, the offline task-loop simulation, cross-discipline regression cases, and official kit submission validation/build.
- The current workflow does **not** run `eval/run.py`, does not create official PLE task artifacts, and does not establish live-model task performance.
- The structural axial-member trial under `submission/demo/structural_axial_member/` is an internal synthetic demonstration, not one of the official 29 tasks.

Official guide: https://ple-bench.com/competition/guide

Official dev-set evaluation instructions: https://github.com/google-research/ple/blob/main/eval/README.md

Competition page: https://ple-bench.com/competition

