# Copyright David Abrahams 2004. Distributed under the Boost
# Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import pytest
import weakref
import object_ext as _ext


def test_ref_to_noncopyable():
    """Test returning reference to non-copyable object."""
    result = _ext.ref_to_noncopyable()
    assert type(result).__name__ == 'NotCopyable'


def test_call_object():
    """Test calling a Python callable from C++."""
    output = []
    def print1(x):
        output.append(x)

    _ext.call_object_3(print1)
    assert output == [3]


def test_message():
    """Test message function."""
    assert _ext.message() == 'hello, world!'


def test_number():
    """Test number function."""
    assert _ext.number() == 42


def test_truth_value_true():
    """Test truth value testing with truthy value."""
    assert _ext.test('hi') == 1


def test_truth_value_false():
    """Test truth value testing with falsy value."""
    assert _ext.test(None) == 0


def test_not_truth_value_true():
    """Test not operator with truthy value."""
    assert _ext.test_not('hi') == 0


def test_not_truth_value_false():
    """Test not operator with falsy value."""
    assert _ext.test_not(0) == 1


# Attribute tests
class TestAttributes:
    """Tests for object attribute access."""

    def test_getattr_missing(self):
        """Test getting non-existent attribute raises AttributeError."""
        class X:
            pass
        x = X()

        with pytest.raises(AttributeError):
            _ext.obj_getattr(x, 'foo')

    def test_objgetattr_missing(self):
        """Test obj_objgetattr with missing attribute."""
        class X:
            pass
        x = X()

        with pytest.raises(AttributeError):
            _ext.obj_objgetattr(x, 'objfoo')

    def test_setattr_and_getattr(self):
        """Test setting and getting attributes."""
        class X:
            pass
        x = X()

        _ext.obj_setattr(x, 'foo', 1)
        assert x.foo == 1
        assert _ext.obj_getattr(x, 'foo') == 1

    def test_objsetattr_and_objgetattr(self):
        """Test object-based setattr and getattr."""
        class X:
            pass
        x = X()

        _ext.obj_objsetattr(x, 'objfoo', 1)
        assert x.objfoo == 1
        assert _ext.obj_objgetattr(x, 'objfoo') == 1

    def test_objsetattr_invalid_name(self):
        """Test obj_objsetattr with invalid attribute name."""
        class X:
            pass
        x = X()

        with pytest.raises(TypeError):
            _ext.obj_objsetattr(x, 1)

    def test_objgetattr_invalid_name(self):
        """Test obj_objgetattr with invalid attribute name."""
        class X:
            pass
        x = X()
        x.objfoo = 1

        with pytest.raises(TypeError):
            _ext.obj_objgetattr(x, 1)

    def test_const_getattr(self):
        """Test const getattr."""
        class X:
            pass
        x = X()
        _ext.obj_setattr(x, 'foo', 1)

        assert _ext.obj_const_getattr(x, 'foo') == 1

    def test_const_objgetattr(self):
        """Test const obj getattr."""
        class X:
            pass
        x = X()
        _ext.obj_objsetattr(x, 'objfoo', 1)

        assert _ext.obj_const_objgetattr(x, 'objfoo') == 1

    def test_setattr42(self):
        """Test setattr with fixed value."""
        class X:
            pass
        x = X()

        _ext.obj_setattr42(x, 'foo')
        assert x.foo == 42

    def test_objsetattr42(self):
        """Test obj setattr with fixed value."""
        class X:
            pass
        x = X()

        _ext.obj_objsetattr42(x, 'objfoo')
        assert x.objfoo == 42

    def test_moveattr(self):
        """Test moving attribute to new name."""
        class X:
            pass
        x = X()
        _ext.obj_setattr42(x, 'foo')

        _ext.obj_moveattr(x, 'foo', 'bar')
        assert x.bar == 42

    def test_objmoveattr(self):
        """Test moving object attribute to new name."""
        class X:
            pass
        x = X()
        _ext.obj_objsetattr42(x, 'objfoo')

        _ext.obj_objmoveattr(x, 'objfoo', 'objbar')
        assert x.objbar == 42

    def test_attr_exists(self):
        """Test checking if attribute exists (truthy)."""
        class X:
            pass
        x = X()
        x.foo = 1

        assert _ext.test_attr(x, 'foo') == 1

    def test_objattr_exists(self):
        """Test checking if object attribute exists (truthy)."""
        class X:
            pass
        x = X()
        x.objfoo = 1

        assert _ext.test_objattr(x, 'objfoo') == 1

    def test_not_attr_exists(self):
        """Test negation of attribute existence (truthy)."""
        class X:
            pass
        x = X()
        x.foo = 1

        assert _ext.test_not_attr(x, 'foo') == 0

    def test_not_objattr_exists(self):
        """Test negation of object attribute existence (truthy)."""
        class X:
            pass
        x = X()
        x.objfoo = 1

        assert _ext.test_not_objattr(x, 'objfoo') == 0

    def test_attr_none(self):
        """Test attribute set to None (falsy)."""
        class X:
            pass
        x = X()
        x.foo = None

        assert _ext.test_attr(x, 'foo') == 0
        assert _ext.test_not_attr(x, 'foo') == 1

    def test_objattr_none(self):
        """Test object attribute set to None (falsy)."""
        class X:
            pass
        x = X()
        x.objfoo = None

        assert _ext.test_objattr(x, 'objfoo') == 0
        assert _ext.test_not_objattr(x, 'objfoo') == 1

    def test_delattr(self):
        """Test deleting attribute."""
        class X:
            pass
        x = X()
        x.foo = 1

        _ext.obj_delattr(x, 'foo')

        with pytest.raises(AttributeError):
            _ext.obj_delattr(x, 'foo')

    def test_objdelattr(self):
        """Test deleting object attribute."""
        class X:
            pass
        x = X()
        x.objfoo = 1

        _ext.obj_objdelattr(x, 'objfoo')

        with pytest.raises(AttributeError):
            _ext.obj_objdelattr(x, 'objfoo')


# Item tests
class TestItems:
    """Tests for object item access."""

    def test_setitem_and_getitem(self):
        """Test setting and getting items."""
        d = {}
        _ext.obj_setitem(d, 'foo', 1)

        assert d['foo'] == 1
        assert _ext.obj_getitem(d, 'foo') == 1

    def test_const_getitem(self):
        """Test const getitem."""
        d = {'foo': 1}
        assert _ext.obj_const_getitem(d, 'foo') == 1

    def test_setitem42(self):
        """Test setitem with fixed value."""
        d = {}
        _ext.obj_setitem42(d, 'foo')

        assert _ext.obj_getitem(d, 'foo') == 42
        assert d['foo'] == 42

    def test_moveitem(self):
        """Test moving item to new key."""
        d = {}
        _ext.obj_setitem42(d, 'foo')

        _ext.obj_moveitem(d, 'foo', 'bar')
        assert d['bar'] == 42

    def test_moveitem2(self):
        """Test moving item between dicts."""
        d = {}
        _ext.obj_setitem42(d, 'foo')
        _ext.obj_moveitem(d, 'foo', 'bar')

        _ext.obj_moveitem2(d, 'bar', d, 'baz')
        assert d['baz'] == 42

    def test_item_exists(self):
        """Test checking if item exists (missing)."""
        d = {'foo': 1}
        assert _ext.test_item(d, 'foo') == 1

    def test_not_item_exists(self):
        """Test negation of item existence (missing)."""
        d = {'foo': 1}
        assert _ext.test_not_item(d, 'foo') == 0

    def test_item_none(self):
        """Test item set to None (falsy)."""
        d = {'foo': None}
        assert _ext.test_item(d, 'foo') == 0
        assert _ext.test_not_item(d, 'foo') == 1


def test_string_slice():
    """Test string slicing."""
    assert _ext.check_string_slice()


def test_call_with_args_and_kwargs():
    """Test calling object with args and kwargs."""
    output = []
    def print_args(*args, **kwds):
        output.append((args, kwds))

    _ext.test_call(print_args, (0, 1, 2, 3), {'a': 'A'})

    assert len(output) == 1
    assert output[0] == ((0, 1, 2, 3), {'a': 'A'})


def test_binary_operators():
    """Test binary operators."""
    assert _ext.check_binary_operators()


def test_inplace_operators():
    """Test in-place operators."""
    class X:
        pass

    assert _ext.check_inplace(list(range(3)), X())


def test_reference_counting():
    """Test that object properly manages reference counts."""
    class Z:
        pass

    z = Z()
    deaths = []

    def death(r):
        deaths.append('death')

    r = weakref.ref(z, death)
    z.foo = 1

    assert _ext.obj_getattr(z, 'foo') == 1

    del z
    # Death callback should have been called
    assert deaths == ['death']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
