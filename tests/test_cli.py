"""Tests for CLI error handling."""

import json

from click.testing import CliRunner

from brc_schema.cli import main


def test_transmit_osti_missing_records_field(tmp_path):
    """transmit-osti should return a descriptive error for invalid input shape."""
    input_file = tmp_path / "invalid.json"
    input_file.write_text(json.dumps({"foo": []}), encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(main, ["transmit-osti", str(input_file)])

    assert result.exit_code != 0
    assert "missing required top-level 'records' field" in result.output
