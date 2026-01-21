"""
Demo script showcasing PrettyTable basic functionality after mypy fixes.
"""

from prettytable import PrettyTable
from prettytable.colortable import ColorTable, Themes


def demo_basic_table() -> None:
    print("=" * 60)
    print("Demo 1: Basic table")
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
    print("=" * 60)
    print("Demo 2: Alignment")
    print("=" * 60)

    table = PrettyTable()
    table.field_names = ["Name", "Age", "City"]
    table.add_row(["Alice", 30, "New York"])
    table.add_row(["Bob", 25, "Los Angeles"])
    table.add_row(["Charlie", 35, "Chicago"])

    table.align["Name"] = "l"
    table.align["Age"] = "r"
    table.align["City"] = "c"

    print(table)
    print()


def demo_sorting() -> None:
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

    print("Sorted by Score descending:")
    print(table.get_string(sortby="Score", reversesort=True))
    print()


def demo_styling() -> None:
    print("=" * 60)
    print("Demo 4: Styling")
    print("=" * 60)

    table = PrettyTable()
    table.field_names = ["Item", "Price"]
    table.add_row(["Apple", "$1.50"])
    table.add_row(["Banana", "$0.75"])
    table.add_row(["Orange", "$1.25"])

    table.border = True
    table.header = True
    table.padding_width = 2

    print(table)
    print()


def demo_color_table() -> None:
    print("=" * 60)
    print("Demo 5: ColorTable themes")
    print("=" * 60)

    table = ColorTable()
    table.field_names = ["Name", "Value"]
    table.add_row(["Foo", 1])
    table.add_row(["Bar", 2])

    from prettytable.colortable import Theme  # local import to avoid cycles in typing

    for theme_name, theme in vars(Themes).items():
        if isinstance(theme, Theme):
            table.theme = theme
            print(f"Theme: {theme_name}")
            print(table)
            print()


if __name__ == "__main__":
    print("PrettyTable Issue #206 Demo")
    print()
    demo_basic_table()
    demo_alignment()
    demo_sorting()
    demo_styling()
    demo_color_table()
    print("=" * 60)
    print("Demo complete! Run `mypy src/prettytable` and `pytest` to verify.")
    print("=" * 60)
