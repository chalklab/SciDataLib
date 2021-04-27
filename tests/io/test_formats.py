"""Tests for io.formats"""
import pytest
from scidatalib import io


def test_get_ioformat_raise_exception():
    with pytest.raises(io.formats.UnknownFileTypeError):
        io.formats._get_ioformat('cat')
