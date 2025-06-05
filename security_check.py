#!/usr/bin/env python3
"""
Security Check Script for LangTest

This script checks for potential security issues before publishing to GitHub.
Run this before committing your code to ensure no sensitive data is exposed.
"""

import os
import re
import json
from pathlib import Path

def check_api_keys():
    """Check for hardcoded API keys in Python files"""
    print("🔍 Checking for hardcoded API keys...")
    
    # More specific OpenAI API key pattern
    api_key_patterns = [
        r'sk-proj-[a-zA-Z0-9_-]{20,}',  # OpenAI project API keys
        r'sk-[a-zA-Z0-9_-]{48,}',       # OpenAI API keys (specific length)
    ]
    
    issues = []
    
    for py_file in Path('.').rglob('*.py'):
        # Skip virtual environments and cache directories
        if any(skip in str(py_file) for skip in ['venv', 'env', '__pycache__', 'site-packages', '.git']):
            continue
            
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for pattern in api_key_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    # Skip placeholder values
                    if 'your-' not in match.lower() and 'example' not in match.lower():
                        issues.append(f"Potential API key in {py_file}: {match[:15]}...")
        except Exception as e:
            print(f"Warning: Could not read {py_file}: {e}")
    
    if issues:
        print("❌ Found potential API keys:")
        for issue in issues:
            print(f"   {issue}")
        return False
    else:
        print("✅ No hardcoded API keys found")
        return True

def check_sensitive_files():
    """Check for sensitive files that should be gitignored"""
    print("\n🔍 Checking for sensitive files...")
    
    sensitive_patterns = [
        'reports/*.json',
        'exploration_reports/*.json',
        '.env',
        '*.log',
    ]
    
    # Check for __pycache__ in project root (not in venv)
    pycache_dirs = []
    for item in Path('.').iterdir():
        if item.name == '__pycache__' and item.is_dir():
            pycache_dirs.append(item)
    
    issues = []
    
    for pattern in sensitive_patterns:
        files = list(Path('.').glob(pattern))
        if files:
            issues.append(f"Found {len(files)} files matching '{pattern}'")
    
    if pycache_dirs:
        issues.append(f"Found {len(pycache_dirs)} __pycache__ directories in project root")
    
    if issues:
        print("⚠️  Found sensitive files (should be in .gitignore):")
        for issue in issues:
            print(f"   {issue}")
        
        # Check if .gitignore exists
        if Path('.gitignore').exists():
            print("✅ .gitignore file exists")
        else:
            print("❌ .gitignore file missing!")
            return False
    else:
        print("✅ No sensitive files found in repository")
    
    return True

def check_env_setup():
    """Check environment setup"""
    print("\n🔍 Checking environment setup...")
    
    issues = []
    
    # Check for .env.example
    if not Path('.env.example').exists():
        issues.append(".env.example file missing")
    else:
        print("✅ .env.example file exists")
    
    # Check config.py for proper environment variable usage
    if Path('config.py').exists():
        with open('config.py', 'r') as f:
            config_content = f.read()
            
        if 'sk-' in config_content and 'os.getenv' not in config_content:
            issues.append("config.py may contain hardcoded API keys")
        elif 'os.getenv' in config_content:
            print("✅ config.py uses environment variables")
    
    if issues:
        print("❌ Environment setup issues:")
        for issue in issues:
            print(f"   {issue}")
        return False
    
    return True

def check_gitignore():
    """Check .gitignore completeness"""
    print("\n🔍 Checking .gitignore completeness...")
    
    if not Path('.gitignore').exists():
        print("❌ .gitignore file missing!")
        return False
    
    with open('.gitignore', 'r') as f:
        gitignore_content = f.read()
    
    required_patterns = [
        'reports/',
        'exploration_reports/',
        '.env',
        '__pycache__/',
        '*.log',
        'generated_tests/',
    ]
    
    missing = []
    for pattern in required_patterns:
        if pattern not in gitignore_content:
            missing.append(pattern)
    
    if missing:
        print("⚠️  Missing patterns in .gitignore:")
        for pattern in missing:
            print(f"   {pattern}")
    else:
        print("✅ .gitignore appears complete")
    
    return len(missing) == 0

def main():
    """Run all security checks"""
    print("🛡️  LangTest Security Check")
    print("=" * 50)
    
    checks = [
        check_api_keys,
        check_sensitive_files,
        check_env_setup,
        check_gitignore,
    ]
    
    all_passed = True
    
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All security checks passed! Safe to publish to GitHub.")
    else:
        print("❌ Some security issues found. Please fix before publishing.")
        print("\n📋 Recommended actions:")
        print("1. Remove any hardcoded API keys")
        print("2. Add sensitive files to .gitignore")
        print("3. Create .env.example with placeholder values")
        print("4. Ensure config.py uses environment variables")
    
    return all_passed

if __name__ == "__main__":
    main()