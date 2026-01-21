# Solution Documentation

## Issue #206: Add mypy via pre-commit and make mypy pass

### Problem Analysis

#### Original Error Messages

When running `mypy src/prettytable` on the original code, the following errors were reported:

```
src\prettytable\prettytable.py:3030: error: Skipping analyzing "wcwidth": module is installed, but missing library stubs or py.typed marker  [import-untyped]
        import wcwidth
    ^
src\prettytable\colortable.py:6: error: Library stubs not installed for "colorama"  [import-untyped]
        from colorama import init
    ^
Found 2 errors in 2 files (checked 5 source files)
```

#### Root Cause

The errors occur because:

1. **wcwidth** - This library provides Unicode character width calculations. It does not include type stubs (`.pyi` files) or a `py.typed` marker file, so mypy cannot verify type safety of imports from this module.

2. **colorama** - This library provides cross-platform colored terminal text. While type stubs exist (`types-colorama`), they may not be installed. The library itself doesn't include inline type annotations.

These are **not bugs in the PrettyTable code** - the code functions correctly. The issue is that mypy's strict checking flags imports from untyped third-party libraries as errors by default.

### Solution Approach

There are several ways to handle untyped third-party library imports:

1. **Install type stubs** (if available) - e.g., `pip install types-colorama`
2. **Use inline `# type: ignore` comments** - Ignore specific imports
3. **Configure mypy to ignore specific modules** - Global configuration
4. **Create stub files** - Write `.pyi` files for the libraries

For this fix, we used the **mypy configuration approach**:

#### Mypy Configuration in pyproject.toml

We updated `pyproject.toml` with mypy overrides to tell mypy to ignore missing imports from specific modules:

```toml
[tool.mypy]
python_version = "3.10"
pretty = true
# ... other settings ...

# Ignore missing stubs for third-party libraries
[[tool.mypy.overrides]]
module = [
  "wcwidth",
  "colorama",
]
ignore_missing_imports = true
```

This configuration tells mypy: "When checking imports from `wcwidth` or `colorama`, don't report errors about missing type information."

### Why This Approach?

1. **Minimal Code Changes**: No changes to source files needed - only configuration
2. **Preserves Type Safety**: All other code remains fully type-checked
3. **Centralized Configuration**: All mypy settings in one place (pyproject.toml)
4. **Future-Proof**: If these libraries add type stubs later, just remove the override
5. **No New Dependencies**: Doesn't require installing additional type stub packages
6. **Clean Code**: No inline comments cluttering the source code

### Alternative Approaches Considered

1. **Installing types-colorama**
   - Pro: Provides full type checking for colorama
   - Con: Adds a dependency; types-colorama may not be available for all Python versions

2. **Creating custom stub files**
   - Pro: Full control over type definitions
   - Con: Maintenance burden; need to update when libraries change

3. **Using `--ignore-missing-imports` flag**
   - Pro: Simple command-line fix
   - Con: Too broad; ignores ALL missing imports, reducing type safety

### Verification

After applying the fixes:

```bash
$ mypy src/prettytable
Success: no issues found in 5 source files
```

All 5 source files are now checked:
- `__init__.py`
- `__main__.py`
- `_version.py`
- `colortable.py`
- `prettytable.py`

### Lessons Learned

1. **Third-party library typing is improving but incomplete** - Many popular libraries still lack type stubs
2. **Targeted ignores are better than global suppression** - Use specific error codes like `[import-untyped]`
3. **Configuration and code-level ignores complement each other** - Both approaches have valid use cases
4. **Type checking is about trade-offs** - Sometimes ignoring specific errors is the pragmatic solution

### References

- [GitHub Issue #206](https://github.com/prettytable/prettytable/issues/206)
- [mypy Documentation - Missing Imports](https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports)
- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [PEP 561 - Distributing and Packaging Type Information](https://www.python.org/dev/peps/pep-0561/)
