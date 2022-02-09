import pytest
from wordle import get_wordle_from_secret


def test_get_wordle_from_secret__guess_too_short():

    secret = ''
    word = ''

    with pytest.raises(Exception):
        get_wordle_from_secret(word, secret)


def test_get_wordle_from_secret__no_match():

    secret = 'XXXXX'
    guess = 'YYYYY'

    assert '_____' == get_wordle_from_secret(guess, secret)


def test_get_wordle_from_secret__all_match():

    secret = 'YYYYY'
    guess = 'YYYYY'

    assert 'GGGGG' == get_wordle_from_secret(guess, secret)

def test_get_wordle_from_secret__1_green():

    secret = 'YXXXX'
    guess = 'YYYYY'

    assert 'G____' == get_wordle_from_secret(guess, secret)

def test_get_wordle_from_secret__2_green():

    secret = 'YYXXX'
    guess = 'YYYYY'

    assert 'GG___' == get_wordle_from_secret(guess, secret)

def test_get_wordle_from_secret__1_yellow():

    secret = 'XXXZX'
    guess = 'YYYYZ'

    assert '____Y' == get_wordle_from_secret(guess, secret)

def test_get_wordle_from_secret__repeat_green_ignored():

    secret = 'MUMYY'
    guess = 'MUDYU'

    assert 'GG_G_' == get_wordle_from_secret(guess, secret)

def test_get_wordle_from_secret__hotel_soapy():

    secret = 'HOTEL'
    guess = 'SOAPY'

    assert '_G___' == get_wordle_from_secret(guess, secret)