# Analysis API Reference

## ThematicAnalyzer

Performs thematic analysis on studies.

```python
from ehdslens.analysis import ThematicAnalyzer
```

### Methods

#### analyze_axis(studies, axis)

Analyze studies within a thematic axis.

```python
analyzer = ThematicAnalyzer()
result = analyzer.analyze_axis(studies, ThematicAxis.GOVERNANCE_RIGHTS_ETHICS)
```

#### get_coding_framework()

Get the 7-category coding framework.

```python
framework = analyzer.get_coding_framework()
for category, codes in framework.items():
    print(f"{category}: {codes}")
```

## QualityAssessor

Implements MMAT quality assessment.

```python
from ehdslens.analysis import QualityAssessor
```

### Methods

#### assess_study(study)

Assess study quality using MMAT criteria.

```python
assessor = QualityAssessor()
assessment = assessor.assess_study(study)
```

#### get_mmat_criteria()

Get MMAT assessment criteria.

```python
criteria = assessor.get_mmat_criteria()
```

## GRADECERQual

Implements GRADE-CERQual confidence assessment.

```python
from ehdslens.analysis import GRADECERQual
```

### CERQualAssessment

Dataclass representing an assessment.

```python
from ehdslens.analysis import CERQualAssessment

assessment = CERQualAssessment(
    finding="Finding statement",
    confidence=ConfidenceLevel.HIGH,
    num_studies=15,
    methodological_limitations="Minor concerns",
    coherence="High coherence",
    adequacy="Rich data",
    relevance="Directly relevant"
)
```

### Methods

#### get_ehds_assessments()

Get pre-configured EHDS assessments.

```python
grade = GRADECERQual()
assessments = grade.get_ehds_assessments()

for a in assessments:
    print(f"[{a.confidence.value}] {a.finding}")
```

#### create_summary_table()

Generate summary table data.

```python
table = grade.create_summary_table()
```
