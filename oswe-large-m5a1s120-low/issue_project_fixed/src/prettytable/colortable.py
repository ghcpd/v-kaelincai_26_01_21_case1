from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .prettytable import PrettyTable

if TYPE_CHECKING:
    # colorama is an optional runtime dependency; types provided via types-colorama
    from colorama import ansi  # noqa: F401

try:  # pragma: no cover - optional dependency
    from colorama import init as _colorama_init

    _colorama_init()
except Exception:  # noqa: BLE001 - we accept absence of colorama
    _colorama_init = None  # type: ignore[assignment]

RESET_CODE = "\x1b[0m"


class Theme:
    """Encapsulates ANSI color/style codes for table rendering."""

    def __init__(
        self,
        default_color: str = "",
        vertical_char: str = "|",
        vertical_color: str = "",
        horizontal_char: str = "-",
        horizontal_color: str = "",
        junction_char: str = "+",
        junction_color: str = "",
    ) -> None:
        self.default_color: str = Theme.format_code(default_color)
        self.vertical_char: str = vertical_char
        self.vertical_color: str = Theme.format_code(vertical_color)
        self.horizontal_char: str = horizontal_char
        self.horizontal_color: str = Theme.format_code(horizontal_color)
        self.junction_char: str = junction_char
        self.junction_color: str = Theme.format_code(junction_color)

    @staticmethod
    def format_code(s: str) -> str:
        """Return a normalized ANSI escape sequence (or empty string).

        If ``s`` is already an escape sequence, return as-is; otherwise wrap in
        ``\x1b[...m``. Empty/whitespace-only strings return "".
        """

        if s.strip() == "":
            return ""
        if s.startswith("\x1b["):
            return s
        return f"\x1b[{s}m"

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return (
            f"Theme(default_color={self.default_color!r}, vertical_char={self.vertical_char!r}, "
            f"vertical_color={self.vertical_color!r}, horizontal_char={self.horizontal_char!r}, "
            f"horizontal_color={self.horizontal_color!r}, junction_char={self.junction_char!r}, "
            f"junction_color={self.junction_color!r})"
        )


class Themes:
    DEFAULT = Theme()
    DYSLEXIA_FRIENDLY = Theme(
        default_color="38;5;223",
        vertical_color="38;5;22",
        horizontal_color="38;5;22",
        junction_color="38;5;58",
    )
    EARTH = Theme(
        default_color="33",
        vertical_color="38;5;94",
        horizontal_color="38;5;22",
        junction_color="38;5;130",
    )
    GLARE_REDUCTION = Theme(
        default_color="38;5;252",
        vertical_color="38;5;240",
        horizontal_color="38;5;240",
        junction_color="38;5;246",
    )
    HIGH_CONTRAST = Theme(
        default_color="97",
        vertical_color="91",
        horizontal_color="94",
        junction_color="93",
    )
    LAVENDER = Theme(
        default_color="38;5;183",
        vertical_color="35",
        horizontal_color="38;5;147",
        junction_color="38;5;219",
    )
    OCEAN = Theme(
        default_color="96",
        vertical_color="34",
        horizontal_color="34",
        junction_color="36",
    )
    OCEAN_DEEP = Theme(
        default_color="96",
        vertical_color="34",
        horizontal_color="36",
        junction_color="94",
    )
    PASTEL = Theme(
        default_color="38;5;223",
        vertical_color="38;5;152",
        horizontal_color="38;5;187",
        junction_color="38;5;157",
    )


class ColorTable(PrettyTable):
    """PrettyTable variant that applies ANSI colors/styles via a Theme."""

    def __init__(
        self,
        field_names: list[str] | tuple[str, ...] | None = None,
        *,
        theme: Theme | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(field_names=field_names, **kwargs)
        self.theme: Theme = theme or Themes.DEFAULT

    @property
    def theme(self) -> Theme:
        return self._theme

    @theme.setter
    def theme(self, value: Theme) -> None:
        self._theme = value
        self.update_theme()

    def update_theme(self) -> None:
        theme = self._theme

        self._vertical_char = (
            theme.vertical_color + theme.vertical_char + RESET_CODE + theme.default_color
        )

        self._horizontal_char = (
            theme.horizontal_color + theme.horizontal_char + RESET_CODE + theme.default_color
        )

        self._junction_char = (
            theme.junction_color + theme.junction_char + RESET_CODE + theme.default_color
        )

    def get_string(self, **kwargs: Any) -> str:
        # Append a trailing reset so downstream renderings do not leak styles
        return super().get_string(**kwargs) + RESET_CODE
