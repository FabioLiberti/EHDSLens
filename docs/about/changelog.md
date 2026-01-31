# Changelog

All notable changes to EHDSLens are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-31

### Added

- Initial release of EHDSLens
- **Core Features:**
  - `EHDSAnalyzer` main interface class
  - `StudyDatabase` with 52 EHDS studies
  - `Study` dataclass with full metadata
  - Search and filter functionality
  - Statistics generation

- **Analysis Module:**
  - `ThematicAnalyzer` for axis-based analysis
  - `QualityAssessor` with MMAT implementation
  - `GRADECERQual` confidence assessment

- **Visualization Module:**
  - PRISMA flow diagram data
  - Year/axis/quality distribution charts
  - ASCII, data, and Plotly output formats

- **Export Module:**
  - Markdown report generation
  - Bibliography export (BibTeX, RIS, APA, Vancouver)
  - JSON data export
  - Data extraction templates

- **Command Line Interface:**
  - `stats` - Database statistics
  - `analyze` - Thematic analysis
  - `search` - Study search
  - `report` - Report generation
  - `export` - Bibliography export
  - `grade` - GRADE-CERQual findings
  - `hypotheses` - Testable hypotheses
  - `prisma` - PRISMA diagram data

- **Documentation:**
  - Full API reference
  - User guides
  - Methodology documentation
  - Jupyter notebook examples

- **Infrastructure:**
  - GitHub Actions CI/CD
  - MkDocs documentation site
  - PyPI package distribution
  - Comprehensive test suite

### Data

- 52 studies from EHDS systematic review
- 5 thematic axes
- MMAT quality assessments
- GRADE-CERQual confidence ratings
- Testable hypotheses
- Research gaps

## [Unreleased]

### Planned

- Interactive dashboard
- Network analysis visualization
- Study comparison tools
- Extended export formats
- Multi-language support
