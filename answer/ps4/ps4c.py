# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
from ps4a import get_permutations

### HELPER CODE ###


def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''

    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'


class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object

        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.

        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()

    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)

        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled
        according to vowels_permutation. The first letter in vowels_permutation
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''

        result_dict = {}
        l = list(vowels_permutation.lower())  # 统一先化为小写
        for i in VOWELS_LOWER+VOWELS_UPPER+CONSONANTS_LOWER+CONSONANTS_UPPER:
            if i == 'a':  # 对于元音特殊处理
                result_dict[i] = l[0]
            elif i == 'e':
                result_dict[i] = l[1]
            elif i == 'i':
                result_dict[i] = l[2]
            elif i == 'o':
                result_dict[i] = l[3]
            elif i == 'u':
                result_dict[i] = l[4]
            elif i == 'A':
                result_dict[i] = l[0].upper()
            elif i == 'E':
                result_dict[i] = l[1].upper()
            elif i == 'I':
                result_dict[i] = l[2].upper()
            elif i == 'O':
                result_dict[i] = l[3].upper()
            elif i == 'U':
                result_dict[i] = l[4].upper()
            else:
                result_dict[i] = i
        return result_dict

    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary

        Returns: an encrypted version of the message text, based
        on the dictionary
        '''
        s = ''
        for i in self.get_message_text():
            if i != ' 'and i not in string.punctuation:
                s += transpose_dict[i]
            else:
                s += i
        return s


class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        super().__init__(text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message

        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.

        If no good permutations are found (i.e. no permutations result in
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message

        Hint: use your function from Part 4A
        '''
        max_num = 0
        best_perm = ''
        for i in get_permutations(VOWELS_LOWER):  # 遍历所有排列方式
            str = self.apply_transpose(self.build_transpose_dict(i))
            valid_num = 0
            list = str.split()
            for j in list:
                if is_word(self.get_valid_words(), j):
                    valid_num = valid_num+1  # 计算单词合法数
            if valid_num > max_num:
                best_perm = i  # 记录最佳的
            max_num = max(max_num, valid_num)
        return self.apply_transpose(self.build_transpose_dict(best_perm))


if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(),
          "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

    # TODO: WRITE YOUR TEST CASES HERE

    # test for SubMessage (first)
    message = SubMessage("I'm Chinese!")
    permutation = "iuoae"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(),
          "Permutation:", permutation)
    print("Expected encryption:", "O'm Chonusu!")
    print("Actual encryption:", message.apply_transpose(enc_dict))

    # test for EncryptedSubMessage (first)
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

    # test for SubMessage (second)
    message = SubMessage("I'm studying!")
    permutation = "eauio"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(),
          "Permutation:", permutation)
    print("Expected encryption:", "U'm stodyung!")
    print("Actual encryption:", message.apply_transpose(enc_dict))

    # test for EncryptedSubMessage (second)
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
