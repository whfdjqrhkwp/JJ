#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import konlpy
from konlpy.tag import Kkma

import import_ipynb
from Content_Morpheme import Morpheme
from Calculate import Calculator

from Log import Logger
log = Logger('Content_Sentence')


# In[ ]:


class Sentence(object):
    kk = Kkma()
    
    infos = list()
    infos_each = list()
    scores = list()
    scores_voca = list()
    scores_gram = list()

    def __init__(self, sentence = None):
        if sentence == None:
            Sentence.scores.append(0)
            return
        
        self.sentence = sentence
        self.analysis()
        self.create_info()
        self.add_info()
        
    def analysis(self):
        #log.info('Start Getting Morphemes')
        positions = Sentence.kk.pos(self.sentence)
        #log.info('Complete Getting {} Morphemes'.format(len(positions)))
        
        for position in positions:
            Morpheme(position)
            
        self.score, self.score_voca, self.score_gram = Calculator.calculate_sentence_score()
        Calculator.clean_sentence_score()
        
        Sentence.scores.append(self.score)
        Sentence.scores_voca.append(self.score_voca)
        Sentence.scores_gram.append(self.score_gram)
        
        #log.info('Sentence Analysis Complete')
    
    def create_info(self):
        self.info = Morpheme.get_infos()
        Morpheme.clean_info()
        
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
    def get_scores_voca(cls):
        if len(cls.scores_voca) == 0:
            cls.scores_voca.append(0)
        return cls.scores_voca
    
    @classmethod
    def get_scores_gram(cls):
        if len(cls.scores_gram) == 0:
            cls.scores_gram.append(0)
        return cls.scores_gram
    
    @classmethod
    def clean(cls):
        cls.infos = list()
        cls.infos_each = list()
        cls.scores = list()
        cls.scores_voca = list()
        cls.scores_gram = list()

