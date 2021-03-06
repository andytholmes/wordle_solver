import pytest
from unittest.mock import patch, mock_open, call
from wordle import Word, Guess, \
                    get_wordle_from_secret, \
                    is_guess_a_valid_word, \
                    get_list_of_words, \
                    save_list_of_words, \
                    prepare_word_file, \
                    get_word_attributes, \
                    make_a_guess, \
                    guess_from_secret


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


@pytest.mark.parametrize('secret, guess, expected', [
    ("XXXXX", "YYYYY", "_____"),
    ("YYYYY", "YYYYY", "GGGGG"),
    ("YXXXX", "YYYYY", "G____"),
    ("YYXXX", "YYYYY", "GG___"),
    ("XXXZX", "YYYYZ", "____Y"),
    ("MUMYY", "MUDYU", "GG_G_"),
    ("HOTEL", "SOAPY", "_G___")
])
def test_get_wordle_from_secret(secret, guess, expected):
    assert expected == get_wordle_from_secret(guess, secret)


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
    with patch("builtins.open",
               mock_open(read_data="word1\nword2\n")) as mock_file:

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


@patch('wordle.get_list_of_words', return_value=['54321', '12345', '123456'])
@patch('wordle.save_list_of_words')
def test_prepare_word_file(mock_save, mock_get):
    prepare_word_file("filepath1", "filepath2")

    assert mock_get.call_args == call("filepath1")
    assert mock_save.call_args == call(['54321', '12345'], "filepath2")


def test_get_word_attributes__one_element():
    words = ['storm']
    expected = get_word_attributes(words)
    assert len(expected) == 1
    assert expected[0].word == 'storm'
    assert expected[0].distinct_letters == 5
    assert expected[0].distinct_vowels == 1


@patch('wordfreq.word_frequency')
def test_get_word_attributes__elements_ordered(mock_freq):
    mock_freq.side_effect = [1, 2]
    words = ['storm', 'soapy']
    expected = get_word_attributes(words)
    assert expected[0].word == 'soapy'
    assert expected[1].word == 'storm'


@pytest.mark.parametrize('word, wordle, expected', [
    ("taste", "G____", "t____"),
    ("taste", "GG___", "ta___"),
    ("taste", "GGG__", "tas__"),
    ("taste", "GGGG_", "tast_"),
    ("taste", "GGGGG", "taste"),
    ("taste", "Y____", "_____"),
    ("taste", "YG___", "_a___")])
def test_add_wordle__finalword(word, wordle, expected):
    guess = Guess()
    guess.add_wordle(wordle, word)
    assert guess.final_word == expected
    assert word in guess.used_words


def test_add_wordle__included():
    guess = Guess()
    wordle = 'Y____'
    word = 'taste'
    guess.add_wordle(wordle, word)
    assert 't' in guess.letters_in_word


def test_make_a_guess():
    guess = Guess()
    word = Word()
    word.word = 'soapy'
    word_array = [word]
    next_word = make_a_guess(word_array, guess)
    assert next_word == 'soapy'


@pytest.mark.parametrize('word, final_word, expected', [
    ("abcde", "a____", True),
    ("abcde", "_b___", True),
    ("abcde", "x____", False)
])
def test_is_word_good_guess__final_word(word, final_word, expected):
    guess = Guess()
    guess.final_word = final_word
    assert guess.is_word_good_guess(word) == expected


@pytest.mark.parametrize('final_word, word, excluded_letters, expected', [
    ("_____", "abcde", ['a'], False),
    ("_____", "abcde", ['f', 'a'], False),
    ("_____", "abcde", ['x'], True),
    ("_____", "abcde", [], True),
    # a letter may match an ordinal and then get exluded
    ("a____", "abcde", ['a'], True)
])
def test_is_word_good_guess__exluded_letters(final_word, word,
                                             excluded_letters,
                                             expected):
    guess = Guess()
    guess.final_word = final_word
    guess.excluded_letters = excluded_letters
    assert guess.is_word_good_guess(word) == expected


@pytest.mark.parametrize('final_word, word, excl_ord, expected', [
    ('_____', "abcde", [['a']], False),
    ('_____', "abcde", [['x'], ['b']], False),
    ('_____', "abcde", [[]], True),
    ('_____', "abcde", [['x']], True)
])
def test_is_word_good_guess__exluded_letters_ordinal(final_word, word,
                                                     excl_ord, expected):
    guess = Guess()
    guess.final_word = final_word
    guess.excluded_letters_ordinal = excl_ord
    assert guess.is_word_good_guess(word) == expected


@patch('wordle.make_a_guess')
@patch('wordle.save_list_of_words')
@patch('wordle.get_wordle_from_secret')
def test_guess_from_secret(mock_make_guess,
                           mock_save_list_of_words,
                           mock_get_wordle_from_secret):
    secret = 'abcdef'
    guess = Guess()
    guess.final_word = 'abcdef'
    expected = guess_from_secret(secret, guess)
    assert expected is True


def test_overall():
    word_str_array = get_list_of_words("words.txt")
    word_array = get_word_attributes(word_str_array)
    guess = Guess()
    guess.add_wordle('___GY', 'audio')
    guess.add_wordle('_G_G_', 'motif')
    guess.add_wordle('_G_G_', 'cosie')
    guess.add_wordle('_G_G_', 'polio')
    word = make_a_guess(word_array, guess)
    assert word == 'robin'
