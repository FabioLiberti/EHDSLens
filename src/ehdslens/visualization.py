"""
Visualization module for EHDS literature analysis.

Provides functions for creating charts, graphs, and visual
representations of systematic review data.
"""

from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
import json

from .data import StudyDatabase, ThematicAxis, QualityRating, StudyType


class EHDSVisualizer:
    """
    Creates visualizations for EHDS systematic review data.

    Supports multiple output formats including:
    - Matplotlib charts (PNG, PDF, SVG)
    - Plotly interactive charts (HTML)
    - Text-based ASCII charts
    - Data exports for external tools
    """

    # Color schemes
    AXIS_COLORS = {
        ThematicAxis.GOVERNANCE_RIGHTS_ETHICS: "#1f77b4",
        ThematicAxis.SECONDARY_USE_PETS: "#ff7f0e",
        ThematicAxis.NATIONAL_IMPLEMENTATION: "#2ca02c",
        ThematicAxis.CITIZEN_ENGAGEMENT: "#d62728",
        ThematicAxis.FEDERATED_LEARNING_AI: "#9467bd"
    }

    QUALITY_COLORS = {
        QualityRating.HIGH: "#28a745",
        QualityRating.MODERATE: "#ffc107",
        QualityRating.LOW: "#dc3545",
        QualityRating.NOT_APPLICABLE: "#6c757d"
    }

    CONFIDENCE_COLORS = {
        "HIGH": "#28a745",
        "MODERATE": "#ffc107",
        "LOW": "#fd7e14",
        "VERY_LOW": "#dc3545"
    }

    def __init__(self, database: StudyDatabase):
        """Initialize visualizer with study database."""
        self.db = database

    def create_prisma_diagram_data(self) -> Dict[str, Any]:
        """
        Generate data structure for PRISMA flow diagram.

        Returns:
            Dictionary with node and edge data for diagram creation.
        """
        return {
            "identification": {
                "databases": [
                    {"name": "PubMed", "records": 187},
                    {"name": "IEEE Xplore", "records": 89},
                    {"name": "Scopus", "records": 156},
                    {"name": "Web of Science", "records": 124},
                    {"name": "ScienceDirect", "records": 98},
                    {"name": "Springer Nature", "records": 112},
                    {"name": "Frontiers", "records": 45},
                    {"name": "arXiv", "records": 36}
                ],
                "total_database": 847,
                "grey_literature": 44,
                "total": 891
            },
            "screening": {
                "after_duplicates": 691,
                "duplicates_removed": 156,
                "title_abstract_excluded": 567,
                "to_full_text": 124
            },
            "eligibility": {
                "full_text_assessed": 124,
                "excluded": {
                    "insufficient_focus": 28,
                    "methodological": 19,
                    "duplicate_superseded": 14,
                    "language": 7,
                    "abstract_only": 4
                },
                "total_excluded": 72
            },
            "included": {
                "peer_reviewed": 38,
                "grey_literature": 14,
                "total": 52
            }
        }

    def create_year_distribution_chart(
        self,
        output_path: Optional[Path] = None,
        format: str = "data"
    ) -> Dict[str, Any]:
        """
        Create publication year distribution chart.

        Args:
            output_path: Path to save chart (if applicable)
            format: Output format ("data", "matplotlib", "plotly", "ascii")

        Returns:
            Chart data or path to saved file
        """
        stats = self.db.get_statistics()
        year_data = stats.get("by_year", {})

        if format == "ascii":
            return self._ascii_bar_chart(year_data, "Publication Year Distribution")

        return {
            "title": "Publication Year Distribution",
            "x_label": "Year",
            "y_label": "Number of Studies",
            "data": year_data,
            "annotations": {
                2024: "Political agreement (March 2024)",
                2025: "Formal adoption (January 2025)"
            }
        }

    def create_axis_distribution_chart(
        self,
        output_path: Optional[Path] = None,
        format: str = "data"
    ) -> Dict[str, Any]:
        """
        Create thematic axis distribution chart.

        Args:
            output_path: Path to save chart
            format: Output format

        Returns:
            Chart data
        """
        stats = self.db.get_statistics()
        axis_data = stats.get("by_axis", {})

        # Format axis names for display
        display_names = {
            "governance_rights_ethics": "Governance, Rights, Ethics",
            "secondary_use_pets": "Secondary Use & PETs",
            "national_implementation": "National Implementation",
            "citizen_engagement": "Citizen Engagement",
            "federated_learning_ai": "Federated Learning & AI"
        }

        formatted_data = {display_names.get(k, k): v for k, v in axis_data.items()}

        if format == "ascii":
            return self._ascii_bar_chart(formatted_data, "Distribution by Thematic Axis")

        return {
            "title": "Distribution by Thematic Axis",
            "type": "pie",
            "data": formatted_data,
            "colors": [self.AXIS_COLORS.get(ThematicAxis(k), "#333")
                       for k in axis_data.keys()]
        }

    def create_quality_distribution_chart(
        self,
        output_path: Optional[Path] = None,
        format: str = "data"
    ) -> Dict[str, Any]:
        """
        Create quality rating distribution chart.

        Returns:
            Chart data for quality distribution
        """
        stats = self.db.get_statistics()
        quality_data = stats.get("by_quality", {})

        # Order by rating level
        ordered = {
            "High": quality_data.get("high", 0),
            "Moderate": quality_data.get("moderate", 0),
            "Low": quality_data.get("low", 0)
        }

        if format == "ascii":
            return self._ascii_bar_chart(ordered, "Quality Rating Distribution")

        return {
            "title": "Quality Rating Distribution (MMAT)",
            "type": "bar",
            "data": ordered,
            "colors": ["#28a745", "#ffc107", "#dc3545"]
        }

    def create_country_map_data(self) -> Dict[str, Any]:
        """
        Create data for geographic distribution map.

        Returns:
            Dictionary with country codes and study counts
        """
        stats = self.db.get_statistics()
        country_data = stats.get("by_country", {})

        # Map to ISO codes for mapping libraries
        iso_mapping = {
            "Netherlands": "NLD",
            "Germany": "DEU",
            "UK": "GBR",
            "Denmark": "DNK",
            "Belgium": "BEL",
            "Sweden": "SWE",
            "Norway": "NOR",
            "Finland": "FIN",
            "Estonia": "EST",
            "Ireland": "IRL",
            "Spain": "ESP",
            "Italy": "ITA",
            "USA": "USA",
            "Australia": "AUS",
            "Canada": "CAN",
            "Switzerland": "CHE",
            "Malaysia": "MYS",
            "EU": "EU"
        }

        return {
            "title": "Geographic Distribution of Studies",
            "data": {iso_mapping.get(k, k): v for k, v in country_data.items()},
            "original_names": country_data
        }

    def create_grade_cerqual_table(self) -> str:
        """
        Create formatted GRADE-CERQual summary table.

        Returns:
            Formatted table as string
        """
        from .analysis import GRADECERQual

        gc = GRADECERQual(self.db)
        assessments = gc.get_ehds_assessments()

        # Create table header
        header = "| Finding | Studies | Meth.Lim | Coherence | Adequacy | Confidence |"
        separator = "|---------|---------|----------|-----------|----------|------------|"

        rows = []
        for a in assessments:
            # Truncate finding for display
            finding_short = a.finding[:50] + "..." if len(a.finding) > 50 else a.finding
            rows.append(
                f"| {finding_short} | n={len(a.supporting_studies)} | "
                f"{a.methodological_limitations} | {a.coherence} | "
                f"{a.adequacy} | **{a.overall_confidence.value.upper()}** |"
            )

        return "\n".join([header, separator] + rows)

    def create_study_type_chart(self) -> Dict[str, Any]:
        """
        Create study type distribution chart.

        Returns:
            Chart data for study methodology types
        """
        stats = self.db.get_statistics()
        type_data = stats.get("by_type", {})

        display_names = {
            "qualitative": "Qualitative",
            "quantitative": "Quantitative",
            "mixed_methods": "Mixed Methods",
            "conceptual": "Conceptual/Analytical",
            "systematic_review": "Systematic Review",
            "policy_document": "Policy Document",
            "technical": "Technical"
        }

        formatted = {display_names.get(k, k): v for k, v in type_data.items()}

        return {
            "title": "Distribution by Study Type",
            "type": "horizontal_bar",
            "data": formatted
        }

    def _ascii_bar_chart(
        self,
        data: Dict[str, int],
        title: str,
        max_width: int = 40
    ) -> str:
        """
        Create simple ASCII bar chart.

        Args:
            data: Dictionary of labels to values
            title: Chart title
            max_width: Maximum bar width in characters

        Returns:
            ASCII chart as string
        """
        if not data:
            return f"{title}\n(No data)"

        max_val = max(data.values())
        max_label = max(len(str(k)) for k in data.keys())

        lines = [f"\n{title}", "=" * (max_label + max_width + 10)]

        for label, value in data.items():
            bar_len = int((value / max_val) * max_width) if max_val > 0 else 0
            bar = "█" * bar_len
            lines.append(f"{str(label):>{max_label}} | {bar} {value}")

        lines.append("=" * (max_label + max_width + 10))
        return "\n".join(lines)

    def export_for_plotly(self, output_path: Path) -> None:
        """
        Export all chart data in Plotly-compatible JSON format.

        Args:
            output_path: Path to save JSON file
        """
        export_data = {
            "year_distribution": self.create_year_distribution_chart(),
            "axis_distribution": self.create_axis_distribution_chart(),
            "quality_distribution": self.create_quality_distribution_chart(),
            "country_map": self.create_country_map_data(),
            "study_type": self.create_study_type_chart(),
            "prisma": self.create_prisma_diagram_data()
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)

    def export_for_latex(self, output_path: Path) -> None:
        """
        Export data in LaTeX table format.

        Args:
            output_path: Path to save LaTeX file
        """
        stats = self.db.get_statistics()

        latex = []
        latex.append("% EHDS Systematic Review Tables")
        latex.append("% Generated by EHDSLens\n")

        # Study characteristics table
        latex.append("\\begin{table}[htbp]")
        latex.append("\\centering")
        latex.append("\\caption{Characteristics of Included Studies by Thematic Focus}")
        latex.append("\\begin{tabular}{lcccc}")
        latex.append("\\hline")
        latex.append("Thematic Axis & Peer-reviewed & Grey lit. & Total & Quality H/M/L \\\\")
        latex.append("\\hline")

        axis_names = {
            "governance_rights_ethics": "Governance, Rights, Ethics",
            "secondary_use_pets": "Secondary Use \\& PETs",
            "national_implementation": "National Implementation",
            "citizen_engagement": "Citizen Engagement",
            "federated_learning_ai": "Federated Learning \\& AI"
        }

        for axis in ThematicAxis:
            studies = self.db.filter_by_axis(axis)
            peer = len([s for s in studies if s.study_type != StudyType.POLICY_DOCUMENT])
            grey = len([s for s in studies if s.study_type == StudyType.POLICY_DOCUMENT])
            total = len(studies)
            high = len([s for s in studies if s.quality_rating == QualityRating.HIGH])
            mod = len([s for s in studies if s.quality_rating == QualityRating.MODERATE])
            low = len([s for s in studies if s.quality_rating == QualityRating.LOW])

            name = axis_names.get(axis.value, axis.value)
            latex.append(f"{name} & {peer} & {grey} & {total} & {high}/{mod}/{low} \\\\")

        latex.append("\\hline")
        latex.append("\\end{tabular}")
        latex.append("\\end{table}")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(latex))
