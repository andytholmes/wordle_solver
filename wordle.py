

from os import remove
from site import getuserbase


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
