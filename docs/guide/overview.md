# User Guide Overview

EHDSLens is organized into several modules, each serving a specific purpose in analyzing the EHDS systematic literature review.

## Architecture

```
ehdslens/
├── core.py          # EHDSAnalyzer - main interface
├── data.py          # Study, StudyDatabase, enums
├── analysis.py      # ThematicAnalyzer, QualityAssessor, GRADECERQual
├── visualization.py # EHDSVisualizer - charts and diagrams
├── export.py        # ReportGenerator - reports and bibliographies
└── cli.py           # Command line interface
```

## Core Components

### EHDSAnalyzer

The main entry point providing a unified interface to all functionality:

```python
from ehdslens import EHDSAnalyzer

analyzer = EHDSAnalyzer()
analyzer.load_default_data()
```

### StudyDatabase

Container for the 52 studies with filtering and search capabilities:

```python
from ehdslens import StudyDatabase

db = analyzer.db
print(f"Contains {len(db)} studies")
```

### Study Dataclass

Individual study representation with rich metadata:

```python
study = db.get_study(1)
print(study.authors)
print(study.title)
print(study.primary_axis)
print(study.quality_rating)
```

## Thematic Axes

The five thematic axes from the systematic review:

| Axis | Description |
|------|-------------|
| `GOVERNANCE_RIGHTS_ETHICS` | Data governance, patient rights, ethical frameworks |
| `SECONDARY_USE_PETS` | Privacy-enhancing technologies, data access policies |
| `NATIONAL_IMPLEMENTATION` | Member state transposition, regulatory harmonization |
| `CITIZEN_ENGAGEMENT` | Public trust, participation, health literacy |
| `FEDERATED_LEARNING_AI` | Distributed analytics, AI governance |

## Quality Ratings

MMAT-based quality assessment:

| Rating | Criteria Met |
|--------|--------------|
| `HIGH` | 4-5 of 5 |
| `MODERATE` | 3 of 5 |
| `LOW` | 1-2 of 5 |
| `NOT_APPLICABLE` | Policy documents |

## Workflow Example

```python
from ehdslens import EHDSAnalyzer
from ehdslens.data import ThematicAxis, QualityRating

# 1. Load data
analyzer = EHDSAnalyzer()
analyzer.load_default_data()

# 2. Explore statistics
stats = analyzer.get_statistics()

# 3. Filter relevant studies
studies = analyzer.filter_studies(
    axis=ThematicAxis.FEDERATED_LEARNING_AI,
    min_quality=QualityRating.MODERATE
)

# 4. Analyze themes
analysis = analyzer.analyze_axis(ThematicAxis.FEDERATED_LEARNING_AI)

# 5. Get evidence confidence
findings = analyzer.get_grade_cerqual_summary()

# 6. Export results
from ehdslens.export import ReportGenerator
reporter = ReportGenerator(analyzer.db)
reporter.save_markdown_report("report.md")
```
