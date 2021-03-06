# Problem Set 2, hangman.py
# Name: Guoziyu
# Collaborators: None
# Time spent: two hours

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------


# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for i in range(len(secret_word)):
        if secret_word[i] not in letters_guessed:  # 若所猜单词的字母不在已猜字母中，返回false
            return False
    return True  # 若无误，返回true


'''
secret_word ='apple'
letters_guessed = ['e','i','k','p','r','s']
print(is_word_guessed(secret_word,letters_guessed))
'''


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    result = ''
    for i in range(len(secret_word)):
        if secret_word[i] in letters_guessed:  # 若已猜过则加该字母和空格
            result = result+secret_word[i]+' '
        else:
            result = result+'_ '  # 若未猜过则加_和空格
    return result


'''
secret_word = 'apple'
letters_guessed = ['e', 'i', 'k', 'p', 'r', 's']
print(get_guessed_word(secret_word, letters_guessed))
'''


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    result = ''
    for i in range(len(string.ascii_lowercase)):
        if string.ascii_lowercase[i] not in letters_guessed:  # 若该字母未猜过则加入
            result = result+string.ascii_lowercase[i]
    return result


'''
letters_guessed = ['e', 'i', 'k', 'p', 'r', 's']
print(get_available_letters(letters_guessed))
'''


def hangman(secret_word):
    Bingo = False  # 是否猜中
    unique_letter = 0  # 单词中的独特字母数
    warning_num = 3  # 剩余warning数目
    guess_num = 6  # 剩余guess数目
    letters_guessed = []  # 已猜字母列表
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is %s letters long." % len(secret_word))
    print("You have %s warnings left." % warning_num)
    print("-------------")
    while Bingo == False and guess_num > 0:
        print("You have %s guesses left." % guess_num)
        print("Available letters: %s" % get_available_letters(letters_guessed))
        letter = input("Please guess a letter:")  # 输入一个字母
        if str.isalpha(letter) == False or len(letter) != 1:  # 若不是字母以及输入长度不是一个
            if warning_num > 0:  # 若还有warning
                warning_num = warning_num-1
                print("Oops! That is not a valid letter. You have %s warnings left: %s" % (warning_num,
                                                                                           get_guessed_word(secret_word, letters_guessed)))
            else:  # warning数为0减少guess剩余数
                guess_num = guess_num-1
                print("Oops! That is not a valid letter. You have no warnings left: %s" %
                      get_guessed_word(secret_word, letters_guessed))
        else:  # 输入为字母
            letter = str.lower(letter)  # 化为小写
            if letter not in letters_guessed:  # 该字母未猜过
                letters_guessed.append(letter)  # 加入已猜列表
                if is_word_guessed(secret_word, letters_guessed) == True:  # 若已猜中则Bingo为true退出循环
                    Bingo = True
                    unique_letter = unique_letter+1
                    print("Good guess: %s" % get_guessed_word(
                        secret_word, letters_guessed))
                else:  # 若还未猜出单词
                    if letter in secret_word:  # 字母猜中了
                        unique_letter = unique_letter+1
                        print("Good guess: %s" % get_guessed_word(
                            secret_word, letters_guessed))
                    else:  # 字母未在单词中
                        print("Oops! That letter is not in my word: %s" %
                              get_guessed_word(secret_word, letters_guessed))
                        if letter == 'a' or letter == 'e' or letter == 'i' or letter == 'o' or letter == 'u':  # 元音
                            guess_num = guess_num-2
                        else:  # 辅音
                            guess_num = guess_num-1
            else:  # 该字母已猜过
                if warning_num > 0:
                    warning_num = warning_num-1
                    print("Oops! You've already guessed that letter. You now have %s warnings: %s" %
                          (warning_num, get_guessed_word(secret_word, letters_guessed)))
                else:
                    guess_num = guess_num-1
                    print("Oops! You've already guessed that letter. You now have no warnings: %s" %
                          get_guessed_word(secret_word, letters_guessed))

        print("-------------")
    if Bingo == True:  # 游戏胜利
        print("Congratulations, you won!\nYour total score for this game is: %s" %
              (guess_num*unique_letter))
    else:  # 失败
        print("Sorry, you ran out of guesses. The word was %s." % secret_word)
# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    my_word = my_word.replace(' ', '')  # 去掉my_word的空格
    if len(my_word) != len(other_word):  # 长度不同直接返回false
        return False
    else:
        for i in range(len(my_word)):
            if my_word[i] != '_':
                if my_word[i] != other_word[i]:  # 若不是_且不相同则不匹配返回false
                    return False
            else:
                if other_word[i] in my_word:  # 若是_但该字母已出现在my_word中也返回false
                    return False
    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    flag = False  # 是否匹配
    for i in range(len(wordlist)):
        if match_with_gaps(my_word, wordlist[i]):
            flag = True
            print(wordlist[i], ' ', end='')  # 输出单词，注意去掉换行
    if not flag:
        print("No matches found.")  # 若无匹配
    else:
        print("")


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    '''
    Bingo = False  # 是否猜中
    unique_letter = 0  # 单词中的独特字母数
    warning_num = 3  # 剩余warning数
    guess_num = 6  # 剩余guess数
    letters_guessed = []  # 已猜字母列表
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is %s letters long." % len(secret_word))
    print("You have %s warnings left." % warning_num)
    print("-------------")
    while Bingo == False and guess_num > 0:
        print("You have %s guesses left." % guess_num)
        print("Available letters: %s" % get_available_letters(letters_guessed))
        letter = input("Please guess a letter:")
        if str.isalpha(letter) == False or len(letter) != 1: # not a alpha (length should be one!)
            if letter == '*':  # 输出提示
                show_possible_matches(get_guessed_word(
                    secret_word, letters_guessed))
            else:
                if warning_num > 0:  # 剩余warning大于0
                    warning_num = warning_num-1
                    print("Oops! That is not a valid letter. You have %s warnings left: %s" % (warning_num,
                                                                                               get_guessed_word(secret_word, letters_guessed)))
                else:  # no warning decrease guess number
                    guess_num = guess_num-1
                    print("Oops! That is not a valid letter. You have no warnings left: %s" %
                          get_guessed_word(secret_word, letters_guessed))
        else:  # is a alpha
            letter = str.lower(letter)
            if letter not in letters_guessed:  # had not guessed
                letters_guessed.append(letter)
                if is_word_guessed(secret_word, letters_guessed) == True:  # win
                    Bingo = True
                    unique_letter = unique_letter+1
                    print("Good guess: %s" % get_guessed_word(
                        secret_word, letters_guessed))
                else:
                    if letter in secret_word:  # guess right
                        unique_letter = unique_letter+1
                        print("Good guess: %s" % get_guessed_word(
                            secret_word, letters_guessed))
                    else:  # guess wrong
                        print("Oops! That letter is not in my word: %s" %
                              get_guessed_word(secret_word, letters_guessed))
                        if letter == 'a' or letter == 'e' or letter == 'i' or letter == 'o' or letter == 'u':  # vowel
                            guess_num = guess_num-2
                        else:  # consonat
                            guess_num = guess_num-1
            else:  # letter had been guessed
                if warning_num > 0:
                    warning_num = warning_num-1
                    print(
                        "Oops! You've already guessed that letter. You now have %s warnings: %s" % (warning_num, get_guessed_word(secret_word, letters_guessed)))
                else:
                    guess_num = guess_num-1
                    print(
                        "Oops! You've already guessed that letter. You now have no warnings: %s" % get_guessed_word(secret_word, letters_guessed))

        print("-------------")
    if Bingo == True:
        print("Congratulations, you won!\nYour total score for this game is: %s" %
              (guess_num*unique_letter))
    else:
        print("Sorry, you ran out of guesses. The word was %s." % secret_word)


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.
if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

    ###############

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.

    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
