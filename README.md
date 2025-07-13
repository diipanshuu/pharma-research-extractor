# Pharma Research Extractor

A Python package for extracting pharmaceutical research papers with non-academic (industry/company) affiliations from PubMed. Provides both a **Python module** for programmatic use and a **command-line interface** for direct usage.

This tool is particularly useful for identifying pharmaceutical and biotech industry research publications, academic-industry collaborations, and corporate-sponsored research.

## Features

- 🔍 **Dual Interface**: Use as Python module or command-line tool
- 🔬 **PubMed Integration**: Search PubMed database using custom queries
- 🏢 **Smart Classification**: Automatically identify non-academic affiliations (companies, corporations, industry)
- 📧 **Contact Extraction**: Extract corresponding author email addresses
- 📊 **Multiple Formats**: Export results to CSV or JSON format
- 🎨 **Rich Output**: Beautiful console output with colors and progress indicators
- 🛡️ **Robust Error Handling**: Comprehensive validation and retry logic
- 🐛 **Debug Support**: Detailed logging for troubleshooting

## Installation

### Prerequisites

- Python 3.8 or higher
- pip or Poetry

### From TestPyPI (Recommended for Testing)

```bash
# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pharma-research-extractor
```

### From PyPI (When Available)

```bash
# Install from PyPI (when officially released)
pip install pharma-research-extractor
```

### From Source (Development)

#### Using Poetry (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd pharma_research_extractor

# Install dependencies
poetry install
```

#### Using pip

```bash
# Clone the repository
git clone <your-repo-url>
cd pharma_research_extractor

# Install in development mode
pip install -e .
```

## Usage

This package provides both a **Python module** for programmatic integration and a **command-line interface** for direct usage.

### 🐍 As a Python Module

Import and use the package in your Python code:

```python
from pharma_research_extractor import PubMedClient, OutputWriter

# Initialize the client
client = PubMedClient()

# Search for papers with industry affiliations
articles = client.search_and_extract(
    query="cancer treatment AND pharmaceutical", 
    max_results=10
)

print(f"Found {len(articles)} papers with industry affiliations")

# Save results in different formats
writer = OutputWriter()
writer.write_csv(articles, "cancer_industry_papers.csv")
writer.write_json(articles, "cancer_industry_papers.json")

# Access individual article data
for article in articles:
    print(f"Title: {article['Title']}")
    print(f"Companies: {article['CompanyAffiliation(s)']}")
    print(f"Non-academic Authors: {article['Non-academicAuthor(s)']}")
    print("---")
```

### 🖥️ Command Line Interface

The command-line tool provides a simple interface for direct usage:

```bash
get-papers-list "your search query" [OPTIONS]
```

#### Basic Usage Examples

```bash
# Basic search for pharmaceutical research
get-papers-list "acne AND pharmaceutical"

# Search with custom output file and format
get-papers-list "diabetes drug development" --file diabetes_research.csv --format csv

# JSON output format
get-papers-list "cancer immunotherapy" --file results.json --format json

# Enable debug mode for detailed logging
get-papers-list "alzheimer drug" --debug

# Limit number of results
get-papers-list "covid vaccine" --max-results 20
```

#### Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `query` | PubMed search query (required) | - |
| `--file` | Output filename | `output.csv` |
| `--format` | Output format: `csv` or `json` | `csv` |
| `--max-results` | Maximum number of results | `50` |
| `--debug` | Enable debug logging | `False` |

#### Advanced Search Examples

```bash
# Disease-specific research with industry involvement
get-papers-list "alzheimer AND drug development AND (company OR corporation)"

# Company-specific research
get-papers-list "pfizer OR novartis OR roche AND clinical trial"

# Therapeutic area research with time filter
get-papers-list "oncology AND pharmaceutical AND 2023[PDAT]"

# Large-scale analysis
get-papers-list "diabetes AND industry" --max-results 100 --format json
```

## 📊 Output Formats

### CSV Format
```csv
PubmedID,Title,Publication Date,Non-academicAuthor(s),CompanyAffiliation(s),Corresponding Author Email
12345678,"Novel acne treatment approaches","2023-06-15","John Smith; Jane Doe","Pharma Corp; BioTech Inc","john.smith@pharmacorp.com"
```

### JSON Format
```json
[
  {
    "PubmedID": "12345678",
    "Title": "Novel acne treatment approaches",
    "Publication Date": "2023-06-15",
    "Non-academicAuthor(s)": "John Smith; Jane Doe",
    "CompanyAffiliation(s)": "Pharma Corp; BioTech Inc", 
    "Corresponding Author Email": "john.smith@pharmacorp.com"
  }
]
```

## 🔬 Academic vs Non-Academic Classification

The tool uses intelligent keyword-based classification to distinguish between academic and industry affiliations:

### Academic Affiliations (Filtered Out)
- **Educational**: university, college, school, institute, academy
- **Medical**: hospital, medical center, clinic, laboratory
- **Research**: research center, department, faculty, lab
- **Personnel**: professor, lecturer, phd, student, researcher

### Non-Academic Affiliations (Included)
- **Pharmaceutical**: pharma, pharmaceutical, drug company
- **Biotechnology**: biotech, biotechnology, life sciences
- **Corporate**: corporation, company, inc, ltd, gmbh
- **Medical Devices**: medical device, diagnostics, equipment
- **Contract Research**: CRO, contract research organization

## 📦 Package Architecture

This package follows Python best practices with clear separation of concerns:

### Module Structure
```python
from pharma_research_extractor import PubMedClient, OutputWriter
# Main classes for programmatic use

from pharma_research_extractor.exceptions import PubMedAPIError, NetworkError  
# Exception handling

# CLI is separate: get-papers-list command
```

### Directory Layout
```
pharma_research_extractor/
├── pyproject.toml              # Package configuration  
├── README.md                   # This documentation
├── src/pharma_research_extractor/  # Source package
│   ├── __init__.py            # Package initialization & exports
│   ├── cli.py                 # Command-line interface
│   ├── pubmed_client.py       # PubMed API client
│   ├── output.py              # Output formatting (CSV/JSON)
│   ├── text_utils.py          # Text processing utilities
│   ├── validation.py          # Input validation
│   ├── exceptions.py          # Custom exceptions
│   └── config.py              # Configuration constants
└── tests/                     # Test suite
```

## 🛠️ Development & Contributing

### Dependencies

- **requests**: HTTP library for PubMed API calls
- **typer**: Modern CLI framework with rich features
- **rich**: Beautiful console output and progress indicators

### Installation for Development

```bash
# Clone the repository
git clone https://github.com/diipanshuu/pharma-research-extractor.git
cd pharma-research-extractor

# Install in development mode
pip install -e .

# Verify installation
get-papers-list --help
python -c "from pharma_research_extractor import PubMedClient; print('✅ Module import works')"
```

### Testing

```bash
# Run basic functionality test
python -c "
from pharma_research_extractor import PubMedClient
client = PubMedClient()
print('✅ Package ready for use')
"

# Test CLI
get-papers-list "test query" --max-results 1 --debug
```

### 📤 Publishing to TestPyPI

```bash
# Build the package
pip install build twine
python -m build

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pharma-research-extractor
```

### Contributing Guidelines

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
4. **Make** your changes with clear, focused commits
5. **Test** your changes thoroughly
6. **Commit** your changes (`git commit -m 'Add amazing feature'`)
7. **Push** to your branch (`git push origin feature/amazing-feature`)
8. **Open** a Pull Request with a clear description

## 🔧 API Reference

### PubMedClient

Main class for interacting with PubMed API:

```python
from pharma_research_extractor import PubMedClient

client = PubMedClient()
articles = client.search_and_extract(
    query="cancer AND pharmaceutical",
    max_results=50
)
```

### OutputWriter

Handle different output formats:

```python
from pharma_research_extractor import OutputWriter

writer = OutputWriter()
writer.write_csv(articles, "results.csv")
writer.write_json(articles, "results.json")
```

### Error Handling

```python
from pharma_research_extractor.exceptions import PubMedAPIError, NetworkError

try:
    articles = client.search_and_extract("your query")
except PubMedAPIError as e:
    print(f"PubMed API error: {e}")
except NetworkError as e:
    print(f"Network error: {e}")
```

## ❓ Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **No results found** | Verify your search query syntax using [PubMed](https://pubmed.ncbi.nlm.nih.gov/) |
| **Network errors** | Check internet connection; API may be temporarily unavailable |
| **Import errors** | Ensure package is installed: `pip install -e .` |
| **CLI not found** | Add Python Scripts directory to PATH |
| **Permission errors** | Check file write permissions for output directory |

### Debug Mode

Enable detailed logging to diagnose issues:

```bash
# CLI debug mode
get-papers-list "your query" --debug

# Python module debug mode
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help

1. **Check the logs** with `--debug` flag
2. **Verify installation** with `pip list | grep pharma`
3. **Test basic functionality**:
   ```bash
   python -c "from pharma_research_extractor import PubMedClient; print('✅ Working')"
   ```
4. **Check GitHub Issues** for similar problems
5. **Create a new issue** with debug output if needed

## 🌐 External Resources

- **PubMed Search Help**: https://pubmed.ncbi.nlm.nih.gov/help/
- **E-utilities API**: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- **Search Syntax Guide**: https://pubmed.ncbi.nlm.nih.gov/advanced/
- **MeSH Terms**: https://www.ncbi.nlm.nih.gov/mesh

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

**Author**: diipanshuu  
**Email**: diipanshuu@gmail.com

## Acknowledgments

- PubMed/NCBI for providing the E-utilities API
- The Python community for excellent libraries (typer, rich, requests)
