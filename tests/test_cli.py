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


def test_retrieve_osti_site_defaults_to_both_sources(tmp_path, monkeypatch):
    """retrieve-osti-site should query legacy and E-Link 2.0 by default."""
    output_file = tmp_path / "site_records.json"
    captured = {}

    class FakeRetriever:
        def __init__(self, api_key=None, api_url=None, legacy_api_url=None):
            captured["api_key"] = api_key
            captured["api_url"] = api_url
            captured["legacy_api_url"] = legacy_api_url

        def save_records_by_site_code_to_file(self, **kwargs):
            captured.update(kwargs)
            output_data = {
                "retrieval_sources": [
                    {"api": "legacy", "record_count": 1},
                    {"api": "elink2", "record_count": 1},
                ],
                "records": [{"osti_id": "1"}, {"osti_id": 2}],
            }
            kwargs["output_path"].write_text(json.dumps(output_data), encoding="utf-8")
            return output_data

    monkeypatch.setattr("brc_schema.cli.OSTIRecordRetriever", FakeRetriever)

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "retrieve-osti-site",
            "--site-code",
            "glbrc",
            "--entry-date-start",
            "2026-01-01",
            "--limit",
            "3",
            "-o",
            str(output_file),
        ],
    )

    assert result.exit_code == 0, result.output
    assert captured["site_code"] == "glbrc"
    assert captured["sources"] == ("legacy", "elink2")
    assert captured["entry_date_start"] == "2026-01-01"
    assert captured["limit"] == 3
    assert captured["pretty"] is True
    assert "legacy=1, elink2=1" in result.output


def test_retrieve_osti_site_allows_source_selection(tmp_path, monkeypatch):
    """A caller can request only one origin API when needed."""
    captured = {}

    class FakeRetriever:
        def __init__(self, **kwargs):
            pass

        def save_records_by_site_code_to_file(self, **kwargs):
            captured.update(kwargs)
            return {
                "retrieval_sources": [{"api": "legacy", "record_count": 0}],
                "records": [],
            }

    monkeypatch.setattr("brc_schema.cli.OSTIRecordRetriever", FakeRetriever)

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "retrieve-osti-site",
            "--site-code",
            "CBI",
            "--source",
            "legacy",
            "-o",
            str(tmp_path / "records.json"),
        ],
    )

    assert result.exit_code == 0, result.output
    assert captured["sources"] == ("legacy",)
