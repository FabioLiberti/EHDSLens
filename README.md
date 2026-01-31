# EHDSLens 🔍

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://fabioliberti.github.io/EHDSLens/)
[![Demo](https://img.shields.io/badge/demo-Streamlit%20Cloud-FF4B4B)](https://ehdslens.streamlit.app)
[![Docker](https://img.shields.io/badge/docker-available-2496ED)](https://github.com/FabioLiberti/EHDSLens)

**European Health Data Space Literature Analysis Toolkit**

🌐 **[Live Demo](https://ehdslens.streamlit.app)** | 📖 **[Documentation](https://fabioliberti.github.io/EHDSLens/)** | 🐳 **[Docker](#docker)**

A comprehensive Python toolkit for systematic literature review analysis of the European Health Data Space (EHDS) regulatory framework, based on the methodology described in:

> Liberti, F. (2026). *The European Health Data Space: A Systematic Literature Review - Governance, Privacy-Enhancing Technologies, and Implementation Challenges in the Post-Adoption Era (2022–2026)*.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Data Structure](#data-structure)
- [Methodology](#methodology)
- [Citation](#citation)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The European Health Data Space (EHDS), established by Regulation (EU) 2025/327, represents the EU's most comprehensive regulatory initiative for cross-border health data governance. **EHDSLens** provides researchers, policymakers, and healthcare professionals with tools to:

- **Analyze** the systematic review corpus of 52 studies
- **Explore** thematic distributions across five research axes
- **Assess** study quality using MMAT criteria
- **Evaluate** evidence confidence using GRADE-CERQual
- **Generate** reports and bibliographies
- **Visualize** research trends and gaps

### Key Findings from the Review

| Finding | Studies | Confidence |
|---------|---------|------------|
| Governance tensions between secondary use and rights protection | n=18 | 🟢 HIGH |
| PET maturity gap: 23% FL production deployment | n=15 | 🟡 MODERATE |
| Nordic countries 2-3 years ahead in HDAB capacity | n=9 | 🟡 MODERATE |
| Citizen engagement predominantly symbolic | n=6 | 🟢 HIGH |
| Legal uncertainty re: FL compliance | n=4 | 🟡 MODERATE |

---

## ✨ Features

### Core Functionality

- **Study Database**: Complete dataset of 52 included studies with full metadata
- **Thematic Analysis**: Seven-category coding framework aligned with EHDS dimensions
- **Quality Assessment**: MMAT-based quality ratings for empirical studies
- **GRADE-CERQual**: Confidence assessment for synthesized findings
- **Search & Filter**: Flexible queries across authors, titles, themes, and years

### Export Options

- **Reports**: Markdown, HTML, and JSON formats
- **Bibliographies**: BibTeX, RIS, APA, Vancouver styles
- **Data**: CSV, JSON, and Excel exports
- **Visualizations**: Chart data for Matplotlib, Plotly, and LaTeX

### Interactive Dashboard

```bash
# Launch Streamlit dashboard
ehdslens dashboard

# Custom port
ehdslens dashboard --port 8501
```

### REST API

```bash
# Start API server
ehdslens api

# With custom host/port
ehdslens api --host 0.0.0.0 --port 8000 --reload
```

### Command Line Interface

```bash
# Show database statistics
ehdslens stats

# Analyze specific thematic axis
ehdslens analyze governance

# Search studies
ehdslens search "federated learning"

# Generate report
ehdslens report markdown -o report.md

# Export bibliography
ehdslens export bibtex -o references.bib

# Launch dashboard
ehdslens dashboard

# Start API server
ehdslens api
```

---

## 📦 Installation

### From PyPI (recommended)

```bash
pip install ehdslens
```

### From Source

```bash
git clone https://github.com/FabioLiberti/EHDSLens.git
cd EHDSLens
pip install -e .
```

### What's Included

The base installation includes everything you need:
- ✅ Interactive Streamlit Dashboard
- ✅ FastAPI REST API
- ✅ Plotly visualizations
- ✅ Pandas data manipulation

### Optional Dependencies

```bash
# For matplotlib support
pip install ehdslens[viz]

# For Excel export
pip install ehdslens[export]

# For development
pip install ehdslens[dev]

# All optional dependencies
pip install ehdslens[all]
```

### Docker

Run with Docker (no installation needed):

```bash
# Clone repository
git clone https://github.com/FabioLiberti/EHDSLens.git
cd EHDSLens

# Run with Docker Compose (Dashboard + API)
docker-compose up

# Or just the dashboard
docker build -t ehdslens .
docker run -p 8501:8501 ehdslens
```

Access:
- Dashboard: http://localhost:8501
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🚀 Quick Start

### Python API

```python
from ehdslens import EHDSAnalyzer

# Initialize and load the 52-study database
analyzer = EHDSAnalyzer()
analyzer.load_default_data()

# Get overview statistics
stats = analyzer.get_statistics()
print(f"Total studies: {stats['total']}")
print(f"Year range: {stats['year_range']}")

# Analyze specific thematic axis
governance = analyzer.analyze_axis(ThematicAxis.GOVERNANCE_RIGHTS_ETHICS)
print(f"Governance studies: {governance['total_studies']}")

# Get GRADE-CERQual summary
findings = analyzer.get_grade_cerqual_summary()
for f in findings:
    print(f"{f['confidence']}: {f['finding']}")

# Search studies
results = analyzer.search_studies("federated learning")
for study in results:
    print(f"{study.authors} ({study.year}): {study.title}")
```

### Command Line

```bash
# View statistics
ehdslens stats

# Analyze all axes
ehdslens analyze all --json > analysis.json

# Generate comprehensive report
ehdslens report html -o ehds_report.html

# Show GRADE-CERQual findings
ehdslens grade
```

---

## 📖 Usage

### Working with Studies

```python
from ehdslens import EHDSAnalyzer
from ehdslens.data import ThematicAxis, QualityRating

analyzer = EHDSAnalyzer()
analyzer.load_default_data()

# Filter studies by multiple criteria
studies = analyzer.filter_studies(
    axis=ThematicAxis.SECONDARY_USE_PETS,
    year_start=2024,
    min_quality=QualityRating.HIGH
)

# Export filtered results
for study in studies:
    print(study.get_citation(style="apa"))
```

### Quality Assessment

```python
from ehdslens.analysis import QualityAssessor

assessor = QualityAssessor(analyzer.db)

# Get MMAT criteria for a study type
criteria = assessor.get_criteria(StudyType.QUALITATIVE)
for criterion in criteria:
    print(f"- {criterion}")

# Get quality distribution summary
summary = assessor.generate_quality_summary()
print(f"High quality: {summary['high']['percentage']:.1f}%")
```

### GRADE-CERQual Analysis

```python
from ehdslens.analysis import GRADECERQual

grade = GRADECERQual(analyzer.db)

# Get pre-configured assessments
assessments = grade.get_ehds_assessments()
for a in assessments:
    print(f"{a.overall_confidence.value.upper()}: {a.finding}")
    print(f"  Explanation: {a.explanation}")
```

### Generating Reports

```python
from ehdslens.export import ReportGenerator
from pathlib import Path

generator = ReportGenerator(analyzer.db)

# Full analysis report
generator.generate_full_report(Path("report.md"), format="markdown")

# Bibliography in BibTeX
generator.generate_bibliography(Path("refs.bib"), format="bibtex")

# Data extraction template
generator.generate_data_extraction_template(Path("template.md"))
```

### Visualization

```python
from ehdslens.visualization import EHDSVisualizer

viz = EHDSVisualizer(analyzer.db)

# Get PRISMA diagram data
prisma = viz.create_prisma_diagram_data()
print(f"Records identified: {prisma['identification']['total_database']}")
print(f"Studies included: {prisma['included']['total']}")

# Export for Plotly
viz.export_for_plotly(Path("chart_data.json"))

# ASCII chart for terminal
print(viz.create_year_distribution_chart(format="ascii"))
```

---

## 📊 Data Structure

### Thematic Axes

The systematic review organizes studies across five thematic axes:

| Axis | Focus | Studies |
|------|-------|---------|
| **Governance, Rights, Ethics** | Consent, opt-out, HDAB design, accountability | 18 |
| **Secondary Use & PETs** | Federated learning, SPEs, interoperability | 15 |
| **National Implementation** | Member State readiness, HDAB capacity | 9 |
| **Citizen Engagement** | Public trust, transparency, participation | 6 |
| **Federated Learning & AI** | Legal compliance, governance frameworks | 4 |

### Study Types

- Qualitative empirical (n=12)
- Quantitative empirical (n=6)
- Mixed methods (n=4)
- Conceptual/analytical (n=16)
- Systematic reviews (n=4)
- Policy documents (n=10)

### Quality Ratings

Based on Mixed Methods Appraisal Tool (MMAT) 2018:
- **High**: ≥80% criteria met
- **Moderate**: 60-79% criteria met
- **Low**: <60% criteria met

---

## 🔬 Methodology

### Theoretical Framework

EHDSLens implements an integrated theoretical framework combining:

1. **TOE Framework** (Tornatzky & Fleischer, 1990): Technology-Organization-Environment analysis
2. **Social Licence Theory** (Gunningham et al., 2004): Legitimacy and trust dimensions
3. **Multi-Level Governance** (Hooghe & Marks, 2003): EU-national coordination

### PRISMA 2020 Flow

```
Records identified (n=847)
         │
         ▼
Duplicates removed (n=156)
         │
         ▼
Title/abstract screened (n=691)
         │
         ▼
Full-text assessed (n=124)
         │
         ▼
Studies included (n=52)
  ├── Peer-reviewed: 38
  └── Grey literature: 14
```

### GRADE-CERQual Components

1. **Methodological limitations**: Study quality concerns
2. **Coherence**: Consistency of findings across studies
3. **Adequacy**: Richness and quantity of data
4. **Relevance**: Applicability to review question

---

## 📚 API Reference

### Core Classes

#### `EHDSAnalyzer`

Main entry point for analysis.

```python
class EHDSAnalyzer:
    def load_default_data() -> None
    def get_statistics() -> Dict[str, Any]
    def analyze_axis(axis: ThematicAxis) -> Dict[str, Any]
    def search_studies(query: str) -> List[Study]
    def filter_studies(**criteria) -> List[Study]
    def get_grade_cerqual_summary() -> List[Dict]
    def get_testable_hypotheses() -> Dict[str, List[str]]
```

#### `StudyDatabase`

Study data management.

```python
class StudyDatabase:
    def add_study(study: Study) -> None
    def get_study(id: int) -> Optional[Study]
    def filter_by_axis(axis: ThematicAxis) -> List[Study]
    def filter_by_year(start: int, end: int) -> List[Study]
    def search(query: str) -> List[Study]
    def to_json(filepath: Path) -> str
    def to_csv(filepath: Path) -> None
```

#### `Study`

Individual study data model.

```python
@dataclass
class Study:
    id: int
    authors: str
    year: int
    title: str
    journal: str
    study_type: StudyType
    primary_axis: ThematicAxis
    quality_rating: QualityRating
    doi: Optional[str]
    country: Optional[str]
```

### Enumerations

```python
class ThematicAxis(Enum):
    GOVERNANCE_RIGHTS_ETHICS
    SECONDARY_USE_PETS
    NATIONAL_IMPLEMENTATION
    CITIZEN_ENGAGEMENT
    FEDERATED_LEARNING_AI

class QualityRating(Enum):
    HIGH
    MODERATE
    LOW
    NOT_APPLICABLE

class StudyType(Enum):
    QUALITATIVE
    QUANTITATIVE
    MIXED_METHODS
    CONCEPTUAL
    SYSTEMATIC_REVIEW
    POLICY_DOCUMENT
    TECHNICAL
```

---

## 📖 Citation

If you use EHDSLens in your research, please cite:

```bibtex
@article{liberti2026ehds,
  title={The European Health Data Space: A Systematic Literature Review},
  author={Liberti, Fabio},
  journal={Journal of Medical Internet Research},
  year={2026},
  doi={10.2196/xxxxx}
}
```

And the software:

```bibtex
@software{ehdslens,
  author={Liberti, Fabio},
  title={EHDSLens: European Health Data Space Literature Analysis Toolkit},
  year={2026},
  url={https://github.com/FabioLiberti/EHDSLens},
  version={1.2.0}
}
```

---

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guidelines](CONTRIBUTING.md).

### Development Setup

```bash
git clone https://github.com/FabioLiberti/EHDSLens.git
cd EHDSLens
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
isort src/

# Type checking
mypy src/
```

### Adding New Studies

To add studies from future literature:

```python
from ehdslens.data import Study, StudyDatabase, StudyType, ThematicAxis

db = StudyDatabase()
db.from_json("existing_data.json")

new_study = Study(
    id=53,
    authors="New Author et al.",
    year=2026,
    title="New EHDS Study",
    journal="New Journal",
    study_type=StudyType.QUALITATIVE,
    primary_axis=ThematicAxis.GOVERNANCE_RIGHTS_ETHICS,
    quality_rating=QualityRating.HIGH
)
db.add_study(new_study)
db.to_json("updated_data.json")
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **TEHDAS Joint Action** for making preparatory materials publicly available
- **PRISMA 2020** guidelines for systematic review methodology
- **GRADE-CERQual** working group for confidence assessment framework
- All authors of the 52 studies included in the systematic review

---

## 📬 Contact

**Fabio Liberti, PhD**
Department of Computer Science
Universitas Mercatorum, Rome, Italy
📧 fabio.liberti@studenti.unimercatorum.it

---

<p align="center">
  <b>EHDSLens</b> - Illuminating the European Health Data Space Research Landscape
</p>
