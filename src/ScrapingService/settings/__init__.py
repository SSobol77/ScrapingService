# чтобы запускались local_settings и production пишем:
from .production import *
try:
    from .local_settings import *
except ImportError:
    pass
