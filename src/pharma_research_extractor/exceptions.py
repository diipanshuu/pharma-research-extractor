"""
Custom exceptions for the pharma research extractor.

Provides specific exception types for different error scenarios
to enable better error handling and user feedback.
"""


class PharmaExtractorError(Exception):
    """Base exception for all pharma extractor errors."""
    pass


class ValidationError(PharmaExtractorError):
    """Raised when input validation fails."""
    pass


class PubMedAPIError(PharmaExtractorError):
    """Raised when PubMed API interactions fail."""
    pass


class DataProcessingError(PharmaExtractorError):
    """Raised when data processing or parsing fails."""
    pass


class OutputError(PharmaExtractorError):
    """Raised when output operations fail."""
    pass


class NetworkError(PharmaExtractorError):
    """Raised when network-related operations fail."""
    pass


class ConfigurationError(PharmaExtractorError):
    """Raised when configuration is invalid."""
    pass
