"""Test the Design checker - bad-exit-condition."""
from pathlib import Path

import astroid
from pylint.testutils import CheckerTestCase, MessageTest
from pylint.utils import ASTWalker

from cnes_checker.cnes_checker import DesignChecker


class TestDesignCheckerBadExitCondition(CheckerTestCase):
    CHECKER_CLASS = DesignChecker
    checker: DesignChecker

    def test_bad_exit_condition(self) -> None:
        """Test test_bad_exit_condition."""
        # Given
        simple_example = """
            while i != 10:  #@
                print(i)
                i += 1
        """
        node = astroid.extract_node(simple_example)

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertAddsMessages(
                MessageTest(
                    msg_id="bad-exit-condition",
                    node=node,
                    line = 2, col_offset=0, end_line=4, end_col_offset=10,
                )
        ):
            walker.walk(node)

    def test_acceptable_exit_condition(self) -> None:
        """Test test_acceptable_exit_condition."""
        # Given
        good_example = """
            while i < 10:  #@
                print(i)
                i += 1
        """
        node = astroid.extract_node(good_example)

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertNoMessages():
            walker.walk(node)

    def test_bad_exit_condition_file(self, reference_path: Path, no_message: str) -> None:
        """Test bad_exit_condition_file."""
        # Given
        nodes = astroid.extract_node(
            (reference_path / "bad_exit_condition.py").read_text())

        assert len(nodes) == 6

        excepted_messages = [

            no_message,
            no_message,

        ]

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)
        with self.assertAddsMessages(
            MessageTest(
                msg_id="bad-exit-condition",
                node=nodes[0],
                line=6, col_offset=0, end_line=7, end_col_offset=10,
            ),
            MessageTest(
                msg_id="bad-exit-condition",
                node=nodes[1],
                line=9, col_offset=0, end_line=10, end_col_offset=10,
            ),
            MessageTest(
                msg_id="bad-exit-condition",
                node=nodes[2],
                line=11, col_offset=0, end_line=12, end_col_offset=10,
            ),
        ):
            walker.walk(nodes[0])
            walker.walk(nodes[1])
            walker.walk(nodes[2])
            walker.walk(nodes[3])
            walker.walk(nodes[4])

        with self.assertAddsMessages(
            MessageTest(
                msg_id="bad-exit-condition",
                node=nodes[5],
                line=17, col_offset=0, end_line=18, end_col_offset=8,
            ),
        ):
            walker.walk(nodes[5])
