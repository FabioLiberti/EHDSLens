# Export API Reference

## ReportGenerator

Generate reports and bibliographies.

```python
from ehdslens.export import ReportGenerator
```

### Constructor

```python
reporter = ReportGenerator(database: StudyDatabase)
```

### Report Methods

#### generate_markdown_report()

Generate comprehensive Markdown report.

**Returns:** Markdown string

```python
md = reporter.generate_markdown_report()
```

#### save_markdown_report(path)

Save Markdown report to file.

```python
from pathlib import Path
reporter.save_markdown_report(Path("report.md"))
```

### Bibliography Methods

#### generate_bibliography(format)

Generate bibliography in specified format.

**Parameters:**
- `format`: "bibtex", "ris", "apa", or "vancouver"

**Returns:** Formatted bibliography string

```python
bibtex = reporter.generate_bibliography(format="bibtex")
ris = reporter.generate_bibliography(format="ris")
apa = reporter.generate_bibliography(format="apa")
vancouver = reporter.generate_bibliography(format="vancouver")
```

#### save_bibliography(path, format)

Save bibliography to file.

```python
reporter.save_bibliography(Path("refs.bib"), format="bibtex")
reporter.save_bibliography(Path("refs.ris"), format="ris")
```

### JSON Export

#### export_json()

Export full dataset as JSON.

**Returns:** JSON string

```python
json_str = reporter.export_json()
```

#### save_json(path)

Save JSON to file.

```python
reporter.save_json(Path("data.json"))
```

### Templates

#### generate_data_extraction_template()

Generate data extraction template for systematic reviews.

**Returns:** Template string

```python
template = reporter.generate_data_extraction_template()
```

### Bibliography Formats

#### BibTeX

```bibtex
@article{liberti2025ehds,
  author = {Liberti, Fabio},
  title = {European Health Data Space...},
  journal = {Journal Name},
  year = {2025},
  doi = {10.xxxx/xxxxx}
}
```

#### RIS

```
TY  - JOUR
AU  - Liberti, Fabio
TI  - European Health Data Space...
JO  - Journal Name
PY  - 2025
DO  - 10.xxxx/xxxxx
ER  -
```

#### APA

```
Liberti, F. (2025). European Health Data Space... Journal Name.
```

#### Vancouver

```
1. Liberti F. European Health Data Space... Journal Name. 2025.
```
