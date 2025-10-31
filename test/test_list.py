# Copyright David Abrahams 2004. Distributed under the Boost
# Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import pytest
from list_ext import *


def test_new_list():
    """Test creating a new empty list."""
    result = new_list()
    assert result == []


def test_listify_tuple():
    """Test converting tuple to list."""
    result = listify((1, 2, 3))
    assert result == [1, 2, 3]


def test_listify_string():
    """Test converting string to list of characters."""
    letters = listify_string('hello')
    assert letters == ['h', 'e', 'l', 'l', 'o']


def test_x_repr():
    """Test X object representation."""
    x = X(22)
    assert repr(x) == 'X(22)'


def test_apply_object_list_identity():
    """Test applying identity function to list (should return same object)."""
    letters = listify_string('hello')

    def identity(x):
        return x

    result = apply_object_list(identity, letters)
    assert result is letters


def test_apply_object_list_type_error():
    """Test that non-list argument raises TypeError."""
    def identity(x):
        return x

    with pytest.raises(TypeError):
        apply_object_list(identity, 5)


def test_apply_list_list():
    """Test applying function that returns list."""
    letters = listify_string('hello')

    def identity(x):
        return x

    result = apply_list_list(identity, letters)
    assert result is letters


def test_apply_list_list_return_type_error():
    """Test that function returning non-list raises TypeError."""
    letters = listify_string('hello')

    with pytest.raises(TypeError):
        apply_list_list(len, letters)


def test_append_object():
    """Test appending object to list."""
    letters = listify_string('hello')
    append_object(letters, '.')
    assert letters == ['h', 'e', 'l', 'l', 'o', '.']


def test_append_list_tuple_fails():
    """Test that tuples do not automatically convert to lists."""
    letters = listify_string('hello')

    with pytest.raises(TypeError):
        append_list(letters, (1, 2))


def test_append_list():
    """Test appending list to list."""
    letters = listify_string('hello')
    append_object(letters, '.')
    append_list(letters, [1, 2])
    assert letters == ['h', 'e', 'l', 'l', 'o', '.', [1, 2]]


def test_subclass_method_calls():
    """Check that subclass functions are properly called."""
    class mylist(list):
        def append(self, o):
            list.append(self, o)
            if not hasattr(self, 'nappends'):
                self.nappends = 1
            else:
                self.nappends += 1

    l2 = mylist()
    append_object(l2, 'hello')
    append_object(l2, 'world')
    assert l2 == ['hello', 'world']
    assert l2.nappends == 2


def test_exercise_complex():
    """
    Complex test of various list operations.
    Note: This test exercises many operations and validates output.
    """
    letters = listify_string('hello')
    append_object(letters, '.')
    append_list(letters, [1, 2])

    y = X(42)

    # Collect output from exercise function
    output_lines = []

    def printer(*args):
        line = ' '.join(str(x) for x in args)
        output_lines.append(line)

    exercise(letters, y, printer)

    # Validate that expected operations occurred
    assert len(output_lines) > 0
    assert 'after append:' in output_lines[0]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
