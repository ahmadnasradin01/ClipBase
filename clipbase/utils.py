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

def gitignore_to_regex(pattern):
    """Converts a .gitignore pattern to a regex pattern."""
    if pattern.startswith('!'):
        # Negated patterns are handled separately
        return None, gitignore_to_regex(pattern[1:])[0]

    regex = ''
    if pattern.startswith('/'):
        regex += '^'
        pattern = pattern[1:]
    elif '/**/' in pattern:
        pattern = pattern.replace('**/', '(.*/)?')
    elif pattern.startswith('**/'):
        pattern = pattern.replace('**/', '(.*/)?')
    elif '/' in pattern:
        # Patterns with slashes that don't start with one can match anywhere
        pass
    else:
        # Patterns without slashes match at any level
        regex += '(^|.*/)'

    # Escape special regex characters, but keep our wildcards
    pattern = re.escape(pattern).replace(r'\*', '.*').replace(r'\?', '.')

    if pattern.endswith('/'):
        regex += pattern + '.*'
    else:
        regex += pattern + '(/.*)?$'
    
    return re.compile(regex), None

def is_ignored(path, ignore_rules):
    """
    Checks if a path should be ignored based on a list of regex rules.
    Handles negation ('!') correctly.
    """
    ignored = False
    path = path.replace(os.sep, '/') # Use forward slashes for matching
    for ignore_regex, negate_regex in ignore_rules:
        if ignore_regex and ignore_regex.match(path):
            ignored = True
        if negate_regex and negate_regex.match(path):
            ignored = False
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