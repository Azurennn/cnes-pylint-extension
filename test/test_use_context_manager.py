"""Test the Design checker - use-context-manager."""
from pathlib import Path

import astroid
from pylint.testutils import CheckerTestCase, MessageTest
from pylint.utils import ASTWalker

from cnes_checker.cnes_checker import DesignChecker


class TestDesignCheckerUseContextManager(CheckerTestCase):
    CHECKER_CLASS = DesignChecker
    checker: DesignChecker

    def test_use_context_manager(self) -> None:
        """Test use_context_manager."""
        # Given
        node = astroid.extract_node("""
            f = open("file.txt")  #@
        """)

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertAddsMessages(
                MessageTest(
                    msg_id="use-context-manager",
                    node=node.value,
                    args="opening the file",
                    line = 2, col_offset=4, end_line=2, end_col_offset=20,
                ),
        ):
            walker.walk(node)

    def test_context_manager_used(self) -> None:
        """Test context_manager_used."""
        # Given
        node = astroid.extract_node("""
            with open("file.txt") as f:  #@
                pass
        """)

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertNoMessages():
            walker.walk(node)

    def test_use_context_manager_file(self, reference_path: Path) -> None:
        """Test use_context_manager_file."""
        # Given
        nodes = astroid.extract_node(
            (reference_path / "use_context_manager.py").read_text())

        assert len(nodes) == 10

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertAddsMessages(
            MessageTest(
                msg_id="use-context-manager",
                node=nodes[1].value,
                args="opening the file",
                line=10, col_offset=4, end_line=10, end_col_offset=21,
            ),
            MessageTest(
                msg_id="use-context-manager",
                node=nodes[4].func,
                args="acquiring the lock",
                line=15, col_offset=0, end_line=15, end_col_offset=12,
            ),
            MessageTest(
                msg_id="use-context-manager",
                node=nodes[7].func,
                args="acquiring the lock",
                line=19, col_offset=0, end_line=19, end_col_offset=12,
            ),
            MessageTest(
                msg_id="use-context-manager",
                node=nodes[9].func,
                args="acquiring the lock",
                line=22, col_offset=0, end_line=22, end_col_offset=12,
            ),
        ):
            for node in nodes:
                walker.walk(node)
