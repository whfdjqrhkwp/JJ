#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import re
import pandas as pd
import matplotlib.pyplot as pp
import seaborn as sb

import import_ipynb
from Categorize import categorize


# In[ ]:


class FindZero(object):
    address = os.path.join(os.getcwd(), 'Output', 'Aggregate')
    
    address_txt = os.path.join(address, 'txt')
    address_xlsx = os.path.join(address, 'xlsx')
    
    zero_code = [tuple(['Adjective', 0]),
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
    
    zero_data = [set() for i in zero_code]
    
    @classmethod
    def add_data(cls, obj):
        infos = obj.get_info()
        
        for info in infos:
            if 'score : 0' in info:
                data = info.split('\n')
                morph = data[0].split(' : ')[1]
                kind = data[1].split(' : ')[1]
                
                category = categorize(kind)
                code = cls.get_code(category[0])
                if code == -1:
                    continue
                
                cls.zero_data[code].add(tuple([morph, kind]))
                
    @classmethod
    def get_code(cls, category):
        for code in cls.zero_code:
            if category == code[0]:
                return code[1]
        
        return -1
    
    @classmethod
    def get_buf_data(cls, data):
        delim = '\n{}\n'.format('-' * 50)
        
        buf = 'Total Number(s) : {}\n{}\n'.format(len(data), '=' * 50)
        for info in data:
            buf += 'Morph : {}'.format(info[0])
            buf += '\nClass : {}'.format(info[1])
            buf += delim
            
        return buf
        
    @classmethod
    def write_txt(cls):
        for data in enumerate(cls.zero_data):
            if len(data[1]) == 0:
                continue
            
            buf = cls.get_buf_data(data[1])
            name = '{}.txt'.format(cls.zero_code[data[0]][0])
            
            with open(os.path.join(cls.address_txt, name), 'w', encoding = 'utf-8') as file:
                file.write(buf)
                
    @classmethod
    def write_xlsx(cls):
        for data in enumerate(cls.zero_data):
            if len(data[1]) == 0:
                continue
                
            name = '{}.xlsx'.format(cls.zero_code[data[0]][0])
            
            df = pd.DataFrame(data[1])
            df.to_excel(os.path.join(cls.address_xlsx, name), header = False, index = False)
    
    @classmethod
    def create_dir(cls):
        if not os.path.isdir(cls.address):
            os.mkdir(cls.address)
            
        if not os.path.isdir(cls.address_txt):
            os.mkdir(cls.address_txt)
        
        if not os.path.isdir(cls.address_xlsx):
            os.mkdir(cls.address_xlsx)
            
    @classmethod
    def run(cls):
        cls.create_dir()
        cls.write_txt()
        cls.write_xlsx()
        
        print('Complete : FindZero\n')


# In[ ]:


class Chart(object):
    address = os.path.join(os.getcwd(), 'Output', 'Aggregate')
    
    data_score = list()
    data_zero_voca = list()
    data_zero_gram = list()
    
    num_kind = list([['Output', 0]])

    chart_score = list()
    chart_voca = list()
    chart_gram = list()
    
    
    @classmethod
    def add_data(cls, obj, address):
        score = obj.get_score()
        
        total_voca = sum(obj.get_scores_voca())
        total_gram = sum(obj.get_scores_gram())
        
        if total_voca == 0:
            total_voca = 1
        if total_gram == 0:
            total_gram = 1
        
        zero_voca = obj.get_scores_voca()[0] / total_voca
        zero_gram = obj.get_scores_gram()[0] / total_gram
        
        kind = address.split('\\')[-2]
        if kind == 'Output':
            kind = 'Unclassified'
        
        score = [kind, score]
        voca = [kind, zero_voca]
        gram = [kind, zero_gram]
        
        cls.data_score.append(score)
        cls.data_zero_voca.append(voca)
        cls.data_zero_gram.append(gram)
        
        already = False
        
        for _kind in enumerate(cls.num_kind):
            if kind == _kind[1][0]:
                cls.num_kind[_kind[0]][1] += 1
                already = True
        
        if not already:
            cls.num_kind.append([kind, 1])
            
    @classmethod
    def sort_num_kind(cls):
        cls.num_kind.sort(key = lambda num : (-num[1], num[0]))
        cls.num_kind.remove(['Output', 0])
        
    @classmethod
    def classify(cls):
        kinds = len(cls.num_kind) # [['A', 10], ['B', 6], ['C', 3]]
        
        bit_score = list()
        bit_voca = list()
        bit_gram = list()

        while not cls.num_kind[0][1] == 0:
            for kind in enumerate(cls.num_kind):
                if not kind[1][1] == 0:
                    for score in enumerate(cls.data_score):
                        if kind[1][0] == score[1][0]:
                            bit_score.append(score[1][1])
                            bit_voca.append(cls.data_zero_voca[score[0]][1])
                            bit_gram.append(cls.data_zero_gram[score[0]][1])
                            
                            del cls.data_score[score[0]]
                            del cls.data_zero_voca[score[0]]
                            del cls.data_zero_gram[score[0]]
                            
                            break
                            
                    cls.num_kind[kind[0]][1] -= 1
                    
            cls.chart_score.append(bit_score)
            cls.chart_voca.append(bit_voca)
            cls.chart_gram.append(bit_gram)
            
            bit_score = list()
            bit_voca = list()
            bit_gram = list()
            
    @classmethod
    def create_dir(cls):
        if not os.path.isdir(cls.address):
            os.mkdir(cls.address)
            
    @classmethod
    def draw_chart(cls):
        column = [kind[0] for kind in cls.num_kind]
        
        df_score = pd.DataFrame(cls.chart_score, columns = column)
        df_voca = pd.DataFrame(cls.chart_voca, columns = column)
        df_gram = pd.DataFrame(cls.chart_gram, columns = column)
        
        pp.figure(figsize = (12, 4))
        pp.title('Distribution chart : Average score')
        sb.swarmplot(data = df_score)
        pp.savefig(os.path.join(cls.address, 'img_average_score.png'))
        pp.show()

        pp.figure(figsize = (12, 4))
        pp.title('Distribution chart : Vocabulary zero ratio')
        sb.swarmplot(data = df_voca)
        pp.savefig(os.path.join(cls.address, 'img_voca_zero_ratio.png'))
        pp.show()

        pp.figure(figsize = (12, 4))
        pp.title('Distribution chart : Grammar zero ratio')
        sb.swarmplot(data = df_gram)
        pp.savefig(os.path.join(cls.address, 'img_gram_zero_ratio.png'))
        pp.show()
        
    @classmethod
    def clean(cls):
        cls.data_score = list()
        cls.data_zero_voca = list()
        cls.data_zero_gram = list()

        cls.num_kind = list([['Unclassified', 0]])

        cls.chart_score = list()
        cls.chart_voca = list()
        cls.chart_gram = list()
            
    @classmethod
    def run(cls):
        cls.sort_num_kind()
        cls.classify()
        cls.create_dir()
        cls.draw_chart()
        
        print('Complete : Chart\n')

