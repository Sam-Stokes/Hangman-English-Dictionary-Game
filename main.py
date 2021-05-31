import functools
import random
import re

print("English Dictionary Word and Definition Hangman Game")

# Reads from text file to pull random word
with open("english_dict.txt", "r") as file:
    all_words = file.read()
    all_words = re.sub("\n", " ", all_words)  # Replace new line characters with a space

pattern = """
(?P<word>[A-Z*]{3,})
([\s\S]*?Defn:\ )
(?P<definition>.+?\.(?= ))
"""

word_from_file = []  # list containing all words
definition = []  # list containing definitions of words

# loop to append the lists for all words and definitions
for item in re.finditer(pattern, all_words, re.VERBOSE):
    word_from_file.append(item.group(1))
    definition.append(item.group(3))


def play_game():
    word = random.choice(word_from_file)  # choose a random word
    index_of_word = word_from_file.index(word)  # find the index of random word

    # Function that repeats the game or ends the game
    def menu():
        choice = input("\nEnter 'y' to play again, or any other character to quit: ")
        if choice.lower() == 'y':
            play_game()
        else:
            print("Thanks for playing")
            return False

    # Function to split the word pulled from file into list format
    def split(word_split):
        return [char for char in word_split]

    # Function to track the amount of calls made by another function
    def track_calls(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.has_been_called = True
            return func(*args, **kwargs)

        wrapper.has_been_called = False
        return wrapper

    # Game function
    def hangman_game(word):
        game = True
        num_of_guesses = 11
        hidden_word = split(word)
        word_to_guess = split(word)

        # Replace letters with blank spaces
        for index, item in enumerate(word_to_guess):
            word_to_guess.remove(item)
            word_to_guess.insert(index, '_')

        while game:

            while num_of_guesses > 0:
                # Function that fills in the blanks if letter is guessed correctly
                @track_calls
                def fill_blanks():
                    word_to_guess[index] = user_guess
                    return word_to_guess

                print("\nYou have", num_of_guesses, "guesses")
                print(word_to_guess)  # Prints word. Updates with letters guessed
                user_guess = input("Enter a letter: ").upper()

                # If letter is guessed, fill_blanks function adds the letter to the list
                for index, letter in enumerate(hidden_word):
                    if user_guess == letter:
                        fill_blanks()

                if hidden_word == word_to_guess:  # Winning the game
                    print("You win! The word is", word)
                    print("Definition:", definition[index_of_word])
                    game = menu()
                    break

                if num_of_guesses == 1:  # Losing the game
                    print("Game over! The word was", word)
                    print("Definition:", definition[index_of_word])
                    game = menu()
                    break

                # If the fill_blanks function is not called, then the guess is incorrect
                # and the number of guesses left is reduced
                if not fill_blanks.has_been_called:
                    num_of_guesses -= 1
                    break

    hangman_game(word)


play_game()
