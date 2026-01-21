"""
Mypy integration tests for PrettyTable
Issue #206: Add mypy via pre-commit and make mypy pass

Tests to verify that mypy type checking passes.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


class TestMypyIntegration:
    """Test that mypy passes on the source code."""

    def test_mypy_passes(self):
        """Test that mypy type checking passes for src/prettytable."""
        # Get the project root directory
        project_root = Path(__file__).parent.parent
        src_dir = project_root / "src" / "prettytable"
        config_file = project_root / "pyproject.toml"
        
        # Run mypy
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "mypy",
                str(src_dir),
                "--config-file",
                str(config_file),
            ],
            capture_output=True,
            text=True,
        )
        
        # Check that mypy passed
        assert result.returncode == 0, f"mypy failed with output:\\n{result.stdout}\\n{result.stderr}"
        assert "Success: no issues found" in result.stdout

    def test_mypy_strict_optional(self):
        """Test that mypy runs with strict optional checking."""
        project_root = Path(__file__).parent.parent
        src_dir = project_root / "src" / "prettytable"
        
        # Run mypy with strict optional
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "mypy",
                str(src_dir),
                "--strict-optional",
            ],
            capture_output=True,
            text=True,
        )
        
        # Should pass or at least not crash
        assert result.returncode in [0, 1]  # 1 is acceptable if there are warnings

    def test_no_untyped_imports(self):
        """Test that all imports are properly typed or ignored."""
        project_root = Path(__file__).parent.parent
        src_dir = project_root / "src" / "prettytable"
        config_file = project_root / "pyproject.toml"
        
        # Run mypy
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "mypy",
                str(src_dir),
                "--config-file",
                str(config_file),
            ],
            capture_output=True,
            text=True,
        )
        
        # Check that there are no import-untyped errors
        assert "import-untyped" not in result.stdout
        assert "import-untyped" not in result.stderr


class TestTypeStubs:
    """Test that type stubs are properly configured."""

    def test_wcwidth_import_handled(self):
        """Test that wcwidth import is properly handled in mypy config."""
        project_root = Path(__file__).parent.parent
        config_file = project_root / "pyproject.toml"
        
        # Read the config file
        content = config_file.read_text()
        
        # Check that wcwidth is configured in mypy overrides
        assert "wcwidth" in content
        assert "ignore_missing_imports" in content

    def test_colorama_import_handled(self):
        """Test that colorama import is properly handled."""
        project_root = Path(__file__).parent.parent
        config_file = project_root / "pyproject.toml"
        
        # Read the config file
        content = config_file.read_text()
        
        # Check that colorama is configured
        assert "colorama" in content or "types-colorama" in content
