#!/usr/bin/env python3
"""Archive additional unnecessary files."""

import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent
ARCHIVE_DIR = BASE_DIR / "archive" / "docker_migration" / "additional_cleanup"
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

# Files to archive
files_to_archive = [
    # Documentation to archive (keep only README.md and DOCKER_DEPLOYMENT.md)
    "CLEANUP_SUMMARY.md",
    "DOCKER_REVIEW_SUMMARY.md",
    "DOCKER_SETUP_CHECKLIST.md",
    "PROJECT_STRUCTURE.md",
    "DOCKER_QUICK_START.md",  # Will merge into DOCKER_DEPLOYMENT.md
    
    # Optional Docker files
    "Dockerfile.combined",
    "docker-compose.combined.yml",
    
    # Scripts
    "archive_files.py",
    
    # Frontend README (not essential)
    "frontend/README.md",
]

print("🗂️  Archiving additional unnecessary files...\n")

moved_count = 0
for file_path in files_to_archive:
    source = BASE_DIR / file_path
    if source.exists():
        # Preserve directory structure
        if "/" in file_path or "\\" in file_path:
            rel_path = Path(file_path)
            target = ARCHIVE_DIR / rel_path
            target.parent.mkdir(parents=True, exist_ok=True)
        else:
            target = ARCHIVE_DIR / source.name
        
        shutil.move(str(source), str(target))
        print(f"  ✅ Moved: {file_path}")
        moved_count += 1
    else:
        print(f"  ⚠️  Not found: {file_path}")

print(f"\n✅ Archived {moved_count} additional files")

