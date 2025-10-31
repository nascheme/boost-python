# Copyright David Abrahams 2004. Distributed under the Boost
# Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import pytest
import callbacks_ext as _ext


def test_apply_int_int():
    """Test applying int->int function."""
    def double(x):
        return x + x

    result = _ext.apply_int_int(double, 42)
    assert result == 84


def test_apply_void_int():
    """Test applying void function."""
    def double(x):
        return x + x

    result = _ext.apply_void_int(double, 42)
    assert result is None


def test_apply_to_string_literal_fails():
    """Test that applying to string literal raises ReferenceError."""
    def identity(x):
        return x

    with pytest.raises(ReferenceError):
        _ext.apply_to_string_literal(identity)


def test_apply_x_ref_handle_returns_temporary():
    """Test that returning temporary X raises ReferenceError."""
    with pytest.raises(ReferenceError):
        _ext.apply_X_ref_handle(lambda ignored: _ext.X_callbacks(42), None)


def test_apply_x_ref_handle():
    """Test applying function that returns X reference."""
    def identity(x):
        return x

    x = _ext.X_callbacks(42)
    x.y = _ext.X_callbacks(7)
    result = _ext.apply_X_ref_handle(lambda z: z.y, x).value()
    assert result == 7


def test_apply_x_x():
    """Test applying X->X function."""
    def identity(x):
        return x

    x = _ext.apply_X_X(identity, _ext.X_callbacks(42))
    assert x.value() == 42
    assert _ext.x_count() == 1

    del x
    assert _ext.x_count() == 0


def test_apply_void_x_ref():
    """Test applying function with X& parameter."""
    def increment(x):
        x.set(x.value() + 1)

    x = _ext.X_callbacks(42)
    _ext.apply_void_X_ref(increment, x)
    assert x.value() == 43


def test_apply_void_x_cref():
    """Test applying function with X const& parameter."""
    def increment(x):
        x.set(x.value() + 1)

    x = _ext.X_callbacks(43)
    _ext.apply_void_X_cref(increment, x)
    # Note: const-ness is not respected
    assert x.value() == 44


def test_apply_void_x_ptr():
    """Test applying function with X* parameter."""
    last_x = []

    def decrement(x):
        last_x.append(x)
        if x is not None:
            x.set(x.value() - 1)

    x = _ext.X_callbacks(44)
    _ext.apply_void_X_ptr(decrement, x)
    assert x.value() == 43
    assert last_x[0].value() == 43

    # Modifying last_x should affect x (same object)
    def increment(x):
        x.set(x.value() + 1)

    increment(last_x[0])
    assert x.value() == 44
    assert last_x[0].value() == 44


def test_apply_void_x_ptr_none():
    """Test applying function with None as X* parameter."""
    last_x = []

    def decrement(x):
        last_x.append(x)
        if x is not None:
            x.set(x.value() - 1)

    x = _ext.X_callbacks(44)
    _ext.apply_void_X_ptr(decrement, None)
    assert last_x[0] is None
    assert x.value() == 44


def test_apply_void_x_deep_ptr_none():
    """Test applying function with None as X** parameter."""
    last_x = []

    def decrement(x):
        last_x.append(x)
        if x is not None:
            x.set(x.value() - 1)

    x = _ext.X_callbacks(44)
    _ext.apply_void_X_deep_ptr(decrement, None)
    assert last_x[0] is None
    assert x.value() == 44


def test_apply_void_x_deep_ptr():
    """Test applying function with X** parameter."""
    last_x = []

    def decrement(x):
        last_x.append(x)
        if x is not None:
            x.set(x.value() - 1)

    x = _ext.X_callbacks(44)
    _ext.apply_void_X_deep_ptr(decrement, x)
    assert x.value() == 44  # Deep ptr doesn't modify original
    assert last_x[0].value() == 43


def test_apply_x_ref_handle_identity():
    """Test that X& handle returns same object."""
    def identity(x):
        return x

    def increment(x):
        x.set(x.value() + 1)

    x = _ext.X_callbacks(45)
    y = _ext.apply_X_ref_handle(identity, x)
    assert y.value() == x.value()

    increment(x)
    assert y.value() == x.value()


def test_apply_x_ptr_handle_cref():
    """Test X* handle with const ref."""
    def identity(x):
        return x

    def increment(x):
        x.set(x.value() + 1)

    x = _ext.X_callbacks(46)
    y = _ext.apply_X_ptr_handle_cref(identity, x)
    assert y.value() == x.value()

    increment(x)
    assert y.value() == x.value()


def test_apply_x_ptr_handle_cref_none():
    """Test X* handle with None."""
    def identity(x):
        return x

    y = _ext.apply_X_ptr_handle_cref(identity, None)
    assert y is None


def test_apply_x_ref_handle_new_x_fails():
    """Test that returning new X from ref handle fails."""
    def new_x(ignored):
        return _ext.X_callbacks(666)

    with pytest.raises(ReferenceError):
        _ext.apply_X_ref_handle(new_x, 1)


def test_apply_x_ptr_handle_cref_new_x_fails():
    """Test that returning new X from ptr handle fails."""
    def new_x(ignored):
        return _ext.X_callbacks(666)

    with pytest.raises(ReferenceError):
        _ext.apply_X_ptr_handle_cref(new_x, 1)


def test_apply_cstring_cstring_fails():
    """Test that returning string from cstring function fails."""
    def identity(x):
        return x

    with pytest.raises(ReferenceError):
        _ext.apply_cstring_cstring(identity, 'hello')


def test_apply_char_char():
    """Test char->char function."""
    def identity(x):
        return x

    result = _ext.apply_char_char(identity, 'x')
    assert result == 'x'


def test_apply_cstring_pyobject():
    """Test cstring->PyObject* function."""
    def identity(x):
        return x

    result = _ext.apply_cstring_pyobject(identity, 'hello')
    assert result == 'hello'


def test_apply_cstring_pyobject_none():
    """Test cstring->PyObject* function with None."""
    def identity(x):
        return x

    result = _ext.apply_cstring_pyobject(identity, None)
    assert result is None


def test_apply_to_own_type():
    """Test that function returns its own type."""
    def identity(x):
        return x

    result = _ext.apply_to_own_type(identity)
    assert result is type(identity)


def test_apply_object_object():
    """Test object->object function with identity."""
    def identity(x):
        return x

    result = _ext.apply_object_object(identity, identity)
    assert result is identity


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
