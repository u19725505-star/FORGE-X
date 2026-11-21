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
