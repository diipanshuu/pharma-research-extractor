# Pharma Research Extractor

A Python command-line tool that searches PubMed for research papers and extracts publications with non-academic (industry/company) affiliations. This tool is particularly useful for identifying pharmaceutical and biotech industry research publications.

## Features

- 🔍 Search PubMed database using custom queries
- 🏢 Automatically identify non-academic affiliations (companies, corporations, industry)
- 📧 Extract corresponding author email addresses
- 📊 Export results to CSV format
- 🎨 Rich console output with colors and formatting
- 🐛 Debug mode for troubleshooting

## Installation

### Prerequisites

- Python 3.13 or higher
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

# Activate the virtual environment
poetry shell
```

#### Using pip

```bash
# Clone the repository
git clone <your-repo-url>
cd pharma_research_extractor

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Usage

### Command Line Interface

The tool provides a simple command-line interface:

```bash
get-papers-list "your search query" [OPTIONS]
```

### Basic Usage

```bash
# Search for acne-related pharmaceutical research
get-papers-list "acne AND pharmaceutical"

# Search with custom output file
get-papers-list "diabetes drug development" --file diabetes_research.csv

# Enable debug mode for detailed logging
get-papers-list "cancer immunotherapy" --debug
```

### Options

- `query` (required): PubMed search query string
- `--file`: Output CSV filename (default: `output.csv`)
- `--debug`: Enable debug logging for troubleshooting

### Search Query Examples

```bash
# Disease-specific research
get-papers-list "alzheimer AND drug development"

# Company-specific research
get-papers-list "pfizer OR novartis OR roche"

# Therapeutic area research
get-papers-list "oncology AND clinical trial"

# Time-limited search
get-papers-list "covid-19 vaccine AND 2023[PDAT]"
```

## Output Format

The tool generates a CSV file with the following columns:

| Column | Description |
|--------|-------------|
| PubmedID | Unique PubMed identifier |
| Title | Article title |
| Publication Date | Publication date (YYYY-MM-DD format) |
| Non-academicAuthor(s) | Authors with non-academic affiliations |
| CompanyAffiliation(s) | Company/industry affiliations |
| Corresponding Author Email | Email address of corresponding author |

### Sample Output

```csv
PubmedID,Title,Publication Date,Non-academicAuthor(s),CompanyAffiliation(s),Corresponding Author Email
12345678,"Novel acne treatment approaches","2023-06-15","John Smith; Jane Doe","Pharma Corp; BioTech Inc","john.smith@pharmacorp.com"
```

## Academic vs Non-Academic Classification

The tool automatically classifies affiliations as academic or non-academic based on keywords:

### Academic Keywords (Filtered Out)
- school, university, college, institute
- department, faculty, academy, center
- hospital, medical, clinic, laboratory
- professor, lecturer, phd, student
- And more...

### Non-Academic (Included)
- Pharmaceutical companies
- Biotechnology firms
- Contract research organizations
- Medical device companies
- Other industry affiliations

## Development

### Project Structure

```
pharma_research_extractor/
├── src/
│   └── pharma_research_extractor/
│       ├── __init__.py
│       └── cli.py              # Main CLI application
├── tests/
│   └── __init__.py
├── pyproject.toml              # Project configuration
├── poetry.lock                 # Dependency lock file
└── README.md                   # This file
```

### Dependencies

- **requests**: HTTP library for API calls
- **typer**: Modern CLI framework
- **rich**: Rich text and beautiful formatting

### Running Tests

```bash
# Using poetry
poetry run pytest

# Using pip
python -m pytest
```

### Building and Publishing

#### Publishing to TestPyPI

```bash
# Build the package
poetry build

# Configure TestPyPI repository (one time setup)
poetry config repositories.testpypi https://test.pypi.org/legacy/

# Publish to TestPyPI
poetry publish -r testpypi

# Or using twine
pip install twine
twine upload --repository testpypi dist/*
```

#### Publishing to PyPI (Production)

```bash
# Build the package
poetry build

# Publish to PyPI
poetry publish

# Or using twine
twine upload dist/*
```

**Note**: Make sure to update the version in `pyproject.toml` before publishing.

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## API Usage

The PubMed E-utilities API is used for data retrieval:

- **Rate Limiting**: Please be respectful of NCBI's servers
- **Query Limits**: Default maximum of 50 results per query
- **Search Syntax**: Uses standard PubMed search syntax

For more information on PubMed search syntax, visit: https://pubmed.ncbi.nlm.nih.gov/help/

## Troubleshooting

### Common Issues

1. **No results found**: Check your search query syntax
2. **Network errors**: Verify internet connection and try again
3. **XML parsing errors**: Enable debug mode to see detailed error messages

### Debug Mode

Enable debug mode to see detailed logging:

```bash
get-papers-list "your query" --debug
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

**Author**: diipanshuu  
**Email**: diipanshuu@gmail.com

## Acknowledgments

- PubMed/NCBI for providing the E-utilities API
- The Python community for excellent libraries (typer, rich, requests)