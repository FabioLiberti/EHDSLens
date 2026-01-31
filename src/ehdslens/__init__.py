"""
EHDSLens - European Health Data Space Literature Analysis Toolkit

A comprehensive Python toolkit for systematic literature review analysis
of the European Health Data Space (EHDS) regulatory framework.

Based on the methodology described in:
Liberti, F. (2026). The European Health Data Space: A Systematic Literature Review.
Journal of Medical Internet Research.

Author: Fabio Liberti, PhD
Institution: Universitas Mercatorum, Rome, Italy
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Fabio Liberti"
__email__ = "fabio.liberti@unimercatorum.it"

from .core import EHDSAnalyzer
from .data import StudyDatabase, Study
from .analysis import ThematicAnalyzer, QualityAssessor, GRADECERQual
from .visualization import EHDSVisualizer
from .export import ReportGenerator

__all__ = [
    "EHDSAnalyzer",
    "StudyDatabase",
    "Study",
    "ThematicAnalyzer",
    "QualityAssessor",
    "GRADECERQual",
    "EHDSVisualizer",
    "ReportGenerator"
]
