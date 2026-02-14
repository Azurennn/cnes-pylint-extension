"""Test the Design checker - too-many-decorators."""
from pathlib import Path

import astroid
from pylint.testutils import CheckerTestCase, MessageTest
from pylint.utils import ASTWalker

from cnes_checker.cnes_checker import DesignChecker


class TestDesignCheckerTooManyDecorators(CheckerTestCase):
    CHECKER_CLASS = DesignChecker
    checker: DesignChecker

    simple_example = """
        @decorator1
        @decorator2
        def hello():  #@
            return
    """

    def test_too_many_decorators(self) -> None:
        """Test too_many_decorators."""
        # Given
        self.checker.config.max_decorators = 1
        node = astroid.extract_node(self.simple_example)

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertAddsMessages(
                MessageTest(
                    msg_id="too-many-decorators",
                    node=node,
                    args=(2, 1),
                    line = 4, col_offset=0, end_line=4, end_col_offset=9,
                ),
        ):
            walker.walk(node)

    def test_enough_decorators(self) -> None:
        """Test enough_decorators."""
        # Given
        self.checker.config.max_decorators = 2
        node = astroid.extract_node(self.simple_example)

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertNoMessages():
            walker.walk(node)

    def test_too_many_decorators_file(self, reference_path: Path, no_message: str) -> None:
        """Test too_many_decorators_file."""
        # Given
        self.checker.config.max_decorators = 5  # default is 5 anyway
        nodes = astroid.extract_node(
            (reference_path / "too_many_decorators.py").read_text())

        assert len(nodes) == 4

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertAddsMessages(
            MessageTest(
                msg_id="too-many-decorators",
                node=nodes[1],
                args=(6, 5),
                line=19, col_offset=0, end_line=19, end_col_offset=11,
            ),
        ):
            walker.walk(nodes[0])
            walker.walk(nodes[1])

        with self.assertAddsMessages(
            MessageTest(
                msg_id="too-many-decorators",
                node=nodes[3],
                args=(6, 5),
                line=30, col_offset=4, end_line=30, end_col_offset=14,
            ),
        ):
            walker.walk(nodes[2])
