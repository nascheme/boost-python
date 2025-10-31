# Copyright David Abrahams 2004. Distributed under the Boost
# Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import pytest
from extract_ext import *


def test_bool_check_none():
    """Anything has a truth value in Python - test None."""
    assert check_bool(None)
    assert extract_bool(None) == 0


def test_bool_check_int():
    """Test truth value of integer."""
    assert check_bool(2)
    assert extract_bool(2) == 1


def test_bool_check_empty_string():
    """Test truth value of empty string."""
    assert not check_bool('')


def test_list_check_fails_on_int():
    """Check that object manager types work properly - list vs int."""
    assert not check_list(2)

    with pytest.raises(TypeError) as exc_info:
        extract_list(2)

    # Check error message
    assert 'Expecting an object of type list' in str(exc_info.value)
    assert 'got an object of type int instead' in str(exc_info.value)


def test_list_check_tuple():
    """Can't extract a list from a tuple without explicit conversion."""
    assert not check_list((1, 2, 3))


def test_list_check_and_extract():
    """Test successful list check and extraction."""
    assert check_list([1, 2, 3])
    result = extract_list([1, 2, 3])
    assert result == [1, 2, 3]


def test_cstring_from_string():
    """Can get a char const* from a Python string."""
    assert check_cstring('hello')
    assert extract_cstring('hello') == 'hello'


def test_cstring_from_int_fails():
    """Can't get a char const* from a Python int."""
    assert not check_cstring(1)

    with pytest.raises(TypeError):
        extract_cstring(1)


def test_string_rvalue_extraction():
    """Extract an std::string (class) rvalue from a native Python type."""
    assert check_string('hello')
    assert extract_string('hello') == 'hello'


def test_string_cref_not_rvalue():
    """Constant references are not treated as rvalues for extract."""
    assert not check_string_cref('hello')


def test_x_lvalue_extraction():
    """Test extracting lvalues where appropriate."""
    x = X(42)
    assert check_X(x) == 1
    assert repr(extract_X(x)) == 'X(42)'


def test_x_ptr_extraction():
    """Test extracting X pointer."""
    x = X(42)
    assert check_X_ptr(x) == 1
    assert repr(extract_X_ptr(x)) == 'X(42)'


def test_x_ref_extraction():
    """Test extracting X reference."""
    x = X(42)
    assert repr(extract_X_ref(x)) == 'X(42)'


def test_double_extraction_rvalue():
    """Demonstrate that double-extraction of an rvalue works."""
    n = count_Xs()
    result = double_X(333)
    assert result == 666
    # All created copies should be destroyed
    assert count_Xs() - n == 0


def test_cleanup():
    """General check for cleanliness - all X objects destroyed."""
    # Create and destroy an X
    x = X(99)
    del x
    assert count_Xs() == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
