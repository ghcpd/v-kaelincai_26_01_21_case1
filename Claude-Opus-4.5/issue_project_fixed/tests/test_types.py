"""
Test suite for PrettyTable type annotations
Issue #206: Add mypy via pre-commit and make mypy pass

This test module verifies that type annotations work correctly
and the module passes mypy type checking.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from prettytable import (
    PrettyTable,
    HRuleStyle,
    VRuleStyle,
    TableStyle,
    from_csv,
    from_html,
    from_html_one,
    from_json,
)


class TestTypeAnnotations:
    """Tests to verify type annotations are correct and usable."""

    def test_prettytable_init_types(self) -> None:
        """Test PrettyTable initialization accepts correct types."""
        # Test with no arguments
        table1 = PrettyTable()
        assert table1 is not None

        # Test with field_names as list
        table2 = PrettyTable(["A", "B", "C"])
        assert len(table2.field_names) == 3

        # Test with keyword arguments
        table3 = PrettyTable(field_names=["X", "Y"], border=True, header=True)
        assert table3.border is True

    def test_hrule_style_enum(self) -> None:
        """Test HRuleStyle enum values."""
        assert HRuleStyle.FRAME == 0
        assert HRuleStyle.ALL == 1
        assert HRuleStyle.NONE == 2
        assert HRuleStyle.HEADER == 3

    def test_vrule_style_enum(self) -> None:
        """Test VRuleStyle enum values."""
        assert VRuleStyle.FRAME == 0
        assert VRuleStyle.ALL == 1
        assert VRuleStyle.NONE == 2

    def test_table_style_enum(self) -> None:
        """Test TableStyle enum values."""
        assert TableStyle.DEFAULT == 10
        assert TableStyle.MSWORD_FRIENDLY == 11
        assert TableStyle.MARKDOWN == 13

    def test_align_type(self) -> None:
        """Test alignment types."""
        table = PrettyTable()
        table.field_names = ["Name", "Value"]
        
        # Valid alignment values
        table.align["Name"] = "l"
        table.align["Value"] = "c"
        
        assert table.align["Name"] == "l"
        assert table.align["Value"] == "c"

    def test_valign_type(self) -> None:
        """Test vertical alignment types."""
        table = PrettyTable()
        table.field_names = ["Name", "Value"]
        
        # Valid vertical alignment values
        table.valign["Name"] = "t"
        table.valign["Value"] = "m"
        
        assert table.valign["Name"] == "t"
        assert table.valign["Value"] == "m"

    def test_get_string_return_type(self) -> None:
        """Test get_string returns str."""
        table = PrettyTable()
        table.field_names = ["A"]
        table.add_row([1])
        
        result = table.get_string()
        assert isinstance(result, str)

    def test_get_html_string_return_type(self) -> None:
        """Test get_html_string returns str."""
        table = PrettyTable()
        table.field_names = ["A"]
        table.add_row([1])
        
        result = table.get_html_string()
        assert isinstance(result, str)

    def test_rows_property_type(self) -> None:
        """Test rows property returns list."""
        table = PrettyTable()
        table.field_names = ["A", "B"]
        table.add_row([1, 2])
        
        rows = table.rows
        assert isinstance(rows, list)
        assert len(rows) == 1

    def test_field_names_property_type(self) -> None:
        """Test field_names property returns list."""
        table = PrettyTable()
        table.field_names = ["A", "B", "C"]
        
        names = table.field_names
        assert isinstance(names, list)
        assert len(names) == 3

    def test_custom_format_callable(self) -> None:
        """Test custom_format accepts callable."""
        table = PrettyTable()
        table.field_names = ["Price"]
        table.add_row([1234.56])
        
        def format_currency(field: str, value) -> str:
            return f"${value:,.2f}"
        
        table.custom_format = format_currency
        result = table.get_string()
        assert "$1,234.56" in result


class TestMypyIntegration:
    """Tests to verify mypy passes on the codebase."""

    def test_mypy_passes(self) -> None:
        """Test that mypy passes on the prettytable source code."""
        src_path = Path(__file__).parent.parent / "src" / "prettytable"
        
        result = subprocess.run(
            [sys.executable, "-m", "mypy", str(src_path)],
            capture_output=True,
            text=True,
        )
        
        # Check if mypy passed (return code 0) or show the error
        assert result.returncode == 0, f"mypy failed:\n{result.stdout}\n{result.stderr}"


class TestFromFactories:
    """Tests for factory functions type handling."""

    def test_from_html_returns_list(self) -> None:
        """Test from_html returns list of PrettyTable."""
        html = """
        <table>
            <tr><th>A</th><th>B</th></tr>
            <tr><td>1</td><td>2</td></tr>
        </table>
        """
        tables = from_html(html)
        assert isinstance(tables, list)
        if tables:
            assert isinstance(tables[0], PrettyTable)

    def test_from_html_one_returns_table(self) -> None:
        """Test from_html_one returns PrettyTable."""
        html = """
        <table>
            <tr><th>A</th><th>B</th></tr>
            <tr><td>1</td><td>2</td></tr>
        </table>
        """
        table = from_html_one(html)
        assert isinstance(table, PrettyTable)

    def test_from_json_returns_table(self) -> None:
        """Test from_json returns PrettyTable."""
        import json
        
        data = [["A", "B"], {"A": 1, "B": 2}]
        json_str = json.dumps(data)
        
        table = from_json(json_str)
        assert isinstance(table, PrettyTable)
