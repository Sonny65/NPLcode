import nltk
from nltk import conlltags2tree, tree2conlltags
from nltk.tokenize import *

# set up NER path
from nltk.tag.stanford import StanfordNERTagger
jar = './stanford-ner-tagger/stanford-ner.jar'
model = './stanford-ner-tagger/english.all.3class.distsim.crf.ser.gz'
ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')

# corpus trainning data
from nltk.corpus import conll2000

# chunkLocation =  r"""Wh: {<WRB>}"""{<PRP.?>*<RB.?>*<JJ.?>*<POS.?>*<NN>}
chunkGram = r"""
                WH: {<WRB>}
                SUFDESC: {<IN><PRP.?|RB.?|JJ.?|DT>*<NN>}
                DESC: {<PRP.?|RB.?|JJ.?|DT>*(<PERSON><POS>)*}
                TAR: {<DESC>*(<CC><DESC>+)*<NN|GRE><SUFDESC>*<DESC>*}
                """

def chunking(input):
    token = word_tokenize(input)
    tag = nltk.pos_tag(token)
    # nameEnt = ner_tagger.tag(token)
    nameEnt = nltk.ne_chunk(tag)

    chunkParser = nltk.RegexpParser(chunkGram)

    chunk = chunkParser.parse(nameEnt)

    # iob_tag = tree2conlltags(chunk)
    #
    # tree = conlltags2tree(iob_tag)

    print chunk

    return chunk

def relation_extraction(chunk):
    # find command type
    for subtree in chunk:
        if hasattr(subtree, 'label'):
            if subtree.label() == 'WH':
                wh_loc(chunk)
                break

def wh_loc(chunk):
    targets = []
    # find the target location
    for subtree in chunk:
        if hasattr(subtree, 'label'):
            if subtree.label() == 'TAR':
                targets.append(target_chunk(subtree))

    print "Instruction: Where"

    for target in targets:
        for index,element in enumerate(target):
            if index == 0:
                print ""
                print "Taget: "+element
                print ""
                print "Desc:",
            else:
                print "[ ",
                for word in element:
                    print word+" ",

                print "] ",

    print ""
    print ""


def target_chunk(subtree):

    descCollection = []

    for element in subtree:

        # this is the DESC or SUFDESC
        if hasattr(element, 'label'):
            desc = []
            for word in element:
                desc.append(word[0])
            descCollection.append(desc)
        else:
            descCollection = [element[0]]+descCollection

    return descCollection

while True:
    input = raw_input("Sentence:")
    print ""

    chunk = chunking(input)

    relation_extraction(chunk)
