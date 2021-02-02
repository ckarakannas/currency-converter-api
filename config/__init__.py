import os
import sys
import config.cfg

API_ENV = os.environ.get('API_ENV', 'Development')
_current_config = getattr(
    sys.modules['config.cfg'], '{0}Config'.format(API_ENV))()

for atr in [f for f in dir(_current_config) if not '__' in f]:
    # environment can override attrs
    val = os.environ.get(atr, getattr(_current_config, atr))
    setattr(sys.modules[__name__], atr, val)
