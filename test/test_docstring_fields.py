"""Test the Sphinx Doc checker."""
from pathlib import Path

import astroid
from pylint.testutils import CheckerTestCase, MessageTest
from cnes_checker.cnes_checker import SphinxDocChecker


class TestSphinxDocChecker(CheckerTestCase):
    CHECKER_CLASS = SphinxDocChecker
    checker: SphinxDocChecker

    def setup_method(self):
        super().setup_method()
        # Initialise required config attributes for DocstringParameterChecker, parent of SphinxDocChecker
        self.linter.config.no_docstring_rgx = None
        self.linter.config.docstring_min_length = -1
        self.linter.config.default_docstring_type = "default"
        self.linter.config.ignored_argument_names = []

    def test_missing_docstring_field_module(self) -> None:
        """Test missing-docstring-field for module (missing :author:)."""
        # Given
        code = '''
            """Module docstring.
            
            :version: 1.0
            :date: 2024-01-01
            """
        '''
        module = astroid.parse(code)
        module.doc = code

        # When - Then
        with self.assertAddsMessages(
            MessageTest(
                msg_id="missing-docstring-field",
                node=module,
                args=("author", ""),
                line=0, col_offset=0, end_line=None, end_col_offset=None,
            )
        ):
            self.checker.visit_module(module)

    def test_malformed_docstring_field_module(self) -> None:
        """Test malformed-docstring-field for module (:author: with no value)."""
        # Given
        code = '''
            """Module docstring.
            
            :author:
            :version: 1.0
            :date: 2024-01-01
            """
        '''
        module = astroid.parse(code)
        module.doc = code

        # When - Then
        with self.assertAddsMessages(
            MessageTest(
                msg_id="malformed-docstring-field",
                node=module,
                args=("author", ""),
                line=0, col_offset=0, end_line=None, end_col_offset=None,
            )
        ):
            self.checker.visit_module(module)

    def test_acceptable_module_docstring(self) -> None:
        """Test module with all required fields."""
        # Given
        code = '''
            """Module docstring.
            
            :author: John Doe
            :version: 1.0
            :date: 2024-01-01
            """
        '''
        module = astroid.parse(code)
        module.doc = code

        # When - Then
        with self.assertNoMessages():
            self.checker.visit_module(module)

    def test_missing_docstring_description_class(self) -> None:
        """Test missing-docstring-description for class."""
        # Given
        doc = ''':param x: some parameter'''
        code = f'''
            class MyClass:
                """{doc}"""
                pass
        '''
        module = astroid.parse(code)
        class_node = module.body[0]
        class_node.doc = doc

        # When - Then
        with self.assertAddsMessages(
            MessageTest(
                msg_id="missing-docstring-description",
                node=class_node,
                args="MyClass",
                line=2, col_offset=0, end_line=2, end_col_offset=13,
            )
        ):
            self.checker.visit_classdef(class_node)

    def test_malformed_class_docstring(self) -> None:
        """Test class with malformed description."""
        # Given
        doc = '''
    This is a class description.
        
    :param x:
    :param y: xxxxx
    '''
        code = f'''
class MyClass:
    """{doc}"""
    pass
'''
        print(code)
        module = astroid.parse(code)
        class_node = module.body[0]
        class_node.doc = doc

        # When - Then
        with self.assertAddsMessages(
            MessageTest(
                msg_id="malformed-docstring-field",
                node=class_node,
                args="MyClass",
                line=2, col_offset=0, end_line=2, end_col_offset=13,
            )
        ):
            self.checker.visit_classdef(class_node)

    def test_acceptable_class_docstring(self) -> None:
        """Test class with proper description."""
        # Given
        doc = """
    This is a class description.
        
    :param x: some parameter
    """
        code = f'''
class MyClass:
    """{doc}"""
    pass
'''
        module = astroid.parse(code)
        class_node = module.body[0]
        class_node.doc = doc

        # When - Then
        with self.assertNoMessages():
            self.checker.visit_classdef(class_node)

    func_missing = '''

    '''

    func_malformed_param = '''

    '''

    func_good = '''

    '''


    def test_missing_docstring_description_function(self) -> None:
        """Test missing-docstring-description for function."""
        # Given
        doc = """
    :param x: some parameter
    :return: something
        """
        code = f'''
def my_function(x):
    """{doc}"""
    return x
'''
        module = astroid.parse(code)
        function_node = module.body[0]
        function_node.doc = doc

        # When - Then
        with self.assertAddsMessages(
                MessageTest(
                    msg_id="missing-docstring-description",
                    node=function_node,
                    args=("my_function",),
                )
        ):
            self.checker.visit_functiondef(function_node)

    def test_malformed_function_docstring(self) -> None:
        """Test function with malformed description."""
        # Given
        doc = """
    This function does something.
    
    :param x:
    :return: something
        """
        code = f'''
def my_function(x):
    """{doc}"""
    return x
'''
        module = astroid.parse(code)
        function_node = module.body[0]
        function_node.doc = doc

        # When - Then
        with self.assertAddsMessages(
            MessageTest(
                msg_id="malformed-docstring-field",
                node=function_node,
                args=("author", ""),
            )
        ):
            self.checker.visit_functiondef(function_node)

    def test_acceptable_function_docstring(self) -> None:
        """Test function with proper description."""
        # Given
        doc = """
    This function does something.
    
    :param x: some parameter
    :return: something
        """
        code = f'''
def my_function(x):
    """{doc}"""
    return x
'''
        module = astroid.parse(code)
        function_node = module.body[0]
        function_node.doc = doc

        # When - Then
        with self.assertNoMessages():
            self.checker.visit_functiondef(function_node)

    def test_sphinx_doc_file(self, reference_path: Path) -> None:
        """Test sphinx documentation with multiple issues."""
        # Given
        module_text = (reference_path / "check_docstring_fields.py").read_text()
        module = astroid.parse(module_text)
        module.name = "sphinx_doc_issues"

        func1 = module.body[0]
        class1 = module.body[1]
        func2 = class1.body[1]

        # When - Then
        with self.assertAddsMessages(
            MessageTest(
                msg_id="missing-docstring-field",
                node=module,
                args=("author", "sphinx_doc_issues"),
            ),
            MessageTest(
                msg_id="missing-docstring-description",
                node=func1,
                args=("BadClass", "sphinx_doc_issues"),
            ),
            MessageTest(
                msg_id="missing-docstring-description",
                node=class1,
                args=("bad_function", "sphinx_doc_issues"),
            ),
            MessageTest(
                msg_id="missing-docstring-description",
                node=func2,
                args=("bad_function", "sphinx_doc_issues"),
            ),
        ):
            self.checker.visit_module(module)
            self.checker.visit_functiondef(func1)
            self.checker.visit_classdef(class1)
            self.checker.visit_functiondef(func2)
