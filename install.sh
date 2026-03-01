#!/bin/bash
# Install Visio Import extension for Inkscape (Linux)
set -e

EXT_DIR="${HOME}/.config/inkscape/extensions"
mkdir -p "$EXT_DIR"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cp "$SCRIPT_DIR/visio_import.py" "$EXT_DIR/"
cp "$SCRIPT_DIR/visio_import.inx" "$EXT_DIR/"
cp "$SCRIPT_DIR/visio_import_vsd.inx" "$EXT_DIR/"

echo "Installed to $EXT_DIR"
echo "Make sure libvisio-ng is installed: pip install libvisio-ng"
echo "Restart Inkscape to use the extension."
