# Installation

## Requirements

- Python 3.9 or higher
- pip package manager

## Basic Installation

Install EHDSLens from PyPI:

```bash
pip install ehdslens
```

## Installation Options

### With Visualization Support

For matplotlib and plotly charts:

```bash
pip install ehdslens[viz]
```

### With Export Support

For advanced export features:

```bash
pip install ehdslens[export]
```

### Full Installation

All optional dependencies:

```bash
pip install ehdslens[all]
```

### Development Installation

For contributing to the project:

```bash
git clone https://github.com/FabioLiberti/EHDSLens.git
cd EHDSLens
pip install -e ".[dev]"
```

## Verify Installation

```python
import ehdslens
print(ehdslens.__version__)
```

Or from command line:

```bash
ehdslens --version
```

## Troubleshooting

### Common Issues

**ImportError: No module named 'ehdslens'**

Ensure you've installed the package in your active Python environment:

```bash
pip show ehdslens
```

**Permission errors on Linux/Mac**

Use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
pip install ehdslens
```

### Getting Help

- [GitHub Issues](https://github.com/FabioLiberti/EHDSLens/issues)
- [Documentation](https://fabioliberti.github.io/EHDSLens/)
