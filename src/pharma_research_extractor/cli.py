"""
Pharma Research Extractor - CLI Module

This module provides a command-line interface for searching PubMed publications
and extracting papers with non-academic (industry/company) affiliations.

The tool uses PubMed's E-utilities API to efficiently search and retrieve
publication data, then filters results to identify industry-sponsored research.
"""

from typing import Optional
import typer
from rich import print
from rich.console import Console

from .pubmed_client import PubMedClient
from .output import OutputWriter
from .config import DEFAULT_FETCH_LIMIT
from .exceptions import (
    PubMedAPIError, NetworkError, DataProcessingError, 
    OutputError, ValidationError
)
from .validation import InputValidator

# Initialize console for rich text output
console = Console()
app = typer.Typer(help="Extract pharmaceutical industry research from PubMed")

def run_cli():
    """Entry point for the CLI when installed as a package."""
    typer.run(main)


def main(
    query: str = typer.Argument(..., help="PubMed search query."),
    file: str = typer.Option(default="output.csv", help="Output CSV file name.", show_default=True),
    debug: bool = typer.Option(default=False, help="Enable debug logging."),
    format: str = typer.Option(default="csv", help="Output format: csv or json", show_default=True)
):
    """
    Search PubMed for pharmaceutical industry research publications.
    
    This tool searches PubMed using your query and extracts publications
    that have authors affiliated with non-academic institutions (companies,
    pharmaceutical firms, biotech organizations, etc.).
    
    Args:
        query: PubMed search query (e.g., "acne AND drug development")
        file: Output file name (default: output.csv)
        debug: Enable detailed logging for troubleshooting
        format: Output format - csv or json (default: csv)
        
    Examples:
        get-papers-list "acne AND pharmaceutical"
        get-papers-list "diabetes drug" --file diabetes.csv --debug
        get-papers-list "cancer research" --format json --file results.json
        
    Returns:
        Exits with code 0 on success, 1 on failure
    """
    if debug:
        console.log(f"[bold cyan]Running query:[/bold cyan] {query}")
        console.log(f"[bold cyan]Output format:[/bold cyan] {format}")
    
    try:
        # Validate inputs
        query = InputValidator.validate_query(query)
        filename = InputValidator.validate_filename(file)
        output_format = InputValidator.validate_format(format)
        
        if debug:
            console.log(f"[dim]Validated inputs: query='{query[:50]}...', file='{filename}', format='{output_format}'[/dim]")
        
        # Initialize PubMed client
        client = PubMedClient()
        
        # Step 1: Search PubMed and get session identifiers
        console.print("[blue]🔍 Searching PubMed...[/blue]")
        query_key, webenv = client.search(query)
        
        if debug:
            console.log(f"[cyan]Query Key: {query_key}, WebEnv: {webenv[:20]}...[/cyan]")
        
        # Step 2: Fetch detailed article information
        console.print("[blue]📥 Fetching article details...[/blue]")
        results = client.fetch_details(query_key, webenv, retmax=DEFAULT_FETCH_LIMIT)
        
        if debug:
            console.log(f"[cyan]Found {len(results)} papers with industry affiliations[/cyan]")
        
        # Step 3: Write results to specified format
        console.print("[blue]💾 Writing results...[/blue]")
        if output_format == "json":
            OutputWriter.write_json(results, filename)
        else:
            OutputWriter.write_csv(results, filename)
        
        # Success message
        console.print(f"[green]🎉 Successfully processed query: '{query}'[/green]")
        
    except ValidationError as e:
        console.print(f"[bold red]❌ Input Validation Error:[/bold red] {e}")
        console.print("[yellow]💡 Tip: Check your query syntax and output filename[/yellow]")
        raise typer.Exit(code=2)  # Different exit code for validation errors
        
    except NetworkError as e:
        console.print(f"[bold red]❌ Network Error:[/bold red] {e}")
        console.print("[yellow]💡 Tip: Check your internet connection and try again[/yellow]")
        raise typer.Exit(code=3)  # Different exit code for network errors
        
    except PubMedAPIError as e:
        console.print(f"[bold red]❌ PubMed API Error:[/bold red] {e}")
        console.print("[yellow]💡 Tip: Try a different search query or check PubMed status[/yellow]")
        raise typer.Exit(code=4)  # Different exit code for API errors
        
    except DataProcessingError as e:
        console.print(f"[bold red]❌ Data Processing Error:[/bold red] {e}")
        console.print("[yellow]💡 Tip: This might be a temporary issue with data format[/yellow]")
        raise typer.Exit(code=5)  # Different exit code for processing errors
        
    except OutputError as e:
        console.print(f"[bold red]❌ Output Error:[/bold red] {e}")
        console.print("[yellow]💡 Tip: Check file permissions and available disk space[/yellow]")
        raise typer.Exit(code=6)  # Different exit code for output errors
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Operation cancelled by user[/yellow]")
        raise typer.Exit(code=130)  # Standard exit code for SIGINT
        
    except Exception as e:
        console.print(f"[bold red]❌ Unexpected Error:[/bold red] {e}")
        console.print("[yellow]💡 This is an unexpected error. Please report this issue.[/yellow]")
        if debug:
            import traceback
            console.print(f"[red]Traceback:[/red] {traceback.format_exc()}")
        raise typer.Exit(code=1)  # General error code

