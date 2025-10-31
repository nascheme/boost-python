# Copyright David Abrahams 2004. Distributed under the Boost
# Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import pytest
import sys
from long_ext import *

# Python 3 compatibility
if sys.version_info.major >= 3:
    long = int


def test_new_long():
    """Test creating a new long."""
    assert new_long() == 0


def test_longify_int():
    """Test converting int to long."""
    assert longify(42) == 42


def test_longify_string():
    """Test converting string to long."""
    assert longify_string('300') == 300


def test_is_long_with_long():
    """Test is_long check with actual long."""
    assert is_long(long(20)) == 'yes'


def test_is_long_with_string():
    """Test is_long check with string (should fail)."""
    assert is_long('20') == 0


def test_y_construction():
    """Test Y object construction with large long value."""
    x = Y(long(4294967295))
    # Just verify it constructs without error
    assert x is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
