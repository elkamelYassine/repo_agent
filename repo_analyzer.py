"""Repository analysis module."""
import os
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class FileInfo:
    """Information about a file."""
    path: Path
    rel_path: str
    extension: str
    language: str


@dataclass
class RepoSummary:
    """Repository analysis summary."""
    root: Path
    files: list = field(default_factory=list)
    
    def by_language(self):
        """Group files by language."""
        result = {}
        for f in self.files:
            result.setdefault(f.language, []).append(f)
        return result
    
    def code_files(self):
        """Get code files only."""
        code_exts = {'.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.go', '.rs'}
        return [f for f in self.files if f.extension in code_exts]


def detect_language(path):
    """Detect language from file extension."""
    ext = path.suffix.lower()
    languages = {
        '.py': 'Python',
        '.js': 'JavaScript', '.jsx': 'JavaScript',
        '.ts': 'TypeScript', '.tsx': 'TypeScript',
        '.java': 'Java',
        '.cpp': 'C++', '.c': 'C',
        '.go': 'Go',
        '.rs': 'Rust',
        '.rb': 'Ruby',
        '.php': 'PHP',
    }
    return languages.get(ext, 'Other')


def analyze_local_repo(root):
    """Analyze a local repository."""
    root = Path(root).resolve()
    summary = RepoSummary(root=root)
    
    skip_dirs = {'.git', 'venv', '.venv', '__pycache__', 'node_modules', 'dist', 'build'}
    
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip certain directories
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in skip_dirs]
        
        for fname in filenames:
            if fname.startswith('.'):
                continue
            
            path = Path(dirpath) / fname
            rel_path = str(path.relative_to(root).as_posix())
            ext = path.suffix.lower()
            lang = detect_language(path)
            
            summary.files.append(FileInfo(
                path=path,
                rel_path=rel_path,
                extension=ext,
                language=lang
            ))
    
    return summary


def read_file_safely(file_path):
    """Read file with encoding fallback."""
    for encoding in ['utf-8', 'latin-1']:
        try:
            return file_path.read_text(encoding=encoding)
        except:
            continue
    return ""
