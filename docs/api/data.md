# Data API Reference

## Study

Dataclass representing a single study.

```python
from ehdslens import Study
```

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | int | Unique identifier |
| `authors` | str | Author list |
| `year` | int | Publication year |
| `title` | str | Study title |
| `journal` | str | Journal/source name |
| `study_type` | StudyType | Type of study |
| `primary_axis` | ThematicAxis | Primary thematic axis |
| `quality_rating` | QualityRating | MMAT quality rating |
| `doi` | Optional[str] | DOI if available |
| `country` | Optional[str] | First author country |

### Methods

#### get_citation(style)

Generate a citation in the specified format.

```python
study = db.get_study(1)
print(study.get_citation(style="apa"))
print(study.get_citation(style="vancouver"))
```

#### to_dict()

Convert to dictionary representation.

```python
data = study.to_dict()
```

## StudyDatabase

Container for managing studies.

```python
from ehdslens import StudyDatabase
```

### Methods

#### add_study(study)

Add a study to the database.

```python
db = StudyDatabase()
db.add_study(study)
```

#### get_study(id)

Get study by ID.

```python
study = db.get_study(1)
```

#### filter_by_axis(axis)

Filter by thematic axis.

```python
studies = db.filter_by_axis(ThematicAxis.GOVERNANCE_RIGHTS_ETHICS)
```

#### filter_by_quality(rating)

Filter by quality rating.

```python
studies = db.filter_by_quality(QualityRating.HIGH)
```

#### filter_by_year(start, end)

Filter by year range.

```python
studies = db.filter_by_year(2024, 2025)
```

#### search(query)

Search across authors, titles, journals.

```python
results = db.search("privacy")
```

### Properties

#### studies

Iterator over all studies.

```python
for study in db.studies:
    print(study.title)
```

#### `__len__`

Number of studies.

```python
print(len(db))  # 52
```

## Enums

### ThematicAxis

```python
from ehdslens.data import ThematicAxis

ThematicAxis.GOVERNANCE_RIGHTS_ETHICS
ThematicAxis.SECONDARY_USE_PETS
ThematicAxis.NATIONAL_IMPLEMENTATION
ThematicAxis.CITIZEN_ENGAGEMENT
ThematicAxis.FEDERATED_LEARNING_AI
```

### QualityRating

```python
from ehdslens.data import QualityRating

QualityRating.HIGH
QualityRating.MODERATE
QualityRating.LOW
QualityRating.NOT_APPLICABLE
```

### StudyType

```python
from ehdslens.data import StudyType

StudyType.QUALITATIVE
StudyType.QUANTITATIVE
StudyType.MIXED_METHODS
StudyType.THEORETICAL
StudyType.REVIEW
StudyType.POLICY_DOCUMENT
```

### ConfidenceLevel

```python
from ehdslens.data import ConfidenceLevel

ConfidenceLevel.HIGH
ConfidenceLevel.MODERATE
ConfidenceLevel.LOW
ConfidenceLevel.VERY_LOW
```

## Helper Functions

### load_ehds_studies()

Load the default 52 studies.

```python
from ehdslens.data import load_ehds_studies

studies = load_ehds_studies()
print(f"Loaded {len(studies)} studies")
```
