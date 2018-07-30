import pytest
import main

def test_add_word():
    assert main.add_a_word('a', 'make').find('make') > -1

def test_get_words_by_group():
    assert main.get_group_of_words('a').find('make') > -1
