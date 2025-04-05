# 4gpt

`4gpt` ist ein CLI-Tool zur automatisierten Sammlung und Analyse von Dateien innerhalb eines Projekts.  
Die inkludierten und exkludierten Dateien lassen sich dynamisch oder permanent über `.gptignore` und/oder eine zentrale `config.json` steuern.

## 🔧 Features

- 📁 Generierung einer Dateistrukturübersicht als Baum + JSON
- 🔍 Einschluss/ Ausschluss nach Muster (z. B. `*.py`, `*.png`)
- 🧠 Lokale und globale Konfigurationsverwaltung (`--global-config`)
- ✅ Temporäre oder permanente Änderungen mit `--permanent`

## ⚡ Quick Install (Recommended)

Install directly from GitHub:

```bash
pip install "git+https://github.com/krausality/4gpt.git"
```

To install a specific version or for production builds, pin the commit:

```bash
pip install "git+https://github.com/krausality/4gpt.git@<commit-hash>"
```

Note: This method requires an internet connection and Git to be available in your environment.

## 🖥️ Installation


```bash
git clone https://github.com/krausality/4gpt.git
cd 4gpt
pip install -r requirements.txt
pip install .
```

Alternativ als Wheel:

```bash
python -m build --wheel
pip install dist/4gpt-*.whl
```

## 🚀 Usage

```bash
4gpt                          # Führt Analyse mit der aktuellen Konfiguration aus
4gpt include "*.ts"          # Temporär .ts-Dateien einbeziehen
4gpt exclude "*.png" --permanent   # Permanent PNG-Dateien ausschließen
4gpt list-includes           # Zeigt aktuelle Include-Muster
4gpt list-excludes --global-config  # Zeigt globale Excludes
```

## ⚙️ Konfigurationslogik

| Modus                                | Konfigurationsquelle        |
|-------------------------------------|-----------------------------|
| `4gpt`                               | Lokale `.gptignore` oder globale `config.json` |
| `--global-config`                    | Ignoriert lokale Konfig, nutzt `config.json`   |
| `--permanent` ohne `--global-config`| Lokale `.gptignore` wird erstellt/angepasst    |
| `--permanent --global-config`       | Globale Konfig wird dauerhaft angepasst        |

## 📂 Beispiel-Ausgabe

```txt
File Structure:
project
├── .gptignore
├── main.py
├── utils/
│   └── helper.py
```

Danach folgen alle Inhalte (nach Include/Exclude gefiltert) in `allfiles.txt`.

## 📝 Lizenz

Dieses Projekt steht unter der GNU GPL 3 Lizenz. Siehe [LICENSE](LICENSE).

