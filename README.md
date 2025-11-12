# 4gpt

`4gpt` is a CLI tool for automated collection and analysis of files within a project.  
Included and excluded files can be controlled dynamically or permanently via `.gptignore` and/or a central `config.json`.

## 🔧 Features

- 🗂️ Generates a file structure overview as a tree + JSON
- 📂 **Whitelist-based filtering:** only files matching `include_patterns` are collected (see [How File Filtering Works](#-how-file-filtering-works))
- 📏 **File size display:** shows human-readable file sizes (B, KB, MB, GB) for each collected file
- 🧠 Local and global configuration management (`--global-config`)
- ✅ Temporary or permanent changes with `--permanent`)
- 🔍 Dry-run mode to preview filtering before execution

## ⚡ Quick Install (Recommended)

Install directly from GitHub:

```bash
pip install "git+https://github.com/krausality/4gpt.git"
```

To install a specific version or for production builds, pin the commit:

```bash
pip install "git+https://github.com/krausality/4gpt.git@<commit-hash>"
```

**Note**: This method requires an internet connection and Git to be available in your environment.

## � Dependencies

`4gpt` depends on the following external packages:

- **[dir_tree](https://github.com/krausality/dir_tree)** (v0.2.0+): Generates the directory tree structure with file sizes
  - Automatically installed from GitHub when you install 4gpt
  - Provides the file tree visualization and file size display features

**Note:** Dependencies are automatically installed when using any of the installation methods above.

## �🖥️ Installation

```bash
git clone https://github.com/krausality/4gpt.git
cd 4gpt
pip install -r requirements.txt
pip install .
```

Alternatively, as a wheel:

```bash
python -m build --wheel
pip install dist/4gpt-*.whl
```

## 🔄 Updating

To update `4gpt` to the latest version:

**From GitHub (Quick Install users):**
```bash
pip install --upgrade "git+https://github.com/krausality/4gpt.git"
```

**From local clone:**
```bash
cd 4gpt
git pull
pip install --upgrade -r requirements.txt
pip install --upgrade .
```

**Editable install (Development Mode):**
```bash
cd 4gpt
git pull
# Dependencies are automatically updated
```

**Note:** Updates will also pull the latest compatible version of `dir_tree` as specified in `requirements.txt`.


## 🛠  Development Mode (Editable Installs)

If you plan to **develop or modify this project locally**, it's recommended to use an **editable install**. This allows Python to load the package **directly from your source directory**, so any code changes are reflected immediately — no need to reinstall after every edit.

### Setup

```bash
cd 4gpt
python -m venv .venv
source .venv/bin/activate      # or .venv\Scripts\activate on Windows
pip install --editable .
```

Once installed, you can run the tool in either of the following ways:

### ✅ Option 1: Module Invocation

```bash
python -m 4gpt COMMAND ...
```

  - Runs the package via the Python module system.
  - Always works inside an activated virtual environment.

### ✅ Option 2: Executable Invocation

```bash
4gpt COMMAND ...
```

  - A **console script entry point** is automatically created during install.
  - On Windows: creates `4gpt.exe` in `.venv\Scripts\`
  - On macOS/Linux: creates `4gpt` in `.venv/bin/`

💡 **Pro tip**: Check where the executable lives with:

```bash
where 4gpt    # on Windows
which 4gpt    # on macOS/Linux
```

If the command isn’t found, make sure your virtual environment is activated and your PATH is correctly set.

-----

### Optional: Strict Editable Mode

If you want more control over which files are actually included in the package (e.g. to detect missing modules or simulate a release install), enable **strict mode**:

```bash
pip install -e . --config-settings editable_mode=strict
```

In this mode:

  - **New files won’t be exposed automatically** — you’ll need to reinstall to pick them up.
  - The install behaves more like a production wheel, which is useful for debugging packaging issues.

-----

### Notes

  - Code edits are reflected **immediately** in both normal and strict modes.
  - Any changes to **dependencies**, **entry-points**, or **project metadata** require reinstallation.
  - If you encounter import issues (especially with namespace packages), consider switching to a `src/`-based layout.  
      See the Python Packaging Authority’s recommendations for [modern package structures](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/).


## 🚀 Usage

```bash
4gpt                                # Runs analysis with current configuration
4gpt include "*.ts"                # Temporarily include .ts files
4gpt exclude "*.png" --permanent  # Permanently exclude PNG files
4gpt list-includes                 # Shows current include patterns
4gpt list-excludes --global-config  # Shows global excludes

```


4gpt: Standardverhalten. dir_tree zeigt Symlinks zu Verzeichnissen als mylink -> ziel, collect_files folgt ihnen nicht.

4gpt --follow-symlinks: dir_tree expandiert Symlinks zu Verzeichnissen in der Struktur, collect_files folgt ihnen und sammelt Inhalte.



## 🕵️ Dry Run Mode

Use `--dry-run` to preview which files would be included or excluded **without writing anything to `allfiles.txt`** or modifying any config files.

This is useful to test inclusion/exclusion patterns before running the actual collection.

```bash
4gpt --dry-run
```

Example output:

```bash
--- Dry Run Mode ---
Include patterns: {'*.py', '*.md'}
Exclude patterns: {'*.png', '*.svg', 'allfiles.txt', '.gptignore'}

✅ ./main.py
✅ ./utils/helper.py
❌ ./logo.png
❌ ./dist/bundle.zip
```

You can combine this with `--global-config` to simulate the global configuration as well:

```bash
4gpt --dry-run --global-config
```

## Console Output and Encoding

This tool and its dependency `dir_tree` use Unicode characters for visual elements (like tree structures) and aim to produce UTF-8 encoded output.

If you see garbled characters (e.g., `Ôö£ÔöÇÔöÇ`) when running scripts directly in your console (this does not affect the content of the generated `allfiles.txt` which is always UTF-8):

*   **Windows CMD:** Run `chcp 65001` in your CMD session before executing the script.
*   **Windows PowerShell:** Run `$OutputEncoding = [System.Text.Encoding]::UTF8` in your PowerShell session.
*   **Windows Terminal:** It is highly recommended to use Windows Terminal, which handles UTF-8 much better by default.
*   **Linux/macOS:** Ensure your locale (e.g., `LANG` environment variable) is set to a UTF-8 variant (like `en_US.UTF-8`).

Additionally, ensure your console is using a font that supports a wide range of Unicode characters (e.g., Consolas, Cascadia Code, DejaVu Sans Mono).

## ⚙️ Configuration Logic

| Mode                                | Configuration Source                          |
|-------------------------------------|-----------------------------------------------|
| `4gpt`                              | Local `.gptignore` or global `config.json`    |
| `--global-config`                   | Ignores local config, uses `config.json`      |
| `--permanent` without `--global-config` | Creates/modifies local `.gptignore`      |
| `--permanent --global-config`       | Modifies the global configuration permanently |

## 📂 Example Output

```txt
File Structure:
project/
├── .gptignore (234.0 B)
├── main.py (2.3 KB)
└── utils/
    └── helper.py (856.0 B)

----- START OF main.py (2.3 KB) -----
import argparse
...
----- END OF main.py -----


----- START OF utils\helper.py (856.0 B) -----
def helper_function():
    pass
----- END OF utils\helper.py -----
```

The generated `allfiles.txt` contains:
1. **File tree structure** showing all files with their sizes (filtered by `exclude_patterns`)
2. **Concatenated file contents** with headers showing the file path and size in human-readable format (KB, MB, etc.)

All file contents are filtered by both `include_patterns` and `exclude_patterns`.

## 🎯 How File Filtering Works

Understanding the **whitelist-based filtering mechanism** is crucial to using `4gpt` effectively.

### Two-Stage Output Structure

The generated `allfiles.txt` consists of **two distinct sections**:

#### 1. **File Tree** (Visual Structure)
- Shows **all files and directories** in your project
- Filtered **only** by `exclude_patterns`
- Provides a complete structural overview
- **Does NOT** consider `include_patterns`

#### 2. **File Contents** (Concatenated Code)
- Contains the **actual content** of files
- Filtered by **BOTH** `include_patterns` AND `exclude_patterns`
- Uses a **whitelist approach**: only files matching at least one `include_pattern` are included
- Files must **match an include pattern** AND **not match any exclude pattern**
- Each file is prefixed with a header showing its **path and size** in human-readable format:
  ```
  ----- START OF path/to/file.py (12.3 KB) -----
  ```

### The Whitelist Principle

**Critical:** A file will **NEVER** appear in the content section unless it matches at least one pattern in `include_patterns`.

```python
# Simplified filtering logic from core.py
included = any(pattern matches file for pattern in include_patterns)
excluded = any(pattern matches file for pattern in exclude_patterns)

if included and not excluded:
    # ✅ File content is appended to allfiles.txt
else:
    # ❌ File is skipped (may still appear in tree)
```

### Example Scenario

Given this configuration:

```json
{
  "include_patterns": ["*.py", "*.md"],
  "exclude_patterns": ["*.png", "test_*"]
}
```

**File tree will show:**
- ✅ `main.py`
- ✅ `README.md`
- ✅ `config.json` (shown in tree, not in content!)
- ✅ `test_utils.py` (shown in tree, not in content!)
- ❌ `logo.png` (excluded from tree AND content)

**File contents will include:**
- ✅ `main.py` (matches `*.py`, not excluded)
- ✅ `README.md` (matches `*.md`, not excluded)
- ❌ `config.json` (no include match - even though not explicitly excluded!)
- ❌ `test_utils.py` (matches `*.py` but excluded by `test_*`)
- ❌ `logo.png` (explicitly excluded)

### Default Behavior

The global `config.json` comes with a comprehensive whitelist of common code file types:

```json
"include_patterns": [
    "*.py", "*.js", "*.ts", "*.tsx", "*.java", "*.cpp", "*.c", 
    "*.md", "*.json", "*.yaml", "*.yml", "*.sh", "*.sql",
    "Dockerfile", /* ... and more */
]
```

**This means:**
- Binary files (`.exe`, `.dll`, `.so`) are automatically excluded
- Media files (`.jpg`, `.gif`, `.mp4`) are automatically excluded  
- Archive files (`.zip`, `.tar`, `.gz`) are automatically excluded
- **Any file type not listed** is excluded from content collection

### Why This Design?

1. **🔒 Security:** Prevents accidental inclusion of credentials, API keys, or sensitive data often stored in non-code files
2. **⚡ Performance:** Avoids processing large binary files or archives
3. **🎯 Relevance:** Focuses output on human-readable source code and documentation
4. **🛡️ Safety:** Reduces risk of encoding errors from binary data

### Customizing the Whitelist

To include additional file types:

```bash
# Temporarily for one run
4gpt include "*.toml"

# Permanently in local config
4gpt include "*.config" --permanent

# Permanently in global config
4gpt include "*.env" --permanent --global-config
```

To see what's currently included:

```bash
4gpt list-includes
4gpt list-includes --global-config  # for global config
```

### Troubleshooting

**Problem:** "My file appears in the tree but not in the content section"

**Solution:** The file doesn't match any `include_pattern`. Either:
1. Add the file extension to includes: `4gpt include "*.yourext" --permanent`
2. Use dry-run to verify: `4gpt --dry-run` (will show `"(no include match)"`)

**Problem:** "I want ALL files included"

**Solution:** Add a catch-all pattern (use with caution):
```bash
4gpt include "*" --permanent
```

## 📄 License

This project is licensed under the GNU GPL 3 License. See [LICENSE](LICENSE).


---

+++OUTDATED+++

"""
2gpt

Lokale config wird ausgelesen falls sie exististiert 
Falls lokale config nicht existiert. Globale config auslesen.
Einen run starten mit determinierter config.


2gpt include "file.py"

Lokale config wird ausgelesen falls sie exististiert 
Falls lokale config nicht existiert. Globale config auslesen.

file.py wird nur für den direkt folgenden run included, config files bleiben unverändert.
Einen run starten mit determinierter config.


2gpt include "file.py" --permanent

Lokale config wird ausgelesen falls sie exististiert 
Falls lokale config nicht existiert. Globale config auslesen und als .gptignore in
das jeweilig rootverzeichnis abspeichern.
Dann die include "file.py" operation auf der configdatei durschführen, sodass "file.py" jetzt permanent und für
erstmal alle zukünftigen runs included ist.

2gpt include "file.py" --permanent --global-config

Lokale config wird ignoriert
Globale config auslesen.
Dann die include "file.py" operation auf der globalen configdatei durchführen, sodass "file.py" jetzt permanent
und für alle zukünftigen runs included ist, welche die globale config nutzen müssen.


Einen run starten mit determinierter config.


Globale config wird nur ausgelesen fall "--global-config" als parameter, dann egal ob lokale existiert

Perm



---------------------


To implement the desired behavior for the **CLI tool** with local and global configuration management for `include`, `exclude`, `list-includes`, `list-excludes`, and `remove` functionality, here’s how the CLI should behave for each command:

### Overall Workflow for Local and Global Configurations:

1. **Default Run (`2gpt`)**:
    - **Local config is used** if it exists.
    - **If local config does not exist**, the global config is used.
    - Perform the run with the determined config (local or global).

2. **Temporary Include (`2gpt include "file.py"`)**:
    - **Local config is used** if it exists.
    - **If local config does not exist**, the global config is used.
    - Include the file `file.py` for this run temporarily (the config files remain unchanged).
    - Start a run with the determined config and the temporary include.

3. **Permanent Include Locally (`2gpt include "file.py" --permanent`)**:
    - **Local config is used** if it exists.
    - **If local config does not exist**, the global config is copied to a new local `.gptignore` file.
    - Modify the local config to include `file.py` permanently.
    - Start a run with the modified local config.

4. **Permanent Include Globally (`2gpt include "file.py" --permanent --global-config`)**:
    - **Local config is ignored**.
    - **Global config is used**.
    - Modify the global config to include `file.py` permanently.
    - Start a run with the modified global config.

---

### Adding `exclude`, `list-includes`, `list-excludes`, and `remove` Functionality:

1. **Temporary Exclude (`2gpt exclude "file.py"`)**:
    - **Local config is used** if it exists.
    - **If local config does not exist**, the global config is used.
    - Exclude the file `file.py` for this run temporarily (the config files remain unchanged).
    - Start a run with the determined config and the temporary exclusion.

2. **Permanent Exclude Locally (`2gpt exclude "file.py" --permanent`)**:
    - **Local config is used** if it exists.
    - **If local config does not exist**, the global config is copied to a new local `.gptignore` file.
    - Modify the local config to exclude `file.py` permanently.
    - Start a run with the modified local config.

3. **Permanent Exclude Globally (`2gpt exclude "file.py" --permanent --global-config`)**:
    - **Local config is ignored**.
    - **Global config is used**.
    - Modify the global config to exclude `file.py` permanently.
    - Start a run with the modified global config.

4. **List Includes (`2gpt list-includes`)**:
    - **Local config is used** if it exists.
    - **If local config does not exist**, the global config is used.
    - List all files or patterns that are included in the config.

5. **List Includes Globally (`2gpt list-includes --global-config`)**:
    - **Local config is ignored**.
    - **Global config is used**.
    - List all files or patterns that are included in the global config.

6. **List Excludes (`2gpt list-excludes`)**:
    - **Local config is used** if it exists.
    - **If local config does not exist**, the global config is used.
    - List all files or patterns that are excluded in the config.

7. **List Excludes Globally (`2gpt list-excludes --global-config`)**:
    - **Local config is ignored**.
    - **Global config is used**.
    - List all files or patterns that are excluded in the global config.

8. **Remove Include/Exclude Locally (`2gpt remove-include "file.py"` or `2gpt remove-exclude "file.py"`)**:
    - **Local config is used** if it exists.
    - **If local config does not exist**, the global config is used.
    - Remove the specified file or pattern (`file.py`) from the inclusion/exclusion list.
    - If the file is removed temporarily, the config remains unchanged.
    - **If `--permanent` is specified**, the change is applied permanently to the local config.

9. **Remove Include/Exclude Globally (`2gpt remove-include "file.py" --permanent --global-config` or `2gpt remove-exclude "file.py" --permanent --global-config`)**:
    - **Local config is ignored**.
    - **Global config is used**.
    - Remove the specified file or pattern (`file.py`) from the inclusion/exclusion list in the global config permanently.

---

### Command Breakdown:

#### 1. **Default Run (`2gpt`)**:
- **Local config** is used if it exists. If not, the **global config** is used.
- Executes a run based on the configuration.

#### 2. **Include**:
- `2gpt include "file.py"`:
    - Temporarily includes `file.py` for the next run without modifying the config files.

- `2gpt include "file.py" --permanent`:
    - Modifies the **local config** permanently to include `file.py`. If no local config exists, the global config is copied to the local `.gptignore`.

- `2gpt include "file.py" --permanent --global-config`:
    - Modifies the **global config** permanently to include `file.py`. The local config is ignored.

#### 3. **Exclude**:
- `2gpt exclude "file.py"`:
    - Temporarily excludes `file.py` for the next run without modifying the config files.

- `2gpt exclude "file.py" --permanent`:
    - Modifies the **local config** permanently to exclude `file.py`. If no local config exists, the global config is copied to the local `.gptignore`.

- `2gpt exclude "file.py" --permanent --global-config`:
    - Modifies the **global config** permanently to exclude `file.py`. The local config is ignored.

#### 4. **List Includes**:
- `2gpt list-includes`:
    - Lists all files or patterns included in the **local config** (if it exists) or the **global config**.

- `2gpt list-includes --global-config`:
    - Lists all files or patterns included in the **global config**.

#### 5. **List Excludes**:
- `2gpt list-excludes`:
    - Lists all files or patterns excluded in the **local config** (if it exists) or the **global config**.

- `2gpt list-excludes --global-config`:
    - Lists all files or patterns excluded in the **global config**.

#### 6. **Remove Include/Exclude**:
- `2gpt remove-include "file.py"` or `2gpt remove-exclude "file.py"`:
    - Removes `file.py` from the inclusion/exclusion list temporarily (no permanent config changes).

- `2gpt remove-include "file.py" --permanent` or `2gpt remove-exclude "file.py" --permanent`:
    - Permanently removes `file.py` from the **local config**.

- `2gpt remove-include "file.py" --permanent --global-config` or `2gpt remove-exclude "file.py" --permanent --global-config`:
    - Permanently removes `file.py` from the **global config**, ignoring the local config.

---

### Example Workflows:

1. **Run with Default Configuration**:
    ```bash
    2gpt
    ```

2. **Temporarily Include a File**:
    ```bash
    2gpt include "file.py"
    ```

3. **Permanently Include a File Locally**:
    ```bash
    2gpt include "file.py" --permanent
    ```

4. **Permanently Include a File Globally**:
    ```bash
    2gpt include "file.py" --permanent --global-config
    ```

5. **List Includes in Local Config**:
    ```bash
    2gpt list-includes
    ```

6. **List Includes in Global Config**:
    ```bash
    2gpt list-includes --global-config
    ```

7. **Remove a File from Local Exclude List Permanently**:
    ```bash
    2gpt remove-exclude "file.py" --permanent
    ```

8. **Remove a File from Global Include List Permanently**:
    ```bash
    2gpt remove-include "file.py" --permanent --global-config
    ```

---

This description covers the complete behavior for `include`, `exclude`, `list-includes`, `list-excludes`, and `remove` operations with local and global configurations, using the `--permanent` and `--global-config` flags where appropriate.

"""
