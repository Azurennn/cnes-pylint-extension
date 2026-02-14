"""
Checks that loop exit conditions don't use equality or difference comparison
"""
string = '   hello world'
i = 0
while string[i] == ' ':  #@
    i += 1
i = 0
while string[i] != 'h':  #@
    i += 1
while i < 5 and string[i] == ' ':  #@
    i += 1
while i > 0:  #@
    i -= 1
while True:  #@
    pass
while string[i] == ' ' and True or i != 3:  #@
    pass
