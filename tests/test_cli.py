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


def test_transmit_osti_limit_zero_is_respected(tmp_path, monkeypatch):
    """transmit-osti should treat --limit 0 as processing zero records."""
    input_file = tmp_path / "input.yaml"
    input_file.write_text(
        "records:\n  - title: Test Dataset\n", encoding="utf-8")

    captured = {}

    class FakeTransmitter:
        def __init__(self, api_key=None, api_url=None, dry_run=False):
            self.record_limit = None
            self.skip_urls = ""
            self.new_only = False

        def post_records(self, records):
            captured["record_limit"] = self.record_limit
            captured["records"] = records

            class Summary:
                new_count = 0
                update_count = 0
                fail_count = 0
                skip_count = 0

                @staticmethod
                def message():
                    return "Transmit Summary - New: 0, Updated: 0, Skipped: 0, Failed: 0"

                @staticmethod
                def failures():
                    return []

            return Summary()

    monkeypatch.setattr(
        "brc_schema.cli.OSTIRecordTransmitter", FakeTransmitter)

    runner = CliRunner()
    result = runner.invoke(
        main, ["transmit-osti", "--dry-run", "--limit", "0", str(input_file)])

    assert result.exit_code == 0, result.output
    assert captured["record_limit"] == 0
    assert len(captured["records"]) == 1
