"""Input adapter tests; only the Inkscape UI base class is stubbed."""
import importlib.util
import io
from pathlib import Path
import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest


@pytest.fixture
def importer(monkeypatch):
    class AbortExtension(Exception):
        pass
    monkeypatch.setitem(sys.modules, 'inkex', SimpleNamespace(
        InputExtension=object, AbortExtension=AbortExtension, errormsg=Mock()))
    spec = importlib.util.spec_from_file_location('visio_import_under_test', Path(__file__).parents[1] / 'visio_import.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    instance = module.VisioImport()
    instance.options = SimpleNamespace(page=0)
    return module, instance


@pytest.mark.parametrize('page', [-1, 2])
def test_invalid_page_does_not_silently_import_another_page(importer, monkeypatch, page):
    module, instance = importer
    instance.options.page = page
    directories = []
    def convert(path, output_dir):
        directories.append(Path(output_dir))
        return ['unused.svg']
    monkeypatch.setattr(module, 'convert', convert)
    with pytest.raises(module.inkex.AbortExtension, match='out of range'):
        instance.load(io.BytesIO(b'PK'))
    assert not directories[0].exists()


@pytest.mark.parametrize('data,suffix', [(b'PK', '.vsdx'), (bytes.fromhex('D0CF11E0A1B11AE1'), '.vsd')])
def test_anonymous_stream_format_and_cleanup(importer, monkeypatch, data, suffix):
    module, instance = importer
    paths = []
    def convert(path, output_dir):
        paths.append(Path(path))
        assert Path(path).suffix == suffix
        assert Path(path).read_bytes() == data
        svg = Path(output_dir) / 'page.svg'
        svg.write_text('<svg xmlns="http://www.w3.org/2000/svg"><text>hello</text></svg>')
        return [str(svg)]
    monkeypatch.setattr(module, 'convert', convert)
    root = instance.load(io.BytesIO(data))
    assert root[0].text == 'hello'
    assert not paths[0].parent.exists()


def test_failed_conversion_cleans_input_copy(importer, monkeypatch):
    module, instance = importer
    paths = []
    def convert(path, output_dir):
        paths.append(Path(path))
        raise RuntimeError('broken file')
    monkeypatch.setattr(module, 'convert', convert)
    with pytest.raises(module.inkex.AbortExtension, match='broken file'):
        instance.load(io.BytesIO(b'PK'))
    assert not paths[0].parent.exists()
