from IPython import get_ipython

ipython = get_ipython()

if ipython:
    if ipython.has_trait('kernel'):
        ipython.magic('matplotlib inline')
        ipython.magic('reload_ext autoreload')
        ipython.magic('autoreload 2')
