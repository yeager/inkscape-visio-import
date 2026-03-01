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
    from libvisio_ng import convert, get_page_info
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
        # Write stream to a temp file since libvisio-ng requires a file path
        if hasattr(stream, "name") and os.path.exists(stream.name):
            file_path = stream.name
            tmp_path = None
        else:
            suffix = ".vsdx"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(stream.read())
                tmp_path = tmp.name
            file_path = tmp_path

        try:
            output_dir = tempfile.mkdtemp(prefix="inkscape_visio_")
            svg_files = convert(file_path, output_dir=output_dir)

            if not svg_files:
                inkex.errormsg("No pages found in the Visio file.")
                sys.exit(1)

            page_idx = min(self.options.page, len(svg_files) - 1)
            svg_path = svg_files[page_idx]

            with open(svg_path, "rb") as svg_file:
                return etree.parse(svg_file).getroot()
        finally:
            if tmp_path is not None:
                os.unlink(tmp_path)


if __name__ == "__main__":
    VisioImport().run()
