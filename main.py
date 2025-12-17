"""Simple main script for repo_agent."""
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from config import Config
from github_service import GitHubService
from ai_service import AIService
from repo_analyzer import analyze_local_repo
from doc_generator import DocGenerator
from test_generator import TestGenerator

console = Console()


def main():
    """Main function to generate documentation and tests."""
    console.print(Panel.fit(
        "[bold cyan]Repository Agent[/bold cyan]\n"
        "AI-powered documentation and test generator",
        border_style="cyan"
    ))
    
    # 1. Validate configuration
    try:
        Config.validate()
        console.print("[green]✓[/green] Configuration validated\n")
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        console.print("[dim]Set GEMINI_API_KEY in your .env file[/dim]\n")
        return
    
    # 2. Get repository URL
    repo_url = input("\nEnter GitHub repository URL: ").strip()
    if not repo_url:
        console.print("[red]No URL provided[/red]")
        return
    
    try:
        # 3. Initialize services
        console.print("\n[bold blue]Initializing services...[/bold blue]")
        github_service = GitHubService()
        ai_service = AIService(api_key=Config.GEMINI_API_KEY)
        
        # Parse URL
        owner, repo_name = github_service.parse_github_url(repo_url)
        console.print(f"[green]✓[/green] Repository: {owner}/{repo_name}")
        
        # 4. Clone and analyze repository
        console.print("\n[bold blue]Cloning repository...[/bold blue]")
        workdir = Path("tmp_repo")
        repo_path = github_service.clone_repo(repo_url, workdir)
        
        console.print("\n[bold blue]Analyzing repository...[/bold blue]")
        summary = analyze_local_repo(repo_path)
        console.print(f"[green]✓[/green] Found {len(summary.files)} files")
        console.print(f"[green]✓[/green] Code files: {len(summary.code_files())}")
        
        # Display language distribution
        by_lang = summary.by_language()
        console.print("\n[dim]Languages:[/dim]")
        for lang, files in sorted(by_lang.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
            console.print(f"  [dim]{lang}: {len(files)} files[/dim]")
        
        # 5. Set output directory
        output_dir = Path(f"output_{repo_name}")
        console.print(f"\n[dim]Output: {output_dir.absolute()}[/dim]\n")
        
        # 6. Generate documentation
        console.print("[bold blue]Generating documentation...[/bold blue]")
        doc_generator = DocGenerator(ai_service)
        doc_generator.generate_all(repo_name, summary, output_dir)
        
        # 7. Generate tests
        console.print("\n[bold blue]Generating tests...[/bold blue]")
        test_generator = TestGenerator(ai_service)
        test_generator.generate_tests(summary, output_dir)
        
        # 8. Success message
        console.print(Panel.fit(
            f"[bold green]✓ Complete![/bold green]\n\n"
            f"Documentation and tests saved to:\n"
            f"[cyan]{output_dir.absolute()}[/cyan]",
            border_style="green"
        ))
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}\n")


if __name__ == "__main__":
    main()
