'''
Created on 2018/09/16

@author: Kusunoki
'''
import nltk

def GetMaxByFunc(item, func_name):
    
    
def SortByFunc(item, func_name):
    sorted_terms = sorted(item.items(), key =func_name, reverse = True)
    return sorted_terms

def SeparateTerm(text):
    tokens = nltk.word_tokenize(text) 
    tagged = nltk.pos_tag(tokens)
    return tagged
