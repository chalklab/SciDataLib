"""Tests for io.formats"""
import pytest
from scidatalib import io


def test_get_ioformat_raise_exception():
    with pytest.raises(io.formats.UnknownFileTypeError):
        io.formats._get_ioformat('cat')


def test_get_ioformat_jcamp():
    fmt = io.formats._get_ioformat('jcamp')
    assert fmt.__name__ == 'scidatalib.io.jcamp'
