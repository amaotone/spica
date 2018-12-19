from IPython import get_ipython

__ipy = get_ipython()

if __ipy:
    if __ipy.has_trait('kernel'):
        __ipy.magic('matplotlib inline')
        __ipy.magic('reload_ext autoreload')
        __ipy.magic('autoreload 2')
