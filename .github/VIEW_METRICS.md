# Where to View Metrics

## 1. README Badges (Main Display)

The metrics are displayed as badges at the top of your README:

```markdown
[![CI](https://github.com/ElaMCB/E2E-AI-engineering/actions/workflows/ci.yml/badge.svg)]
![Coverage](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/ElaMCB/E2E-AI-engineering/main/coverage.json)
![Eval Score](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/ElaMCB/E2E-AI-engineering/main/eval.json)
```

**Location:** Top of `README.md` file

## 2. JSON Files (Source Data)

The actual metric data is stored in:
- `coverage.json` - Coverage percentage
- `eval.json` - Evaluation score

**Location:** Repository root directory

**View online:**
- https://raw.githubusercontent.com/ElaMCB/E2E-AI-engineering/main/coverage.json
- https://raw.githubusercontent.com/ElaMCB/E2E-AI-engineering/main/eval.json

## 3. GitHub Actions (Generation Logs)

To see how metrics are generated:
1. Go to **Actions** tab on GitHub
2. Click on a workflow run
3. Find the **`generate-metrics`** job
4. Click to see logs showing:
   - Coverage calculation
   - Eval score generation
   - File creation

## 4. CI Status

To check CI status:
- **Badge in README:** Shows pass/fail status
- **Actions tab:** https://github.com/ElaMCB/E2E-AI-engineering/actions
- **Latest run:** Shows all job statuses

## Current Metrics

- **Coverage:** 0% (will update when tests generate proper coverage)
- **Eval Score:** N/A (placeholder until real evals run)

## How Metrics Update

1. CI runs on every push/PR
2. Tests generate coverage reports
3. `generate-metrics` job aggregates coverage
4. Metrics committed to `main` branch only
5. Badges automatically update via shields.io

