# Thematic Analysis Methodology

The systematic review employs a deductive-inductive thematic analysis approach organized around five thematic axes.

## Five Thematic Axes

### 1. Governance, Rights & Ethics

**Focus:** Data governance frameworks, patient rights, ethical considerations

**Key Themes:**
- GDPR alignment and harmonization
- Patient consent mechanisms
- Data altruism frameworks
- Ethical oversight structures
- Rights to access and portability

**Studies:** ~15 papers addressing governance frameworks

### 2. Secondary Use & PETs

**Focus:** Privacy-enhancing technologies, anonymization, data access

**Key Themes:**
- Anonymization techniques
- Differential privacy
- Secure multi-party computation
- Data access bodies
- Permit systems

**Studies:** ~12 papers on technical privacy solutions

### 3. National Implementation

**Focus:** Member state transposition, regulatory challenges

**Key Themes:**
- Transposition timelines
- Institutional readiness
- Resource allocation
- Cross-border coordination
- Legacy system integration

**Studies:** ~10 papers on implementation challenges

### 4. Citizen Engagement

**Focus:** Public trust, participation, health literacy

**Key Themes:**
- Trust building mechanisms
- Public consultation processes
- Health data literacy
- Participation models
- Communication strategies

**Studies:** ~8 papers on citizen perspectives

### 5. Federated Learning & AI

**Focus:** Distributed analytics, AI governance, interoperability

**Key Themes:**
- Federated learning architectures
- AI model governance
- Interoperability standards
- HL7 FHIR implementation
- Algorithm transparency

**Studies:** ~7 papers on technical infrastructure

## Coding Framework

The review uses a 7-category coding framework:

| Category | Description |
|----------|-------------|
| **Governance** | Regulatory frameworks, oversight |
| **Technical** | Technologies, infrastructure |
| **Ethical** | Rights, consent, fairness |
| **Implementation** | Practical challenges |
| **Stakeholder** | Actors, interests |
| **Outcome** | Impacts, benefits |
| **Context** | Setting, conditions |

## Analysis Process

### Phase 1: Familiarization
- Full-text reading
- Initial observations
- Data extraction

### Phase 2: Initial Coding
- Deductive codes from framework
- Inductive codes from data
- Code refinement

### Phase 3: Theme Development
- Code clustering
- Theme identification
- Axis assignment

### Phase 4: Review & Refinement
- Theme coherence check
- Cross-axis connections
- Final synthesis

## Access Thematic Analysis

```python
from ehdslens import EHDSAnalyzer
from ehdslens.data import ThematicAxis

analyzer = EHDSAnalyzer()
analyzer.load_default_data()

# Analyze specific axis
analysis = analyzer.analyze_axis(ThematicAxis.GOVERNANCE_RIGHTS_ETHICS)

print(f"Studies: {analysis['total_studies']}")
print(f"Themes: {analysis['themes']}")
```

## References

Braun V, Clarke V. Using thematic analysis in psychology. Qualitative Research in Psychology. 2006;3(2):77-101.
