from typing import Optional, List
import typer
from rich import print
from rich.console import Console
import requests
import xml.etree.ElementTree as ET
import csv
import sys

console = Console()
app = typer.Typer()

ACADEMIC_KEYWORDS = [
    "school", "university", "college", "institute", "department", "faculty",
    "academy", "center", "centre", "hospital", "medical", "clinic", "grad",
    "postdoc", "fellow", "professor", "lecturer", "phd", "student", "library",
    "conservatory", "polytechnic", "laboratory", "lab"
]

def is_academic_affiliation(affil: str) -> bool:
    affil = affil.lower()
    return any(keyword in affil for keyword in ACADEMIC_KEYWORDS)

def extract_email(affil_text: str) -> str:
    if not affil_text:
        return ""
    for word in affil_text.split():
        if "@" in word and "." in word:
            return word.strip(";.,()<>")
    return ""

def search_pubmed(query: str, retmax: int = 20) -> tuple[str, str]:
    try:
        params = {
            "db": "pubmed",
            "term": query,
            "retmode": "xml",
            "usehistory": "y",
            "retmax": retmax
        }
        response = requests.get("https://eutils.ncbi.nlm.nih.gov/eutils/esearch.fcgi", params=params)
        response.raise_for_status()
        root = ET.fromstring(response.text)
        query_key = root.findtext("QueryKey")
        webenv = root.findtext("WebEnv")
        if not query_key or not webenv:
            raise ValueError("Missing QueryKey or WebEnv in response.")
        return query_key, webenv
    except Exception as e:
        console.print(f"[red]Error during PubMed search:[/red] {e}")
        raise

def fetch_pubmed_details(query_key: str, webenv: str, retstart: int = 0, retmax: int = 20) -> List[dict]:
    try:
        params = {
            "db": "pubmed",
            "query_key": query_key,
            "WebEnv": webenv,
            "retstart": retstart,
            "retmax": retmax,
            "retmode": "xml"
        }
        response = requests.get("https://eutils.ncbi.nlm.nih.gov/eutils/efetch.fcgi", params=params)
        response.raise_for_status()
        return parse_pubmed_xml(response.text)
    except Exception as e:
        console.print(f"[red]Error fetching article details:[/red] {e}")
        raise

def parse_pubmed_xml(xml_text: str) -> List[dict]:
    root = ET.fromstring(xml_text)
    results = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID") or "N/A"
        title = article.findtext(".//ArticleTitle") or "N/A"

        pub_date_elem = article.find(".//PubDate")
        year = pub_date_elem.findtext("Year") or ""
        month = pub_date_elem.findtext("Month") or ""
        day = pub_date_elem.findtext("Day") or ""
        pub_date = f"{year}-{month}-{day}".strip("-")

        non_academic_authors = []
        affiliations = []
        corresponding_email = ""

        for author in article.findall(".//Author"):
            fore = author.findtext("ForeName") or ""
            last = author.findtext("LastName") or ""
            full_name = f"{fore} {last}".strip()

            affil_elem = author.find(".//AffiliationInfo/Affiliation")
            affil = affil_elem.text.strip() if affil_elem is not None else ""

            if affil:
                email = extract_email(affil)
                if not corresponding_email and email:
                    corresponding_email = email

            if affil and not is_academic_affiliation(affil):
                non_academic_authors.append(full_name)
                affiliations.append(affil)

        if non_academic_authors:
            results.append({
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academicAuthor(s)": "; ".join(non_academic_authors),
                "CompanyAffiliation(s)": "; ".join(affiliations),
                "Corresponding Author Email": corresponding_email
            })

    return results

def write_to_csv(results: List[dict], filename: str) -> None:
    try:
        if not results:
            console.print("[yellow]No non-academic papers found.[/yellow]")
            return

        fieldnames = [
            "PubmedID", "Title", "Publication Date",
            "Non-academicAuthor(s)", "CompanyAffiliation(s)", "Corresponding Author Email"
        ]
        with open(filename, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        console.print(f"[green]✅ Results saved to '{filename}'[/green]")
    except Exception as e:
        console.print(f"[red]Error writing to CSV:[/red] {e}")
        raise

def run_cli():
    typer.run(main)
def main(
    query: str = typer.Argument(..., help="PubMed search query."),
    file: str = typer.Option(default="output.csv", help="Output CSV file name.", show_default=True),
    debug: bool = typer.Option(default=False, help="Enable debug logging.")
):
    if debug:
        console.log(f"[bold cyan]Running query:[/bold cyan] {query}")
    try:
        query_key, webenv = search_pubmed(query)
        results = fetch_pubmed_details(query_key, webenv, retmax=50)
        write_to_csv(results, file)
    except Exception as e:
        console.print(f"[bold red]❌ Failed:[/bold red] {e}")
        raise typer.Exit(code=1)

