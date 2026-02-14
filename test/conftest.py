from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def reference_path() -> Path:
    return Path(__file__).parent / "functional"


@pytest.fixture(scope="session")
def no_message() -> str:
    return "NO-MESSAGE"
