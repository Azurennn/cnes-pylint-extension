"""Test the Comment Metrics checker - too-few-comments."""
import io
import tokenize
from pathlib import Path

import astroid
from pylint.testutils import CheckerTestCase, MessageTest

from cnes_checker.cnes_checker import CommentMetricsChecker


class TestCommentMetricsChecker(CheckerTestCase):
    CHECKER_CLASS = CommentMetricsChecker
    checker: CommentMetricsChecker

    def test_too_few_comments(self) -> None:
        """Test too_few_comments."""
        # Given
        self.checker.config.min_func_comments_ratio = 30
        self.checker.config.min_module_comments_ratio = 40
        self.checker.config.min_func_size_to_check_comments = 1

        code = """
            def bad_function():
                x = 1
                y = 2
                z = 3
                return x + y + z
        """

        module = astroid.parse(code)

        tokens = tokenize.generate_tokens(io.StringIO(code).readline)
        self.checker.process_tokens(list(tokens))

        # When - Then
        with self.assertAddsMessages(
                MessageTest(
                    msg_id="too-few-comments",
                    node=module,
                    args=('0.00', 40),
                    line = 0, col_offset=0, end_line=None, end_col_offset=None,
                ),
                MessageTest(
                    msg_id="too-few-comments",
                    node=module.body[0],
                    args=('0.00', 30),
                    line=2, col_offset=0, end_line=2, end_col_offset=16,
                ),
        ):
            self.checker.visit_module(module)
            self.checker.visit_functiondef(module.body[0])

    def test_enough_comments(self) -> None:
        """Test enough_comments."""
        # Given
        self.checker.config.min_func_comments_ratio = 30
        self.checker.config.min_module_comments_ratio = 40
        self.checker.config.min_func_size_to_check_comments = 1

        code = """
            def bad_function():
                # comment
                x = 1
                # comment
                y = 2
                # comment
                z = 3
                # comment
                return x + y + z
        """

        module = astroid.parse(code)

        tokens = tokenize.generate_tokens(io.StringIO(code).readline)
        self.checker.process_tokens(list(tokens))

        # When - Then
        with self.assertNoMessages():
            self.checker.visit_module(module)
            self.checker.visit_functiondef(module.body[0])

    def test_too_few_comments_file(self, reference_path: Path) -> None:
        """Test too_few_comments_file."""
        # Given
        self.checker.config.min_func_comments_ratio = 30  # default
        self.checker.config.min_module_comments_ratio = 40
        self.checker.config.min_func_size_to_check_comments = 10  # default

        code = (reference_path / "too_few_comments.py").read_text()
        module = astroid.parse(code)

        tokens = tokenize.generate_tokens(io.StringIO(code).readline)
        self.checker.process_tokens(list(tokens))

        # When - Then
        with self.assertAddsMessages(
            MessageTest(
                msg_id="too-few-comments",
                node=module,
                args=('27.59', 40),
                line=0, col_offset=0, end_line=None, end_col_offset=None,
            ),
            MessageTest(
                msg_id="too-few-comments",
                node=module.body[2],
                args=('27.78', 30),
                line=48, col_offset=0, end_line=48, end_col_offset=13,
            ),
        ):
            self.checker.visit_module(module)
            self.checker.visit_functiondef(module.body[0])
            self.checker.visit_functiondef(module.body[2])
            self.checker.visit_functiondef(module.body[3])
