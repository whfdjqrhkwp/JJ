#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import import_ipynb

from Result_Each import Information
from Result_Aggregate import FindZero
from Result_Each import Graph
from Result_Aggregate import Chart

from Content_Text import Text
from Calculate import Score

import os
import re


# In[ ]:


base_address = os.path.join(os.getcwd(), 'Input')


# In[ ]:


def init():
    Score.load_data()


# In[ ]:


def show_index():
    indexes = os.listdir(base_address)
    for index in enumerate(indexes):
        address = os.path.join(base_address, index[1])
        if os.path.isdir(address):
            indexes[index[0]] = '{} {}'.format('[Directory]', index[1])
        else:
            indexes[index[0]] = '{} {}'.format('[File]', index[1])
            
    print('\n============================Index=============================\n')
    for index in enumerate(indexes):
        show = '{}. {}'.format(index[0] + 1, index[1])
        if '[File]' in index[1]: 
            print(show.replace('.txt', ''))
        else:
            print(show)
        
    return indexes


# In[ ]:


def select_index():
    indexes = show_index()
    
    show_text = '\n========================항목 번호 입력=========================\n'
    show_text += '- 쉼표 구분으로 여러 번호 입력 (n1, n2, n3, ...)\n'
    show_text += '- 물결표로 구간 지정 (n1 ~ n2)\n'
    show_text += '- 디렉토리 선택 시 하위 txt 모두 읽음\n'
    show_text += '- 0 입력 시 종료\n'
    show_text += '- R 또는 r 입력 시 분포도 데이터 초기화\n'
    show_text += '===============================================================\n'
    show_text += 'Input : '
    
    addresses = list()
    
    select = input(show_text)
    
    if select == '0':
        return 0
    if select.upper() == 'R':
        return 'R'
    
    if ',' in select:
        split = select.split(',')
        select = [int(e) for e in split]
    if '~' in select:
        split = select.split('~')
        select = [e for e in range(int(split[0]), int(split[1]) + 1)]
    
    for index in select:
        selected = re.sub(pattern = '\[.*\]\s', repl = '', string = indexes[int(index) - 1])
        address = os.path.join(base_address, selected)
        addresses.append(address)
        
    return addresses


# In[ ]:


def read_text(address):
    if not os.path.isfile(address):
        return read_dir(address)
    
    if not '.txt' in address:
        print('Error : This program is executable for txt file only')
        print('Address = {}\n'.format(address))
        return
    
    file_name = address.split('\\')[-1]
    print('Selected file : {}'.format(file_name))
    
    text = ''
    with open(address, 'r', encoding = 'utf-8') as file:
        text = file.read()
        
    obj = Text(text)
    obj.simple()
    
    Information(obj, address)
    Graph(obj, address)
    
    Chart.add_data(obj, address)
    FindZero.add_data(obj)
    
    del obj
    
    print('-' * 100)
    


# In[ ]:


def read_dir(address):
    dir_name = address.split('\\')[-1]
    files = os.listdir(address)
    addresses = list()
    
    for file in files:
        addr = os.path.join(address, file)
        addresses.append(addr)
        
    for address in enumerate(addresses):
        print('Current directory : {} [{} / {}]'.format(dir_name, address[0] + 1, len(addresses)))
        read_text(address[1])


# In[ ]:


def read():
    while True:
        address = select_index()
        if address == 0:
            break
        if address == 'R':
            Chart.clean()
            print('\n... Distribution chart data deleted ...\n')
            continue

        for addr in address:
            read_text(addr)


# In[ ]:


def draw_chart():
    while True:
        key = input('Create distribution chart ? [y/n] : ')

        if key.upper() == 'Y':
            Chart.run()
            return
        elif key.upper() == 'N':
            return
        else:
            print('You can input y(Y) or n(N) only')
            continue


# In[ ]:


def find_zero():
    while True:
        key = input('Wrtie zero point morphemes (txt, xlsx) ? [y/n] : ')

        if key.upper() == 'Y':
            FindZero.run()
            return
        elif key.upper() == 'N':
            return
        else:
            print('You can input y(Y) or n(N) only')
            continue


# In[ ]:


def run():
    init()
    read()
    draw_chart()
    find_zero()


# In[ ]:




