#!/usr/bin/env python3
"""
Fix API dependency issues across all API files
"""

import os
import re

def fix_api_file(file_path):
    """Fix lambda dependency issues in a single API file"""
    print(f"Fixing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if the file needs fixing
    if 'lambda: get_current_admin_user(security, db)' not in content:
        print(f"  ✅ {file_path} already fixed or doesn't need fixing")
        return
    
    # Add the dependency function after the imports
    if 'def get_admin_user(' not in content:
        # Find the line with auth imports
        auth_import_pattern = r'from auth import.*'
        auth_import_match = re.search(auth_import_pattern, content)
        
        if auth_import_match:
            # Add the dependency function after the auth import
            dependency_function = """
# Dependency function for admin authentication
def get_admin_user(db: Session = Depends(get_db)):
    return get_current_admin_user(security, db)
"""
            
            # Insert after the auth import line
            insert_pos = auth_import_match.end()
            content = content[:insert_pos] + dependency_function + content[insert_pos:]
    
    # Replace all lambda functions
    content = re.sub(
        r'Depends\(lambda: get_current_admin_user\(security, db\)\)',
        'Depends(get_admin_user)',
        content
    )
    
    # Write the fixed content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ Fixed {file_path}")

def main():
    """Fix all API files"""
    api_dir = 'api'
    
    if not os.path.exists(api_dir):
        print("API directory not found!")
        return
    
    # Get all Python files in the api directory
    api_files = [f for f in os.listdir(api_dir) if f.endswith('.py')]
    
    print(f"Found {len(api_files)} API files to check...")
    
    for api_file in api_files:
        file_path = os.path.join(api_dir, api_file)
        try:
            fix_api_file(file_path)
        except Exception as e:
            print(f"  ❌ Error fixing {file_path}: {e}")
    
    print("\n✅ All API files have been processed!")
    print("Now commit and push the changes to Railway.")

if __name__ == "__main__":
    main()
