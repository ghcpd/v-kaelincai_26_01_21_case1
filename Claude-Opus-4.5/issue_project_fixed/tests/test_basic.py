"""
Test suite for PrettyTable core functionality
Issue #206: Add mypy via pre-commit and make mypy pass

This test module verifies that all core PrettyTable features work correctly
after adding type annotations and fixing mypy errors.
"""
from __future__ import annotations

import pytest

from prettytable import PrettyTable, HRuleStyle, VRuleStyle, TableStyle


class TestBasicCreation:
    """Tests for basic table creation and data manipulation."""

    def test_create_empty_table(self) -> None:
        """Test creating an empty table."""
        table = PrettyTable()
        assert table is not None
        assert table.rowcount == 0

    def test_create_table_with_field_names(self) -> None:
        """Test creating a table with field names."""
        table = PrettyTable(["Name", "Age", "City"])
        assert len(table.field_names) == 3
        assert "Name" in table.field_names

    def test_add_row(self) -> None:
        """Test adding a row to the table."""
        table = PrettyTable()
        table.field_names = ["Name", "Age"]
        table.add_row(["Alice", 30])
        result = table.get_string()
        assert "Alice" in result
        assert "30" in result

    def test_add_multiple_rows(self) -> None:
        """Test adding multiple rows to the table."""
        table = PrettyTable()
        table.field_names = ["Name", "Age"]
        table.add_rows([["Alice", 30], ["Bob", 25]])
        assert table.rowcount == 2


class TestAlignment:
    """Tests for alignment functionality."""

    def test_left_alignment(self) -> None:
        """Test left alignment."""
        table = PrettyTable()
        table.field_names = ["Name", "Value"]
        table.add_row(["Test", "123"])
        table.align["Name"] = "l"
        result = table.get_string()
        assert len(result) > 0

    def test_center_alignment(self) -> None:
        """Test center alignment."""
        table = PrettyTable()
        table.field_names = ["Name", "Value"]
        table.add_row(["Test", "123"])
        table.align["Name"] = "c"
        result = table.get_string()
        assert len(result) > 0

    def test_right_alignment(self) -> None:
        """Test right alignment."""
        table = PrettyTable()
        table.field_names = ["Name", "Value"]
        table.add_row(["Test", "123"])
        table.align["Name"] = "r"
        result = table.get_string()
        assert len(result) > 0

    def test_vertical_alignment(self) -> None:
        """Test vertical alignment options."""
        table = PrettyTable()
        table.field_names = ["Name", "Value"]
        table.add_row(["Test", "123"])
        table.valign["Name"] = "t"
        table.valign["Value"] = "m"
        result = table.get_string()
        assert len(result) > 0


class TestSorting:
    """Tests for sorting functionality."""

    def test_sort_by_field(self) -> None:
        """Test sorting by a specific field."""
        table = PrettyTable()
        table.field_names = ["Name", "Score"]
        table.add_row(["Alice", 85])
        table.add_row(["Bob", 92])
        table.add_row(["Charlie", 78])
        
        sorted_result = table.get_string(sortby="Score")
        assert "Charlie" in sorted_result

    def test_reverse_sort(self) -> None:
        """Test reverse sorting."""
        table = PrettyTable()
        table.field_names = ["Name", "Score"]
        table.add_row(["Alice", 85])
        table.add_row(["Bob", 92])
        
        result = table.get_string(sortby="Score", reversesort=True)
        assert len(result) > 0


class TestBorderSettings:
    """Tests for border configuration."""

    def test_border_on_off(self) -> None:
        """Test toggling border on and off."""
        table = PrettyTable()
        table.field_names = ["A", "B"]
        table.add_row([1, 2])
        
        table.border = False
        no_border = table.get_string()
        
        table.border = True
        with_border = table.get_string()
        
        assert len(with_border) > len(no_border)

    def test_hrules(self) -> None:
        """Test horizontal rule styles."""
        table = PrettyTable()
        table.field_names = ["A", "B"]
        table.add_row([1, 2])
        
        table.hrules = HRuleStyle.ALL
        result = table.get_string()
        assert len(result) > 0

    def test_vrules(self) -> None:
        """Test vertical rule styles."""
        table = PrettyTable()
        table.field_names = ["A", "B"]
        table.add_row([1, 2])
        
        table.vrules = VRuleStyle.ALL
        result = table.get_string()
        assert len(result) > 0


class TestWidthSettings:
    """Tests for width configuration."""

    def test_max_width(self) -> None:
        """Test maximum width setting."""
        table = PrettyTable()
        table.field_names = ["Long Text"]
        table.add_row(["This is a very long text that should be wrapped"])
        table.max_width["Long Text"] = 20
        result = table.get_string()
        assert len(result) > 0

    def test_min_width(self) -> None:
        """Test minimum width setting."""
        table = PrettyTable()
        table.field_names = ["Short"]
        table.add_row(["X"])
        table.min_width["Short"] = 15
        result = table.get_string()
        assert len(result) > 0

    def test_padding_width(self) -> None:
        """Test padding width setting."""
        table = PrettyTable()
        table.field_names = ["A", "B"]
        table.add_row([1, 2])
        table.padding_width = 3
        result = table.get_string()
        assert len(result) > 0


class TestColumnOperations:
    """Tests for column operations."""

    def test_add_column(self) -> None:
        """Test adding a column."""
        table = PrettyTable()
        table.add_column("Name", ["Alice", "Bob", "Charlie"])
        table.add_column("Age", [30, 25, 35])
        result = table.get_string()
        assert "Alice" in result
        assert "30" in result

    def test_del_column(self) -> None:
        """Test deleting a column."""
        table = PrettyTable()
        table.field_names = ["A", "B", "C"]
        table.add_row([1, 2, 3])
        table.del_column("B")
        assert "B" not in table.field_names


class TestClearOperations:
    """Tests for clear operations."""

    def test_clear_rows(self) -> None:
        """Test clearing rows."""
        table = PrettyTable()
        table.field_names = ["A", "B"]
        table.add_row([1, 2])
        table.add_row([3, 4])
        
        table.clear_rows()
        result = table.get_string()
        
        assert "A" in result
        assert "1" not in result

    def test_clear_all(self) -> None:
        """Test clearing all data."""
        table = PrettyTable()
        table.field_names = ["A", "B"]
        table.add_row([1, 2])
        
        table.clear()
        assert table.rowcount == 0
        assert len(table.field_names) == 0


class TestOutputFormats:
    """Tests for different output formats."""

    def test_get_string(self) -> None:
        """Test getting string representation."""
        table = PrettyTable()
        table.field_names = ["Name", "Value"]
        table.add_row(["Test", 123])
        result = table.get_string()
        assert isinstance(result, str)

    def test_get_html_string(self) -> None:
        """Test getting HTML representation."""
        table = PrettyTable()
        table.field_names = ["Name", "Value"]
        table.add_row(["Test", 123])
        result = table.get_html_string()
        assert "<table>" in result
        assert "</table>" in result

    def test_get_csv_string(self) -> None:
        """Test getting CSV representation."""
        table = PrettyTable()
        table.field_names = ["Name", "Value"]
        table.add_row(["Test", 123])
        result = table.get_csv_string()
        assert "Name" in result

    def test_get_json_string(self) -> None:
        """Test getting JSON representation."""
        table = PrettyTable()
        table.field_names = ["Name", "Value"]
        table.add_row(["Test", 123])
        result = table.get_json_string()
        assert "Name" in result

    def test_get_latex_string(self) -> None:
        """Test getting LaTeX representation."""
        table = PrettyTable()
        table.field_names = ["Name", "Value"]
        table.add_row(["Test", 123])
        result = table.get_latex_string()
        assert "\\begin{tabular}" in result


class TestStyles:
    """Tests for table styles."""

    def test_set_style_default(self) -> None:
        """Test setting default style."""
        table = PrettyTable()
        table.field_names = ["A", "B"]
        table.add_row([1, 2])
        table.set_style(TableStyle.DEFAULT)
        result = table.get_string()
        assert len(result) > 0

    def test_set_style_markdown(self) -> None:
        """Test setting markdown style."""
        table = PrettyTable()
        table.field_names = ["A", "B"]
        table.add_row([1, 2])
        table.set_style(TableStyle.MARKDOWN)
        result = table.get_string()
        assert len(result) > 0

    def test_set_style_double_border(self) -> None:
        """Test setting double border style."""
        table = PrettyTable()
        table.field_names = ["A", "B"]
        table.add_row([1, 2])
        table.set_style(TableStyle.DOUBLE_BORDER)
        result = table.get_string()
        assert len(result) > 0


class TestMiscFeatures:
    """Tests for miscellaneous features."""

    def test_table_title(self) -> None:
        """Test table title."""
        table = PrettyTable()
        table.field_names = ["A", "B"]
        table.add_row([1, 2])
        table.title = "My Table"
        result = table.get_string()
        assert "My Table" in result

    def test_header_style(self) -> None:
        """Test header style settings."""
        table = PrettyTable()
        table.field_names = ["name", "value"]
        table.add_row(["Test", 123])
        table.header_style = "upper"
        result = table.get_string()
        assert "NAME" in result

    def test_copy_table(self) -> None:
        """Test table copying."""
        table = PrettyTable()
        table.field_names = ["A", "B"]
        table.add_row([1, 2])
        
        copy = table.copy()
        assert copy.rowcount == table.rowcount
        assert copy.field_names == table.field_names

    def test_slicing(self) -> None:
        """Test table slicing."""
        table = PrettyTable()
        table.field_names = ["Index", "Value"]
        for i in range(5):
            table.add_row([i, i * 10])
        
        sliced = table[1:3]
        assert sliced.rowcount == 2
