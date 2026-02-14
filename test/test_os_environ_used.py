"""Test the Forbidden Usage checker - os-environ-used."""
from pathlib import Path

import astroid
from pylint.testutils import CheckerTestCase, MessageTest
from pylint.utils import ASTWalker

from cnes_checker.cnes_checker import ForbiddenUsageChecker


class TestForbiddenUsageChecker(CheckerTestCase):
    CHECKER_CLASS = ForbiddenUsageChecker
    checker: ForbiddenUsageChecker

    def test_os_environ_used(self) -> None:
        """Test os_environ_used."""
        # Given
        simple_example = """
            import os
            os.getenv()  #@
        """
        node = astroid.extract_node(simple_example)

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertAddsMessages(
                MessageTest(
                    msg_id="os-environ-used",
                    node=node,
                    args="getenv()",
                    line = 3, col_offset=0, end_line=3, end_col_offset=11,
                ),
        ):
            walker.walk(node)

    def test_no_os_environ_used(self) -> None:
        """Test no_os_environ_used."""
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

    def test_os_environ_used_file(self, reference_path: Path) -> None:
        """Test os_environ_used_file."""
        # Given
        module = astroid.parse(
            (reference_path / "os_environ_used.py").read_text())

        assert len(module.body) == 9

        # When - Then
        walker = ASTWalker(self.linter)
        walker.add_checker(self.checker)

        with self.assertAddsMessages(
            MessageTest(
                msg_id="os-environ-used",
                node=module.body[3].body[0].value,
                args="os.environ",
                line=10, col_offset=6, end_line=13, end_col_offset=16,
            ),
            MessageTest(
                msg_id="os-environ-used",
                node=module.body[4].value,
                args="os.environ",
                line=12, col_offset=6, end_line=13, end_col_offset=16,
            ),
            MessageTest(
                msg_id="os-environ-used",
                node=module.body[5].value,
                args="getenv()",
                line=13, col_offset=6, end_line=13, end_col_offset=16,
            ),
            MessageTest(
                msg_id="os-environ-used",
                node=module.body[6],
                args="putenv()",
                line=14, col_offset=0, end_line=14, end_col_offset=24,
            ),
            MessageTest(
                msg_id="os-environ-used",
                node=module.body[8],
                args="unsetenv()",
                line=16, col_offset=0, end_line=16, end_col_offset=18,
            ),
        ):
            self.checker.visit_attribute(module.body[3].body[0].value)
