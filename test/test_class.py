# Distributed under the Boost
# Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import pytest


def test_basic_functionality():
    """Ensure sanity: basic X construction and function call."""
    import class_ext as _ext

    x = _ext.X(42)
    assert _ext.x_function(x) == 42


def test_metaclass_extraction():
    """Demonstrate extraction in the presence of metaclass changes."""
    import class_ext as _ext

    class MetaX(_ext.X.__class__):
        def __new__(cls, *args):
            return super(MetaX, cls).__new__(cls, *args)

    class XPlusMetatype(_ext.X):
        __metaclass__ = MetaX

    x = XPlusMetatype(42)
    assert _ext.x_function(x) == 42


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
