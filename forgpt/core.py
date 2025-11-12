import argparse
import json
import os
import fnmatch
import re
from dir_tree import DirectoryTree
import shutil
import sys
import subprocess # NEU
import platform   # NEU

# NEUE FUNKTION
def copy_to_clipboard(text: str):
    """Copies the given text to the system clipboard."""
    system = platform.system()
    try:
        if system == "Windows":
            process = subprocess.Popen(['clip.exe'], stdin=subprocess.PIPE, close_fds=True)
            process.communicate(input=text.encode('utf-8')) # oder 'mbcs'
            print("Content copied to clipboard (Windows).")
        elif system == "Darwin": # macOS
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(input=text.encode('utf-8'))
            print("Content copied to clipboard (macOS).")
        elif system == "Linux":
            try:
                process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
                process.communicate(input=text.encode('utf-8'))
                print("Content copied to clipboard (Linux with xclip).")
            except FileNotFoundError:
                try:
                    process = subprocess.Popen(['xsel', '--clipboard', '--input'], stdin=subprocess.PIPE)
                    process.communicate(input=text.encode('utf-8'))
                    print("Content copied to clipboard (Linux with xsel).")
                except FileNotFoundError:
                    print("Clipboard tool (xclip or xsel) not found on Linux. Please install one to use this feature.")
        else:
            print(f"Clipboard operations not supported on this platform: {system}")
    except Exception as e:
        print(f"Error copying to clipboard: {e}")


class FileCollector:
    # ... (Die gesamte FileCollector Klasse bleibt exakt so, wie sie in deinem letzten Post war) ...
    # (also init, reload_settings, load_global, load_local, save_local, save_global,
    # add_include, remove_include, add_exclude, remove_exclude, list_includes, list_excludes,
    # generate_tree, collect_files, _compile_patterns, _append_file_content, run, dry_run)
    # Diese Methoden müssen nicht geändert werden.
    def __init__(self, root_dir='.', use_global_config=False, permanent=False, follow_symlinks=False):
        self.root_dir = root_dir
        self.use_global_config = use_global_config
        self.permanent = permanent # Relevant für das Erstellen einer lokalen .gptignore
        self.follow_symlinks = follow_symlinks

        if self.use_global_config:
            self.config = self.load_global_config()
        elif self.local_config_exists():
            self.config = self.load_local_config()
        elif self.permanent: 
            self.config = self.load_local_config() 
        else: 
            self.config = self.load_global_config()
        
        self.reload_settings_from_permanent_config()

    def reload_settings_from_permanent_config(self):
        self.output_file = self.config.get("output_file", "allfiles.txt")
        self.ignore_file = self.config.get("ignore_file", ".gptignore")
        self.include_patterns = set(self.config.get("include_patterns", []))
        self.exclude_patterns = set(self.config.get("exclude_patterns", []))
        self.exclude_patterns.add(self.output_file)
        self.exclude_patterns.add(self.ignore_file) 


    def local_config_exists(self):
        local_config_path = os.path.join(self.root_dir, '.gptignore')
        return os.path.exists(local_config_path)

    def load_global_config(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        if not os.path.exists(config_path):
            return {"output_file": "allfiles.txt", "ignore_file": ".gptignore", "include_patterns": [], "exclude_patterns": []}
        with open(config_path, 'r') as config_file:
            return json.load(config_file)

    def load_local_config(self):
        local_config_path = os.path.join(self.root_dir, '.gptignore')
        
        if os.path.exists(local_config_path):
            with open(local_config_path, 'r') as config_file:
                try:
                    return json.load(config_file)
                except json.JSONDecodeError:
                    return self.load_global_config()
        elif self.permanent: 
            global_config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            if not os.path.exists(global_config_path):
                default_conf = {"output_file": "allfiles.txt", "ignore_file": ".gptignore", "include_patterns": [], "exclude_patterns": []}
                with open(local_config_path, 'w') as f:
                    json.dump(default_conf, f, indent=4)
                return default_conf
            try:
                shutil.copy(global_config_path, local_config_path)
                with open(local_config_path, 'r') as copied_file: 
                    return json.load(copied_file)
            except Exception as e:
                return self.load_global_config() 
        else: 
            return self.load_global_config()

    def _ensure_config_keys_exist(self):
        if 'include_patterns' not in self.config: self.config['include_patterns'] = []
        if 'exclude_patterns' not in self.config: self.config['exclude_patterns'] = []
        if 'output_file' not in self.config: self.config['output_file'] = "allfiles.txt"
        if 'ignore_file' not in self.config: self.config['ignore_file'] = ".gptignore"

    def save_local_config(self):
        self._ensure_config_keys_exist()
        local_config_path = os.path.join(self.root_dir, '.gptignore')
        with open(local_config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    def save_global_config(self):
        self._ensure_config_keys_exist()
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, 'w') as config_file:
            json.dump(self.config, config_file, indent=4)

    def add_include(self, pattern, permanent=False):
        self.include_patterns.add(pattern)
        if permanent:
            self._ensure_config_keys_exist()
            if pattern not in self.config['include_patterns']:
                self.config['include_patterns'].append(pattern)
            if self.use_global_config:
                self.save_global_config()
            else:
                self.save_local_config()

    def remove_include(self, pattern, permanent=False):
        if pattern in self.include_patterns:
            self.include_patterns.remove(pattern)
        if permanent:
            self._ensure_config_keys_exist()
            if pattern in self.config['include_patterns']:
                self.config['include_patterns'].remove(pattern)
            if self.use_global_config:
                self.save_global_config()
            else:
                self.save_local_config()

    def add_exclude(self, pattern, permanent=False):
        self.exclude_patterns.add(pattern)
        if permanent:
            self._ensure_config_keys_exist()
            if pattern not in self.config['exclude_patterns']:
                self.config['exclude_patterns'].append(pattern)
            if self.use_global_config:
                self.save_global_config()
            else:
                self.save_local_config()

    def remove_exclude(self, pattern, permanent=False):
        if pattern in self.exclude_patterns:
            self.exclude_patterns.remove(pattern)
        if permanent:
            self._ensure_config_keys_exist()
            if pattern in self.config['exclude_patterns']:
                self.config['exclude_patterns'].remove(pattern)
            if self.use_global_config:
                self.save_global_config()
            else:
                self.save_local_config()

    def list_includes(self):
        print("Currently included file patterns (from effective config):")
        for pattern in sorted(list(self.include_patterns)):
            print(f"  {pattern}")

    def list_excludes(self):
        print("Currently excluded file patterns (from effective config):")
        for pattern in sorted(list(self.exclude_patterns)):
            print(f"  {pattern}")

    def generate_tree(self):
        tree = DirectoryTree(
            root_dir=self.root_dir,
            exclude_dirs=set(), 
            exclude_files=self.exclude_patterns, 
            follow_symlinks_in_tree=self.follow_symlinks,
            show_file_sizes=True
        )
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write("File Structure:\n")
                tree_json_str = tree.to_json()
                tree_data = json.loads(tree_json_str)
                f.write(tree_data["tree_print"])
                f.write("\n\n")
        except IOError as e:
            print(f"Error writing to output file {self.output_file}: {e}")
            return

    def collect_files(self):
        compiled_include_patterns = self._compile_patterns(list(self.include_patterns))
        compiled_exclude_patterns = self._compile_patterns(list(self.exclude_patterns))
        
        try:
            with open(self.output_file, 'a', encoding='utf-8') as f_out:
                for root, dirs, files in os.walk(self.root_dir, followlinks=self.follow_symlinks):
                    dirs[:] = [
                        d for d in dirs 
                        if not any(fnmatch.fnmatch(d, pattern) for pattern in self.exclude_patterns)
                    ]
                    
                    for file_name in files:
                        file_path = os.path.join(root, file_name)
                        
                        # Calculate relative path for path-based pattern matching
                        relative_path = os.path.relpath(file_path, self.root_dir)
                        # Normalize to forward slashes (cross-platform compatibility)
                        relative_path = relative_path.replace(os.sep, '/')
                        
                        # Match against BOTH filename and relative path
                        # This enables both "*.v" (filename) and "spartan6/ddr3.v" (path) patterns
                        included = any(
                            re.fullmatch(pattern_re, file_name) or re.fullmatch(pattern_re, relative_path)
                            for pattern_re in compiled_include_patterns
                        )
                        excluded = any(
                            re.fullmatch(pattern_re, file_name) or re.fullmatch(pattern_re, relative_path)
                            for pattern_re in compiled_exclude_patterns
                        )
                        
                        if included and not excluded:
                            self._append_file_content(f_out, file_path)
        except IOError as e:
            print(f"Error appending to output file {self.output_file}: {e}")

    def _compile_patterns(self, patterns):
        compiled = []
        if not patterns: return compiled
        for p in patterns:
            if p == "*":
                compiled.append(r"^.*$") 
            elif p == "*.*":
                 compiled.append(r"^.*\..*$") 
            else:
                translated = fnmatch.translate(p)
                if translated.startswith("(?s:") and translated.endswith("\\Z"):
                    regex_body = translated[4:-3] 
                elif translated.endswith("\\Z"):
                    regex_body = translated[:-2]
                else: 
                    regex_body = translated
                compiled.append(f"^{regex_body}$")
        return compiled

    def _format_size(self, size_bytes):
        """Convert bytes to human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def _append_file_content(self, output_file_obj, file_path):
        try:
            if os.path.isdir(file_path): 
                return
            file_size = os.path.getsize(file_path)
            size_str = self._format_size(file_size)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f_content:
                content = f_content.read()
            output_file_obj.write(f"----- START OF {os.path.normpath(file_path)} ({size_str}) -----\n")
            output_file_obj.write(content)
            output_file_obj.write(f"\n----- END OF {os.path.normpath(file_path)} -----\n\n\n")
        except Exception as e:
            pass 

    def run(self):
        self.generate_tree()
        self.collect_files()

    def dry_run(self):
        compiled_include_patterns = self._compile_patterns(list(self.include_patterns))
        compiled_exclude_patterns = self._compile_patterns(list(self.exclude_patterns))

        print("\n--- Dry Run Mode ---")
        print(f"Root directory: {os.path.abspath(self.root_dir)}")
        print(f"Following symlinks: {self.follow_symlinks}")
        print(f"Include patterns (runtime): {sorted(list(self.include_patterns))}")
        print(f"Exclude patterns (runtime): {sorted(list(self.exclude_patterns))}")
        print("Scanning files...\n")

        for root, dirs, files in os.walk(self.root_dir, followlinks=self.follow_symlinks):
            dirs[:] = [
                d for d in dirs 
                if not any(fnmatch.fnmatch(d, pattern) for pattern in self.exclude_patterns)
            ]

            for file_name in files:
                file_path = os.path.join(root, file_name)
                
                included = any(re.fullmatch(p_re, file_name) for p_re in compiled_include_patterns)
                excluded = any(re.fullmatch(p_re, file_name) for p_re in compiled_exclude_patterns)
                
                if included and not excluded:
                    print(f"✅ {os.path.normpath(file_path)}")
                else:
                    reason = ""
                    if not included: reason += " (no include match)"
                    if excluded: reason += f" (exclude match)" 
                    print(f"❌ {os.path.normpath(file_path)}{reason}")
        print("\n--- End of Dry Run ---")


def main():
    parser = argparse.ArgumentParser(
        description="FileCollector CLI to manage file inclusion and exclusion.",
        epilog="""
Examples:
  4gpt                                # Run with current config.
  4gpt -c                             # Run and copy output to clipboard.
  4gpt --follow-symlinks -c           # Run, follow symlinks, and copy to clipboard.
  4gpt include "*.py" --permanent     # Permanently include Python files in local config.
  4gpt list-excludes --global-config  # List excludes from global config.
  4gpt --dry-run --follow-symlinks    # Dry run, following directory symlinks.
""",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Globale Optionen
    parser.add_argument('--dry-run', action='store_true',
                        help='Show which files would be included or excluded without writing output.')
    parser.add_argument('--global-config', action='store_true',
                        help='Use global config. If combined with --permanent, modifies global config.')
    parser.add_argument('--follow-symlinks', action='store_true',
                        help='Follow symbolic links to directories when collecting files and generating tree structure.')
    parser.add_argument('--to-clipboard', '-c', action='store_true',  # NEUER PARAMETER
                        help='Copy the content of the generated output file to the clipboard after a successful run.')

    subparsers = parser.add_subparsers(dest="command", title="Commands",
                                       description="Available commands:",
                                       help="Action to perform. If no command is given, a run is performed.")

    # Subkommandos (bleiben gleich)
    include_parser = subparsers.add_parser("include", help="Add a file pattern to the include list.")
    include_parser.add_argument("pattern", help="Pattern to include (e.g., '*.py').")
    include_parser.add_argument("--permanent", action="store_true", help="Make the inclusion permanent in the selected config.")

    exclude_parser = subparsers.add_parser("exclude", help="Add a file pattern to the exclude list.")
    exclude_parser.add_argument("pattern", help="Pattern to exclude (e.g., '*.png').")
    exclude_parser.add_argument("--permanent", action="store_true", help="Make the exclusion permanent in the selected config.")

    remove_include_parser = subparsers.add_parser("remove-include", help="Remove a file pattern from the include list.")
    remove_include_parser.add_argument("pattern", help="Pattern to remove from include list.")
    remove_include_parser.add_argument("--permanent", action="store_true", help="Remove permanently from the selected config.")

    remove_exclude_parser = subparsers.add_parser("remove-exclude", help="Remove a file pattern from the exclude list.")
    remove_exclude_parser.add_argument("pattern", help="Pattern to remove from exclude list.")
    remove_exclude_parser.add_argument("--permanent", action="store_true", help="Remove permanently from the selected config.")

    subparsers.add_parser("list-includes", help="List current include patterns based on effective config.")
    subparsers.add_parser("list-excludes", help="List current exclude patterns based on effective config.")


    args = parser.parse_args()

    use_global_conf_cli = args.global_config
    collector_init_permanent_flag = False
    if args.command in ["include", "exclude", "remove-include", "remove-exclude"] and \
       args.permanent and not use_global_conf_cli:
        collector_init_permanent_flag = True
    
    collector = FileCollector(
        root_dir=".", 
        use_global_config=use_global_conf_cli, 
        permanent=collector_init_permanent_flag,
        follow_symlinks=args.follow_symlinks
    )

    action_is_permanent = args.permanent if hasattr(args, 'permanent') and args.permanent else False
    command_executed = True 

    if args.command == "include":
        collector.add_include(args.pattern, permanent=action_is_permanent)
        print(f"Pattern '{args.pattern}' added to include list {'permanently.' if action_is_permanent else 'for this session.'}")
    elif args.command == "exclude":
        collector.add_exclude(args.pattern, permanent=action_is_permanent)
        print(f"Pattern '{args.pattern}' added to exclude list {'permanently.' if action_is_permanent else 'for this session.'}")
        if not action_is_permanent:  # If temporary, run immediately
            collector.run()
    elif args.command == "remove-include":
        collector.remove_include(args.pattern, permanent=action_is_permanent)
        print(f"Pattern '{args.pattern}' removed from include list {'permanently.' if action_is_permanent else 'for this session.'}")
    elif args.command == "remove-exclude":
        collector.remove_exclude(args.pattern, permanent=action_is_permanent)
        print(f"Pattern '{args.pattern}' removed from exclude list {'permanently.' if action_is_permanent else 'for this session.'}")
    elif args.command == "list-includes":
        collector.list_includes()
    elif args.command == "list-excludes":
        collector.list_excludes()
    else:
        command_executed = False


    if args.dry_run:
        collector.dry_run()
        # Nach einem Dry-Run wird nichts in die Zwischenablage kopiert
        # und auch kein Dateiinhalt direkt geprintet, da die Datei nicht (final) geschrieben wurde.
    elif not command_executed: # Kein Subkommando wurde ausgeführt, also ein normaler Run
        # print(f"Performing run... (Follow symlinks: {args.follow_symlinks})")
        try:
            collector.run() # Führt generate_tree() und collect_files() aus
            output_file_path = os.path.join(collector.root_dir, collector.output_file)
            print(f"Run finished. Output written to {output_file_path}")

            if args.to_clipboard:
                # In die Zwischenablage kopieren
                if os.path.exists(output_file_path):
                    try:
                        with open(output_file_path, 'r', encoding='utf-8') as f:
                            content_to_copy = f.read()
                        if content_to_copy:
                            copy_to_clipboard(content_to_copy)
                        else:
                            print(f"Output file '{output_file_path}' is empty. Nothing to copy to clipboard.")
                    except Exception as e:
                        print(f"Error reading output file '{output_file_path}' for clipboard: {e}")
                else:
                    print(f"Output file '{output_file_path}' not found. Cannot copy to clipboard.")
            else: # Nicht --to-clipboard
                if os.path.exists(output_file_path):
                    try:
                        with open(output_file_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                        if file_content:
                            print("\n--- Content of " + output_file_path + " ---")
                            
                            # Bestimme das Encoding von stdout, mit Fallback auf ASCII
                            stdout_encoding = sys.stdout.encoding if sys.stdout.encoding else 'ascii'
                            
                            # Versuche, den String für stdout zu kodieren und dabei Fehler zu ersetzen,
                            # dann wieder zu dekodieren, um ihn an print() zu übergeben.
                            # print() wird dann versuchen, diesen (potenziell modifizierten) String
                            # erneut gemäß sys.stdout.encoding zu behandeln.
                            # Diese Methode ist etwas umständlich, aber ein Weg, den Fehler abzufangen.
                            try:
                                print(file_content) # Erster Versuch
                            except UnicodeEncodeError:
                                print(f"Warning: Console encoding '{stdout_encoding}' cannot display all characters. Replacing unmappable characters.")
                                # Kodieren mit Fehlerersetzung, dann für print wieder dekodieren
                                # Dies stellt sicher, dass print einen String erhält, den es verarbeiten kann,
                                # auch wenn das bedeutet, dass einige Zeichen durch '?' ersetzt wurden.
                                printable_content = file_content.encode(stdout_encoding, errors='replace').decode(stdout_encoding)
                                print(printable_content)
                            print("--- End of Content ---")
                        else:
                            print(f"Output file '{output_file_path}' is empty. Nothing to display.")
                    except Exception as e:
                        print(f"Error reading or printing output file '{output_file_path}': {e}")
                else:
                    print(f"Output file '{output_file_path}' not found. Cannot display content.")
        except Exception as e:
            print(f"An error occurred during the run: {e}")

if __name__ == "__main__":
    main()