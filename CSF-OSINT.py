import os
import argparse
import requests 
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track

# Configuration & Branding
BASE_URL = "https://wikiservices.lovable.app/sim-database"
UA_STRING = "Mozilla/5.0 (X11; Kali Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

class CSF_OSINT:
    """
    Cyber Squad Forge - Open Source Intelligence Tool
    Developed for Educational & Security Research Purposes.
    """
    def __init__(self):
        self.console = Console()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": UA_STRING,
            "Origin": "https://wikiservices.lovable.app/sim-database",
            "Referer": BASE_URL,
            "Content-Type": "application/x-www-form-urlencoded"
        })

    def banner(self):
        self.console.print(Panel.fit(
            "[bold cyan]CSF-OSINT v1.0[/bold cyan]\n[bold white]Developed by Engr. Muhammad Muzammil Khokhar[/bold white]\n[green]Academy: Cyber Squad Forge[/green]",
            border_style="green"
        ))

    def run_intel_scan(self, target):
        """Perform the automated intelligence gathering."""
        payload = {"searchinfo": target}
        try:
            response = self.session.post(BASE_URL, data=payload, timeout=15)
            response.raise_for_status()
            
            parser = BeautifulSoup(response.text, "html.parser")
            nodes = parser.find_all("div", class_="resultcontainer")
            return nodes
        except Exception as e:
            self.console.print(f"[bold red][!] Error encountered: {str(e)}[/bold red]")
            return []

    def format_output(self, target, data):
        """Generate a structured report on the CLI."""
        if not data:
            self.console.print(f"[-] [bold red]Zero intelligence found for: {target}[/bold red]")
            return

        self.console.print(f"\n[bold green][+][/bold green] [white]Captured Data for:[/white] [bold yellow]{target}[/bold yellow]")
        
        for i, node in enumerate(data, start=1):
            intel_table = Table(
                title=f"CSF-Report Entry #{i}", 
                show_lines=True, 
                header_style="bold green",
                border_style="white"
            )
            intel_table.add_column("Field", style="cyan")
            intel_table.add_column("Information", style="bold white")

            rows = node.find_all("div", class_="row")
            for row in rows:
                key = row.find("span", class_="detailshead")
                val = row.find("span", class_="details")
                
                if key and val:
                    intel_table.add_row(key.get_text(strip=True).replace(":", ""), val.get_text(strip=True))

            self.console.print(intel_table)

    def log_to_file(self, target, data, path):
        """Export the intelligence report to a text file."""
        with open(path, "a", encoding="utf-8") as f:
            if not data:
                f.write(f"Query: {target} | Status: No Result\n")
            else:
                f.write(f"\n[CSF-OSINT Intel Report - {target}]\n")
                for i, node in enumerate(data, start=1):
                    f.write(f"--- Entry {i} ---\n")
                    for row in node.find_all("div", class_="row"):
                        k = row.find("span", class_="detailshead").get_text(strip=True)
                        v = row.find("span", class_="details").get_text(strip=True)
                        f.write(f"{k} {v}\n")
                f.write("="*40 + "\n")

def main():
    csf = CSF_OSINT()
    csf.banner()
    
    parser = argparse.ArgumentParser(description="CSF-OSINT Tool for Cybersecurity Experts")
    parser.add_argument("-n", "--number", help="Target number to investigate")
    parser.add_argument("-l", "--list", help="Bulk scan from a file")
    args = parser.parse_args()

    if args.number:
        results = csf.run_intel_scan(args.number)
        csf.format_output(args.number, results)

    elif args.list:
        if not os.path.exists(args.list):
            csf.console.print(f"[bold red][!] File not found: {args.list}[/bold red]")
            return

        report_path = "csf_intel_logs.txt"
        with open(args.list, "r") as f:
            targets = [line.strip() for line in f if line.strip()]

        for target in track(targets, description="[bold cyan]Processing Batch...[/bold cyan]"):
            results = csf.run_intel_scan(target)
            csf.log_to_file(target, results, report_path)
        
        csf.console.print(f"\n[bold green][V][/bold green] Logs successfully saved to [bold white]{report_path}[/bold white]")

    else:
        parser.print_help()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Scanning halted by user.")
