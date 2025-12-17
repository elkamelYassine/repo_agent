"""Test generation module."""
from pathlib import Path
from rich.console import Console
from repo_analyzer import read_file_safely

console = Console()


class TestGenerator:
    """Generate unit tests for repositories."""
    
    def __init__(self, ai_service):
        self.ai = ai_service
    
    def generate_tests(self, summary, output_dir):
        """Generate comprehensive tests."""
        # Get code files (not test files)
        code_files = [f for f in summary.code_files() 
                      if 'test' not in f.rel_path.lower()][:10]
        
        if not code_files:
            console.print("[yellow]No code files found[/yellow]")
            return
        
        # Prepare code samples
        code_samples = []
        for f in code_files:
            content = read_file_safely(f.path)
            if content:
                code_samples.append(f"File: {f.rel_path}\n```\n{content[:1500]}\n```")
        
        # Detect language and test framework
        primary_ext = code_files[0].extension
        test_info = self._get_test_info(primary_ext)
        
        prompt = f"""Generate comprehensive unit tests for this code.

Code to test:
{chr(10).join(code_samples)}

Requirements:
1. Language: {test_info['language']}
2. Framework: {test_info['framework']}
3. Test normal cases, edge cases, and errors
4. Include proper imports and setup
5. Output ONLY valid, runnable code (no explanations)
6. Create complete test suites

Generate production-ready test code."""

        console.print(f"  Generating {test_info['framework']} tests...")
        test_content = self.ai.generate(prompt)
        
        # Save test file
        tests_dir = output_dir / "tests"
        tests_dir.mkdir(parents=True, exist_ok=True)
        
        test_file = tests_dir / test_info['filename']
        test_file.write_text(test_content, encoding='utf-8')
        
        console.print(f"[green]✓[/green] Tests saved to {test_file.name}")
    
    def _get_test_info(self, extension):
        """Get test framework info based on file extension."""
        mapping = {
            '.py': {
                'language': 'Python',
                'framework': 'pytest',
                'filename': 'test_generated.py'
            },
            '.js': {
                'language': 'JavaScript',
                'framework': 'Jest',
                'filename': 'generated.test.js'
            },
            '.ts': {
                'language': 'TypeScript',
                'framework': 'Jest',
                'filename': 'generated.test.ts'
            },
            '.java': {
                'language': 'Java',
                'framework': 'JUnit',
                'filename': 'GeneratedTest.java'
            },
            '.go': {
                'language': 'Go',
                'framework': 'testing',
                'filename': 'generated_test.go'
            },
        }
        
        return mapping.get(extension, {
            'language': 'Unknown',
            'framework': 'Standard',
            'filename': 'test_generated.txt'
        })
