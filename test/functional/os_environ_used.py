"""
Checks the access to environment variables triggers a refactor message
"""

import os as o
import os
from os import environ as e

def function1():
    a = os.environ  #@

print(e)  #@
env = o.getenv()  #@
o.putenv('TOTO', 'titi')  #@
sep = o.sep  #@
o.unsetenv('TOTO')  #@
