# Manuel Adrianzen and Maciej Girek
# CS 421 Natural Language Processing
# UIC Spring 2019

import sys
import sqlite3
import nltk.tokenize
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet
# stanford NER
import nltk
from nltk.tag.stanford import StanfordNERTagger

# Proper noun import details
import os

java_path = "C:/Program Files/Java/jdk1.8.0_161/bin/java.exe"
os.environ['JAVAHOME'] = java_path
jar = './stanford-ner.jar'

model = './english.all.3class.distsim.crf.ser.gz'

# Prepare NER tagger with english model
ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')


############################### NER

try:
    from itertools import izip as zip
except ImportError: # will be 3.x series
    pass

import os
from nltk.parse import stanford
from nltk.tag import StanfordPOSTagger

# break the sentence up into tokens and tags

##### CONVERT TO N
from nltk.corpus import wordnet as wn

# Just to make it a bit more readable
WN_NOUN = 'n'
WN_VERB = 'v'
WN_ADJECTIVE = 'a'
WN_ADJECTIVE_SATELLITE = 's'
WN_ADVERB = 'r'


def convert(word, from_pos, to_pos):
    """ Transform words given from/to POS tags """

    synsets = wn.synsets(word, pos=from_pos)

    # Word not found
    if not synsets:
        return []

    # Get all lemmas of the word (consider 'a'and 's' equivalent)
    lemmas = [l for s in synsets
              for l in s.lemmas
              if s.name.split('.')[1] == from_pos
              or from_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)
              and s.name.split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)]

    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms()) for l in lemmas]

    # filter only the desired pos (consider 'a' and 's' equivalent)
    related_noun_lemmas = [l for drf in derivationally_related_forms
                           for l in drf[1]
                           if l.synset.name.split('.')[1] == to_pos
                           or to_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)
                           and l.synset.name.split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)]

    # Extract the words from the lemmas
    words = [l.name for l in related_noun_lemmas]
    len_words = len(words)

    # Build the result in the form of a list containing tuples (word, probability)
    result = [(w, float(words.count(w)) / len_words) for w in set(words)]
    result.sort(key=lambda w: -w[1])

    # return all the possibilities sorted by probability
    return result
#####

def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

def largestSimilarity(geoPercenatge,musicPercentage,moviePercentage):
    if( geoPercenatge > musicPercentage):
        if( geoPercenatge > moviePercentage):
            return 'Geography'
    elif( musicPercentage > geoPercenatge):
        if( musicPercentage > moviePercentage):
            return 'Music'
    elif ( moviePercentage > geoPercenatge):
        if ( moviePercentage > musicPercentage):
            return 'Movie'
    elif (moviePercentage == geoPercenatge):
        return 'Movie, Geography'
    elif (musicPercentage == geoPercenatge):
        return 'Music, Geography'
    elif (moviePercentage == musicPercentage):
        return 'Movie, Music'
    else:
        # should never reach
        return 'Movie ' + str(moviePercentage) + ' Geography ' + str(geoPercenatge) + 'Music ' + str(musicPercentage)

def nounSimilarity(noun):

    w1 = wordnet.synset(str(noun)+'.n.01')
    w2 = wordnet.synset('location.n.01')
    w3 = wordnet.synset('album.n.01')
    w4 = wordnet.synset('movie.n.01')
    
    geoPercenatge = w1.path_similarity(w2);
    musicPercentage = w1.path_similarity(w3);
    moviePercentage = w1.path_similarity(w4);
    return largestSimilarity(geoPercenatge,musicPercentage,moviePercentage)

def ProperNounNER(word):
    words = nltk.word_tokenize(word)
    tupple = ner_tagger.tag(words)

    # return the NER tag
    tag = tupple[0][1]

    if tag == 'LOCATION':
        tag =  'Geography'
    else:
        tag =  'Movie'
    return tag


def main():

    # Get sentences from input file
    with open('input.txt', 'r') as f:
        data = [line.strip() for line in f]
    #POS tag sentences
    taggedSentences = []
    from nltk import Tree

    pattern = """NP: {(<DT>?<NNP>+<JJR>) | (<DT>?<NN>+<JJR>)  | (<DT>?<JJ>*<NN>)|(<DT>?<JJ>*<NNP>+) | (<DT>?<NN>+<JJS>) | (<DT>?<JJS><NN>+) | (<WDT>?<WRB>?<WP>?)} 
        VBD: {<VBD>}
        PP: { <IN><NP> | <IN>}
        IN: {<IN>}
        VP: {<V> | <NP> | <PP> | <NP><PP>+ }"""

    for s in data:
        taggedSentences.append(nltk.pos_tag(nltk.word_tokenize(s)))

    #print(taggedSentences)

    NounList = []
    categories = []

    for sentence in taggedSentences:
        element = ''
        for i,j in sentence:
            if( j == 'NN'):
                if( element == ''):
                    element += nounSimilarity(i)
            if (j == 'NNP'):
                if( ProperNounNER(i) != None):
                    if( element == ''):
                        element += ProperNounNER(i)
        categories.append(element)
        if( element != ''):
            sentence.append(element)

    counter = 0
    for s in data:
        print("<QUESTION> " + s)
        print("<CATEGORY> " + categories[counter])
        print("<PARSETREE>")
        result = nltk.pos_tag(nltk.word_tokenize(s))
        NPChunker = nltk.RegexpParser(pattern)
        result = NPChunker.parse(result)
        Tree.fromstring(str(result)).pretty_print()
        counter+=1;

if __name__ == "__main__":
    main()
