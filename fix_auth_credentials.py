#!/usr/bin/env python3
"""
Fix authentication credentials in all API files
"""

import os
import re

def fix_api_file(file_path):
    """Fix authentication credentials in a single API file"""
    print(f"Fixing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip files that don't have get_admin_user function
    if 'def get_admin_user(' not in content:
        print(f"  ✅ {file_path} doesn't need fixing")
        return
    
    # Add HTTPAuthorizationCredentials import if not present
    if 'HTTPAuthorizationCredentials' not in content:
        # Find the fastapi import line
        fastapi_import_pattern = r'from fastapi import ([^\\n]+)'
        fastapi_import_match = re.search(fastapi_import_pattern, content)
        
        if fastapi_import_match:
            # Add HTTPAuthorizationCredentials to the import
            current_imports = fastapi_import_match.group(1)
            if 'HTTPAuthorizationCredentials' not in current_imports:
                # Add the import on a new line
                insert_pos = fastapi_import_match.end()
                new_import = "\\nfrom fastapi.security import HTTPAuthorizationCredentials"
                content = content[:insert_pos] + new_import + content[insert_pos:]
    
    # Fix the get_admin_user function
    old_function = r'def get_admin_user\(db: Session = Depends\(get_db\)\):\s*return get_current_admin_user\(security, db\)'
    new_function = '''def get_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    return get_current_admin_user(credentials, db)'''
    
    content = re.sub(old_function, new_function, content, flags=re.MULTILINE | re.DOTALL)
    
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
    
    print("\\n✅ All API files have been processed!")
    print("Now commit and push the changes to Railway.")

if __name__ == "__main__":
    main()
