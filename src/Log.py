#!/usr/bin/env python
# coding: utf-8

# In[8]:


import os
import logging
import logging.handlers

class Setting(object):
    dir_address = os.path.join(os.getcwd(), '_Log')
    
    LEVEL = logging.DEBUG
    FILENAME_RECENT = os.path.join(dir_address, 'Recent.log')
    FILENAME_ALL = os.path.join(dir_address, 'ALL.log')
    MAX_BYTES = 10 * 1024 * 1024
    ENCODING = 'utf-8'
    MODE = 'a'
    FORMAT = 'asctime : %(asctime)s\n'            + 'created : %(created)f\n'            + 'filename : %(filename)s\n'            + 'funcName : %(funcName)s\n'            + 'levelname : %(levelname)s\n'            + 'levelno : %(levelno)s\n'            + 'lineno : %(lineno)d\n'            + 'message : %(message)s\n'            + 'module : %(module)s\n'            + 'msecs : %(msecs)d\n'            + 'name : %(name)s\n'            + 'pathname : %(pathname)s\n'            + 'relativeCreated : %(relativeCreated)d\n'            + '-' * 50
    
    FORMAT = '[%(asctime)s] %(levelname)s :: <%(name)s> %(funcName)s = %(message)s'
    
    @classmethod
    def setting(cls):
        if not os.path.isdir(cls.dir_address):
            os.mkdir(cls.dir_address)
            
        if os.path.exists(cls.FILENAME_RECENT):
            with open(cls.FILENAME_RECENT, 'w', encoding = cls.ENCODING) as log:
                log.write('')
                
        if os.path.exists(cls.FILENAME_ALL) and os.path.getsize(cls.FILENAME_ALL) > cls.MAX_BYTES:
            with open(cls.FILENAME_ALL, 'w', encoding = cls.ENCODING) as log:
                log.write('')


def Logger(name):
    Setting.setting()
    
    logger = logging.getLogger(name)
    formatter = logging.Formatter(Setting.FORMAT)
    
    streamHandler = logging.StreamHandler()
    
    FileHandler_recent = logging.FileHandler(
        filename = Setting.FILENAME_RECENT,
        mode = Setting.MODE,
        encoding = Setting.ENCODING)
    
    FileHandler_all = logging.FileHandler(
        filename = Setting.FILENAME_ALL,
        mode = Setting.MODE,
        encoding = Setting.ENCODING)
    
    streamHandler.setFormatter(formatter)
    FileHandler_recent.setFormatter(formatter)
    FileHandler_all.setFormatter(formatter)

    #logger.addHandler(streamHandler)
    logger.addHandler(FileHandler_recent)
    logger.addHandler(FileHandler_all)

    logger.setLevel(Setting.LEVEL)

    return logger

