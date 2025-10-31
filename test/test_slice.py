# Copyright David Abrahams 2004. Distributed under the Boost
# Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import pytest
import sys
from slice_ext import *


def test_accept_slice_valid():
    """Test that accept_slice accepts slice objects."""
    result = accept_slice(slice(1, None, (1, 2)))
    assert result == 1


def test_accept_slice_invalid():
    """Test that accept_slice rejects non-slice objects."""
    try:
        accept_slice(list((1, 2)))
        assert False, "Expected an exception"
    except:
        # Expected exception
        pass


def test_string_rich_slice():
    """Test extended slicing for strings (Python 2.3+/Python 3+)."""
    if sys.version_info[0] == 2 and sys.version_info[1] >= 3:
        result = check_string_rich_slice()
    elif sys.version_info[0] > 2:
        result = check_string_rich_slice()
    else:
        result = 1

    assert result == 1


def test_slice_get_indices_none():
    """Test slice.indices with slice(None)."""
    result = check_slice_get_indices(slice(None))
    assert result == 0


def test_slice_get_indices_2_neg2():
    """Test slice.indices with slice(2, -2)."""
    result = check_slice_get_indices(slice(2, -2))
    assert result == 0


def test_slice_get_indices_step():
    """Test slice.indices with slice(2, None, 2)."""
    result = check_slice_get_indices(slice(2, None, 2))
    assert result == 5


def test_slice_get_indices_negative_step():
    """Test slice.indices with negative step."""
    result = check_slice_get_indices(slice(2, None, -1))
    assert result == -12


def test_slice_get_indices_large_start():
    """Test slice.indices with large start value."""
    result = check_slice_get_indices(slice(20, None))
    assert result == 0


def test_slice_get_indices_negative_range():
    """Test slice.indices with negative range."""
    result = check_slice_get_indices(slice(-2, -5, -2))
    assert result == 6


def test_docstring():
    """Test that function has correct docstring."""
    doc_first_line = check_slice_get_indices.__doc__.strip().split('\n')[0]
    assert doc_first_line == 'check_slice_get_indices( (slice)arg1) -> int :'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
