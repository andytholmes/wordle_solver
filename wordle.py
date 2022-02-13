from typing import List
import numpy as np
import wordfreq


class Word:
    def __init__(self):
        self.word = ''
        self.frequency = 0
        self.distinct_vowels = []
        self.distinct_letters = []

    def __repr__(self):
        return f"Word({self.word},{self.get_score()})"

    def setproperties(self, word: str, frequency: float, distinct_vowels: int,
                      distinct_letters: int):
        self.word = word
        self.frequency = frequency
        self.distinct_vowels = distinct_vowels
        self.distinct_letters = distinct_letters

    def get_score(self):
        score = 0
        if self.frequency != 0:
            score = self.frequency + \
                    self.distinct_vowels + \
                    self.distinct_letters
        return score


class Guess:
    def __init__(self):
        self.letters_in_word = []
        self.final_word = "_____"
        self.excluded_letters_ordinal = [[], [], [], [], []]
        self.excluded_letters = []
        self.used_words = []
        self.wordles = []

    def __repr__(self):
        return f"Guess({self.final_word})"

    def is_word_good_guess(self, word: str):
        for w in self.used_words:
            if w == word:
                return False

        for i, letter in enumerate(word):
            if self.final_word[i] == word[i]:
                continue
            if i < len(self.excluded_letters_ordinal) and \
               letter in self.excluded_letters_ordinal[i]:
                return False
            if letter.upper() == letter:
                return False
            if letter in self.excluded_letters:
                return False

        for letter in self.letters_in_word:
            if letter not in word:
                return False

        for i, letter in enumerate(self.final_word):
            if letter == '_':
                continue
            if letter != word[i]:
                return False
        return True

    def add_wordle(self, wordle: str, word: str):
        for i, letter in enumerate(wordle):
            if letter == 'G':
                self.final_word = self.final_word[:i] + \
                                word[i] + \
                                self.final_word[i+1:]
            if letter == 'Y':
                self.excluded_letters_ordinal[i].append(word[i])
                self.letters_in_word.append(word[i])
            if letter == '_':
                self.excluded_letters.append(word[i])
        self.used_words.append(word)
        self.wordles.append(wordle)


def get_wordle_from_secret(guess, secret):
    if len(secret) != 5:
        raise Exception('Secret word needs to be 5 letters')

    if len(guess) != 5:
        raise Exception('guess word needs to be 5 letters')

    wordle = ''
    g_check = ''
    s_check = ''
    for i, letter in enumerate(guess):
        if letter == secret[i]:
            wordle = wordle + 'G'
            g_check = g_check + 'X'
            s_check = s_check + 'X'

        else:
            wordle = wordle + '_'
            g_check = g_check + '_'
            s_check = s_check + '_'

    for g, g_letter in enumerate(guess):
        if g_check[g] != '_':
            continue
        for s, s_letter in enumerate(secret):
            if s_check[s] != '_':
                continue
            if s_letter == g_letter:
                wordle = wordle[:g] + 'Y' + wordle[g+1:]
                g_check = g_check[:g] + 'X' + g_check[g+1:]
                s_check = s_check[:s] + 'X' + s_check[s+1:]
                continue
    return wordle


def is_guess_a_valid_word(guess):

    word_list = ['valid', 'tough']
    ret_val = False

    if guess in word_list:
        ret_val = True

    return ret_val


def get_list_of_words(filepath):
    text_file = open(filepath, "r")
    file_str = text_file.read().strip()
    words = file_str.split('\n')
    text_file.close()
    return words


def save_list_of_words(words, filepath):
    a_file = open(filepath, "w")
    np.savetxt(a_file, words, fmt='%s')
    a_file.close()
    return


# prepare_word_file('/usr/share/dict/words','words.txt')
def prepare_word_file(from_filepath, to_filepath):
    word_array = get_list_of_words(from_filepath)

    good_words = []
    for word in word_array:
        if len(word) == 5:
            good_words.append(word)

    save_list_of_words(good_words, to_filepath)


def count_vowels_in_word(word: str) -> int:
    letters = set(word)
    cnt = 0
    for letter in letters:
        if letter in ('a', 'e', 'i', 'o', 'u'):
            cnt = cnt + 1
    return cnt


def get_word_attributes(words: List[str]) -> List[Word]:
    n = []
    for word in words:
        freq = wordfreq.word_frequency(word, 'en', wordlist='small')
        distinct_vowels = count_vowels_in_word(word)
        distinct_letters = len(set(word))
        w = Word()
        w.setproperties(word, freq, distinct_vowels, distinct_letters)
        n.append(w)
    n.sort(key=lambda x: x.get_score(), reverse=True)
    return n


def make_a_guess(word_array: Word, guess: Guess):
    for word in word_array:
        if guess.is_word_good_guess(word.word) is True:
            return word.word
    return ''


def guess_from_secret(secret: str, guess: Guess):
    word_string_array = get_list_of_words("words.txt")
    word_array = get_word_attributes(word_string_array)
    i = 0
    while '_' in guess.final_word and i < 10:
        word = make_a_guess(word_array, guess)
        wordle = get_wordle_from_secret(word.word, secret)
        parse_wordle(guess, wordle, word.word)
        i = i+1

    if '_' in guess.final_word:
        return False
    return True
