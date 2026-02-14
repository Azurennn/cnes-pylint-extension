"""Test the Design checker - builtin-name-used."""
from pathlib import Path

import astroid
from pylint.testutils import CheckerTestCase, MessageTest
from pylint.utils import ASTWalker

from cnes_checker.cnes_checker import DesignChecker


class TestDesignCheckerBuiltinNameUsed(CheckerTestCase):
    CHECKER_CLASS = DesignChecker
    checker: DesignChecker

    def test_builtin_name_used(self) -> None:
        """Test builtin_name_used."""
        # Given
        simple_example = """
            class MyClass(object):  #@
                str = "hello"  #@
        """
        nodes = astroid.extract_node(simple_example)

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertAddsMessages(
                MessageTest(
                    msg_id="builtin-name-used",
                    node=nodes[1].targets[0],
                    args=("str",),
                    line = 3, col_offset=4, end_line=3, end_col_offset=7,
                )
        ):
            walker.walk(nodes[0])

    def test_acceptable_name_used(self) -> None:
        """Test acceptable_name_used."""
        # Given
        good_example = """
            class MyClass(object):  #@
                _str = "hello"
        """
        node = astroid.extract_node(good_example)

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertNoMessages():
            walker.walk(node)

    def test_builtin_name_used_file(self, reference_path: Path, no_message: str) -> None:
        """Test builtin_name_used_file."""
        # Given
        nodes = astroid.extract_node(
            (reference_path / "builtin_name_used.py").read_text())

        assert len(nodes) == 7

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertAddsMessages(
            MessageTest(
                msg_id="builtin-name-used",
                node=nodes[1].targets[0].elts[0].elts[0],  # specifically the self.str in the tuple attribution
                args=("str",),
                line=7, col_offset=10, end_line=7, end_col_offset=18
            ),
            MessageTest(
                msg_id="builtin-name-used",
                node=nodes[2].targets[0],
                args=("bool",),
                line=9, col_offset=4, end_line=9, end_col_offset=8
            ),
            MessageTest(
                msg_id="builtin-name-used",
                node=nodes[3],
                args=("map",),
                line=11, col_offset=4, end_line=11, end_col_offset=11
            ),
            MessageTest(
                msg_id="builtin-name-used",
                node=nodes[4].targets[0],
                args=("zip",),
                line=16, col_offset=4, end_line=16, end_col_offset=7
            ),
            MessageTest(
                msg_id="builtin-name-used",
                node=nodes[5].targets[0],
                args=("dict",),
                line=18, col_offset=0, end_line=18, end_col_offset=12
            ),
        ):
            walker.walk(nodes[0])

        with self.assertNoMessages():
            walker.walk(nodes[6])
