# Default patterns to ignore, covering common project artifacts and large directories
DEFAULT_IGNORE_PATTERNS = [
    # Version control
    '.git/', '.svn/', '.hg/',

    # Node.js
    'node_modules/', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',

    # Python
    '__pycache__/', '*.pyc', '*.pyo', '*.pyd', '.venv/', 'venv/', 'env/',
    '*.egg-info/', 'dist/', 'build/',

    # Laravel
    'vendor/', 'storage/framework/', 'storage/logs/', '.env',

    # IDE/Editor specific
    '.vscode/', '.idea/', '*.suo', '*.ntvs*', '*.njsproj', '*.sln',

    # OS specific
    '.DS_Store', 'Thumbs.db',

    # Logs and temp files
    '*.log', '*.tmp', '*.temp',

    # Compiled files
    '*.o', '*.obj', '*.so', '*.dll', '*.lib', '*.out',

    # Archives
    '*.zip', '*.tar.gz', '*.rar',
]

# File extensions that are likely to be text-based and useful for prompts
# An empty list means all non-binary files are considered.
# Example: ALLOWED_EXTENSIONS = ['.py', '.js', '.html', '.css', '.md']
ALLOWED_EXTENSIONS = []

# File extensions to always treat as binary
BINARY_EXTENSIONS = [
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.tif', '.tiff',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.eot', '.otf', '.ttf', '.woff', '.woff2',
    '.mp3', '.wav', '.mp4', '.mov', '.avi',
    '.exe', '.bin', '.dll', '.so',
]