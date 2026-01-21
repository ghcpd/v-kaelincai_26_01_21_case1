"""
Basic functionality tests for PrettyTable
Issue #206: Add mypy via pre-commit and make mypy pass

Tests basic table creation and manipulation features.
"""

from __future__ import annotations

import pytest
from prettytable import PrettyTable


class TestBasicCreation:
    """Test basic table creation and manipulation."""

    def test_empty_table(self):
        """Test creating an empty table."""
        table = PrettyTable()
        assert table is not None
        assert len(table.field_names) == 0

    def test_field_names_setting(self):
        """Test setting field names."""
        table = PrettyTable()
        table.field_names = ["Name", "Age", "City"]
        assert len(table.field_names) == 3
        assert table.field_names == ["Name", "Age", "City"]

    def test_add_single_row(self):
        """Test adding a single row."""
        table = PrettyTable()
        table.field_names = ["Name", "Age"]
        table.add_row(["Alice", 30])
        result = table.get_string()
        assert "Alice" in result
        assert "30" in result

    def test_add_multiple_rows(self):
        """Test adding multiple rows."""
        table = PrettyTable()
        table.field_names = ["Name", "Age", "City"]
        table.add_row(["Alice", 30, "New York"])
        table.add_row(["Bob", 25, "Los Angeles"])
        table.add_row(["Charlie", 35, "Chicago"])
        result = table.get_string()
        assert "Alice" in result
        assert "Bob" in result
        assert "Charlie" in result

    def test_add_column(self):
        """Test adding columns."""
        table = PrettyTable()
        table.add_column("Name", ["Alice", "Bob", "Charlie"])
        table.add_column("Age", [30, 25, 35])
        result = table.get_string()
        assert "Name" in result
        assert "Age" in result
        assert "Alice" in result
        assert "30" in result

    def test_clear_rows(self):
        """Test clearing rows while keeping field names."""
        table = PrettyTable()
        table.field_names = ["A", "B"]
        table.add_row([1, 2])
        table.add_row([3, 4])
        table.clear_rows()
        result = table.get_string()
        assert "A" in result
        assert "B" in result
        # Data should be cleared
        assert "1" not in result
        assert "2" not in result

    def test_clear_table(self):
        """Test clearing entire table."""
        table = PrettyTable()
        table.field_names = ["A", "B"]
        table.add_row([1, 2])
        table.clear()
        assert len(table.field_names) == 0


class TestAlignment:
    """Test text alignment features."""

    def test_left_alignment(self):
        """Test left alignment."""
        table = PrettyTable()
        table.field_names = ["Name", "Age"]
        table.add_row(["Alice", 30])
        table.align["Name"] = "l"
        result = table.get_string()
        assert len(result) > 0

    def test_center_alignment(self):
        """Test center alignment."""
        table = PrettyTable()
        table.field_names = ["Name", "Age"]
        table.add_row(["Alice", 30])
        table.align["Name"] = "c"
        result = table.get_string()
        assert len(result) > 0

    def test_right_alignment(self):
        """Test right alignment."""
        table = PrettyTable()
        table.field_names = ["Name", "Age"]
        table.add_row(["Alice", 30])
        table.align["Age"] = "r"
        result = table.get_string()
        assert len(result) > 0

    def test_mixed_alignment(self):
        """Test mixed alignment for different columns."""
        table = PrettyTable()
        table.field_names = ["Left", "Center", "Right"]
        table.add_row(["L", "C", "R"])
        table.align["Left"] = "l"
        table.align["Center"] = "c"
        table.align["Right"] = "r"
        result = table.get_string()
        assert len(result) > 0


class TestSorting:
    """Test sorting features."""

    def test_sort_by_column(self):
        """Test sorting by a specific column."""
        table = PrettyTable()
        table.field_names = ["Name", "Score"]
        table.add_row(["Alice", 85])
        table.add_row(["Bob", 92])
        table.add_row(["Charlie", 78])
        sorted_result = table.get_string(sortby="Score")
        assert "Charlie" in sorted_result

    def test_reverse_sort(self):
        """Test reverse sorting."""
        table = PrettyTable()
        table.field_names = ["Name", "Score"]
        table.add_row(["Alice", 85])
        table.add_row(["Bob", 92])
        table.add_row(["Charlie", 78])
        sorted_result = table.get_string(sortby="Score", reversesort=True)
        assert "Bob" in sorted_result


class TestBorderAndStyle:
    """Test border and styling features."""

    def test_border_on_off(self):
        """Test toggling borders."""
        table = PrettyTable()
        table.field_names = ["A", "B"]
        table.add_row([1, 2])
        
        table.border = False
        no_border = table.get_string()
        
        table.border = True
        with_border = table.get_string()
        
        # With border should be longer
        assert len(with_border) > len(no_border)

    def test_header_on_off(self):
        """Test toggling headers."""
        table = PrettyTable()
        table.field_names = ["A", "B"]
        table.add_row([1, 2])
        
        table.header = False
        no_header = table.get_string()
        
        table.header = True
        with_header = table.get_string()
        
        assert "A" not in no_header
        assert "A" in with_header

    def test_padding_width(self):
        """Test padding width settings."""
        table = PrettyTable()
        table.field_names = ["A", "B"]
        table.add_row([1, 2])
        table.padding_width = 2
        result = table.get_string()
        assert len(result) > 0


class TestMaxWidth:
    """Test maximum width settings."""

    def test_max_width_single_column(self):
        """Test setting max width for a single column."""
        table = PrettyTable()
        table.field_names = ["Long Text"]
        table.add_row(["This is a very long text that should be wrapped"])
        table.max_width["Long Text"] = 20
        result = table.get_string()
        assert len(result) > 0

    def test_max_width_multiple_columns(self):
        """Test setting max width for multiple columns."""
        table = PrettyTable()
        table.field_names = ["Col1", "Col2"]
        table.add_row(["Very long text here", "Another long text here"])
        table.max_width["Col1"] = 15
        table.max_width["Col2"] = 15
        result = table.get_string()
        assert len(result) > 0


class TestSlicing:
    """Test table slicing features."""

    def test_slice_single_row(self):
        """Test accessing a single row by index."""
        table = PrettyTable()
        table.field_names = ["Name", "Age"]
        table.add_row(["Alice", 30])
        table.add_row(["Bob", 25])
        table.add_row(["Charlie", 35])
        
        single_row = table[1]
        result = single_row.get_string()
        assert "Bob" in result

    def test_slice_range(self):
        """Test slicing a range of rows."""
        table = PrettyTable()
        table.field_names = ["Name", "Age"]
        table.add_row(["Alice", 30])
        table.add_row(["Bob", 25])
        table.add_row(["Charlie", 35])
        
        sliced = table[0:2]
        result = sliced.get_string()
        assert "Alice" in result
        assert "Bob" in result
