# Analysis

Learn how to perform thematic analysis and quality assessment.

## Thematic Analysis

### Analyze by Axis

```python
from ehdslens import EHDSAnalyzer
from ehdslens.data import ThematicAxis

analyzer = EHDSAnalyzer()
analyzer.load_default_data()

# Analyze a specific axis
analysis = analyzer.analyze_axis(ThematicAxis.GOVERNANCE_RIGHTS_ETHICS)

print(f"Total studies: {analysis['total_studies']}")
print(f"Key themes: {analysis['themes']}")
print(f"Quality distribution: {analysis['quality_distribution']}")
```

### Available Axes

| Axis | Key Themes |
|------|------------|
| Governance, Rights & Ethics | GDPR alignment, patient rights, consent mechanisms |
| Secondary Use & PETs | Anonymization, differential privacy, secure computation |
| National Implementation | Regulatory transposition, institutional readiness |
| Citizen Engagement | Trust building, health literacy, participation models |
| Federated Learning & AI | Distributed analytics, model governance, interoperability |

## GRADE-CERQual Assessment

### Get Confidence Findings

```python
findings = analyzer.get_grade_cerqual_summary()

for f in findings:
    print(f"Confidence: {f['confidence']}")
    print(f"Finding: {f['finding']}")
    print(f"Studies: n={f['studies']}")
    print()
```

### Confidence Levels

| Level | Interpretation |
|-------|----------------|
| **High** | Highly likely that the finding is a reasonable representation |
| **Moderate** | Likely that the finding is a reasonable representation |
| **Low** | Possible that the finding is a reasonable representation |
| **Very Low** | Unclear whether the finding is a reasonable representation |

### Assessment Components

GRADE-CERQual assesses:

1. **Methodological limitations** - Quality of contributing studies
2. **Coherence** - How well data supports the finding
3. **Adequacy** - Richness and quantity of data
4. **Relevance** - Applicability to review question

## Quality Assessment (MMAT)

### Access Quality Assessor

```python
from ehdslens.analysis import QualityAssessor

assessor = QualityAssessor()

# Get MMAT criteria
criteria = assessor.get_mmat_criteria()
```

### Quality Distribution

```python
stats = analyzer.get_statistics()

print("Quality Distribution:")
for rating, count in stats['by_quality'].items():
    print(f"  {rating}: {count} studies")
```

## Research Gaps

```python
gaps = analyzer.get_research_gaps()

print("Identified Research Gaps:")
for i, gap in enumerate(gaps, 1):
    print(f"{i}. {gap}")
```

## Testable Hypotheses

```python
hypotheses = analyzer.get_testable_hypotheses()

for category, hyps in hypotheses.items():
    print(f"\n{category}:")
    for h in hyps:
        print(f"  • {h}")
```
