import pytest
from lexer import lexer


def test_module_import():
    assert lexer.bool() == ""
