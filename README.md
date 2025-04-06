# 4gpt

`4gpt` is a CLI tool for automated collection and analysis of files within a project.  
Included and excluded files can be controlled dynamically or permanently via `.gptignore` and/or a central `config.json`.

## 🔧 Features

- 🗂️ Generates a file structure overview as a tree + JSON
- 📂 Inclusion/exclusion via patterns (e.g. `*.py`, `*.png`)
- 🧠 Local and global configuration management (`--global-config`)
- ✅ Temporary or permanent changes with `--permanent`

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

## 🖥️ Installation

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

## 🚀 Usage

```bash
4gpt                                # Runs analysis with current configuration
4gpt include "*.ts"                # Temporarily include .ts files
4gpt exclude "*.png" --permanent  # Permanently exclude PNG files
4gpt list-includes                 # Shows current include patterns
4gpt list-excludes --global-config  # Shows global excludes
```

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
project
├── .gptignore
├── main.py
├── utils/
│   └── helper.py
```

After that, all contents (filtered by include/exclude rules) are appended to `allfiles.txt`.

## 📄 License

This project is licensed under the GNU GPL 3 License. See [LICENSE](LICENSE).

