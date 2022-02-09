import pytest
from unittest.mock import patch, mock_open, call
from wordle import get_wordle_from_secret, \
                    is_guess_a_valid_word, \
                    get_list_of_words, \
                    save_list_of_words, \
                    prepare_word_file


def test_get_wordle_from_secret__guess_too_short():

    secret = 'XXXXX'
    word = ''

    with pytest.raises(Exception):
        get_wordle_from_secret(word, secret)


def test_get_wordle_from_secret__secret_too_short():

    secret = ''
    word = 'XXXXX'

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


def test_is_guess_a_valid_word__valid():

    # Given
    guess = 'valid'

    # When
    actual = is_guess_a_valid_word(guess)

    # Then
    assert actual is True


def test_is_guess_a_valid_word__invalid():

    # Given
    guess = 'invalid'

    # When
    actual = is_guess_a_valid_word(guess)

    # Then
    assert actual is False


def test_is_guess_a_valid_word__tough():

    # Given
    guess = 'tough'

    # When
    actual = is_guess_a_valid_word(guess)

    # Then
    assert actual is True


def test_get_list_of_words():
    with patch("builtins.open", mock_open(read_data="word1\nword2\n")) as mock_file:

        # Given
        expected = ['word1', 'word2']

        # When
        actual = get_list_of_words("words.txt")

        # Then
        assert expected == actual
        mock_file.assert_called_with("words.txt", "r")


def test_save_list_of_words__1_word():
    open_mock = mock_open()
    with patch("builtins.open", open_mock, create=True):

        # Given
        expected_array = ['word1']

        # When
        save_list_of_words(expected_array, "save_words.txt")

        open_mock.assert_called_with("save_words.txt", "w")
        open_mock.return_value.write.assert_called_once_with("word1\n")


def test_save_list_of_words__2_words():
    open_mock = mock_open()
    with patch("builtins.open", open_mock, create=True):

        # Given
        expected_array = ['word1', 'word2']

        # When
        save_list_of_words(expected_array, "save_words.txt")

        open_mock.assert_called_with("save_words.txt", "w")
        open_mock.return_value.write.assert_has_calls([call('word1\n'),
                                                       call('word2\n')])


@patch('wordle.get_list_of_words', return_value=['word1', 'word2', 'word123'])
@patch('wordle.save_list_of_words')
def test_prepare_word_file(mock_save, mock_get):
    prepare_word_file("filepath1", "filepath2")

    assert mock_get.call_args == call("filepath1")
    assert mock_save.call_args == call(['word1', 'word2'], "filepath2")
