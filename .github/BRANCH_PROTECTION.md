# Branch Protection Setup

This repository uses branch protection to ensure code quality. The `main` branch is read-only; all changes must go through pull requests that pass CI checks.

## Required Settings

To enable branch protection, go to:
**Settings → Branches → Add rule** (or edit existing rule for `main`)

### Required Checks

Enable these required status checks:
- ✅ `test / ai-monitor`
- ✅ `test / ai-30day-sprint/p1-csv-chat`
- ✅ `test / evals`
- ✅ `lint`
- ✅ `build-status`
- ✅ `generate-metrics`

### Protection Rules

1. **Require a pull request before merging**
   - ✅ Require approvals: 0 (or 1 if you want reviews)
   - ✅ Dismiss stale pull request approvals when new commits are pushed

2. **Require status checks to pass before merging**
   - ✅ Require branches to be up to date before merging
   - ✅ Require all status checks to pass

3. **Require conversation resolution before merging**
   - ✅ (Optional) Require all conversations on code to be resolved

4. **Restrict who can push to matching branches**
   - ❌ **DO NOT ENABLE "Restrict updates"** - This blocks ALL merges!
   - ✅ (Optional) Restrict pushes that create files larger than 100 MB

5. **Do not allow bypassing the above settings**
   - ✅ (Recommended) Do not allow bypassing the above settings

## What This Means

- **Direct pushes to `main` are blocked** - You must create a branch and open a PR
- **PRs must pass all CI checks** - Tests, linting, and build must succeed
- **CI badge will be red if checks fail** - This gates merges automatically
- **Metrics are updated automatically** - Coverage and eval scores are calculated by CI

## Workflow

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and commit
3. Push and create PR: `git push origin feature/my-feature`
4. CI runs automatically
5. Once all checks pass (green), PR can be merged
6. After merge, CI updates `coverage.json` and `eval.json` on main

## Troubleshooting

If CI fails:
- Check the Actions tab for error details
- Fix issues locally: `pytest`, `black .`, `flake8 .`
- Push fixes to the same branch
- CI will re-run automatically

