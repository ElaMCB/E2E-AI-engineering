# Fix: "Cannot update this protected ref"

This error means branch protection is blocking the merge. Here's how to fix it:

## Most Common Cause: "Restrict updates" is enabled

If "Restrict updates" is enabled in your ruleset, it blocks ALL updates to the branch, including merges.

### Fix:
1. Go to **Settings → Rulesets → Edit "main branch"**
2. Find **"Restrict updates"**
3. **DISABLE IT** (uncheck the box)
4. Save the ruleset

## Other Things to Check:

### 1. Status Checks Configuration
- Go to "Require status checks to pass"
- Make sure all 6 checks are selected:
  - `test / ai-monitor`
  - `test / ai-30day-sprint/p1-csv-chat`
  - `test / evals`
  - `lint`
  - `build-status`
  - `generate-metrics`
- Make sure "Require branches to be up to date" is enabled

### 2. Required Approvals
- Under "Require a pull request before merging"
- Set "Required approvals" to **0**

### 3. Deployments
- Make sure "Require deployments to succeed" is **DISABLED**

### 4. Merge Methods
- Under "Require a pull request before merging"
- Make sure at least one merge method is enabled (e.g., "Allow merge commits")

## Quick Fix Order:

1. **Disable "Restrict updates"** ← Most likely the issue
2. Set "Required approvals" to 0
3. Disable "Require deployments to succeed"
4. Verify all 6 status checks are selected
5. Save and try merging again

## If Still Blocked:

Temporarily disable the entire ruleset:
1. Go to Settings → Rulesets
2. Click on "main branch"
3. Change "Enforcement status" to "Disabled"
4. Try merging
5. Re-enable with correct settings

