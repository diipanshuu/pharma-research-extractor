"""
Pharma Research Extractor

A Python package for extracting pharmaceutical research papers with non-academic
affiliations from PubMed.
"""

from .pubmed_client import PubMedClient
from .output import OutputWriter
from .exceptions import (
    PharmaExtractorError,
    ValidationError,
    PubMedAPIError,
    NetworkError,
    DataProcessingError,
    OutputError,
    ConfigurationError
)

__version__ = "0.1.1"
__author__ = "diipanshuu"

# Expose main API for programmatic use
__all__ = [
    "PubMedClient",
    "OutputWriter",
    "PharmaExtractorError",
    "ValidationError", 
    "PubMedAPIError",
    "NetworkError",
    "DataProcessingError",
    "OutputError",
    "ConfigurationError"
]