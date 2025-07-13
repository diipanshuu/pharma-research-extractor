"""
PubMed API client for the pharma research extractor.

Handles all interactions with the PubMed E-utilities API including
search operations and data retrieval with comprehensive error handling.
"""

from typing import List, Tuple, Dict, Any
import requests
import xml.etree.ElementTree as ET
from rich.console import Console
import time

from .config import PUBMED_SEARCH_URL, PUBMED_FETCH_URL, DEFAULT_SEARCH_LIMIT
from .text_utils import is_academic_affiliation, extract_email, clean_title, format_publication_date
from .exceptions import PubMedAPIError, NetworkError, DataProcessingError
from .validation import InputValidator

console = Console()


class PubMedClient:
    """
    Client for interacting with PubMed E-utilities API.
    
    Provides methods for searching PubMed and retrieving detailed article information
    using the efficient history-based approach recommended by NCBI.
    """
    
    def __init__(self):
        """Initialize the PubMed client."""
        self.session = requests.Session()
        # Set a user agent to be respectful to NCBI servers
        self.session.headers.update({
            'User-Agent': 'pharma-research-extractor/0.1.1 (https://github.com/your-repo)'
        })
    
    def search(self, query: str, retmax: int = DEFAULT_SEARCH_LIMIT) -> Tuple[str, str]:
        """
        Search PubMed and return session identifiers for efficient result retrieval.
        
        Uses PubMed's E-utilities API with history server to enable efficient
        batch retrieval of search results. This is the recommended approach
        for retrieving multiple records.
        
        Args:
            query: PubMed search query string (e.g., "acne AND pharmaceutical")
            retmax: Maximum number of results to retrieve (default from config)
            
        Returns:
            Tuple containing (query_key, webenv) for use in subsequent API calls
            
        Raises:
            PubMedAPIError: If the API response is invalid or missing required data
            NetworkError: If network connectivity issues occur
            ValidationError: If input parameters are invalid
        """
        # Validate inputs
        query = InputValidator.validate_query(query)
        retmax = InputValidator.validate_batch_size(retmax, min_size=1, max_size=10000)
        
        max_retries = 3
        retry_delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                params = {
                    "db": "pubmed",
                    "term": query,
                    "retmode": "xml",
                    "usehistory": "y",  # Store results on NCBI server for efficient retrieval
                    "retmax": retmax,
                    "tool": "pharma-research-extractor",  # Identify our tool
                    "email": "diipanshuu@gmail.com"  # Contact info as requested by NCBI
                }
                
                # Add timeout to prevent hanging
                response = self.session.get(
                    PUBMED_SEARCH_URL, 
                    params=params, 
                    timeout=30
                )
                response.raise_for_status()  # Raise exception for HTTP errors
                
                # Validate response content
                if not response.text:
                    raise PubMedAPIError("Empty response from PubMed API")
                
                # Parse XML response to extract session identifiers
                try:
                    root = ET.fromstring(response.text)
                except ET.ParseError as e:
                    raise DataProcessingError(f"Failed to parse XML response: {e}")
                
                # Check for API errors in response
                error_list = root.find(".//ErrorList")
                if error_list is not None:
                    errors = [error.text for error in error_list.findall(".//PhraseNotFound")]
                    if errors:
                        raise PubMedAPIError(f"PubMed query errors: {'; '.join(errors)}")
                
                query_key = root.findtext("QueryKey")
                webenv = root.findtext("WebEnv")
                count = root.findtext("Count")
                
                if not query_key or not webenv:
                    raise PubMedAPIError("Missing QueryKey or WebEnv in API response")
                
                # Log search results for debugging
                if count:
                    console.log(f"[dim]Found {count} total papers in PubMed[/dim]")
                
                return query_key, webenv
                
            except requests.Timeout:
                if attempt < max_retries - 1:
                    console.log(f"[yellow]Request timeout, retrying in {retry_delay}s... (attempt {attempt + 1}/{max_retries})[/yellow]")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    raise NetworkError("Request timeout after multiple retries")
                    
            except requests.ConnectionError as e:
                if attempt < max_retries - 1:
                    console.log(f"[yellow]Connection error, retrying in {retry_delay}s... (attempt {attempt + 1}/{max_retries})[/yellow]")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    raise NetworkError(f"Network connection failed: {e}")
                    
            except requests.HTTPError as e:
                status_code = e.response.status_code if e.response else "Unknown"
                if status_code == 429:  # Rate limiting
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * 2
                        console.log(f"[yellow]Rate limited, waiting {wait_time}s before retry...[/yellow]")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise PubMedAPIError("Rate limit exceeded after multiple retries")
                elif status_code >= 500:  # Server errors
                    if attempt < max_retries - 1:
                        console.log(f"[yellow]Server error {status_code}, retrying in {retry_delay}s...[/yellow]")
                        time.sleep(retry_delay)
                        retry_delay *= 2
                        continue
                    else:
                        raise PubMedAPIError(f"Server error: {e}")
                else:
                    # Client errors (4xx) - don't retry
                    raise PubMedAPIError(f"HTTP error {status_code}: {e}")
                    
            except requests.RequestException as e:
                raise NetworkError(f"Request failed: {e}")
        
        # Should never reach here due to the loop structure, but just in case
        raise PubMedAPIError("Maximum retries exceeded")
    
    def fetch_details(self, query_key: str, webenv: str, retstart: int = 0, retmax: int = 20) -> List[Dict[str, Any]]:
        """
        Fetch detailed article information using stored search results.
        
        Retrieves full article details from PubMed using session identifiers
        from a previous search. This approach is much more efficient than
        making individual requests for each article.
        
        Args:
            query_key: Query identifier from search()
            webenv: Web environment identifier from search()
            retstart: Starting index for pagination (default: 0)
            retmax: Maximum number of records to fetch (default: 20)
            
        Returns:
            List of dictionaries containing article data for non-academic papers
            
        Raises:
            PubMedAPIError: If the API request fails or XML parsing fails
        """
        try:
            params = {
                "db": "pubmed",
                "query_key": query_key,    # Use stored search results
                "WebEnv": webenv,          # Session identifier
                "retstart": retstart,      # Enable pagination for large result sets
                "retmax": retmax,          # Batch size control
                "retmode": "xml"
            }
            response = self.session.get(PUBMED_FETCH_URL, params=params)
            response.raise_for_status()
            
            return self._parse_xml_response(response.text)
            
        except ET.ParseError as e:
            raise PubMedAPIError(f"Failed to parse XML response: {e}")
        except requests.RequestException as e:
            raise PubMedAPIError(f"HTTP request failed: {e}")
    
    def _parse_xml_response(self, xml_text: str) -> List[Dict[str, Any]]:
        """
        Parse PubMed XML response and extract non-academic research papers.
        
        Processes the XML response from PubMed's efetch API, extracting relevant
        information from each article and filtering to include only papers with
        non-academic (industry/company) author affiliations.
        
        Args:
            xml_text: Raw XML response from PubMed efetch API
            
        Returns:
            List of dictionaries containing structured article data
        """
        root = ET.fromstring(xml_text)
        results = []

        # Process each article in the XML response
        for article in root.findall(".//PubmedArticle"):
            article_data = self._extract_article_data(article)
            
            # Only include articles with at least one non-academic author
            if article_data["non_academic_authors"]:
                results.append({
                    "PubmedID": article_data["pmid"],
                    "Title": article_data["title"],
                    "Publication Date": article_data["pub_date"],
                    "Non-academicAuthor(s)": "; ".join(article_data["non_academic_authors"]),
                    "CompanyAffiliation(s)": "; ".join(article_data["affiliations"]),
                    "Corresponding Author Email": article_data["corresponding_email"]
                })

        return results
    
    def _extract_article_data(self, article: ET.Element) -> Dict[str, Any]:
        """
        Extract structured data from a single PubMed article XML element.
        
        Args:
            article: XML element representing a single PubMed article
            
        Returns:
            Dictionary containing extracted article data
        """
        # Extract basic article information
        pmid = article.findtext(".//PMID") or "N/A"
        title = clean_title(article.findtext(".//ArticleTitle"))

        # Parse publication date (may have year, month, day)
        pub_date_elem = article.find(".//PubDate")
        year = pub_date_elem.findtext("Year") or "" if pub_date_elem is not None else ""
        month = pub_date_elem.findtext("Month") or "" if pub_date_elem is not None else ""
        day = pub_date_elem.findtext("Day") or "" if pub_date_elem is not None else ""
        pub_date = format_publication_date(year, month, day)

        # Track non-academic authors and their affiliations
        non_academic_authors = []
        affiliations = []
        corresponding_email = ""

        # Process each author to check their affiliation
        for author in article.findall(".//Author"):
            author_data = self._extract_author_data(author)
            
            if author_data["email"] and not corresponding_email:
                corresponding_email = author_data["email"]

            # Check if this is a non-academic affiliation
            if author_data["affiliation"] and not is_academic_affiliation(author_data["affiliation"]):
                non_academic_authors.append(author_data["full_name"])
                affiliations.append(author_data["affiliation"])

        return {
            "pmid": pmid,
            "title": title,
            "pub_date": pub_date,
            "non_academic_authors": non_academic_authors,
            "affiliations": affiliations,
            "corresponding_email": corresponding_email
        }
    
    def _extract_author_data(self, author: ET.Element) -> Dict[str, str]:
        """
        Extract author information from XML element.
        
        Args:
            author: XML element representing a single author
            
        Returns:
            Dictionary containing author data
        """
        # Extract author name
        fore = author.findtext("ForeName") or ""
        last = author.findtext("LastName") or ""
        full_name = f"{fore} {last}".strip()

        # Extract affiliation information
        affil_elem = author.find(".//AffiliationInfo/Affiliation")
        affiliation = affil_elem.text.strip() if affil_elem is not None else ""
        
        # Try to extract email from affiliation text
        email = extract_email(affiliation) if affiliation else ""

        return {
            "full_name": full_name,
            "affiliation": affiliation,
            "email": email
        }
