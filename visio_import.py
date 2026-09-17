#!/usr/bin/env python3
# coding=utf-8
#
# Copyright (C) 2026 Daniel Nylander <daniel@danielnylander.se>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
"""
Import Microsoft Visio files (.vsdx, .vsd) into Inkscape using libvisio-ng.

libvisio-ng is a pure-Python library for parsing Visio files with support for
themes, gradients, shadows, connectors, master shapes, and binary .vsd format.

See: https://pypi.org/project/libvisio-ng/
"""

import os
import sys
import tempfile

from lxml import etree

import inkex

try:
    from libvisio_ng import convert
except ImportError:
    inkex.errormsg(
        "The libvisio-ng Python package is required for Visio import.\n"
        "Install it with: pip install libvisio-ng"
    )
    sys.exit(1)


class VisioImport(inkex.InputExtension):
    """Import Microsoft Visio files (.vsdx, .vsd) as SVG."""

    multi_inx = True

    def add_arguments(self, pars):
        pars.add_argument(
            "--page",
            type=int,
            default=0,
            help="Page number to import (0-based)",
        )

    def load(self, stream):
        """Load a Visio file and convert to SVG."""
        # Keep both the input copy and converted pages within one owned directory.
        with tempfile.TemporaryDirectory(prefix="inkscape_visio_") as output_dir:
            name = getattr(stream, "name", None)
            if isinstance(name, (str, bytes, os.PathLike)) and os.path.isfile(name):
                file_path = name
            else:
                data = stream.read()
                # Anonymous binary streams must retain the .vsd parser dispatch.
                suffix = ".vsd" if data.startswith(bytes.fromhex("D0CF11E0A1B11AE1")) else ".vsdx"
                file_path = os.path.join(output_dir, "input" + suffix)
                with open(file_path, "wb") as tmp:
                    tmp.write(data)

            try:
                svg_files = convert(file_path, output_dir=output_dir)
            except (RuntimeError, OSError) as error:
                raise inkex.AbortExtension(str(error)) from error

            if not svg_files:
                raise inkex.AbortExtension("No pages found in the Visio file.")
            page_idx = self.options.page
            if not 0 <= page_idx < len(svg_files):
                raise inkex.AbortExtension(
                    f"Page {page_idx} is out of range; choose 0–{len(svg_files) - 1}."
                )
            # Parse fully before the temporary directory is removed.
            with open(svg_files[page_idx], "rb") as svg_file:
                return etree.parse(svg_file).getroot()



if __name__ == "__main__":
    VisioImport().run()
