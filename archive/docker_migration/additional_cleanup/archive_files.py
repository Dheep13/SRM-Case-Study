#!/usr/bin/env python3
"""Script to archive unnecessary files for Docker deployment."""

import os
import shutil
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent
ARCHIVE_DIR = BASE_DIR / "archive" / "docker_migration"

# Create archive directory structure
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
(ARCHIVE_DIR / "cloud_foundry").mkdir(exist_ok=True)
(ARCHIVE_DIR / "old_docs").mkdir(exist_ok=True)
(ARCHIVE_DIR / "old_scripts").mkdir(exist_ok=True)
(ARCHIVE_DIR / "test_files").mkdir(exist_ok=True)
(ARCHIVE_DIR / "frontend_cf").mkdir(exist_ok=True)

# Files to archive
files_to_archive = {
    "cloud_foundry": [
        "manifest.yml",
        "Procfile",
        "runtime.txt",
        "deploy_to_cf.bat",
        "deploy-backend.bat",
        "deploy-both.bat",
        "set_cf_env.bat",
        "set_cf_env.bat.example",
        "check-logs.bat",
        "check-status.bat",
        "monitor-apps.bat",
        "README_CF_DEPLOYMENT.md",
        "CF_TROUBLESHOOTING.md",
        "DEPLOYMENT_GUIDE.md",
        "DEPLOY_NOW_FULL_STACK.md",
        "FULL_STACK_DEPLOYMENT.md",
    ],
    "old_docs": [
        "ADMIN_ACCESS_CONTROL_GUIDE.md",
        "ADMIN_ACCESS_GUIDE.md",
        "ADMIN_FEATURES_COMPLETE.md",
        "ADMIN_GUIDE.md",
        "ADMIN_HEALTH_FIX.md",
        "AGENT_ACCESS_CONTROL_GUIDE.md",
        "AGENT_ACCESS_CONTROL_IMPLEMENTATION.md",
        "COMPLETION_SUMMARY.md",
        "DATE_FILTER_SUMMARY.md",
        "DEPLOYMENT_QUICK_FIX.md",
        "DISCOVERY_FIX_SUMMARY.md",
        "FRONTEND_SUMMARY.md",
        "IMPLEMENTATION_SUMMARY.md",
        "PERFORMANCE_OPTIMIZATIONS.md",
        "REFRESH_BUTTON_FIX.md",
        "SKILL_FORECAST_TAVILY.md",
        "TECH_NEWS_TAVILY_INTEGRATION.md",
        "TRENDING_SKILLS_COMPLETE.md",
        "ENVIRONMENT_SETUP.md",
        "QUICK_START.md",
        "RUN_REACT.md",
        "TROUBLESHOOTING.md",
    ],
    "old_scripts": [
        "set_env_vars.bat",
        "verify_env.bat",
        "run_app.bat",
        "start_dev.bat",
    ],
    "test_files": [
        "test_agentic_chatbot.py",
        "test_api_key.py",
        "test_chatbot.py",
        "diagnose_openai.py",
        "neo4j_test.py",
        "neo4j_notebook.ipynb",
    ],
    "frontend_cf": [
        "frontend/manifest.yml",
        "frontend/manifest-nodejs.yml",
        "frontend/Staticfile",
        "frontend/cf-deploy.bat",
        "frontend/cf-deploy-fixed.bat",
        "frontend/deploy-with-env.bat",
        "frontend/deploy.sh",
        "frontend/force-cleanup.bat",
        "frontend/pre-deploy-check.bat",
        "frontend/pre-deploy-cleanup.bat",
        "frontend/quick-deploy.bat",
        "frontend/CF_DEPLOYMENT_CHECKLIST.md",
        "frontend/CLOUD_FOUNDRY_SETUP.md",
        "frontend/DEPLOY_NOW.md",
        "frontend/DEPLOYMENT_FIX_SUMMARY.md",
        "frontend/DEPLOYMENT.md",
        "frontend/README_CF.md",
        "frontend/server.js",  # Not needed with Docker nginx
    ],
}

def archive_files():
    """Move files to archive directories."""
    moved_count = 0
    not_found = []
    
    print("🗂️  Archiving unnecessary files for Docker deployment...\n")
    
    for category, files in files_to_archive.items():
        print(f"📁 Category: {category}")
        target_dir = ARCHIVE_DIR / category
        
        for file_path in files:
            source = BASE_DIR / file_path
            
            if source.exists():
                # Preserve directory structure for frontend files
                if file_path.startswith("frontend/"):
                    rel_path = Path(file_path).relative_to("frontend")
                    target = target_dir / rel_path
                    target.parent.mkdir(parents=True, exist_ok=True)
                else:
                    target = target_dir / source.name
                
                shutil.move(str(source), str(target))
                print(f"  ✅ Moved: {file_path}")
                moved_count += 1
            else:
                not_found.append(file_path)
                print(f"  ⚠️  Not found: {file_path}")
        
        print()
    
    print(f"\n📊 Summary:")
    print(f"  ✅ Moved {moved_count} files")
    if not_found:
        print(f"  ⚠️  {len(not_found)} files not found (may have been moved already)")
    
    # Create a README in archive
    readme_content = """# Archived Files - Docker Migration

This directory contains files that are no longer needed after migrating to Docker deployment.

## Structure

- `cloud_foundry/` - Cloud Foundry deployment files (manifest.yml, Procfile, etc.)
- `old_docs/` - Old documentation and summary files
- `old_scripts/` - Old deployment and setup scripts
- `test_files/` - Test and diagnostic scripts
- `frontend_cf/` - Frontend Cloud Foundry deployment files

## Note

These files are kept for reference but are not needed for Docker deployment.
All Docker-related files are in the root directory.
"""
    
    (ARCHIVE_DIR / "README.md").write_text(readme_content)
    print(f"\n📝 Created README.md in archive directory")
    print(f"\n✅ Archiving complete!")

if __name__ == "__main__":
    archive_files()

