#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import re
import pandas as pd
import matplotlib.pyplot as pp
import seaborn as sb

#pp.switch_backend('agg')

import import_ipynb
from Categorize import categorize

from Log import Logger
log = Logger('Result_Aggregate')


# In[ ]:


class FindZero(object):
    address = os.path.join(os.getcwd(), 'Output', '_Aggregate')
    
    address_txt = os.path.join(address, 'Zero_txt')
    address_xlsx = os.path.join(address, 'Zero_xlsx')
    
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
        log.info('Start Adding Zero Point Morphemes')
        infos = obj.get_info()
        
        for info in infos:
            if 'score : 0' in info:
                data = info.split('\n')
                morph = data[0].split(' : ')[1]
                kind = data[1].split(' : ')[1]
                
                if kind == 'UN':
                    continue
                
                category = categorize(kind)
                code = cls.get_code(category[0])
                
                if code == -1:
                    continue
                
                cls.zero_data[code].add(tuple([morph, kind]))
                
        log.info('Complete Adding Zero Point Morphemes')
                
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
    def clean(cls):
        cls.zero_data = [set() for i in cls.zero_code]
            
    @classmethod
    def run(cls):
        log.info('Start Writing Zero Point Morphemes File')
        cls.create_dir()
        cls.write_txt()
        cls.write_xlsx()
        
        log.info('Complete Writing Zero Point Morphemes File')
        print('Complete : FindZero\n')


# In[ ]:


class Chart(object):
    address = os.path.join(os.getcwd(), 'Output', '_Aggregate')
    
    data_score = list()
    data_score_voca = list()
    data_score_gram = list()
    data_zero_voca = list()
    data_zero_gram = list()
    
    num_kind = list([['Input', 0]])

    chart_score = list()
    chart_score_voca = list()
    chart_score_gram = list()
    chart_zero_voca = list()
    chart_zero_gram = list()
    
    isjupyter = True
    
    
    @classmethod
    def add_data(cls, obj, address):
        log.info('Start Adding Text Score For Distribution Chart')
        score = obj.get_score()
        score_voca = obj.get_score_voca()
        score_gram = obj.get_score_gram()
        
        total_voca = sum(obj.get_scores_voca_num())
        total_gram = sum(obj.get_scores_gram_num())
        
        if total_voca == 0:
            total_voca = 1
        if total_gram == 0:
            total_gram = 1
        
        zero_voca = obj.get_scores_voca_num()[0] / total_voca
        zero_gram = obj.get_scores_gram_num()[0] / total_gram
        
        kind = address.split('\\')[-2]
        if kind == 'Input':
            kind = 'Unclassified'
        
        score = [kind, score]
        score_voca = [kind, score_voca]
        score_gram = [kind, score_gram]
        zero_voca = [kind, zero_voca]
        zero_gram = [kind, zero_gram]
        
        cls.data_score.append(score)
        cls.data_score_voca.append(score_voca)
        cls.data_score_gram.append(score_gram)
        cls.data_zero_voca.append(zero_voca)
        cls.data_zero_gram.append(zero_gram)
        
        already = False
        
        for _kind in enumerate(cls.num_kind):
            if kind == _kind[1][0]:
                cls.num_kind[_kind[0]][1] += 1
                already = True
        
        if not already:
            cls.num_kind.append([kind, 1])
        
        log.info('Complete Adding Text Score For Distribution Chart')
            
    @classmethod
    def sort_num_kind(cls):
        cls.num_kind.sort(key = lambda num : (-num[1], num[0]))
        cls.num_kind.remove(['Input', 0])
        
    @classmethod
    def classify(cls):
        kinds = len(cls.num_kind)
        
        bit_score = list()
        bit_score_voca = list()
        bit_score_gram = list()
        bit_zero_voca = list()
        bit_zero_gram = list()

        while not cls.num_kind[0][1] == 0:
            for kind in enumerate(cls.num_kind):
                if not kind[1][1] == 0:
                    for score in enumerate(cls.data_score):
                        if kind[1][0] == score[1][0]:
                            bit_score.append(score[1][1])
                            bit_score_voca.append(cls.data_score_voca[score[0]][1])
                            bit_score_gram.append(cls.data_score_gram[score[0]][1])
                            bit_zero_voca.append(cls.data_zero_voca[score[0]][1])
                            bit_zero_gram.append(cls.data_zero_gram[score[0]][1])
                            
                            del cls.data_score[score[0]]
                            del cls.data_score_voca[score[0]]
                            del cls.data_score_gram[score[0]]
                            del cls.data_zero_voca[score[0]]
                            del cls.data_zero_gram[score[0]]
                            
                            break
                            
                    cls.num_kind[kind[0]][1] -= 1
                    
            cls.chart_score.append(bit_score)
            cls.chart_score_voca.append(bit_score_voca)
            cls.chart_score_gram.append(bit_score_gram)
            cls.chart_zero_voca.append(bit_zero_voca)
            cls.chart_zero_gram.append(bit_zero_gram)
            
            bit_score = list()
            bit_score_voca = list()
            bit_score_gram = list()
            bit_zero_voca = list()
            bit_zero_gram = list()
            
    @classmethod
    def create_dir(cls):
        if not os.path.isdir(cls.address):
            os.mkdir(cls.address)
            
    @classmethod
    def draw_chart(cls):
        column = [kind[0] for kind in cls.num_kind]
        
        df_score = pd.DataFrame(cls.chart_score, columns = column)
        df_score_voca = pd.DataFrame(cls.chart_score_voca, columns = column)
        df_score_gram = pd.DataFrame(cls.chart_score_gram, columns = column)
        df_zero_voca = pd.DataFrame(cls.chart_zero_voca, columns = column)
        df_zero_gram = pd.DataFrame(cls.chart_zero_gram, columns = column)
        
        fig = pp.figure(figsize = (12, 4))
        pp.title('Distribution chart : Average score')
        sb.swarmplot(data = df_score)
        pp.savefig(os.path.join(cls.address, 'img_average_score.png'))
        
        if cls.isjupyter:
            pp.show()
        pp.close(fig)
        
        fig = pp.figure(figsize = (12, 4))
        pp.title('Distribution chart : Average vocabulary score')
        sb.swarmplot(data = df_score_voca)
        pp.savefig(os.path.join(cls.address, 'img_average_score_voca.png'))
        
        if cls.isjupyter:
            pp.show()
        pp.close(fig)
        
        fig = pp.figure(figsize = (12, 4))
        pp.title('Distribution chart : Average grammar score')
        sb.swarmplot(data = df_score_gram)
        pp.savefig(os.path.join(cls.address, 'img_average_score_gram.png'))
        
        if cls.isjupyter:
            pp.show()
        pp.close(fig)

        fig = pp.figure(figsize = (12, 4))
        pp.title('Distribution chart : Vocabulary zero ratio')
        sb.swarmplot(data = df_zero_voca)
        pp.savefig(os.path.join(cls.address, 'img_voca_zero_ratio.png'))
        
        if cls.isjupyter:
            pp.show()
        pp.close(fig)

        fig = pp.figure(figsize = (12, 4))
        pp.title('Distribution chart : Grammar zero ratio')
        sb.swarmplot(data = df_zero_gram)
        pp.savefig(os.path.join(cls.address, 'img_gram_zero_ratio.png'))
        
        if cls.isjupyter:
            pp.show()
        pp.close(fig)
        
    @classmethod
    def clean(cls):
        cls.data_score = list()
        cls.data_score_voca = list()
        cls.data_score_gram = list()
        cls.data_zero_voca = list()
        cls.data_zero_gram = list()

        cls.num_kind = list([['Unclassified', 0]])

        cls.chart_score = list()
        cls.chart_score_voca = list()
        cls.chart_score_gram = list()
        cls.chart_zero_voca = list()
        cls.chart_zero_gram = list()
            
    @classmethod
    def run(cls):
        log.info('Start Drawing Distribution Chart')
        cls.sort_num_kind()
        cls.classify()
        cls.create_dir()
        cls.draw_chart()
        
        log.info('Complete Drawing Distribution Chart')
        print('Complete : Chart\n')

