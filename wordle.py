import numpy as np


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

