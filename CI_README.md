# FORGE-X — PLE GitHub Actions CI Bundle

## Contents

- `submission/` — clean copy of the verified Cell 32 candidate.
- `.github/workflows/forge-x-ple-validation.yml` — GitHub Actions workflow.
- `CI_README.md` — this handoff guide.

## Pinned official PLE source

Repository: https://github.com/google-research/ple

Commit:

`8320f0402fdca9f42476607f72bcfd5271cd50c9`

## Python version

Selected version: `3.10`

Reason: Derived from requires-python='>=3.10'.

## GitHub setup

1. Create or select a GitHub repository for FORGE-X.
2. Keep the repository visibility and GitHub Actions usage within the available free quota.
3. Copy the contents of this bundle into the root of that repository.
4. Confirm that `.github/workflows/forge-x-ple-validation.yml` is in the repository.
5. Commit and push the files.
6. Open the repository's Actions tab.
7. Run **FORGE-X PLE Validation**.

The workflow checks out the pinned official PLE source and uses a standard
Ubuntu GitHub-hosted runner with Docker availability.

## Important limitations

- This Kaggle cell does not push files to GitHub.
- No GitHub repository URL was assumed.
- No GitHub credentials or model API keys are embedded.
- `kit check` may report missing model connectivity if the official
  configuration requires credentials not available in CI.
- `kit artifacts` is run only when evaluator-produced artifacts exist.
- A Docker-capable runner does not mean a Docker build has already passed.
- A passing CI workflow does not establish successful hidden-task performance.

## Zero-cost policy

Use standard GitHub-hosted runner availability and quotas. Do not enable paid
cloud services, paid API subscriptions, or paid runner capacity for this project.

## Candidate integrity

This bundle is copied from:

`/kaggle/working/forge_x/ple_candidate_cell32`

The original Cell 32 candidate and immutable Cell 27 baseline are not modified
by this cell.
