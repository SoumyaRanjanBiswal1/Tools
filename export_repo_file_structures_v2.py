import os
from pathlib import Path
from fnmatch import fnmatch

# --------- CONFIG: tweak as you like ----------
ROOT = Path(".")
OUT_FILE = Path("project_structure.txt")

# Directories to skip entirely
IGNORE_DIRS = {
    "__pycache__", "node_modules", "venv", ".venv", ".git", ".github", ".next",
    ".mypy_cache", ".pytest_cache", ".ruff_cache", ".idea", ".vscode",
    "dist", "build", "cache", ".turbo", ".pnpm-store"
}

# File name globs to skip
IGNORE_FILE_GLOBS = {
    "*.env", ".env", ".env.*", "*.db", "*.sqlite*", "*.pyc", "*.pyo",
    "*.log", "*.lock", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "*.map", "*.DS_Store", "trace"
}

# Skip ALL hidden files (starting with ".") except a small allowlist:
ALLOW_HIDDEN_FILES = {"README.md", ".gitignore"}
# ----------------------------------------------

def is_hidden(p: Path) -> bool:
    return p.name.startswith(".")

def should_skip_dir(name: str) -> bool:
    return name in IGNORE_DIRS or name.startswith(".")

def should_skip_file(p: Path) -> bool:
    name = p.name
    if is_hidden(p) and name not in ALLOW_HIDDEN_FILES:
        return True
    for pat in IGNORE_FILE_GLOBS:
        if fnmatch(name, pat):
            return True
    return False

def list_dir_sorted(path: Path):
    dirs, files = [], []
    for entry in os.scandir(path):
        if entry.is_dir():
            dirs.append(entry.name)
        else:
            files.append(entry.name)
    return sorted(dirs, key=str.lower), sorted(files, key=str.lower)

def build_tree(path: Path, indent: str, lines: list[str]):
    dir_names, file_names = list_dir_sorted(path)

    # Directories first
    for d in dir_names:
        if should_skip_dir(d):
            continue
        child = path / d
        lines.append(f"{indent}📁 {d}/")
        build_tree(child, indent + "    ", lines)

    # Then files
    for f in file_names:
        fp = path / f
        if should_skip_file(fp):
            continue
        lines.append(f"{indent}📄 {f}")

def main():
    lines: list[str] = []
    # root line (do not show just "."; show folder name)
    root_name = ROOT.resolve().name
    lines.append(f"📁 {root_name}/")
    build_tree(ROOT, "    ", lines)

    OUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Saved clean project tree to {OUT_FILE}")

if __name__ == "__main__":
    main()
