import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import track
from pathlib import Path
import pandas as pd 
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import shutil
from typing import Dict, List, Optional, Any

from utils.utils import get_current_time_and_date

# Initialize typer app and rich console
app = typer.Typer(help="Network Configlet Generator")
console = Console()

# Get current date-time for file naming
cdt: str = get_current_time_and_date()

def validate_csv(csv_path: Path) -> Path:
    """
    Validate CSV file exists and has correct extension.
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        Path: Validated CSV file path
        
    Raises:
        typer.BadParameter: If file doesn't exist or has wrong extension
    """
    if not csv_path.exists():
        raise typer.BadParameter(f"CSV file {csv_path} does not exist")
    if csv_path.suffix.lower() != '.csv':
        raise typer.BadParameter("First argument must be a CSV file")
    return csv_path

def validate_template(template_path: Path) -> Path:
    """
    Validate template file exists and has correct extension.
    
    Args:
        template_path: Path to the template file
        
    Returns:
        Path: Validated template file path
        
    Raises:
        typer.BadParameter: If file doesn't exist or has wrong extension
    """
    if not template_path.exists():
        raise typer.BadParameter(f"Template file {template_path} does not exist")
    if template_path.suffix.lower() != '.j2':
        raise typer.BadParameter("Second argument must be a Jinja2 template file (.j2)")
    return template_path

@app.command()
def generate(
    csv_file: Path = typer.Argument(..., callback=validate_csv, help="CSV file with variables"),
    template_file: Path = typer.Argument(..., callback=validate_template, help="Jinja2 template file"),
    output_dir: Optional[str] = typer.Option(None, "--output", "-o", help="Custom output directory name")
) -> None:
    """
    Generate network configlets from CSV variables and Jinja2 template.
    
    Args:
        csv_file: Path to the CSV file containing variables
        template_file: Path to the Jinja2 template file
        output_dir: Optional custom output directory name
        
    Returns:
        None
    """
    
    # Display header
    console.print(Panel.fit(
        "[bold cyan]Network Configlet Generator[/bold cyan]\n\n"
        "This script generates configlets in separate files based on the first column of CSV variables.\n"
        "User input defines the output location; if the directory doesn't exist, it will be created.",
        title="Welcome",
        border_style="cyan"
    ))

    # Get project directory name if not provided
    if not output_dir:
        output_dir = Prompt.ask("\nEnter the name of the project directory where configlets will be placed")

    # Setup output directory
    base_path: Path = Path.cwd() / 'output' / output_dir
    if base_path.exists():
        overwrite: str = Prompt.ask(
            "\nDirectory already exists. Overwrite?",
            choices=["y", "n"],
            default="n"
        )
        if overwrite.lower() == "y":
            console.print("\n[green]Overwriting existing directory...[/green]")
            shutil.rmtree(base_path)
        else:
            console.print("\n[red]Directory remains. Please rerun with a different name.[/red]")
            raise typer.Exit(1)
    
    base_path.mkdir(parents=True, exist_ok=True)
    console.print(f"\nOutput will be placed into: [cyan]{base_path}[/cyan]\n")

    # Read CSV data
    try:
        df: pd.DataFrame = pd.read_csv(csv_file, na_filter=False, dtype=str)
        data_list: List[Dict[str, Any]] = df.to_dict('records')
    except Exception as e:
        console.print(f"[red]Error reading CSV file: {e}[/red]")
        raise typer.Exit(1)

    # Setup Jinja environment
    try:
        env: Environment = Environment(loader=FileSystemLoader(template_file.parent))
        template = env.get_template(template_file.name)
    except Exception as e:
        console.print(f"[red]Error loading template: {e}[/red]")
        raise typer.Exit(1)

    # Generate configlets with progress bar
    with console.status("[bold green]Generating configlets...") as status:
        for item in track(data_list, description="Processing"):
            try:
                config: str = template.render(item)
                fname: str = list(item.values())[0]
                output_file: Path = base_path / f"{fname}.txt"
                output_file.write_text(config)
            except Exception as e:
                console.print(f"[red]Error processing {fname}: {e}[/red]")

    # Display completion message
    duration: str = datetime.now().strftime("%H:%M:%S")
    console.print(f"\n[green]✓[/green] Configlet generation completed at {duration}")
    console.print(f"[green]✓[/green] Output files are in: [cyan]{base_path}[/cyan]")

    # Generate single file
    single_file: Path = base_path / f'{cdt}-output-singlefile.txt'
    with single_file.open("w") as f:
        for item in data_list:
            config = template.render(item)
            f.write(config)

if __name__ == "__main__":
    app()
