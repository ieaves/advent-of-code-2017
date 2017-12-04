"""
--- Part One ---
A new system policy has been put in place that requires all accounts to use a passphrase instead of simply a password. A passphrase consists of a series of words (lowercase letters) separated by spaces.

To ensure security, a valid passphrase must contain no duplicate words.

For example:

aa bb cc dd ee is valid.
aa bb cc dd aa is not valid - the word aa appears more than once.
aa bb cc dd aaa is valid - aa and aaa count as different words.
The system's full passphrase list is available as your puzzle input. How many passphrases are valid?

--- Part Two ---

For added security, yet another system policy has been put in place. Now, a valid passphrase must contain no two words that are anagrams of each other - that is, a passphrase is invalid if any word's letters can be rearranged to form any other word in the passphrase.

For example:

abcde fghij is a valid passphrase.
abcde xyz ecdab is not valid - the letters from the third word can be rearranged to form the first word.
a ab abc abd abf abj is a valid passphrase, because all letters need to be used when forming another word.
iiii oiii ooii oooi oooo is valid.
oiii ioii iioi iiio is not valid - any of these words can be rearranged to form any other word.
Under this new system policy, how many passphrases are valid?

Although it hasn't changed, you can still get your puzzle input.


"""
import math
import collections


def line_reader(file):
    with open(file, 'r') as f:
        for line in f:
            res = [item for item in line.strip().split()]
            yield(res)


def has_repeated_words(phrase):
    ret = False if len(phrase) == len(set(phrase)) else True
    return(ret)


def has_anagrams(phrase):
    counters = [collections.Counter(word) for word in phrase]
    for i, word_count in enumerate(counters):
        if word_count in counters[i+1:]:
            return(True)
    return(False)


def valid_phrase(phrase):
    if has_repeated_words(phrase):
        return(False)
    if has_anagrams(phrase):
        return(False)
    return(True)


def count_valid_phrases(file, valid_func):
    lines = line_reader(file)
    count = sum(1 for line in lines if valid_func(line))
    return(count)


if __name__ == "__main__":
    assert valid_phrase("abcde fghij".split()) is True
    assert valid_phrase("abcde xyz ecdab".split()) is False
    assert valid_phrase("a ab abc abd abf abj".split()) is True
    assert valid_phrase("iiii oiii ooii oooi oooo".split()) is True
    assert valid_phrase("oiii ioii iioi iiio".split()) is False

    phrase_count = count_valid_phrases('input.txt', lambda x: not has_repeated_words(x))
    print('part 1 count: ' + str(phrase_count))
    phrase_count = count_valid_phrases('input.txt', valid_phrase)
    print('part 2 count: ' + str(phrase_count))
