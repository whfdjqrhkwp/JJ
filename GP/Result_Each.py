#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re
import pandas as pd
import matplotlib.pyplot as pp
import seaborn as sb


# In[ ]:


class Information(object):
    
    @classmethod
    def __init__(cls, obj, address):
        cls.obj = obj
        cls.title = address.split('\\')[-1]
        cls.dir_address = get_result_address(address)
        
        cls.write_result_txt()
        cls.write_info_each()
    
    @classmethod
    def write_result_txt(cls):
        #with open(os.path.join(cls.dir_address, 'info_all.txt'), 'w', encoding = 'utf-8') as file:
        #    file.write(cls.obj.get_buf_info())
        
        with open(os.path.join(cls.dir_address, 'info_zero.txt'), 'w', encoding = 'utf-8') as file:
            file.write(cls.obj.get_buf_info_zero())
        
        with open(os.path.join(cls.dir_address, 'info_UN.txt'), 'w', encoding = 'utf-8') as file:
            file.write(cls.obj.get_buf_info_UN())
            
        with open(os.path.join(cls.dir_address, 'info_XR_zero.txt'), 'w', encoding = 'utf-8') as file:
            file.write(cls.obj.get_buf_info_XR_zero())
        
        with open(os.path.join(cls.dir_address, 'scores_sentence.txt'), 'w', encoding = 'utf-8') as file:
            file.write(cls.obj.get_buf_scores_sentence())
        
        with open(os.path.join(cls.dir_address, 'summary.txt'), 'w', encoding = 'utf-8') as file:
            buf = 'File name : {}\n'.format(cls.title)
            buf += cls.obj.get_buf_summary()
            file.write(buf)
            
        
    @classmethod
    def write_info_each(cls):
        address = os.path.join(cls.dir_address, 'info_each')
        if not os.path.isdir(address):
            os.mkdir(address)
            
        info_each = cls.obj.get_info_each()
        name = '{}.txt'
        delim = '\n{}\n'.format('-' * 50)
        
        for info in enumerate(info_each):
            with open(os.path.join(address, name.format(str(info[0] + 1))), 'w', encoding = ' utf-8') as file:
                buf = delim.join(info[1])
                file.write(buf)
        


# In[ ]:


class Graph(object):
    rate_label = ['{}p'.format(i + 1) for i in range(6)]
    rate_color = ['#DCDCDC', '#90EE90', '#7FFFD4', '#FFD700', '#FF6347', '#EE82EE']
    rate_wedgeprops = {'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}
    
    @classmethod
    def __init__(cls, obj, address):
        cls.obj = obj
        cls.dir_address = get_result_address(address)
        
        cls.draw_score()
        cls.draw_density()
        cls.draw_rate_voca()
        cls.draw_rate_gram()
        
    @classmethod
    def draw_score(cls):
        df = pd.DataFrame(cls.obj.get_scores_sentence())
        
        pp.figure(figsize = (12, 4))
        pp.title('Score of sentences')
        pp.plot(df)
        pp.xlabel('sentence')
        pp.ylabel('score')
        pp.savefig(os.path.join(cls.dir_address, 'img_score.png'))
        pp.show()
        
    @classmethod
    def draw_density(cls):
        df = pd.DataFrame(cls.obj.get_scores_sentence(), columns = ['score'])
        
        pp.figure(figsize = (12, 4))
        pp.title('Density of scores')
        sb.kdeplot(df['score'])
        pp.savefig(os.path.join(cls.dir_address, 'img_density.png'))
        pp.show()
        
    @classmethod
    def draw_rate_voca(cls):
        voca_num = cls.obj.get_scores_voca()
        del voca_num[0]
    
        total_num = sum(voca_num)
        if total_num == 0:
            print('Vocabulary score ratio : All data are zero')
            return
 
        data = [round(num / total_num, 2) for num in voca_num]
       
        pp.figure(figsize = (6, 6))
        pp.title('Vocabulary score ratio')
        pp.pie(data, labels = cls.rate_label, autopct = '%.2f%%', colors = cls.rate_color , wedgeprops = cls.rate_wedgeprops, normalize = True)
        pp.savefig(os.path.join(cls.dir_address, 'img_rate_voca.png'))
        pp.show()
        
    @classmethod
    def draw_rate_gram(cls):
        gram_num = cls.obj.get_scores_gram()
        del gram_num[0]
     
        total_num = sum(gram_num)
        if total_num == 0:
            print('Grammar score ratio : All data are zero')
            return
 
        data = [round(num / total_num, 2) for num in gram_num]
    
        pp.figure(figsize = (6, 6))
        pp.title('Grammar score ratio')
        pp.pie(data, labels = cls.rate_label, autopct = '%.2f%%', colors = cls.rate_color , wedgeprops = cls.rate_wedgeprops, normalize = True)
        pp.savefig(os.path.join(cls.dir_address, 'img_rate_gram.png'))
        pp.show()
        


# In[ ]:


def get_result_address(address):
    
    def create_result_dir():
        address = os.path.join(os.getcwd(), 'Output')
        if not os.path.isdir(address):
            os.mkdir(address)
    
    def create_output_address(address, parent):
        if not parent:
            address = re.sub(pattern = r'\\[^\\]*.txt', repl = '', string = address)

        address = address.replace('.txt', '') 

        additional = address.replace(os.getcwd(), '')[1:]
        additional = additional.replace('Input', 'Output')

        result_address = os.path.join(os.getcwd(), additional)

        return result_address
    
    def create_output_dir(address):
        if not address.split('\\')[-2] == 'Input':
            addr = create_output_address(address, False)
            if not os.path.isdir(addr):
                os.mkdir(addr)

        dir_address = create_output_address(address, True)

        if not os.path.isdir(dir_address):
            os.mkdir(dir_address)

        return dir_address
    
    create_result_dir()
    address = create_output_dir(address)
    
    return address

