#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os

import import_ipynb
from Interface import run

from Log import Logger
log = Logger('Run')


# In[ ]:


if __name__ == '__main__':
    log.info('START')
    run()
    log.info('END\n{}'.format('=' * 150))
    
    os.system('pause')

