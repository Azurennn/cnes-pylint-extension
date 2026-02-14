"""Test the Design checker - recursive-call."""
from pathlib import Path

import astroid
from pylint.testutils import CheckerTestCase, MessageTest
from pylint.utils import ASTWalker

from cnes_checker.cnes_checker import DesignChecker


class TestDesignCheckerRecursiveCall(CheckerTestCase):
    CHECKER_CLASS = DesignChecker
    checker: DesignChecker

    def test_recursive_call(self) -> None:
        """Test recursive_call."""
        # Given
        nodes = astroid.extract_node("""
            def func1():  #@
                func1()  #@
        """)

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertAddsMessages(
                MessageTest(
                    msg_id="recursive-call",
                    node=nodes[1],
                    line = 3, col_offset=4, end_line=3, end_col_offset=11,
                ),
        ):
            walker.walk(nodes[0])

    def test_no_recursive_call(self) -> None:
        """Test no_recursive_call."""
        # Given
        node = astroid.extract_node("""
            def func1():  #@
                func2()
        """)

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertNoMessages():
            walker.walk(node)

    def test_recursive_call_file(self, reference_path: Path, no_message: str) -> None:
        """Test recursive_call_file."""
        # Given
        nodes = astroid.extract_node(
            (reference_path / "recursive_call.py").read_text())

        assert len(nodes) == 5

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertAddsMessages(
            MessageTest(
                msg_id="recursive-call",
                node=nodes[3],
                line=14, col_offset=8, end_line=14, end_col_offset=15,
            ),
            MessageTest(
                msg_id="recursive-call",
                node=nodes[4],
                line=17, col_offset=4, end_line=17, end_col_offset=11,
            ),
        ):
            walker.walk(nodes[0])
            walker.walk(nodes[1])
            walker.walk(nodes[2])
