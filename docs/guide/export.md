# Export & Reports

Generate reports and export bibliographies in various formats.

## Setup

```python
from ehdslens import EHDSAnalyzer
from ehdslens.export import ReportGenerator
from pathlib import Path

analyzer = EHDSAnalyzer()
analyzer.load_default_data()

reporter = ReportGenerator(analyzer.db)
```

## Markdown Reports

```python
# Generate report
md_report = reporter.generate_markdown_report()
print(md_report)

# Save to file
reporter.save_markdown_report(Path("ehds_report.md"))
```

## Bibliography Export

### BibTeX

```python
bibtex = reporter.generate_bibliography(format="bibtex")
print(bibtex)

# Save to file
reporter.save_bibliography(Path("references.bib"), format="bibtex")
```

### RIS (EndNote, Zotero)

```python
ris = reporter.generate_bibliography(format="ris")
reporter.save_bibliography(Path("references.ris"), format="ris")
```

### APA Format

```python
apa = reporter.generate_bibliography(format="apa")
print(apa)
```

### Vancouver Format

```python
vancouver = reporter.generate_bibliography(format="vancouver")
print(vancouver)
```

## JSON Export

```python
# Export full dataset
json_data = reporter.export_json()

# Save to file
reporter.save_json(Path("ehds_data.json"))
```

## Data Extraction Template

Generate a template for systematic review data extraction:

```python
template = reporter.generate_data_extraction_template()
print(template)
```

## Filtered Exports

Export only a subset of studies:

```python
from ehdslens.data import StudyDatabase, ThematicAxis

# Filter studies
governance = analyzer.filter_studies(axis=ThematicAxis.GOVERNANCE_RIGHTS_ETHICS)

# Create new database with filtered studies
filtered_db = StudyDatabase()
for study in governance:
    filtered_db.add_study(study)

# Generate bibliography for filtered set
filtered_reporter = ReportGenerator(filtered_db)
bibtex = filtered_reporter.generate_bibliography(format="bibtex")
```

## CLI Export

```bash
# Export BibTeX
ehdslens export --format bibtex -o references.bib

# Export RIS
ehdslens export --format ris -o references.ris

# Generate report
ehdslens report -o report.md
```
