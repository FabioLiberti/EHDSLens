"""
Report generation and export functionality for EHDS analysis.

Provides tools for creating formatted reports, bibliographies,
and data exports in multiple formats.
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime
import json

from .data import StudyDatabase, Study, ThematicAxis, QualityRating
from .analysis import ThematicAnalyzer, QualityAssessor, GRADECERQual


class ReportGenerator:
    """
    Generates comprehensive reports from EHDS analysis.

    Supports multiple output formats:
    - Markdown (.md)
    - HTML (.html)
    - JSON (.json)
    - BibTeX (.bib)
    - RIS (.ris)
    """

    def __init__(self, database: StudyDatabase):
        """Initialize report generator with study database."""
        self.db = database
        self.thematic = ThematicAnalyzer(database)
        self.quality = QualityAssessor(database)
        self.grade = GRADECERQual(database)

    def generate_full_report(self, output_path: Path, format: str = "markdown") -> None:
        """
        Generate comprehensive analysis report.

        Args:
            output_path: Path to save report
            format: Output format ("markdown", "html", "json")
        """
        if format == "markdown":
            content = self._generate_markdown_report()
        elif format == "html":
            content = self._generate_html_report()
        elif format == "json":
            content = json.dumps(self._generate_json_report(), indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_markdown_report(self) -> str:
        """Generate Markdown-formatted report."""
        stats = self.db.get_statistics()
        quality_summary = self.quality.generate_quality_summary()
        grade_summary = self.grade.generate_summary_table()

        lines = [
            "# EHDS Systematic Literature Review Analysis Report",
            f"\n*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
            f"\n*EHDSLens v1.0.0*\n",

            "## Executive Summary\n",
            f"This report summarizes the analysis of **{stats['total']} studies** "
            f"examining the European Health Data Space (EHDS) from {stats['year_range'][0]} "
            f"to {stats['year_range'][1]}.\n",

            "## Study Selection\n",
            "| Stage | Records |",
            "|-------|---------|",
            "| Records identified | 847 |",
            "| After duplicates | 691 |",
            "| Title/abstract screened | 691 |",
            "| Full-text assessed | 124 |",
            "| **Included in synthesis** | **52** |\n",

            "## Distribution by Thematic Axis\n",
            "| Axis | Studies | Percentage |",
            "|------|---------|------------|",
        ]

        for axis, count in stats.get('by_axis', {}).items():
            pct = count / stats['total'] * 100 if stats['total'] > 0 else 0
            display_name = axis.replace('_', ' ').title()
            lines.append(f"| {display_name} | {count} | {pct:.1f}% |")

        lines.extend([
            "\n## Quality Assessment (MMAT)\n",
            f"- **High quality**: {quality_summary['high']['count']} ({quality_summary['high']['percentage']:.1f}%)",
            f"- **Moderate quality**: {quality_summary['moderate']['count']} ({quality_summary['moderate']['percentage']:.1f}%)",
            f"- **Low quality**: {quality_summary['low']['count']} ({quality_summary['low']['percentage']:.1f}%)\n",

            "## GRADE-CERQual Summary of Findings\n",
            "| Finding | Studies | Confidence |",
            "|---------|---------|------------|",
        ])

        for finding in grade_summary:
            conf_emoji = "🟢" if finding['confidence'] == "HIGH" else "🟡"
            lines.append(f"| {finding['finding'][:60]}... | {finding['studies']} | {conf_emoji} {finding['confidence']} |")

        lines.extend([
            "\n## Key Findings\n",
            "### Axis 1: Governance, Rights, and Ethics",
            "- Persistent tensions between secondary use promotion and rights protection",
            "- Opt-out mechanisms as political compromises with legitimacy concerns",
            "- **Confidence: HIGH**\n",

            "### Axis 2: Secondary Use and PETs",
            "- Significant gaps between data reuse aspirations and PET maturity",
            "- Only 23% of federated learning implementations in production",
            "- **Confidence: MODERATE**\n",

            "### Axis 3: National Implementation",
            "- Nordic countries 2-3 years ahead in HDAB capacity",
            "- Substantial heterogeneity in Member State readiness",
            "- **Confidence: MODERATE**\n",

            "### Axis 4: Citizen Engagement",
            "- Predominantly symbolic rather than substantive engagement",
            "- Only 3/52 studies employed participatory methods",
            "- **Confidence: HIGH**\n",

            "### Axis 5: Federated Learning and AI",
            "- Unresolved legal uncertainties regarding GDPR/EHDS compliance",
            "- Questions about model gradients as personal data",
            "- **Confidence: MODERATE**\n",

            "## Research Gaps Identified\n",
            "1. Empirical citizen attitude studies",
            "2. National-European integration studies",
            "3. Economic sustainability models for HDABs",
            "4. Longitudinal implementation tracking (2025-2031)",
            "5. Interdisciplinary research integration",
            "6. Emerging technology assessment (synthetic data, MPC)\n",

            "## Testable Hypotheses\n",
            "### Governance",
            "- H1a: Pre-existing opt-out frameworks → higher data availability",
            "- H1b: Opt-out rates inversely related to institutional trust\n",

            "### Technology",
            "- H2a: >50% FHIR implementation → faster EHDS compliance",
            "- H2b: FL deployment to increase from 23% to >50% by 2029\n",

            "### Implementation",
            "- H3a: Nordic compliance by 2029; Southern/Eastern by 2031",
            "- H3b: HDAB staffing stronger predictor than infrastructure\n",

            "### Engagement",
            "- H4a: Public awareness to increase from <20% to >50% by 2029",
            "- H4b: Deliberative mechanisms → lower opt-out rates\n",

            "---",
            "*Report generated by EHDSLens - EHDS Literature Analysis Toolkit*"
        ])

        return "\n".join(lines)

    def _generate_html_report(self) -> str:
        """Generate HTML-formatted report."""
        md_content = self._generate_markdown_report()

        # Simple markdown to HTML conversion
        html = md_content
        html = html.replace("# ", "<h1>").replace("\n## ", "</h1>\n<h2>")
        html = html.replace("### ", "</h2>\n<h3>")
        html = html.replace("**", "<strong>").replace("</strong><strong>", "")
        html = html.replace("*", "<em>").replace("</em><em>", "")

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EHDS Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #1F4E79; border-bottom: 2px solid #1F4E79; }}
        h2 {{ color: #2E75B6; }}
        table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #1F4E79; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .high {{ color: #28a745; font-weight: bold; }}
        .moderate {{ color: #ffc107; font-weight: bold; }}
    </style>
</head>
<body>
{html}
</body>
</html>"""

    def _generate_json_report(self) -> Dict[str, Any]:
        """Generate JSON-formatted report data."""
        return {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "tool": "EHDSLens v1.0.0",
                "description": "EHDS Systematic Literature Review Analysis"
            },
            "statistics": self.db.get_statistics(),
            "quality_summary": self.quality.generate_quality_summary(),
            "grade_cerqual": self.grade.generate_summary_table(),
            "studies": [s.to_dict() for s in self.db.studies],
            "thematic_analysis": self.thematic.analyze_all_axes()
        }

    def generate_bibliography(
        self,
        output_path: Path,
        format: str = "bibtex",
        style: str = "apa"
    ) -> None:
        """
        Generate bibliography in specified format.

        Args:
            output_path: Path to save bibliography
            format: Output format ("bibtex", "ris", "apa", "vancouver")
            style: Citation style for text formats
        """
        if format == "bibtex":
            content = self._generate_bibtex()
        elif format == "ris":
            content = self._generate_ris()
        elif format in ["apa", "vancouver"]:
            content = self._generate_text_bibliography(style=format)
        else:
            raise ValueError(f"Unsupported format: {format}")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_bibtex(self) -> str:
        """Generate BibTeX bibliography."""
        entries = []

        for study in self.db.studies:
            # Create citation key
            first_author = study.authors.split(',')[0].split(' ')[-1].lower()
            key = f"{first_author}{study.year}"

            entry_type = "article"
            if study.study_type.value == "policy_document":
                entry_type = "techreport"

            entry = [
                f"@{entry_type}{{{key},",
                f"  author = {{{study.authors}}},",
                f"  title = {{{study.title}}},",
                f"  journal = {{{study.journal}}},",
                f"  year = {{{study.year}}},"
            ]

            if study.doi:
                entry.append(f"  doi = {{{study.doi}}},")

            entry.append("}")
            entries.append("\n".join(entry))

        header = "% EHDS Systematic Review Bibliography\n% Generated by EHDSLens\n\n"
        return header + "\n\n".join(entries)

    def _generate_ris(self) -> str:
        """Generate RIS bibliography."""
        entries = []

        for study in self.db.studies:
            entry = [
                "TY  - JOUR",
                f"AU  - {study.authors}",
                f"TI  - {study.title}",
                f"JO  - {study.journal}",
                f"PY  - {study.year}"
            ]

            if study.doi:
                entry.append(f"DO  - {study.doi}")

            entry.append("ER  - ")
            entries.append("\n".join(entry))

        return "\n\n".join(entries)

    def _generate_text_bibliography(self, style: str = "apa") -> str:
        """Generate text bibliography in specified style."""
        citations = []

        for i, study in enumerate(sorted(self.db.studies, key=lambda s: (s.year, s.authors)), 1):
            citation = f"[{i}] {study.get_citation(style)}"
            citations.append(citation)

        header = f"# EHDS Systematic Review Bibliography ({style.upper()} Style)\n\n"
        return header + "\n\n".join(citations)

    def generate_data_extraction_template(self, output_path: Path) -> None:
        """
        Generate data extraction form template.

        Args:
            output_path: Path to save template
        """
        template = """# EHDS Study Data Extraction Form

## Bibliographic Information
- **Study ID**: [Numeric identifier]
- **First Author**: [Last name]
- **Publication Year**: [YYYY]
- **Title**: [Full title]
- **Journal/Source**: [Journal name or source type]
- **DOI**: [If available]
- **Country**: [Country of first author]

## Study Characteristics
- **Study Design**: [ ] Qualitative [ ] Quantitative [ ] Mixed Methods [ ] Conceptual [ ] Review [ ] Policy
- **Methodology**: [Specific method]
- **Sample/Data Sources**: [Description]
- **Sample Size**: [n, if applicable]
- **Theoretical Framework**: [If stated]

## EHDS Focus
- **Primary Use Focus**: [ ] Yes [ ] No
- **Secondary Use Focus**: [ ] Yes [ ] No
- **EHDS Articles Referenced**: [List]
- **Geographic Scope**: [ ] EU-wide [ ] Specific MS [ ] Comparative

## Thematic Content
Primary Axis (select one):
- [ ] 1. Governance, Rights, Ethics
- [ ] 2. Secondary Use & PETs
- [ ] 3. National Implementation
- [ ] 4. Citizen Engagement
- [ ] 5. Federated Learning & AI

Secondary Themes (select all that apply):
- [ ] Rights and autonomy
- [ ] Governance and institutions
- [ ] Technical infrastructure
- [ ] Data quality and interoperability
- [ ] Equity and inclusion
- [ ] Public engagement
- [ ] Sectoral impacts

## Key Findings
- **Main Findings**: [Summary, max 200 words]
- **Recommendations**: [If provided]
- **Limitations Acknowledged**: [ ] Yes [ ] No

## Quality Assessment (MMAT)
- **Criteria Met**: [Number out of 5]
- **Quality Rating**: [ ] High [ ] Moderate [ ] Low
- **Reviewer Notes**: [Free text]

---
*Template generated by EHDSLens*
"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(template)

    def export_study_table(
        self,
        output_path: Path,
        format: str = "csv",
        columns: Optional[List[str]] = None
    ) -> None:
        """
        Export study data as table.

        Args:
            output_path: Path to save table
            format: Output format ("csv", "tsv", "xlsx")
            columns: Columns to include (default: all)
        """
        if format == "csv":
            self.db.to_csv(output_path)
        elif format == "tsv":
            import csv
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='\t')
                if self.db.studies:
                    writer.writerow(list(self.db.studies[0].to_dict().keys()))
                    for study in self.db.studies:
                        row = list(study.to_dict().values())
                        writer.writerow(row)
        else:
            # For xlsx, use pandas if available
            try:
                import pandas as pd
                data = [s.to_dict() for s in self.db.studies]
                df = pd.DataFrame(data)
                if columns:
                    df = df[columns]
                df.to_excel(output_path, index=False)
            except ImportError:
                raise RuntimeError("pandas required for xlsx export")
