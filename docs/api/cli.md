# CLI Reference

EHDSLens provides a command-line interface for quick analysis.

## Installation

The CLI is automatically installed with the package:

```bash
pip install ehdslens
```

## Commands

### stats

Display database statistics.

```bash
ehdslens stats
```

Output includes:
- Total studies
- Year range
- Studies by thematic axis
- Studies by quality rating
- Studies by type

### analyze

Analyze a specific thematic axis.

```bash
ehdslens analyze <axis>
```

**Arguments:**
- `axis`: One of `governance`, `pets`, `implementation`, `engagement`, `federated`

**Examples:**

```bash
ehdslens analyze governance
ehdslens analyze pets
ehdslens analyze federated
```

### search

Search studies by keyword.

```bash
ehdslens search <query>
```

**Arguments:**
- `query`: Search term (searches authors, titles, journals)

**Examples:**

```bash
ehdslens search "privacy"
ehdslens search "federated learning"
ehdslens search "GDPR"
```

### report

Generate a Markdown report.

```bash
ehdslens report [-o OUTPUT]
```

**Options:**
- `-o, --output`: Output file path (default: stdout)

**Examples:**

```bash
ehdslens report
ehdslens report -o ehds_report.md
```

### export

Export bibliography.

```bash
ehdslens export --format FORMAT [-o OUTPUT]
```

**Options:**
- `--format`: One of `bibtex`, `ris`, `apa`, `vancouver`
- `-o, --output`: Output file path (default: stdout)

**Examples:**

```bash
ehdslens export --format bibtex
ehdslens export --format bibtex -o references.bib
ehdslens export --format ris -o references.ris
ehdslens export --format apa
```

### grade

Display GRADE-CERQual findings.

```bash
ehdslens grade
```

Shows confidence assessments for key findings.

### hypotheses

Display testable hypotheses.

```bash
ehdslens hypotheses
```

Shows hypotheses organized by category.

### prisma

Display PRISMA flow diagram data.

```bash
ehdslens prisma
```

Shows identification, screening, eligibility, and inclusion counts.

## Global Options

### --version

Show version number.

```bash
ehdslens --version
```

### --help

Show help message.

```bash
ehdslens --help
ehdslens analyze --help
```

## Examples

```bash
# Quick overview
ehdslens stats

# Find privacy-related studies
ehdslens search "privacy"

# Analyze federated learning axis
ehdslens analyze federated

# Export bibliography for reference manager
ehdslens export --format bibtex -o refs.bib

# Generate report
ehdslens report -o analysis.md

# View confidence assessments
ehdslens grade
```
