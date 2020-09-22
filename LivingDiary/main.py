import pandas as pd
import spacy
from spacy import displacy
import re
import neuralcoref
nlp = spacy.load('en_core_web_sm')
coref = neuralcoref.NeuralCoref(nlp.vocab)
nlp.add_pipe(coref, name='neuralcoref')
text = """
        Today was a rough day. a giant lizard destroyed my home, and The Avengers crashed my car during the fight! I 
        hate The Avengers. Also, I've been feeling sad that Jeffery got eaten by wolves. He didn't give me back my
        Elvis records before he died, so now I feel awkward asking his mom for them back.  
"""
doc = nlp(text)
displacy.serve(list(doc.sents), style="dep")
'''
The system you want to use is thus:
Pipeline 1: feelings/events towards objects (ex: "I hate the Avengers" or "A giant lizard destroyed my house")
    1. find Nouns and proper nouns
    2. filter by nouns that have a dobj
    3. filter by dobj with nsubj
    4. determine if date is established

Pipeline 2: what happened to proper nouns (ex: "Jeffery got eaten by wolves")
    1. find proper nouns
    2. filer by nouns with nsubjpass
    3. check if nsubjpass has agent with pobj/noun
    
Pipeline 3: what are YOU feeling and what about? (ex: "I feel sad that Jeffery died")  
    1. Check for "I" or 'I've/I'm/etc'
    2. nsubj to "I" is 'feeling/feel/thought/felt/etc'
    3. feeling should be acomp
    4. find ccomp to nsubj to find reason
    
Feature additions:
    1. "who is [PRNOUN]?" feature to identify people
    2. class instance for different types of 'topics'
        a. ex: 'Jeffery' is a 'person'. What is inside the 'person' class? The 'event' class? The 'feelings' class?
    3. 

Things to do:
    1. Talk to counseling/linguist experts at SJSU/CSUMB
    2. look into event store
    3. get public diary entires for testing data 
    
'''
def pipeline_1(doc):
    return_texts = pd.DataFrame(index=range(len(list(doc.noun_chunks))),
                                columns=['text', 'sent_structure_', 'sent_structure', 'keywords', 'pos_tags', 'pipeline'])
    k = 0
    for token in doc.noun_chunks:
        if (token.root.pos_ in ['NOUN', 'PRON']) & (token.root.head.pos_ == 'VERB') & (token.root.dep_ == 'nsubj'):
            for token2 in doc.noun_chunks:
                if (token2.text != token.text) & (token2.root.head.i == token.root.head.i) & (token2.root.dep_ == 'dobj'):
                    child_deps = [i.dep_ for i in token.root.head.children]
                    if 'neg' in child_deps:
                        neg = 'did not '
                    else:
                        neg = ''
                    final_text = re.sub('  +', ' ', f"{token.text} {neg}{token.root.head.text} {token2.text}")
                    final_text = re.sub('\n', '', final_text)
                    print(final_text)
                    return_texts.loc[k, :] = [final_text,
                                            [i.pos_ for i in token.root.sent],
                                            [i.pos for i in token.root.sent],
                                            [i.text for i in token.root.sent if i.pos_ in ['PROPN', 'NOUN']],
                                            [i.pos_ for i in token.root.sent if i.pos_ in ['PROPN', 'NOUN']],
                                            1]
                    k += 1
    return return_texts.dropna()


def pipeline_1(doc):
    return_texts = pd.DataFrame(index=range(len(list(doc.noun_chunks))),
                                columns=['text', 'sent_structure_', 'sent_structure', 'keywords', 'pos_tags',
                                         'pipeline'])

    # if token.root.pos_ == 'NOUN' & (token.root.dep_ == 'dobj') & (token.root.head):
        #     break

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)


import spacy
import neuralcoref

nlp = spacy.load('en')
neuralcoref.add_to_pipe(nlp)
doc = nlp('My sister has a dog. She loves him.')
print(doc1._.coref_clusters)

doc2 = nlp('Angela lives in Boston. She is quite happy in that city.')
for ent in doc2.ents:
    print(ent._.coref_cluster)



class people(object):
    def __init__(self, name, age=None, location=None, article=None, conneciton=None):
        self.name = name
        self.age = age
    def new article(self):
        '''
        do some stuff, make a new article
        '''




