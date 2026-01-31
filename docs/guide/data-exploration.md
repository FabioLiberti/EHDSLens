# Data Exploration

Learn how to explore and filter the EHDS systematic review dataset.

## Loading the Database

```python
from ehdslens import EHDSAnalyzer

analyzer = EHDSAnalyzer()
analyzer.load_default_data()

db = analyzer.db
print(f"Loaded {len(db)} studies")
```

## Accessing Individual Studies

### By ID

```python
study = db.get_study(1)
if study:
    print(f"Authors: {study.authors}")
    print(f"Year: {study.year}")
    print(f"Title: {study.title}")
    print(f"Journal: {study.journal}")
    print(f"DOI: {study.doi}")
```

### Iterating All Studies

```python
for study in db.studies:
    print(f"{study.authors} ({study.year})")
```

## Searching

Search across authors, titles, and journals:

```python
# Keyword search
results = analyzer.search_studies("privacy")

# Case-insensitive
results = analyzer.search_studies("GDPR")

# Partial matches work
results = analyzer.search_studies("feder")  # finds "federated"
```

## Filtering

### By Thematic Axis

```python
from ehdslens.data import ThematicAxis

governance = db.filter_by_axis(ThematicAxis.GOVERNANCE_RIGHTS_ETHICS)
pets = db.filter_by_axis(ThematicAxis.SECONDARY_USE_PETS)
```

### By Quality Rating

```python
from ehdslens.data import QualityRating

high_quality = db.filter_by_quality(QualityRating.HIGH)
```

### By Year Range

```python
recent = db.filter_by_year(2024, 2025)
```

### Combined Filters

```python
# Using the analyzer's filter method
filtered = analyzer.filter_studies(
    axis=ThematicAxis.FEDERATED_LEARNING_AI,
    year_start=2023,
    min_quality=QualityRating.MODERATE,
    study_type=StudyType.EMPIRICAL
)
```

### Custom Filters

```python
# Direct filtering with comprehensions
empirical_2024 = [
    s for s in db.studies
    if s.year >= 2024
    and s.study_type in [StudyType.QUALITATIVE, StudyType.QUANTITATIVE]
]
```

## Statistics

```python
stats = analyzer.get_statistics()

# Available statistics
print(stats['total'])           # Total number of studies
print(stats['year_range'])      # (min_year, max_year)
print(stats['by_axis'])         # Count per thematic axis
print(stats['by_quality'])      # Count per quality rating
print(stats['by_type'])         # Count per study type
```

## Citation Generation

```python
study = db.get_study(1)

# APA format
print(study.get_citation(style="apa"))

# Vancouver format
print(study.get_citation(style="vancouver"))
```

## Export Options

```python
# To dictionary
study_dict = study.to_dict()

# Database to JSON
import json
data = [s.to_dict() for s in db.studies]
json_str = json.dumps(data, indent=2)
```
