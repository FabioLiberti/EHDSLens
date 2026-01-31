# Quick Start

Get up and running with EHDSLens in 5 minutes.

## Basic Usage

### 1. Import and Initialize

```python
from ehdslens import EHDSAnalyzer

# Create analyzer and load the 52-study database
analyzer = EHDSAnalyzer()
analyzer.load_default_data()
```

### 2. Get Statistics

```python
stats = analyzer.get_statistics()

print(f"Total studies: {stats['total']}")
print(f"Year range: {stats['year_range']}")
print(f"Studies by axis: {stats['by_axis']}")
print(f"Quality distribution: {stats['by_quality']}")
```

### 3. Search Studies

```python
# Search by keyword
results = analyzer.search_studies("privacy")
for study in results:
    print(f"- {study.authors} ({study.year}): {study.title}")
```

### 4. Filter Studies

```python
from ehdslens.data import ThematicAxis, QualityRating

# Get high-quality governance studies from 2024+
filtered = analyzer.filter_studies(
    axis=ThematicAxis.GOVERNANCE_RIGHTS_ETHICS,
    year_start=2024,
    min_quality=QualityRating.HIGH
)
```

### 5. Analyze Themes

```python
# Analyze a specific thematic axis
analysis = analyzer.analyze_axis(ThematicAxis.SECONDARY_USE_PETS)

print(f"Studies: {analysis['total_studies']}")
print(f"Key themes: {analysis['themes']}")
```

### 6. Get GRADE-CERQual Findings

```python
findings = analyzer.get_grade_cerqual_summary()

for f in findings:
    print(f"[{f['confidence'].upper()}] {f['finding']}")
```

## Command Line Usage

```bash
# Show database statistics
ehdslens stats

# Analyze governance axis
ehdslens analyze governance

# Search for studies
ehdslens search "federated learning"

# Export bibliography
ehdslens export --format bibtex -o references.bib

# Generate report
ehdslens report -o report.md

# Show GRADE-CERQual findings
ehdslens grade
```

## Next Steps

- [Data Exploration Guide](../guide/data-exploration.md)
- [Visualization Tutorial](../guide/visualization.md)
- [API Reference](../api/core.md)
