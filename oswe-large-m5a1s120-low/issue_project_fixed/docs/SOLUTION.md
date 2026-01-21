# SOLUTION — PrettyTable Issue #206 (mypy fixes)

## 🧩 Problem Analysis
- Original `mypy src/prettytable` failed primarily due to **missing stubs** for `wcwidth` and `colorama`.
- `prettytable.py` used `TYPE_CHECKING = False` instead of `typing.TYPE_CHECKING`, risking missing type imports and hiding type info.
- Several internal helpers/validators/callbacks lacked annotations, triggering `--strict` complaints (`no-untyped-def`, `no-untyped-call`).
- Internal state dicts (`align`, `valign`, `min_width`, `max_width`, formatting dicts) had loose/implicit types, causing optional vs. required type mismatches.

## 🎯 Goals
- Achieve **zero mypy errors under `--strict`** while preserving public API and behavior.
- Provide **stub coverage** for third-party deps (`wcwidth`, `colorama`).
- Improve **developer ergonomics** (IDE hints, py.typed marker) without breaking compatibility.

## 🛠️ Fix Approach
1. **Type stub coverage**
   - Added `wcwidth-stubs` and `types-colorama` to `requirements.txt` (and `optional-dependencies.typecheck` in `pyproject.toml`).
   - Kept runtime dependency on `wcwidth`; `colorama` remains optional (Windows-only) but is safely typed.

2. **Type import hygiene**
   - Replaced `TYPE_CHECKING = False` with `from typing import TYPE_CHECKING` and moved type-only imports (`SupportsRichComparison`, `Self`) behind the guard.
   - Imported `Callable`, `Sequence`, `Mapping`, `Final`, `TypeAlias`, `IO` at top-level for clarity.

3. **Annotate internals**
   - Added `@property` return types and setter annotations across the board (`align`, `valign`, `none_format`, `int_format`, `float_format`, `min_width`, `max_width`, etc.).
   - Typed all validator helpers (`_validate_option`, `_validate_*`) and callbacks (`_align_callback`, `_valign_callback`, `_remove_custom_format_callback`, `_custom_format_callback`).
   - Typed `_format_value` to ensure formatter returns `str` and avoid `Any` leakage.
   - Annotated factory functions (`from_csv`, `from_db_cursor`, `from_json`, `from_html*`, `from_mediawiki`) and `TableHandler` for HTML parsing.

4. **Normalize internal dict types**
   - Ensured `align`/`valign` dictionaries store **only literals** (`"l"|"c"|"r"`, `"t"|"m"|"b"`).
   - `min_width`/`max_width` now consistently `dict[str, int]` (validation supports `int|dict|None`).
   - `int_format`/`float_format` now `dict[str, str]`; `none_format` allows `None` per-field.

5. **ColorTable typing**
   - Added explicit types for `Theme` fields and `ColorTable` constructor (`field_names`, `theme`, `**kwargs`).
   - Optional `colorama` import guarded; stubs ensure mypy friendliness.
   - Ensured trailing ANSI reset appended (`RESET_CODE`) to avoid leaking styles.

6. **py.typed marker**
   - Added `src/prettytable/py.typed` so mypy/IDEs treat package as typed.

7. **Tests & type assertions**
   - Migrated original functional tests to `pytest` (`tests/test_basic.py`).
   - Added `tests/test_types.py` with `typing_extensions.assert_type` and a `mypy.api.run` invocation to enforce type-check on the package in CI.

## ✅ Results
- `python -m mypy src/prettytable` → **Success: no issues found** under `--strict` (config in `pyproject.toml`).
- `pytest` → all functional and type tests pass.
- `python demo.py` → renders tables correctly with formatting, sorting, alignment, and color themes.
- Public API unchanged; backward compatibility preserved (deprecated names still routed via `__getattr__` in `__init__.py`).

## 🤔 Challenges & Resolutions
- **Editable installs with hatchling**: `pip install -e .` can fail with `prepare_metadata_for_build_editable`. Workaround: use non-editable install (`pip install .`) or set `PYTHONPATH=src` when running tools.
- **Optional dependencies**: `colorama` is optional; ensured try/except import with stubs to satisfy mypy without forcing runtime dependency on non-Windows platforms.
- **Validator flexibility**: Some validators needed to accept both `int` and `dict[str,int]` inputs. Adjusted Type hints and logic to iterate mappings safely.

## 📌 Key Code Snippets
- **Type-safe formatter**
  ```py
  def _format_value(self, field: str, value: Any) -> str:
      if isinstance(value, int) and field in self._int_format:
          return (f"%{self._int_format[field]}d") % value
      if isinstance(value, float) and field in self._float_format:
          return (f"%{self._float_format[field]}f") % value
      formatter: Callable[[str, Any], str] = self._custom_format.get(field, lambda f, v: str(v))
      return formatter(field, value)
  ```

- **Validator accepting dict/int/None**
  ```py
  def _validate_nonnegative_int(self, name: str, val: int | Mapping[str, int] | None) -> None:
      if val is None:
          return
      if isinstance(val, Mapping):
          for k, v in val.items():
              self._validate_nonnegative_int(f"{name}.{k}", v)
          return
      try:
          assert int(val) >= 0
      except Exception:
          raise ValueError(f"Invalid value for {name}: {val}")
  ```

## 🛡️ Backward Compatibility
- Deprecated constants and names still routed via `_warn_deprecation` in `__init__.py`.
- No public API signature changes; only added type annotations and internal normalization.

## 📚 References
- Issue: https://github.com/prettytable/prettytable/issues/206
- Related PRs: #205 (type hints), #218 (mypy config)
- Typing refs: PEP 484, PEP 563, mypy docs

---
**Assistant:** GitHub Copilot (model: vscswe-d64-mix5-arm1-s120)
