"""Tests that verify StrEnum compatibility handling does not pollute the
global ``enum`` module and that StrEnum-based choices work on Python 3.11+.
"""
from __future__ import annotations

import enum
import sys

import pytest

import click

_has_str_enum = sys.version_info >= (3, 11)


@pytest.mark.skipif(not _has_str_enum, reason="StrEnum requires Python 3.11+")
def test_enum_module_not_monkey_patched():
    """On Python 3.11+, ``enum.StrEnum`` must be the real stdlib class,
    not ``enum.Enum`` injected by a test-time monkey-patch."""
    # Force import of test_options to trigger any side effects
    import tests.test_options  # noqa: F401

    assert enum.StrEnum is not enum.Enum


@pytest.mark.skipif(not _has_str_enum, reason="StrEnum requires Python 3.11+")
def test_strenum_choice_works(runner):
    """StrEnum choices should accept member names on the command line."""

    class Color(enum.StrEnum):
        RED = "red"
        GREEN = "green"
        BLUE = "blue"

    @click.command()
    @click.option("-c", type=click.Choice(Color))
    def cli(c):
        click.echo(f"color={c.value}")

    result = runner.invoke(cli, ["-c", "RED"])
    assert result.exit_code == 0
    assert "color=red" in result.output
