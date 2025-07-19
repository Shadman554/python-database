#!/usr/bin/env python3
"""
Fix corrupted import statements in all API files
"""

import os
import re

def fix_corrupted_imports(file_path):
    """Fix corrupted import statements in a single API file"""
    print(f"Fixing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match the corrupted import line
    corrupted_pattern = r'from fastapi import APIRouter, Depe\\nfrom fastapi\.security import HTTPAuthorizationCredentials[a-z]*nds, HTTPException(?:, Query)?'
    
    # Check if this file has the corrupted import
    if re.search(corrupted_pattern, content):
        print(f"  ⚠️  Found corrupted import in {file_path}")
        
        # Replace with correct imports
        fixed_imports = '''from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials'''
        
        content = re.sub(corrupted_pattern, fixed_imports, content)
        
        # Write the fixed content back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ Fixed corrupted import in {file_path}")
    else:
        print(f"  ✅ {file_path} imports are correct")

def main():
    """Fix corrupted imports in all API files"""
    api_dir = 'api'
    
    if not os.path.exists(api_dir):
        print("API directory not found!")
        return
    
    # Get all Python files in the api directory
    api_files = [f for f in os.listdir(api_dir) if f.endswith('.py')]
    
    print(f"Fixing corrupted imports in {len(api_files)} API files...")
    
    for api_file in api_files:
        file_path = os.path.join(api_dir, api_file)
        try:
            fix_corrupted_imports(file_path)
        except Exception as e:
            print(f"  ❌ Error fixing {file_path}: {e}")
    
    print("\n✅ All API files have been processed!")

if __name__ == "__main__":
    main()
