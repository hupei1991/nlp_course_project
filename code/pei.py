# This script would be based on James' script
# Please put this file in /data/ directory :pei:

import os
import nltk
import random
import re
from nltk import sent_tokenize

# Read the whole folder and return a list of texts :meshal:
# Revised by :pei
def readFolder(folder, hamOrSpam, fileidx):
    for filename in os.listdir(folder):
        fileidx_filename[fileidx[0]] = filename
        f = open(folder + filename, 'r', errors ='ignore') # added ignore for character that couldn't be read :james:
        fileidx_content[fileidx[0]] = f.read()
        fileidx_class[fileidx[0]] = hamOrSpam
        f.close()
        fileidx[0] += 1

# create a method to remove newline characters :chris:
def restringify(email):
    n = email.split('\n')
    s = ' '.join(n)
    return s

# Restringify, and segment the contents of each piece of email into sentences
# Split the emails by sentence :james:

# Also get rid spaces in front of '?' , and '!', according to the definition
# of Punkt Sentence Segmenter;  revised by :pei:
def sentenceSegmenter(email):
    import re
    from nltk import sent_tokenize
    symbols_removed = re.sub(r'\s+(?:\.+|\?+|!+)', '.', email) 
    # remove the spaces before the period
    # from here, we would only consider the '$' sign in order to reduce the feature dimension :pei:
    money_spaces_removed = re.sub(r'(\$)(\s+)(\d+\.)(\s+)(\d+)', r'\1', symbols_removed) # remove the spaces involved with money :james:
    sents = sent_tokenize(money_spaces_removed)
    return sents

# Here defines the function used to do the word tokenization modified from :kayla:
# Since the punctuation won't be able to provide too much information on the classification
# of spam and ham, thus we would only use RegexpTokenizer to tokenize the sentences. Revised by :pei:
def wordTokenizer(sentence):
    from nltk.tokenize import RegexpTokenizer
    toker = RegexpTokenizer(r'\w+|\$+')
    # a list of words is returned :pei:
    return toker.tokenize(sentence)

# By :derek:
def lowerWord(word):
    #email is a string
    return word.lower()

# Remove stopwords function by :pei:
# The return value would be boolean, in order to remove the stopwords in the main function
def isStopword(word):
    from nltk.corpus import stopwords
    if word in stopwords.words('english'):
        return True
    return False


# Use a main function to organize each piece :pei:
# I will not use any other specific data structure to store metadata except for these dictionarys :pei:
if __name__ == "__main__":
    global fileidx_filename, fileidx_class, fileidx_content, fileidx_sentences, fileidxsentenceidxwordidx_word
    fileidx_filename = {} # {file_name : file_index} :pei:
    fileidx_class = {} # {file_index : file_class} :pei:
    fileidx_content = {} # {file_index : file_content} :pei:
    fileidxsentenceidx_sentence = {} # {file_index::sentence_index : sentence} :pei:
    fileidxsentenceidxwordidx_word = {} # {file_index::sentence_index:word_index : word}
    
    fileidx = [0] # file_index :pei:
    # Run readFolder separately on ham and spam to get dict data stored :pei:
    readFolder('corpus/ham/' , 'ham', fileidx)
    readFolder('corpus/spam/' , 'spam', fileidx)
    # Since we are not going to use the fileidx viarable again, we delete it from the memory stack :pei:
    del fileidx
    # We don't actually need to shuffle because they are in a dictionary which is unordered :pei:

    # Generate the dictionary of fileidx_sentences, by applying restringify and sentenseSegmenter on contents :pei:
    # with key of file_index::sentence_index, and segmented sentences as value :pei:
    for fileidx, content in fileidx_content.items():
        for idx, sent in enumerate(sentenceSegmenter(restringify(content))):
            fileidxsentenceidx_sentence[fileidx_filename[fileidx] + "::" + str(idx)] = sent

    # Generate the dictionary of fileidx::sentence_index::word_index and words, applying word tokenization :pei:
    for sentenceidx, sentence in fileidxsentenceidx_sentence.items():
        for idx, word in enumerate(wordTokenizer(sentence)):
            fileidxsentenceidxwordidx_word[sentenceidx + "::" + str(idx)] = word

    # Generate the dictionary of fileidx::sentence_index::word_index and lowercased words, applying lowerWord() :pei:
    for index, word in fileidxsentenceidxwordidx_word.items():
        fileidxsentenceidxwordidx_word[index] = lowerWord(word)

    # Remove the stopwords from the dictionary of fileidx::sentence_index::word_index and lowercased words,
    # CAUTION: THIS PART MAY NEED TO RUN FOR MINUTES (254.4 seconds on my machine) :pei:
    for index in list(fileidxsentenceidxwordidx_word):
        if isStopword(fileidxsentenceidxwordidx_word[index]):
            # remove the stopwords :pei:
            del fileidxsentenceidxwordidx_word[index]
    # We would save the dictionary into pickles to save time during development
    import pickle
    pickle.dump(fileidxsentenceidxwordidx_word, open( "temp.pkl", "wb" ) )
    # fileidxsentenceidxwordidx_word = pickle.load( open( "temp.pkl", "rb" ) )

    # Now, we are going to make each word as the key, with a list of their indices as the correspondingvalue :pei:
    # So that we can know the correlation of being spam or ham, for each word :pei:
    global word_indexlist
    word_indexlist = {}
    for index, word in fileidxsentenceidxwordidx_word.items():
        indexlist = []
        if word in word_indexlist:
            word_indexlist[word].append(index)
        else:
            indexlist.append(index)
            word_indexlist[word] = indexlist
    print(len(word_indexlist))

    # The final step would be calculation the correlation, separately for spam and ham
    # for one word being spam or ham :pei:
    global word_spamham
    word_spamham = {}
