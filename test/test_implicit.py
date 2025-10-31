# Copyright David Abrahams 2004. Distributed under the Boost
# Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import pytest

@pytest.fixture
def ext():
    import implicit_ext as ext
    return ext

def test_x_value_with_x(ext):
    """Test x_value with X object."""
    result = ext.x_value(ext.X(42))
    assert result == 42


def test_x_value_with_int(ext):
    """Test x_value with int (implicit conversion)."""
    result = ext.x_value(42)
    assert result == 42


def test_make_x_with_x(ext):
    """Test make_x with X object."""
    x = ext.make_x(ext.X(42))
    assert x.value() == 42


def test_make_x_with_invalid_type(ext):
    """Test make_x with invalid type raises TypeError."""
    with pytest.raises(TypeError):
        ext.make_x('fool')


def test_x_value_docstring(ext):
    """Test x_value function docstring."""
    doc_line = ext.x_value.__doc__.splitlines()[1]
    assert doc_line == 'x_value( (X)arg1) -> int :'


def test_make_x_docstring(ext):
    """Test make_x function docstring."""
    doc_line = ext.make_x.__doc__.splitlines()[1]
    assert doc_line == 'make_x( (object)arg1) -> X :'


def test_x_value_method_docstring(ext):
    """Test X.value method docstring."""
    doc_line = ext.X.value.__doc__.splitlines()[1]
    assert doc_line == 'value( (X)arg1) -> int :'


def test_x_set_method_docstring(ext):
    """Test X.set method docstring."""
    doc_line = ext.X.set.__doc__.splitlines()[1]
    assert doc_line == 'set( (X)arg1, (object)arg2) -> None :'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
