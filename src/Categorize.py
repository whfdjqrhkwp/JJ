#!/usr/bin/env python
# coding: utf-8

# In[1]:


def categorize(form):
    
    V = 'voca'
    G = 'gram'
    
    # 명사
    Noun = ['NN', 'NNG', 'NNP', 'UN']
    
    # 대명사
    Pronoun = ['NP']
    
    # 의존명사
    BoundNoun = ['NNB', 'NNM']
    
    # 동사
    Verb = ['VV', 'VXV']
    
    # 형용사
    Adjective = ['VA', 'VXA', 'VCN']
    
    # 수사
    Numeral = ['NR']
    
    # 부사
    Adverb = ['MA', 'MAC', 'MAG']
    
    # 접사
    Affix = ['XP', 'XPN', 'XPV', 'XSA', 'XSN', 'XSV']
    
    # 관형사
    Determiner = ['MD', 'MDN', 'MDT']
    
    # 감탄사
    Interjection = ['IC']
    
    # 조사
    Postposition = ['JC', 'JK', 'JKC', 'JKG', 'JKI', 'JKM', 'JKO', 'JKQ', 'JKS', 'JX', 'VCP']
    
    # 선어말 어미
    PreFinalEnding = ['EP', 'EPH', 'EPP', 'EPT']
    
    # 연결 어미
    ConnectEnding = ['EC', 'ECD', 'ECE', 'ECS', ]
    
    # 전성 어미
    TransEnding = ['ET', 'ETD', 'ETN']
    
    # 종결 어미
    FinalEnding = ['EF', 'EFA', 'EFI', 'EFN', 'EFO', 'EFQ', 'EFR']
    
    #어근
    Root = ['XR']
    
    
    if form in Noun:
        return 'Noun', V
    
    if form in Pronoun:
        return 'Pronoun', V
    
    if form in BoundNoun:
        return 'BoundNoun', V
    
    if form in Verb:
        return 'Verb', V
    
    if form in Adjective:
        return 'Adjective', V
    
    if form in Numeral:
        return 'Numeral', V
        
    if form in Adverb:
        return 'Adverb', V
    
    if form in Affix:
        return 'Affix', V
    
    if form in Determiner:
        return 'Determiner', V
    
    if form in Interjection:
        return 'Interjection', V
    
    if form in Postposition:
        return 'Postposition', G
    
    if form in PreFinalEnding:
        return 'PreFinalEnding', G
    
    if form in ConnectEnding:
        return 'ConnectEnding', G
    
    if form in TransEnding:
        return 'TransEnding', G
    
    if form in FinalEnding:
        return 'FinalEnding', G
    
    if form in Root:
        return 'Root', V
        
    return None, None

