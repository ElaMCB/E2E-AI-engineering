# Fix: Metrics Push Blocked by Branch Protection

## Problem

The `generate-metrics` job fails with:
```
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote: - Changes must be made through a pull request.
remote: - 2 of 2 required status checks are expected.
```

This happens because branch protection rules block direct pushes to `main`, even from GitHub Actions.

## Solutions

### Option 1: Use a Personal Access Token (PAT) with Bypass Permissions (Recommended)

1. **Create a PAT:**
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate a new token with `repo` scope
   - **Important:** The token must be created by a user who has admin access to the repository

2. **Add PAT as Secret:**
   - Go to Repository Settings → Secrets and variables → Actions
   - Add a new secret named `METRICS_PAT` with the token value

3. **Configure Branch Protection:**
   - Go to Repository Settings → Branches → Branch protection rules → `main`
   - Under "Restrict who can push to matching branches", add the user who created the PAT
   - This allows that user (and workflows using their PAT) to bypass protection

4. **The workflow will automatically use the PAT** if it's available, otherwise it will fall back to `GITHUB_TOKEN` (which will still fail, but with a warning)

### Option 2: Allow Workflow to Bypass Branch Protection

1. Go to Repository Settings → Branches → Branch protection rules → `main`
2. Scroll to "Allow specified actors to bypass required pull requests"
3. Add the GitHub App or user that runs the workflow
4. **Note:** This may not work with the default `GITHUB_TOKEN` - you may still need a PAT

### Option 3: Commit to Separate Branch and Auto-Merge

Modify the workflow to:
1. Commit metrics to a branch like `metrics/auto-update`
2. Create a PR automatically
3. Use a separate workflow or GitHub API to auto-merge the PR

This is more complex but doesn't require bypass permissions.

### Option 4: Use GitHub API to Update Files

Instead of `git push`, use the GitHub API to update the files directly. This requires more complex scripting but can work around branch protection.

## Current Status

The workflow is configured to:
- Try to push using `METRICS_PAT` if available
- Fall back to `GITHUB_TOKEN` if PAT is not set
- Show warnings if push fails but not fail the entire job
- Generate metrics files even if they can't be committed (they'll be in artifacts)

## Verification

After setting up the PAT:
1. Push a commit to `main` (or merge a PR)
2. Check the `generate-metrics` job logs
3. Verify that `coverage.json` and `eval.json` are committed to `main`
4. Check that badges update on the README
