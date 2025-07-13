"""
File output utilities for the pharma research extractor.

Handles writing results to various output formats with comprehensive
error handling and validation.
"""

from typing import List, Dict, Any
import csv
import json
import os
from pathlib import Path
from rich.console import Console

from .config import CSV_FIELDNAMES
from .exceptions import OutputError
from .validation import InputValidator

console = Console()


class OutputWriter:
    """
    Handles writing research results to output files.
    
    Supports multiple output formats and provides consistent error handling
    and user feedback.
    """
    
    @staticmethod
    def write_csv(results: List[Dict[str, Any]], filename: str) -> None:
        """
        Write extracted research data to a CSV file.
        
        Creates a structured CSV file with standardized columns for further
        analysis of pharmaceutical industry research publications.
        
        Args:
            results: List of article dictionaries from PubMed parsing
            filename: Output CSV file path
            
        Raises:
            OutputError: If file cannot be written or data is invalid
        """
        try:
            # Validate inputs
            filename = InputValidator.validate_filename(filename)
            
            if not isinstance(results, list):
                raise OutputError("Results must be a list")
            
            if not results:
                console.print("[yellow]⚠️ No non-academic papers found to save.[/yellow]")
                return
            
            # Validate each result
            validated_results = []
            for i, result in enumerate(results):
                try:
                    validated_result = InputValidator.validate_article_data(result)
                    validated_results.append(validated_result)
                except Exception as e:
                    console.log(f"[yellow]Warning: Skipping invalid article at index {i}: {e}[/yellow]")
                    continue
            
            if not validated_results:
                console.print("[yellow]⚠️ No valid articles to save after validation.[/yellow]")
                return
            
            # Ensure output directory exists
            output_path = Path(filename)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Check write permissions
            if output_path.exists() and not os.access(output_path, os.W_OK):
                raise OutputError(f"No write permission for file: {filename}")
            
            # Check available disk space (basic check)
            try:
                free_space = os.statvfs(output_path.parent).f_bavail * os.statvfs(output_path.parent).f_frsize
                if free_space < 1024 * 1024:  # Less than 1MB
                    console.print("[yellow]⚠️ Warning: Low disk space available[/yellow]")
            except (AttributeError, OSError):
                # statvfs not available on Windows, skip check
                pass
            
            # Write results with UTF-8 encoding for international character support
            with open(filename, "w", newline='', encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDNAMES)
                writer.writeheader()
                writer.writerows(validated_results)

            console.print(f"[green]✅ Results saved to '{filename}'[/green]")
            console.print(f"[blue]📊 Saved {len(validated_results)} papers with industry affiliations[/blue]")
            
            # Show file size
            try:
                file_size = os.path.getsize(filename)
                if file_size < 1024:
                    size_str = f"{file_size} bytes"
                elif file_size < 1024 * 1024:
                    size_str = f"{file_size / 1024:.1f} KB"
                else:
                    size_str = f"{file_size / (1024 * 1024):.1f} MB"
                console.print(f"[dim]File size: {size_str}[/dim]")
            except OSError:
                pass
            
        except PermissionError:
            raise OutputError(f"Permission denied writing to file: {filename}")
        except FileNotFoundError:
            raise OutputError(f"Directory not found for file: {filename}")
        except OSError as e:
            raise OutputError(f"File system error: {e}")
        except UnicodeEncodeError as e:
            raise OutputError(f"Character encoding error: {e}")
        except Exception as e:
            raise OutputError(f"Failed to write CSV file: {e}")
    
    @staticmethod
    def write_json(results: List[Dict[str, Any]], filename: str) -> None:
        """
        Write extracted research data to a JSON file.
        
        Args:
            results: List of article dictionaries from PubMed parsing
            filename: Output JSON file path
        """
        import json
        
        try:
            with open(filename, "w", encoding="utf-8") as jsonfile:
                json.dump(results, jsonfile, indent=2, ensure_ascii=False)
            
            console.print(f"[green]✅ Results saved to '{filename}'[/green]")
            console.print(f"[blue]📊 Found {len(results)} papers with industry affiliations[/blue]")
            
        except Exception as e:
            console.print(f"[red]Error writing to JSON:[/red] {e}")
            raise
