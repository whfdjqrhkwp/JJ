#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import import_ipynb

from Result_Each import Information
from Result_Each import Graph
from Result_Each import PDF
from Result_Aggregate import FindZero
from Result_Aggregate import Chart

from Content_Text import Text
from Calculate import Score

from Log import Logger
log = Logger('Interface')

import os
import re


# In[ ]:


import os
import re
import pandas as pd
import matplotlib.pyplot as pp
import seaborn as sb

class T(object):
    score_voca = list()
    score_gram = list()
    
    info = list()
    
    @classmethod
    def add(cls, obj, name):
        v = obj.get_score_voca()
        g = obj.get_score_gram()
        
        cls.score_voca.append(v)
        cls.score_gram.append(g)
        
        sentence_number = len(obj.get_sentences())
        charactor_number = len(obj.get_text())
        
        hanja = 'X'
        if 'class : OH' in obj.get_buf_info():
            hanja = 'O'
            
        e = [name, sentence_number, charactor_number, hanja]
        cls.info.append(e)
            
    @classmethod
    def run(cls):
        
        df = pd.DataFrame(cls.score_voca, columns = ['score'])
        pp.figure(figsize = (12, 4))
        pp.hist(df, bins = int(max(cls.score_voca)), rwidth = 0.5)
        pp.xlabel('vocabulary score')
        pp.ylabel('number')
        pp.savefig(os.path.join(os.getcwd(), 'Output', 'voca.png'))
        pp.show()
        
        df = pd.DataFrame(cls.score_gram, columns = ['score'])
        pp.figure(figsize = (12, 4))
        pp.hist(df, bins = int(max(cls.score_gram)), rwidth = 0.5)
        pp.xlabel('grammar score')
        pp.ylabel('number')
        pp.savefig(os.path.join(os.getcwd(), 'Output', 'gram.png'))
        pp.show()
        
        df = pd.DataFrame(cls.info)
        df.to_excel(os.path.join(os.getcwd(), 'Output', 'INFO.xlsx'), header = False, index = False)


# In[ ]:


class Input(object):

    BASE_ADDRESS = os.path.join(os.getcwd(), 'Input')
    PROCESSED = set()
    
    @classmethod
    def show_processed(cls):
        processed = list(cls.PROCESSED)
        processed.sort()
        
        print('===========================PROCESSED===========================')
        for n in processed:
            print(' - {}'.format(n))
        print('===============================================================')


# In[ ]:


def init():
    NAME = 'Korean Text Complexity Calculator'
    VERSION = 'Version {}'.format('1.4.2')
    MADE = 'Made by JJ'
    
    INFO = '\n - {}\n - {}\n - {}\n'.format(NAME, VERSION, MADE)
    print(INFO)
    
    Score.load_data()


# In[ ]:


def check_input():
    if not os.path.isdir(Input.BASE_ADDRESS):
        os.mkdir(Input.BASE_ADDRESS)
        print('Press Enter After Create Text Files in Input Directory')
        i = input()


# In[ ]:


def show_index():
    indexes = os.listdir(Input.BASE_ADDRESS)
    log.info('Get Directory & File List')
    
    for index in enumerate(indexes):
        address = os.path.join(Input.BASE_ADDRESS, index[1])
        if os.path.isdir(address):
            indexes[index[0]] = '{} {}'.format('[Directory]', index[1])
        else:
            indexes[index[0]] = '{} {}'.format('[File]', index[1])
            
    print('\n============================INDEX=============================\n')
    for index in enumerate(indexes):
        index_string = str(index[0] + 1).rjust(len(str(len(indexes))), '0')
        show = '{}. {}'.format(index_string, index[1])
        if '[File]' in index[1]: 
            print(show.replace('.txt', ''))
        else:
            print(show)
        
    return indexes


# In[ ]:


def select_index():
    indexes = show_index()
    
    show_text = '\n========================항목 번호 입력========================\n'
    show_text += '- 쉼표 구분으로 여러 번호 입력 (n1, n2, n3, ...)\n'
    show_text += '- 물결표로 구간 지정 (n1 ~ n2)\n'
    show_text += '- 디렉토리 선택 시 하위 txt 모두 읽음\n'
    show_text += '- 0 입력 시 종료\n'
    show_text += '- A 또는 a 입력 시 분포도 데이터, 0점 목록 파일 생성\n'
    show_text += '- R 또는 r 입력 시 분포도 데이터, 0점 목록 초기화\n'
    show_text += '===============================================================\n'
    show_text += 'Input : '
    
    addresses = list()
    
    select = input(show_text)
    log.info('Get Index String : {}'.format(select))
    
    if select.replace(' ', '') == '':
        return 1
    if select == '0':
        return 0
    if select.upper() == 'R':
        return 'R'
    if select.upper() == 'A':
        return 'A'
    
    if ',' in select:
        split = select.split(',')
        select = [int(e) for e in split]
    elif '~' in select:
        split = select.split('~')
        select = [e for e in range(int(split[0]), int(split[1]) + 1)]
    else:
        select = [int(select)]
    
    for index in select:
        name = indexes[int(index) - 1]
        Input.PROCESSED.add(name)
        selected = re.sub(pattern = '\[.*\]\s', repl = '', string = name)
        address = os.path.join(Input.BASE_ADDRESS, selected)
        addresses.append(address)
    
    log_buf = '\n~ '.join(addresses)
    log.info('Get Address List \n~ {}'.format(log_buf))
    
    return addresses


# In[ ]:


def read_text(address):
    if not os.path.isfile(address):
        return read_dir(address)
    
    if not '.txt' in address:
        log.info('Get Not txt File Address \n~ {}'.format(address))
        print('Error : This program is executable for txt file only')
        print('Address = {}\n'.format(address))
        return
    
    file_name = address.split('\\')[-1]
    print('Selected File : {}'.format(file_name))
    
    log.info('Open txt File Address \n~ {}'.format(address))
    text = ''
    with open(address, 'r', encoding = 'utf-8') as file:
        text = file.read()
        log.info('Read txt File Address \n~ {}'.format(address))
        
    obj = Text(text)
    obj.simple()
    
    #T.add(obj, file_name)

    Information(obj, address)
    Graph(obj, address)
    PDF(obj, address)
    
    Chart.add_data(obj, address)
    FindZero.add_data(obj)
    
    del obj
    
    print('-' * 100)
    


# In[ ]:


def read_dir(address):
    log.info('Get Directory Address \n~ {}'.format(address))
    dir_name = address.split('\\')[-1]
    files = os.listdir(address)
    addresses = list()
    
    for file in files:
        addr = os.path.join(address, file)
        addresses.append(addr)
    
    log_buf = '\n~ '.join(addresses)
    log.info('Get Subfile Address List \n~ {}'.format(log_buf))
        
    for address in enumerate(addresses):
        print('Current Directory : {} [{} / {}]'.format(dir_name, address[0] + 1, len(addresses)))
        read_text(address[1])


# In[ ]:


def read():
    while True:
        address = select_index()
        
        if address == 1:
            continue
        if address == 0:
            log.info('Break Reading')
            break
        if address == 'A':
            Input.show_processed()
            draw_chart()
            find_zero()
            Input.PROCESSED = set()
            continue
        if address == 'R':
            Chart.clean()
            FindZero.clean()
            Input.PROCESSED = set()
            log.info('Distribution Chart Data Deleted')
            print('\n... Distribution Chart Data Deleted ...\n')
            continue

        for addr in address:
            read_text(addr)


# In[ ]:


def draw_chart():
    while True:
        key = input('Draw Distribution Chart ? [y/n] : ')

        if key.upper() == 'Y':
            Chart.run()
            Chart.clean()
            return
        elif key.upper() == 'N':
            log.info('Deny Drawing Distribution Chart')
            return
        else:
            print('You can input y(Y) or n(N) only')
            continue


# In[ ]:


def find_zero():
    while True:
        key = input('Wrtie Zero Point Morphemes (txt, xlsx) ? [y/n] : ')

        if key.upper() == 'Y':
            FindZero.run()
            FindZero.clean()
            return
        elif key.upper() == 'N':
            log.info('Deny Writing Zero Point Morphemes')
            return
        else:
            print('You can input y(Y) or n(N) only')
            continue


# In[ ]:


def run():
    init()
    check_input()
    read()
    
    #T.run()


# In[ ]:




