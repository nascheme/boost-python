# Copyright David Abrahams 2004. Distributed under the Boost
# Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import pytest
from return_arg_ext import *


def test_label_returns_self():
    """Test that label method returns self."""
    l1 = Label()
    assert l1 is l1.label("bar")


def test_chained_methods_return_self():
    """Test that chained methods return self."""
    l1 = Label()
    assert l1 is l1.label("bar").sensitive(0)


def test_multiple_chains_return_same():
    """Test that multiple call chains return the same object."""
    l1 = Label()
    assert l1.label("foo").sensitive(0) is l1.sensitive(1).label("bar")


def test_return_arg_function():
    """Test return_arg function returns its argument."""
    assert return_arg is return_arg(return_arg)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
