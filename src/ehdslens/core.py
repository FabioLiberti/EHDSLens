"""
Core EHDSLens analyzer - main entry point for EHDS literature analysis.

Provides a unified interface for loading data, performing analysis,
and generating outputs.
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
import json

from .data import StudyDatabase, Study, ThematicAxis, QualityRating, load_ehds_studies
from .analysis import ThematicAnalyzer, QualityAssessor, GRADECERQual


class EHDSAnalyzer:
    """
    Main analyzer class for EHDS systematic literature review.

    Provides high-level interface for:
    - Loading and managing study data
    - Performing thematic analysis
    - Quality assessment
    - GRADE-CERQual confidence evaluation
    - Generating reports and exports

    Example:
        >>> analyzer = EHDSAnalyzer()
        >>> analyzer.load_default_data()
        >>> stats = analyzer.get_statistics()
        >>> print(f"Total studies: {stats['total']}")
    """

    def __init__(self, database: Optional[StudyDatabase] = None):
        """
        Initialize the analyzer.

        Args:
            database: Optional pre-populated StudyDatabase.
                      If None, creates empty database.
        """
        self.db = database or StudyDatabase()
        self._thematic_analyzer: Optional[ThematicAnalyzer] = None
        self._quality_assessor: Optional[QualityAssessor] = None
        self._grade_cerqual: Optional[GRADECERQual] = None

    def load_default_data(self) -> None:
        """Load the 52 studies from the EHDS systematic review."""
        self.db = load_ehds_studies()
        self._reset_analyzers()

    def load_from_json(self, filepath: Path) -> None:
        """Load study data from JSON file."""
        self.db.from_json(filepath)
        self._reset_analyzers()

    def load_from_csv(self, filepath: Path) -> None:
        """Load study data from CSV file."""
        import csv
        from .data import StudyType

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                study = Study(
                    id=int(row['id']),
                    authors=row['authors'],
                    year=int(row['year']),
                    title=row['title'],
                    journal=row['journal'],
                    study_type=StudyType(row['study_type']),
                    primary_axis=ThematicAxis(row['primary_axis']),
                    quality_rating=QualityRating(row.get('quality_rating', 'n/a')),
                    doi=row.get('doi'),
                    country=row.get('country')
                )
                self.db.add_study(study)
        self._reset_analyzers()

    def _reset_analyzers(self) -> None:
        """Reset analyzer instances when data changes."""
        self._thematic_analyzer = None
        self._quality_assessor = None
        self._grade_cerqual = None

    @property
    def thematic_analyzer(self) -> ThematicAnalyzer:
        """Get or create thematic analyzer."""
        if self._thematic_analyzer is None:
            self._thematic_analyzer = ThematicAnalyzer(self.db)
        return self._thematic_analyzer

    @property
    def quality_assessor(self) -> QualityAssessor:
        """Get or create quality assessor."""
        if self._quality_assessor is None:
            self._quality_assessor = QualityAssessor(self.db)
        return self._quality_assessor

    @property
    def grade_cerqual(self) -> GRADECERQual:
        """Get or create GRADE-CERQual assessor."""
        if self._grade_cerqual is None:
            self._grade_cerqual = GRADECERQual(self.db)
        return self._grade_cerqual

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about the study database.

        Returns:
            Dictionary containing:
            - total: Total number of studies
            - by_year: Distribution by publication year
            - by_axis: Distribution by thematic axis
            - by_type: Distribution by study type
            - by_quality: Distribution by quality rating
            - by_country: Distribution by country
        """
        return self.db.get_statistics()

    def analyze_axis(self, axis: ThematicAxis) -> Dict[str, Any]:
        """
        Perform detailed analysis of a thematic axis.

        Args:
            axis: ThematicAxis to analyze

        Returns:
            Dictionary with analysis results
        """
        return self.thematic_analyzer.analyze_axis(axis)

    def analyze_all_axes(self) -> Dict[str, Any]:
        """
        Perform analysis across all thematic axes.

        Returns:
            Dictionary with results for each axis
        """
        return self.thematic_analyzer.analyze_all_axes()

    def get_quality_summary(self) -> Dict[str, Any]:
        """
        Get summary of quality assessments.

        Returns:
            Dictionary with quality distribution statistics
        """
        return self.quality_assessor.generate_quality_summary()

    def get_grade_cerqual_summary(self) -> List[Dict[str, Any]]:
        """
        Get GRADE-CERQual summary of findings table.

        Returns:
            List of findings with confidence assessments
        """
        return self.grade_cerqual.generate_summary_table()

    def search_studies(self, query: str) -> List[Study]:
        """
        Search studies by title, authors, or findings.

        Args:
            query: Search string

        Returns:
            List of matching Study objects
        """
        return self.db.search(query)

    def filter_studies(
        self,
        axis: Optional[ThematicAxis] = None,
        year_start: Optional[int] = None,
        year_end: Optional[int] = None,
        min_quality: Optional[QualityRating] = None,
        country: Optional[str] = None
    ) -> List[Study]:
        """
        Filter studies by multiple criteria.

        Args:
            axis: Filter by thematic axis
            year_start: Minimum publication year
            year_end: Maximum publication year
            min_quality: Minimum quality rating
            country: Filter by country

        Returns:
            List of studies matching all specified criteria
        """
        results = list(self.db.studies)

        if axis:
            results = [s for s in results if s.primary_axis == axis]

        if year_start:
            results = [s for s in results if s.year >= year_start]

        if year_end:
            results = [s for s in results if s.year <= year_end]

        if min_quality:
            ratings = [QualityRating.LOW, QualityRating.MODERATE, QualityRating.HIGH]
            min_idx = ratings.index(min_quality)
            results = [s for s in results if s.quality_rating in ratings[min_idx:]]

        if country:
            results = [s for s in results
                       if s.country and s.country.lower() == country.lower()]

        return results

    def export_to_json(self, filepath: Path) -> None:
        """Export database to JSON file."""
        self.db.to_json(filepath)

    def export_to_csv(self, filepath: Path) -> None:
        """Export database to CSV file."""
        self.db.to_csv(filepath)

    def generate_prisma_stats(self) -> Dict[str, int]:
        """
        Generate PRISMA flow statistics.

        Returns:
            Dictionary with record counts at each stage
        """
        return {
            "records_identified": 847,
            "duplicates_removed": 156,
            "records_screened": 691,
            "records_excluded_screening": 567,
            "full_text_assessed": 124,
            "full_text_excluded": 72,
            "studies_included": len(self.db),
            "exclusion_reasons": {
                "insufficient_ehds_focus": 28,
                "methodological_limitations": 19,
                "duplicate_superseded": 14,
                "language": 7,
                "abstract_only": 4
            }
        }

    def get_research_gaps(self) -> List[str]:
        """
        Identify research gaps from the analysis.

        Returns:
            List of identified research gap descriptions
        """
        return [
            "Empirical citizen attitude studies: Limited systematic evidence on European citizens' EHDS awareness and attitudes",
            "National-European integration studies: Insufficient attention to how national digital health programs align with EHDS",
            "Economic sustainability models: Inadequate attention to HDAB financial sustainability and fee structures",
            "Longitudinal implementation tracking: Need for systematic documentation of implementation processes (2025-2031)",
            "Interdisciplinary integration: Research teams integrating technical, legal, ethical, and organizational expertise",
            "Emerging technology assessment: Roles of synthetic data, homomorphic encryption, and MPC remain underexplored"
        ]

    def get_testable_hypotheses(self) -> Dict[str, List[str]]:
        """
        Get testable hypotheses for future research.

        Returns:
            Dictionary with hypotheses organized by category
        """
        return {
            "governance": [
                "H1a: Member States with pre-existing opt-out frameworks will achieve higher data availability",
                "H1b: National opt-out rates will vary inversely with public trust in healthcare institutions",
                "H1c: HDAB authorization timelines will be positively associated with regulatory complexity"
            ],
            "technology": [
                "H2a: Organizations with >50% FHIR implementation will achieve EHDS compliance faster",
                "H2b: FL production deployment will increase from 23% to >50% by 2029",
                "H2c: SPE utilization will be higher for cross-border than single-Member-State requests"
            ],
            "implementation": [
                "H3a: Nordic Member States will achieve full compliance by 2029; Southern/Eastern by 2031",
                "H3b: HDAB staffing levels will predict throughput better than technical infrastructure",
                "H3c: Article 33(5) restrictions will reduce cross-border genomic research participation"
            ],
            "engagement": [
                "H4a: Public EHDS awareness will increase from <20% to >50% by 2029",
                "H4b: Trust in EHDS governance will correlate with HDAB transparency",
                "H4c: Deliberative engagement mechanisms will reduce opt-out rates"
            ]
        }

    def __repr__(self) -> str:
        return f"EHDSAnalyzer(studies={len(self.db)})"
