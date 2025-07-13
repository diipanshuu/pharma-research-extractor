"""
Input validation utilities for the pharma research extractor.

Provides comprehensive validation for user inputs, API responses,
and configuration parameters to ensure robustness.
"""

import re
from typing import Any, Dict, List
from .exceptions import ValidationError


class InputValidator:
    """
    Validates user inputs and API responses to ensure data integrity.
    """
    
    @staticmethod
    def validate_query(query: str) -> str:
        """
        Validate and sanitize PubMed search query.
        
        Args:
            query: User-provided search query
            
        Returns:
            Sanitized query string
            
        Raises:
            ValidationError: If query is invalid
        """
        if not query:
            raise ValidationError("Search query cannot be empty")
        
        if not isinstance(query, str):
            raise ValidationError("Search query must be a string")
        
        # Remove leading/trailing whitespace
        query = query.strip()
        
        if len(query) < 2:
            raise ValidationError("Search query must be at least 2 characters long")
        
        if len(query) > 1000:
            raise ValidationError("Search query cannot exceed 1000 characters")
        
        # Check for potentially problematic characters
        dangerous_chars = ['<', '>', '"', "'", '&', '\x00']
        for char in dangerous_chars:
            if char in query:
                raise ValidationError(f"Search query contains invalid character: {char}")
        
        return query
    
    @staticmethod
    def validate_filename(filename: str) -> str:
        """
        Validate output filename.
        
        Args:
            filename: User-provided filename
            
        Returns:
            Validated filename
            
        Raises:
            ValidationError: If filename is invalid
        """
        if not filename:
            raise ValidationError("Filename cannot be empty")
        
        if not isinstance(filename, str):
            raise ValidationError("Filename must be a string")
        
        # Remove leading/trailing whitespace
        filename = filename.strip()
        
        # Check for invalid filename characters (Windows/Unix)
        invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
        if re.search(invalid_chars, filename):
            raise ValidationError("Filename contains invalid characters")
        
        # Check filename length
        if len(filename) > 255:
            raise ValidationError("Filename cannot exceed 255 characters")
        
        # Ensure file has an extension
        if '.' not in filename:
            raise ValidationError("Filename must include an extension (e.g., .csv, .json)")
        
        return filename
    
    @staticmethod
    def validate_format(format_type: str) -> str:
        """
        Validate output format.
        
        Args:
            format_type: User-specified output format
            
        Returns:
            Validated format string
            
        Raises:
            ValidationError: If format is unsupported
        """
        if not format_type:
            raise ValidationError("Output format cannot be empty")
        
        format_type = format_type.lower().strip()
        
        supported_formats = ['csv', 'json']
        if format_type not in supported_formats:
            raise ValidationError(
                f"Unsupported format '{format_type}'. "
                f"Supported formats: {', '.join(supported_formats)}"
            )
        
        return format_type
    
    @staticmethod
    def validate_api_response(response_data: Any, expected_fields: List[str]) -> None:
        """
        Validate API response structure.
        
        Args:
            response_data: Response data to validate
            expected_fields: List of required fields
            
        Raises:
            ValidationError: If response structure is invalid
        """
        if response_data is None:
            raise ValidationError("API response is None")
        
        if not isinstance(response_data, dict):
            raise ValidationError("API response must be a dictionary")
        
        missing_fields = [field for field in expected_fields if field not in response_data]
        if missing_fields:
            raise ValidationError(f"API response missing required fields: {missing_fields}")
    
    @staticmethod
    def validate_article_data(article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and sanitize article data.
        
        Args:
            article: Article data dictionary
            
        Returns:
            Validated article data
            
        Raises:
            ValidationError: If article data is invalid
        """
        if not isinstance(article, dict):
            raise ValidationError("Article data must be a dictionary")
        
        # Ensure required fields exist with defaults
        validated_article = {
            "PubmedID": str(article.get("PubmedID", "N/A")).strip(),
            "Title": str(article.get("Title", "N/A")).strip(),
            "Publication Date": str(article.get("Publication Date", "")).strip(),
            "Non-academicAuthor(s)": str(article.get("Non-academicAuthor(s)", "")).strip(),
            "CompanyAffiliation(s)": str(article.get("CompanyAffiliation(s)", "")).strip(),
            "Corresponding Author Email": str(article.get("Corresponding Author Email", "")).strip()
        }
        
        # Validate PubMed ID format (should be numeric)
        pmid = validated_article["PubmedID"]
        if pmid != "N/A" and not pmid.isdigit():
            raise ValidationError(f"Invalid PubMed ID format: {pmid}")
        
        # Validate email format if present
        email = validated_article["Corresponding Author Email"]
        if email and email != "N/A":
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                # Don't fail validation, just clear invalid email
                validated_article["Corresponding Author Email"] = ""
        
        return validated_article
    
    @staticmethod
    def validate_batch_size(batch_size: int, min_size: int = 1, max_size: int = 100) -> int:
        """
        Validate API batch size parameters.
        
        Args:
            batch_size: Requested batch size
            min_size: Minimum allowed size
            max_size: Maximum allowed size
            
        Returns:
            Validated batch size
            
        Raises:
            ValidationError: If batch size is invalid
        """
        if not isinstance(batch_size, int):
            raise ValidationError("Batch size must be an integer")
        
        if batch_size < min_size:
            raise ValidationError(f"Batch size must be at least {min_size}")
        
        if batch_size > max_size:
            raise ValidationError(f"Batch size cannot exceed {max_size}")
        
        return batch_size
