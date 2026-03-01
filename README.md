# Visio Import for Inkscape

Import Microsoft Visio files (`.vsdx` and `.vsd`) into Inkscape.

Uses [libvisio-ng](https://pypi.org/project/libvisio-ng/), a pure-Python library for parsing Visio files with support for themes, gradients, shadows, connectors, master shapes, and binary .vsd format.

## Installation

### 1. Install the Python dependency

```bash
pip install libvisio-ng
```

> **Note:** Use the same Python that Inkscape uses. On Linux this is usually the system Python. On macOS/Windows you may need to check Inkscape's Python path.

### 2. Copy extension files

Copy `visio_import.py`, `visio_import.inx`, and `visio_import_vsd.inx` to your Inkscape extensions directory:

| Platform | Extensions Directory |
|----------|---------------------|
| Linux    | `~/.config/inkscape/extensions/` |
| macOS    | `~/Library/Application Support/org.inkscape.Inkscape/config/inkscape/extensions/` |
| Windows  | `%APPDATA%\inkscape\extensions\` |

Or use the included install script (Linux):

```bash
chmod +x install.sh
./install.sh
```

### 3. Restart Inkscape

### 4. Import a Visio file

**File → Import** (or **File → Open**), then select a `.vsdx` or `.vsd` file.

You can choose which page to import (0-based page number).

## Features

- Import `.vsdx` (Visio 2013+) and `.vsd` (Visio 97-2003) files
- Converts shapes, text, connectors, gradients, and themes to SVG
- Page selection for multi-page documents
- Pure Python — no native dependencies required

## Requirements

- Inkscape 1.0 or later
- Python 3.8+
- libvisio-ng (`pip install libvisio-ng`)

## License

GPL-2.0-or-later — same as Inkscape.

## Links

- [libvisio-ng on PyPI](https://pypi.org/project/libvisio-ng/)
- [Inkscape Extensions](https://inkscape.org/gallery/)
- [GitLab MR #718](https://gitlab.com/inkscape/extensions/-/merge_requests/718) — original merge request
