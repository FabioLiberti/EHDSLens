# Core API Reference

## EHDSAnalyzer

The main entry point for analyzing the EHDS systematic review dataset.

```python
from ehdslens import EHDSAnalyzer
```

### Class Definition

```python
class EHDSAnalyzer:
    """Main analyzer class providing unified interface to EHDS SLR data."""

    def __init__(self):
        """Initialize the analyzer."""

    def load_default_data(self) -> None:
        """Load the default 52-study database."""

    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the database."""

    def analyze_axis(self, axis: ThematicAxis) -> Dict[str, Any]:
        """Analyze studies within a specific thematic axis."""

    def search_studies(self, query: str) -> List[Study]:
        """Search studies by keyword."""

    def filter_studies(
        self,
        axis: Optional[ThematicAxis] = None,
        year_start: Optional[int] = None,
        year_end: Optional[int] = None,
        min_quality: Optional[QualityRating] = None,
        study_type: Optional[StudyType] = None
    ) -> List[Study]:
        """Filter studies by multiple criteria."""

    def get_grade_cerqual_summary(self) -> List[Dict[str, Any]]:
        """Get GRADE-CERQual confidence assessments."""

    def get_testable_hypotheses(self) -> Dict[str, List[str]]:
        """Get testable hypotheses by category."""

    def get_research_gaps(self) -> List[str]:
        """Get identified research gaps."""
```

### Methods

#### load_default_data()

Load the built-in database of 52 studies from the systematic review.

```python
analyzer = EHDSAnalyzer()
analyzer.load_default_data()
print(f"Loaded {len(analyzer.db)} studies")
```

#### get_statistics()

Returns a dictionary with:

- `total`: Total number of studies
- `year_range`: Tuple of (min_year, max_year)
- `by_axis`: Count per thematic axis
- `by_quality`: Count per quality rating
- `by_type`: Count per study type

```python
stats = analyzer.get_statistics()
```

#### analyze_axis(axis)

Analyze a specific thematic axis.

**Parameters:**
- `axis`: ThematicAxis enum value

**Returns:** Dictionary with:
- `total_studies`: Number of studies in axis
- `themes`: List of key themes
- `quality_distribution`: Quality counts
- `year_distribution`: Year counts

```python
analysis = analyzer.analyze_axis(ThematicAxis.GOVERNANCE_RIGHTS_ETHICS)
```

#### search_studies(query)

Search across authors, titles, and journals.

**Parameters:**
- `query`: Search string (case-insensitive)

**Returns:** List of matching Study objects

```python
results = analyzer.search_studies("federated learning")
```

#### filter_studies(...)

Filter studies by multiple criteria.

**Parameters:**
- `axis`: Optional ThematicAxis
- `year_start`: Optional minimum year
- `year_end`: Optional maximum year
- `min_quality`: Optional minimum QualityRating
- `study_type`: Optional StudyType

**Returns:** List of matching Study objects

```python
filtered = analyzer.filter_studies(
    axis=ThematicAxis.SECONDARY_USE_PETS,
    year_start=2024,
    min_quality=QualityRating.HIGH
)
```

#### get_grade_cerqual_summary()

Get GRADE-CERQual confidence assessments.

**Returns:** List of dictionaries with:
- `finding`: The finding statement
- `confidence`: Confidence level (high/moderate/low/very_low)
- `studies`: Number of contributing studies

```python
findings = analyzer.get_grade_cerqual_summary()
for f in findings:
    print(f"[{f['confidence']}] {f['finding']}")
```

#### get_testable_hypotheses()

Get testable hypotheses organized by category.

**Returns:** Dictionary mapping categories to lists of hypotheses

```python
hypotheses = analyzer.get_testable_hypotheses()
for category, hyps in hypotheses.items():
    print(f"{category}: {len(hyps)} hypotheses")
```

#### get_research_gaps()

Get identified research gaps.

**Returns:** List of research gap descriptions

```python
gaps = analyzer.get_research_gaps()
for gap in gaps:
    print(f"• {gap}")
```
