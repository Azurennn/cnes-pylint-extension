"""
Check direct recursion isn't permitted.
"""

def func1():  #@
    """does nothing"""

class MyClass(object):  #@
    def func2(self):
        pass

def func2():  #@
    if True:
        func2()  #@
    for i in range(10):
        func1()
    func2()  #@
    c = MyClass()
    c.func2()
