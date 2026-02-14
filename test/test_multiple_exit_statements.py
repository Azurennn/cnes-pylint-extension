"""Test the Design checker - multiple-exit-statements."""
from pathlib import Path

import astroid
from pylint.testutils import CheckerTestCase, MessageTest
from pylint.utils import ASTWalker

from cnes_checker.cnes_checker import DesignChecker


class TestDesignCheckerMultipleExitStatements(CheckerTestCase):
    CHECKER_CLASS = DesignChecker
    checker: DesignChecker

    def test_multiple_exit_statements(self) -> None:
        """Test multiple_exit_statements."""
        # Given
        simple_example = """
            for i in range(10):  #@
                if i > 3:
                    break
                if i > 5:
                    return
        """
        node = astroid.extract_node(simple_example)

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertAddsMessages(
                MessageTest(
                    msg_id="multiple-exit-statements",
                    node=node,
                    line = 2, col_offset=0, end_line=6, end_col_offset=14,
                )
        ):
            walker.walk(node)

    def test_one_exit_statement(self) -> None:
        """Test one_exit_statement."""
        # Given
        good_example = """
            for i in range(10):  #@
                return
        """
        node = astroid.extract_node(good_example)

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertNoMessages():
            walker.walk(node)

    def test_multiple_exit_statements_file(self, reference_path: Path) -> None:
        """Test multiple_exit_statements_file."""
        # Given
        nodes = astroid.extract_node(
            (reference_path / "multiple_exit_statement.py").read_text())

        assert len(nodes) == 4

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertAddsMessages(
            MessageTest(
                msg_id="multiple-exit-statements",
                node=nodes[0],
                line=6, col_offset=4, end_line=10, end_col_offset=18,
            ),
        ):
            walker.walk(nodes[0])
            walker.walk(nodes[1])

        with self.assertAddsMessages(
            MessageTest(
                msg_id="multiple-exit-statements",
                node=nodes[2],
                line=19, col_offset=4, end_line=27, end_col_offset=21,
            ),
        ):
            walker.walk(nodes[2])
            walker.walk(nodes[3])
