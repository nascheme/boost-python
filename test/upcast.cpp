// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#include <boost/python/cast.hpp>
#include <boost/detail/lightweight_test.hpp>

struct X { long x; };
struct Y : X, PyObject {};

int main()
{
    PyTypeObject o;
    Y y;
    // Test that upcast preserves object identity by comparing pointers.
#if PY_VERSION_HEX >= 0x030a0000
    // In Python >= 3.10, Py_REFCNT cannot be used as an l-value.  Instead, we
    // directly compare the object pointers. For types directly derived from
    // PyObject (like PyTypeObject), the addresses should match. For Y, which
    // has multiple inheritance, upcast correctly adjusts to the PyObject base.
    BOOST_TEST(boost::python::upcast<PyObject>(&o) == reinterpret_cast<PyObject*>(&o));
    BOOST_TEST(boost::python::upcast<PyObject>(&y) == static_cast<PyObject*>(&y));
#else
    BOOST_TEST(&Py_REFCNT(boost::python::upcast<PyObject>(&o)) == &Py_REFCNT(&o));
    BOOST_TEST(&Py_REFCNT(boost::python::upcast<PyObject>(&y)) == &Py_REFCNT(&y));
#endif
    return boost::report_errors();
}
