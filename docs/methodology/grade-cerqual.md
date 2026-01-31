# GRADE-CERQual Methodology

GRADE-CERQual (Confidence in the Evidence from Reviews of Qualitative Research) is used to assess confidence in review findings.

## Overview

GRADE-CERQual assesses how much confidence to place in findings from qualitative evidence syntheses. It evaluates four components:

1. **Methodological limitations**
2. **Coherence**
3. **Adequacy of data**
4. **Relevance**

## Confidence Levels

| Level | Definition |
|-------|------------|
| **High** | Highly likely that the review finding is a reasonable representation of the phenomenon of interest |
| **Moderate** | Likely that the review finding is a reasonable representation |
| **Low** | Possible that the review finding is a reasonable representation |
| **Very Low** | Not clear whether the review finding is a reasonable representation |

## Assessment Components

### 1. Methodological Limitations

Concerns about the design or conduct of the primary studies:

- Study design appropriateness
- Data collection methods
- Analysis rigor
- Researcher reflexivity

### 2. Coherence

How well the review finding is supported by the data:

- Consistency across studies
- Pattern clarity
- Explanation of variations
- Fit between data and interpretation

### 3. Adequacy of Data

Richness and quantity of data supporting the finding:

- Number of studies
- Depth of data
- Breadth of contexts
- Saturation indicators

### 4. Relevance

Applicability of the data to the review question:

- Context alignment
- Population match
- Phenomenon relevance
- Setting appropriateness

## EHDS Review Findings

### High Confidence Findings

- **Data governance frameworks are essential** (n=18 studies)
  - Strong methodological quality
  - High coherence across contexts
  - Rich, saturated data

- **Privacy concerns require technical solutions** (n=15 studies)
  - Consistent evidence
  - Multiple country contexts
  - Adequate data depth

### Moderate Confidence Findings

- **National implementation varies significantly** (n=12 studies)
  - Some methodological concerns
  - Good coherence
  - Adequate relevance

- **Citizen trust depends on transparency** (n=10 studies)
  - Minor limitations
  - Moderate data adequacy

### Low Confidence Findings

- **Federated learning adoption faces barriers** (n=8 studies)
  - Limited study count
  - Emerging evidence base
  - Technical focus

## Access CERQual Data

```python
from ehdslens import EHDSAnalyzer

analyzer = EHDSAnalyzer()
analyzer.load_default_data()

findings = analyzer.get_grade_cerqual_summary()

for f in findings:
    print(f"[{f['confidence'].upper()}]")
    print(f"  Finding: {f['finding']}")
    print(f"  Studies: n={f['studies']}")
```

## References

Lewin S, Booth A, Glenton C, et al. Applying GRADE-CERQual to qualitative evidence synthesis findings: introduction to the series. Implementation Science. 2018;13(Suppl 1):2.
