"""
Data models and database management for EHDS literature analysis.

This module provides data structures for managing systematic review studies,
including bibliographic information, quality assessments, and thematic coding.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
import json
import csv
from pathlib import Path


class StudyType(Enum):
    """Classification of study methodologies."""
    QUALITATIVE = "qualitative"
    QUANTITATIVE = "quantitative"
    MIXED_METHODS = "mixed_methods"
    CONCEPTUAL = "conceptual"
    SYSTEMATIC_REVIEW = "systematic_review"
    POLICY_DOCUMENT = "policy_document"
    TECHNICAL = "technical"


class QualityRating(Enum):
    """MMAT-based quality rating categories."""
    HIGH = "high"          # ≥80% criteria met
    MODERATE = "moderate"  # 60-79% criteria met
    LOW = "low"            # <60% criteria met
    NOT_APPLICABLE = "n/a"


class ThematicAxis(Enum):
    """Five thematic axes from the EHDS systematic review."""
    GOVERNANCE_RIGHTS_ETHICS = "governance_rights_ethics"
    SECONDARY_USE_PETS = "secondary_use_pets"
    NATIONAL_IMPLEMENTATION = "national_implementation"
    CITIZEN_ENGAGEMENT = "citizen_engagement"
    FEDERATED_LEARNING_AI = "federated_learning_ai"


class ConfidenceLevel(Enum):
    """GRADE-CERQual confidence levels."""
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    VERY_LOW = "very_low"


@dataclass
class Study:
    """
    Represents a single study in the systematic review.

    Attributes:
        id: Unique identifier
        authors: List of author names
        year: Publication year
        title: Full title of the study
        journal: Journal or source name
        doi: Digital Object Identifier (optional)
        study_type: Methodology classification
        country: Country of first author affiliation
        primary_axis: Main thematic focus
        secondary_themes: Additional themes addressed
        quality_rating: MMAT quality assessment
        mmat_score: Percentage of MMAT criteria met
        abstract: Study abstract (optional)
        key_findings: Main findings summary
        ehds_focus: Primary/secondary use focus
        ehds_articles: Specific EHDS articles referenced
        sample_size: Sample size for empirical studies
        limitations: Stated limitations
        funding: Funding sources
    """
    id: int
    authors: str
    year: int
    title: str
    journal: str
    study_type: StudyType
    primary_axis: ThematicAxis
    quality_rating: QualityRating = QualityRating.NOT_APPLICABLE
    doi: Optional[str] = None
    country: Optional[str] = None
    secondary_themes: List[str] = field(default_factory=list)
    mmat_score: Optional[float] = None
    abstract: Optional[str] = None
    key_findings: Optional[str] = None
    ehds_focus: str = "both"  # "primary", "secondary", "both"
    ehds_articles: List[str] = field(default_factory=list)
    sample_size: Optional[int] = None
    limitations: Optional[str] = None
    funding: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert study to dictionary representation."""
        return {
            "id": self.id,
            "authors": self.authors,
            "year": self.year,
            "title": self.title,
            "journal": self.journal,
            "doi": self.doi,
            "study_type": self.study_type.value,
            "country": self.country,
            "primary_axis": self.primary_axis.value,
            "secondary_themes": self.secondary_themes,
            "quality_rating": self.quality_rating.value,
            "mmat_score": self.mmat_score,
            "abstract": self.abstract,
            "key_findings": self.key_findings,
            "ehds_focus": self.ehds_focus,
            "ehds_articles": self.ehds_articles,
            "sample_size": self.sample_size,
            "limitations": self.limitations,
            "funding": self.funding
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Study":
        """Create Study instance from dictionary."""
        return cls(
            id=data["id"],
            authors=data["authors"],
            year=data["year"],
            title=data["title"],
            journal=data["journal"],
            doi=data.get("doi"),
            study_type=StudyType(data["study_type"]),
            country=data.get("country"),
            primary_axis=ThematicAxis(data["primary_axis"]),
            secondary_themes=data.get("secondary_themes", []),
            quality_rating=QualityRating(data.get("quality_rating", "n/a")),
            mmat_score=data.get("mmat_score"),
            abstract=data.get("abstract"),
            key_findings=data.get("key_findings"),
            ehds_focus=data.get("ehds_focus", "both"),
            ehds_articles=data.get("ehds_articles", []),
            sample_size=data.get("sample_size"),
            limitations=data.get("limitations"),
            funding=data.get("funding")
        )

    def get_citation(self, style: str = "apa") -> str:
        """Generate formatted citation string."""
        if style == "apa":
            doi_str = f" https://doi.org/{self.doi}" if self.doi else ""
            return f"{self.authors} ({self.year}). {self.title}. {self.journal}.{doi_str}"
        elif style == "vancouver":
            return f"{self.authors}. {self.title}. {self.journal}. {self.year}."
        return f"{self.authors} ({self.year})"


class StudyDatabase:
    """
    Database for managing systematic review studies.

    Provides functionality for storing, querying, filtering, and exporting
    study data with support for JSON and CSV formats.
    """

    def __init__(self):
        """Initialize empty study database."""
        self.studies: List[Study] = []
        self._index: Dict[int, Study] = {}
        self.metadata = {
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat(),
            "version": "1.0",
            "description": "EHDS Systematic Literature Review Database"
        }

    def add_study(self, study: Study) -> None:
        """Add a study to the database."""
        if study.id in self._index:
            raise ValueError(f"Study with ID {study.id} already exists")
        self.studies.append(study)
        self._index[study.id] = study
        self.metadata["modified"] = datetime.now().isoformat()

    def get_study(self, study_id: int) -> Optional[Study]:
        """Retrieve a study by ID."""
        return self._index.get(study_id)

    def remove_study(self, study_id: int) -> bool:
        """Remove a study from the database."""
        if study_id in self._index:
            study = self._index.pop(study_id)
            self.studies.remove(study)
            self.metadata["modified"] = datetime.now().isoformat()
            return True
        return False

    def filter_by_axis(self, axis: ThematicAxis) -> List[Study]:
        """Filter studies by primary thematic axis."""
        return [s for s in self.studies if s.primary_axis == axis]

    def filter_by_year(self, start: int, end: int) -> List[Study]:
        """Filter studies by publication year range."""
        return [s for s in self.studies if start <= s.year <= end]

    def filter_by_quality(self, min_rating: QualityRating) -> List[Study]:
        """Filter studies by minimum quality rating."""
        ratings_order = [QualityRating.LOW, QualityRating.MODERATE, QualityRating.HIGH]
        min_idx = ratings_order.index(min_rating) if min_rating in ratings_order else 0
        return [s for s in self.studies
                if s.quality_rating in ratings_order[min_idx:]]

    def filter_by_type(self, study_type: StudyType) -> List[Study]:
        """Filter studies by methodology type."""
        return [s for s in self.studies if s.study_type == study_type]

    def filter_by_country(self, country: str) -> List[Study]:
        """Filter studies by country of first author."""
        return [s for s in self.studies
                if s.country and s.country.lower() == country.lower()]

    def search(self, query: str) -> List[Study]:
        """Search studies by title, authors, or key findings."""
        query = query.lower()
        return [s for s in self.studies
                if query in s.title.lower()
                or query in s.authors.lower()
                or (s.key_findings and query in s.key_findings.lower())]

    def get_statistics(self) -> Dict[str, Any]:
        """Calculate database statistics."""
        if not self.studies:
            return {"total": 0}

        by_year = {}
        by_axis = {}
        by_type = {}
        by_quality = {}
        by_country = {}

        for study in self.studies:
            # Year distribution
            by_year[study.year] = by_year.get(study.year, 0) + 1

            # Axis distribution
            axis = study.primary_axis.value
            by_axis[axis] = by_axis.get(axis, 0) + 1

            # Type distribution
            stype = study.study_type.value
            by_type[stype] = by_type.get(stype, 0) + 1

            # Quality distribution
            quality = study.quality_rating.value
            by_quality[quality] = by_quality.get(quality, 0) + 1

            # Country distribution
            if study.country:
                by_country[study.country] = by_country.get(study.country, 0) + 1

        return {
            "total": len(self.studies),
            "by_year": dict(sorted(by_year.items())),
            "by_axis": by_axis,
            "by_type": by_type,
            "by_quality": by_quality,
            "by_country": dict(sorted(by_country.items(),
                                       key=lambda x: x[1], reverse=True)),
            "year_range": (min(by_year.keys()), max(by_year.keys())),
            "peer_reviewed": len([s for s in self.studies
                                  if s.study_type != StudyType.POLICY_DOCUMENT])
        }

    def to_json(self, filepath: Optional[Path] = None) -> str:
        """Export database to JSON format."""
        data = {
            "metadata": self.metadata,
            "studies": [s.to_dict() for s in self.studies]
        }
        json_str = json.dumps(data, indent=2, ensure_ascii=False)

        if filepath:
            Path(filepath).write_text(json_str, encoding="utf-8")

        return json_str

    def from_json(self, filepath: Path) -> None:
        """Import database from JSON file."""
        data = json.loads(Path(filepath).read_text(encoding="utf-8"))
        self.metadata = data.get("metadata", self.metadata)
        self.studies = []
        self._index = {}

        for study_data in data.get("studies", []):
            study = Study.from_dict(study_data)
            self.add_study(study)

    def to_csv(self, filepath: Path) -> None:
        """Export database to CSV format."""
        if not self.studies:
            return

        fieldnames = list(self.studies[0].to_dict().keys())

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for study in self.studies:
                row = study.to_dict()
                # Convert lists to strings for CSV
                row["secondary_themes"] = "|".join(row["secondary_themes"])
                row["ehds_articles"] = "|".join(row["ehds_articles"])
                writer.writerow(row)

    def __len__(self) -> int:
        return len(self.studies)

    def __iter__(self):
        return iter(self.studies)

    def __getitem__(self, key: int) -> Study:
        return self._index[key]


def load_ehds_studies() -> StudyDatabase:
    """
    Load the 52 studies from the EHDS systematic review.

    Returns:
        StudyDatabase populated with all included studies.
    """
    db = StudyDatabase()

    # The 52 studies from the systematic review
    studies_data = [
        {"id": 1, "authors": "Ahmadi, H. et al.", "year": 2017, "title": "Organizational decision to adopt hospital information system", "journal": "Int J Med Inform", "study_type": "quantitative", "primary_axis": "national_implementation", "quality_rating": "high", "country": "Malaysia"},
        {"id": 2, "authors": "Aitken, M. et al.", "year": 2016, "title": "Public responses to sharing and linkage of health data", "journal": "BMC Med Ethics", "study_type": "systematic_review", "primary_axis": "citizen_engagement", "quality_rating": "high", "country": "UK"},
        {"id": 3, "authors": "Ayaz, M. et al.", "year": 2021, "title": "FHIR standard: Systematic literature review", "journal": "JMIR Med Inform", "study_type": "systematic_review", "primary_axis": "secondary_use_pets", "quality_rating": "high", "country": "Malaysia"},
        {"id": 4, "authors": "Baumgart, D.C. & Kvedar, J.C.", "year": 2025, "title": "Germany and Europe lead digital innovation", "journal": "npj Digit Med", "study_type": "conceptual", "primary_axis": "national_implementation", "quality_rating": "high", "country": "Germany"},
        {"id": 5, "authors": "BEUC", "year": 2023, "title": "Consumer attitudes to health data sharing", "journal": "Policy report", "study_type": "policy_document", "primary_axis": "citizen_engagement", "quality_rating": "moderate", "country": "EU"},
        {"id": 6, "authors": "Blasimme, A. & Vayena, E.", "year": 2020, "title": "What's next for COVID-19 apps?", "journal": "Science", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "Switzerland"},
        {"id": 7, "authors": "Christiansen, C.F. et al.", "year": 2025, "title": "Piloting an infrastructure for secondary use", "journal": "Eur J Public Health", "study_type": "qualitative", "primary_axis": "national_implementation", "quality_rating": "high", "country": "Denmark"},
        {"id": 8, "authors": "Dove, E.S.", "year": 2024, "title": "The EHDS as a Case Study", "journal": "Ethics Hum Res", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "UK"},
        {"id": 9, "authors": "EFPIA", "year": 2024, "title": "Position on opt-out in the EHDS Regulation", "journal": "Position paper", "study_type": "policy_document", "primary_axis": "governance_rights_ethics", "quality_rating": "moderate", "country": "EU"},
        {"id": 10, "authors": "EIT Health", "year": 2024, "title": "Implementing the EHDS: Think Tank Report", "journal": "Policy report", "study_type": "policy_document", "primary_axis": "national_implementation", "quality_rating": "moderate", "country": "EU"},
        {"id": 11, "authors": "European Commission", "year": 2025, "title": "Regulation (EU) 2025/327", "journal": "Official Journal", "study_type": "policy_document", "primary_axis": "governance_rights_ethics", "quality_rating": "n/a", "country": "EU"},
        {"id": 12, "authors": "European Patient Forum", "year": 2025, "title": "EPF's analysis of the EHDS Regulation", "journal": "Policy report", "study_type": "policy_document", "primary_axis": "citizen_engagement", "quality_rating": "moderate", "country": "EU"},
        {"id": 13, "authors": "Forster, R.B. et al.", "year": 2025, "title": "User journeys in cross-European secondary use", "journal": "Eur J Public Health", "study_type": "qualitative", "primary_axis": "national_implementation", "quality_rating": "high", "country": "Denmark"},
        {"id": 14, "authors": "Fröhlich, H. et al.", "year": 2025, "title": "Reality check: The aspirations of the EHDS", "journal": "JMIR", "study_type": "technical", "primary_axis": "secondary_use_pets", "quality_rating": "high", "country": "Germany"},
        {"id": 15, "authors": "Frontiers", "year": 2025, "title": "Synthetic data in medical imaging within EHDS", "journal": "Front Digit Health", "study_type": "conceptual", "primary_axis": "secondary_use_pets", "quality_rating": "high", "country": "EU"},
        {"id": 16, "authors": "Ganna, A. et al.", "year": 2024, "title": "EHDS can be a boost for research beyond borders", "journal": "Nat Med", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "Sweden"},
        {"id": 17, "authors": "Gunningham, N. et al.", "year": 2004, "title": "Social license and environmental protection", "journal": "Law Soc Inquiry", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "Australia"},
        {"id": 18, "authors": "Haugo, H.T. & de Frutos Lucas, J.", "year": 2024, "title": "Moving forward with the EHDS", "journal": "Lancet Reg Health Eur", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "Norway"},
        {"id": 19, "authors": "Health Policy", "year": 2025, "title": "Anticipating ethical and social dimensions of EHDS", "journal": "Health Policy", "study_type": "systematic_review", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "Netherlands"},
        {"id": 20, "authors": "Hong, Q.N. et al.", "year": 2018, "title": "MMAT version 2018", "journal": "Educ Inform", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "Canada"},
        {"id": 21, "authors": "Hooghe, L. & Marks, G.", "year": 2003, "title": "Types of multi-level governance", "journal": "Am Polit Sci Rev", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "USA"},
        {"id": 22, "authors": "Hussein, R. et al.", "year": 2025, "title": "Interoperability framework of the EHDS", "journal": "JMIR", "study_type": "technical", "primary_axis": "secondary_use_pets", "quality_rating": "high", "country": "Germany"},
        {"id": 23, "authors": "JMIR", "year": 2025, "title": "Lessons learned from European health data projects", "journal": "JMIR", "study_type": "qualitative", "primary_axis": "secondary_use_pets", "quality_rating": "high", "country": "EU"},
        {"id": 24, "authors": "Kalkman, S. et al.", "year": 2022, "title": "Patients' and public views on health data sharing", "journal": "J Med Ethics", "study_type": "systematic_review", "primary_axis": "citizen_engagement", "quality_rating": "high", "country": "Netherlands"},
        {"id": 25, "authors": "Kaye, J. et al.", "year": 2015, "title": "Dynamic consent", "journal": "Eur J Hum Genet", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "UK"},
        {"id": 26, "authors": "Lehne, M. et al.", "year": 2019, "title": "Why digital medicine depends on interoperability", "journal": "npj Digit Med", "study_type": "conceptual", "primary_axis": "secondary_use_pets", "quality_rating": "high", "country": "Germany"},
        {"id": 27, "authors": "Lewin, S. et al.", "year": 2018, "title": "Applying GRADE-CERQual", "journal": "Implement Sci", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "Norway"},
        {"id": 28, "authors": "Marelli, L. et al.", "year": 2020, "title": "Fit for purpose? GDPR and European digital health", "journal": "Policy Stud", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "Belgium"},
        {"id": 29, "authors": "Mostert, M. et al.", "year": 2016, "title": "Big Data in medical research and EU data protection", "journal": "Eur J Hum Genet", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "Netherlands"},
        {"id": 30, "authors": "Nature Medicine", "year": 2025, "title": "Data sharing restrictions hampering precision health", "journal": "Nat Med", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "USA"},
        {"id": 31, "authors": "Noyes, J. et al.", "year": 2019, "title": "Synthesising quantitative and qualitative evidence", "journal": "BMJ Glob Health", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "UK"},
        {"id": 32, "authors": "npj Digital Medicine", "year": 2025, "title": "Scoping review of FL governance in healthcare", "journal": "npj Digit Med", "study_type": "systematic_review", "primary_axis": "federated_learning_ai", "quality_rating": "high", "country": "USA"},
        {"id": 33, "authors": "Page, M.J. et al.", "year": 2021, "title": "PRISMA 2020 statement", "journal": "BMJ", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "Australia"},
        {"id": 34, "authors": "Peng, L. et al.", "year": 2024, "title": "Federated ML in healthcare: Systematic review", "journal": "Comput Methods Programs Biomed", "study_type": "systematic_review", "primary_axis": "federated_learning_ai", "quality_rating": "high", "country": "USA"},
        {"id": 35, "authors": "Pormeister, K.", "year": 2020, "title": "GDPR and big data: Leading the way for genetic data?", "journal": "Comput Law Secur Rev", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "Estonia"},
        {"id": 36, "authors": "Quinn, P. et al.", "year": 2024, "title": "Will GDPR restrain HDABs under the EHDS?", "journal": "Comput Law Secur Rev", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "Belgium"},
        {"id": 37, "authors": "Quinn, P. & Quinn, L.", "year": 2018, "title": "Big genetic data and its protection challenges", "journal": "Comput Law Secur Rev", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "Belgium"},
        {"id": 38, "authors": "Raab, R. et al.", "year": 2023, "title": "Federated EHRs for the EHDS", "journal": "Lancet Digit Health", "study_type": "technical", "primary_axis": "secondary_use_pets", "quality_rating": "high", "country": "Germany"},
        {"id": 39, "authors": "Rieke, N. et al.", "year": 2020, "title": "Future of digital health with federated learning", "journal": "npj Digit Med", "study_type": "systematic_review", "primary_axis": "federated_learning_ai", "quality_rating": "high", "country": "Germany"},
        {"id": 40, "authors": "Royo, R. et al.", "year": 2025, "title": "Genomic data sharing in research across Europe", "journal": "Eur J Public Health", "study_type": "conceptual", "primary_axis": "secondary_use_pets", "quality_rating": "high", "country": "Spain"},
        {"id": 41, "authors": "Shabani, M. & Borry, P.", "year": 2018, "title": "Rules for processing genetic data under GDPR", "journal": "Eur J Hum Genet", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "Belgium"},
        {"id": 42, "authors": "Slokenberga, S. et al.", "year": 2021, "title": "GDPR and biobanking", "journal": "Springer", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "Sweden"},
        {"id": 43, "authors": "Staunton, C. et al.", "year": 2024, "title": "Ethical and social reflections on the proposed EHDS", "journal": "Eur J Hum Genet", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "Ireland"},
        {"id": 44, "authors": "Svingel, L.S. et al.", "year": 2025, "title": "Recommendations for HDAB implementation", "journal": "Eur J Public Health", "study_type": "qualitative", "primary_axis": "national_implementation", "quality_rating": "high", "country": "Denmark"},
        {"id": 45, "authors": "TEHDAS", "year": 2024, "title": "Are EU member states ready for EHDS?", "journal": "Eur J Public Health", "study_type": "mixed_methods", "primary_axis": "national_implementation", "quality_rating": "high", "country": "EU"},
        {"id": 46, "authors": "TEHDAS2", "year": 2025, "title": "Draft guideline: How to implement opt-out", "journal": "Policy document", "study_type": "policy_document", "primary_axis": "governance_rights_ethics", "quality_rating": "moderate", "country": "EU"},
        {"id": 47, "authors": "TEHDAS2", "year": 2025, "title": "Guideline on SPE use", "journal": "Policy document", "study_type": "policy_document", "primary_axis": "secondary_use_pets", "quality_rating": "moderate", "country": "EU"},
        {"id": 48, "authors": "Thomas, J. & Harden, A.", "year": 2008, "title": "Methods for thematic synthesis", "journal": "BMC Med Res Methodol", "study_type": "conceptual", "primary_axis": "governance_rights_ethics", "quality_rating": "high", "country": "UK"},
        {"id": 49, "authors": "Tornatzky, L.G. & Fleischer, M.", "year": 1990, "title": "The processes of technological innovation", "journal": "Book", "study_type": "conceptual", "primary_axis": "national_implementation", "quality_rating": "high", "country": "USA"},
        {"id": 50, "authors": "van Drumpt, S. et al.", "year": 2025, "title": "Secondary use under EHDS: PETs research agenda", "journal": "Front Digit Health", "study_type": "qualitative", "primary_axis": "secondary_use_pets", "quality_rating": "high", "country": "Netherlands"},
        {"id": 51, "authors": "Vorisek, C.N. et al.", "year": 2022, "title": "FHIR for interoperability in health research", "journal": "JMIR Med Inform", "study_type": "systematic_review", "primary_axis": "secondary_use_pets", "quality_rating": "high", "country": "Germany"},
        {"id": 52, "authors": "Welzel, C. et al.", "year": 2025, "title": "Enabling secure health data sharing and consent", "journal": "npj Digit Med", "study_type": "technical", "primary_axis": "citizen_engagement", "quality_rating": "high", "country": "Germany"},
    ]

    for data in studies_data:
        study = Study(
            id=data["id"],
            authors=data["authors"],
            year=data["year"],
            title=data["title"],
            journal=data["journal"],
            study_type=StudyType(data["study_type"]),
            primary_axis=ThematicAxis(data["primary_axis"]),
            quality_rating=QualityRating(data["quality_rating"]),
            country=data.get("country")
        )
        db.add_study(study)

    return db
