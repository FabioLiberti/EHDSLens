"""
Analysis modules for EHDS systematic literature review.

Provides thematic analysis, quality assessment, and GRADE-CERQual
confidence evaluation functionality.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import Counter
import statistics

from .data import (
    Study, StudyDatabase, ThematicAxis, QualityRating,
    StudyType, ConfidenceLevel
)


@dataclass
class ThematicFinding:
    """
    Represents a synthesized thematic finding.

    Attributes:
        axis: Thematic axis this finding relates to
        title: Brief title of the finding
        description: Detailed description
        supporting_studies: List of study IDs supporting this finding
        confidence: GRADE-CERQual confidence level
        key_quotes: Representative quotes from studies
    """
    axis: ThematicAxis
    title: str
    description: str
    supporting_studies: List[int] = field(default_factory=list)
    confidence: ConfidenceLevel = ConfidenceLevel.MODERATE
    key_quotes: List[str] = field(default_factory=list)

    def get_study_count(self) -> int:
        """Return number of supporting studies."""
        return len(self.supporting_studies)


class ThematicAnalyzer:
    """
    Performs thematic analysis on EHDS literature.

    Implements the seven-category coding framework from the systematic review:
    1. Rights and autonomy
    2. Governance and institutions
    3. Technical infrastructure
    4. Data quality and interoperability
    5. Equity and inclusion
    6. Public engagement
    7. Sectoral impacts
    """

    CODING_FRAMEWORK = {
        "rights_autonomy": {
            "description": "Consent, opt-out, portability, individual control",
            "codes": ["opt-out", "consent", "portability", "autonomy",
                      "re-identification", "data rights", "citizen control"]
        },
        "governance_institutions": {
            "description": "HDABs, EHDS Board, national authorities, coordination",
            "codes": ["HDAB", "EHDS Board", "authorization", "permit",
                      "governance", "accountability", "coordination"]
        },
        "technical_infrastructure": {
            "description": "MyHealth@EU, HealthData@EU, SPEs, PETs",
            "codes": ["SPE", "federated", "PET", "infrastructure",
                      "MyHealth@EU", "HealthData@EU", "encryption"]
        },
        "data_quality_interoperability": {
            "description": "FAIR principles, FHIR, semantic standards",
            "codes": ["FHIR", "FAIR", "interoperability", "semantic",
                      "EHR format", "quality", "standardization"]
        },
        "equity_inclusion": {
            "description": "Digital divide, capacity asymmetries, vulnerable populations",
            "codes": ["equity", "divide", "vulnerable", "capacity",
                      "asymmetry", "inclusion", "disparities"]
        },
        "public_engagement": {
            "description": "Citizen participation, trust, transparency",
            "codes": ["trust", "transparency", "engagement", "participation",
                      "social licence", "public", "consultation"]
        },
        "sectoral_impacts": {
            "description": "Research, industry, policy, clinical care",
            "codes": ["research", "pharma", "industry", "clinical",
                      "innovation", "policy", "healthcare"]
        }
    }

    def __init__(self, database: StudyDatabase):
        """Initialize analyzer with study database."""
        self.db = database
        self.findings: List[ThematicFinding] = []

    def analyze_axis(self, axis: ThematicAxis) -> Dict[str, Any]:
        """
        Perform thematic analysis for a specific axis.

        Returns:
            Dictionary containing analysis results including
            study counts, themes, and synthesis.
        """
        studies = self.db.filter_by_axis(axis)

        # Count study types
        type_counts = Counter(s.study_type.value for s in studies)

        # Count quality ratings
        quality_counts = Counter(s.quality_rating.value for s in studies)

        # Count by year
        year_counts = Counter(s.year for s in studies)

        # Count by country
        country_counts = Counter(s.country for s in studies if s.country)

        # High quality studies
        high_quality = [s for s in studies
                        if s.quality_rating == QualityRating.HIGH]

        return {
            "axis": axis.value,
            "total_studies": len(studies),
            "peer_reviewed": len([s for s in studies
                                  if s.study_type != StudyType.POLICY_DOCUMENT]),
            "grey_literature": len([s for s in studies
                                    if s.study_type == StudyType.POLICY_DOCUMENT]),
            "high_quality_count": len(high_quality),
            "type_distribution": dict(type_counts),
            "quality_distribution": dict(quality_counts),
            "year_distribution": dict(sorted(year_counts.items())),
            "country_distribution": dict(country_counts.most_common(5)),
            "studies": [s.to_dict() for s in studies]
        }

    def analyze_all_axes(self) -> Dict[str, Any]:
        """Perform analysis across all thematic axes."""
        results = {}
        for axis in ThematicAxis:
            results[axis.value] = self.analyze_axis(axis)
        return results

    def identify_cross_cutting_themes(self) -> List[str]:
        """
        Identify themes appearing across multiple axes.

        Returns:
            List of cross-cutting theme descriptions.
        """
        themes = []

        # Check for trust-related content across axes
        trust_axes = []
        for axis in ThematicAxis:
            studies = self.db.filter_by_axis(axis)
            for study in studies:
                if study.title and "trust" in study.title.lower():
                    trust_axes.append(axis.value)
                    break

        if len(trust_axes) > 1:
            themes.append(f"Trust appears in {len(trust_axes)} axes: "
                          f"{', '.join(trust_axes)}")

        # Check for governance themes
        governance_count = len(self.db.filter_by_axis(
            ThematicAxis.GOVERNANCE_RIGHTS_ETHICS))
        if governance_count > 10:
            themes.append(f"Governance dominates with {governance_count} studies")

        return themes

    def calculate_inter_rater_reliability(
        self,
        coder1_assignments: Dict[int, ThematicAxis],
        coder2_assignments: Dict[int, ThematicAxis]
    ) -> float:
        """
        Calculate Cohen's kappa for inter-rater reliability.

        Args:
            coder1_assignments: Study ID to axis mapping from coder 1
            coder2_assignments: Study ID to axis mapping from coder 2

        Returns:
            Cohen's kappa coefficient
        """
        common_ids = set(coder1_assignments.keys()) & set(coder2_assignments.keys())
        if not common_ids:
            return 0.0

        agreements = sum(1 for sid in common_ids
                         if coder1_assignments[sid] == coder2_assignments[sid])

        # Observed agreement
        po = agreements / len(common_ids)

        # Expected agreement (by chance)
        axes = list(ThematicAxis)
        pe = sum(
            (sum(1 for sid in common_ids if coder1_assignments[sid] == ax) / len(common_ids)) *
            (sum(1 for sid in common_ids if coder2_assignments[sid] == ax) / len(common_ids))
            for ax in axes
        )

        # Cohen's kappa
        if pe == 1:
            return 1.0
        return (po - pe) / (1 - pe)


class QualityAssessor:
    """
    Implements MMAT-based quality assessment for systematic review studies.

    Mixed Methods Appraisal Tool (MMAT) version 2018 criteria are applied
    based on study type.
    """

    MMAT_CRITERIA = {
        StudyType.QUALITATIVE: [
            "Is the qualitative approach appropriate?",
            "Are data collection methods adequate?",
            "Are findings adequately derived from data?",
            "Is interpretation sufficiently substantiated?",
            "Is there coherence between sources, collection, analysis?",
        ],
        StudyType.QUANTITATIVE: [
            "Is the sampling strategy relevant?",
            "Is the sample representative?",
            "Are measurements appropriate?",
            "Is nonresponse bias low?",
            "Is statistical analysis appropriate?",
        ],
        StudyType.MIXED_METHODS: [
            "Is there adequate rationale for mixed methods?",
            "Are different components effectively integrated?",
            "Are outputs adequately interpreted?",
            "Are divergences addressed?",
            "Do components adhere to quality criteria?",
        ],
        StudyType.CONCEPTUAL: [
            "Is the research question clearly stated?",
            "Is there explicit methodology?",
            "Is argumentation logically structured?",
            "Are counterarguments engaged?",
            "Are limitations acknowledged?",
        ]
    }

    def __init__(self, database: StudyDatabase):
        """Initialize assessor with study database."""
        self.db = database

    def get_criteria(self, study_type: StudyType) -> List[str]:
        """Get MMAT criteria for a study type."""
        return self.MMAT_CRITERIA.get(study_type, self.MMAT_CRITERIA[StudyType.CONCEPTUAL])

    def assess_study(
        self,
        study_id: int,
        criteria_met: List[bool]
    ) -> Tuple[QualityRating, float]:
        """
        Assess a study's quality based on criteria.

        Args:
            study_id: ID of study to assess
            criteria_met: List of booleans indicating if each criterion is met

        Returns:
            Tuple of (QualityRating, percentage score)
        """
        study = self.db.get_study(study_id)
        if not study:
            raise ValueError(f"Study {study_id} not found")

        if not criteria_met:
            return QualityRating.NOT_APPLICABLE, 0.0

        score = sum(criteria_met) / len(criteria_met) * 100

        if score >= 80:
            rating = QualityRating.HIGH
        elif score >= 60:
            rating = QualityRating.MODERATE
        else:
            rating = QualityRating.LOW

        return rating, score

    def generate_quality_summary(self) -> Dict[str, Any]:
        """
        Generate summary statistics of quality assessments.

        Returns:
            Dictionary with quality distribution and statistics.
        """
        peer_reviewed = [s for s in self.db.studies
                         if s.study_type != StudyType.POLICY_DOCUMENT]

        quality_counts = Counter(s.quality_rating.value for s in peer_reviewed)

        high_pct = quality_counts.get("high", 0) / len(peer_reviewed) * 100 if peer_reviewed else 0
        moderate_pct = quality_counts.get("moderate", 0) / len(peer_reviewed) * 100 if peer_reviewed else 0
        low_pct = quality_counts.get("low", 0) / len(peer_reviewed) * 100 if peer_reviewed else 0

        return {
            "total_assessed": len(peer_reviewed),
            "high": {"count": quality_counts.get("high", 0), "percentage": high_pct},
            "moderate": {"count": quality_counts.get("moderate", 0), "percentage": moderate_pct},
            "low": {"count": quality_counts.get("low", 0), "percentage": low_pct},
            "by_study_type": self._quality_by_type(peer_reviewed)
        }

    def _quality_by_type(self, studies: List[Study]) -> Dict[str, Dict[str, int]]:
        """Calculate quality distribution by study type."""
        result = {}
        for stype in StudyType:
            type_studies = [s for s in studies if s.study_type == stype]
            if type_studies:
                result[stype.value] = {
                    "total": len(type_studies),
                    "high": len([s for s in type_studies if s.quality_rating == QualityRating.HIGH]),
                    "moderate": len([s for s in type_studies if s.quality_rating == QualityRating.MODERATE]),
                    "low": len([s for s in type_studies if s.quality_rating == QualityRating.LOW]),
                }
        return result


@dataclass
class CERQualAssessment:
    """
    GRADE-CERQual assessment for a review finding.

    Evaluates confidence based on four components:
    - Methodological limitations
    - Coherence
    - Adequacy of data
    - Relevance
    """
    finding: str
    axis: ThematicAxis
    supporting_studies: List[int]
    methodological_limitations: str  # "none", "minor", "moderate", "serious"
    coherence: str  # "high", "moderate", "low"
    adequacy: str  # "adequate", "limited", "very_limited"
    relevance: str  # "high", "moderate", "low"
    overall_confidence: ConfidenceLevel = field(init=False)
    explanation: str = ""

    def __post_init__(self):
        """Calculate overall confidence based on components."""
        self.overall_confidence = self._calculate_confidence()

    def _calculate_confidence(self) -> ConfidenceLevel:
        """
        Calculate overall confidence level.

        Starts at HIGH and downgrades based on concerns.
        """
        score = 4  # Start at high

        # Methodological limitations
        if self.methodological_limitations == "serious":
            score -= 2
        elif self.methodological_limitations == "moderate":
            score -= 1

        # Coherence
        if self.coherence == "low":
            score -= 2
        elif self.coherence == "moderate":
            score -= 1

        # Adequacy
        if self.adequacy == "very_limited":
            score -= 2
        elif self.adequacy == "limited":
            score -= 1

        # Relevance
        if self.relevance == "low":
            score -= 2
        elif self.relevance == "moderate":
            score -= 1

        if score >= 4:
            return ConfidenceLevel.HIGH
        elif score >= 3:
            return ConfidenceLevel.MODERATE
        elif score >= 2:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW


class GRADECERQual:
    """
    Implements GRADE-CERQual methodology for assessing
    confidence in qualitative evidence synthesis.
    """

    def __init__(self, database: StudyDatabase):
        """Initialize with study database."""
        self.db = database
        self.assessments: List[CERQualAssessment] = []

    def assess_finding(
        self,
        finding: str,
        axis: ThematicAxis,
        study_ids: List[int],
        meth_limitations: str = "minor",
        coherence: str = "high",
        adequacy: str = "adequate",
        relevance: str = "high",
        explanation: str = ""
    ) -> CERQualAssessment:
        """
        Assess confidence in a review finding.

        Args:
            finding: Description of the finding
            axis: Thematic axis
            study_ids: IDs of studies supporting the finding
            meth_limitations: Level of methodological limitations
            coherence: Level of coherence across studies
            adequacy: Adequacy of data
            relevance: Relevance to review question
            explanation: Additional explanation

        Returns:
            CERQualAssessment with calculated confidence
        """
        assessment = CERQualAssessment(
            finding=finding,
            axis=axis,
            supporting_studies=study_ids,
            methodological_limitations=meth_limitations,
            coherence=coherence,
            adequacy=adequacy,
            relevance=relevance,
            explanation=explanation
        )
        self.assessments.append(assessment)
        return assessment

    def get_ehds_assessments(self) -> List[CERQualAssessment]:
        """
        Return pre-configured GRADE-CERQual assessments for EHDS findings.

        Based on the systematic review results.
        """
        # Pre-configured assessments matching the paper
        assessments = [
            CERQualAssessment(
                finding="Governance tensions between secondary use promotion and rights protection",
                axis=ThematicAxis.GOVERNANCE_RIGHTS_ETHICS,
                supporting_studies=list(range(1, 19)),
                methodological_limitations="minor",
                coherence="high",
                adequacy="adequate",
                relevance="high",
                explanation="11 high-quality studies with convergent conclusions"
            ),
            CERQualAssessment(
                finding="PET maturity gap: 23% FL production deployment",
                axis=ThematicAxis.SECONDARY_USE_PETS,
                supporting_studies=list(range(19, 34)),
                methodological_limitations="moderate",
                coherence="high",
                adequacy="limited",
                relevance="high",
                explanation="Limited by small number of rigorous technical evaluations (n=4)"
            ),
            CERQualAssessment(
                finding="Nordic countries 2-3 years ahead in HDAB capacity",
                axis=ThematicAxis.NATIONAL_IMPLEMENTATION,
                supporting_studies=list(range(34, 43)),
                methodological_limitations="minor",
                coherence="high",
                adequacy="limited",
                relevance="high",
                explanation="Limited empirical data on actual implementation trajectories"
            ),
            CERQualAssessment(
                finding="Citizen engagement predominantly symbolic (3/52 participatory)",
                axis=ThematicAxis.CITIZEN_ENGAGEMENT,
                supporting_studies=list(range(43, 49)),
                methodological_limitations="minor",
                coherence="high",
                adequacy="adequate",
                relevance="high",
                explanation="Well-supported by 3 high-quality studies with convergent conclusions"
            ),
            CERQualAssessment(
                finding="Legal uncertainty re: FL compliance with GDPR/EHDS",
                axis=ThematicAxis.FEDERATED_LEARNING_AI,
                supporting_studies=list(range(49, 53)),
                methodological_limitations="minor",
                coherence="high",
                adequacy="limited",
                relevance="high",
                explanation="Limited by small evidence base (n=4) and rapidly evolving landscape"
            ),
        ]
        return assessments

    def generate_summary_table(self) -> List[Dict[str, Any]]:
        """
        Generate summary of findings table for GRADE-CERQual.

        Returns:
            List of dictionaries suitable for table rendering.
        """
        assessments = self.get_ehds_assessments()
        return [
            {
                "finding": a.finding,
                "studies": f"n={len(a.supporting_studies)}",
                "meth_limitations": a.methodological_limitations,
                "coherence": a.coherence,
                "adequacy": a.adequacy,
                "relevance": a.relevance,
                "confidence": a.overall_confidence.value.upper(),
                "explanation": a.explanation
            }
            for a in assessments
        ]
