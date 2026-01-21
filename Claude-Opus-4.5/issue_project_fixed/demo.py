"""
Demo script: Demonstrates basic PrettyTable functionality
Issue #206: Add mypy via pre-commit and make mypy pass

This script demonstrates that PrettyTable functionality works correctly
after adding type annotations and fixing mypy errors.
"""
from __future__ import annotations

from prettytable import PrettyTable


def demo_basic_table() -> None:
    """Create a basic table."""
    print("=" * 60)
    print("Demo 1: Basic Table")
    print("=" * 60)
    
    table = PrettyTable()
    table.field_names = ["City name", "Area", "Population", "Annual Rainfall"]
    table.add_row(["Adelaide", 1295, 1158259, 600.5])
    table.add_row(["Brisbane", 5905, 1857594, 1146.4])
    table.add_row(["Darwin", 112, 120900, 1714.7])
    table.add_row(["Hobart", 1357, 205556, 619.5])
    
    print(table)
    print()


def demo_alignment() -> None:
    """Demonstrate alignment features."""
    print("=" * 60)
    print("Demo 2: Alignment Settings")
    print("=" * 60)
    
    table = PrettyTable()
    table.field_names = ["Name", "Age", "City"]
    table.add_row(["Alice", 30, "New York"])
    table.add_row(["Bob", 25, "Los Angeles"])
    table.add_row(["Charlie", 35, "Chicago"])
    
    # Set alignment
    table.align["Name"] = "l"  # Left align
    table.align["Age"] = "r"   # Right align
    table.align["City"] = "c"  # Center align
    
    print(table)
    print()


def demo_sorting() -> None:
    """Demonstrate sorting features."""
    print("=" * 60)
    print("Demo 3: Sorting")
    print("=" * 60)
    
    table = PrettyTable()
    table.field_names = ["Name", "Score"]
    table.add_row(["Alice", 85])
    table.add_row(["Bob", 92])
    table.add_row(["Charlie", 78])
    table.add_row(["David", 95])
    
    print("Original order:")
    print(table)
    print()
    
    print("Sorted by Score (descending):")
    print(table.get_string(sortby="Score", reversesort=True))
    print()


def demo_styling() -> None:
    """Demonstrate styling features."""
    print("=" * 60)
    print("Demo 4: Styling")
    print("=" * 60)
    
    table = PrettyTable()
    table.field_names = ["Item", "Price"]
    table.add_row(["Apple", "$1.50"])
    table.add_row(["Banana", "$0.75"])
    table.add_row(["Orange", "$1.25"])
    
    # Set border style
    table.border = True
    table.header = True
    table.padding_width = 2
    
    print(table)
    print()


def demo_html_output() -> None:
    """Demonstrate HTML output."""
    print("=" * 60)
    print("Demo 5: HTML Output")
    print("=" * 60)
    
    table = PrettyTable()
    table.field_names = ["Language", "Creator"]
    table.add_row(["Python", "Guido van Rossum"])
    table.add_row(["Java", "James Gosling"])
    table.add_row(["C++", "Bjarne Stroustrup"])
    
    print(table.get_html_string())
    print()


if __name__ == "__main__":
    print("PrettyTable Issue #206 Demo")
    print("Demonstrating basic functionality after mypy type fixes")
    print()
    
    demo_basic_table()
    demo_alignment()
    demo_sorting()
    demo_styling()
    demo_html_output()
    
    print("=" * 60)
    print("All demos completed successfully!")
    print("Next step: Run 'mypy src/prettytable' to verify type checking passes")
    print("=" * 60)
