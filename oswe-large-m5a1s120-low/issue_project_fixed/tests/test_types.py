from __future__ import annotations

from typing import Literal

import pytest
from mypy import api as mypy_api
from typing_extensions import assert_type

from prettytable import HRuleStyle, PrettyTable, TableStyle, VRuleStyle


def test_public_api_types() -> None:
    table = PrettyTable()
    table.field_names = ["Name", "Age"]
    table.add_row(["Alice", 42])

    # align/valign dictionaries expose concrete literal types
    assert_type(table.align, dict[str, Literal["l", "c", "r"]])
    assert_type(table.valign, dict[str, Literal["t", "m", "b"]])

    # style enums
    assert isinstance(HRuleStyle.FRAME, HRuleStyle)
    assert isinstance(VRuleStyle.ALL, VRuleStyle)
    assert isinstance(TableStyle.DEFAULT, TableStyle)

    # factory functions
    csv_table = table  # placeholder for type checking
    assert isinstance(csv_table.get_string(), str)


def test_mypy_passes_on_package(tmp_path: pytest.PathLike[str]) -> None:
    # Run mypy against the installed (or source) package to ensure stubs/deps available.
    result = mypy_api.run([
        "--config-file=",
        "--strict",
        "src/prettytable",
    ])
    stdout, stderr, exit_code = result
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)
    assert exit_code == 0
