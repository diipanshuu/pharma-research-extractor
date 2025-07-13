"""
Configuration module for the pharma research extractor.

Contains constants and configuration settings used throughout the application.
"""

# Keywords used to identify academic institutions
# These terms commonly appear in university, hospital, and research institution names
ACADEMIC_KEYWORDS = [
    "school", "university", "college", "institute", "department", "faculty",
    "academy", "center", "centre", "hospital", "medical", "clinic", "grad",
    "postdoc", "fellow", "professor", "lecturer", "phd", "student", "library",
    "conservatory", "polytechnic", "laboratory", "lab"
]

# PubMed API configuration
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/eutils/efetch.fcgi"

# Default batch sizes for API calls
DEFAULT_SEARCH_LIMIT = 20
DEFAULT_FETCH_LIMIT = 50

# CSV output configuration
CSV_FIELDNAMES = [
    "PubmedID", "Title", "Publication Date",
    "Non-academicAuthor(s)", "CompanyAffiliation(s)", "Corresponding Author Email"
]
