#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import import_ipynb
from Categorize import categorize

from Log import Logger
log = Logger('Calculate')

import os
import sys
import pandas as pd


# In[ ]:


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)


# In[ ]:


class Score(object):
    data_dir = 'Data'
    data_set = list()
    data_code = [tuple(['Adjective', 0]),
                tuple(['Adverb', 1]),
                tuple(['Affix', 2]),
                tuple(['BoundNoun', 3]),
                tuple(['ConnectEnding', 4]),
                tuple(['Determiner', 5]),
                tuple(['FinalEnding', 6]),
                tuple(['Interjection', 7]),
                tuple(['Noun', 8]),
                tuple(['Numeral', 9]),
                tuple(['Postposition', 10]),
                tuple(['PreFinalEnding', 11]),
                tuple(['Pronoun', 12]),
                tuple(['TransEnding', 13]),
                tuple(['Verb', 14]),
                tuple(['Root', 15])]
    
    loaded = False
    
    def __init__(self, morph = None):
        if morph == None:
            return
        
        self.word = morph[0]
        self.form, self.type = categorize(morph[1])
        
        self.get_score_type()
    
    def get_code(self, form):
        for code in Score.data_code:
            if form == code[0]:
                return code[1]
        return -1
        
    def get_score_type(self):
        code = self.get_code(self.form)
        self.score = 0
        
        for data in Score.data_set[code]:
            if self.form in ['Adjective', 'Verb']:
                if data[1] == self.word + '다':
                    self.score = data[0]
                    return data[0], self.type
            else:
                if data[1] == self.word:
                    self.score = data[0]
                    return data[0], self.type
        return 0, self.type
    
    @classmethod
    def load_data(cls):
        if cls.loaded:
            return
        
        file_form = 'Data_{}.xlsx'
        print('... Load data ...', end = '\r')
        
        for code in cls.data_code:
            log.info('Start Loading {}.xlsx'.format(code[0]))
            print('... Load data ... {}{}'.format(code[0], ' ' * 10), end = '\r')
            
            relative_file_address = os.path.join('Data', file_form.format(code[0]))
            file_address = resource_path(relative_file_address)
    
            df = pd.read_excel(file_address, header = None)
            data_list = df.values.tolist()
            
            cls.data_set.append(data_list)
            
            log.info('Complete Loading {}.xlsx'.format(code[0]))
        
        cls.loaded = True
        print('... Load data ... Done{}'.format(' ' * 10))


# In[ ]:


class Calculator(object):
    Grade = 7
    
    GRADE_WEIGHT = 0.28
    GRADE_POWER = 2.0
    TOTAL_WEIGHT = 30
    VOCA_WEIGHT = 1.43
    GRAM_WEIGHT = 1.57
    VOCA_CORRECTION = 6.8
    GRAM_CORRECTION = 5.2
    
    sentence_score_voca = list([0] * Grade)
    sentence_score_gram = list([0] * Grade)
    
    text_score_voca = list([0] * Grade)
    text_score_gram = list([0] * Grade)
    
    
    @classmethod
    def add_score_type(cls, score, _type):
        if _type == 'voca':
            cls.sentence_score_voca[score] += 1
            cls.text_score_voca[score] += 1
        if _type == 'gram':
            cls.sentence_score_gram[score] += 1
            cls.text_score_gram[score] += 1
    
    @classmethod
    def calculate_sentence_score(cls):
        num_voca = sum(cls.sentence_score_voca) - cls.sentence_score_voca[0]
        num_gram = sum(cls.sentence_score_gram) - cls.sentence_score_gram[0]
        
        if num_voca == 0:
            num_voca = 1
        if num_gram == 0:
            num_gram = 1
        
        score_voca = 0
        score_gram = 0
        
        for i in range(cls.Grade):
            weight = cls.TOTAL_WEIGHT * pow(i * cls.GRADE_WEIGHT, cls.GRADE_POWER)
            score_voca += (cls.sentence_score_voca[i] / (num_voca + cls.VOCA_CORRECTION)) * weight
            score_gram += (cls.sentence_score_gram[i] / (num_gram + cls.GRAM_CORRECTION)) * weight
        
        score = round(cls.VOCA_WEIGHT * score_voca + cls.GRAM_WEIGHT * score_gram, 2)
        
        #log.info('Get Sentence Score')
        return score, score_voca, score_gram
    
    @classmethod
    def get_text_score(cls):
        return cls.text_score_voca, cls.text_score_gram
    
    @classmethod
    def clean_sentence_score(cls):
        cls.sentence_score_voca = list([0] * cls.Grade)
        cls.sentence_score_gram = list([0] * cls.Grade)
        
    @classmethod
    def clean_text_score(cls):
        cls.text_score_voca = list([0] * cls.Grade)
        cls.text_score_gram = list([0] * cls.Grade)
        


# In[ ]:


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)

