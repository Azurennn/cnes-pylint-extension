"""Test the McCabe Simplified checker too-high-complexity-simplified."""
from pathlib import Path

import astroid
from pylint.testutils import CheckerTestCase, MessageTest
from pylint.utils import ASTWalker
from cnes_checker.cnes_checker import McCabeChecker


class TestMcCabeCheckerSimplified(CheckerTestCase):
    CHECKER_CLASS = McCabeChecker
    checker: McCabeChecker
    walker: ASTWalker

    simple_example = """
        def complex_function(x):  #@
            if x > 0:
                for i in range(10):
                    while i < 5:
                        print(i)
    """

    def test_too_high_complexity_simplified(self) -> None:
        """Test too_high_complexity_simplified."""
        # Given
        self.checker.linter.config.max_simplified_mccabe_number = 1

        node = astroid.extract_node(self.simple_example)

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertAddsMessages(
                MessageTest(
                    msg_id="too-high-complexity-simplified",
                    node=node,
                    args=(3, 1),  # (actual complexity, max allowed)
                    line=2, col_offset=0, end_line=2, end_col_offset=20
                )
        ):
            walker.walk(node)

    def test_acceptable_simplified_complexity(self) -> None:
        """Test acceptable_simplified_complexity."""
        # Given
        self.checker.linter.config.max_simplified_mccabe_number = 10

        node = astroid.extract_node(self.simple_example)

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertNoMessages():
            walker.walk(node)

    def test_too_high_complexity_simplified_file(self, reference_path: Path, no_message: str) -> None:
        """Test too_high_complexity_simplified_file."""
        # Given
        self.checker.linter.config.max_simplified_mccabe_number = 2

        nodes = astroid.extract_node(
            (reference_path / "too_high_complexity_simplified.py").read_text())

        assert len(nodes) == 3

        excepted_messages = [
            MessageTest(
                msg_id="too-high-complexity-simplified",
                node=nodes[0],
                args=(10, 2),  # (actual complexity, max allowed)
                line=5, col_offset=0, end_line=5, end_col_offset=8,
            ),
            MessageTest(
                msg_id="too-high-complexity-simplified",
                node=nodes[1],
                args=(11, 2),  # (actual complexity, max allowed)
                line=36, col_offset=4, end_line=36, end_col_offset=14,
            ),
            no_message,
        ]
        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        for node, expected_message in zip(nodes, excepted_messages):
            if expected_message != no_message:
                with self.assertAddsMessages(expected_message):
                    walker.walk(node)
            else:
                with self.assertNoMessages():
                    walker.walk(node)
