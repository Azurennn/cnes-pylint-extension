"""
Checks that the number of decorators applied on a function does not exceed the limit
"""

@decorator1
@decorator2
@decorator3
@decorator4
@decorator5
def func_ok():  #@
    pass

@decorator1
@decorator2
@decorator3
@decorator4
@decorator5
@decorator6
def func_ko():  #@
    pass

class MyClass(object):  #@

    @decorator1
    @decorator2
    @decorator3
    @decorator4
    @decorator5
    @decorator6
    def method(self):  #@
        pass
