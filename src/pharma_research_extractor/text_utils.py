"""
Text processing utilities for the pharma research extractor.

Contains functions for processing and analyzing text data from research papers.
"""

from .config import ACADEMIC_KEYWORDS


def is_academic_affiliation(affil: str) -> bool:
    """
    Determine if an affiliation string represents an academic institution.
    
    Uses keyword matching to identify universities, hospitals, research institutes,
    and other academic organizations that should be filtered out from industry research.
    
    Args:
        affil: The affiliation string to check (e.g., "Harvard Medical School")
        
    Returns:
        True if the affiliation appears to be academic, False if it appears to be industry
        
    Example:
        >>> is_academic_affiliation("Harvard University")
        True
        >>> is_academic_affiliation("Pfizer Inc.")
        False
    """
    affil = affil.lower()  # Case-insensitive matching
    # Return True if any academic keyword is found in the affiliation string
    return any(keyword in affil for keyword in ACADEMIC_KEYWORDS)


def extract_email(affil_text: str) -> str:
    """
    Extract email address from affiliation text.
    
    Searches through affiliation text to find email addresses, which often
    indicate corresponding authors for potential collaboration contacts.
    
    Args:
        affil_text: The affiliation text that may contain an email address
        
    Returns:
        The first email address found, or empty string if none found
        
    Example:
        >>> extract_email("Pfizer Inc., contact: john.doe@pfizer.com")
        "john.doe@pfizer.com"
    """
    if not affil_text:
        return ""
    
    # Split text into words and look for email patterns
    for word in affil_text.split():
        if "@" in word and "." in word:  # Basic email pattern check
            # Strip common punctuation that might surround the email
            return word.strip(";.,()<>")
    return ""


def clean_title(title: str) -> str:
    """
    Clean and normalize article titles.
    
    Args:
        title: Raw article title from PubMed
        
    Returns:
        Cleaned title string
    """
    if not title:
        return "N/A"
    return title.strip()


def format_publication_date(year: str, month: str, day: str) -> str:
    """
    Format publication date components into standardized format.
    
    Args:
        year: Publication year
        month: Publication month
        day: Publication day
        
    Returns:
        Formatted date string in YYYY-MM-DD format
    """
    date_parts = [year, month, day]
    # Filter out empty parts and join with dashes
    return "-".join(part for part in date_parts if part).strip("-")
