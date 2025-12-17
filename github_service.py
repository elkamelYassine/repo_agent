"""GitHub service for repository operations."""
import os
import shutil
import time
from pathlib import Path
from git import Repo
from rich.console import Console

console = Console()


class GitHubService:
    """Service for cloning and accessing GitHub repositories."""
    
    def __init__(self, token=None):
        self.token = token
    
    def parse_github_url(self, url):
        """Extract owner and repo name from GitHub URL."""
        url = url.rstrip('/').replace('.git', '')
        parts = url.split('/')
        
        if 'github.com' not in url:
            raise ValueError("Invalid GitHub URL")
        
        repo_name = parts[-1]
        owner = parts[-2]
        return owner, repo_name
    
    def clone_repo(self, repo_url, target_dir):
        """Clone repository to local directory."""
        target_dir = Path(target_dir)
        
        # Clean existing directory with retry logic for Windows
        if target_dir.exists():
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # On Windows, files might be locked, so we need to handle permissions
                    if os.name == 'nt':  # Windows
                        # Try to remove read-only files
                        def handle_remove_readonly(func, path, exc):
                            os.chmod(path, 0o777)
                            func(path)
                        
                        shutil.rmtree(target_dir, onerror=handle_remove_readonly)
                    else:
                        shutil.rmtree(target_dir)
                    break
                except (PermissionError, OSError) as e:
                    if attempt < max_retries - 1:
                        console.print(f"[yellow]⚠[/yellow] Retrying cleanup... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(1)
                    else:
                        # If cleanup fails, try to clone to a different directory
                        import uuid
                        target_dir = target_dir.parent / f"{target_dir.name}_{uuid.uuid4().hex[:8]}"
                        console.print(f"[yellow]⚠[/yellow] Using alternative directory: {target_dir}")
                        break
        
        # Ensure parent directory exists
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        
        # Clone
        try:
            Repo.clone_from(repo_url, target_dir)
            console.print(f"[green]✓[/green] Cloned to {target_dir}")
        except Exception as e:
            # Clean up on failure
            if target_dir.exists():
                try:
                    shutil.rmtree(target_dir, ignore_errors=True)
                except:
                    pass
            raise Exception(f"Failed to clone repository: {str(e)}")
        
        return target_dir
