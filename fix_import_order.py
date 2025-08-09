#!/usr/bin/env python3
"""
Fix import order issues in API files
"""

import os
import re

def fix_import_order(file_path):
    """Fix import order in a single API file"""
    print(f"Checking {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for misplaced imports after function definitions
    # Pattern: function definition followed by import statements
    pattern = r'(def get_admin_user\([^}]+?\):\s*return get_current_admin_user\([^}]+?\))\s*((?:from [^\n]+\n|import [^\n]+\n)+)'
    
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if match:
        print(f"  ⚠️  Found misplaced imports in {file_path}")
        
        function_def = match.group(1)
        misplaced_imports = match.group(2).strip()
        
        # Remove the misplaced imports from after the function
        content = content.replace(match.group(0), function_def)
        
        # Find where to insert the imports (after the auth import line)
        auth_import_pattern = r'(from auth import [^\n]+\n)'
        auth_match = re.search(auth_import_pattern, content)
        
        if auth_match:
            # Insert the imports after the auth import
            insert_pos = auth_match.end()
            content = content[:insert_pos] + misplaced_imports + '\n' + content[insert_pos:]
            
            print(f"  ✅ Fixed import order in {file_path}")
            
            # Write the fixed content back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            print(f"  ❌ Could not find auth import line in {file_path}")
    else:
        print(f"  ✅ {file_path} import order is correct")

def main():
    """Fix import order in all API files"""
    api_dir = 'api'
    
    if not os.path.exists(api_dir):
        print("API directory not found!")
        return
    
    # Get all Python files in the api directory
    api_files = [f for f in os.listdir(api_dir) if f.endswith('.py')]
    
    print(f"Checking {len(api_files)} API files for import order issues...")
    
    for api_file in api_files:
        file_path = os.path.join(api_dir, api_file)
        try:
            fix_import_order(file_path)
        except Exception as e:
            print(f"  ❌ Error checking {file_path}: {e}")
    
    print("\n✅ All API files have been checked!")

if __name__ == "__main__":
    main()
