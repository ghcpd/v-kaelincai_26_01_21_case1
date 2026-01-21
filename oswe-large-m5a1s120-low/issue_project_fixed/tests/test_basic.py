import pytest

from prettytable import PrettyTable
from prettytable.colortable import ColorTable, Themes


def test_basic_creation() -> None:
    table = PrettyTable()
    table.field_names = ["Name", "Age"]
    table.add_row(["Alice", 30])
    result = table.get_string()
    assert "Alice" in result
    assert "30" in result


def test_alignment() -> None:
    table = PrettyTable()
    table.field_names = ["Left", "Center", "Right"]
    table.add_row(["L", "C", "R"])
    table.align["Left"] = "l"
    table.align["Center"] = "c"
    table.align["Right"] = "r"
    result = table.get_string()
    assert result  # non-empty


def test_sorting() -> None:
    table = PrettyTable()
    table.field_names = ["Name", "Score"]
    table.add_row(["Alice", 85])
    table.add_row(["Bob", 92])
    table.add_row(["Charlie", 78])

    sorted_result = table.get_string(sortby="Score")
    assert "Charlie" in sorted_result


def test_border_settings() -> None:
    table = PrettyTable()
    table.field_names = ["A", "B"]
    table.add_row([1, 2])

    table.border = False
    no_border = table.get_string()

    table.border = True
    with_border = table.get_string()

    assert len(with_border) > len(no_border)


def test_max_width() -> None:
    table = PrettyTable()
    table.field_names = ["Long Text"]
    table.add_row(["This is a very long text that should be wrapped"])
    table.max_width["Long Text"] = 20
    result = table.get_string()
    assert result


def test_add_column() -> None:
    table = PrettyTable()
    table.add_column("Name", ["Alice", "Bob", "Charlie"])
    table.add_column("Age", [30, 25, 35])
    result = table.get_string()
    assert "Alice" in result
    assert "30" in result


def test_field_names() -> None:
    table = PrettyTable()
    table.field_names = ["Column1", "Column2", "Column3"]
    assert len(table.field_names) == 3
    assert "Column1" in table.field_names


def test_clear() -> None:
    table = PrettyTable()
    table.field_names = ["A", "B"]
    table.add_row([1, 2])
    table.add_row([3, 4])

    table.clear_rows()
    result = table.get_string()

    assert "A" in result
    assert "1" not in result


def test_colortable_theme_update() -> None:
    table = ColorTable()
    table.field_names = ["Name"]
    table.add_row(["Alice"])
    table.theme = Themes.OCEAN
    result = table.get_string()
    # trailing reset code should be appended
    assert result.endswith("\x1b[0m")
