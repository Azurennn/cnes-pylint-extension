"""Checks the access to sys.argv triggers a refactor message
"""
#pylint: disable=too-few-comments,missing-docstring-field

import sys as s
import sys
from sys import argv as a

def function1():
    a = s.argv[0]  #@

print(a)  #@

if len(sys.argv > 1):  #@
    param = sys.argv[1]  #@

stdout = sys.stdout  #@
