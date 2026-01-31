# Changelog

All notable changes to EHDSLens will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-31

### Added

- Initial release of EHDSLens
- Complete database of 52 studies from EHDS systematic review
- Core analysis functionality:
  - `EHDSAnalyzer` main class
  - `StudyDatabase` for data management
  - `Study` dataclass with full metadata support
- Thematic analysis module:
  - `ThematicAnalyzer` with seven-category coding framework
  - `QualityAssessor` implementing MMAT criteria
  - `GRADECERQual` confidence assessment
- Visualization module:
  - PRISMA diagram data generation
  - Chart data for year, axis, quality distributions
  - ASCII chart support for terminal output
  - Export for Plotly and LaTeX
- Export module:
  - Markdown, HTML, JSON report generation
  - BibTeX, RIS, APA, Vancouver bibliography formats
  - CSV and JSON data exports
  - Data extraction template generation
- Command line interface:
  - `ehdslens stats` - database statistics
  - `ehdslens analyze` - thematic analysis
  - `ehdslens search` - study search
  - `ehdslens report` - report generation
  - `ehdslens export` - data export
  - `ehdslens grade` - GRADE-CERQual summary
  - `ehdslens hypotheses` - testable hypotheses
  - `ehdslens prisma` - PRISMA flow statistics
- Comprehensive test suite
- Full documentation with examples

### Research Content

- 52 studies included (38 peer-reviewed, 14 grey literature)
- 5 thematic axes analyzed
- GRADE-CERQual assessments for all major findings
- 12 testable hypotheses for future research
- 6 identified research gaps

## [Unreleased]

### Planned

- Interactive web dashboard
- Integration with reference managers (Zotero, Mendeley)
- Automatic literature update checking
- Machine learning-based study classification
- Multi-language support

---

[1.0.0]: https://github.com/FabioLiberti/EHDSLens/releases/tag/v1.0.0
