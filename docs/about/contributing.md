# Contributing

Thank you for your interest in contributing to EHDSLens!

## Getting Started

### 1. Fork the Repository

```bash
git clone https://github.com/FabioLiberti/EHDSLens.git
cd EHDSLens
```

### 2. Set Up Development Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

pip install -e ".[dev]"
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

## Development Guidelines

### Code Style

- Follow PEP 8
- Use Black for formatting
- Use isort for import sorting
- Type hints encouraged

```bash
# Format code
black src/ tests/
isort src/ tests/

# Check linting
flake8 src/ tests/
mypy src/ehdslens
```

### Testing

```bash
# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=ehdslens --cov-report=term-missing
```

### Documentation

- Docstrings for all public functions
- Update relevant docs/ files
- Add examples for new features

## Contribution Types

### Bug Reports

1. Check existing issues first
2. Include Python version
3. Provide minimal reproduction code
4. Include error traceback

### Feature Requests

1. Describe the use case
2. Explain proposed solution
3. Consider alternatives

### Pull Requests

1. Reference related issues
2. Include tests for new features
3. Update documentation
4. Follow commit message conventions

## Commit Messages

```
feat: Add new visualization function
fix: Correct bibliography export format
docs: Update API reference
test: Add tests for search function
refactor: Simplify data loading logic
```

## Pull Request Process

1. Ensure all tests pass
2. Update CHANGELOG.md
3. Request review
4. Address feedback
5. Squash commits if needed

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Follow project guidelines

## Questions?

- Open a GitHub issue
- Contact: fxlybs@gmail.com

Thank you for contributing!
