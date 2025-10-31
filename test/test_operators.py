# Copyright David Abrahams 2004. Distributed under the Boost
# Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import pytest

@pytest.fixture
def ext():
    import operators_ext as ext
    return ext

def test_nonzero_true(ext):
    """Check __nonzero__ support - truthy value."""

    assert ext.X(2)


def test_nonzero_false(ext):
    """Check __nonzero__ support - falsy value."""
    assert not ext.X(0)


def test_value(ext):
    """Test basic value retrieval."""
    x = ext.X(42)
    assert x.value() == 42


def test_subtract_x(ext):
    """Test subtracting X from X."""
    x = ext.X(42)
    y = x - ext.X(5)
    assert y.value() == 37


def test_subtract_int(ext):
    """Test subtracting int from X."""
    x = ext.X(42)
    y = x - 4
    assert y.value() == 38


def test_rsubtract(ext):
    """Test reverse subtraction (int - X)."""
    x = ext.X(42)
    y = 3 - x
    assert y.value() == -39


def test_negate(ext):
    """Test negation operator."""
    x = ext.X(42)
    y = 3 - x
    assert (-y).value() == 39


def test_add(ext):
    """Test addition."""
    x = ext.X(42)
    y = 3 - x
    assert (x + y).value() == 3


def test_abs(ext):
    """Test absolute value."""
    x = ext.X(42)
    y = 3 - x
    assert abs(y).value() == 39


def test_less_than_int_false(ext):
    """Test X < int when false."""
    x = ext.X(42)
    assert (x < 10) == 0


def test_less_than_int_true(ext):
    """Test X < int when true."""
    x = ext.X(42)
    assert (x < 43) == 1


def test_less_than_rint_true(ext):
    """Test int < X when true."""
    x = ext.X(42)
    assert (10 < x) == 1


def test_less_than_rint_false(ext):
    """Test int < X when false."""
    x = ext.X(42)
    assert (43 < x) == 0


def test_less_than_x_false(ext):
    """Test X < X when false."""
    x = ext.X(42)
    y = 3 - x
    assert (x < y) == 0


def test_less_than_x_true(ext):
    """Test X < X when true."""
    x = ext.X(42)
    y = 3 - x
    assert (y < x) == 1


def test_greater_than_int_true(ext):
    """Test X > int when true."""
    x = ext.X(42)
    assert (x > 10) == 1


def test_greater_than_int_false(ext):
    """Test X > int when false."""
    x = ext.X(42)
    assert (x > 43) == 0


def test_greater_than_rint_false(ext):
    """Test int > X when false."""
    x = ext.X(42)
    assert (10 > x) == 0


def test_greater_than_rint_true(ext):
    """Test int > X when true."""
    x = ext.X(42)
    assert (43 > x) == 1


def test_greater_than_x_true(ext):
    """Test X > X when true."""
    x = ext.X(42)
    y = 3 - x
    assert (x > y) == 1


def test_greater_than_x_false(ext):
    """Test X > X when false."""
    x = ext.X(42)
    y = 3 - x
    assert (y > x) == 0


def test_inplace_subtract(ext):
    """Test in-place subtraction."""
    x = ext.X(42)
    y = x - 5
    x -= y
    assert x.value() == 5


def test_str(ext):
    """Test string conversion."""
    x = ext.X(5)
    assert str(x) == '5'


def test_z_int(ext):
    """Test int conversion of Z."""
    z = ext.Z(10)
    assert int(z) == 10


def test_z_float(ext):
    """Test float conversion of Z."""
    z = ext.Z(10)
    assert float(z) == 10.0


def test_z_complex(ext):
    """Test complex conversion of Z."""
    z = ext.Z(10)
    assert complex(z) == (10+0j)


def test_pow_int_x(ext):
    """Test pow(int, X)."""
    x = ext.X(5)
    assert pow(2, x) == 32


def test_pow_x_int(ext):
    """Test pow(X, int)."""
    x = ext.X(5)
    assert pow(x, 2).value() == 25


def test_pow_x_x(ext):
    """Test pow(X, X)."""
    x = ext.X(5)
    assert pow(ext.X(2), x).value() == 32


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
