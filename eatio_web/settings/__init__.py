import os

if 'IS_RUNNING_ON_AMAZON' in os.environ:

    from .production import *
else:
    from .dev import*
