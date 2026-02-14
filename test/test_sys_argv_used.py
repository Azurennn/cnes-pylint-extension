"""Test the Forbidden Usage checker - sys-argv-used."""
from pathlib import Path

import astroid
from pylint.testutils import CheckerTestCase, MessageTest
from pylint.utils import ASTWalker

from cnes_checker.cnes_checker import ForbiddenUsageChecker


class TestForbiddenUsageChecker(CheckerTestCase):
    CHECKER_CLASS = ForbiddenUsageChecker
    checker: ForbiddenUsageChecker

    def test_sys_argv_used(self) -> None:
        """Test sys_argv_used."""
        # Given
        simple_example = """
            import sys
            sys.argv  #@
        """
        node = astroid.extract_node(simple_example)

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertAddsMessages(
                MessageTest(
                    msg_id="sys-argv-used",
                    node=node,
                    line = 3, col_offset=0, end_line=3, end_col_offset=11,
                ),
        ):
            walker.walk(node)

    def test_no_sys_argv_used(self) -> None:
        """Test no_sys_argv_used."""
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

    def test_sys_argv_used_file(self, reference_path: Path) -> None:
        """Test sys_argv_used_file."""
        # Given
        nodes = astroid.extract_node(
            (reference_path / "sys_argv_used.py").read_text())

        assert len(nodes) == 5

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertAddsMessages(
            MessageTest(
                msg_id="sys-argv-used",
                node=nodes[2],
                args="os.environ",
                line=10, col_offset=6, end_line=13, end_col_offset=16,
            ),
        ):
            for node in nodes:
                walker.walk(node)
