#!/usr/bin/env python
# coding: utf-8

# In[2]:


import konlpy
from konlpy.tag import Kkma

import import_ipynb
from Content_Sentence import Sentence
from Content_Morpheme import Morpheme
from Calculate import Calculator

from Log import Logger
log = Logger('Content_Text')


# In[3]:


class Text(object):
    kk = Kkma()
    
    def __init__(self, text = ''):
        self.text = text
        self.length = len(text)
        self.analysis()
        
    def analysis(self):
        log.info('Start Getting Sentences')
        self.sentences = Text.kk.sentences(self.text)
        log.info('Complete Getting {} Sentences'.format(len(self.sentences)))

        log.info('Start Analyzing Sentences')
        count = 0
        for sentence in enumerate(self.sentences):
            Sentence(sentence[1])
            count += 1
            notice = 'Completed ... [{} / {}]'.format(sentence[0] + 1, len(self.sentences))
            print(notice, end = '\r')
            
        log.info('Complete Analyzing {} Sentences'.format(count))
        print()
        
        self.scores_voca_num, self.scores_gram_num = Calculator.get_text_score()
        Calculator.clean_text_score()
        
        self.scores_sentence = Sentence.get_scores()
        self.scores_voca_sentence = Sentence.get_scores_voca()
        self.scores_gram_sentence = Sentence.get_scores_gram()
        
        self.score_and_sentence = list()
        for index, score in enumerate(self.scores_sentence):
            e = (score, self.sentences[index])
            self.score_and_sentence.append(e)
        
        self.score = round(sum(self.scores_sentence) / len(self.scores_sentence), 2)
        self.score_voca = round(sum(self.scores_voca_sentence) / len(self.scores_voca_sentence), 2)
        self.score_gram = round(sum(self.scores_gram_sentence) / len(self.scores_gram_sentence), 2)
        
        deviation_power = [pow(score - self.score, 2) for score in self.scores_sentence]
        variance = sum(deviation_power) / len(deviation_power)
        self.standard_deviation = round(pow(variance, 0.5), 2)
       
        self.info = Sentence.get_infos()
        self.info_each = Sentence.get_infos_each()
        
        self.morph_num = Morpheme.get_morph_num()
        self.morph_num.sort(key = lambda num : (-num[1], num[0][0]))
        
        Sentence.clean()
        Morpheme.clean_morph_num()
        
        log.info('Text Analysis Complete')
        
    def simple(self):
        buf = 'Average Score : {}'.format(self.score)
        buf += '\n - Maximum Score : {}'.format(max(self.scores_sentence))
        buf += '\n - Minimum Score : {}'.format(min(self.scores_sentence))
        buf += '\nStandard Deviation : {}'.format(self.standard_deviation)
        buf += '\n'
        buf += '\nAverage Vocabulary Score : {}'.format(self.score_voca)
        buf += '\nAverage Grammar Score : {}'.format(self.score_gram)
        
        print('\n{}\n'.format(buf))
        
    def get_buf_info(self):
        delim = '\n{}\n'.format('-' * 50)
        
        buf = 'Total number : {}\n{}\n'.format(len(self.info), '=' * 50)
        buf += delim.join(self.info)
        
        return buf
    
    def get_buf_info_zero(self):
        delim = '\n{}\n'.format('-' * 50)
        info = list()
        
        for e in self.info:
            if 'score : 0' in e:
                info.append(e)
        info = set(info)
        
        buf = 'Total number : {}\n{}\n'.format(len(info), '=' * 50)
        buf += delim.join(info)
        
        return buf
    
    def get_buf_info_UN(self):
        delim = '\n{}\n'.format('-' * 50)
        info = list()
        
        for e in self.info:
            if 'class : UN' in e:
                info.append(e)
        info = set(info)
        
        buf = 'Total number : {}\n{}\n'.format(len(info), '=' * 50)
        buf += delim.join(info)
        
        return buf
    
    def get_buf_info_XR_zero(self):
        delim = '\n{}\n'.format('-' * 50)
        info = list()
        
        for e in self.info:
            if 'class : XR' in e and 'score : 0' in e:
                info.append(e)
        info = set(info)
        
        buf = 'Total number : {}\n{}\n'.format(len(info), '=' * 50)
        buf += delim.join(info)
        
        return buf
    
    
    def get_buf_scores_sentence(self):
        delim = '\n{}\n'.format('-' * 50)
        scores_sentence = list()
        for score in enumerate(self.scores_sentence):
            add = 'Number : {}'.format(score[0] + 1)
            add += '\nScore : {}'.format(score[1])
            add += '\n{}'.format(self.sentences[score[0]])
            scores_sentence.append(add)
        
        buf = 'Total number : {}\n{}\n'.format(len(self.sentences), '=' * 50)
        buf += delim.join(scores_sentence)
        
        return buf
    
    def get_buf_morph_num(self):
        delim = '\n{}\n'.format('-' * 50)
        morph_num = list()
        for morph in self.morph_num:
            add = 'Morph : {}'.format(morph[0][0])
            add += '\nClass : {}'.format(morph[0][1])
            add += '\nNumber : {}'.format(morph[1])
            morph_num.append(add)
        
        buf = 'Total number : {}\n{}\n'.format(len(self.morph_num), '=' * 50)
        buf += delim.join(morph_num)
        
        return buf
    
    def get_buf_summary(self):
        buf = 'Sentences Number : {}'.format(len(self.sentences))
        buf += '\nCharacters Number : {}'.format(self.length)
        buf += '\nAverage Score : {}'.format(self.score)
        buf += '\n - Maximum Score : {}'.format(max(self.scores_sentence))
        buf += '\n - Minimum Score : {}'.format(min(self.scores_sentence))
        buf += '\nStandard Deviation : {}'.format(self.standard_deviation)
        buf += '\n'
        buf += '\nAverage Vocabulary Score : {}'.format(self.score_voca)
        buf += '\nAverage Grammar Score : {}'.format(self.score_gram)
        buf += '\nVocabulary score number : {}'.format(self.scores_voca_num)
        buf += '\nGrammar score number : {}'.format(self.scores_gram_num)
        
        return buf
    
    def get_lenght(self):
        return self.length
    
    def get_morph_num(self):
        return self.morph_num
        
    def get_info(self):
        return self.info
    
    def get_info_each(self):
        return self.info_each
    
    def get_text(self):
        return self.text
    
    def get_sentences(self):
        return self.sentences
    
    def get_score(self):
        return self.score
    
    def get_score_voca(self):
        return self.score_voca
    
    def get_score_gram(self):
        return self.score_gram
    
    def get_standard_deviation(self):
        return self.standard_deviation
    
    def get_score_and_sentence(self):
        return self.score_and_sentence
    
    def get_scores_sentence(self):
        return self.scores_sentence
    
    def get_scores_voca_sentence(self):
        return self.scores_voca_sentence
    
    def get_scores_gram_sentence(self):
        return self.scores_gram_sentence
    
    def get_scores_voca_num(self):
        return self.scores_voca_num
    
    def get_scores_gram_num(self):
        return self.scores_gram_num


# In[ ]:




