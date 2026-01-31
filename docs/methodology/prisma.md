# PRISMA 2020 Methodology

The systematic review follows the PRISMA 2020 guidelines for transparent reporting.

## Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      IDENTIFICATION                          │
├─────────────────────────────────────────────────────────────┤
│  Records from databases (n=847)                              │
│  ├── Web of Science: 312                                     │
│  ├── Scopus: 289                                             │
│  ├── PubMed: 156                                             │
│  └── IEEE Xplore: 90                                         │
│                                                              │
│  Grey literature (n=45)                                      │
│  ├── EU publications                                         │
│  ├── WHO reports                                             │
│  └── Policy documents                                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       SCREENING                              │
├─────────────────────────────────────────────────────────────┤
│  Duplicates removed (n=234)                                  │
│  Records screened (n=658)                                    │
│  Records excluded (n=523)                                    │
│  ├── Not EHDS-focused: 312                                   │
│  ├── Wrong study type: 145                                   │
│  └── Not English: 66                                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      ELIGIBILITY                             │
├─────────────────────────────────────────────────────────────┤
│  Full-text assessed (n=135)                                  │
│  Excluded (n=83)                                             │
│  ├── Insufficient EHDS focus: 45                             │
│  ├── Duplicate content: 23                                   │
│  └── Quality concerns: 15                                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       INCLUDED                               │
├─────────────────────────────────────────────────────────────┤
│  Studies in review (n=52)                                    │
│  ├── Peer-reviewed articles: 46                              │
│  └── Grey literature: 6                                      │
└─────────────────────────────────────────────────────────────┘
```

## Search Strategy

### Databases Searched

1. **Web of Science** - Core Collection
2. **Scopus** - All fields
3. **PubMed** - Title/Abstract
4. **IEEE Xplore** - Full text

### Search Terms

```
("European Health Data Space" OR "EHDS" OR
 "EU health data" OR "Regulation 2025/327")
AND
("implementation" OR "governance" OR "privacy" OR
 "secondary use" OR "federated learning" OR "interoperability")
```

### Date Range

January 2020 - May 2025

### Language

English only

## Eligibility Criteria

### Inclusion Criteria

1. Focus on EHDS or EU health data governance
2. Published 2020-2025
3. Peer-reviewed or official policy document
4. Available in English
5. Addresses implementation, governance, or technology aspects

### Exclusion Criteria

1. Editorial/commentary without original analysis
2. Conference abstracts only
3. Non-EU focused studies
4. Technical specifications without policy analysis

## Access PRISMA Data

```python
from ehdslens.visualization import EHDSVisualizer

viz = EHDSVisualizer(analyzer.db)
prisma = viz.create_prisma_diagram_data()

print(f"Identified: {prisma['identification']['total_database']}")
print(f"Screened: {prisma['screening']['records_screened']}")
print(f"Included: {prisma['included']['total']}")
```

## References

Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ. 2021;372:n71.
