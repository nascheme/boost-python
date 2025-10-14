// Copyright 2025 Boost.Python Contributors
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef BOOST_PYTHON_DETAIL_PYMUTEX_HPP
#define BOOST_PYTHON_DETAIL_PYMUTEX_HPP

#include <boost/python/detail/prefix.hpp>

namespace boost { namespace python { namespace detail {

#ifdef Py_GIL_DISABLED

// Wrapper around PyMutex to provide BasicLockable semantics for free-threaded Python
class pymutex {
    PyMutex m_mutex;

public:
    pymutex() : m_mutex({}) {}

    // Non-copyable, non-movable
    pymutex(const pymutex&) = delete;
    pymutex& operator=(const pymutex&) = delete;

    void lock() { PyMutex_Lock(&m_mutex); }
    void unlock() { PyMutex_Unlock(&m_mutex); }
};


// RAII lock guard for pymutex
class pymutex_guard {
    pymutex& m_mutex;

public:
    explicit pymutex_guard(pymutex& mutex) : m_mutex(mutex) {
        m_mutex.lock();
    }

    ~pymutex_guard() {
        m_mutex.unlock();
    }

    // Non-copyable, non-movable
    pymutex_guard(const pymutex_guard&) = delete;
    pymutex_guard& operator=(const pymutex_guard&) = delete;
};

#endif // Py_GIL_DISABLED

}}} // namespace boost::python::detail

#endif // BOOST_PYTHON_DETAIL_PYMUTEX_HPP
