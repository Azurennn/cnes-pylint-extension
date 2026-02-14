"""Test the Forbidden Usage checker - sys-exit-used."""
from pathlib import Path

import astroid
from pylint.testutils import CheckerTestCase, MessageTest
from pylint.utils import ASTWalker

from cnes_checker.cnes_checker import ForbiddenUsageChecker


class TestForbiddenUsageChecker(CheckerTestCase):
    CHECKER_CLASS = ForbiddenUsageChecker
    checker: ForbiddenUsageChecker

    def test_sys_exit_used(self) -> None:
        """Test sys_exit_used."""
        # Given
        simple_example = """
            import sys
            sys.exit(0)  #@
        """
        node = astroid.extract_node(simple_example)

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertAddsMessages(
                MessageTest(
                    msg_id="sys-exit-used",
                    node=node,
                    line = 3, col_offset=0, end_line=3, end_col_offset=11,
                ),
        ):
            walker.walk(node)

    def test_no_sys_exit_used(self) -> None:
        """Test no_sys_exit_used."""
        # Given
        good_example = """
            print("hello")  #@
        """
        node = astroid.extract_node(good_example)

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertNoMessages():
            walker.walk(node)

    def test_sys_exit_used_file(self, reference_path: Path) -> None:
        """Test sys_exit_used_file."""
        # Given
        nodes = astroid.extract_node(
            (reference_path / "sys_exit_used.py").read_text())

        assert len(nodes) == 8

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertAddsMessages(
            MessageTest(
                msg_id="sys-exit-used",
                node=nodes[0],
                line=13, col_offset=8, end_line=13, end_col_offset=12,
            ),
            MessageTest(
                msg_id="sys-exit-used",
                node=nodes[1],
                line=15, col_offset=8, end_line=15, end_col_offset=19,
            ),
            MessageTest(
                msg_id="sys-exit-used",
                node=nodes[2],
                line=17, col_offset=0, end_line=17, end_col_offset=4,
            ),
            MessageTest(
                msg_id="sys-exit-used",
                node=nodes[5],
                line=22, col_offset=4, end_line=22, end_col_offset=15,
            ),
            MessageTest(
                msg_id="sys-exit-used",
                node=nodes[6],
                line=25, col_offset=4, end_line=25, end_col_offset=13,
            ),
            MessageTest(
                msg_id="sys-exit-used",
                node=nodes[7],
                line=29, col_offset=4, end_line=29, end_col_offset=15,
            ),
        ):
            for node in nodes:
                walker.walk(node)
