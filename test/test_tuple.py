# Copyright David Abrahams 2004. Distributed under the Boost
# Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import pytest
import tuple_ext as _ext


def test_convert_to_tuple():
    """Test converting string to tuple of characters."""
    result = _ext.convert_to_tuple("this is a test string")
    expected = ('t', 'h', 'i', 's', ' ', 'i', 's', ' ', 'a', ' ', 't', 'e', 's', 't', ' ', 's', 't', 'r', 'i', 'n', 'g')
    assert result == expected


def test_tuple_operators(capsys):
    """Test tuple concatenation operators."""
    t1 = _ext.convert_to_tuple("this is")
    t2 = (1, 2, 3, 4)

    output_lines = []
    def printer(*args):
        for x in args: print(x,)
        print('')

    _ext.test_operators(t1, t2, printer)
    captured = capsys.readouterr()
    # The result should be the two tuples concatenated
    assert captured.out.strip() == "('t', 'h', 'i', 's', ' ', 'i', 's', 1, 2, 3, 4)"


def test_make_tuple_empty():
    """Test creating empty tuple."""
    result = _ext.make_tuple()
    assert result == ()


def test_make_tuple_one_arg():
    """Test creating tuple with one argument."""
    result = _ext.make_tuple(42)
    assert result == (42,)


def test_make_tuple_two_args():
    """Test creating tuple with two arguments."""
    result = _ext.make_tuple('hello', 42)
    assert result == ('hello', 42)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
