#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import import_ipynb
from Calculate import Score
from Calculate import Calculator

from Log import Logger
log = Logger('Content_Morpheme')


# In[ ]:


class Morpheme(object):
    infos = list()
    morph_num = list()

    def __init__(self, position = None): 
        if position == None:
            log.info('Get None Value')
            return
        
        self.position = position
        
        self.take_score_type()
        self.create_info()
        self.add_info()
        self.add_morph_num()
        
        Calculator.add_score_type(self.score, self.type)
        
    def take_score_type(self):
        self.score, self.type = Score(self.position).get_score_type()
    
    def create_info(self):
        self.info = 'morph : ' + self.position[0]
        self.info += '\nclass : ' + self.position[1]
        self.info += '\nscore : ' + str(self.score)
        
    def add_info(self):
        Morpheme.infos.append(self.info)
        
    def add_morph_num(self):
        find = False
        
        if len(self.morph_num) == 0:
            e = [self.position, 1]
            Morpheme.morph_num.append(e)
        else:
            for i, morph in enumerate(Morpheme.morph_num):
                if morph[0] == self.position:
                    Morpheme.morph_num[i][1] += 1
                    find = True
                    
            if not find:
                e = [self.position, 1]
                Morpheme.morph_num.append(e)
    
    @classmethod
    def get_infos(cls):
        return cls.infos
    
    @classmethod
    def get_morph_num(cls):
        return cls.morph_num
        
    @classmethod
    def clean_info(cls):
        cls.infos = list()
    
    @classmethod
    def clean_morph_num(cls):
        cls.morph_num = list()
        

