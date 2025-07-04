import os
import argparse
import pyperclip
from concurrent.futures import ThreadPoolExecutor, as_completed
from clipbase.config import DEFAULT_IGNORE_PATTERNS, ALLOWED_EXTENSIONS
from clipbase.utils import (
    is_binary_by_content, is_binary_by_extension, gitignore_to_regex,
    is_ignored, build_file_tree, generate_tree_string, get_gitignore_patterns
)

class CodebaseGenerator:
    def __init__(self, args):
        self.args = args
        self.source_dir = os.path.abspath(args.directory)
        self.ignore_rules = []
        self.collected_files_data = []

    def run(self):
        if not os.path.isdir(self.source_dir):
            print(f"Error: Directory not found at '{self.source_dir}'")
            return

        self._build_ignore_rules()
        self._collect_and_process_files_concurrently()
        self._generate_output()

    def _build_ignore_rules(self):
        patterns = []
        if not self.args.no_defaults:
            patterns.extend(DEFAULT_IGNORE_PATTERNS)
        
        if not self.args.no_gitignore:
            gitignore_path = os.path.join(self.source_dir, '.gitignore')
            patterns.extend(get_gitignore_patterns(gitignore_path))
        
        patterns.extend(self.args.exclude)

        # Process patterns into regex rules, handling negation
        raw_rules = [p for p in patterns if p and not p.startswith('#')]
        self.ignore_rules = [gitignore_to_regex(p) for p in raw_rules]

    def _collect_and_process_files_concurrently(self):
        print("Scanning project and collecting all file paths...")
        candidate_paths = []
        for root, dirs, files in os.walk(self.source_dir, topdown=True):
            rel_root = os.path.relpath(root, self.source_dir)
            if rel_root == '.':
                rel_root = ''

            # Prune ignored directories
            dirs[:] = [d for d in dirs if not is_ignored(os.path.join(rel_root, d), self.ignore_rules)]

            for file in files:
                candidate_paths.append(os.path.join(root, file))
        
        print(f"Found {len(candidate_paths)} total files. Processing...")

        with ThreadPoolExecutor() as executor:
            future_to_path = {executor.submit(self._process_file, path): path for path in candidate_paths}
            for future in as_completed(future_to_path):
                try:
                    result = future.result()
                    if result:
                        self.collected_files_data.append(result)
                except Exception as e:
                    path = future_to_path[future]
                    print(f"Error processing file {path}: {e}")

        self.collected_files_data.sort(key=lambda x: x[0])
        print(f"Collected content from {len(self.collected_files_data)} files.")

    def _process_file(self, full_path):
        relative_path = os.path.relpath(full_path, self.source_dir)
        
        if is_ignored(relative_path, self.ignore_rules):
            return None

        if ALLOWED_EXTENSIONS and os.path.splitext(relative_path)[1] not in ALLOWED_EXTENSIONS:
            return None

        if is_binary_by_extension(relative_path) or is_binary_by_content(full_path):
            print(f"  - Skipping binary file: {relative_path}")
            return None

        try:
            if os.path.getsize(full_path) > self.args.max_size:
                print(f"  - Skipping large file: {relative_path} (> {self.args.max_size} bytes)")
                return None
        except OSError:
            return None

        print(f"  - Fetching content from: {relative_path}")
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as content_file:
                content = content_file.read()
            return relative_path, content
        except Exception as e:
            return relative_path, f"Error reading file: {e}"

    def _generate_output(self):
        output_content = []
        
        project_name = os.path.basename(self.source_dir)
        output_content.append("Directory Structure:\n")
        
        collected_files = [item[0] for item in self.collected_files_data]
        file_tree = build_file_tree(collected_files)
        tree_string = generate_tree_string(file_tree)
        output_content.append(f"└── {project_name}/\n{tree_string}\n")

        for relative_path, content in self.collected_files_data:
            output_content.append(f"\n---\nFile: /{relative_path.replace(os.sep, '/')}\n---\n")
            output_content.append(content)
        
        final_output = "\n".join(output_content)

        if self.args.clipboard:
            try:
                pyperclip.copy(final_output)
                print("\nOutput successfully copied to clipboard.")
            except pyperclip.PyperclipException:
                print("\nError: Could not copy to clipboard. Pyperclip is not configured for your system.")
                print("Writing to file instead.")
                self._write_to_file(final_output)
        else:
            self._write_to_file(final_output)

    def _write_to_file(self, content):
        try:
            with open(self.args.output, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(content)
            print(f"\nSuccessfully generated '{self.args.output}'.")
        except IOError as e:
            print(f"Error writing to output file: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Convert a local project folder into a single formatted text file for LLM prompts.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "directory",
        nargs='?',
        default=os.getcwd(),
        help="The path to the local project directory. Defaults to the current directory."
    )
    parser.add_argument(
        "-o", "--output",
        default="prompt.txt",
        help="The name of the output file. (default: prompt.txt)"
    )
    parser.add_argument(
        "-c", "--clipboard",
        action="store_true",
        help="Copy the output to the clipboard instead of writing to a file."
    )
    parser.add_argument(
        "-e", "--exclude",
        action='append',
        default=[],
        help="Additional glob patterns to exclude. Can be used multiple times."
    )
    parser.add_argument(
        "--no-defaults",
        action="store_true",
        help="Disable the default ignore patterns (e.g., node_modules, .git, vendor)."
    )
    parser.add_argument(
        "--no-gitignore",
        action="store_true",
        help="Do not use the .gitignore file for exclusion."
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=1024 * 1024,  # 1MB
        help="Maximum file size in bytes to include. (default: 1048576)"
    )

    args = parser.parse_args()
    generator = CodebaseGenerator(args)
    generator.run()

if __name__ == "__main__":
    main()