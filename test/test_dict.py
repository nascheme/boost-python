# Copyright David Abrahams 2004. Distributed under the Boost
# Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import pytest

@pytest.fixture
def ext():
    import dict_ext as ext
    return ext


def test_new_dict(ext):
    """Test creating a new empty dict."""
    result = ext.new_dict()
    assert result == {}


def test_data_dict(ext):
    """Test creating a dict with data."""
    result = ext.data_dict()
    assert result == {1: {'key2': 'value2'}, 'key1': 'value1'}


def test_dict_keys(ext):
    """Test extracting keys from dict."""
    tmp = ext.data_dict()
    keys = ext.dict_keys(tmp)
    assert keys == [1, 'key1']


def test_dict_values(ext):
    """Test extracting values from dict."""
    tmp = ext.data_dict()
    values = ext.dict_values(tmp)
    # Values can be in any order, so check both are present
    assert {'key2': 'value2'} in values
    assert 'value1' in values
    assert len(values) == 2


def test_dict_items(ext):
    """Test extracting items from dict."""
    tmp = ext.data_dict()
    items = ext.dict_items(tmp)
    # Items can be in any order
    assert (1, {'key2': 'value2'}) in items
    assert ('key1', 'value1') in items
    assert len(items) == 2


def test_dict_from_sequence(ext):
    """Test creating dict from sequence of tuples."""
    result = ext.dict_from_sequence([(1, 1), (2, 2), (3, 3)])
    assert result == {1: 1, 2: 2, 3: 3}


#@pytest.mark.usefixtures("ext", "capsys")
def test_templates(capsys, ext):
    """Test template operations on dict."""
    output_lines = []

    def printer(*args):
        for x in args: print(x)

    ext.test_templates(printer)
    captured = capsys.readouterr()
    output_lines = [line.strip() for line in captured.out.split('\n')]

    # Verify expected output
    assert output_lines[0] == '13'
    assert output_lines[1] == 'a test string'
    assert output_lines[2] == 'None'
    assert output_lines[3] == "{1.5: 13, 1: 'a test string'}"
    assert output_lines[4] == 'default'
    assert output_lines[5] == 'default'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
