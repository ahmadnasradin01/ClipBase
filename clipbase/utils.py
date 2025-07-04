import os
import re
from clipbase.config import BINARY_EXTENSIONS

def is_binary_by_extension(filepath):
    """Check if a file is binary based on its extension."""
    return os.path.splitext(filepath)[1].lower() in BINARY_EXTENSIONS

def is_binary_by_content(filepath):
    """Check if a file is likely binary by reading a chunk of it."""
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
            return b'\0' in chunk
    except IOError:
        return True

def get_gitignore_patterns(gitignore_path):
    """Reads and returns patterns from a .gitignore file."""
    if not os.path.exists(gitignore_path):
        return []
    with open(gitignore_path, 'r', encoding='utf-8', errors='ignore') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def gitignore_to_regex(pattern, is_dir_only=False):
    """Converts a .gitignore pattern to a regex pattern."""
    if pattern.startswith('!'):
        return None, gitignore_to_regex(pattern[1:], is_dir_only)[0]

    regex = ''
    # Anchor the pattern to the start if it begins with a slash
    if pattern.startswith('/'):
        regex += '^'
        pattern = pattern[1:]
    # If the pattern does not contain a slash, it should match anywhere
    elif '/' not in pattern:
        regex += '(.*/)?'

    # Handle directory-only patterns
    if pattern.endswith('/'):
        is_dir_only = True
        pattern = pattern[:-1]

    # Escape the pattern and convert gitignore wildcards to regex wildcards
    pattern = re.escape(pattern).replace(r'\*\*', '.*').replace(r'\*', '[^/]*').replace(r'\?', '.')
    
    regex += pattern
    
    if is_dir_only:
        regex += '(/.*)?$'
    else:
        # Match files or directories
        regex += '(/.*)?$'

    return re.compile(regex), None

def is_ignored(path, ignore_rules):
    """
    Checks if a path should be ignored based on a list of regex rules.
    Handles negation ('!') correctly.
    """
    path_to_check = path.replace(os.sep, '/')
    if not path_to_check.startswith('/'):
        path_to_check = '/' + path_to_check

    ignored = False
    for ignore_regex, negate_regex in ignore_rules:
        if ignore_regex and ignore_regex.search(path_to_check):
            ignored = True
        if negate_regex and negate_regex.search(path_to_check):
            ignored = False # Un-ignore if a negation pattern matches
    
    return ignored

def build_file_tree(file_paths):
    """Builds a nested dictionary representing the file tree structure."""
    tree = {}
    for path in file_paths:
        parts = path.split(os.sep)
        current_level = tree
        for part in parts:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
    return tree

def generate_tree_string(tree, prefix=""):
    """Generates a string representation of the file tree."""
    entries = sorted(tree.keys())
    output = ""
    for i, entry in enumerate(entries):
        is_last = i == (len(entries) - 1)
        connector = "└── " if is_last else "├── "
        output += f"{prefix}{connector}{entry}\n"
        
        if tree[entry]: # It's a directory, recurse
            extension = "    " if is_last else "│   "
            output += generate_tree_string(tree[entry], prefix + extension)
    return output