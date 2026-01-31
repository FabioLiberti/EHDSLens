# EHDSLens

**A Python toolkit for analyzing the European Health Data Space (EHDS) systematic literature review**

[![PyPI version](https://badge.fury.io/py/ehdslens.svg)](https://badge.fury.io/py/ehdslens)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/FabioLiberti/EHDSLens/actions/workflows/ci.yml/badge.svg)](https://github.com/FabioLiberti/EHDSLens/actions/workflows/ci.yml)

---

## Overview

EHDSLens provides programmatic access to the dataset and analytical tools from the systematic literature review:

> **"European Health Data Space (EHDS) Regulation (EU) 2025/327: A Systematic Review of Implementation Challenges and Opportunities"**

The toolkit enables researchers, policymakers, and practitioners to:

- 📊 **Explore** 52 peer-reviewed studies and grey literature
- 🔍 **Search & Filter** by thematic axis, quality rating, year, and more
- 📈 **Visualize** publication trends, quality distributions, and thematic coverage
- 📝 **Export** bibliographies (BibTeX, RIS, APA, Vancouver) and reports
- 🎯 **Analyze** GRADE-CERQual confidence assessments

## Quick Example

```python
from ehdslens import EHDSAnalyzer

# Initialize and load the 52-study database
analyzer = EHDSAnalyzer()
analyzer.load_default_data()

# Get statistics
stats = analyzer.get_statistics()
print(f"Total studies: {stats['total']}")

# Search for federated learning studies
fl_studies = analyzer.search_studies("federated learning")
print(f"Found {len(fl_studies)} studies about federated learning")

# Get GRADE-CERQual findings
findings = analyzer.get_grade_cerqual_summary()
for f in findings:
    print(f"{f['confidence'].upper()}: {f['finding']}")
```

## Installation

```bash
pip install ehdslens
```

Or with visualization support:

```bash
pip install ehdslens[viz]
```

## Features

### Five Thematic Axes

The systematic review organizes findings across five key domains:

| Axis | Focus Area |
|------|------------|
| **Governance, Rights & Ethics** | Data governance frameworks, patient rights, ethical considerations |
| **Secondary Use & PETs** | Privacy-enhancing technologies, anonymization, data access |
| **National Implementation** | Member state transposition, regulatory challenges |
| **Citizen Engagement** | Public trust, participation, health literacy |
| **Federated Learning & AI** | Distributed analytics, AI governance, interoperability |

### Quality Assessment

All studies are assessed using the Mixed Methods Appraisal Tool (MMAT):

- 🟢 **High Quality**: 4-5 criteria met
- 🟡 **Moderate Quality**: 3 criteria met
- 🟠 **Low Quality**: 1-2 criteria met
- ⚪ **N/A**: Policy documents (different criteria)

### GRADE-CERQual

Confidence in findings assessed using GRADE-CERQual methodology:

- Methodological limitations
- Coherence
- Adequacy of data
- Relevance

## Command Line Interface

```bash
# Show statistics
ehdslens stats

# Analyze a thematic axis
ehdslens analyze governance

# Search studies
ehdslens search "privacy"

# Export bibliography
ehdslens export --format bibtex -o references.bib

# Show GRADE-CERQual findings
ehdslens grade
```

## Documentation

- [Getting Started](getting-started/installation.md)
- [User Guide](guide/overview.md)
- [API Reference](api/core.md)
- [Methodology](methodology/prisma.md)

## Citation

If you use EHDSLens in your research, please cite:

```bibtex
@article{liberti2025ehds,
  title={European Health Data Space (EHDS) Regulation (EU) 2025/327:
         A Systematic Review of Implementation Challenges and Opportunities},
  author={Liberti, Fabio},
  journal={[Journal Name]},
  year={2025},
  doi={[DOI]}
}
```

## License

MIT License - see [LICENSE](https://github.com/FabioLiberti/EHDSLens/blob/main/LICENSE) for details.
