# === IMPORTS ===

# Standard library imports
from pathlib import Path

# === FUNCTION DEFINITIONS ===

def folder_structure(user_path):
    """
    Accepts string of a path to a folder and returns the folder structure
    """
    user_path = Path(user_path)
    
    # Reject path to filename
    if user_path.is_file:
        print('Path to a file was provided. Folder structure is generated from the parent folder:')
        user_path = user_path.parent
        print(user_path)

    print(f'+ {user_path}')
    for path in sorted(user_path.rglob('*')):
        depth = len(path.relative_to(user_path).parts)
        spacer = '    ' * depth
        print(f'{spacer}+ {path.name}')

# ============================

directory = input('Enter path: ')
folder_structure(directory)

# TODO: write to file