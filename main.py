# http://www.andrew-tremblay.com/blog/anagrams-python-nltk-001/
# https://www.geeksforgeeks.org/given-a-sequence-of-words-print-all-anagrams-together/
# http://echochamber.me/viewtopic.php?t=32247
# https://www.reddit.com/r/dailyprogrammer/comments/52enht/20160912_challenge_283_easy_anagram_detector/

"""
You've made an important decision. Now, let's get to the matter.
We have a message for you. But we hid it.
Unless you know the secret phrase, it will remain hidden.
Can you write the algorithm to find it?
Here is a couple of important hints to help you out:
- An anagram of the phrase is: "poultry outwits ants"
- There are three levels of difficulty to try your skills with
- The MD5 hash of the easiest secret phrase is "e4820b45d2277f3844eac66c903e84be"
- The MD5 hash of the more difficult secret phrase is "23170acc097c24edb98fc5488ab033fe"
- The MD5 hash of the hard secret phrase is "665e5bcb0c20062fe8abaaf4628bb154"
Here is a list of english words, it should help you out.
Type the secret phrase here to see if you found the right one
Trustpilot Development Team
We imagine that right now, you're feeling a bit like Alice. Hmm? Tumbling down the rabbit hole?
"""

 

import hashlib
import itertools
import functools


def memoize(obj):
    cache = obj.cache = {}
    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memoizer
    

def get_string_dict(string):
    string = ''.join([i for i in string if i.isalnum()]).lower()
    string_dict = {i: 0 for i in string}
    for i in string:
        string_dict[i] += 1
    return string_dict
 

def is_candidate(string_dict, word):
    for char in word:
        if char not in string_dict or string_dict[char] - 1 < 0:
            return False
        else:
            string_dict[char] -= 1
    return True


def is_anagram(string_dict, anagram_words):
    for word in anagram_words:
        if not is_candidate(string_dict, word):
            return False

    for i in string_dict.values():
        if i != 0:
            return False
    else:
        return True

# ------------ #
# ------------ #

with open('wordlist') as f:
    words = f.read().splitlines()
f.close()

md5_hashes = ['e4820b45d2277f3844eac66c903e84be', '23170acc097c24edb98fc5488ab033fe', '665e5bcb0c20062fe8abaaf4628bb154']
string = 'poultry outwits ants'
words = [word for word in words if is_candidate(get_string_dict(string).copy(), word) and word.isalpha()]
words = list(set(words))
words = sorted(words, key=lambda s: -len(s))

def find_anagrams(string, words, level=0):
 
    results = []
    string_dist = get_string_dict(string)

    for word in words:

        if is_candidate(string_dist.copy(), word):
            match_base = [word]

            # check if this is the end of recursion
            # or if adding this word finishes the anagram
            if len(word) == len(string):
                results.append(match_base)

            # if the anagram is not finished
            # keep only remaining chars in string
            # look for anagrams inside tha remaining string
            elif len(word) < len(string):
                string_part = string
                for char in word:
                    string_part = string_part.replace(char, '', 1)
                match_part = find_anagrams(string_part, words[words.index(word):], level=level+1)

                # unstack
                for part in match_part:
                    match = match_base.copy()
                    match.extend(part)
                    results.append(match)

                    # check the stack level
                    # permute the anagram words
                    # and check if it matches md5 hash
                    if level == 0:
                        print(match)
                        for anagram in itertools.permutations(match, len(match)):
                            anagram = ' '.join(anagram)
                            md5_hash = hashlib.md5(anagram.encode('utf-8')).hexdigest()
                            if md5_hash in md5_hashes:
                                print(f'Match found: {md5_hash} {anagram}')

    return results


results = find_anagrams(string, words)
