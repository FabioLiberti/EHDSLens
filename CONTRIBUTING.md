# Contributing to EHDSLens

Thank you for your interest in contributing to EHDSLens! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to fabio.liberti@unimercatorum.it.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment
4. Create a branch for your changes
5. Make your changes
6. Test your changes
7. Submit a pull request

## How to Contribute

### Reporting Bugs

Before submitting a bug report:
- Check the existing issues to avoid duplicates
- Use the latest version of EHDSLens
- Collect information about the bug (Python version, OS, error messages)

When submitting a bug report, include:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Code samples if applicable
- Environment details

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:
- A clear description of the enhancement
- The motivation and use case
- Possible implementation approach

### Adding Studies

To add new EHDS-related studies to the database:

1. Ensure the study meets inclusion criteria:
   - Published between May 2022 and present
   - Explicit EHDS focus
   - Peer-reviewed or from recognized institutions
   - English language

2. Create a study entry with all required fields:
   ```python
   Study(
       id=NEW_ID,
       authors="Author names",
       year=YEAR,
       title="Full title",
       journal="Journal name",
       study_type=StudyType.APPROPRIATE_TYPE,
       primary_axis=ThematicAxis.APPROPRIATE_AXIS,
       quality_rating=QualityRating.APPROPRIATE_RATING,
       doi="DOI if available",
       country="Country of first author"
   )
   ```

3. Submit via pull request with justification

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/EHDSLens.git
cd EHDSLens

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Verify installation
pytest
```

## Coding Standards

### Style Guide

- Follow PEP 8 guidelines
- Use Black for code formatting (line length: 88)
- Use isort for import sorting
- Add type hints to all functions

### Code Formatting

```bash
# Format code
black src/ tests/
isort src/ tests/

# Check types
mypy src/

# Lint
flake8 src/ tests/
```

### Naming Conventions

- Classes: `PascalCase`
- Functions/methods: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private members: `_leading_underscore`

### Documentation

- All public functions must have docstrings
- Use Google-style docstrings
- Include type hints in signatures

Example:
```python
def analyze_axis(self, axis: ThematicAxis) -> Dict[str, Any]:
    """
    Perform thematic analysis for a specific axis.

    Args:
        axis: The ThematicAxis to analyze.

    Returns:
        Dictionary containing analysis results including
        study counts, themes, and quality distribution.

    Raises:
        ValueError: If axis is not a valid ThematicAxis.
    """
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ehdslens --cov-report=html

# Run specific test file
pytest tests/test_core.py

# Run specific test
pytest tests/test_core.py::TestEHDSAnalyzer::test_load_default_data
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files as `test_*.py`
- Name test functions as `test_*`
- Use pytest fixtures for common setup
- Aim for >80% code coverage

Example:
```python
import pytest
from ehdslens import EHDSAnalyzer

class TestEHDSAnalyzer:
    def test_load_default_data(self):
        """Test that default data loads correctly."""
        analyzer = EHDSAnalyzer()
        analyzer.load_default_data()
        assert len(analyzer.db) == 52
```

## Documentation

### Updating Documentation

- Update README.md for user-facing changes
- Update docstrings for API changes
- Add examples for new features

### Building Documentation

```bash
# If using Sphinx (future)
cd docs
make html
```

## Pull Request Process

1. **Update your fork**
   ```bash
   git fetch upstream
   git merge upstream/main
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make changes**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation as needed

4. **Run quality checks**
   ```bash
   black src/ tests/
   isort src/ tests/
   mypy src/
   pytest
   ```

5. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add description of change"
   ```

   Use conventional commits:
   - `feat:` new feature
   - `fix:` bug fix
   - `docs:` documentation
   - `test:` tests
   - `refactor:` code refactoring

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a pull request on GitHub.

7. **PR Review**
   - Address reviewer feedback
   - Ensure CI passes
   - Maintain a clean commit history

## Questions?

Feel free to open an issue for any questions about contributing.

Thank you for contributing to EHDSLens! 🙏
