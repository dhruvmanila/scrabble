import random
import json
from string import ascii_lowercase, punctuation, digits, whitespace
from typing import Tuple, Iterable
from itertools import chain

# Globals
INSTRUCTION_FILENAME = "instructions.txt"
WORDS_FILENAME = 'words.json'
INPUT_CHECK = punctuation + digits + whitespace
VOWELS = 'aeiou'
LINE_SEP = '-' * 70


def display_hangman(guess_rem: int, guessed: str, word: str = '') -> None:
    if '_' not in guessed:
        print(fr"""
                    +------+    +----------+
                    |         __| You won! |
                    |        /  +----------+
                    |       o
                    |      \|/
                    |       |
                    |      / \
                ==================
          You saved the hangman: {guessed}
                """)
        return 
    
    stages = [
                fr"""
                    +------+
                    |      |
                    |      o
                    |     |||
                    |      |
                    |     | |
                    |
                ==================
              You lost him: {word}
                """,
                fr"""
                    +------+
                    |      |
                    |      o
                    |     \|/
                    |      |
                    |     /
                    |
                ==================
                {guessed}
                """,
                fr"""
                    +------+
                    |      |
                    |      o
                    |     \|/
                    |      |
                    |
                    |
                ==================
                {guessed}
                """,
                fr"""
                    +------+
                    |      |
                    |      o
                    |     \|
                    |      |
                    |
                    |
                ==================
                {guessed}
                """,
                fr"""
                    +------+
                    |      |
                    |      o
                    |      |
                    |      |
                    |
                    |
                ==================
                {guessed}
                """,
                fr"""
                    +------+
                    |      |
                    |      o
                    |
                    |
                    |
                    |
                ==================
                {guessed}
                """,
                fr"""
                    +------+
                    |      |
                    |
                    |
                    |
                    |
                    |
                ==================
                {guessed}
                """
    ]
    print(stages[guess_rem])


def load_words() -> dict:
    """
    Returns a dictionary of valid words with keys being the length of the
    words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print(f"Loading words from the file...")
    with open(WORDS_FILENAME) as word_file:
        word_dict = json.load(word_file)
    print(f"Words loaded. Game on!\n{LINE_SEP}")
    return word_dict


def choose_word(word_dict: dict) -> str:
    """
    word_list (list): list of words (strings)
    Returns a word from wordlist at random
    """
    word_list = list(chain(*word_dict.values()))
    return random.choice(word_list)


def is_word_guessed(secret_word: str, letters_guessed: list) -> bool:
    """
    secret_word: string, the word the user is guessing;
        assumes all letters are lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in
        letters_guessed; False otherwise
    """
    found = None
    for letter in secret_word:
        found = True if letter in letters_guessed else False
        if not found:
            break
    return found


def get_guessed_word(secret_word: str, letters_guessed: list) -> str:
    """
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces
        that represents which letters in secret_word have been guessed so far.
    """
    word = ''
    for letter in secret_word:
        if letter in letters_guessed:
            word += letter
        else:
            word += '_ '
    return word


def get_available_letters(letters_guessed: list) -> str:
    """
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which
    letters have not yet been guessed.
    """
    letter_list = list(ascii_lowercase)
    for letter in letters_guessed:
        letter_list.remove(letter)
    letter_string = ''.join(letter_list)
    return letter_string


def warnings_check(letters_guessed: list, user_letter: str,
                   num_warnings: int, num_guess: int) -> Tuple[int, int]:
    """
    TODO: Make this more readable and efficient.
    secret_word: string, the secret word to guess
    letters_gussed: list (of letters), which letters have been guessed so far
    user_letter: string, user input letter
    num_warnings: integer, number of warnings remaining
    num_guess: integer, number of guesses remaining

    returns: prints appropriate message when user input is not an alphabet
    and also when the input is already guessed. Makes changes to the number of
    guesses and warnings and returns them as a tuple: (num_guess, num_warnings)
    """
    if len(user_letter) > 1 or user_letter in INPUT_CHECK:
        if num_warnings == 0:
            print("\nOops! That is not a valid letter. \nYou have no warnings "
                  "left so you lose one guess:")
            num_guess -= 1
        else:
            num_warnings -= 1
            print("\nOops! That is not a valid letter. \nYou "
                  "have", num_warnings, "warnings left:")

    if user_letter in letters_guessed:
        if num_warnings == 0:
            print("\nOops! You've already guessed that letter. \nYou "
                  "have no warnings left so you lose one guess:")
            num_guess -= 1
        else:
            num_warnings -= 1
            print("\nOops! You've already guessed that letter. \nYou "
                  "have", num_warnings, "warnings left:")

    return num_guess, num_warnings


def input_handling(request_msg: str, input_option: Iterable,
                   error_msg: str = "Invalid input.") -> str:
    """
    returns (str) user choice from the option and handles invalid input

    request_msg (str): input prompt (exclude ':')
    input_option (str/list): string/list containing the options
    error_msg (str)(Optional): Default "Invalid input."

    NOTE: For str input, one string options only
          otherwise input a list of options.
    """
    option_list = list(input_option)

    while True:
        user_input = input(f"{request_msg}: ").lower()
        try:
            assert user_input in option_list
            return user_input
        except AssertionError:
            print(f'"{user_input}": {error_msg}\n')


def match_with_gaps(my_word_string: str, other_word: str) -> bool:
    """
    my_word_string: string with _ characters but no spaces, 
    current guess of secret word
    other_word: string, regular English word
    Assuming my_word_string and other_word are of the same length

    returns: boolean, True if all the actual letters of my_word_string match
    the corresponding letters of other_word, or the letter is the special
    symbol _ ; False otherwise
    """
    for i in range(len(my_word_string)):
        if my_word_string[i] == '_' or my_word_string[i] == other_word[i]:
            continue
        else:
            return False
    return True


def show_possible_matches(my_word: str, word_length: str, word_dict: dict) -> None:
    """
    my_word: string with _ characters, current guess of secret word
    word_length: integer, length of the secretWord
    returns: None, prints out every word in wordlist that matches myWord

    Keep in mind that in hangman when a letter is guessed, all the positions
    at which that letter occurs in the secret word are revealed. Therefore,
    the hidden letter(_ ) cannot be one of the letters in the word that has
    already been revealed.

    """
    word_matches = ''
    my_word_string = ''.join([letter for letter in my_word if letter != ' '])
    letter_count = 0

    for word in word_dict[word_length]:
        if match_with_gaps(my_word_string, word):
            letter_count += len(word) + 1
            if letter_count > len(LINE_SEP):
                word_matches += '\n'
                letter_count = len(word) + 1
            word_matches += (word + ' ')

    print(f"\nPossible word matches for [ {my_word} ] are:\n{word_matches}")


def hangman_game(secret_word: str, word_dict: dict, hint_choice: str) -> int:
    """
    secret_word: string, the secret word to guess.
    Starts up an interactive game of Hangman.
    """
    letters_guessed = []
    num_guess = 6
    num_warnings = 3
    hint_count = 1
    total_score = 0

    print(r"""
   _                                             
  | |                                            
  | |__   __ _ _ __   __ _ _ __ ___   __ _ _ __  
  | '_ \ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
  | | | | (_| | | | | (_| | | | | | | (_| | | | |
  |_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
                     |___/  
                           """)

    print(f'{LINE_SEP}\nWelcome to the game, Hangman!')
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    print(f'You have {num_warnings} warnings left.')

    while num_guess > 0:
        guessed_word = get_guessed_word(secret_word, letters_guessed)
        display_hangman(num_guess, guessed_word)
        print(f'{LINE_SEP}\nYou have {num_guess} guesses left.')

        available_letters = get_available_letters(letters_guessed)
        print(f'Available letters: {available_letters}')

        user_letter = input('Please guess a letter: ').lower()

        if len(user_letter) > 1 or user_letter in INPUT_CHECK:
            if hint_choice == 'y' and user_letter == '*' and hint_count == 1:
                word_length = str(len(secret_word))
                show_possible_matches(guessed_word, word_length, word_dict)
                hint_count -= 1
                continue

            num_guess, num_warnings = warnings_check(
                letters_guessed, user_letter, num_warnings,
                num_guess)
            continue

        elif user_letter in letters_guessed:
            num_guess, num_warnings = warnings_check(
                letters_guessed, user_letter, num_warnings,
                num_guess)

        elif user_letter not in secret_word:
            print(f"\nOops! That letter is not in my word:")
            letters_guessed.append(user_letter)
            num_guess = num_guess - 2 if user_letter in VOWELS else \
                num_guess - 1

        elif user_letter in secret_word:
            letters_guessed.append(user_letter)
            guessed_word = get_guessed_word(secret_word, letters_guessed)
            print(f"\nGood guess:")

            if is_word_guessed(secret_word, letters_guessed):
                game_score = num_guess * len(set(secret_word))
                total_score += game_score
                display_hangman(num_guess, guessed_word)
                print(f"{LINE_SEP}\nCongratulations, you won!")
                print(f"Your score for this game is: {game_score}")
                break

    if num_guess <= 0:
        display_hangman(0, guessed_word, secret_word)
        print(f"{LINE_SEP}\nSorry, you ran out of guesses. The word was "
              f"{secret_word}.")

    return total_score


def play():
    with open(INSTRUCTION_FILENAME) as fhand:
        for line in fhand:
            line = line.rstrip()
            print(line)

    WORD_DICT = load_words()
    final_score = 0

    hint_choice = input_handling('Do you want to play with hints? [y/n]', 'yn')

    user_choice = 'y'
    while user_choice == 'y':
        secret_word = choose_word(WORD_DICT)
        total_score = hangman_game(secret_word, WORD_DICT, hint_choice)
        final_score += total_score
        user_choice = input_handling('Do you want to play again? [y/n]', 'yn')

    print(f'{LINE_SEP}\nYour total score for this session is: {final_score}')
    print(f'Thank you for playing.\n{LINE_SEP}')


if __name__ == "__main__":
    play()
