import datetime

import pytest

from lrdp.dbcreator import compute_next_date


@pytest.mark.parametrize(
    "current,expected",
    [
        ("2021-12-24", "2021-12-27"),
        ("2021-12-25", "2021-12-27"),
        ("2021-12-26", "2021-12-27"),
        ("2021-12-27", "2021-12-28"),
    ]
)
def test_compute_next_date(current: str, expected: str):
    current_date = datetime.date.fromisoformat(current)
    expected_date = datetime.date.fromisoformat(expected)
    next_date = compute_next_date(current_date)
    assert next_date == expected_date
