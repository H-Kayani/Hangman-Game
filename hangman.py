from string import ascii_lowercase
import random

#loads the text file
wordlist = 'words.txt'

def main():
    
    print("")
    print('----- Welcome to Hangman Ultimate Edition -----')
    print("")

    #options for the users
    option = input("Do you want to Play (p),  view the leaderboard (l) or quit (q) ")
    print("")
    if option == "p":
        hangman()
    elif option == "l":
        score()
    elif option == "q":
        print ("Thanks for playing")

def hangman():

    print("")
    name = input("Please enter your name: ")
    name = name
    print("")

    #gets the number of attempts
    attempts_remaining = get_num_attempts()
    #gets the length of the word
    min_word_length = get_min_word_length()

    # Randomly select a word
    print('Loading word list from file...')
    word = load_words(min_word_length)
    print()

    # Initialize game state variables
    index = [letter not in ascii_lowercase for letter in word]
    letters_guessed = set(ascii_lowercase)
    wrong_letters = []
    word_solved = False

    # Main game loop
    while attempts_remaining > 0 and not word_solved:
        # Print current game state
        print('Word: {0}'.format(get_guessed_word(word, index)))
        print('Attempts Remaining: {0}'.format(attempts_remaining))
        print('Previous Guesses: {0}'.format(' '.join(wrong_letters)))

        # Get player's next letter guess
        next_letter = get_remaining_letters(letters_guessed)

        # Check if letter guess is in word
        if next_letter in word:
            # Guessed correctly
            print('{0} is in the word!'.format(next_letter))

            # Reveal matching letters
            for i in range(len(word)):
                if word[i] == next_letter:
                    index[i] = True
        else:
            # Guessed incorrectly
            print('{0} is NOT in the word!'.format(next_letter))

            # Decrement num of attempts left and append guess to wrong guesses
            attempts_remaining -= 1
            wrong_letters.append(next_letter)

        # Check if word is completely solved
        if False not in index:
            word_solved = True
        print()


    # The game is over: reveal the word
    print('The word is {0}'.format(word))

    # Notify player of victory or defeat
    if word_solved:
        print('Congratulations, you won!')
    else:
        print('Try again next time!')

    # Gets the remaining attempts and multiply it by min word length
    score = (min_word_length * attempts_remaining)
    print("Your final scrore is ", score)
    print("")

    score_list = [[score,name]]

    # Saves the final score and name of the user
    with open('score.txt', 'a') as score:
        for item in score_list:
            score.write("%s\n" % item)

    option = input("Press 'm' for main menu, Press 'p' to play again ")
    if option == "m":
        main()
    elif option == "p":
        hangman()

def score():
    score_file = open("score.txt", "r")

    # Reads the text file and display the score table
    if score_file.mode == 'r':
        contents = score_file.read()
        print(contents)

    option = input("Press 'm' for main menu ")
    if option == "m":
        main()
    elif option != "":
        print("Please select a valid option")


def get_num_attempts():
    while True:
        print("")
        num_attempts = input('How many attempts would you like to have [1-25] ')
        print("")
        # Sets the number of attempts according to the users choice
        try:
            num_attempts = int(num_attempts)
            if 1 <= num_attempts <= 25:
                return num_attempts
            else:
                print('{0} is not between 1 and 25'.format(num_attempts))
        except ValueError:
            print('{0} is not an integer between 1 and 25'.format(
                num_attempts))


def get_min_word_length():
    """Get user-inputted minimum word length for the game."""
    while True:
        print("")
        min_word_length = input('What minimum word length do you want? [4-10] ')
        print("")
        # Finds the len of a word according to the users choice
        try:
            min_word_length = int(min_word_length)
            if 4 <= min_word_length <= 16:
                return min_word_length
            else:
                print('{0} is not between 4 and 16'.format(min_word_length))
        except ValueError:
            print('{0} is not an integer between 4 and 16'.format(
                min_word_length))


def get_guessed_word(word, index):
    # Sets up the guessed word and when a users get it right it displays the word
    if len(word) != len(index):
        raise ValueError('Word length and indices length are not the same')
    displayed_word = ''.join(
        [letter if index[i] else '_ ' for i, letter in enumerate(word)])
    return displayed_word.strip()


def get_remaining_letters(letters_guessed):
    # Gets the user next letter guessed
    if len(letters_guessed) == 0:
        raise ValueError('There are no remaining letters')
    while True:
        next_letter = input('Choose the next letter: ').lower()
        if len(next_letter) != 1:
            print('{0} is not a single character'.format(next_letter))
        elif next_letter not in ascii_lowercase:
            print('{0} is not a letter'.format(next_letter))
        elif next_letter not in letters_guessed:
            print('{0} has been guessed before'.format(next_letter))
        else:
            letters_guessed.remove(next_letter)
            return next_letter
    
def load_words(min_word_length):
    num_words_processed = 0
    curr_word = None
    # Finds the exact length of the word the user requested and make it as the guessed word
    with open(wordlist, 'r') as f:
        for word in f:
            if '(' in word or ')' in word:
                continue
            word = word.strip().lower()
            if len(word) < min_word_length:
                continue
            num_words_processed += 1
            if random.randint(1, num_words_processed) == 1:
                curr_word = word
    return curr_word



if __name__ == '__main__':
    # Runs the program
    while main():
        print()

