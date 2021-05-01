#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import import_ipynb
from Calculate import Score
from Calculate import Calculator


# In[ ]:


class Morpheme(object):
    infos = list()

    def __init__(self, position = None): # ('사람', 'NNG')
        if position == None:
            return

        self.position = position
        
        self.take_score_type()
        self.create_info()
        self.add_info()
        
        Calculator.add_score_type(self.score, self.type)
        
    def take_score_type(self):
        self.score, self.type = Score(self.position).get_score_type() # 1, voca
    
    def create_info(self):
        self.info = 'morph : ' + self.position[0]
        self.info += '\nclass : ' + self.position[1]
        self.info += '\nscore : ' + str(self.score)
        
    def add_info(self):
        Morpheme.infos.append(self.info)
    
    @classmethod
    def get_infos(cls):
        return cls.infos
        
    @classmethod
    def clean(cls):
        cls.infos = list()
        

