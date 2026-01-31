"""
Tests for EHDSLens core functionality.
"""

import pytest
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ehdslens import EHDSAnalyzer
from ehdslens.data import (
    StudyDatabase, Study, ThematicAxis, QualityRating,
    StudyType, load_ehds_studies
)


class TestStudyDatabase:
    """Test StudyDatabase functionality."""

    def test_create_empty_database(self):
        """Test creating an empty database."""
        db = StudyDatabase()
        assert len(db) == 0
        assert db.metadata is not None

    def test_add_study(self):
        """Test adding a study to database."""
        db = StudyDatabase()
        study = Study(
            id=1,
            authors="Test Author",
            year=2024,
            title="Test Study",
            journal="Test Journal",
            study_type=StudyType.QUALITATIVE,
            primary_axis=ThematicAxis.GOVERNANCE_RIGHTS_ETHICS
        )
        db.add_study(study)
        assert len(db) == 1
        assert db.get_study(1) == study

    def test_add_duplicate_raises_error(self):
        """Test that adding duplicate ID raises error."""
        db = StudyDatabase()
        study = Study(
            id=1,
            authors="Test",
            year=2024,
            title="Test",
            journal="Test",
            study_type=StudyType.QUALITATIVE,
            primary_axis=ThematicAxis.GOVERNANCE_RIGHTS_ETHICS
        )
        db.add_study(study)

        with pytest.raises(ValueError):
            db.add_study(study)

    def test_filter_by_axis(self):
        """Test filtering by thematic axis."""
        db = StudyDatabase()
        for i in range(5):
            axis = ThematicAxis.GOVERNANCE_RIGHTS_ETHICS if i < 3 else ThematicAxis.SECONDARY_USE_PETS
            db.add_study(Study(
                id=i+1,
                authors=f"Author {i}",
                year=2024,
                title=f"Study {i}",
                journal="Journal",
                study_type=StudyType.QUALITATIVE,
                primary_axis=axis
            ))

        governance = db.filter_by_axis(ThematicAxis.GOVERNANCE_RIGHTS_ETHICS)
        assert len(governance) == 3

        pets = db.filter_by_axis(ThematicAxis.SECONDARY_USE_PETS)
        assert len(pets) == 2

    def test_filter_by_year(self):
        """Test filtering by year range."""
        db = StudyDatabase()
        for year in [2022, 2023, 2024, 2025]:
            db.add_study(Study(
                id=year,
                authors="Author",
                year=year,
                title=f"Study {year}",
                journal="Journal",
                study_type=StudyType.QUALITATIVE,
                primary_axis=ThematicAxis.GOVERNANCE_RIGHTS_ETHICS
            ))

        recent = db.filter_by_year(2024, 2025)
        assert len(recent) == 2

    def test_search(self):
        """Test search functionality."""
        db = StudyDatabase()
        db.add_study(Study(
            id=1,
            authors="Staunton, C.",
            year=2024,
            title="Ethical reflections on EHDS",
            journal="EJHG",
            study_type=StudyType.CONCEPTUAL,
            primary_axis=ThematicAxis.GOVERNANCE_RIGHTS_ETHICS
        ))
        db.add_study(Study(
            id=2,
            authors="Fröhlich, H.",
            year=2025,
            title="Reality check on federated learning",
            journal="JMIR",
            study_type=StudyType.TECHNICAL,
            primary_axis=ThematicAxis.SECONDARY_USE_PETS
        ))

        results = db.search("ethical")
        assert len(results) == 1
        assert results[0].id == 1

        results = db.search("federated")
        assert len(results) == 1
        assert results[0].id == 2

    def test_statistics(self):
        """Test statistics generation."""
        db = load_ehds_studies()
        stats = db.get_statistics()

        assert stats['total'] == 52
        assert 'by_year' in stats
        assert 'by_axis' in stats
        assert 'by_quality' in stats


class TestStudy:
    """Test Study data class."""

    def test_study_creation(self):
        """Test creating a Study instance."""
        study = Study(
            id=1,
            authors="Test Author",
            year=2024,
            title="Test Title",
            journal="Test Journal",
            study_type=StudyType.QUALITATIVE,
            primary_axis=ThematicAxis.GOVERNANCE_RIGHTS_ETHICS,
            quality_rating=QualityRating.HIGH,
            doi="10.1234/test"
        )

        assert study.id == 1
        assert study.year == 2024
        assert study.quality_rating == QualityRating.HIGH

    def test_study_to_dict(self):
        """Test converting study to dictionary."""
        study = Study(
            id=1,
            authors="Test",
            year=2024,
            title="Test",
            journal="Journal",
            study_type=StudyType.QUALITATIVE,
            primary_axis=ThematicAxis.GOVERNANCE_RIGHTS_ETHICS
        )

        d = study.to_dict()
        assert d['id'] == 1
        assert d['study_type'] == 'qualitative'
        assert d['primary_axis'] == 'governance_rights_ethics'

    def test_study_from_dict(self):
        """Test creating study from dictionary."""
        data = {
            'id': 1,
            'authors': 'Test',
            'year': 2024,
            'title': 'Test',
            'journal': 'Journal',
            'study_type': 'qualitative',
            'primary_axis': 'governance_rights_ethics',
            'quality_rating': 'high'
        }

        study = Study.from_dict(data)
        assert study.id == 1
        assert study.study_type == StudyType.QUALITATIVE

    def test_get_citation_apa(self):
        """Test APA citation generation."""
        study = Study(
            id=1,
            authors="Smith, J.",
            year=2024,
            title="Test Study",
            journal="Test Journal",
            study_type=StudyType.QUALITATIVE,
            primary_axis=ThematicAxis.GOVERNANCE_RIGHTS_ETHICS,
            doi="10.1234/test"
        )

        citation = study.get_citation(style="apa")
        assert "Smith, J." in citation
        assert "2024" in citation
        assert "10.1234/test" in citation


class TestLoadEHDSStudies:
    """Test loading the default EHDS study database."""

    def test_load_default_studies(self):
        """Test loading the 52 EHDS studies."""
        db = load_ehds_studies()

        assert len(db) == 52
        assert db.get_study(1) is not None
        assert db.get_study(52) is not None

    def test_study_distribution(self):
        """Test that studies are distributed across axes."""
        db = load_ehds_studies()

        for axis in ThematicAxis:
            studies = db.filter_by_axis(axis)
            assert len(studies) > 0, f"No studies for axis {axis}"


class TestEHDSAnalyzer:
    """Test main analyzer class."""

    def test_analyzer_creation(self):
        """Test creating analyzer."""
        analyzer = EHDSAnalyzer()
        assert len(analyzer.db) == 0

    def test_load_default_data(self):
        """Test loading default data."""
        analyzer = EHDSAnalyzer()
        analyzer.load_default_data()
        assert len(analyzer.db) == 52

    def test_get_statistics(self):
        """Test getting statistics."""
        analyzer = EHDSAnalyzer()
        analyzer.load_default_data()
        stats = analyzer.get_statistics()

        assert stats['total'] == 52
        assert stats['peer_reviewed'] > 0

    def test_analyze_axis(self):
        """Test analyzing specific axis."""
        analyzer = EHDSAnalyzer()
        analyzer.load_default_data()

        result = analyzer.analyze_axis(ThematicAxis.GOVERNANCE_RIGHTS_ETHICS)
        assert result['total_studies'] > 0
        assert 'type_distribution' in result

    def test_grade_cerqual_summary(self):
        """Test GRADE-CERQual summary."""
        analyzer = EHDSAnalyzer()
        analyzer.load_default_data()

        summary = analyzer.get_grade_cerqual_summary()
        assert len(summary) == 5  # 5 thematic axes

        # Check that each finding has required fields
        for finding in summary:
            assert 'finding' in finding
            assert 'confidence' in finding
            assert finding['confidence'] in ['HIGH', 'MODERATE', 'LOW', 'VERY_LOW']

    def test_get_research_gaps(self):
        """Test research gaps identification."""
        analyzer = EHDSAnalyzer()
        analyzer.load_default_data()

        gaps = analyzer.get_research_gaps()
        assert len(gaps) >= 5

    def test_get_testable_hypotheses(self):
        """Test testable hypotheses."""
        analyzer = EHDSAnalyzer()
        analyzer.load_default_data()

        hypotheses = analyzer.get_testable_hypotheses()
        assert 'governance' in hypotheses
        assert 'technology' in hypotheses
        assert len(hypotheses['governance']) >= 2

    def test_filter_studies(self):
        """Test filtering studies with multiple criteria."""
        analyzer = EHDSAnalyzer()
        analyzer.load_default_data()

        # Filter high quality 2024-2025 studies
        results = analyzer.filter_studies(
            year_start=2024,
            year_end=2025,
            min_quality=QualityRating.HIGH
        )

        for study in results:
            assert 2024 <= study.year <= 2025
            assert study.quality_rating == QualityRating.HIGH


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
