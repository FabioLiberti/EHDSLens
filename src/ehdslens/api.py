"""
EHDSLens REST API
FastAPI-based REST API for programmatic access to EHDS systematic review data.
"""

from typing import List, Optional
from enum import Enum
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from .core import EHDSAnalyzer
from .data import ThematicAxis, QualityRating, StudyType, ConfidenceLevel


# ============================================================================
# Pydantic Models
# ============================================================================

class StudyResponse(BaseModel):
    """Study response model."""
    id: int
    authors: str
    year: int
    title: str
    journal: str
    study_type: str
    primary_axis: str
    quality_rating: str
    doi: Optional[str] = None
    country: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "authors": "Author A et al.",
                "year": 2024,
                "title": "Study on EHDS Implementation",
                "journal": "Journal of Health Informatics",
                "study_type": "qualitative",
                "primary_axis": "governance_rights_ethics",
                "quality_rating": "high",
                "doi": "10.1000/example",
                "country": "Germany"
            }
        }


class StatisticsResponse(BaseModel):
    """Statistics response model."""
    total: int
    year_range: List[int]
    by_axis: dict
    by_quality: dict
    by_type: dict


class AxisAnalysisResponse(BaseModel):
    """Axis analysis response model."""
    axis: str
    total_studies: int
    themes: List[str]
    quality_distribution: dict
    year_distribution: dict


class GRADECERQualFinding(BaseModel):
    """GRADE-CERQual finding model."""
    finding: str
    confidence: str
    studies: int


class SearchResponse(BaseModel):
    """Search response model."""
    query: str
    count: int
    results: List[StudyResponse]


class HypothesesResponse(BaseModel):
    """Hypotheses response model."""
    categories: dict


class ResearchGapsResponse(BaseModel):
    """Research gaps response model."""
    gaps: List[str]


class PRISMAResponse(BaseModel):
    """PRISMA flow diagram data."""
    identification: dict
    screening: dict
    eligibility: dict
    included: dict


class CitationResponse(BaseModel):
    """Citation response model."""
    study_id: int
    style: str
    citation: str


class BibliographyResponse(BaseModel):
    """Bibliography response model."""
    format: str
    count: int
    content: str


# ============================================================================
# API Application
# ============================================================================

# Initialize FastAPI app
app = FastAPI(
    title="EHDSLens API",
    description="""
## European Health Data Space - Systematic Literature Review API

This API provides programmatic access to the EHDS systematic review dataset
containing 52 peer-reviewed studies and grey literature.

### Features
- 📊 **Statistics**: Get overview statistics of the review
- 📚 **Studies**: Browse, search, and filter studies
- 🔬 **Analysis**: Thematic analysis by axis
- 📈 **GRADE-CERQual**: Confidence assessments for findings
- 📝 **Export**: Generate citations and bibliographies

### Thematic Axes
1. Governance, Rights & Ethics
2. Secondary Use & PETs
3. National Implementation
4. Citizen Engagement
5. Federated Learning & AI
    """,
    version="1.0.0",
    contact={
        "name": "Fabio Liberti",
        "email": "fxlybs@gmail.com",
        "url": "https://github.com/FabioLiberti/EHDSLens"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzer at startup
analyzer = EHDSAnalyzer()
analyzer.load_default_data()


# ============================================================================
# Helper Functions
# ============================================================================

def study_to_response(study) -> StudyResponse:
    """Convert Study object to response model."""
    return StudyResponse(
        id=study.id,
        authors=study.authors,
        year=study.year,
        title=study.title,
        journal=study.journal,
        study_type=study.study_type.value,
        primary_axis=study.primary_axis.value,
        quality_rating=study.quality_rating.value,
        doi=study.doi,
        country=study.country
    )


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """API root endpoint."""
    return {
        "message": "Welcome to EHDSLens API",
        "version": "1.0.0",
        "documentation": "/docs",
        "studies": len(analyzer.db)
    }


@app.get("/health", tags=["Root"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "studies_loaded": len(analyzer.db)}


# ----------------------------------------------------------------------------
# Statistics
# ----------------------------------------------------------------------------

@app.get("/statistics", response_model=StatisticsResponse, tags=["Statistics"])
async def get_statistics():
    """
    Get comprehensive statistics about the systematic review database.

    Returns counts by year, thematic axis, quality rating, and study type.
    """
    stats = analyzer.get_statistics()
    return StatisticsResponse(
        total=stats['total'],
        year_range=list(stats['year_range']),
        by_axis=stats['by_axis'],
        by_quality=stats['by_quality'],
        by_type=stats['by_type']
    )


# ----------------------------------------------------------------------------
# Studies
# ----------------------------------------------------------------------------

@app.get("/studies", response_model=List[StudyResponse], tags=["Studies"])
async def get_studies(
    axis: Optional[str] = Query(None, description="Filter by thematic axis"),
    quality: Optional[str] = Query(None, description="Minimum quality rating (high, moderate, low)"),
    year_start: Optional[int] = Query(None, description="Minimum publication year"),
    year_end: Optional[int] = Query(None, description="Maximum publication year"),
    study_type: Optional[str] = Query(None, description="Filter by study type"),
    limit: int = Query(100, ge=1, le=100, description="Maximum results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip")
):
    """
    Get all studies with optional filtering.

    Supports filtering by thematic axis, quality rating, year range, and study type.
    """
    # Parse filters
    axis_enum = None
    if axis:
        try:
            axis_enum = ThematicAxis(axis)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid axis: {axis}")

    quality_enum = None
    if quality:
        try:
            quality_enum = QualityRating(quality)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid quality: {quality}")

    type_enum = None
    if study_type:
        try:
            type_enum = StudyType(study_type)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid study_type: {study_type}")

    # Filter studies
    filtered = analyzer.filter_studies(
        axis=axis_enum,
        year_start=year_start,
        year_end=year_end,
        min_quality=quality_enum,
        study_type=type_enum
    )

    # Apply pagination
    paginated = filtered[offset:offset + limit]

    return [study_to_response(s) for s in paginated]


@app.get("/studies/{study_id}", response_model=StudyResponse, tags=["Studies"])
async def get_study(study_id: int):
    """
    Get a specific study by ID.
    """
    study = analyzer.db.get_study(study_id)
    if not study:
        raise HTTPException(status_code=404, detail=f"Study {study_id} not found")
    return study_to_response(study)


@app.get("/studies/{study_id}/citation", response_model=CitationResponse, tags=["Studies"])
async def get_study_citation(
    study_id: int,
    style: str = Query("apa", description="Citation style: apa or vancouver")
):
    """
    Get citation for a specific study.
    """
    study = analyzer.db.get_study(study_id)
    if not study:
        raise HTTPException(status_code=404, detail=f"Study {study_id} not found")

    if style not in ["apa", "vancouver"]:
        raise HTTPException(status_code=400, detail="Style must be 'apa' or 'vancouver'")

    return CitationResponse(
        study_id=study_id,
        style=style,
        citation=study.get_citation(style=style)
    )


# ----------------------------------------------------------------------------
# Search
# ----------------------------------------------------------------------------

@app.get("/search", response_model=SearchResponse, tags=["Search"])
async def search_studies(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(50, ge=1, le=100, description="Maximum results")
):
    """
    Search studies by keyword.

    Searches across authors, titles, and journals.
    """
    results = analyzer.search_studies(q)[:limit]

    return SearchResponse(
        query=q,
        count=len(results),
        results=[study_to_response(s) for s in results]
    )


# ----------------------------------------------------------------------------
# Analysis
# ----------------------------------------------------------------------------

@app.get("/analysis/axes", tags=["Analysis"])
async def get_axes():
    """
    Get list of all thematic axes.
    """
    return {
        "axes": [
            {
                "id": a.value,
                "name": a.value.replace('_', ' ').title(),
                "studies": len(analyzer.db.filter_by_axis(a))
            }
            for a in ThematicAxis
        ]
    }


@app.get("/analysis/axes/{axis}", response_model=AxisAnalysisResponse, tags=["Analysis"])
async def analyze_axis(axis: str):
    """
    Get detailed analysis for a specific thematic axis.
    """
    try:
        axis_enum = ThematicAxis(axis)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid axis: {axis}")

    analysis = analyzer.analyze_axis(axis_enum)

    return AxisAnalysisResponse(
        axis=axis,
        total_studies=analysis['total_studies'],
        themes=analysis['themes'],
        quality_distribution=analysis['quality_distribution'],
        year_distribution=analysis['year_distribution']
    )


# ----------------------------------------------------------------------------
# GRADE-CERQual
# ----------------------------------------------------------------------------

@app.get("/grade-cerqual", response_model=List[GRADECERQualFinding], tags=["GRADE-CERQual"])
async def get_grade_cerqual():
    """
    Get GRADE-CERQual confidence assessments for key findings.
    """
    findings = analyzer.get_grade_cerqual_summary()
    return [
        GRADECERQualFinding(
            finding=f['finding'],
            confidence=f['confidence'],
            studies=f['studies']
        )
        for f in findings
    ]


@app.get("/grade-cerqual/{confidence}", response_model=List[GRADECERQualFinding], tags=["GRADE-CERQual"])
async def get_findings_by_confidence(confidence: str):
    """
    Get findings filtered by confidence level.
    """
    valid_levels = ['high', 'moderate', 'low', 'very_low']
    if confidence not in valid_levels:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid confidence level. Must be one of: {valid_levels}"
        )

    findings = analyzer.get_grade_cerqual_summary()
    filtered = [f for f in findings if f['confidence'] == confidence]

    return [
        GRADECERQualFinding(
            finding=f['finding'],
            confidence=f['confidence'],
            studies=f['studies']
        )
        for f in filtered
    ]


# ----------------------------------------------------------------------------
# Research Gaps & Hypotheses
# ----------------------------------------------------------------------------

@app.get("/research-gaps", response_model=ResearchGapsResponse, tags=["Research"])
async def get_research_gaps():
    """
    Get identified research gaps from the systematic review.
    """
    gaps = analyzer.get_research_gaps()
    return ResearchGapsResponse(gaps=gaps)


@app.get("/hypotheses", response_model=HypothesesResponse, tags=["Research"])
async def get_hypotheses():
    """
    Get testable hypotheses organized by category.
    """
    hypotheses = analyzer.get_testable_hypotheses()
    return HypothesesResponse(categories=hypotheses)


# ----------------------------------------------------------------------------
# PRISMA
# ----------------------------------------------------------------------------

@app.get("/prisma", response_model=PRISMAResponse, tags=["PRISMA"])
async def get_prisma_data():
    """
    Get PRISMA 2020 flow diagram data.
    """
    from .visualization import EHDSVisualizer
    viz = EHDSVisualizer(analyzer.db)
    prisma = viz.create_prisma_diagram_data()
    return PRISMAResponse(**prisma)


# ----------------------------------------------------------------------------
# Export
# ----------------------------------------------------------------------------

@app.get("/export/bibliography", response_model=BibliographyResponse, tags=["Export"])
async def export_bibliography(
    format: str = Query("bibtex", description="Format: bibtex, ris, apa, or vancouver")
):
    """
    Export full bibliography in specified format.
    """
    valid_formats = ['bibtex', 'ris', 'apa', 'vancouver']
    if format not in valid_formats:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid format. Must be one of: {valid_formats}"
        )

    from .export import ReportGenerator
    reporter = ReportGenerator(analyzer.db)
    content = reporter.generate_bibliography(format=format)

    return BibliographyResponse(
        format=format,
        count=len(analyzer.db),
        content=content
    )


# ============================================================================
# Main
# ============================================================================

def run_api(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Run the API server."""
    uvicorn.run(
        "ehdslens.api:app",
        host=host,
        port=port,
        reload=reload
    )


if __name__ == "__main__":
    run_api()
