"""
Check no method nor attribute it named after a builtin
"""

class MyClass(object):  #@
    def __init__(self):
        ((self.str, self.something), plop) = (('test.txt', 'hello'), 'plop')  #@

    bool = True  #@

    def map(self):  #@
        pass

    def dummy_method(cls):
        pass
    zip = classmethod(dummy_method)  #@

MyClass.dict = "hi there"  #@


class ChildClass(MyClass):  #@

    def map(self):
        """inherited: should be ok"""
