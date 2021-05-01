#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import konlpy
from konlpy.tag import Kkma

import import_ipynb
from Content_Morpheme import Morpheme
from Calculate import Calculator


# In[ ]:


class Sentence(object):
    kk = Kkma()
    
    infos = list()
    infos_each = list()
    scores = list()

    def __init__(self, sentence = None):
        if sentence == None:
            Sentence.scores.append(0)
            return
        
        self.sentence = sentence
        self.analysis()
        self.create_info()
        self.add_info()
        
    def analysis(self):
        positions = Sentence.kk.pos(self.sentence)
        
        for position in positions:
            Morpheme(position)
            
        self.score = Calculator.calculate_sentence_score()
        Calculator.clean_sentence_score()
        Sentence.scores.append(self.score)
    
    def get_score(self):
        return self.score
    
    def get_sentence(self):
        return self.sentence
    
    def create_info(self):
        self.info = Morpheme.get_infos()
        Morpheme.clean()
        
    def add_info(self):
        for info in self.info:
            Sentence.infos.append(info)
        
        Sentence.infos_each.append(self.info)
        
    @classmethod
    def get_infos(cls):
        return cls.infos
    
    @classmethod
    def get_infos_each(cls):
        return cls.infos_each
    
    @classmethod
    def get_scores(cls):
        return cls.scores
    
    @classmethod
    def clean(cls):
        cls.infos = list()
        cls.infos_each = list()
        cls.scores = list()

