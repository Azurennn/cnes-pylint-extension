"""Test the McCabe checker too-high-complexity."""
from pathlib import Path

import astroid
from pylint.testutils import CheckerTestCase, MessageTest
from pylint.utils import ASTWalker
from cnes_checker.cnes_checker import McCabeChecker


class TestMcCabeChecker(CheckerTestCase):
    CHECKER_CLASS = McCabeChecker
    checker: McCabeChecker
    walker: ASTWalker

    simple_example = """
        def check_value(x):  #@
            if x < 0:
                return "negative"
            elif x == 0:
                return "zero"
            else:
                return "positive"
    """

    def test_too_high_complexity(self) -> None:
        """Test too_high_complexity."""
        # Given
        self.checker.linter.config.max_mccabe_number = 1

        module = astroid.parse(self.simple_example)

        # When - Then
        with self.assertAddsMessages(
                MessageTest(
                    msg_id="too-high-complexity",
                    node=module.body[0],
                    args=(3, 1),  # (actual complexity, max allowed)
                    line=2, col_offset=0, end_line=2, end_col_offset=15
                )
        ):
            self.checker.visit_module(module)

    def test_acceptable_complexity(self) -> None:
        """Test acceptable_complexity."""
        # Given
        self.checker.linter.config.max_mccabe_number = 10

        module = astroid.parse(self.simple_example)

        # When - Then
        with self.assertNoMessages():
            self.checker.visit_module(module)

    def test_too_high_complexity_file(self, reference_path: Path) -> None:
        """Test too_high_complexity_file."""
        # Given
        self.checker.linter.config.max_mccabe_number = 3

        module = astroid.parse(
            (reference_path / "too_high_complexity.py").read_text()
        )

        assert len(module.body) == 3

        # When - Then
        with self.assertAddsMessages(
            MessageTest(
                msg_id="too-high-complexity",
                node=module.body[0],
                args=(14, 3),  # (actual complexity, max allowed)
                line=5, col_offset=0, end_line=5, end_col_offset=8,
            ),
            MessageTest(
                msg_id="too-high-complexity",
                node=module.body[1].body[0],  # First method of class which is the second object
                args=(16, 3),  # (actual complexity, max allowed)
                line=45, col_offset=4, end_line=45, end_col_offset=15,
            ),
        ):
            self.checker.visit_module(module)
