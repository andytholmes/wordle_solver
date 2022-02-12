import wordle as w


word_string_array = w.get_list_of_words("words.txt")
word_array = w.get_word_attributes(word_string_array)
guess = w.Guess()
i = 0
secret = input("1. input secret:")
w.get_wordles_from_secret(secret)



while '_' in guess.final_word and i < 10:
    word = w.make_a_guess(word_array, guess)
    print(f'{i+1}: {word.word}')
    wordle = w.get_wordle_from_secret(word.word, secret)
    print(f'{i+1}: {wordle}')
    w.parse_wordle(guess, wordle, word.word)
    print(f'{i+1}: {guess.final_word}')
    i = i+1
print('Finished')
