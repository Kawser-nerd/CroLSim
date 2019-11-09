import os
import code_comment
from fnmatch import fnmatch

source_folder = '/home/sr-p2irc-big14/testData/Python'
pattern = "*.py"

for path, subdirs, files in os.walk(source_folder):
    for name in files:
        if fnmatch(name, pattern):
            print(os.path.join(path, name))


for comment in code_comment.extract('/home/sr-p2irc-big14/testData/Python/abbott/abbott/transport.py'):
    print(comment.body_str)


import nltk
lines = 'Note: iterating over the listener dictionaries and sets are done with copies, not an iterator, because of the posibility of the dictionary being modified somewhere down the stack in an event handler'
# function to test if something is a noun
is_noun = lambda pos: pos[:2] == 'VB'
# do the nlp stuff
tokenized = nltk.word_tokenize(lines)
nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]

print(nouns)