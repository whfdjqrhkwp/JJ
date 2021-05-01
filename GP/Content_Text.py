#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import konlpy
from konlpy.tag import Kkma

import import_ipynb
from Content_Sentence import Sentence
from Calculate import Calculator


# In[ ]:


class Text(object):
    kk = Kkma()
    
    def __init__(self, text = ''):
        self.text = text
        self.analysis()
        
    def analysis(self):
        self.sentences = Text.kk.sentences(self.text)
        
        for sentence in enumerate(self.sentences):
            Sentence(sentence[1])
            notice = 'Completed ... [{} / {}]'.format(sentence[0] + 1, len(self.sentences))
            print(notice, end = '\r')

        print()
        
        self.scores_voca, self.scores_gram = Calculator.get_text_score()
        Calculator.clean_text_score()
        
        self.scores_sentence = Sentence.get_scores()
        self.score = round(sum(self.scores_sentence) / len(self.scores_sentence), 2)
        
        self.info = Sentence.get_infos()
        self.info_each = Sentence.get_infos_each()
        
        Sentence.clean()
        
    def simple(self):
        buf = 'Average Score : {}'.format(str(self.score))
        buf += '\nMaximum Score : {}'.format(str(max(self.scores_sentence)))
        buf += '\nMinimum Score : {}'.format(str(min(self.scores_sentence)))
        
        print('\n{}\n'.format(buf))
        
    def get_buf_info(self):
        delim = '\n{}\n'.format('-' * 50)
        
        buf = 'Total number(s) : {}\n{}\n'.format(len(self.info), '=' * 50)
        buf += delim.join(self.info)
        
        return buf
    
    def get_buf_info_zero(self):
        delim = '\n{}\n'.format('-' * 50)
        info = list()
        
        for e in self.info:
            if 'score : 0' in e:
                info.append(e)
        info = set(info)
        
        buf = 'Total number(s) : {}\n{}\n'.format(len(info), '=' * 50)
        buf += delim.join(info)
        
        return buf
    
    def get_buf_info_UN(self):
        delim = '\n{}\n'.format('-' * 50)
        info = list()
        
        for e in self.info:
            if 'class : UN' in e:
                info.append(e)
        info = set(info)
        
        buf = 'Total number(s) : {}\n{}\n'.format(len(info), '=' * 50)
        buf += delim.join(info)
        
        return buf
    
    def get_buf_info_XR_zero(self):
        delim = '\n{}\n'.format('-' * 50)
        info = list()
        
        for e in self.info:
            if 'class : XR' in e and 'score : 0' in e:
                info.append(e)
        info = set(info)
        
        buf = 'Total number(s) : {}\n{}\n'.format(len(info), '=' * 50)
        buf += delim.join(info)
        
        return buf
    
    
    def get_buf_scores_sentence(self):
        delim = '\n{}\n'.format('-' * 50)
        scores_sentence = list()
        for score in enumerate(self.scores_sentence):
            add = 'Number : {}'.format(str(score[0] + 1))
            add += '\nScore : {}'.format(score[1])
            add += '\n{}'.format(self.sentences[score[0]])
            scores_sentence.append(add)
        
        buf = 'Total number(s) : {}\n{}\n'.format(len(self.sentences), '=' * 50)
        buf += delim.join(scores_sentence)
        
        return buf
    
    def get_buf_summary(self):
        buf = 'Sentences number : {}'.format(len(self.sentences))
        buf += '\nAverage Score : {}'.format(self.score)
        buf += '\nVocabulary score number : {}'.format(self.scores_voca)
        buf += '\nGrammar score number : {}'.format(self.scores_gram)
        
        return buf
        
    def get_info(self):
        return self.info
    
    def get_info_each(self):
        return self.info_each
    
    def get_sentences(self):
        return self.sentences
    
    def get_score(self):
        return self.score
    
    def get_scores_sentence(self):
        return self.scores_sentence
    
    def get_scores_voca(self):
        return self.scores_voca
    
    def get_scores_gram(self):
        return self.scores_gram

