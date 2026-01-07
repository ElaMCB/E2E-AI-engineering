# Contributing to E2E AI Engineering

Thank you for your interest in contributing. This document provides guidelines and instructions for contributing to this repository.

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- (Optional) Docker and Docker Compose

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ElaMCB/E2E-AI-engineering.git
   cd E2E-AI-engineering
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install pre-commit hooks**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

4. **Run tests**
   ```bash
   pytest
   ```

## Code Style

We use automated tools to maintain code quality:

- **Black** for code formatting (line length: 120)
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run all checks before committing:
```bash
black .
isort .
flake8 .
mypy .
```

Or use pre-commit hooks (automatically runs on commit):
```bash
pre-commit run --all-files
```

## Testing

- Write tests for all new features
- Maintain or improve test coverage
- Run tests locally before submitting PRs
- Tests should be fast and deterministic

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest ai-monitor/test_monitor.py
```

## Pull Request Process

**Important:** The `main` branch is protected. All changes must go through pull requests that pass CI checks.

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow code style guidelines
   - Add tests for new functionality
   - Update documentation as needed

3. **Ensure tests pass locally**
   ```bash
   pytest
   pre-commit run --all-files
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a pull request on GitHub.

6. **PR Requirements (Enforced by CI)**
   - ✅ All tests must pass (blocks merge if failing)
   - ✅ All linting checks must pass (blocks merge if failing)
   - ✅ Build status must succeed (blocks merge if failing)
   - ✅ Code coverage is calculated and updated automatically
   - ✅ Evaluation metrics are calculated and updated automatically

7. **After PR is merged**
   - CI automatically updates `coverage.json` and `eval.json` on main
   - Badges in README reflect the latest metrics
   - No manual updates needed

## Project Structure

- `ai-monitor/` - Multi-agent monitoring system
- `ai-30day-sprint/` - Sprint projects
- `evals/` - Evaluation frameworks and metrics
- `docs/` - Documentation and live pages
- `.github/workflows/` - CI/CD workflows

## Evaluation Guidelines

When adding new evaluation metrics or frameworks:

- Document in `evals/README.md`
- Add example configurations
- Include unit tests
- Update case studies if applicable

## Questions?

Open an issue with the `question` label for any clarifications.

