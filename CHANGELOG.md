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

## [1.1.0] - 2026-01-31

### Added

- **Interactive Dashboard** (`ehdslens dashboard`):
  - Streamlit-based web application
  - Real-time filtering by year, axis, and quality
  - Interactive Plotly charts and visualizations
  - Study browser with search functionality
  - GRADE-CERQual findings explorer
  - Export to CSV functionality

- **REST API** (`ehdslens api`):
  - FastAPI-based REST API server
  - Full OpenAPI documentation at `/docs`
  - ReDoc documentation at `/redoc`
  - Endpoints for all analysis features:
    - `GET /statistics` - Database statistics
    - `GET /studies` - List/filter studies
    - `GET /studies/{id}` - Get study by ID
    - `GET /search` - Search studies
    - `GET /analysis/axes/{axis}` - Thematic analysis
    - `GET /grade-cerqual` - GRADE-CERQual findings
    - `GET /research-gaps` - Research gaps
    - `GET /hypotheses` - Testable hypotheses
    - `GET /prisma` - PRISMA diagram data
    - `GET /export/bibliography` - Export bibliography

- New optional dependencies:
  - `ehdslens[dashboard]` - Streamlit dashboard
  - `ehdslens[api]` - FastAPI REST API

- New CLI commands:
  - `ehdslens dashboard` - Launch interactive dashboard
  - `ehdslens api` - Start REST API server

### Changed

- Updated version to 1.1.0
- Enhanced CLI with dashboard and API commands

## [Unreleased]

### Planned

- Integration with reference managers (Zotero, Mendeley)
- Automatic literature update checking
- Machine learning-based study classification
- Multi-language support
- Docker containerization

---

[1.1.0]: https://github.com/FabioLiberti/EHDSLens/releases/tag/v1.1.0
[1.0.0]: https://github.com/FabioLiberti/EHDSLens/releases/tag/v1.0.0
