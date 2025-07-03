# ClipBase CLI

A powerful and flexible command-line tool to convert a local project directory into a single, formatted text file. It's designed to create comprehensive prompts for Large Language Models (LLMs) by including a directory tree and the contents of relevant files, while automatically excluding common and project-specific cruft.

## Features

-   **One-Command Execution**: Run `getcodebase` in any project directory to instantly generate the output.
-   **Intelligent Filtering**:
    -   Automatically respects rules from your project's `.gitignore` file.
    -   Comes with a comprehensive list of default ignores for common directories (`node_modules`, `.git`), languages (Python, Laravel), and artifacts (`build`, `dist`).
    -   Allows for custom exclusion patterns via command-line arguments.
-   **Advanced Directory Tree**: Creates a clean, text-based tree of your project structure.
-   **Smart File Handling**:
    -   Detects and skips binary files (images, executables).
    -   Excludes overly large files to keep the output manageable.
-   **Clipboard Integration**: Directly copy the output to your clipboard with the `-c` flag.
-   **Cross-Platform**: Works seamlessly on Windows, macOS, and Linux.
-   **Zero Dependencies**: Runs with a standard Python installation (pyperclip is included on install).

## Installation

You need Python 3.6+ installed and on your system's PATH.

1.  **Create the files**: Create the directory structure and files as listed above (`setup.py`, `clipbase/` directory, etc.).

2.  **Open Terminal/CMD/PowerShell**: Navigate to the root directory where you created `setup.py`.

3.  **Install the package**: Run the following command to install `clipbase` globally on your system in "editable" mode. This means any changes you make to the script are immediately available.

    ```bash
    pip install -e .
    ```

    After installation, the `getcodebase` command will be available system-wide.

## Usage

Once installed, you can use the `getcodebase` command from any directory.

#### Basic Usage

Simply navigate to your project's root directory and run:

```bash
getcodebase
```

This will scan the current directory and create a prompt.txt file inside it.

### Advanced Usage

#### Specify a Directory and Output File

```bash
getcodebase C:\Users\You\Projects\my-laravel-app -o laravel_prompt.txt
```

#### Copy Output Directly to Clipboard

This is extremely useful for pasting directly into an LLM chat interface.

```bash
getcodebase -c
```

#### Exclude Additional Files or Directories

You can add custom ignore patterns. For example, to exclude all test files:

```bash
getcodebase --exclude "*_test.py" --exclude "tests/"
```

#### Run Without Default Ignores

If you want to include files that are normally ignored (like dist or .env):

```bash
getcodebase --no-defaults
```

#### Ignore the .gitignore File

To process all files without considering the project's .gitignore:

```bash
getcodebase --no-gitignore
```
### Full Options
```
usage: getcodebase [-h] [-o OUTPUT] [-c] [-e EXCLUDE] [--no-defaults] [--no-gitignore] [--max-size MAX_SIZE] [directory]

Convert a local project folder into a single formatted text file for LLM prompts.

positional arguments:
  directory             The path to the local project directory. Defaults to the current directory.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        The name of the output file. (default: prompt.txt)
  -c, --clipboard       Copy the output to the clipboard instead of writing to a file.
  -e EXCLUDE, --exclude EXCLUDE
                        Additional glob patterns to exclude. Can be used multiple times.
  --no-defaults         Disable the default ignore patterns (e.g., node_modules, .git, vendor).
  --no-gitignore        Do not use the .gitignore file for exclusion.
  --max-size MAX_SIZE   Maximum file size in bytes to include. (default: 1048576)