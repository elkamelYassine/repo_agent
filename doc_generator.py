"""Documentation generation module."""
from pathlib import Path
from rich.console import Console
from repo_analyzer import read_file_safely

console = Console()


class DocGenerator:
    
    def __init__(self, ai_service):
        self.ai = ai_service
    
    def generate_overview(self, repo_name, summary):
        # Get code files
        code_files = summary.code_files()[:10]
        
        # Prepare file samples
        file_list = "\n".join([f"- {f.rel_path}" for f in code_files[:15]])
        
        # Language stats
        by_lang = summary.by_language()
        lang_stats = "\n".join([f"- {lang}: {len(files)} files" 
                                for lang, files in by_lang.items()])
        
        # Get code samples
        code_samples = []
        for f in code_files[:3]:
            content = read_file_safely(f.path)
            if content:
                code_samples.append(f"File: {f.rel_path}\n```\n{content[:800]}\n```")
        
        prompt = f"""Analyze this repository '{repo_name}' and create a project overview.

Languages:
{lang_stats}

Files:
{file_list}

Code samples:
{chr(10).join(code_samples)}

Generate a technical overview (300-400 words) covering:
1. Project purpose
2. Technology stack
3. Key directories
4. How to explore the code

Write in Markdown format."""

        return self.ai.generate(prompt)
    
    def generate_readme(self, repo_name, summary, overview):
        """Generate README.md."""
        code_files = summary.code_files()[:5]
        
        # Get code samples
        code_samples = []
        for f in code_files:
            content = read_file_safely(f.path)
            if content:
                code_samples.append(f"File: {f.rel_path}\n```\n{content[:1000]}\n```")
        
        prompt = f"""Create a professional README.md for '{repo_name}'.

Overview:
{overview}

Code samples:
{chr(10).join(code_samples)}

Generate a README with:
# {repo_name}

## Description
## Features
## Installation
## Usage
## Project Structure
## Technologies
## License

Write in clear Markdown."""

        return self.ai.generate(prompt)
    
    def generate_all(self, repo_name, summary, output_dir):
        """Generate all documentation."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate overview
        console.print("  Generating overview...")
        overview = self.generate_overview(repo_name, summary)
        (output_dir / "PROJECT_OVERVIEW.md").write_text(overview, encoding='utf-8')
        console.print("[green]✓[/green] Overview saved")
        
        # Generate README
        console.print("  Generating README...")
        readme = self.generate_readme(repo_name, summary, overview)
        (output_dir / "README.md").write_text(readme, encoding='utf-8')
        console.print("[green]✓[/green] README saved")
