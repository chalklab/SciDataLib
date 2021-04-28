"""Input/output module for reading + writing different file formats"""
from importlib import import_module
import types
import typing


_MODULE_BASE = 'scidatalib.io.'


class UnknownFileTypeError(Exception):
    pass


ioformats = {
    'jcamp': 'jcamp',
}


def _get_ioformat(name: str) -> types.ModuleType:
    if name not in ioformats:
        raise UnknownFileTypeError(name)
    module = _MODULE_BASE + ioformats[name]
    fmt = import_module(module)
    return fmt


def _readfunc(module: types.ModuleType, name: str) -> typing.Callable:
    return getattr(module, 'read_' + name)


def _writefunc(module: types.ModuleType, name: str) -> typing.Callable:
    return getattr(module, 'write_' + name)


def read(filename: str, ioformat: str = None, **kwargs) -> dict:
    """
    Read SciData dict from file format
    """
    module = _get_ioformat(ioformat)
    function = _readfunc(module, ioformats.get(ioformat))
    return function(filename, **kwargs)


def write(
    filename: str, scidata_dict: dict, ioformat: str = None, **kwargs
) -> typing.Callable:
    """
    Write SciData dict to file format
    """
    module = _get_ioformat(ioformat)
    function = _writefunc(module, ioformats.get(ioformat))
    return function(filename, scidata_dict, **kwargs)
